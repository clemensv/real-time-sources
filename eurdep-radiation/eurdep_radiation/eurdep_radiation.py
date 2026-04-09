"""EURDEP (European Radiological Data Exchange Platform) bridge to Kafka.

Fetches ambient gamma dose rate measurements from ~5,500 stations across
39 European countries via the IMIS WFS endpoint and forwards them as
CloudEvents to a Kafka topic.
"""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
from confluent_kafka import Producer
from eurdep_radiation_producer_data.eu.jrc.eurdep.station import Station
from eurdep_radiation_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading
from eurdep_radiation_producer_kafka_producer.producer import EuJrcEurdepEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

WFS_BASE = "https://www.imis.bfs.de/ogc/opendata/ows"
FEED_URL = "https://www.imis.bfs.de/ogc/opendata/ows"

WFS_PARAMS_BASE = {
    "service": "WFS",
    "version": "1.1.0",
    "request": "GetFeature",
    "typeName": "opendata:eurdep_latestValue",
    "outputFormat": "application/json",
}

PAGE_SIZE = 1000


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


class EurdepAPI:
    """Client for the EURDEP WFS data interface."""

    def __init__(self):
        self.session = requests.Session()

    def fetch_all_features(self) -> List[Dict[str, Any]]:
        """Fetch all EURDEP features with WFS pagination."""
        all_features: List[Dict[str, Any]] = []
        start_index = 0
        while True:
            params = {
                **WFS_PARAMS_BASE,
                "maxFeatures": str(PAGE_SIZE),
                "startIndex": str(start_index),
            }
            resp = self.session.get(WFS_BASE, params=params, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            features = data.get("features", [])
            all_features.extend(features)
            if len(features) < PAGE_SIZE:
                break
            start_index += PAGE_SIZE
        return all_features

    @staticmethod
    def extract_stations(features: List[Dict[str, Any]]) -> Dict[str, Station]:
        """Extract deduplicated station reference data from features."""
        stations: Dict[str, Station] = {}
        for feature in features:
            props = feature.get("properties", {})
            station_id = props.get("id", "")
            if not station_id or station_id in stations:
                continue
            geom = feature.get("geometry") or {}
            coords = geom.get("coordinates", [None, None])
            country_code = station_id[:2] if len(station_id) >= 2 else ""
            stations[station_id] = Station(
                station_id=station_id,
                name=props.get("name", ""),
                country_code=country_code,
                latitude=coords[1] if coords[1] is not None else 0.0,
                longitude=coords[0] if coords[0] is not None else 0.0,
                height_above_sea=props.get("height_above_sea"),
                site_status=props.get("site_status", 0),
                site_status_text=props.get("site_status_text", ""),
            )
        return stations

    @staticmethod
    def extract_readings(features: List[Dict[str, Any]]) -> List[DoseRateReading]:
        """Extract dose rate readings, keeping only the shortest analyzed_range per station+end_measure."""
        # Group features by (station_id, end_measure) and keep the shortest analyzed_range_in_h
        best: Dict[Tuple[str, str], Dict[str, Any]] = {}
        for feature in features:
            props = feature.get("properties", {})
            station_id = props.get("id", "")
            end_measure = props.get("end_measure", "")
            if not station_id or not end_measure:
                continue
            key = (station_id, end_measure)
            analyzed_range = props.get("analyzed_range_in_h")
            if analyzed_range is None:
                analyzed_range = 9999
            if key not in best or analyzed_range < best[key].get("_analyzed_range", 9999):
                best[key] = {**props, "_analyzed_range": analyzed_range, "_feature": feature}

        readings: List[DoseRateReading] = []
        for entry in best.values():
            props = entry
            readings.append(DoseRateReading(
                station_id=props.get("id", ""),
                name=props.get("name", ""),
                value=props.get("value"),
                unit=props.get("unit", ""),
                start_measure=props.get("start_measure", ""),
                end_measure=props.get("end_measure", ""),
                nuclide=props.get("nuclide", ""),
                duration=props.get("duration", ""),
                validated=props.get("validated", 0),
            ))
        return readings


def _parse_connection_string(connection_string: str):
    """Parse the connection string and extract Kafka config and topic."""
    config_dict = {}
    kafka_topic = None
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                kafka_topic = part.split("=")[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict, kafka_topic


def feed(args):
    """Main feed loop: emit stations then poll for dose rate readings."""
    connection_string = args.connection_string or os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logging.error("CONNECTION_STRING is required")
        sys.exit(1)

    kafka_config, kafka_topic = _parse_connection_string(connection_string)

    tls_enabled = os.environ.get("KAFKA_ENABLE_TLS", "true").lower()
    if tls_enabled == "false" and "security.protocol" not in kafka_config:
        kafka_config["security.protocol"] = "PLAINTEXT"

    polling_interval = int(args.polling_interval or os.environ.get("POLLING_INTERVAL", "3600"))
    state_file = args.state_file or os.environ.get("STATE_FILE", "")

    previous_readings: Dict[str, str] = _load_state(state_file)

    producer = Producer(kafka_config)
    event_producer = EuJrcEurdepEventProducer(producer, kafka_topic)
    api = EurdepAPI()

    logging.info(
        "Starting EURDEP feed to Kafka topic %s at %s",
        kafka_topic,
        kafka_config.get("bootstrap.servers", "?"),
    )

    # Fetch all features once for initial reference + telemetry emission
    features = api.fetch_all_features()
    logging.info("Fetched %d features from EURDEP WFS", len(features))

    # Emit station reference data
    stations = api.extract_stations(features)
    for station in stations.values():
        try:
            event_producer.send_eu_jrc_eurdep_station(
                _feedurl=FEED_URL,
                _station_id=station.station_id,
                data=station,
                flush_producer=False,
            )
        except Exception as e:
            logging.error("Error sending station %s: %s", station.station_id, e)
    producer.flush()
    logging.info("Sent %d station records", len(stations))

    last_reference_emit = datetime.now(timezone.utc)

    # Telemetry polling loop
    while True:
        try:
            count = 0
            start_time = datetime.now(timezone.utc)

            # Re-fetch reference data every 6 hours
            if (start_time - last_reference_emit).total_seconds() >= 21600:
                features = api.fetch_all_features()
                stations = api.extract_stations(features)
                for station in stations.values():
                    try:
                        event_producer.send_eu_jrc_eurdep_station(
                            _feedurl=FEED_URL,
                            _station_id=station.station_id,
                            data=station,
                            flush_producer=False,
                        )
                    except Exception as e:
                        logging.error("Error sending station %s: %s", station.station_id, e)
                producer.flush()
                logging.info("Refreshed %d station records", len(stations))
                last_reference_emit = start_time
            else:
                features = api.fetch_all_features()

            readings = api.extract_readings(features)
            for reading in readings:
                dedup_key = f"{reading.station_id}|{reading.end_measure}"
                if dedup_key in previous_readings:
                    continue
                try:
                    event_producer.send_eu_jrc_eurdep_dose_rate_reading(
                        _feedurl=FEED_URL,
                        _station_id=reading.station_id,
                        data=reading,
                        flush_producer=False,
                    )
                    count += 1
                    previous_readings[dedup_key] = reading.end_measure
                except Exception as e:
                    logging.error("Error sending reading for %s: %s", reading.station_id, e)
            producer.flush()
            end_time = datetime.now(timezone.utc)
            elapsed = (end_time - start_time).total_seconds()
            effective_interval = max(0, polling_interval - elapsed)
            logging.info(
                "Sent %d dose rate readings in %.1f s. Next poll at %s.",
                count,
                elapsed,
                (datetime.now(timezone.utc) + timedelta(seconds=effective_interval)).isoformat(),
            )
            _save_state(state_file, previous_readings)
            if effective_interval > 0:
                time.sleep(effective_interval)
        except KeyboardInterrupt:
            logging.info("Exiting...")
            break
        except Exception as e:
            logging.error("Error occurred: %s", e)
            logging.info("Retrying in %d seconds...", polling_interval)
            time.sleep(polling_interval)


def main():
    parser = argparse.ArgumentParser(description="EURDEP radiation bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Start the feed loop")
    feed_parser.add_argument("--connection-string", help="Kafka connection string")
    feed_parser.add_argument("--polling-interval", type=int, default=3600, help="Polling interval in seconds (default: 3600)")
    feed_parser.add_argument("--state-file", help="Path to state persistence file")

    args = parser.parse_args()
    if args.command == "feed":
        feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
