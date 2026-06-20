from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import parse_csv

logger = logging.getLogger(__name__)
API_ROOT = "https://api.openaq.org/v3"
USER_AGENT = "real-time-sources-openaq/0.1.0 (+https://github.com/clemensv/real-time-sources)"
DEFAULT_LIMIT = 100
PARAMETER_ENUM = {
    "pm25", "pm10", "o3", "no2", "so2", "co", "bc", "no", "nox", "pm1", "co2",
    "temperature", "relativehumidity", "pressure", "windspeed", "winddirection",
    "um003", "um005", "um010", "um025", "um050", "um100",
}


@dataclass(frozen=True)
class LocationRecord:
    location_id: int
    name: Optional[str]
    locality: Optional[str]
    timezone: str
    country_iso: str
    country_name: str
    owner_id: Optional[int]
    owner_name: Optional[str]
    provider_id: Optional[int]
    provider_name: Optional[str]
    is_mobile: bool
    is_monitor: bool
    latitude: Optional[float]
    longitude: Optional[float]
    datetime_first: Optional[datetime]
    datetime_last: Optional[datetime]
    license: Optional[str]
    sensor_count: int


@dataclass(frozen=True)
class SensorRecord:
    location_id: int
    sensor_id: int
    country_iso: str
    sensor_name: str
    parameter_id: int
    parameter_name: str
    parameter_units: str
    parameter_display_name: Optional[str]
    datetime_first: Optional[datetime]
    datetime_last: Optional[datetime]
    latest_value: Optional[float]
    latest_datetime: Optional[datetime]
    latitude: Optional[float]
    longitude: Optional[float]


@dataclass(frozen=True)
class MeasurementRecord:
    location_id: int
    sensor_id: int
    country_iso: str
    parameter_id: int
    parameter_name: str
    parameter_units: str
    datetime: datetime
    value: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]
    is_valid: Optional[bool]
    has_flags: Optional[bool]
    poll_time: datetime


def _make_session(api_key: Optional[str]) -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    if api_key:
        session.headers["X-API-Key"] = api_key
    retry = Retry(total=3, backoff_factor=1.5, status_forcelist=[408, 429, 500, 502, 503, 504], allowed_methods=["GET"], raise_on_status=False)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _dt(obj: Any) -> Optional[datetime]:
    if not obj:
        return None
    if isinstance(obj, str):
        text = obj.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(text)
        except ValueError:
            return None
    if isinstance(obj, dict):
        return _dt(obj.get("utc") or obj.get("local"))
    return None


def _num(obj: Any) -> Optional[float]:
    if obj is None or obj == "":
        return None
    try:
        return float(obj)
    except (TypeError, ValueError):
        return None


def _int(obj: Any) -> Optional[int]:
    if obj is None or obj == "":
        return None
    try:
        return int(obj)
    except (TypeError, ValueError):
        return None


def _entity_id_name(obj: Any) -> tuple[Optional[int], Optional[str]]:
    if not isinstance(obj, dict):
        return None, None
    return _int(obj.get("id")), obj.get("name")


def _coords(obj: Any) -> tuple[Optional[float], Optional[float]]:
    if not isinstance(obj, dict):
        return None, None
    return _num(obj.get("latitude")), _num(obj.get("longitude"))


def _license_text(items: Any) -> Optional[str]:
    if not isinstance(items, list):
        return None
    parts: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        attribution = item.get("attribution")
        if isinstance(attribution, dict):
            attr = attribution.get("name") or attribution.get("url")
        else:
            attr = None
        parts.append(" — ".join(str(x) for x in (name, attr) if x))
    return "; ".join(parts) or None


def slug_segment(value: str | int | None) -> str:
    text = str(value or "unknown").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "unknown"


def _measurement_fingerprint(record: MeasurementRecord) -> str:
    return hashlib.sha256(json.dumps(asdict(record), sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")).hexdigest()


def should_publish_measurement(record: MeasurementRecord, state: Dict[str, Any]) -> bool:
    key = f"measurement:{record.location_id}/{record.sensor_id}"
    digest = _measurement_fingerprint(record)
    if state.get(key) == digest:
        return False
    state[key] = digest
    return True


class OpenAQClient:
    def __init__(self, api_key: Optional[str] = None, session: Optional[requests.Session] = None, api_root: str = API_ROOT):
        self.session = session or _make_session(api_key)
        self.api_root = api_root.rstrip("/")

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.session.get(f"{self.api_root}{path}", params={k: v for k, v in (params or {}).items() if v not in (None, "", [])}, timeout=45)
        response.raise_for_status()
        return response.json()

    def iter_locations(self, countries: list[str], location_ids: list[int], bbox: Optional[str], limit: int = DEFAULT_LIMIT, max_pages: int = 1) -> Iterable[LocationRecord]:
        if location_ids:
            for location_id in location_ids:
                payload = self._get(f"/locations/{location_id}")
                for item in payload.get("results", []):
                    yield self._location_record(item)
            return
        filters: list[dict[str, Any]] = []
        if countries:
            filters.extend({"iso": iso.upper()} for iso in countries)
        else:
            filters.append({})
        for params in filters:
            if bbox:
                params = dict(params, bbox=bbox)
            for page in range(1, max_pages + 1):
                payload = self._get("/locations", {**params, "limit": limit, "page": page})
                results = payload.get("results", [])
                for item in results:
                    yield self._location_record(item)
                if len(results) < limit:
                    break

    def sensors_for_location(self, location: LocationRecord) -> list[SensorRecord]:
        payload = self._get(f"/locations/{location.location_id}/sensors")
        return [self._sensor_record(item, location) for item in payload.get("results", []) if self._sensor_record(item, location) is not None]

    def latest_for_location(self, location: LocationRecord, sensors: Dict[int, SensorRecord]) -> list[MeasurementRecord]:
        payload = self._get(f"/locations/{location.location_id}/latest")
        poll_time = datetime.now(timezone.utc)
        records: list[MeasurementRecord] = []
        for item in payload.get("results", []):
            sensor_id = _int(item.get("sensorsId"))
            sensor = sensors.get(sensor_id or -1)
            if not sensor:
                continue
            timestamp = _dt(item.get("datetime"))
            if timestamp is None:
                continue
            lat, lon = _coords(item.get("coordinates"))
            flags = item.get("flagInfo") if isinstance(item.get("flagInfo"), dict) else {}
            has_flags = flags.get("hasFlags") if isinstance(flags.get("hasFlags"), bool) else None
            records.append(MeasurementRecord(location.location_id, sensor.sensor_id, location.country_iso, sensor.parameter_id, sensor.parameter_name, sensor.parameter_units, timestamp, _num(item.get("value")), lat, lon, (not has_flags) if has_flags is not None else None, has_flags, poll_time))
        return records

    def _location_record(self, item: Dict[str, Any]) -> LocationRecord:
        country = item.get("country") if isinstance(item.get("country"), dict) else {}
        owner_id, owner_name = _entity_id_name(item.get("owner"))
        provider_id, provider_name = _entity_id_name(item.get("provider"))
        lat, lon = _coords(item.get("coordinates"))
        return LocationRecord(
            location_id=int(item["id"]), name=item.get("name"), locality=item.get("locality"), timezone=str(item.get("timezone") or "UTC"),
            country_iso=str(country.get("iso") or country.get("code") or "XX").upper(), country_name=str(country.get("name") or country.get("iso") or "Unknown"),
            owner_id=owner_id, owner_name=owner_name, provider_id=provider_id, provider_name=provider_name,
            is_mobile=bool(item.get("isMobile", False)), is_monitor=bool(item.get("isMonitor", False)), latitude=lat, longitude=lon,
            datetime_first=_dt(item.get("datetimeFirst")), datetime_last=_dt(item.get("datetimeLast")), license=_license_text(item.get("licenses")),
            sensor_count=len(item.get("sensors") or []),
        )

    def _sensor_record(self, item: Dict[str, Any], location: LocationRecord) -> Optional[SensorRecord]:
        parameter = item.get("parameter") if isinstance(item.get("parameter"), dict) else {}
        name = str(parameter.get("name") or "").lower()
        if name not in PARAMETER_ENUM:
            logger.debug("Skipping unsupported OpenAQ parameter for enum-safe producer output: %s", name)
            return None
        latest = item.get("latest") if isinstance(item.get("latest"), dict) else {}
        lat, lon = _coords(latest.get("coordinates"))
        pid = _int(parameter.get("id"))
        sid = _int(item.get("id"))
        if pid is None or sid is None:
            return None
        return SensorRecord(location.location_id, sid, location.country_iso, str(item.get("name") or sid), pid, name, str(parameter.get("units") or "unknown"), parameter.get("displayName"), _dt(item.get("datetimeFirst")), _dt(item.get("datetimeLast")), _num(latest.get("value")), _dt(latest.get("datetime")), lat, lon)


class MockOpenAQClient(OpenAQClient):
    def __init__(self):
        pass

    def iter_locations(self, countries: list[str], location_ids: list[int], bbox: Optional[str], limit: int = DEFAULT_LIMIT, max_pages: int = 1) -> Iterable[LocationRecord]:
        yield LocationRecord(1001, "OpenAQ Mock Brussels Arts-Loi", "Brussels", "Europe/Brussels", "BE", "Belgium", 10, "OpenAQ Mock Owner", 20, "OpenAQ Mock Provider", False, True, 50.8466, 4.3528, datetime(2024, 1, 1, tzinfo=timezone.utc), datetime(2026, 6, 20, 15, 0, tzinfo=timezone.utc), "OpenAQ Platform — source attribution required", 1)

    def sensors_for_location(self, location: LocationRecord) -> list[SensorRecord]:
        return [SensorRecord(location.location_id, 2001, location.country_iso, "pm25 sensor", 2, "pm25", "µg/m³", "PM2.5", datetime(2024, 1, 1, tzinfo=timezone.utc), datetime(2026, 6, 20, 15, 0, tzinfo=timezone.utc), 11.2, datetime(2026, 6, 20, 15, 0, tzinfo=timezone.utc), location.latitude, location.longitude)]

    def latest_for_location(self, location: LocationRecord, sensors: Dict[int, SensorRecord]) -> list[MeasurementRecord]:
        sensor = next(iter(sensors.values()))
        return [MeasurementRecord(location.location_id, sensor.sensor_id, location.country_iso, sensor.parameter_id, sensor.parameter_name, sensor.parameter_units, datetime(2026, 6, 20, 15, 0, tzinfo=timezone.utc), 11.2, location.latitude, location.longitude, True, False, datetime(2026, 6, 20, 15, 1, tzinfo=timezone.utc))]


def build_mock_client() -> MockOpenAQClient:
    return MockOpenAQClient()
