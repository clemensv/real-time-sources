"""BfS ODL (Ortsdosisleistung) gamma dose rate bridge to Kafka."""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests
from confluent_kafka import Producer
from bfs_odl_producer_data.de.bfs.odl.station import Station
from bfs_odl_producer_data.de.bfs.odl.doseratemeasurement import DoseRateMeasurement
from bfs_odl_producer_kafka_producer.producer import DeBfsOdlEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

WFS_BASE = "https://www.imis.bfs.de/ogc/opendata/ows"
FEED_URL = "https://odlinfo.bfs.de"

# WFS parameters for the ODL layers
WFS_PARAMS_BASE = {
    "service": "WFS",
    "version": "1.1.0",
    "request": "GetFeature",
    "outputFormat": "application/json",
}


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


class BfsOdlAPI:
    """Client for the BfS ODL WFS data interface."""

    def __init__(self):
        self.session = requests.Session()

    def fetch_stations(self) -> List[Dict[str, Any]]:
        """Fetch all station metadata from the odlinfo_sitelist layer."""
        params = {**WFS_PARAMS_BASE, "typeName": "opendata:odlinfo_sitelist"}
        resp = self.session.get(WFS_BASE, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("features", [])

    def fetch_latest_measurements(self) -> List[Dict[str, Any]]:
        """Fetch the latest 1-hour dose rate readings for all stations."""
        params = {**WFS_PARAMS_BASE, "typeName": "opendata:odlinfo_odl_1h_latest"}
        resp = self.session.get(WFS_BASE, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("features", [])

    @staticmethod
    def parse_station(feature: Dict[str, Any]) -> Station:
        """Convert a GeoJSON feature from odlinfo_sitelist to a Station data class."""
        props = feature["properties"]
        geom = feature.get("geometry") or {}
        coords = geom.get("coordinates", [None, None])
        return Station(
            station_id=props["kenn"],
            station_code=props.get("id", ""),
            name=props.get("name", ""),
            postal_code=props.get("plz", ""),
            site_status=props.get("site_status", 0),
            site_status_text=props.get("site_status_text", ""),
            kid=props.get("kid", 0),
            height_above_sea=props.get("height_above_sea"),
            longitude=coords[0] if coords[0] is not None else 0.0,
            latitude=coords[1] if coords[1] is not None else 0.0,
        )

    @staticmethod
    def parse_measurement(feature: Dict[str, Any]) -> DoseRateMeasurement:
        """Convert a GeoJSON feature from odlinfo_odl_1h_latest to a DoseRateMeasurement."""
        props = feature["properties"]
        return DoseRateMeasurement(
            station_id=props["kenn"],
            start_measure=props.get("start_measure", ""),
            end_measure=props.get("end_measure", ""),
            value=props.get("value"),
            value_cosmic=props.get("value_cosmic"),
            value_terrestrial=props.get("value_terrestrial"),
            validated=props.get("validated", 0),
            nuclide=props.get("nuclide", ""),
        )


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
    """Main feed loop: emit stations then poll for dose rate measurements."""
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
    event_producer = DeBfsOdlEventProducer(producer, kafka_topic)
    api = BfsOdlAPI()

    logging.info(
        "Starting BfS ODL feed to Kafka topic %s at %s",
        kafka_topic,
        kafka_config["bootstrap.servers"],
    )

    # Emit station reference data
    stations = api.fetch_stations()
    for feature in stations:
        try:
            station = api.parse_station(feature)
            event_producer.send_de_bfs_odl_station(
                _feedurl=FEED_URL,
                _station_id=station.station_id,
                data=station,
                flush_producer=False,
            )
        except Exception as e:
            logging.error("Error sending station %s: %s", feature.get("properties", {}).get("kenn", "?"), e)
    producer.flush()
    logging.info("Sent %d station records", len(stations))

    # Telemetry polling loop
    while True:
        try:
            count = 0
            start_time = datetime.now(timezone.utc)
            measurements = api.fetch_latest_measurements()
            for feature in measurements:
                props = feature.get("properties", {})
                kenn = props.get("kenn", "")
                end_measure = props.get("end_measure", "")
                # Deduplicate: skip if we already sent this station's reading for the same period
                if kenn in previous_readings and previous_readings[kenn] == end_measure:
                    continue
                try:
                    measurement = api.parse_measurement(feature)
                    event_producer.send_de_bfs_odl_dose_rate_measurement(
                        _feedurl=FEED_URL,
                        _station_id=measurement.station_id,
                        data=measurement,
                        flush_producer=False,
                    )
                    count += 1
                    previous_readings[kenn] = end_measure
                except Exception as e:
                    logging.error("Error sending measurement for %s: %s", kenn, e)
            producer.flush()
            end_time = datetime.now(timezone.utc)
            elapsed = (end_time - start_time).total_seconds()
            effective_interval = max(0, polling_interval - elapsed)
            logging.info(
                "Sent %d dose rate measurements in %.1f s. Next poll at %s.",
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
    parser = argparse.ArgumentParser(description="BfS ODL gamma dose rate bridge to Kafka")
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
