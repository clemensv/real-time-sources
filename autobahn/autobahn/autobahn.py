"""German Autobahn API bridge."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import aiohttp
from confluent_kafka import Producer


BASE_URL = "https://verkehr.autobahn.de/o/autobahn"
DEFAULT_KAFKA_TOPIC = "autobahn"
DEFAULT_POLL_INTERVAL_SECONDS = 300
DEFAULT_REQUEST_CONCURRENCY = 16
DEFAULT_STATE_FILE = os.path.expanduser("~/.autobahn_state.json")
SELECTION_SENTINEL = "*"

RESOURCE_RESPONSE_KEYS: dict[str, str] = {
    "roadworks": "roadworks",
    "warning": "warning",
    "closure": "closure",
    "parking_lorry": "parking_lorry",
    "electric_charging_station": "electric_charging_station",
    "webcam": "webcam",
}

EVENT_FAMILIES: dict[str, dict[str, Any]] = {
    "roadwork": {
        "resource": "roadworks",
        "display_types": {"ROADWORKS"},
        "schema": "RoadEvent",
        "method_stem": "roadwork",
    },
    "short_term_roadwork": {
        "resource": "roadworks",
        "display_types": {"SHORT_TERM_ROADWORKS"},
        "schema": "RoadEvent",
        "method_stem": "short_term_roadwork",
    },
    "warning": {
        "resource": "warning",
        "display_types": {"WARNING"},
        "schema": "WarningEvent",
        "method_stem": "warning",
    },
    "closure": {
        "resource": "closure",
        "display_types": {"CLOSURE"},
        "schema": "RoadEvent",
        "method_stem": "closure",
    },
    "entry_exit_closure": {
        "resource": "closure",
        "display_types": {"CLOSURE_ENTRY_EXIT"},
        "schema": "RoadEvent",
        "method_stem": "entry_exit_closure",
    },
    "weight_limit_35_restriction": {
        "resource": "closure",
        "display_types": {"WEIGHT_LIMIT_35"},
        "schema": "RoadEvent",
        "method_stem": "weight_limit35_restriction",
    },
    "parking_lorry": {
        "resource": "parking_lorry",
        "display_types": {"PARKING"},
        "schema": "ParkingLorry",
        "method_stem": "parking_lorry",
    },
    "electric_charging_station": {
        "resource": "electric_charging_station",
        "display_types": {"ELECTRIC_CHARGING_STATION"},
        "schema": "ChargingStation",
        "method_stem": "electric_charging_station",
    },
    "strong_electric_charging_station": {
        "resource": "electric_charging_station",
        "display_types": {"STRONG_ELECTRIC_CHARGING_STATION"},
        "schema": "ChargingStation",
        "method_stem": "strong_electric_charging_station",
    },
    "webcam": {
        "resource": "webcam",
        "display_types": {"WEBCAM"},
        "schema": "Webcam",
        "method_stem": "webcam",
    },
}

DISPLAY_TYPE_TO_FAMILY = {
    (config["resource"], display_type): family
    for family, config in EVENT_FAMILIES.items()
    for display_type in config["display_types"]
}

DEFAULT_RESOURCES = tuple(RESOURCE_RESPONSE_KEYS)


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


class FetchResult:
    """Single Autobahn API fetch result."""

    def __init__(
        self,
        road_id: str,
        resource_type: str,
        status: int,
        etag: Optional[str],
        items: list[dict[str, Any]],
        error: Optional[str] = None,
    ):
        self.road_id = road_id
        self.resource_type = resource_type
        self.status = status
        self.etag = etag
        self.items = items
        self.error = error


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def _parse_optional_int(value: Any) -> Optional[int]:
    if value in (None, "", "undefined"):
        return None
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _parse_optional_float(value: Any) -> Optional[float]:
    if value in (None, "", "undefined"):
        return None
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def _parse_optional_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    return None


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None and str(item) != ""]


def _serialize_json(value: Any) -> Optional[str]:
    if value in (None, [], {}):
        return None
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def _extract_coordinate(raw_coordinate: Any) -> tuple[Optional[float], Optional[float]]:
    if isinstance(raw_coordinate, dict):
        if "lat" in raw_coordinate or "long" in raw_coordinate:
            return (
                _parse_optional_float(raw_coordinate.get("lat")),
                _parse_optional_float(raw_coordinate.get("long")),
            )
        coordinates = raw_coordinate.get("coordinates")
        if isinstance(coordinates, list) and len(coordinates) >= 2:
            return (_parse_optional_float(coordinates[1]), _parse_optional_float(coordinates[0]))
    return (None, None)


def normalize_road_ids(roads: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for road in roads:
        value = str(road).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    return normalized


def parse_resources_argument(resources_value: str) -> tuple[str, ...]:
    if not resources_value or resources_value.strip() == SELECTION_SENTINEL:
        return DEFAULT_RESOURCES
    resources = tuple(resource.strip() for resource in resources_value.split(",") if resource.strip())
    unsupported = [resource for resource in resources if resource not in RESOURCE_RESPONSE_KEYS]
    if unsupported:
        supported = ", ".join(DEFAULT_RESOURCES)
        raise ValueError(f"Unsupported resources: {', '.join(unsupported)}. Supported resources: {supported}")
    return resources or DEFAULT_RESOURCES


def parse_roads_argument(roads_value: str) -> Optional[list[str]]:
    if not roads_value or roads_value.strip() == SELECTION_SENTINEL:
        return None
    return normalize_road_ids(roads_value.split(","))


def parse_connection_string(connection_string: str) -> dict[str, str]:
    config_dict: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
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


def determine_event_family(resource_type: str, display_type: Optional[str]) -> Optional[str]:
    if display_type:
        family = DISPLAY_TYPE_TO_FAMILY.get((resource_type, str(display_type)))
        if family:
            return family
    defaults = {
        "warning": "warning",
        "parking_lorry": "parking_lorry",
        "webcam": "webcam",
    }
    return defaults.get(resource_type)


def _normalize_common_fields(road_id: str, resource_type: str, raw_item: dict[str, Any]) -> Optional[dict[str, Any]]:
    identifier = raw_item.get("identifier")
    if not identifier:
        return None

    coordinate_lat, coordinate_lon = _extract_coordinate(raw_item.get("coordinate"))
    description_lines = _normalize_string_list(raw_item.get("description"))
    footer_lines = _normalize_string_list(raw_item.get("footer"))
    impact = raw_item.get("impact") if isinstance(raw_item.get("impact"), dict) else {}

    return {
        "identifier": str(identifier),
        "road_ids": [road_id],
        "resource_type": resource_type,
        "display_type": raw_item.get("display_type"),
        "title": raw_item.get("title"),
        "subtitle": raw_item.get("subtitle"),
        "description_lines": description_lines,
        "future": _parse_optional_bool(raw_item.get("future")),
        "is_blocked": _parse_optional_bool(raw_item.get("isBlocked")),
        "icon": raw_item.get("icon"),
        "start_lc_position": _parse_optional_int(raw_item.get("startLcPosition")),
        "start_timestamp": raw_item.get("startTimestamp"),
        "extent": raw_item.get("extent"),
        "point": raw_item.get("point"),
        "coordinate_lat": coordinate_lat,
        "coordinate_lon": coordinate_lon,
        "geometry_json": _serialize_json(raw_item.get("geometry")),
        "impact_lower": impact.get("lower"),
        "impact_upper": impact.get("upper"),
        "impact_symbols": _normalize_string_list(impact.get("symbols")),
        "route_recommendation_json": _serialize_json(raw_item.get("routeRecommendation")),
        "footer_lines": footer_lines,
        "amenity_descriptions": [
            str(entry.get("description"))
            for entry in raw_item.get("lorryParkingFeatureIcons", [])
            if isinstance(entry, dict) and entry.get("description")
        ],
        "delay_minutes": _parse_optional_int(raw_item.get("delayTimeValue")),
        "average_speed_kmh": _parse_optional_int(raw_item.get("averageSpeed")),
        "abnormal_traffic_type": raw_item.get("abnormalTrafficType"),
        "source_name": raw_item.get("source"),
        "operator_name": raw_item.get("operator"),
        "image_url": raw_item.get("imageurl"),
        "stream_url": raw_item.get("linkurl"),
    }


def _parse_parking_counts(description_lines: list[str]) -> tuple[Optional[int], Optional[int]]:
    car_spaces = None
    lorry_spaces = None
    for line in description_lines:
        car_match = re.search(r"PKW\s+Stellpl[aä]tze:\s*(\d+)", line, flags=re.IGNORECASE)
        lorry_match = re.search(r"LKW\s+Stellpl[aä]tze:\s*(\d+)", line, flags=re.IGNORECASE)
        if car_match:
            car_spaces = int(car_match.group(1))
        if lorry_match:
            lorry_spaces = int(lorry_match.group(1))
    return car_spaces, lorry_spaces


def parse_charging_points(description_lines: list[str]) -> tuple[Optional[str], Optional[int], Optional[str]]:
    non_empty = [line.strip() for line in description_lines if line.strip()]
    address_line = non_empty[1] if len(non_empty) > 1 else None

    charging_points: list[dict[str, Any]] = []
    current: Optional[dict[str, Any]] = None
    for line in description_lines:
        stripped = line.strip()
        if not stripped:
            continue
        header_match = re.match(r"Ladepunkt\s+(\d+):", stripped, flags=re.IGNORECASE)
        if header_match:
            if current is not None:
                charging_points.append(current)
            current = {
                "index": int(header_match.group(1)),
                "connectors": [],
            }
            continue
        if current is None:
            continue
        if stripped.lower().endswith("kw"):
            current["power_kw"] = _parse_optional_float(stripped.lower().replace("kw", "").strip())
            continue
        current["connectors"] = [part.strip() for part in stripped.split(",") if part.strip()]

    if current is not None:
        charging_points.append(current)

    if not charging_points:
        return address_line, None, None

    return address_line, len(charging_points), json.dumps(charging_points, separators=(",", ":"), ensure_ascii=False)


def _build_road_event_snapshot(common: dict[str, Any]) -> dict[str, Any]:
    return {
        "identifier": common["identifier"],
        "road_ids": common["road_ids"],
        "display_type": common["display_type"],
        "title": common["title"],
        "subtitle": common["subtitle"],
        "description_lines": common["description_lines"],
        "future": common["future"],
        "is_blocked": common["is_blocked"],
        "icon": common["icon"],
        "start_lc_position": common["start_lc_position"],
        "start_timestamp": common["start_timestamp"],
        "extent": common["extent"],
        "point": common["point"],
        "coordinate_lat": common["coordinate_lat"],
        "coordinate_lon": common["coordinate_lon"],
        "geometry_json": common["geometry_json"],
        "impact_lower": common["impact_lower"],
        "impact_upper": common["impact_upper"],
        "impact_symbols": common["impact_symbols"],
        "route_recommendation_json": common["route_recommendation_json"],
        "footer_lines": common["footer_lines"],
    }


def _build_warning_event_snapshot(common: dict[str, Any]) -> dict[str, Any]:
    snapshot = _build_road_event_snapshot(common)
    snapshot.update(
        {
            "delay_minutes": common["delay_minutes"],
            "average_speed_kmh": common["average_speed_kmh"],
            "abnormal_traffic_type": common["abnormal_traffic_type"],
            "source_name": common["source_name"],
        }
    )
    return snapshot


def _build_parking_lorry_snapshot(common: dict[str, Any]) -> dict[str, Any]:
    car_spaces, lorry_spaces = _parse_parking_counts(common["description_lines"])
    return {
        "identifier": common["identifier"],
        "road_ids": common["road_ids"],
        "display_type": common["display_type"],
        "title": common["title"],
        "subtitle": common["subtitle"],
        "description_lines": common["description_lines"],
        "future": common["future"],
        "is_blocked": common["is_blocked"],
        "icon": common["icon"],
        "start_lc_position": common["start_lc_position"],
        "extent": common["extent"],
        "point": common["point"],
        "coordinate_lat": common["coordinate_lat"],
        "coordinate_lon": common["coordinate_lon"],
        "route_recommendation_json": common["route_recommendation_json"],
        "footer_lines": common["footer_lines"],
        "amenity_descriptions": common["amenity_descriptions"],
        "car_space_count": car_spaces,
        "lorry_space_count": lorry_spaces,
    }


def _build_charging_station_snapshot(common: dict[str, Any]) -> dict[str, Any]:
    address_line, charging_point_count, charging_points_json = parse_charging_points(common["description_lines"])
    return {
        "identifier": common["identifier"],
        "road_ids": common["road_ids"],
        "display_type": common["display_type"],
        "title": common["title"],
        "subtitle": common["subtitle"],
        "description_lines": common["description_lines"],
        "future": common["future"],
        "is_blocked": common["is_blocked"],
        "icon": common["icon"],
        "extent": common["extent"],
        "point": common["point"],
        "coordinate_lat": common["coordinate_lat"],
        "coordinate_lon": common["coordinate_lon"],
        "address_line": address_line,
        "charging_point_count": charging_point_count,
        "charging_points_json": charging_points_json,
        "route_recommendation_json": common["route_recommendation_json"],
        "footer_lines": common["footer_lines"],
    }


def _build_webcam_snapshot(common: dict[str, Any]) -> dict[str, Any]:
    return {
        "identifier": common["identifier"],
        "road_ids": common["road_ids"],
        "display_type": common["display_type"],
        "title": common["title"],
        "subtitle": common["subtitle"],
        "description_lines": common["description_lines"],
        "future": common["future"],
        "is_blocked": common["is_blocked"],
        "icon": common["icon"],
        "extent": common["extent"],
        "point": common["point"],
        "coordinate_lat": common["coordinate_lat"],
        "coordinate_lon": common["coordinate_lon"],
        "route_recommendation_json": common["route_recommendation_json"],
        "footer_lines": common["footer_lines"],
        "operator_name": common["operator_name"],
        "image_url": common["image_url"],
        "stream_url": common["stream_url"],
    }


SCHEMA_BUILDERS = {
    "RoadEvent": _build_road_event_snapshot,
    "WarningEvent": _build_warning_event_snapshot,
    "ParkingLorry": _build_parking_lorry_snapshot,
    "ChargingStation": _build_charging_station_snapshot,
    "Webcam": _build_webcam_snapshot,
}


def build_family_snapshot(road_id: str, resource_type: str, raw_item: dict[str, Any]) -> Optional[tuple[str, dict[str, Any]]]:
    common = _normalize_common_fields(road_id, resource_type, raw_item)
    if common is None:
        return None
    family = determine_event_family(resource_type, common.get("display_type"))
    if family is None:
        logger.debug(
            "Skipping Autobahn item %s from %s because display_type %s is not mapped",
            common["identifier"],
            resource_type,
            common.get("display_type"),
        )
        return None
    builder = SCHEMA_BUILDERS[EVENT_FAMILIES[family]["schema"]]
    return family, builder(common)


def merge_snapshots(existing: dict[str, Any], new_snapshot: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    merged["road_ids"] = sorted(set(existing.get("road_ids", [])) | set(new_snapshot.get("road_ids", [])))
    for key, value in new_snapshot.items():
        if key == "road_ids":
            continue
        if key not in merged or _is_missing(merged[key]):
            merged[key] = value
            continue
        if _is_missing(value):
            continue
        if merged[key] != value:
            logger.debug("Conflicting values for Autobahn identifier %s field %s", merged.get("identifier"), key)
    return merged


def diff_items(previous: dict[str, dict[str, Any]], current: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    appeared = [current[identifier] for identifier in current.keys() - previous.keys()]
    updated = [current[identifier] for identifier in current.keys() & previous.keys() if current[identifier] != previous[identifier]]
    resolved = [previous[identifier] for identifier in previous.keys() - current.keys()]
    return {
        "appeared": appeared,
        "updated": updated,
        "resolved": resolved,
    }


def _load_generated_data_classes() -> dict[str, type[Any]]:
    expected = {config["schema"] for config in EVENT_FAMILIES.values()}
    module = importlib.import_module("autobahn_producer_data")
    found: dict[str, type[Any]] = {}
    for class_name in expected:
        candidate = getattr(module, class_name, None)
        if isinstance(candidate, type):
            found[class_name] = candidate
    missing = sorted(expected - set(found))
    if missing:
        raise ImportError(f"Generated Autobahn data classes not found: {', '.join(missing)}. Run ./generate_producer.ps1.")
    return found


def _load_generated_producer_class() -> type[Any]:
    module = importlib.import_module("autobahn_producer_kafka_producer.producer")
    for attribute_name in dir(module):
        candidate = getattr(module, attribute_name)
        if isinstance(candidate, type) and attribute_name.endswith("EventProducer"):
            return candidate
    raise ImportError("Generated Autobahn producer client not found. Run ./generate_producer.ps1.")


class AutobahnPoller:
    """Poll the Autobahn API and send changed items to Kafka."""

    headers = {
        "Accept": "application/json",
        "User-Agent": "(real-time-sources, clemensv@microsoft.com)",
    }

    def __init__(
        self,
        kafka_config: Optional[dict[str, str]] = None,
        kafka_topic: Optional[str] = None,
        state_file: Optional[str] = None,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
        resources: Iterable[str] = DEFAULT_RESOURCES,
        roads: Optional[Iterable[str]] = None,
        request_concurrency: int = DEFAULT_REQUEST_CONCURRENCY,
    ):
        self.kafka_topic = kafka_topic or DEFAULT_KAFKA_TOPIC
        self.state_file = Path(state_file or DEFAULT_STATE_FILE)
        self.poll_interval_seconds = poll_interval_seconds
        self.resources = tuple(resources)
        self.roads = normalize_road_ids(roads or []) or None
        self.request_concurrency = max(1, request_concurrency)
        self._semaphore = asyncio.Semaphore(self.request_concurrency)
        self.state = self.load_state()
        self.data_classes: dict[str, type[Any]] = {}
        self.event_producer: Optional[Any] = None

        if kafka_config is not None:
            producer_class = _load_generated_producer_class()
            self.data_classes = _load_generated_data_classes()
            kafka_producer = Producer(kafka_config)
            self.event_producer = producer_class(kafka_producer, self.kafka_topic)

    def load_state(self) -> dict[str, Any]:
        if self.state_file.exists():
            try:
                with self.state_file.open("r", encoding="utf-8") as handle:
                    loaded = json.load(handle)
                    if isinstance(loaded, dict):
                        loaded.setdefault("etags", {})
                        loaded.setdefault("items", {})
                        loaded.setdefault("resource_items", {})
                        return loaded
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                logger.warning("Failed to load state file %s: %s", self.state_file, exc)
        return {"etags": {}, "items": {}, "resource_items": {}}

    def save_state(self) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.state_file.with_suffix(self.state_file.suffix + ".tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(self.state, handle, indent=2, ensure_ascii=False)
        temp_path.replace(self.state_file)

    async def fetch_roads(self, session: aiohttp.ClientSession) -> list[str]:
        async with session.get(f"{BASE_URL}/", headers=self.headers) as response:
            response.raise_for_status()
            payload = await response.json()
        return normalize_road_ids(payload.get("roads", []))

    async def fetch_resource(self, session: aiohttp.ClientSession, road_id: str, resource_type: str) -> FetchResult:
        async with self._semaphore:
            headers = dict(self.headers)
            etag = self.state.get("etags", {}).get(resource_type, {}).get(road_id)
            if etag:
                headers["If-None-Match"] = etag

            url = f"{BASE_URL}/{road_id}/services/{resource_type}"
            try:
                async with session.get(url, headers=headers) as response:
                    response_etag = response.headers.get("ETag")
                    if response.status == 304:
                        return FetchResult(road_id=road_id, resource_type=resource_type, status=304, etag=response_etag or etag, items=[])

                    response.raise_for_status()
                    payload = await response.json()
            except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                return FetchResult(road_id=road_id, resource_type=resource_type, status=0, etag=etag, items=[], error=str(exc))

        response_key = RESOURCE_RESPONSE_KEYS[resource_type]
        items = payload.get(response_key, []) if isinstance(payload, dict) else []
        if not isinstance(items, list):
            items = []
        return FetchResult(road_id=road_id, resource_type=resource_type, status=200, etag=response_etag, items=items)

    def _get_event_time(self, action: str, snapshot: dict[str, Any], poll_time: datetime) -> str:
        if action == "appeared" and snapshot.get("start_timestamp"):
            return str(snapshot["start_timestamp"])
        return poll_time.isoformat()

    def _send_change(self, family: str, action: str, snapshot: dict[str, Any], poll_time: datetime) -> None:
        if not self.event_producer:
            return

        config = EVENT_FAMILIES[family]
        event_time = self._get_event_time(action, snapshot, poll_time)
        data_kwargs = dict(snapshot)
        data_kwargs["event_time"] = event_time
        data_class = self.data_classes[config["schema"]]
        data = data_class(**data_kwargs)
        method_name = f"send_de_autobahn_{config['method_stem']}_{action}"
        method = getattr(self.event_producer, method_name)
        method(
            _identifier=snapshot["identifier"],
            _event_time=event_time,
            data=data,
            flush_producer=False,
        )

    def _summarize_changes(self, changes_by_family: dict[str, dict[str, int]]) -> str:
        parts: list[str] = []
        for family in EVENT_FAMILIES:
            stats = changes_by_family.get(family, {})
            count = sum(stats.values())
            if count == 0:
                continue
            parts.append(
                f"{family}: {stats.get('appeared', 0)} appeared, {stats.get('updated', 0)} updated, {stats.get('resolved', 0)} resolved"
            )
        return "; ".join(parts)

    def _aggregate_current_items(self, roads: list[str]) -> dict[str, dict[str, dict[str, Any]]]:
        current_by_family = {family: {} for family in EVENT_FAMILIES}
        resource_items = self.state.get("resource_items", {})
        active_road_ids = set(roads)
        active_resources = set(self.resources)

        for resource_type in active_resources:
            for road_id, road_items in resource_items.get(resource_type, {}).items():
                if road_id not in active_road_ids:
                    continue
                for identifier, entry in road_items.items():
                    family = entry.get("family")
                    snapshot = entry.get("snapshot")
                    if family not in current_by_family or not isinstance(snapshot, dict):
                        continue
                    existing = current_by_family[family].get(identifier)
                    if existing is None:
                        current_by_family[family][identifier] = snapshot
                    else:
                        current_by_family[family][identifier] = merge_snapshots(existing, snapshot)

        return current_by_family

    async def poll_once(self, session: aiohttp.ClientSession, poll_time: datetime) -> dict[str, dict[str, int]]:
        roads = self.roads if self.roads is not None else await self.fetch_roads(session)
        tasks = [self.fetch_resource(session, road_id, resource_type) for resource_type in self.resources for road_id in roads]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result.error:
                logger.warning("Fetch failed for %s/%s: %s", result.road_id, result.resource_type, result.error)
                continue

            if result.status == 304:
                if result.etag:
                    self.state.setdefault("etags", {}).setdefault(result.resource_type, {})[result.road_id] = result.etag
                continue

            resource_state = self.state.setdefault("resource_items", {}).setdefault(result.resource_type, {})
            road_state: dict[str, dict[str, Any]] = {}
            for raw_item in result.items:
                if not isinstance(raw_item, dict):
                    continue
                built = build_family_snapshot(result.road_id, result.resource_type, raw_item)
                if built is None:
                    continue
                family, snapshot = built
                identifier = snapshot["identifier"]
                existing = road_state.get(identifier)
                entry = {"family": family, "snapshot": snapshot}
                if existing is None:
                    road_state[identifier] = entry
                else:
                    road_state[identifier] = {
                        "family": family,
                        "snapshot": merge_snapshots(existing["snapshot"], snapshot),
                    }

            resource_state[result.road_id] = road_state
            self.state.setdefault("etags", {}).setdefault(result.resource_type, {})[result.road_id] = result.etag

        current_by_family = self._aggregate_current_items(roads)
        changes_by_family: dict[str, dict[str, int]] = {
            family: {"appeared": 0, "updated": 0, "resolved": 0}
            for family in EVENT_FAMILIES
        }

        previous_by_family = self.state.setdefault("items", {})
        for family in EVENT_FAMILIES:
            previous = previous_by_family.get(family, {})
            current = current_by_family.get(family, {})
            for action, snapshots in diff_items(previous, current).items():
                for snapshot in snapshots:
                    self._send_change(family, action, snapshot, poll_time)
                    changes_by_family[family][action] += 1
            previous_by_family[family] = current

        if self.event_producer:
            self.event_producer.producer.flush()

        self.save_state()
        return changes_by_family

    async def poll_and_send(self) -> None:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            while True:
                cycle_started = datetime.now(timezone.utc)
                changes = await self.poll_once(session, cycle_started)
                summary = self._summarize_changes(changes)
                if summary:
                    logger.info("Autobahn cycle complete: %s", summary)
                else:
                    logger.info("Autobahn cycle complete: no changes")

                elapsed = datetime.now(timezone.utc) - cycle_started
                remaining = timedelta(seconds=self.poll_interval_seconds) - elapsed
                if remaining.total_seconds() > 0:
                    await asyncio.sleep(remaining.total_seconds())


async def run_list_roads() -> None:
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        poller = AutobahnPoller()
        for road_id in await poller.fetch_roads(session):
            print(road_id)


def _resolve_argument(value: Optional[str], env_var: str, default: Optional[str] = None) -> Optional[str]:
    if value is not None:
        return value
    env_value = os.getenv(env_var)
    if env_value is not None:
        return env_value
    return default


def _resolve_int_argument(value: Optional[int], env_var: str, default: int) -> int:
    if value is not None:
        return value
    env_value = os.getenv(env_var)
    if env_value:
        try:
            return int(env_value)
        except ValueError as exc:
            raise ValueError(f"Environment variable {env_var} must be an integer") from exc
    return default


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    connection_string = _resolve_argument(args.connection_string, "CONNECTION_STRING")
    if connection_string:
        parsed = parse_connection_string(connection_string)
        kafka_bootstrap_servers = parsed.get("bootstrap.servers")
        kafka_topic = args.kafka_topic or parsed.get("kafka_topic") or os.getenv("KAFKA_TOPIC") or DEFAULT_KAFKA_TOPIC
        sasl_username = parsed.get("sasl.username")
        sasl_password = parsed.get("sasl.password")
    else:
        kafka_bootstrap_servers = _resolve_argument(args.kafka_bootstrap_servers, "KAFKA_BOOTSTRAP_SERVERS")
        kafka_topic = _resolve_argument(args.kafka_topic, "KAFKA_TOPIC", DEFAULT_KAFKA_TOPIC)
        sasl_username = _resolve_argument(args.sasl_username, "SASL_USERNAME")
        sasl_password = _resolve_argument(args.sasl_password, "SASL_PASSWORD")

    if not kafka_bootstrap_servers:
        raise ValueError("Kafka bootstrap servers must be provided either directly or through CONNECTION_STRING.")

    kafka_config = {
        "bootstrap.servers": kafka_bootstrap_servers,
    }

    tls_enabled = _resolve_argument(None, "KAFKA_ENABLE_TLS", "true").lower() not in {"false", "0", "no"}
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    return kafka_config, kafka_topic


def configure_logging(log_level: str) -> None:
    logging.getLogger().setLevel(getattr(logging, log_level.upper(), logging.INFO))


def main() -> None:
    parser = argparse.ArgumentParser(description="German Autobahn Traffic Bridge")
    subparsers = parser.add_subparsers(dest="subcommand")

    roads_parser = subparsers.add_parser("roads", help="List the available Autobahn road IDs")
    roads_parser.add_argument("--log-level", type=str, default=None, help="Logging level")

    feed_parser = subparsers.add_parser("feed", help="Poll the Autobahn API and publish changes to Kafka")
    feed_parser.add_argument("--state-file", type=str, default=None, help="File used to store ETags and last-seen snapshots")
    feed_parser.add_argument("--poll-interval", type=int, default=None, help="Polling interval in seconds")
    feed_parser.add_argument("--resources", type=str, default=None, help="Comma-separated resource list or *")
    feed_parser.add_argument("--roads", type=str, default=None, help="Comma-separated road list or *")
    feed_parser.add_argument("--request-concurrency", type=int, default=None, help="Maximum concurrent Autobahn API requests")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=None, help="Comma-separated Kafka bootstrap servers")
    feed_parser.add_argument("--kafka-topic", type=str, default=None, help="Kafka topic")
    feed_parser.add_argument("--sasl-username", type=str, default=None, help="SASL username")
    feed_parser.add_argument("--sasl-password", type=str, default=None, help="SASL password")
    feed_parser.add_argument("--connection-string", type=str, default=None, help="Event Hubs or Fabric Event Streams connection string")
    feed_parser.add_argument("--log-level", type=str, default=None, help="Logging level")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        return

    log_level = _resolve_argument(getattr(args, "log_level", None), "LOG_LEVEL", "INFO") or "INFO"
    configure_logging(log_level)

    if args.subcommand == "roads":
        asyncio.run(run_list_roads())
        return

    try:
        kafka_config, kafka_topic = build_kafka_config(args)
        resources = parse_resources_argument(_resolve_argument(args.resources, "AUTOBAHN_RESOURCES", SELECTION_SENTINEL) or SELECTION_SENTINEL)
        roads = parse_roads_argument(_resolve_argument(args.roads, "AUTOBAHN_ROADS", SELECTION_SENTINEL) or SELECTION_SENTINEL)
        poll_interval_seconds = _resolve_int_argument(args.poll_interval, "AUTOBAHN_POLL_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS)
        request_concurrency = _resolve_int_argument(args.request_concurrency, "AUTOBAHN_REQUEST_CONCURRENCY", DEFAULT_REQUEST_CONCURRENCY)
        state_file = _resolve_argument(args.state_file, "AUTOBAHN_STATE_FILE", DEFAULT_STATE_FILE)
    except ValueError as exc:
        logger.error("%s", exc)
        sys.exit(1)

    poller = AutobahnPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=state_file,
        poll_interval_seconds=poll_interval_seconds,
        resources=resources,
        roads=roads,
        request_concurrency=request_concurrency,
    )
    asyncio.run(poller.poll_and_send())


if __name__ == "__main__":
    main()
