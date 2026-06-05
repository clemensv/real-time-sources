from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import ConfiguredFeed

logger = logging.getLogger(__name__)
DEFAULT_POLL_INTERVAL_SECONDS = 60
REFERENCE_REFRESH_INTERVAL_SECONDS = 3600
USER_AGENT = "real-time-sources-gbfs-bikeshare/0.1.0 (+https://github.com/clemensv/real-time-sources)"


@dataclass(frozen=True)
class SystemInformationRecord:
    system_id: str
    name: str
    operator: Optional[str]
    url: Optional[str]
    timezone: str
    language: Optional[str]
    phone_number: Optional[str]


@dataclass(frozen=True)
class StationInformationRecord:
    system_id: str
    station_id: str
    name: str
    short_name: Optional[str]
    lat: float
    lon: float
    capacity: Optional[int]
    region_id: Optional[str]
    address: Optional[str]
    post_code: Optional[str]


@dataclass(frozen=True)
class StationStatusRecord:
    system_id: str
    station_id: str
    num_bikes_available: int
    num_docks_available: Optional[int]
    num_ebikes_available: Optional[int]
    is_installed: bool
    is_renting: bool
    is_returning: bool
    last_reported: int


@dataclass(frozen=True)
class FreeBikeStatusRecord:
    system_id: str
    bike_id: str
    lat: Optional[float]
    lon: Optional[float]
    is_reserved: bool
    is_disabled: bool
    vehicle_type_id: Optional[str]
    current_range_meters: Optional[float]
    last_reported: Optional[int]


@dataclass(frozen=True)
class GbfsSource:
    autodiscovery_url: str
    system_id: str
    feeds: Dict[str, str]
    language: Optional[str]


def _make_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"true", "1", "yes", "on"}


def _coerce_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _coerce_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _derive_system_id(url: str) -> str:
    parsed = urlparse(url)
    parts = [segment for segment in parsed.path.split("/") if segment]
    if parts:
        for candidate in reversed(parts):
            if candidate.lower().endswith(".json"):
                continue
            return candidate
    return parsed.netloc.replace(".", "-")


def _extract_feed_map(payload: Dict[str, Any]) -> Tuple[Dict[str, str], Optional[str]]:
    data = payload.get("data") or {}
    if isinstance(data, dict) and "feeds" in data:
        feeds = {item["name"]: item["url"] for item in data.get("feeds", []) if item.get("name") and item.get("url")}
        return feeds, None
    preferred_language = "en" if "en" in data else (next(iter(data.keys())) if isinstance(data, dict) and data else None)
    if preferred_language and isinstance(data.get(preferred_language), dict):
        feeds = {item["name"]: item["url"] for item in data[preferred_language].get("feeds", []) if item.get("name") and item.get("url")}
        return feeds, preferred_language
    merged: Dict[str, str] = {}
    if isinstance(data, dict):
        for entry in data.values():
            if isinstance(entry, dict):
                for item in entry.get("feeds", []):
                    if item.get("name") and item.get("url"):
                        merged[item["name"]] = item["url"]
    return merged, preferred_language


def _parse_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = payload.get("data")
    return data if isinstance(data, dict) else payload


def _event_key(prefix: str, system_id: str, entity_id: str) -> str:
    return f"{prefix}:{system_id}/{entity_id}"


def _payload_fingerprint(record: Any) -> str:
    return hashlib.sha256(json.dumps(asdict(record), sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


class GbfsSourceClient:
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or _make_session()

    def _get_json(self, url: str) -> Dict[str, Any]:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def discover_source(self, configured_feed: ConfiguredFeed) -> Optional[GbfsSource]:
        try:
            manifest = self._get_json(configured_feed.autodiscovery_url)
            feeds, language = _extract_feed_map(manifest)
            system_id = configured_feed.system_id_override or _derive_system_id(configured_feed.autodiscovery_url)
            system_feed = feeds.get("system_information")
            if system_feed:
                try:
                    system_info = _parse_data(self._get_json(system_feed))
                    system_id = configured_feed.system_id_override or system_info.get("system_id") or system_id
                except Exception as exc:  # pragma: no cover - best effort fallback
                    logger.warning("Unable to prefetch system_information from %s: %s", system_feed, exc)
            return GbfsSource(
                autodiscovery_url=configured_feed.autodiscovery_url,
                system_id=system_id,
                feeds=feeds,
                language=language,
            )
        except Exception as exc:
            logger.warning("Skipping GBFS feed %s because discovery failed: %s", configured_feed.autodiscovery_url, exc)
            return None

    def fetch_system_information(self, source: GbfsSource) -> Optional[Tuple[SystemInformationRecord, str]]:
        feed_url = source.feeds.get("system_information")
        if not feed_url:
            return None
        payload = _parse_data(self._get_json(feed_url))
        record = SystemInformationRecord(
            system_id=source.system_id,
            name=str(payload.get("name") or source.system_id),
            operator=payload.get("operator"),
            url=payload.get("url"),
            timezone=str(payload.get("timezone") or "UTC"),
            language=payload.get("language") or source.language,
            phone_number=payload.get("phone_number"),
        )
        return record, feed_url

    def fetch_station_information(self, source: GbfsSource) -> Tuple[List[StationInformationRecord], Optional[str]]:
        feed_url = source.feeds.get("station_information")
        if not feed_url:
            return [], None
        payload = self._get_json(feed_url)
        stations = payload.get("data", {}).get("stations", [])
        records: List[StationInformationRecord] = []
        for station in stations:
            station_id = station.get("station_id")
            lat = _coerce_float(station.get("lat"))
            lon = _coerce_float(station.get("lon"))
            if not station_id or lat is None or lon is None:
                continue
            records.append(
                StationInformationRecord(
                    system_id=source.system_id,
                    station_id=str(station_id),
                    name=str(station.get("name") or station_id),
                    short_name=station.get("short_name"),
                    lat=lat,
                    lon=lon,
                    capacity=_coerce_int(station.get("capacity")),
                    region_id=station.get("region_id"),
                    address=station.get("address"),
                    post_code=station.get("post_code"),
                )
            )
        return records, feed_url

    def fetch_station_status(self, source: GbfsSource) -> Tuple[List[StationStatusRecord], Optional[str], int]:
        feed_url = source.feeds.get("station_status")
        if not feed_url:
            return [], None, DEFAULT_POLL_INTERVAL_SECONDS
        payload = self._get_json(feed_url)
        ttl = _coerce_int(payload.get("ttl")) or DEFAULT_POLL_INTERVAL_SECONDS
        stations = payload.get("data", {}).get("stations", [])
        records: List[StationStatusRecord] = []
        for station in stations:
            station_id = station.get("station_id")
            last_reported = _coerce_int(station.get("last_reported"))
            bikes_available = _coerce_int(station.get("num_bikes_available"))
            if not station_id or last_reported is None or bikes_available is None:
                continue
            records.append(
                StationStatusRecord(
                    system_id=source.system_id,
                    station_id=str(station_id),
                    num_bikes_available=bikes_available,
                    num_docks_available=_coerce_int(station.get("num_docks_available")),
                    num_ebikes_available=_coerce_int(station.get("num_ebikes_available")),
                    is_installed=_coerce_bool(station.get("is_installed")),
                    is_renting=_coerce_bool(station.get("is_renting")),
                    is_returning=_coerce_bool(station.get("is_returning")),
                    last_reported=last_reported,
                )
            )
        return records, feed_url, ttl

    def fetch_free_bike_status(self, source: GbfsSource) -> Tuple[List[FreeBikeStatusRecord], Optional[str], int]:
        feed_url = source.feeds.get("free_bike_status") or source.feeds.get("vehicle_status")
        if not feed_url:
            return [], None, DEFAULT_POLL_INTERVAL_SECONDS
        payload = self._get_json(feed_url)
        ttl = _coerce_int(payload.get("ttl")) or DEFAULT_POLL_INTERVAL_SECONDS
        bikes = payload.get("data", {}).get("bikes") or payload.get("data", {}).get("vehicles") or []
        records: List[FreeBikeStatusRecord] = []
        for bike in bikes:
            bike_id = bike.get("bike_id") or bike.get("vehicle_id")
            if not bike_id:
                continue
            records.append(
                FreeBikeStatusRecord(
                    system_id=source.system_id,
                    bike_id=str(bike_id),
                    lat=_coerce_float(bike.get("lat")),
                    lon=_coerce_float(bike.get("lon")),
                    is_reserved=_coerce_bool(bike.get("is_reserved")),
                    is_disabled=_coerce_bool(bike.get("is_disabled")),
                    vehicle_type_id=bike.get("vehicle_type_id"),
                    current_range_meters=_coerce_float(bike.get("current_range_meters")),
                    last_reported=_coerce_int(bike.get("last_reported")),
                )
            )
        return records, feed_url, ttl


def discover_sources(client: GbfsSourceClient, feeds: Iterable[ConfiguredFeed]) -> List[GbfsSource]:
    sources: List[GbfsSource] = []
    for feed in feeds:
        source = client.discover_source(feed)
        if source is not None:
            sources.append(source)
    return sources


def should_publish_station_status(record: StationStatusRecord, state: Dict[str, Any]) -> bool:
    key = _event_key("station_status", record.system_id, record.station_id)
    previous = state.setdefault("station_status", {}).get(key)
    current = {"last_reported": record.last_reported, "fingerprint": _payload_fingerprint(record)}
    if previous == current:
        return False
    state["station_status"][key] = current
    return True


def should_publish_free_bike_status(record: FreeBikeStatusRecord, state: Dict[str, Any]) -> bool:
    key = _event_key("free_bike_status", record.system_id, record.bike_id)
    previous = state.setdefault("free_bike_status", {}).get(key)
    current = {"last_reported": record.last_reported, "fingerprint": _payload_fingerprint(record)}
    if previous == current:
        return False
    state["free_bike_status"][key] = current
    return True
