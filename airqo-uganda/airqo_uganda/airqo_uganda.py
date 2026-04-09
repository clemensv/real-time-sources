"""Bridge AirQo Uganda air quality data to Kafka as CloudEvents."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests
from confluent_kafka import Producer

from airqo_uganda_producer_data import Measurement, Site
from airqo_uganda_producer_kafka_producer.producer import NetAirqoUgandaEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

GRIDS_SUMMARY_URL = "https://api.airqo.net/api/v2/devices/grids/summary"
MEASUREMENTS_URL = "https://api.airqo.net/api/v2/devices/measurements"
STATE_FILE_DEFAULT = os.path.expanduser("~/.airqo_uganda_state.json")
POLL_INTERVAL_DEFAULT = 300


def _safe_float(value: Any) -> Optional[float]:
    """Convert a numeric value to float, returning None on invalid input."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"null", "none", "nan", ""}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _safe_str(value: Any) -> Optional[str]:
    """Convert a value to str, returning None on empty/null input."""
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _load_state(state_file: str) -> Dict[str, Any]:
    """Load persisted dedup state from disk."""
    if not state_file:
        return {"latest_timestamps": {}}
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {"latest_timestamps": data.get("latest_timestamps", {})}
    except Exception as exc:
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {"latest_timestamps": {}}


def _save_state(state_file: str, state: Dict[str, Any]) -> None:
    """Persist dedup state to disk."""
    if not state_file:
        return
    try:
        dirname = os.path.dirname(state_file)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception as exc:
        logging.warning("Could not save state to %s: %s", state_file, exc)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse Event Hubs, Fabric, or BootstrapServer-based Kafka connection strings."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if not part.strip():
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if key == "Endpoint":
                config_dict["bootstrap.servers"] = (
                    value.replace("sb://", "").replace("/", "") + ":9093"
                )
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


class AirQoUgandaAPI:
    """Poll the AirQo API and emit site reference and measurement events."""

    def __init__(
        self,
        api_key: str = "",
        state_file: str = "",
        session: Optional[requests.Session] = None,
    ) -> None:
        self.api_key = api_key
        self.session = session or requests.Session()
        self.state_file = state_file
        state = _load_state(state_file)
        self.latest_timestamps: Dict[str, str] = state.get("latest_timestamps", {})

    def fetch_sites(self) -> List[Dict[str, Any]]:
        """Fetch all sites from the AirQo grids summary endpoint (no auth required).

        Paginates through all pages and flattens sites from all grids.
        """
        all_sites: List[Dict[str, Any]] = []
        url: Optional[str] = GRIDS_SUMMARY_URL
        seen_ids: set = set()
        while url:
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                payload = response.json()
            except Exception as exc:
                logging.error("Error fetching AirQo grids summary from %s: %s", url, exc)
                break

            for grid in payload.get("grids", []):
                for site in grid.get("sites", []):
                    site_id = site.get("_id")
                    if site_id and site_id not in seen_ids:
                        seen_ids.add(site_id)
                        all_sites.append(site)

            meta = payload.get("meta", {})
            next_page = meta.get("nextPage")
            if next_page and next_page != url:
                url = next_page
            else:
                url = None

        return all_sites

    def build_site_payload(self, raw_site: Dict[str, Any]) -> Dict[str, Any]:
        """Map upstream site data to the Site event shape."""
        return {
            "site_id": str(raw_site.get("_id", "")),
            "name": str(raw_site.get("name", raw_site.get("generated_name", ""))),
            "formatted_name": _safe_str(raw_site.get("formatted_name")),
            "latitude": _safe_float(raw_site.get("approximate_latitude")),
            "longitude": _safe_float(raw_site.get("approximate_longitude")),
            "country": _safe_str(raw_site.get("country")),
            "region": _safe_str(raw_site.get("region")),
            "city": _safe_str(raw_site.get("city")),
            "is_online": bool(raw_site.get("isOnline", False)),
        }

    def fetch_measurements(self) -> List[Dict[str, Any]]:
        """Fetch recent measurements from the AirQo API (requires API key)."""
        if not self.api_key:
            logging.warning("No API key provided; skipping measurement fetch.")
            return []

        params = {"tenant": "airqo", "recent": "yes", "token": self.api_key}
        try:
            response = self.session.get(MEASUREMENTS_URL, params=params, timeout=60)
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            logging.error("Error fetching AirQo measurements: %s", exc)
            return []

        if not payload.get("success", False):
            logging.warning("AirQo API returned success=false: %s", payload.get("message", ""))
            return []

        return payload.get("measurements", [])

    def build_measurement_payload(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Map upstream measurement data to the Measurement event shape."""
        pm2_5 = raw.get("pm2_5") or {}
        pm10 = raw.get("pm10") or {}
        temperature = raw.get("temperature") or {}
        humidity = raw.get("humidity") or {}
        location = raw.get("location") or {}

        timestamp_str = raw.get("time", "")
        if not timestamp_str:
            timestamp_str = raw.get("timestamp", "")

        return {
            "site_id": str(raw.get("site_id", "")),
            "device": str(raw.get("device", "")),
            "device_id": _safe_str(raw.get("device_id")),
            "timestamp": timestamp_str,
            "pm2_5_raw": _safe_float(pm2_5.get("value") if isinstance(pm2_5, dict) else pm2_5),
            "pm2_5_calibrated": _safe_float(
                pm2_5.get("calibratedValue") if isinstance(pm2_5, dict) else None
            ),
            "pm10_raw": _safe_float(pm10.get("value") if isinstance(pm10, dict) else pm10),
            "pm10_calibrated": _safe_float(
                pm10.get("calibratedValue") if isinstance(pm10, dict) else None
            ),
            "temperature": _safe_float(
                temperature.get("value") if isinstance(temperature, dict) else temperature
            ),
            "humidity": _safe_float(
                humidity.get("value") if isinstance(humidity, dict) else humidity
            ),
            "latitude": _safe_float(
                location.get("latitude") if isinstance(location, dict) else None
            ),
            "longitude": _safe_float(
                location.get("longitude") if isinstance(location, dict) else None
            ),
            "frequency": _safe_str(raw.get("frequency")),
        }

    def should_emit_measurement(self, device: str, timestamp: str) -> bool:
        """Return whether a measurement timestamp is new for the given device."""
        return self.latest_timestamps.get(device) != timestamp

    def remember_measurement(self, device: str, timestamp: str) -> None:
        """Persist the latest measurement timestamp for a device."""
        self.latest_timestamps[device] = timestamp

    def persist_state(self) -> None:
        """Persist in-memory state to disk."""
        _save_state(self.state_file, {"latest_timestamps": self.latest_timestamps})

    def emit_sites(self, event_producer: NetAirqoUgandaEventProducer) -> int:
        """Fetch and emit site reference data. Returns count of sites emitted."""
        raw_sites = self.fetch_sites()
        count = 0
        for raw_site in raw_sites:
            payload = self.build_site_payload(raw_site)
            site_id = payload["site_id"]
            if not site_id:
                continue
            event_producer.send_net_airqo_uganda_site(
                _site_id=site_id,
                data=Site(**payload),
                flush_producer=False,
            )
            count += 1
        if count > 0 and hasattr(event_producer, "producer"):
            event_producer.producer.flush()
        logging.info("Emitted %d site reference events", count)
        return count

    def emit_measurements(self, event_producer: NetAirqoUgandaEventProducer) -> int:
        """Fetch and emit measurement events. Returns count of measurements emitted."""
        raw_measurements = self.fetch_measurements()
        count = 0
        for raw in raw_measurements:
            payload = self.build_measurement_payload(raw)
            device = payload["device"]
            timestamp = payload["timestamp"]
            site_id = payload["site_id"]
            if not device or not timestamp or not site_id:
                continue
            if not self.should_emit_measurement(device, timestamp):
                continue

            event_producer.send_net_airqo_uganda_measurement(
                _site_id=site_id,
                data=Measurement(**payload),
                flush_producer=False,
            )
            self.remember_measurement(device, timestamp)
            count += 1

        if count > 0 and hasattr(event_producer, "producer"):
            event_producer.producer.flush()
        self.persist_state()
        logging.info("Emitted %d measurement events", count)
        return count

    def build_kafka_config(
        self,
        connection_string: Optional[str] = None,
        kafka_bootstrap_servers: Optional[str] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        kafka_enable_tls: Optional[bool] = None,
    ) -> Dict[str, str]:
        """Build Kafka producer configuration from arguments and environment."""
        config: Dict[str, str] = {}
        if connection_string:
            config.update(parse_connection_string(connection_string))
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
            raise ValueError(
                "Kafka bootstrap servers must be provided through arguments or CONNECTION_STRING."
            )
        return config

    def feed(
        self,
        connection_string: Optional[str] = None,
        kafka_bootstrap_servers: Optional[str] = None,
        kafka_topic: Optional[str] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        polling_interval: int = POLL_INTERVAL_DEFAULT,
        kafka_enable_tls: Optional[bool] = None,
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
            raise ValueError(
                "Kafka topic must be provided through --kafka-topic or EntityPath in CONNECTION_STRING."
            )

        producer = Producer(kafka_config)
        event_producer = NetAirqoUgandaEventProducer(producer, resolved_topic)

        logging.info(
            "Starting AirQo Uganda bridge on topic %s at %s",
            resolved_topic,
            kafka_config["bootstrap.servers"],
        )

        # Emit reference data at startup
        self.emit_sites(event_producer)

        while True:
            cycle_started = datetime.now(timezone.utc)
            try:
                measurement_count = self.emit_measurements(event_producer)
                elapsed = (datetime.now(timezone.utc) - cycle_started).total_seconds()
                wait_time = max(0.0, polling_interval - elapsed)
                logging.info(
                    "Emitted %d measurements in %.2f seconds.",
                    measurement_count,
                    elapsed,
                )
                if wait_time > 0:
                    time.sleep(wait_time)
            except KeyboardInterrupt:
                logging.info("Stopping AirQo Uganda bridge.")
                break
            except Exception as exc:
                logging.error("Polling cycle failed: %s", exc)
                time.sleep(polling_interval)
        producer.flush()


def _env_bool(name: str, default: Optional[bool] = None) -> Optional[bool]:
    """Read a boolean environment variable."""
    value = os.getenv(name)
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    """Run the AirQo Uganda bridge."""
    parser = argparse.ArgumentParser(
        description="Bridge AirQo Uganda air quality data to Kafka as CloudEvents."
    )
    parser.add_argument(
        "--kafka-bootstrap-servers",
        type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma separated list of Kafka bootstrap servers",
    )
    parser.add_argument(
        "--kafka-topic",
        type=str,
        default=os.getenv("KAFKA_TOPIC"),
        help="Kafka topic to send messages to",
    )
    parser.add_argument(
        "--sasl-username",
        type=str,
        default=os.getenv("SASL_USERNAME"),
        help="Username for SASL PLAIN authentication",
    )
    parser.add_argument(
        "--sasl-password",
        type=str,
        default=os.getenv("SASL_PASSWORD"),
        help="Password for SASL PLAIN authentication",
    )
    parser.add_argument(
        "--connection-string",
        "-c",
        type=str,
        default=os.getenv("CONNECTION_STRING"),
        help="Microsoft Event Hubs, Fabric, or BootstrapServer connection string",
    )
    parser.add_argument(
        "--polling-interval",
        "-i",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", str(POLL_INTERVAL_DEFAULT))),
        help="Polling interval in seconds",
    )
    parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", STATE_FILE_DEFAULT),
        help="Path to the persisted dedup state file",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.getenv("AIRQO_API_KEY", ""),
        help="AirQo API key for authenticated endpoints",
    )

    args = parser.parse_args()
    tls_enabled = _env_bool("KAFKA_ENABLE_TLS", True)

    api = AirQoUgandaAPI(
        api_key=args.api_key,
        state_file=args.state_file,
    )

    api.feed(
        connection_string=args.connection_string,
        kafka_bootstrap_servers=args.kafka_bootstrap_servers,
        kafka_topic=args.kafka_topic,
        sasl_username=args.sasl_username,
        sasl_password=args.sasl_password,
        polling_interval=args.polling_interval,
        kafka_enable_tls=tls_enabled,
    )


if __name__ == "__main__":
    main()
