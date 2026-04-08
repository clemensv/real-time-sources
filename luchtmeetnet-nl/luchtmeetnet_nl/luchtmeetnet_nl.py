"""Bridge Luchtmeetnet Netherlands air quality data into Kafka as CloudEvents."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from typing import Any

import requests
from confluent_kafka import Producer
from luchtmeetnet_nl_producer_data import Component, LKI, Measurement, Station
from luchtmeetnet_nl_producer_kafka_producer.producer import (
    NlRivmLuchtmeetnetComponentsEventProducer,
    NlRivmLuchtmeetnetEventProducer,
)


LOGGER = logging.getLogger(__name__)


def _load_state(state_file: str) -> dict[str, str]:
    """Load persisted dedup state from a JSON file."""
    if not state_file:
        return {}

    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                data = json.load(handle)
                return data if isinstance(data, dict) else {}
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict[str, str]) -> None:
    """Save dedup state to a JSON file."""
    if not state_file:
        return

    try:
        with open(state_file, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.warning("Could not save state to %s: %s", state_file, exc)


def _iso_to_epoch(value: str | None) -> float:
    if not value:
        return float("-inf")
    return __import__("datetime").datetime.fromisoformat(value).timestamp()


@dataclass
class ReferenceSnapshot:
    stations: list[Station]
    components: list[Component]


class LuchtmeetnetAPI:
    """Polling bridge for the public Luchtmeetnet REST API."""

    def __init__(self, base_url: str = "https://api.luchtmeetnet.nl/open_api", session: requests.Session | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def _request_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def list_stations(self, page: int = 1) -> dict[str, Any]:
        """Return a paged station listing response."""
        return self._request_json("/stations", params={"page": page})

    def get_station_detail(self, station_number: str) -> dict[str, Any]:
        """Return detail data for a station."""
        return self._request_json(f"/stations/{station_number}")

    def list_components(self) -> list[dict[str, Any]]:
        """Return the full component catalog."""
        response = self._request_json("/components")
        return response.get("data", [])

    def get_measurements(self, station_number: str, formula: str) -> list[dict[str, Any]]:
        """Return page-1 measurements for a station and formula."""
        response = self._request_json(
            "/measurements",
            params={"station_number": station_number, "formula": formula, "page": 1},
        )
        return response.get("data", [])

    def get_lki(self, station_number: str) -> list[dict[str, Any]]:
        """Return page-1 LKI values for a station."""
        response = self._request_json("/lki", params={"station_number": station_number, "page": 1})
        return response.get("data", [])

    def fetch_all_stations(self, limit: int | None = None) -> list[Station]:
        """Fetch all station summaries and detail records."""
        first_page = self.list_stations(page=1)
        all_items = list(first_page.get("data", []))
        last_page = first_page.get("pagination", {}).get("last_page", 1)

        for page in range(2, last_page + 1):
            if limit is not None and len(all_items) >= limit:
                break
            all_items.extend(self.list_stations(page=page).get("data", []))

        if limit is not None:
            all_items = all_items[:limit]

        stations: list[Station] = []
        for summary in all_items:
            detail = self.get_station_detail(summary["number"]).get("data", {})
            coordinates = detail.get("geometry", {}).get("coordinates", [0.0, 0.0])
            stations.append(
                Station(
                    station_number=summary["number"],
                    location=detail.get("location") or summary.get("location", ""),
                    type=detail.get("type", ""),
                    organisation=detail.get("organisation", ""),
                    municipality=detail.get("municipality"),
                    province=detail.get("province"),
                    longitude=float(coordinates[0]),
                    latitude=float(coordinates[1]),
                    year_start=detail.get("year_start", ""),
                    components=list(detail.get("components", [])),
                )
            )
        return stations

    def fetch_all_components(self) -> list[Component]:
        """Fetch the component catalog as generated data classes."""
        components = []
        for item in self.list_components():
            names = item.get("name", {})
            components.append(
                Component(
                    formula=item.get("formula", ""),
                    name_nl=names.get("NL", ""),
                    name_en=names.get("EN", ""),
                )
            )
        return components

    def fetch_reference_snapshot(self, station_limit: int | None = None) -> ReferenceSnapshot:
        """Fetch station and component reference data."""
        return ReferenceSnapshot(
            stations=self.fetch_all_stations(limit=station_limit),
            components=self.fetch_all_components(),
        )

    def emit_reference_data(
        self,
        snapshot: ReferenceSnapshot,
        station_producer: NlRivmLuchtmeetnetEventProducer,
        component_producer: NlRivmLuchtmeetnetComponentsEventProducer,
        kafka_producer: Producer,
    ) -> None:
        """Emit reference events before telemetry starts."""
        for station in snapshot.stations:
            station_producer.send_nl_rivm_luchtmeetnet_station(
                _station_number=station.station_number,
                data=station,
                flush_producer=False,
            )
        for component in snapshot.components:
            component_producer.send_nl_rivm_luchtmeetnet_components_component(
                _formula=component.formula,
                data=component,
                flush_producer=False,
            )
        kafka_producer.flush()

    def emit_telemetry_once(
        self,
        stations: list[Station],
        station_producer: NlRivmLuchtmeetnetEventProducer,
        state: dict[str, str],
    ) -> tuple[int, int]:
        """Fetch and emit new measurement and LKI events once."""
        measurement_count = 0
        lki_count = 0

        for station in stations:
            for formula in station.components:
                try:
                    measurement_rows = self.get_measurements(station.station_number, formula)
                except requests.RequestException as exc:
                    LOGGER.warning("Measurement fetch failed for %s %s: %s", station.station_number, formula, exc)
                    continue

                measurement_key = f"measurement:{station.station_number}:{formula}"
                last_seen = state.get(measurement_key)
                newest_seen = last_seen

                for row in reversed(measurement_rows):
                    timestamp = row.get("timestamp_measured")
                    if _iso_to_epoch(timestamp) <= _iso_to_epoch(last_seen):
                        continue
                    station_producer.send_nl_rivm_luchtmeetnet_measurement(
                        _station_number=station.station_number,
                        data=Measurement(
                            station_number=row.get("station_number", station.station_number),
                            formula=row.get("formula", formula),
                            value=row.get("value", 0.0),
                            timestamp_measured=timestamp,
                        ),
                        flush_producer=False,
                    )
                    measurement_count += 1
                    newest_seen = timestamp

                if newest_seen:
                    state[measurement_key] = newest_seen

            try:
                lki_rows = self.get_lki(station.station_number)
            except requests.RequestException as exc:
                LOGGER.warning("LKI fetch failed for %s: %s", station.station_number, exc)
                continue

            lki_key = f"lki:{station.station_number}"
            last_lki = state.get(lki_key)
            newest_lki = last_lki

            for row in reversed(lki_rows):
                timestamp = row.get("timestamp_measured")
                if _iso_to_epoch(timestamp) <= _iso_to_epoch(last_lki):
                    continue
                station_producer.send_nl_rivm_luchtmeetnet_lki(
                    _station_number=station.station_number,
                    data=LKI(
                        station_number=row.get("station_number", station.station_number),
                        value=row.get("value", 0),
                        timestamp_measured=timestamp,
                    ),
                    flush_producer=False,
                )
                lki_count += 1
                newest_lki = timestamp

            if newest_lki:
                state[lki_key] = newest_lki

        return measurement_count, lki_count

    def parse_connection_string(self, connection_string: str) -> dict[str, str]:
        """Parse Event Hubs, Fabric, or plain BootstrapServer connection strings."""
        config_dict: dict[str, str] = {}
        try:
            for part in connection_string.split(";"):
                if not part:
                    continue
                key, value = part.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"')
                if key == "Endpoint":
                    config_dict["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
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

    def feed(
        self,
        kafka_config: dict[str, str],
        kafka_topic: str,
        polling_interval: int,
        state_file: str = "",
        station_refresh_interval: int = 24,
        station_limit: int | None = None,
    ) -> None:
        """Run the reference-data emission and telemetry polling loop."""
        state = _load_state(state_file)
        kafka_producer = Producer(kafka_config)
        station_producer = NlRivmLuchtmeetnetEventProducer(kafka_producer, kafka_topic)
        component_producer = NlRivmLuchtmeetnetComponentsEventProducer(kafka_producer, kafka_topic)

        snapshot = self.fetch_reference_snapshot(station_limit=station_limit)
        self.emit_reference_data(snapshot, station_producer, component_producer, kafka_producer)
        LOGGER.info(
            "Sent %s station records and %s component records",
            len(snapshot.stations),
            len(snapshot.components),
        )

        poll_count = 0
        while True:
            started = time.monotonic()
            try:
                if poll_count and poll_count % station_refresh_interval == 0:
                    snapshot = self.fetch_reference_snapshot(station_limit=station_limit)
                    self.emit_reference_data(snapshot, station_producer, component_producer, kafka_producer)
                    LOGGER.info(
                        "Refreshed %s station records and %s component records",
                        len(snapshot.stations),
                        len(snapshot.components),
                    )

                measurement_count, lki_count = self.emit_telemetry_once(snapshot.stations, station_producer, state)
                kafka_producer.flush()
                _save_state(state_file, state)
                elapsed = time.monotonic() - started
                sleep_for = max(0.0, polling_interval - elapsed)
                LOGGER.info(
                    "Sent %s measurements and %s LKI values in %.1f seconds; sleeping %.1f seconds",
                    measurement_count,
                    lki_count,
                    elapsed,
                    sleep_for,
                )
                poll_count += 1
                if sleep_for:
                    time.sleep(sleep_for)
            except KeyboardInterrupt:
                LOGGER.info("Stopping bridge")
                break
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.exception("Polling loop failed: %s", exc)
                _save_state(state_file, state)
                time.sleep(polling_interval)

        kafka_producer.flush()


def _build_kafka_config(
    kafka_bootstrap_servers: str,
    sasl_username: str | None,
    sasl_password: str | None,
    tls_enabled: bool,
) -> dict[str, str]:
    config: dict[str, str] = {"bootstrap.servers": kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        config["security.protocol"] = "SSL"
    return config


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="Bridge Luchtmeetnet Netherlands air quality data into Kafka.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Emit reference and telemetry events to Kafka")
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma separated list of Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        "--kafka-topic",
        default=os.getenv("KAFKA_TOPIC"),
        help="Kafka topic to send messages to",
    )
    feed_parser.add_argument(
        "--sasl-username",
        default=os.getenv("SASL_USERNAME"),
        help="Username for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "--sasl-password",
        default=os.getenv("SASL_PASSWORD"),
        help="Password for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "-c",
        "--connection-string",
        default=os.getenv("CONNECTION_STRING"),
        help="Microsoft Event Hubs or Fabric Event Stream connection string",
    )
    feed_parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", "3600")),
        help="Polling interval in seconds",
    )
    feed_parser.add_argument(
        "--state-file",
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.luchtmeetnet_nl_state.json")),
        help="JSON file used to persist deduplication state",
    )
    feed_parser.add_argument(
        "--station-refresh-interval",
        type=int,
        default=int(os.getenv("STATION_REFRESH_INTERVAL", "24")),
        help="Refresh station metadata after this many telemetry polls",
    )
    feed_parser.add_argument(
        "--station-limit",
        type=int,
        default=int(os.getenv("STATION_LIMIT", "0")) or None,
        help="Optional cap on the number of stations to poll, mainly for testing and fair-use throttling",
    )

    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return

    api = LuchtmeetnetAPI()

    if args.connection_string:
        config_params = api.parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic") or args.kafka_topic
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config = _build_kafka_config(kafka_bootstrap_servers, sasl_username, sasl_password, tls_enabled)

    api.feed(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        polling_interval=args.polling_interval,
        state_file=args.state_file,
        station_refresh_interval=args.station_refresh_interval,
        station_limit=args.station_limit,
    )
