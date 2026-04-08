"""IRCELINE Belgium air-quality bridge to Kafka."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
from confluent_kafka import Producer
from irceline_belgium_producer_data import Observation, Station, StatusInterval, Timeseries
from irceline_belgium_producer_kafka_producer.producer import (
    BeIrcelineStationsEventProducer,
    BeIrcelineTimeseriesEventProducer,
)


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


LOGGER = logging.getLogger(__name__)


def _load_state(state_file: str) -> Dict[str, int]:
    """Load persisted per-timeseries dedup state from disk."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                raw_state = json.load(handle)
            return {str(key): int(value) for key, value in raw_state.items()}
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, state: Dict[str, int]) -> None:
    """Persist per-timeseries dedup state to disk."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not save state to %s: %s", state_file, exc)


def _parse_bool(value: Any) -> bool:
    """Parse a truthy or falsy string value."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off", ""}


class IrcelineBelgiumAPI:
    """Poll the IRCELINE Belgium SOS timeseries API and emit CloudEvents."""

    BASE_URL = "https://geo.irceline.be/sos/api/v1"
    DEFAULT_TOPIC = "irceline-belgium"
    DEFAULT_TIMEOUT = 30
    DEFAULT_LIMIT = 500
    DEFAULT_REFERENCE_REFRESH_INTERVAL = 24 * 60 * 60

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        *,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        page_limit: int = DEFAULT_LIMIT,
        reference_refresh_interval: int = DEFAULT_REFERENCE_REFRESH_INTERVAL,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.page_limit = page_limit
        self.reference_refresh_interval = reference_refresh_interval
        self.session = session or requests.Session()
        self.session.headers.setdefault("Accept", "application/json")

    @staticmethod
    def parse_connection_string(connection_string: str) -> Tuple[Dict[str, str], Optional[str]]:
        """Parse Event Hubs or plain Kafka connection strings."""
        if not connection_string:
            return {}, None

        parts: Dict[str, str] = {}
        for fragment in connection_string.split(";"):
            fragment = fragment.strip()
            if not fragment:
                continue
            key, separator, value = fragment.partition("=")
            if not separator:
                raise ValueError("Invalid connection string format")
            parts[key.strip()] = value.strip().strip('"')

        if "Endpoint" in parts:
            endpoint = parts["Endpoint"].replace("sb://", "").rstrip("/")
            return (
                {
                    "bootstrap.servers": f"{endpoint}:9093",
                    "security.protocol": "SASL_SSL",
                    "sasl.mechanisms": "PLAIN",
                    "sasl.username": "$ConnectionString",
                    "sasl.password": connection_string.strip(),
                },
                parts.get("EntityPath"),
            )

        if "BootstrapServer" in parts:
            return (
                {
                    "bootstrap.servers": parts["BootstrapServer"],
                },
                parts.get("EntityPath"),
            )

        raise ValueError("Unsupported connection string format")

    @staticmethod
    def timestamp_ms_to_iso8601(timestamp_ms: int | float) -> str:
        """Convert a Unix millisecond timestamp to ISO 8601 UTC."""
        timestamp_float = float(timestamp_ms)
        timestamp = datetime.fromtimestamp(timestamp_float / 1000.0, tz=timezone.utc)
        timespec = "milliseconds" if int(timestamp_float) % 1000 else "seconds"
        return timestamp.isoformat(timespec=timespec).replace("+00:00", "Z")

    def _get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Fetch JSON from the IRCELINE API."""
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _get_paginated_collection(
        self,
        path: str,
        *,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch a paginated list endpoint using IRCELINE limit/offset semantics."""
        items: List[Dict[str, Any]] = []
        offset = 0
        while True:
            params = {"limit": self.page_limit, "offset": offset}
            if extra_params:
                params.update(extra_params)
            page = self._get_json(path, params=params)
            if not page:
                break
            items.extend(page)
            if len(page) < self.page_limit:
                break
            offset += self.page_limit
        return items

    def list_stations(self) -> List[Dict[str, Any]]:
        """Fetch all station reference records."""
        return self._get_paginated_collection("/stations")

    def list_timeseries(self) -> List[Dict[str, Any]]:
        """Fetch all timeseries metadata, expanded to include parameters and status intervals."""
        return self._get_paginated_collection("/timeseries", extra_params={"expanded": "true"})

    def get_timeseries_data(
        self,
        timeseries_id: str,
        *,
        end_time: Optional[datetime] = None,
        lookback_duration: str = "PT2H",
    ) -> List[Dict[str, Any]]:
        """Fetch recent measurements for one timeseries."""
        effective_end_time = end_time or datetime.now(timezone.utc)
        params = {
            "timespan": f"{lookback_duration}/{effective_end_time.isoformat(timespec='seconds').replace('+00:00', 'Z')}"
        }
        payload = self._get_json(f"/timeseries/{timeseries_id}/getData", params=params)
        return payload.get("values", [])

    @staticmethod
    def _extract_coordinates(feature: Optional[Dict[str, Any]]) -> Tuple[Optional[float], Optional[float]]:
        """Extract latitude and longitude from IRCELINE GeoJSON coordinates."""
        coordinates = (((feature or {}).get("geometry") or {}).get("coordinates")) or []
        if len(coordinates) < 2:
            return None, None
        longitude = float(coordinates[0])
        latitude = float(coordinates[1])
        return latitude, longitude

    def normalize_station(self, feature: Dict[str, Any]) -> Station:
        """Normalize one upstream station GeoJSON feature."""
        latitude, longitude = self._extract_coordinates(feature)
        properties = feature.get("properties") or {}
        if latitude is None or longitude is None:
            raise ValueError(f"Station {properties.get('id')} is missing coordinates")
        return Station(
            station_id=str(properties.get("id", "")),
            label=str(properties.get("label", "")),
            latitude=latitude,
            longitude=longitude,
        )

    @staticmethod
    def parse_status_intervals(status_intervals: Optional[Iterable[Dict[str, Any]]]) -> List[StatusInterval]:
        """Normalize optional IRCELINE status intervals."""
        intervals: List[StatusInterval] = []
        for interval in status_intervals or []:
            intervals.append(
                StatusInterval(
                    lower=str(interval.get("lower", "")),
                    upper=str(interval.get("upper", "")),
                    name=str(interval.get("name", "")),
                    color=str(interval.get("color", "")),
                )
            )
        return intervals

    def normalize_timeseries(self, payload: Dict[str, Any]) -> Timeseries:
        """Normalize one upstream timeseries metadata record."""
        station = payload.get("station") or {}
        parameters = payload.get("parameters") or {}
        phenomenon = parameters.get("phenomenon") or {}
        category = parameters.get("category") or {}
        station_properties = station.get("properties") or {}
        latitude, longitude = self._extract_coordinates(station)
        status_intervals = self.parse_status_intervals(payload.get("statusIntervals"))

        return Timeseries(
            timeseries_id=str(payload.get("id", "")),
            label=str(payload.get("label", "")),
            uom=str(payload.get("uom", "")),
            station_id=str(station_properties.get("id", "")),
            station_label=str(station_properties.get("label", "")),
            latitude=latitude,
            longitude=longitude,
            phenomenon_id=str(phenomenon.get("id")) if phenomenon.get("id") is not None else None,
            phenomenon_label=str(phenomenon.get("label")) if phenomenon.get("label") is not None else None,
            category_id=str(category.get("id")) if category.get("id") is not None else None,
            category_label=str(category.get("label")) if category.get("label") is not None else None,
            status_intervals=status_intervals or None,
        )

    def normalize_observation(self, timeseries: Timeseries, payload: Dict[str, Any]) -> Observation:
        """Normalize one upstream timeseries value record."""
        raw_value = payload.get("value")
        return Observation(
            timeseries_id=timeseries.timeseries_id,
            timestamp=self.timestamp_ms_to_iso8601(int(payload["timestamp"])),
            value=float(raw_value) if raw_value is not None else None,
            uom=timeseries.uom,
        )

    @staticmethod
    def filter_new_observations(
        timeseries_id: str,
        values: Iterable[Dict[str, Any]],
        state: Dict[str, int],
    ) -> List[Dict[str, Any]]:
        """Return only values newer than the persisted state and advance the state."""
        last_seen_timestamp = int(state.get(timeseries_id, 0))
        new_values: List[Dict[str, Any]] = []
        max_timestamp = last_seen_timestamp

        for item in sorted(values, key=lambda value: int(value.get("timestamp", 0))):
            timestamp = int(item.get("timestamp", 0))
            if timestamp <= last_seen_timestamp:
                continue
            new_values.append(item)
            max_timestamp = max(max_timestamp, timestamp)

        if max_timestamp > last_seen_timestamp:
            state[timeseries_id] = max_timestamp

        return new_values

    @classmethod
    def build_kafka_config(cls, args: argparse.Namespace) -> Tuple[Dict[str, str], str]:
        """Build Kafka configuration from CLI arguments and environment variables."""
        parsed_config, parsed_topic = cls.parse_connection_string(args.connection_string) if args.connection_string else ({}, None)

        kafka_topic = args.kafka_topic or parsed_topic or cls.DEFAULT_TOPIC
        kafka_enable_tls = _parse_bool(args.kafka_enable_tls)
        kafka_config = dict(parsed_config)

        if args.kafka_bootstrap_servers:
            kafka_config["bootstrap.servers"] = args.kafka_bootstrap_servers

        if "bootstrap.servers" not in kafka_config:
            raise ValueError("Kafka bootstrap servers are required")

        if "sasl.username" not in kafka_config and args.sasl_username:
            kafka_config["sasl.username"] = args.sasl_username
            kafka_config["sasl.password"] = args.sasl_password or ""
            kafka_config["sasl.mechanisms"] = "PLAIN"
            kafka_config["security.protocol"] = "SASL_SSL" if kafka_enable_tls else "SASL_PLAINTEXT"
        elif "security.protocol" not in kafka_config:
            kafka_config["security.protocol"] = "SSL" if kafka_enable_tls else "PLAINTEXT"

        return kafka_config, kafka_topic

    def emit_reference_data(
        self,
        station_producer: BeIrcelineStationsEventProducer,
        timeseries_producer: BeIrcelineTimeseriesEventProducer,
    ) -> Dict[str, Timeseries]:
        """Fetch and emit stations first, then timeseries metadata."""
        stations = [self.normalize_station(item) for item in self.list_stations()]
        for station in stations:
            station_producer.send_be_irceline_station(
                _station_id=station.station_id,
                data=station,
                flush_producer=False,
            )
        station_producer.producer.flush()
        LOGGER.info("Sent %d IRCELINE station reference events", len(stations))

        timeseries_items = [self.normalize_timeseries(item) for item in self.list_timeseries()]
        for timeseries in timeseries_items:
            timeseries_producer.send_be_irceline_timeseries(
                _timeseries_id=timeseries.timeseries_id,
                data=timeseries,
                flush_producer=False,
            )
        timeseries_producer.producer.flush()
        LOGGER.info("Sent %d IRCELINE timeseries reference events", len(timeseries_items))

        return {item.timeseries_id: item for item in timeseries_items}

    def poll_observations(
        self,
        *,
        timeseries_by_id: Dict[str, Timeseries],
        producer: BeIrcelineTimeseriesEventProducer,
        state: Dict[str, int],
    ) -> int:
        """Poll recent values for each timeseries and emit only new observations."""
        observation_count = 0
        end_time = datetime.now(timezone.utc)

        for timeseries in timeseries_by_id.values():
            try:
                raw_values = self.get_timeseries_data(timeseries.timeseries_id, end_time=end_time)
                for raw_value in self.filter_new_observations(timeseries.timeseries_id, raw_values, state):
                    producer.send_be_irceline_observation(
                        _timeseries_id=timeseries.timeseries_id,
                        data=self.normalize_observation(timeseries, raw_value),
                        flush_producer=False,
                    )
                    observation_count += 1
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.warning(
                    "Could not fetch or emit observations for timeseries %s: %s",
                    timeseries.timeseries_id,
                    exc,
                )

        producer.producer.flush()
        return observation_count

    def run_feed(
        self,
        *,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        polling_interval: int,
        state_file: str,
    ) -> None:
        """Run the long-lived reference-data and observation polling loop."""
        producer = Producer(kafka_config)
        station_producer = BeIrcelineStationsEventProducer(producer, kafka_topic)
        timeseries_producer = BeIrcelineTimeseriesEventProducer(producer, kafka_topic)
        state = _load_state(state_file)
        last_reference_refresh = 0.0
        timeseries_by_id: Dict[str, Timeseries] = {}

        LOGGER.info(
            "Starting IRCELINE Belgium bridge for topic %s at bootstrap servers %s",
            kafka_topic,
            kafka_config["bootstrap.servers"],
        )

        try:
            while True:
                cycle_started = time.monotonic()
                now = time.time()

                if not timeseries_by_id or now - last_reference_refresh >= self.reference_refresh_interval:
                    timeseries_by_id = self.emit_reference_data(station_producer, timeseries_producer)
                    last_reference_refresh = now

                observation_count = self.poll_observations(
                    timeseries_by_id=timeseries_by_id,
                    producer=timeseries_producer,
                    state=state,
                )
                _save_state(state_file, state)

                elapsed = time.monotonic() - cycle_started
                sleep_seconds = max(0.0, polling_interval - elapsed)
                LOGGER.info(
                    "Sent %d observation events in %.1f seconds. Waiting %.1f seconds.",
                    observation_count,
                    elapsed,
                    sleep_seconds,
                )
                if sleep_seconds:
                    time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            LOGGER.info("Stopping IRCELINE Belgium bridge")
        finally:
            producer.flush()


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="IRCELINE Belgium air quality bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Poll IRCELINE and emit CloudEvents to Kafka")
    feed_parser.add_argument("--connection-string", type=str, default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC", IrcelineBelgiumAPI.DEFAULT_TOPIC))
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "3600")))
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.irceline_belgium_state.json")),
    )
    feed_parser.add_argument("--kafka-enable-tls", type=str, default=os.getenv("KAFKA_ENABLE_TLS", "true"))

    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return

    kafka_config, kafka_topic = IrcelineBelgiumAPI.build_kafka_config(args)
    api = IrcelineBelgiumAPI()
    api.run_feed(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        polling_interval=args.polling_interval,
        state_file=args.state_file,
    )


if __name__ == "__main__":
    main()
