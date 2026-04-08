"""Bridge FMI Finland air quality observations into Kafka as CloudEvents."""

from __future__ import annotations

import argparse
import json
import logging
import os
import time
import typing
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import requests
from confluent_kafka import Producer

from fmi_finland_producer_data import Observation, Station
from fmi_finland_producer_kafka_producer.producer import FiFmiOpendataAirqualityEventProducer

logger = logging.getLogger(__name__)

FMI_WFS_URL = "https://opendata.fmi.fi/wfs"
STATIONS_STORED_QUERY = "fmi::ef::stations"
OBSERVATIONS_STORED_QUERY = "urban::observations::airquality::hourly::simple"
DEFAULT_TOPIC = "fmi-finland-airquality"
DEFAULT_POLLING_INTERVAL = 3600
DEFAULT_STATION_REFRESH_INTERVAL = 86400

NAMESPACES = {
    "wfs": "http://www.opengis.net/wfs/2.0",
    "gml": "http://www.opengis.net/gml/3.2",
    "BsWfs": "http://xml.fmi.fi/schema/wfs/2.0",
    "ef": "http://inspire.ec.europa.eu/schemas/ef/4.0",
}

PARAM_MAP = {
    "AQINDEX_PT1H_avg": "aqindex",
    "PM10_PT1H_avg": "pm10_ug_m3",
    "PM25_PT1H_avg": "pm2_5_ug_m3",
    "NO2_PT1H_avg": "no2_ug_m3",
    "O3_PT1H_avg": "o3_ug_m3",
    "SO2_PT1H_avg": "so2_ug_m3",
    "CO_PT1H_avg": "co_mg_m3",
}


@dataclass(frozen=True)
class StationMetadata:
    """Station metadata resolved from the FMI station registry."""

    fmisid: str
    station_name: str
    latitude: float
    longitude: float
    municipality: str | None


@dataclass
class StationRegistry:
    """Lookup tables for station resolution."""

    by_id: dict[str, StationMetadata]
    by_coord: dict[tuple[str, str], list[str]]


class FMIAirQualityAPI:
    """Client for FMI OGC WFS air quality endpoints."""

    def __init__(
        self,
        base_url: str = FMI_WFS_URL,
        timeout: int = 60,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.session = session or requests.Session()

    def _get(self, params: dict[str, str]) -> str:
        response = self.session.get(self.base_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def get_station_metadata_xml(self) -> str:
        """Fetch station registry metadata."""
        return self._get(
            {
                "service": "WFS",
                "version": "2.0.0",
                "request": "getFeature",
                "storedquery_id": STATIONS_STORED_QUERY,
            }
        )

    def get_observations_xml(self, start_time: str, end_time: str) -> str:
        """Fetch hourly air quality observations in simple WFS format."""
        return self._get(
            {
                "service": "WFS",
                "version": "2.0.0",
                "request": "getFeature",
                "storedquery_id": OBSERVATIONS_STORED_QUERY,
                "starttime": start_time,
                "endtime": end_time,
            }
        )

    def get_station_registry(self) -> StationRegistry:
        """Fetch and parse the station registry."""
        return parse_station_metadata(self.get_station_metadata_xml())


def parse_connection_string(connection_string: str) -> dict[str, str]:
    """Parse Event Hubs or plain Kafka connection strings."""
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


def _coord_key(latitude: float, longitude: float, precision: int = 5) -> tuple[str, str]:
    return (f"{latitude:.{precision}f}", f"{longitude:.{precision}f}")


def _safe_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text or text.lower() == "nan":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _measurement_arg(value: float | None) -> str | None:
    """Pass floats as strings so generated __post_init__ keeps zero values."""
    if value is None:
        return None
    return format(value, ".15g")


def _flush_event_producer(event_producer: typing.Any) -> None:
    producer = getattr(event_producer, "producer", None)
    if producer is not None and hasattr(producer, "flush"):
        producer.flush()


def _find_named_value(parent: ET.Element, code_space_suffix: str) -> str | None:
    for name_elem in parent.findall("gml:name", NAMESPACES):
        if name_elem.get("codeSpace", "").endswith(code_space_suffix):
            text = (name_elem.text or "").strip()
            if text:
                return text
    return None


def parse_station_metadata(xml_text: str) -> StationRegistry:
    """Parse FMI station metadata into lookup tables."""
    root = ET.fromstring(xml_text)
    by_id: dict[str, StationMetadata] = {}
    by_coord: dict[tuple[str, str], list[str]] = {}

    for facility in root.findall(".//ef:EnvironmentalMonitoringFacility", NAMESPACES):
        identifier_elem = facility.find("gml:identifier", NAMESPACES)
        fmisid = (identifier_elem.text or "").strip() if identifier_elem is not None else ""
        if not fmisid:
            continue

        station_name = (facility.findtext("ef:name", default="", namespaces=NAMESPACES) or "").strip()
        if not station_name:
            station_name = _find_named_value(facility, "/name") or fmisid

        municipality = _find_named_value(facility, "/region")
        pos_elem = facility.find(".//ef:representativePoint//gml:pos", NAMESPACES)
        if pos_elem is None or not pos_elem.text:
            continue

        coords = pos_elem.text.strip().split()
        if len(coords) < 2:
            continue

        latitude = float(coords[0])
        longitude = float(coords[1])
        station = StationMetadata(
            fmisid=fmisid,
            station_name=station_name,
            latitude=latitude,
            longitude=longitude,
            municipality=municipality,
        )
        by_id[fmisid] = station
        by_coord.setdefault(_coord_key(latitude, longitude), []).append(fmisid)

    return StationRegistry(by_id=by_id, by_coord=by_coord)


def _resolve_fmisid(
    gml_id: str,
    latitude: float | None,
    longitude: float | None,
    registry: StationRegistry,
) -> str | None:
    numeric_candidates = [
        part for part in gml_id.split(".") if part.isdigit() and len(part) >= 5
    ]
    for candidate in numeric_candidates:
        if candidate in registry.by_id:
            return candidate

    if latitude is not None and longitude is not None:
        coord_candidates = registry.by_coord.get(_coord_key(latitude, longitude), [])
        if len(coord_candidates) == 1:
            return coord_candidates[0]
        if numeric_candidates:
            for candidate in numeric_candidates:
                if candidate in coord_candidates:
                    return candidate

    return numeric_candidates[0] if numeric_candidates else None


def parse_observations_xml(
    xml_text: str,
    registry: StationRegistry,
) -> tuple[dict[str, StationMetadata], list[dict[str, typing.Any]]]:
    """Parse simple-format WFS observations and aggregate by station and hour."""
    root = ET.fromstring(xml_text)
    aggregates: dict[tuple[str, str], dict[str, typing.Any]] = {}
    discovered_stations: dict[str, StationMetadata] = {}

    for elem in root.findall(".//BsWfs:BsWfsElement", NAMESPACES):
        gml_id = elem.get("{http://www.opengis.net/gml/3.2}id", "")
        location_elem = elem.find(".//gml:pos", NAMESPACES)

        latitude = None
        longitude = None
        if location_elem is not None and location_elem.text:
            coords = location_elem.text.strip().split()
            if len(coords) >= 2:
                latitude = float(coords[0])
                longitude = float(coords[1])

        fmisid = _resolve_fmisid(gml_id, latitude, longitude, registry)
        if not fmisid:
            logger.warning("Skipping observation element with unresolved station id: %s", gml_id)
            continue

        station = registry.by_id.get(fmisid)
        if station is None:
            if latitude is None or longitude is None:
                logger.warning("Skipping station %s because coordinates are missing and metadata lookup failed", fmisid)
                continue
            station = StationMetadata(
                fmisid=fmisid,
                station_name=fmisid,
                latitude=latitude,
                longitude=longitude,
                municipality=None,
            )
        discovered_stations[fmisid] = station

        observation_time = elem.findtext("BsWfs:Time", default="", namespaces=NAMESPACES).strip()
        if not observation_time:
            continue

        key = (fmisid, observation_time)
        aggregate = aggregates.setdefault(
            key,
            {
                "fmisid": fmisid,
                "station_name": station.station_name or fmisid,
                "observation_time": observation_time,
                "aqindex": None,
                "pm10_ug_m3": None,
                "pm2_5_ug_m3": None,
                "no2_ug_m3": None,
                "o3_ug_m3": None,
                "so2_ug_m3": None,
                "co_mg_m3": None,
            },
        )

        param_name = elem.findtext("BsWfs:ParameterName", default="", namespaces=NAMESPACES).strip()
        mapped_field = PARAM_MAP.get(param_name)
        if not mapped_field:
            continue

        param_value = _safe_float(elem.findtext("BsWfs:ParameterValue", default=None, namespaces=NAMESPACES))
        aggregate[mapped_field] = param_value

    return discovered_stations, sorted(aggregates.values(), key=lambda item: (item["observation_time"], item["fmisid"]))


def _observation_window(now: datetime | None = None) -> tuple[str, str]:
    current = now or datetime.now(timezone.utc)
    window_end = current.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    window_start = window_end - timedelta(hours=1)
    return (
        window_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        window_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def _load_state(state_file: str) -> dict[str, typing.Any]:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as handle:
                data = json.load(handle)
                if isinstance(data, dict):
                    return data
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.warning("Could not load state file %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict[str, typing.Any]) -> None:
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.warning("Could not save state file %s: %s", state_file, exc)


def send_station_events(
    stations: dict[str, StationMetadata],
    event_producer: typing.Any,
    known_station_ids: set[str] | None = None,
    force: bool = False,
) -> int:
    """Emit station reference events."""
    sent = 0
    if known_station_ids is None:
        known_station_ids = set()

    for fmisid in sorted(stations):
        if not force and fmisid in known_station_ids:
            continue
        station = stations[fmisid]
        event_producer.send_fi_fmi_opendata_airquality_station(
            station.fmisid,
            Station(
                fmisid=station.fmisid,
                station_name=station.station_name,
                latitude=station.latitude,
                longitude=station.longitude,
                municipality=station.municipality,
            ),
            flush_producer=False,
        )
        known_station_ids.add(fmisid)
        sent += 1

    if sent:
        _flush_event_producer(event_producer)
    return sent


def emit_observation_events(
    observations: list[dict[str, typing.Any]],
    event_producer: typing.Any,
    previous_fingerprints: dict[str, str],
) -> int:
    """Emit deduplicated observation events."""
    sent = 0

    for observation in observations:
        key = f"{observation['fmisid']}:{observation['observation_time']}"
        fingerprint = json.dumps(observation, sort_keys=True)
        if previous_fingerprints.get(key) == fingerprint:
            continue

        event_producer.send_fi_fmi_opendata_airquality_observation(
            observation["fmisid"],
            Observation(
                fmisid=observation["fmisid"],
                station_name=observation["station_name"],
                observation_time=observation["observation_time"],
                aqindex=_measurement_arg(observation["aqindex"]),
                pm10_ug_m3=_measurement_arg(observation["pm10_ug_m3"]),
                pm2_5_ug_m3=_measurement_arg(observation["pm2_5_ug_m3"]),
                no2_ug_m3=_measurement_arg(observation["no2_ug_m3"]),
                o3_ug_m3=_measurement_arg(observation["o3_ug_m3"]),
                so2_ug_m3=_measurement_arg(observation["so2_ug_m3"]),
                co_mg_m3=_measurement_arg(observation["co_mg_m3"]),
            ),
            flush_producer=False,
        )
        previous_fingerprints[key] = fingerprint
        sent += 1

    if sent:
        _flush_event_producer(event_producer)
    return sent


def run_feed_cycle(
    api: FMIAirQualityAPI,
    event_producer: typing.Any,
    state: dict[str, typing.Any],
    *,
    now: datetime | None = None,
    force_station_emit: bool = False,
) -> dict[str, int]:
    """Run one reference-data and observation emission cycle."""
    registry = api.get_station_registry()
    start_time, end_time = _observation_window(now)
    stations, observations = parse_observations_xml(api.get_observations_xml(start_time, end_time), registry)

    known_station_ids = set(state.setdefault("known_station_ids", []))
    previous_fingerprints = state.setdefault("observation_fingerprints", {})

    station_count = send_station_events(
        stations,
        event_producer,
        known_station_ids=known_station_ids,
        force=force_station_emit,
    )
    observation_count = emit_observation_events(observations, event_producer, previous_fingerprints)

    state["known_station_ids"] = sorted(known_station_ids)
    return {
        "stations": station_count,
        "observations": observation_count,
    }


def _build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    if args.connection_string:
        kafka_config = parse_connection_string(args.connection_string)
    else:
        kafka_config = {}

    if args.kafka_bootstrap_servers:
        kafka_config["bootstrap.servers"] = args.kafka_bootstrap_servers
    elif os.getenv("KAFKA_BROKER") and "bootstrap.servers" not in kafka_config:
        kafka_config["bootstrap.servers"] = os.environ["KAFKA_BROKER"]

    if args.sasl_username:
        kafka_config["sasl.username"] = args.sasl_username
    if args.sasl_password:
        kafka_config["sasl.password"] = args.sasl_password
    if args.sasl_username or args.sasl_password:
        kafka_config.setdefault("security.protocol", "SASL_SSL")
        kafka_config.setdefault("sasl.mechanism", "PLAIN")

    topic = args.kafka_topic or kafka_config.pop("_entity_path", DEFAULT_TOPIC)
    if "bootstrap.servers" not in kafka_config:
        raise ValueError("Kafka bootstrap servers are required.")
    return kafka_config, topic


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="FMI Finland air quality bridge")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List FMI stations from the station registry")

    feed_parser = subparsers.add_parser("feed", help="Poll FMI air quality data and publish CloudEvents")
    feed_parser.add_argument(
        "--connection-string",
        default=os.getenv("CONNECTION_STRING"),
        help="Kafka or Event Hubs style connection string",
    )
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma-separated Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        "--kafka-topic",
        default=os.getenv("KAFKA_TOPIC"),
        help=f"Kafka topic name. Default: {DEFAULT_TOPIC}",
    )
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLLING_INTERVAL))),
        help="Polling interval in seconds.",
    )
    feed_parser.add_argument(
        "--station-refresh-interval",
        type=int,
        default=int(os.getenv("STATION_REFRESH_INTERVAL", str(DEFAULT_STATION_REFRESH_INTERVAL))),
        help="How often to re-emit reference station data in seconds.",
    )
    feed_parser.add_argument(
        "--state-file",
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.fmi_finland_state.json")),
        help="JSON file used for deduplication state.",
    )

    args = parser.parse_args()
    _configure_logging()

    api = FMIAirQualityAPI()

    if args.command == "list":
        registry = api.get_station_registry()
        for station in sorted(registry.by_id.values(), key=lambda item: item.fmisid):
            municipality = f" ({station.municipality})" if station.municipality else ""
            print(f"{station.fmisid}: {station.station_name}{municipality} [{station.latitude}, {station.longitude}]")
        return

    if args.command != "feed":
        parser.print_help()
        return

    kafka_config, topic = _build_kafka_config(args)
    event_producer = FiFmiOpendataAirqualityEventProducer(Producer(kafka_config), topic)

    state = _load_state(args.state_file)
    last_station_emit = state.get("last_station_emit")
    last_station_emit_dt = (
        datetime.fromisoformat(last_station_emit) if isinstance(last_station_emit, str) else None
    )

    while True:
        cycle_started = datetime.now(timezone.utc)
        try:
            force_station_emit = (
                last_station_emit_dt is None
                or (cycle_started - last_station_emit_dt).total_seconds() >= args.station_refresh_interval
            )
            counts = run_feed_cycle(
                api,
                event_producer,
                state,
                now=cycle_started,
                force_station_emit=force_station_emit,
            )
            if force_station_emit:
                last_station_emit_dt = cycle_started
                state["last_station_emit"] = cycle_started.isoformat()
            _save_state(args.state_file, state)
            logger.info(
                "Sent %s station events and %s observation events for window %s to %s",
                counts["stations"],
                counts["observations"],
                *_observation_window(cycle_started),
            )
        except KeyboardInterrupt:
            logger.info("Stopping FMI Finland bridge")
            break
        except Exception as exc:  # pragma: no cover - runtime resiliency
            logger.exception("Feed cycle failed: %s", exc)

        sleep_seconds = max(
            0,
            args.polling_interval - (datetime.now(timezone.utc) - cycle_started).total_seconds(),
        )
        time.sleep(sleep_seconds)
