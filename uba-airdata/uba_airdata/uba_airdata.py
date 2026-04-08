"""UBA Germany Air Quality Bridge."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import json
import logging
import os
import sys
import time
from typing import Any
from zoneinfo import ZoneInfo

import requests
from confluent_kafka import Producer

from uba_airdata_producer_kafka_producer.producer import (
    DeUbaAirdataComponentsEventProducer,
    DeUbaAirdataEventProducer,
)

logger = logging.getLogger(__name__)

UBA_API_BASE = "https://www.umweltbundesamt.de/api/air_data/v3"
BERLIN_TZ = ZoneInfo("Europe/Berlin")

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def _load_state(state_file: str) -> dict[str, str]:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return {str(key): str(value) for key, value in data.items()}
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict[str, str]) -> None:
    """Persist dedup state to a JSON file."""
    if not state_file:
        return
    try:
        if len(data) > 200000:
            keys = list(data.keys())[-100000:]
            data = {key: data[key] for key in keys}
        with open(state_file, "w", encoding="utf-8") as file:
            json.dump(data, file)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Could not save state to %s: %s", state_file, exc)


def _normalize_optional_string(value: Any) -> str | None:
    """Normalize blank strings to null."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _as_int(value: Any) -> int:
    """Convert a source value to int."""
    return int(str(value))


def _as_float(value: Any) -> float:
    """Convert a source value to float."""
    return float(str(value))


class UBAAirDataAPI:
    """Client for the UBA Germany air quality API."""

    def __init__(self, base_url: str = UBA_API_BASE, polling_interval: int = 3600, scope_id: int = 2):
        self.base_url = base_url.rstrip("/")
        self.polling_interval = polling_interval
        self.scope_id = scope_id
        self.session = requests.Session()

    def parse_connection_string(self, connection_string: str) -> dict[str, str]:
        """Parse Event Hubs, Fabric, or plain Kafka style connection strings."""
        config_dict: dict[str, str] = {}
        try:
            for part in connection_string.split(";"):
                part = part.strip()
                if not part:
                    continue
                if "Endpoint" in part:
                    config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip('"').strip().replace("sb://", "").replace("/", "") + ":9093"
                elif "EntityPath" in part:
                    config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"').strip()
                elif "SharedAccessKeyName" in part:
                    config_dict["sasl.username"] = "$ConnectionString"
                elif "SharedAccessKey" in part:
                    config_dict["sasl.password"] = connection_string.strip()
                elif "BootstrapServer" in part:
                    config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
        except IndexError as exc:
            raise ValueError("Invalid connection string format") from exc
        if "sasl.username" in config_dict:
            config_dict["security.protocol"] = "SASL_SSL"
            config_dict["sasl.mechanism"] = "PLAIN"
        return config_dict

    def get_stations_payload(self) -> dict[str, Any]:
        """Fetch the station catalog."""
        response = self.session.get(f"{self.base_url}/stations/json", params={"lang": "en"}, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_components_payload(self) -> dict[str, Any]:
        """Fetch the component catalog."""
        response = self.session.get(f"{self.base_url}/components/json", params={"lang": "en"}, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_measures_payload(self, component_id: int, date_from: str, date_to: str) -> dict[str, Any]:
        """Fetch hourly measures for one pollutant component."""
        response = self.session.get(
            f"{self.base_url}/measures/json",
            params={
                "component": str(component_id),
                "scope": str(self.scope_id),
                "date_from": date_from,
                "date_to": date_to,
                "lang": "en",
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_station_data(payload: dict[str, Any]) -> list[Any]:
        """Parse the UBA indexed station payload into generated Station objects."""
        from uba_airdata_producer_data import Station

        indices = payload.get("indices", [])
        stations: list[Any] = []
        for station_id, values in payload.get("data", {}).items():
            row = dict(zip(indices, values))
            stations.append(
                Station(
                    station_id=_as_int(row.get("station id", station_id)),
                    station_code=str(row.get("station code", "")),
                    station_name=str(row.get("station name", "")),
                    station_city=str(row.get("station city", "")),
                    station_synonym=_normalize_optional_string(row.get("station synonym")),
                    active_from=str(row.get("station active from", "")),
                    active_to=_normalize_optional_string(row.get("station active to")),
                    longitude=_as_float(row.get("station longitude")),
                    latitude=_as_float(row.get("station latitude")),
                    network_id=_as_int(row.get("network id")),
                    network_code=str(row.get("network code", "")),
                    network_name=str(row.get("network name", "")),
                    setting_name=str(row.get("station setting name", "")),
                    setting_short=str(row.get("station setting short name", "")),
                    type_name=str(row.get("station type name", "")),
                    street=_normalize_optional_string(row.get("station street")),
                    street_nr=_normalize_optional_string(row.get("station street nr")),
                    zip_code=_normalize_optional_string(row.get("station zip code")),
                )
            )
        return stations

    @staticmethod
    def parse_component_data(payload: dict[str, Any]) -> list[Any]:
        """Parse the peculiar top-level keyed component payload."""
        from uba_airdata_producer_data import Component

        indices = payload.get("indices", [])
        components: list[Any] = []
        for key, values in payload.items():
            if key in {"count", "indices"} or not key.isdigit():
                continue
            row = dict(zip(indices, values))
            components.append(
                Component(
                    component_id=_as_int(row.get("component id", key)),
                    component_code=str(row.get("component code", "")),
                    symbol=str(row.get("component symbol", "")),
                    unit=str(row.get("component unit", "")),
                    name=str(row.get("component name", "")),
                )
            )
        return components

    @staticmethod
    def parse_measure_data(payload: dict[str, Any], active_station_ids: set[int] | None = None) -> list[Any]:
        """Parse station/date keyed measurement payload into generated Measure objects."""
        from uba_airdata_producer_data import Measure

        measures: list[Any] = []
        for station_id_text, slots in payload.get("data", {}).items():
            station_id = _as_int(station_id_text)
            if active_station_ids is not None and station_id not in active_station_ids:
                continue
            for date_start, values in slots.items():
                value = values[2]
                measures.append(
                    Measure(
                        station_id=station_id,
                        component_id=_as_int(values[0]),
                        scope_id=_as_int(values[1]),
                        date_start=str(date_start),
                        date_end=str(values[3]),
                        value=float(value) if value is not None else None,
                        quality_index=str(values[4]) if values[4] is not None else "",
                    )
                )
        return measures


def _build_kafka_config(args: argparse.Namespace, api: UBAAirDataAPI) -> tuple[dict[str, str], str]:
    """Build Kafka config from args and environment."""
    kafka_config: dict[str, str] = {}
    kafka_topic = args.kafka_topic or ""

    if args.connection_string:
        parsed = api.parse_connection_string(args.connection_string)
        kafka_topic = kafka_topic or parsed.pop("kafka_topic", "")
        kafka_config.update(parsed)

    if args.kafka_bootstrap_servers:
        kafka_config["bootstrap.servers"] = args.kafka_bootstrap_servers
    if args.sasl_username:
        kafka_config["sasl.username"] = args.sasl_username
    if args.sasl_password:
        kafka_config["sasl.password"] = args.sasl_password

    kafka_enable_tls = str(os.getenv("KAFKA_ENABLE_TLS", "true")).lower() not in {"false", "0", "no"}
    if "sasl.username" in kafka_config:
        kafka_config["security.protocol"] = "SASL_SSL" if kafka_enable_tls else "SASL_PLAINTEXT"
        kafka_config["sasl.mechanism"] = "PLAIN"
    elif not kafka_enable_tls:
        kafka_config["security.protocol"] = "PLAINTEXT"

    if "bootstrap.servers" not in kafka_config or not kafka_topic:
        raise ValueError("Kafka bootstrap servers and topic must be configured")

    return kafka_config, kafka_topic


def _reference_urls(base_url: str) -> tuple[str, str]:
    """Return the canonical feed URLs for reference events."""
    return (
        f"{base_url}/stations/json?lang=en",
        f"{base_url}/components/json?lang=en",
    )


def _measure_date_range() -> tuple[str, str]:
    """Return the current local Berlin date range covering roughly the last 24 hours."""
    now = datetime.now(BERLIN_TZ)
    return ((now - timedelta(days=1)).date().isoformat(), now.date().isoformat())


def _measure_feed_url(base_url: str, component_id: int, scope_id: int, date_from: str, date_to: str) -> str:
    """Build a deterministic measure feed URL used as CloudEvents source."""
    return (
        f"{base_url}/measures/json?component={component_id}"
        f"&scope={scope_id}&date_from={date_from}&date_to={date_to}&lang=en"
    )


def send_reference_data(
    api: UBAAirDataAPI,
    station_producer: DeUbaAirdataEventProducer,
    component_producer: DeUbaAirdataComponentsEventProducer,
) -> tuple[list[Any], list[Any], set[int]]:
    """Fetch and emit reference data."""
    stations_payload = api.get_stations_payload()
    components_payload = api.get_components_payload()

    stations = api.parse_station_data(stations_payload)
    components = api.parse_component_data(components_payload)

    stations_url, components_url = _reference_urls(api.base_url)

    for station in stations:
        station_producer.send_de_uba_airdata_station(
            _feedurl=stations_url,
            _station_id=station.station_id,
            data=station,
            flush_producer=False,
        )
    station_producer.producer.flush()

    for component in components:
        component_producer.send_de_uba_airdata_components_component(
            _feedurl=components_url,
            _component_id=component.component_id,
            data=component,
            flush_producer=False,
        )
    component_producer.producer.flush()

    active_station_ids = {station.station_id for station in stations if station.active_to is None}
    logger.info(
        "Sent %d station events, %d component events, %d active stations",
        len(stations),
        len(components),
        len(active_station_ids),
    )
    return stations, components, active_station_ids


def feed_measures(
    api: UBAAirDataAPI,
    station_producer: DeUbaAirdataEventProducer,
    components: list[Any],
    active_station_ids: set[int],
    previous_readings: dict[str, str],
) -> int:
    """Fetch and emit new measures."""
    sent = 0
    date_from, date_to = _measure_date_range()
    for component in components:
        payload = api.get_measures_payload(component.component_id, date_from, date_to)
        measures = api.parse_measure_data(payload, active_station_ids)
        feed_url = _measure_feed_url(api.base_url, component.component_id, api.scope_id, date_from, date_to)
        for measure in measures:
            dedupe_key = f"{measure.station_id}:{measure.component_id}:{measure.date_start}"
            if dedupe_key in previous_readings:
                continue
            station_producer.send_de_uba_airdata_measure(
                _feedurl=feed_url,
                _station_id=measure.station_id,
                data=measure,
                flush_producer=False,
            )
            previous_readings[dedupe_key] = measure.date_end
            sent += 1
    station_producer.producer.flush()
    return sent


def main() -> None:
    """Run the UBA AirData bridge."""
    parser = argparse.ArgumentParser(description="Bridge UBA Germany air quality data into Kafka.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed UBA air quality data as CloudEvents")
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
        "-c",
        "--connection-string",
        type=str,
        default=os.getenv("CONNECTION_STRING"),
        help="Microsoft Event Hubs, Fabric, or plain Kafka connection string",
    )
    feed_parser.add_argument(
        "-i",
        "--polling-interval",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", "3600")),
        help="Polling interval in seconds",
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.uba_airdata_state.json")),
        help="Path of the local dedup state file",
    )
    feed_parser.add_argument(
        "--reference-refresh-polls",
        type=int,
        default=int(os.getenv("REFERENCE_REFRESH_POLLS", "24")),
        help="Number of telemetry polls between reference refreshes",
    )

    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return

    api = UBAAirDataAPI(polling_interval=args.polling_interval)
    kafka_config, kafka_topic = _build_kafka_config(args, api)
    previous_readings = _load_state(args.state_file)

    producer = Producer(kafka_config)
    station_producer = DeUbaAirdataEventProducer(producer, kafka_topic)
    component_producer = DeUbaAirdataComponentsEventProducer(producer, kafka_topic)

    logger.info(
        "Starting UBA AirData feed for topic %s at bootstrap servers %s",
        kafka_topic,
        kafka_config["bootstrap.servers"],
    )

    _stations, components, active_station_ids = send_reference_data(api, station_producer, component_producer)
    poll_count = 0

    while True:
        cycle_started = time.monotonic()
        try:
            if poll_count > 0 and poll_count % args.reference_refresh_polls == 0:
                _stations, components, active_station_ids = send_reference_data(api, station_producer, component_producer)
            sent = feed_measures(api, station_producer, components, active_station_ids, previous_readings)
            _save_state(args.state_file, previous_readings)
            poll_count += 1
            elapsed = time.monotonic() - cycle_started
            sleep_seconds = max(0.0, float(args.polling_interval) - elapsed)
            logger.info("Sent %d measure events in %.2f seconds; sleeping %.2f seconds", sent, elapsed, sleep_seconds)
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            logger.info("Exiting on keyboard interrupt")
            break
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Polling cycle failed: %s", exc)
            _save_state(args.state_file, previous_readings)
            time.sleep(args.polling_interval)

    producer.flush()
