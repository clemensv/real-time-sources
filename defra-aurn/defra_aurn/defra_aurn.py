"""Defra AURN bridge for the UK Automatic Urban and Rural Network."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from confluent_kafka import Producer
from defra_aurn_producer_data import Observation, Station, Timeseries
from defra_aurn_producer_kafka_producer.producer import (
    UkGovDefraAurnStationsEventProducer,
    UkGovDefraAurnTimeseriesEventProducer,
)

LOGGER = logging.getLogger(__name__)

BASE_URL = "https://uk-air.defra.gov.uk/sos-ukair/api/v1"
DEFAULT_POLLING_INTERVAL = 3600
DEFAULT_PAGE_LIMIT = 1000
DEFAULT_TIMEOUT = 30
DEFAULT_REFERENCE_REFRESH_INTERVAL = 86400
DEFAULT_LOOKBACK_DURATION = "PT2H"
DEFAULT_BOOTSTRAP_LOOKBACK_DURATION = "PT6H"


def convert_timestamp_ms_to_iso(timestamp_ms: int) -> str:
    """Convert a Unix millisecond timestamp to an ISO 8601 UTC string."""
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()


def format_api_timestamp(value: datetime) -> str:
    """Format a UTC datetime for the SOS API timespan parameter."""
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_state(state_file: str) -> dict[str, int]:
    """Load persisted observation state from a JSON file."""
    try:
        expanded_path = Path(state_file).expanduser()
        if expanded_path.exists():
            return {str(key): int(value) for key, value in json.loads(expanded_path.read_text(encoding="utf-8")).items()}
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, state: dict[str, int]) -> None:
    """Persist observation state to a JSON file."""
    try:
        expanded_path = Path(state_file).expanduser()
        expanded_path.parent.mkdir(parents=True, exist_ok=True)
        expanded_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not save state to %s: %s", state_file, exc)


def parse_connection_string(connection_string: str) -> dict[str, str]:
    """Parse either an Event Hubs or BootstrapServer style connection string."""
    stripped = connection_string.strip()
    config: dict[str, str] = {}
    has_sasl = False

    try:
        for part in stripped.split(";"):
            part = part.strip()
            if not part:
                continue
            if "=" not in part:
                raise ValueError("Invalid connection string format")
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if key == "Endpoint":
                config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "BootstrapServer":
                config["bootstrap.servers"] = value
            elif key == "EntityPath":
                config["kafka_topic"] = value
            elif key == "SharedAccessKeyName":
                has_sasl = True
                config["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                has_sasl = True
                config["sasl.password"] = stripped
    except ValueError:
        raise
    except Exception as exc:  # pylint: disable=broad-except
        raise ValueError("Invalid connection string format") from exc

    if has_sasl:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"

    return config


def _is_truthy(value: str | None, default: bool = True) -> bool:
    """Parse a boolean-like environment setting."""
    if value is None:
        return default
    return value.strip().lower() not in {"false", "0", "no", "off"}


class DefraAURNAPI:
    """Client and bridge logic for the Defra AURN SOS Timeseries API."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        page_limit: int = DEFAULT_PAGE_LIMIT,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.page_limit = page_limit
        self.session = session or requests.Session()
        self.session.headers.setdefault("Accept", "application/json")

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _get_paginated_collection(self, path: str) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        offset = 0
        while True:
            page = self._get_json(path, params={"limit": self.page_limit, "offset": offset})
            if not isinstance(page, list):
                raise ValueError(f"Expected a list response from {path}")
            items.extend(page)
            if len(page) < self.page_limit:
                break
            offset += self.page_limit
        return items

    def list_stations(self) -> list[dict[str, Any]]:
        """Fetch all station GeoJSON features."""
        return self._get_paginated_collection("/stations")

    def list_timeseries(self) -> list[dict[str, Any]]:
        """Fetch all timeseries summary records."""
        return self._get_paginated_collection("/timeseries")

    def get_timeseries_details(self, timeseries_id: str) -> dict[str, Any]:
        """Fetch expanded metadata for a timeseries."""
        return self._get_json(f"/timeseries/{timeseries_id}", params={"expanded": "true"})

    def get_timeseries_data(
        self,
        timeseries_id: str,
        end_time: datetime,
        lookback_duration: str = DEFAULT_LOOKBACK_DURATION,
    ) -> list[dict[str, Any]]:
        """Fetch recent values for a timeseries."""
        payload = self._get_json(
            f"/timeseries/{timeseries_id}/getData",
            params={"timespan": f"{lookback_duration}/{format_api_timestamp(end_time)}"},
        )
        if not isinstance(payload, dict):
            raise ValueError(f"Expected a dict response from /timeseries/{timeseries_id}/getData")
        return payload.get("values", [])

    @staticmethod
    def _extract_coordinates(feature: dict[str, Any] | None) -> tuple[float | None, float | None]:
        coordinates = ((feature or {}).get("geometry") or {}).get("coordinates") or []
        latitude = coordinates[0] if len(coordinates) > 0 else None
        longitude = coordinates[1] if len(coordinates) > 1 else None
        return (
            float(latitude) if latitude is not None else None,
            float(longitude) if longitude is not None else None,
        )

    def normalize_station(self, feature: dict[str, Any]) -> Station:
        """Normalize a station GeoJSON feature into the generated Station data class."""
        properties = feature.get("properties", {})
        latitude, longitude = self._extract_coordinates(feature)
        station = Station(
            station_id=str(properties.get("id")),
            label=str(properties.get("label", "")),
            latitude=latitude if latitude is not None else 0.0,
            longitude=longitude if longitude is not None else 0.0,
        )
        if latitude == 0.0:
            station.latitude = 0.0
        if longitude == 0.0:
            station.longitude = 0.0
        return station

    def normalize_timeseries(self, payload: dict[str, Any]) -> Timeseries:
        """Normalize expanded timeseries metadata into the generated Timeseries data class."""
        station_payload = payload.get("station") or {}
        station_properties = station_payload.get("properties") or {}
        parameters = payload.get("parameters") or {}
        phenomenon = parameters.get("phenomenon") or {}
        category = parameters.get("category") or {}
        latitude, longitude = self._extract_coordinates(station_payload)

        timeseries = Timeseries(
            timeseries_id=str(payload.get("id")),
            label=str(payload.get("label", "")),
            uom=str(payload.get("uom", "")),
            station_id=str(station_properties.get("id")),
            station_label=str(station_properties.get("label", "")),
            latitude=latitude,
            longitude=longitude,
            phenomenon_id=str(phenomenon["id"]) if phenomenon.get("id") is not None else None,
            phenomenon_label=str(phenomenon["label"]) if phenomenon.get("label") is not None else None,
            category_id=str(category["id"]) if category.get("id") is not None else None,
            category_label=str(category["label"]) if category.get("label") is not None else None,
        )
        if latitude == 0.0:
            timeseries.latitude = 0.0
        if longitude == 0.0:
            timeseries.longitude = 0.0
        return timeseries

    @staticmethod
    def normalize_observation(timeseries_id: str, timestamp_ms: int, value: float | None, uom: str) -> Observation:
        """Normalize a value entry into the generated Observation data class."""
        observation = Observation(
            timeseries_id=str(timeseries_id),
            timestamp=convert_timestamp_ms_to_iso(timestamp_ms),
            value=float(value) if value is not None else None,
            uom=str(uom),
        )
        if value == 0:
            observation.value = 0.0
        return observation

    def emit_reference_data(
        self,
        stations_producer: Any,
        timeseries_producer: Any,
    ) -> dict[str, Timeseries]:
        """Fetch and emit all station and timeseries reference data."""
        station_count = 0
        for feature in self.list_stations():
            station = self.normalize_station(feature)
            stations_producer.send_uk_gov_defra_aurn_station(
                _station_id=station.station_id,
                data=station,
                flush_producer=False,
            )
            station_count += 1
        stations_producer.producer.flush()
        LOGGER.info("Emitted %d station reference events", station_count)

        timeseries_catalog: dict[str, Timeseries] = {}
        timeseries_count = 0
        for summary in self.list_timeseries():
            timeseries_id = str(summary.get("id"))
            try:
                details = self.get_timeseries_details(timeseries_id)
                timeseries = self.normalize_timeseries(details)
                timeseries_catalog[timeseries.timeseries_id] = timeseries
                timeseries_producer.send_uk_gov_defra_aurn_timeseries(
                    _timeseries_id=timeseries.timeseries_id,
                    data=timeseries,
                    flush_producer=False,
                )
                timeseries_count += 1
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.error("Failed to fetch metadata for timeseries %s: %s", timeseries_id, exc)
        timeseries_producer.producer.flush()
        LOGGER.info("Emitted %d timeseries reference events", timeseries_count)
        return timeseries_catalog

    def emit_observations(
        self,
        timeseries_producer: Any,
        timeseries_catalog: dict[str, Timeseries],
        state: dict[str, int],
        end_time: datetime | None = None,
    ) -> int:
        """Fetch and emit new observation values for all known timeseries."""
        end_time = end_time or datetime.now(timezone.utc)
        emitted = 0

        for timeseries_id, metadata in timeseries_catalog.items():
            last_seen = int(state.get(timeseries_id, -1))
            lookback_duration = (
                DEFAULT_BOOTSTRAP_LOOKBACK_DURATION
                if last_seen < 0
                else DEFAULT_LOOKBACK_DURATION
            )
            try:
                values = self.get_timeseries_data(timeseries_id, end_time, lookback_duration=lookback_duration)
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.error("Failed to fetch observations for timeseries %s: %s", timeseries_id, exc)
                continue

            max_seen = last_seen

            for entry in sorted(values, key=lambda item: int(item.get("timestamp", -1))):
                timestamp_ms = entry.get("timestamp")
                if timestamp_ms is None:
                    continue
                timestamp_ms = int(timestamp_ms)
                if timestamp_ms <= last_seen:
                    continue
                observation = self.normalize_observation(
                    timeseries_id=timeseries_id,
                    timestamp_ms=timestamp_ms,
                    value=entry.get("value"),
                    uom=metadata.uom,
                )
                timeseries_producer.send_uk_gov_defra_aurn_observation(
                    _timeseries_id=timeseries_id,
                    data=observation,
                    flush_producer=False,
                )
                emitted += 1
                max_seen = max(max_seen, timestamp_ms)

            if max_seen > last_seen:
                state[timeseries_id] = max_seen

        timeseries_producer.producer.flush()
        return emitted


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    """Build Kafka configuration from CLI arguments and environment defaults."""
    kafka_config: dict[str, str] = {}
    if args.connection_string:
        kafka_config.update(parse_connection_string(args.connection_string))

    if args.kafka_bootstrap_servers:
        kafka_config["bootstrap.servers"] = args.kafka_bootstrap_servers
    if args.sasl_username:
        kafka_config["sasl.username"] = args.sasl_username
    if args.sasl_password:
        kafka_config["sasl.password"] = args.sasl_password

    topic = args.kafka_topic or kafka_config.pop("kafka_topic", None) or "defra-aurn"
    tls_enabled = _is_truthy(str(args.kafka_enable_tls) if args.kafka_enable_tls is not None else None, default=True)

    if "sasl.username" in kafka_config and "sasl.password" in kafka_config:
        kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["sasl.mechanism"] = "PLAIN"
        kafka_config["sasl.mechanisms"] = "PLAIN"
    else:
        kafka_config["security.protocol"] = "SSL" if tls_enabled else "PLAINTEXT"

    kafka_config["client.id"] = "defra-aurn-bridge"

    if "bootstrap.servers" not in kafka_config:
        raise ValueError("Kafka bootstrap servers are required")

    return kafka_config, topic


def run_feed(args: argparse.Namespace) -> None:
    """Run the bridge feed loop."""
    kafka_config, kafka_topic = build_kafka_config(args)
    state_file = os.path.expanduser(args.state_file)
    state = _load_state(state_file)

    producer = Producer(kafka_config)
    stations_producer = UkGovDefraAurnStationsEventProducer(producer, kafka_topic)
    timeseries_producer = UkGovDefraAurnTimeseriesEventProducer(producer, kafka_topic)
    api = DefraAURNAPI()

    reference_refresh_interval = DEFAULT_REFERENCE_REFRESH_INTERVAL
    last_reference_refresh = 0.0
    timeseries_catalog: dict[str, Timeseries] = {}

    while True:
        try:
            now = time.time()
            if not timeseries_catalog or now - last_reference_refresh >= reference_refresh_interval:
                timeseries_catalog = api.emit_reference_data(stations_producer, timeseries_producer)
                last_reference_refresh = now
                _save_state(state_file, state)

            emitted = api.emit_observations(timeseries_producer, timeseries_catalog, state)
            _save_state(state_file, state)
            LOGGER.info("Emitted %d observation events", emitted)
            time.sleep(args.polling_interval)
        except KeyboardInterrupt:
            LOGGER.info("Stopping Defra AURN bridge")
            producer.flush()
            return
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.error("Bridge loop failed: %s", exc)
            time.sleep(args.polling_interval)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Defra AURN UK air quality bridge")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Poll the API and emit CloudEvents to Kafka")
    feed_parser.add_argument(
        "--connection-string",
        default=os.getenv("CONNECTION_STRING"),
        help="Azure Event Hubs/Fabric or BootstrapServer connection string",
    )
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma-separated Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        "--kafka-topic",
        default=os.getenv("KAFKA_TOPIC"),
        help="Kafka topic name",
    )
    feed_parser.add_argument(
        "--sasl-username",
        default=os.getenv("SASL_USERNAME"),
        help="Username for SASL authentication",
    )
    feed_parser.add_argument(
        "--sasl-password",
        default=os.getenv("SASL_PASSWORD"),
        help="Password for SASL authentication",
    )
    feed_parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLLING_INTERVAL))),
        help="Polling interval in seconds",
    )
    feed_parser.add_argument(
        "--state-file",
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.defra_aurn_state.json")),
        help="Path to the observation state file",
    )
    feed_parser.add_argument(
        "--kafka-enable-tls",
        default=os.getenv("KAFKA_ENABLE_TLS", "true"),
        help="Whether TLS is enabled for Kafka connections",
    )

    return parser


def main() -> None:
    """Entry point for the Defra AURN bridge."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "feed":
        run_feed(args)
        return

    parser.print_help()
    sys.exit(1)
