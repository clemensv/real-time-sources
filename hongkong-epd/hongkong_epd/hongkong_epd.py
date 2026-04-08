"""Hong Kong EPD AQHI Bridge."""

import argparse
import json
import logging
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests
from confluent_kafka import Producer

from hongkong_epd_producer_data import AQHIReading, Station
from hongkong_epd_producer_kafka_producer.producer import HKGovEPDAQHIEventProducer

logger = logging.getLogger(__name__)

AQHI_FEED_URL = "https://www.aqhi.gov.hk/epd/ddata/html/out/24aqhi_Eng.xml"

STATION_COORDS = {
    "central_western": (22.2863, 114.1500, "General Stations"),
    "eastern": (22.2847, 114.2264, "General Stations"),
    "kwai_chung": (22.3563, 114.1311, "General Stations"),
    "kwun_tong": (22.3123, 114.2289, "General Stations"),
    "north": (22.4966, 114.1388, "General Stations"),
    "sha_tin": (22.3811, 114.1880, "General Stations"),
    "sham_shui_po": (22.3319, 114.1623, "General Stations"),
    "southern": (22.2472, 114.1562, "General Stations"),
    "tai_po": (22.4508, 114.1655, "General Stations"),
    "tap_mun": (22.4716, 114.3608, "General Stations"),
    "tseung_kwan_o": (22.3108, 114.2553, "General Stations"),
    "tsuen_wan": (22.3728, 114.1235, "General Stations"),
    "tuen_mun": (22.3917, 113.9736, "General Stations"),
    "tung_chung": (22.2889, 113.9434, "General Stations"),
    "yuen_long": (22.4413, 114.0222, "General Stations"),
    "causeway_bay": (22.2800, 114.1841, "Roadside Stations"),
    "central": (22.2836, 114.1571, "Roadside Stations"),
    "mong_kok": (22.3194, 114.1688, "Roadside Stations"),
}

STATION_NAME_TO_ID = {
    "Central/Western": "central_western",
    "Eastern": "eastern",
    "Kwai Chung": "kwai_chung",
    "Kwun Tong": "kwun_tong",
    "North": "north",
    "Sha Tin": "sha_tin",
    "Sham Shui Po": "sham_shui_po",
    "Southern": "southern",
    "Tai Po": "tai_po",
    "Tap Mun": "tap_mun",
    "Tseung Kwan O": "tseung_kwan_o",
    "Tsuen Wan": "tsuen_wan",
    "Tuen Mun": "tuen_mun",
    "Tung Chung": "tung_chung",
    "Yuen Long": "yuen_long",
    "Causeway Bay": "causeway_bay",
    "Central": "central",
    "Mong Kok": "mong_kok",
}

STATION_ID_TO_NAME = {station_id: station_name for station_name, station_id in STATION_NAME_TO_ID.items()}


def aqhi_to_health_risk(aqhi: int) -> str:
    """Map AQHI values to the EPD health-risk categories."""
    if aqhi <= 3:
        return "Low"
    if aqhi <= 6:
        return "Moderate"
    if aqhi == 7:
        return "High"
    if aqhi <= 10:
        return "Very High"
    return "Serious"


class HKEPDAQHIAPI:
    """Client for the Hong Kong EPD AQHI XML feed."""

    def __init__(self, base_url: str = AQHI_FEED_URL, polling_interval: int = 3600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()

    def get_feed_xml(self) -> str:
        """Fetch the full 24-hour AQHI XML feed."""
        response = self.session.get(self.base_url, timeout=30)
        response.raise_for_status()
        return response.text

    def get_stations(self) -> dict[str, Station]:
        """Return hard-coded station reference data."""
        stations: dict[str, Station] = {}
        for station_id, station_name in STATION_ID_TO_NAME.items():
            latitude, longitude, station_type = STATION_COORDS[station_id]
            stations[station_id] = Station(
                station_id=station_id,
                station_name=station_name,
                station_type=station_type,
                latitude=latitude,
                longitude=longitude,
            )
        return stations

    def get_latest_readings(self) -> dict[str, AQHIReading]:
        """Parse the feed and keep only the latest AQHI reading per station."""
        xml_text = self.get_feed_xml()
        root = ET.fromstring(xml_text)
        latest_by_station: dict[str, AQHIReading] = {}

        for item in root.findall("item"):
            station_name = (item.findtext("StationName") or "").strip()
            station_id = STATION_NAME_TO_ID.get(station_name)
            if not station_id:
                continue

            try:
                reading_time = parsedate_to_datetime((item.findtext("DateTime") or "").strip())
            except (TypeError, ValueError):
                logger.warning("Could not parse AQHI timestamp for station %s", station_name)
                continue

            try:
                aqhi_value = int((item.findtext("aqhi") or "").strip())
            except ValueError:
                logger.warning("Could not parse AQHI value for station %s", station_name)
                continue

            station_type = (item.findtext("type") or "").strip() or STATION_COORDS[station_id][2]
            current = latest_by_station.get(station_id)
            if current and current.reading_time >= reading_time:
                continue

            latest_by_station[station_id] = AQHIReading(
                station_id=station_id,
                station_name=station_name,
                station_type=station_type,
                reading_time=reading_time,
                aqhi=aqhi_value,
                health_risk_category=aqhi_to_health_risk(aqhi_value),
            )

        return latest_by_station


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config: dict[str, str] = {}
    for part in connection_string.split(";"):
        part = part.strip()
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key == "Endpoint":
            config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
        elif key == "SharedAccessKeyName":
            config["sasl.username"] = "$ConnectionString"
        elif key == "SharedAccessKey":
            config["sasl.password"] = connection_string
        elif key == "BootstrapServer":
            config["bootstrap.servers"] = value
        elif key == "EntityPath":
            config["_entity_path"] = value
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as file_handle:
                return json.load(file_handle)
    except Exception as exc:  # pragma: no cover - defensive logging
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {key: data[key] for key in keys[-50000:]}
        with open(state_file, "w", encoding="utf-8") as file_handle:
            json.dump(data, file_handle)
    except Exception as exc:  # pragma: no cover - defensive logging
        logging.warning("Could not save state to %s: %s", state_file, exc)


def send_stations(api: HKEPDAQHIAPI, producer: HKGovEPDAQHIEventProducer) -> int:
    """Emit station reference data."""
    stations = api.get_stations()
    for station_id, station in stations.items():
        producer.send_hk_gov_epd_aqhi_station(station_id, station, flush_producer=False)
    producer.producer.flush()
    logger.info("Sent %d AQHI station reference events", len(stations))
    return len(stations)


def feed_readings(api: HKEPDAQHIAPI, producer: HKGovEPDAQHIEventProducer, previous_readings: dict) -> int:
    """Emit the newest AQHI reading for each station, deduplicated by station and timestamp."""
    readings = api.get_latest_readings()
    sent = 0
    for station_id, reading in sorted(readings.items()):
        reading_key = f"{station_id}:{reading.reading_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        producer.send_hk_gov_epd_aqhi_aqhireading(station_id, reading, flush_producer=False)
        previous_readings[reading_key] = reading.reading_time.isoformat()
        sent += 1
    producer.producer.flush()
    return sent


def _create_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    if not args.connection_string:
        if not os.environ.get("KAFKA_BROKER"):
            print("Error: --connection-string or KAFKA_BROKER required for feed mode")
            sys.exit(1)
        kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
    else:
        kafka_config = parse_connection_string(args.connection_string)

    topic = args.topic
    if "_entity_path" in kafka_config and not topic:
        topic = kafka_config.pop("_entity_path")
    elif "_entity_path" in kafka_config:
        kafka_config.pop("_entity_path")

    if not topic:
        topic = "hongkong-epd-aqhi"

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    if "sasl.username" in kafka_config:
        kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
    kafka_config["client.id"] = "hongkong-epd-bridge"
    return kafka_config, topic


def main():
    """Main entry point for the Hong Kong EPD AQHI bridge."""
    parser = argparse.ArgumentParser(description="Hong Kong EPD AQHI Bridge")
    parser.add_argument(
        "--connection-string",
        required=False,
        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"),
    )
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.environ.get("POLLING_INTERVAL", "3600")),
    )
    parser.add_argument(
        "--state-file",
        type=str,
        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.hongkong_epd_state.json")),
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List AQHI stations")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    api = HKEPDAQHIAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        for _, station in sorted(api.get_stations().items()):
            print(
                f"{station.station_id}: {station.station_name} "
                f"[{station.station_type}] ({station.latitude}, {station.longitude})"
            )
        return

    if args.command != "feed":
        parser.print_help()
        return

    kafka_config, topic = _create_kafka_config(args)
    kafka_producer = Producer(kafka_config)
    event_producer = HKGovEPDAQHIEventProducer(kafka_producer, topic)
    previous_readings = _load_state(args.state_file)

    logger.info("Starting Hong Kong EPD AQHI bridge, polling every %d seconds", args.polling_interval)
    send_stations(api, event_producer)
    while True:
        try:
            count = feed_readings(api, event_producer, previous_readings)
            _save_state(args.state_file, previous_readings)
            logger.info("Sent %d AQHI reading events", count)
        except Exception as exc:  # pragma: no cover - runtime safety
            logger.error("Error fetching/sending AQHI data: %s", exc)
        time.sleep(args.polling_interval)


if __name__ == "__main__":
    main()
