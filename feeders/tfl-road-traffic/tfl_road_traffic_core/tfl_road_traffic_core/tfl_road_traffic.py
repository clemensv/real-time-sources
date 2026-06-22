"""Transport-neutral acquisition for TfL road traffic feeds."""

from __future__ import annotations

import json
import logging
import os
import time
import unicodedata
from datetime import datetime
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-tfl-road-traffic/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)
TFL_ROAD_URL = "https://api.tfl.gov.uk/Road"
TFL_STATUS_URL = "https://api.tfl.gov.uk/Road/all/Status"
TFL_DISRUPTION_URL = "https://api.tfl.gov.uk/Road/all/Disruption"


def _make_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(total=3, backoff_factor=1.5, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        logger.debug("Could not parse datetime: %s", value)
        return None


def _serialize_geo(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


def _uns_slug(value: Any) -> str:
    raw = unicodedata.normalize("NFKD", str(value or "unknown")).encode("ascii", "ignore").decode("ascii")
    raw = raw.lower().strip()
    out = [ch if ch.isalnum() else "-" for ch in raw]
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


def _normalize_disruption_severity(value: Any, has_closures: Any = None) -> str:
    if has_closures is True:
        return "closure"
    slug = _uns_slug(value)
    aliases = {"minimal": "minor", "low": "minor", "no-disruptions": "information", "unknown": "information", "info": "information"}
    normalized = aliases.get(slug, slug)
    return normalized if normalized in {"serious", "severe", "moderate", "minor", "information", "closure"} else "information"


def _primary_road_id(raw: dict) -> str:
    corridor_ids = raw.get("corridorIds")
    if isinstance(corridor_ids, list) and corridor_ids:
        return _uns_slug(corridor_ids[0])
    return _uns_slug(raw.get("road_id") or raw.get("roadId") or raw.get("id") or "unknown")


def build_road_corridor_record(raw: dict) -> Optional[dict[str, Any]]:
    road_id = raw.get("id")
    display_name = raw.get("displayName")
    if not road_id or not display_name:
        return None
    return {
        "road_id": _uns_slug(road_id),
        "display_name": display_name,
        "status_severity": raw.get("statusSeverity") or None,
        "status_severity_description": raw.get("statusSeverityDescription") or None,
        "bounds": raw.get("bounds") or None,
        "envelope": raw.get("envelope") or None,
        "url": raw.get("url") or None,
        "status_aggregation_start_date": _parse_dt(raw.get("statusAggregationStartDate")),
        "status_aggregation_end_date": _parse_dt(raw.get("statusAggregationEndDate")),
    }


def build_road_status_record(raw: dict) -> Optional[dict[str, Any]]:
    road_id = raw.get("id")
    display_name = raw.get("displayName")
    if not road_id or not display_name:
        return None
    return {
        "road_id": _uns_slug(road_id),
        "display_name": display_name,
        "status_severity": raw.get("statusSeverity") or None,
        "status_severity_description": raw.get("statusSeverityDescription") or None,
        "bounds": raw.get("bounds") or None,
        "envelope": raw.get("envelope") or None,
        "url": raw.get("url") or None,
        "status_aggregation_start_date": _parse_dt(raw.get("statusAggregationStartDate")),
        "status_aggregation_end_date": _parse_dt(raw.get("statusAggregationEndDate")),
    }


def build_street(raw: dict) -> dict:
    return {
        "name": raw.get("name") or None,
        "closure": raw.get("closure") or None,
        "directions": raw.get("directions") or None,
        "source_system_id": raw.get("sourceSystemId") or None,
        "source_system_key": raw.get("sourceSystemKey") or None,
    }


def build_road_disruption_record(raw: dict) -> Optional[dict[str, Any]]:
    disruption_id = raw.get("id")
    if not disruption_id:
        return None
    raw_streets = raw.get("streets")
    streets = [build_street(item) for item in raw_streets] if isinstance(raw_streets, list) else None
    return {
        "road_id": _primary_road_id(raw),
        "disruption_id": _uns_slug(disruption_id),
        "category": raw.get("category") or None,
        "sub_category": raw.get("subCategory") or None,
        "severity": _normalize_disruption_severity(raw.get("severity"), raw.get("hasClosures")),
        "ordinal": raw.get("ordinal"),
        "url": raw.get("url") or None,
        "point": raw.get("point") or None,
        "comments": raw.get("comments") or None,
        "current_update": raw.get("currentUpdate") or None,
        "current_update_datetime": _parse_dt(raw.get("currentUpdateDateTime")),
        "corridor_ids": raw.get("corridorIds") or None,
        "start_datetime": _parse_dt(raw.get("startDateTime")),
        "end_datetime": _parse_dt(raw.get("endDateTime")),
        "last_modified_time": _parse_dt(raw.get("lastModifiedTime")),
        "level_of_interest": raw.get("levelOfInterest") or None,
        "location": raw.get("location") or None,
        "is_provisional": raw.get("isProvisional"),
        "has_closures": raw.get("hasClosures"),
        "streets": streets,
        "geography": _serialize_geo(raw.get("geography")),
        "geometry": _serialize_geo(raw.get("geometry")),
        "status": raw.get("status") or None,
        "is_active": raw.get("isActive"),
    }


class TflRoadTrafficSource:
    def __init__(self, polling_interval: int = 60, reference_refresh_interval: int = 3600, session: Optional[requests.Session] = None):
        self.polling_interval = polling_interval
        self.reference_refresh_interval = reference_refresh_interval
        self.session = session or _make_session()
        self.session.headers["User-Agent"] = USER_AGENT
        self._seen_disruptions: dict[str, str] = {}
        self._last_reference_time = 0.0
        self._cached_corridors: Optional[list[dict]] = None

    def _fetch_json(self, url: str) -> Optional[Any]:
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                return json.loads(response.content.decode("utf-8-sig"))
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning("Failed to fetch %s: %s", url, exc)
            return None

    def fetch_corridors(self) -> Optional[list[dict]]:
        data = self._fetch_json(TFL_ROAD_URL)
        return data if isinstance(data, list) else None

    def fetch_statuses(self) -> Optional[list[dict]]:
        data = self._fetch_json(TFL_STATUS_URL)
        return data if isinstance(data, list) else None

    def fetch_disruptions(self) -> Optional[list[dict]]:
        data = self._fetch_json(TFL_DISRUPTION_URL)
        return data if isinstance(data, list) else None

    def reference_due(self, now: Optional[float] = None) -> bool:
        current = time.monotonic() if now is None else now
        return (current - self._last_reference_time) >= self.reference_refresh_interval

    def remember_reference_fetch(self, corridors: list[dict]) -> None:
        self._cached_corridors = corridors
        self._last_reference_time = time.monotonic()

    def pending_disruptions(self, raw_disruptions: list[dict]) -> tuple[list[dict[str, Any]], dict[str, str]]:
        to_emit: list[dict[str, Any]] = []
        candidate_state: dict[str, str] = {}
        for raw in raw_disruptions:
            disruption_id = raw.get("id")
            if not disruption_id:
                continue
            last_modified = raw.get("lastModifiedTime", "")
            if self._seen_disruptions.get(disruption_id) == last_modified:
                continue
            disruption = build_road_disruption_record(raw)
            if disruption is None:
                continue
            to_emit.append(disruption)
            candidate_state[str(disruption_id)] = last_modified
        return to_emit, candidate_state

    def commit_disruption_state(self, candidate_state: dict[str, str]) -> None:
        self._seen_disruptions.update(candidate_state)


__all__ = [
    "TFL_DISRUPTION_URL",
    "TFL_ROAD_URL",
    "TFL_STATUS_URL",
    "TflRoadTrafficSource",
    "USER_AGENT",
    "_make_session",
    "_normalize_disruption_severity",
    "_parse_dt",
    "_primary_road_id",
    "_serialize_geo",
    "_uns_slug",
    "build_road_corridor_record",
    "build_road_disruption_record",
    "build_road_status_record",
    "build_street",
]
