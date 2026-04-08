"""Bridge Sensor.Community API data to Kafka as CloudEvents."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import requests
from confluent_kafka import Producer

from sensor_community_producer_data import SensorInfo, SensorReading
from sensor_community_producer_kafka_producer.producer import IoSensorCommunityEventProducer


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


DEFAULT_SENSOR_TYPES = "SDS011,BME280,SPS30,DHT22,PMS5003,SHT31,BMP280"
STATE_FILE_DEFAULT = os.path.expanduser("~/.sensor_community_state.json")
API_BASE_URL = "https://data.sensor.community/airrohr/v1"
MEASUREMENT_FIELD_MAP = {
    "P1": "pm10_ug_m3",
    "P2": "pm2_5_ug_m3",
    "P0": "pm1_0_ug_m3",
    "P4": "pm4_0_ug_m3",
    "temperature": "temperature_celsius",
    "humidity": "humidity_percent",
    "pressure": "pressure_pa",
    "pressure_at_sealevel": "pressure_sealevel_pa",
    "noise_LAeq": "noise_laeq_db",
    "noise_LA_min": "noise_la_min_db",
    "noise_LA_max": "noise_la_max_db",
}
READING_FIELDS = [
    "pm10_ug_m3",
    "pm2_5_ug_m3",
    "pm1_0_ug_m3",
    "pm4_0_ug_m3",
    "temperature_celsius",
    "humidity_percent",
    "pressure_pa",
    "pressure_sealevel_pa",
    "noise_laeq_db",
    "noise_la_min_db",
    "noise_la_max_db",
]


def _load_state(state_file: str) -> dict[str, Any]:
    """Load persisted dedup and sensor metadata state."""
    if not state_file:
        return {"latest_timestamps": {}, "sensor_snapshots": {}}
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return {
                    "latest_timestamps": data.get("latest_timestamps", {}),
                    "sensor_snapshots": data.get("sensor_snapshots", {}),
                }
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {"latest_timestamps": {}, "sensor_snapshots": {}}


def _save_state(state_file: str, state: dict[str, Any]) -> None:
    """Persist dedup and sensor metadata state."""
    if not state_file:
        return
    try:
        os.makedirs(os.path.dirname(state_file), exist_ok=True) if os.path.dirname(state_file) else None
        with open(state_file, "w", encoding="utf-8") as file:
            json.dump(state, file)
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not save state to %s: %s", state_file, exc)


def _safe_float(value: Any) -> float | None:
    """Convert a Sensor.Community numeric string to float, returning None on invalid input."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"null", "none", "unknown", "nan"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_bool(value: Any) -> bool:
    """Convert integer-like or string-like values to bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _generated_optional_number(value: float | None) -> str | None:
    """Pass nullable numerics as strings so generated dataclasses preserve zero values."""
    if value is None:
        return None
    return str(value)


@dataclass
class PollResult:
    """Result counts for a polling cycle."""

    sensor_info_count: int = 0
    sensor_reading_count: int = 0


class SensorCommunityAPI:
    """Poll the Sensor.Community API and emit reference and reading events."""

    def __init__(
        self,
        sensor_types: str | list[str] | None = None,
        countries: str | list[str] | None = None,
        state_file: str = "",
        session: requests.Session | None = None,
    ) -> None:
        self.session = session or requests.Session()
        self.sensor_types = self.normalize_sensor_types(sensor_types or DEFAULT_SENSOR_TYPES)
        self.countries = self.normalize_countries(countries or os.getenv("COUNTRIES", ""))
        self.state_file = state_file
        state = _load_state(state_file)
        self.latest_timestamps: dict[str, str] = state.get("latest_timestamps", {})
        self.sensor_snapshots: dict[str, dict[str, Any]] = state.get("sensor_snapshots", {})

    @staticmethod
    def normalize_sensor_types(sensor_types: str | list[str] | None) -> list[str]:
        """Normalize sensor types to an ordered distinct list."""
        if sensor_types is None:
            return []
        if isinstance(sensor_types, list):
            items = sensor_types
        else:
            items = sensor_types.split(",")
        normalized: list[str] = []
        seen: set[str] = set()
        for item in items:
            cleaned = item.strip()
            if not cleaned:
                continue
            upper = cleaned.upper()
            if upper not in seen:
                normalized.append(upper)
                seen.add(upper)
        return normalized

    @staticmethod
    def normalize_countries(countries: str | list[str] | None) -> set[str]:
        """Normalize countries to uppercase ISO-3166-1 alpha-2 codes."""
        if not countries:
            return set()
        if isinstance(countries, list):
            items = countries
        else:
            items = countries.split(",")
        return {item.strip().upper() for item in items if item.strip()}

    @staticmethod
    def parse_connection_string(connection_string: str) -> dict[str, str]:
        """Parse Event Hubs, Fabric, or BootstrapServer-based Kafka connection strings."""
        config_dict: dict[str, str] = {}
        try:
            for part in connection_string.split(";"):
                if not part.strip():
                    continue
                key, value = part.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"')
                if key == "Endpoint":
                    config_dict["bootstrap.servers"] = value.replace("sb://", "").replace("/", "") + ":9093"
                elif key == "EntityPath":
                    config_dict["kafka_topic"] = value
                elif key == "SharedAccessKeyName":
                    config_dict["sasl.username"] = "$ConnectionString"
                elif key == "SharedAccessKey":
                    config_dict["sasl.password"] = connection_string.strip()
                elif key == "BootstrapServer":
                    config_dict["bootstrap.servers"] = value
        except ValueError as exc:
            raise ValueError("Invalid connection string format") from exc
        if "sasl.username" in config_dict:
            config_dict["security.protocol"] = "SASL_SSL"
            config_dict["sasl.mechanism"] = "PLAIN"
        return config_dict

    @staticmethod
    def sensor_feed_url(sensor_id: int | str) -> str:
        """Build the canonical Sensor.Community sensor detail URL."""
        return f"{API_BASE_URL}/sensor/{sensor_id}/"

    @staticmethod
    def extract_measurements(values: list[dict[str, Any]]) -> dict[str, float | None]:
        """Extract normalized measurement values from the sensordatavalues list."""
        measurements = {field: None for field in READING_FIELDS}
        for entry in values or []:
            upstream_name = entry.get("value_type")
            target_name = MEASUREMENT_FIELD_MAP.get(upstream_name)
            if target_name:
                measurements[target_name] = _safe_float(entry.get("value"))
        return measurements

    def should_include_record(self, record: dict[str, Any]) -> bool:
        """Return whether a record passes the configured country filter."""
        if not self.countries:
            return True
        location = record.get("location", {})
        country = str(location.get("country", "")).upper()
        return country in self.countries

    def fetch_sensor_type(self, sensor_type: str) -> list[dict[str, Any]]:
        """Fetch the latest readings for a configured sensor type."""
        response = self.session.get(f"{API_BASE_URL}/filter/type={sensor_type}", timeout=30)
        response.raise_for_status()
        payload = response.json()
        return [record for record in payload if self.should_include_record(record)]

    def build_sensor_info_payload(self, record: dict[str, Any]) -> dict[str, Any]:
        """Map upstream sensor metadata to the SensorInfo event shape."""
        sensor = record.get("sensor", {})
        sensor_type = sensor.get("sensor_type", {})
        location = record.get("location", {})
        return {
            "sensor_id": int(sensor.get("id")),
            "sensor_type_id": int(sensor_type.get("id")),
            "sensor_type_name": str(sensor_type.get("name", "")),
            "sensor_type_manufacturer": str(sensor_type.get("manufacturer", "")),
            "pin": str(sensor.get("pin", "")),
            "location_id": int(location.get("id")),
            "latitude": _safe_float(location.get("latitude")),
            "longitude": _safe_float(location.get("longitude")),
            "altitude": _generated_optional_number(_safe_float(location.get("altitude"))),
            "country": str(location.get("country", "")),
            "indoor": _parse_bool(location.get("indoor")),
        }

    def build_sensor_reading_payload(self, record: dict[str, Any]) -> dict[str, Any]:
        """Map upstream reading data to the SensorReading event shape."""
        sensor = record.get("sensor", {})
        sensor_type = sensor.get("sensor_type", {})
        reading = {
            "sensor_id": int(sensor.get("id")),
            "timestamp": str(record.get("timestamp", "")),
            "sensor_type_name": str(sensor_type.get("name", "")),
        }
        reading.update(
            {
                key: _generated_optional_number(value)
                for key, value in self.extract_measurements(record.get("sensordatavalues", [])).items()
            }
        )
        return reading

    def sensor_info_changed(self, sensor_info: dict[str, Any]) -> bool:
        """Return whether a sensor metadata snapshot is new or changed."""
        sensor_id = str(sensor_info["sensor_id"])
        previous = self.sensor_snapshots.get(sensor_id)
        return previous != sensor_info

    def should_emit_reading(self, sensor_id: int, timestamp: str) -> bool:
        """Return whether a sensor reading timestamp is new."""
        return self.latest_timestamps.get(str(sensor_id)) != timestamp

    def remember_sensor_info(self, sensor_info: dict[str, Any]) -> None:
        """Persist the latest metadata snapshot for a sensor."""
        self.sensor_snapshots[str(sensor_info["sensor_id"])] = sensor_info

    def remember_reading(self, sensor_id: int, timestamp: str) -> None:
        """Persist the latest reading timestamp for a sensor."""
        self.latest_timestamps[str(sensor_id)] = timestamp

    def persist_state(self) -> None:
        """Persist in-memory state to disk."""
        _save_state(
            self.state_file,
            {
                "latest_timestamps": self.latest_timestamps,
                "sensor_snapshots": self.sensor_snapshots,
            },
        )

    def process_records(
        self,
        records: list[dict[str, Any]],
        event_producer: Any,
        flush_producer: bool = False,
    ) -> PollResult:
        """Process upstream records and emit SensorInfo and SensorReading events."""
        result = PollResult()
        for record in records:
            sensor_info = self.build_sensor_info_payload(record)
            sensor_id = sensor_info["sensor_id"]
            feed_url = self.sensor_feed_url(sensor_id)
            if self.sensor_info_changed(sensor_info):
                event_producer.send_io_sensor_community_sensor_info(
                    _feedurl=feed_url,
                    _sensor_id=sensor_id,
                    data=SensorInfo(**sensor_info),
                    flush_producer=False,
                )
                self.remember_sensor_info(sensor_info)
                result.sensor_info_count += 1

            sensor_reading = self.build_sensor_reading_payload(record)
            if self.should_emit_reading(sensor_id, sensor_reading["timestamp"]):
                event_producer.send_io_sensor_community_sensor_reading(
                    _feedurl=feed_url,
                    _sensor_id=sensor_id,
                    data=SensorReading(**sensor_reading),
                    flush_producer=False,
                )
                self.remember_reading(sensor_id, sensor_reading["timestamp"])
                result.sensor_reading_count += 1
        if flush_producer and hasattr(event_producer, "producer"):
            event_producer.producer.flush()
        self.persist_state()
        return result

    def poll_once(self, event_producer: Any) -> PollResult:
        """Fetch all configured sensor types once and emit resulting events."""
        result = PollResult()
        for sensor_type in self.sensor_types:
            logging.debug("Fetching sensor type %s", sensor_type)
            records = self.fetch_sensor_type(sensor_type)
            partial = self.process_records(records, event_producer)
            result.sensor_info_count += partial.sensor_info_count
            result.sensor_reading_count += partial.sensor_reading_count
        if hasattr(event_producer, "producer"):
            event_producer.producer.flush()
        return result

    def build_kafka_config(
        self,
        connection_string: str | None = None,
        kafka_bootstrap_servers: str | None = None,
        sasl_username: str | None = None,
        sasl_password: str | None = None,
        kafka_enable_tls: bool | None = None,
    ) -> dict[str, str]:
        """Build Kafka producer configuration from arguments and environment."""
        config: dict[str, str] = {}
        if connection_string:
            config.update(self.parse_connection_string(connection_string))
        if kafka_bootstrap_servers:
            config["bootstrap.servers"] = kafka_bootstrap_servers
        if sasl_username:
            config["sasl.username"] = sasl_username
        if sasl_password:
            config["sasl.password"] = sasl_password
        if "sasl.username" in config and "security.protocol" not in config:
            config["security.protocol"] = "SASL_SSL"
            config["sasl.mechanism"] = "PLAIN"
        if kafka_enable_tls is False and "security.protocol" not in config:
            config["security.protocol"] = "PLAINTEXT"
        if "bootstrap.servers" not in config:
            raise ValueError("Kafka bootstrap servers must be provided through arguments or CONNECTION_STRING.")
        return config

    def feed(
        self,
        connection_string: str | None = None,
        kafka_bootstrap_servers: str | None = None,
        kafka_topic: str | None = None,
        sasl_username: str | None = None,
        sasl_password: str | None = None,
        polling_interval: int = 300,
        kafka_enable_tls: bool | None = None,
    ) -> None:
        """Start the continuous polling loop."""
        kafka_config = self.build_kafka_config(
            connection_string=connection_string,
            kafka_bootstrap_servers=kafka_bootstrap_servers,
            sasl_username=sasl_username,
            sasl_password=sasl_password,
            kafka_enable_tls=kafka_enable_tls,
        )
        resolved_topic = kafka_topic or kafka_config.pop("kafka_topic", None)
        if not resolved_topic:
            raise ValueError("Kafka topic must be provided through --kafka-topic or EntityPath in CONNECTION_STRING.")

        producer = Producer(kafka_config)
        event_producer = IoSensorCommunityEventProducer(producer, resolved_topic)

        logging.info(
            "Starting Sensor.Community feed for sensor types %s on topic %s at %s",
            ",".join(self.sensor_types),
            resolved_topic,
            kafka_config["bootstrap.servers"],
        )
        while True:
            cycle_started = datetime.now(timezone.utc)
            try:
                result = self.poll_once(event_producer)
                elapsed = (datetime.now(timezone.utc) - cycle_started).total_seconds()
                wait_time = max(0.0, polling_interval - elapsed)
                logging.info(
                    "Emitted %s SensorInfo events and %s SensorReading events in %.2f seconds.",
                    result.sensor_info_count,
                    result.sensor_reading_count,
                    elapsed,
                )
                if wait_time > 0:
                    time.sleep(wait_time)
            except KeyboardInterrupt:
                logging.info("Stopping Sensor.Community bridge.")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logging.error("Polling cycle failed: %s", exc)
                time.sleep(polling_interval)
        producer.flush()


def _env_bool(name: str, default: bool | None = None) -> bool | None:
    """Read a boolean environment variable."""
    value = os.getenv(name)
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    """Run the Sensor.Community bridge."""
    parser = argparse.ArgumentParser(description="Bridge Sensor.Community API data to Kafka as CloudEvents.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Continuously poll Sensor.Community and emit events to Kafka")
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma separated list of Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        "--kafka-topic",
        type=str,
        default=os.getenv("KAFKA_TOPIC"),
        help="Kafka topic to send messages to",
    )
    feed_parser.add_argument(
        "--sasl-username",
        type=str,
        default=os.getenv("SASL_USERNAME"),
        help="Username for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "--sasl-password",
        type=str,
        default=os.getenv("SASL_PASSWORD"),
        help="Password for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "--connection-string",
        "-c",
        type=str,
        default=os.getenv("CONNECTION_STRING"),
        help="Microsoft Event Hubs, Fabric, or BootstrapServer connection string",
    )
    feed_parser.add_argument(
        "--polling-interval",
        "-i",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", "300")),
        help="Polling interval in seconds",
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", STATE_FILE_DEFAULT),
        help="Path to the persisted dedup state file",
    )
    feed_parser.add_argument(
        "--sensor-types",
        type=str,
        default=os.getenv("SENSOR_TYPES", DEFAULT_SENSOR_TYPES),
        help="Comma separated list of Sensor.Community sensor types to poll",
    )
    feed_parser.add_argument(
        "--countries",
        type=str,
        default=os.getenv("COUNTRIES"),
        help="Optional comma separated list of countries to keep",
    )
    feed_parser.add_argument(
        "--kafka-enable-tls",
        type=str,
        default=os.getenv("KAFKA_ENABLE_TLS"),
        help="Set to false to force PLAINTEXT for plain Kafka bootstrap servers",
    )

    args = parser.parse_args()

    if args.command != "feed":
        parser.print_help()
        return

    kafka_enable_tls = None
    if args.kafka_enable_tls is not None:
        kafka_enable_tls = str(args.kafka_enable_tls).strip().lower() in {"1", "true", "yes", "on"}
    else:
        kafka_enable_tls = _env_bool("KAFKA_ENABLE_TLS")

    api = SensorCommunityAPI(
        sensor_types=args.sensor_types,
        countries=args.countries,
        state_file=args.state_file,
    )
    api.feed(
        connection_string=args.connection_string,
        kafka_bootstrap_servers=args.kafka_bootstrap_servers,
        kafka_topic=args.kafka_topic,
        sasl_username=args.sasl_username,
        sasl_password=args.sasl_password,
        polling_interval=args.polling_interval,
        kafka_enable_tls=kafka_enable_tls,
    )
