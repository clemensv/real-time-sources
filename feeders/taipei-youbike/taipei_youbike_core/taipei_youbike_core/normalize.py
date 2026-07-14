"""Normalization of raw YouBike 2.0 station objects into typed records.

The upstream ``station-yb2.json`` feed carries both slow-moving reference data
(identity, bilingual name, district, address, location, nominal capacity, region
codes) and fast-moving telemetry (bike/dock availability, service status, update
timestamps) on the *same* station object. This module cracks that representation
once into a single :class:`ParsedStation` with native Python types, and exposes
stable dedup signatures so every transport variant can decide independently when
to (re-)emit reference and status CloudEvents.

Two upstream-shape decisions are normalized here:

* The wire uses ``lng`` for longitude and ``station_no`` for the station id;
  these are renamed to ``lon`` / ``station_id`` (the upstream keys are recorded
  as ``altnames`` in the xreg schema).
* Timestamps (``updated_at`` / ``time``) are naive ``YYYY-MM-DD HH:MM:SS`` local
  strings in Asia/Taipei (UTC+8); they are parsed and converted to timezone-aware
  UTC ``datetime`` values.
* The nested ``available_spaces_detail`` object is flattened into three sibling
  per-generation counts (``yb1`` / ``yb2`` / ``eyb``).
* Empty strings (the upstream fills unavailable text fields, e.g. the Simplified
  Chinese ``*_cn`` fields, with ``""``) are normalized to ``None``.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any, Dict, Optional

# The upstream ``updated_at`` / ``time`` strings are naive local time in the
# Asia/Taipei zone, which observes no daylight saving and is a fixed UTC+8.
TAIPEI_TZ = datetime.timezone(datetime.timedelta(hours=8))


def _to_float(value: Any) -> Optional[float]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> Optional[int]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _clean_str(value: Any) -> Optional[str]:
    """Return a trimmed string, or ``None`` for empty/whitespace/missing values."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_taipei(value: Any) -> Optional[datetime.datetime]:
    """Parse a naive ``YYYY-MM-DD HH:MM:SS`` Asia/Taipei string to UTC.

    Empty strings and unparseable values yield ``None``. The result is a
    timezone-aware ``datetime`` in UTC so downstream schemas serialize a stable
    ISO-8601 instant regardless of the consumer's locale.
    """
    text = _clean_str(value)
    if text is None:
        return None
    try:
        parsed = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    return parsed.replace(tzinfo=TAIPEI_TZ).astimezone(datetime.timezone.utc)


@dataclass
class ParsedStation:
    """One YouBike 2.0 station cracked into native-typed reference + status fields."""

    # identity / reference
    station_id: str
    name_tw: str
    name_en: Optional[str]
    name_cn: Optional[str]
    district_tw: Optional[str]
    district_en: Optional[str]
    district_cn: Optional[str]
    address_tw: Optional[str]
    address_en: Optional[str]
    address_cn: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    capacity: Optional[int]
    station_type: Optional[int]
    country_code: Optional[str]
    area_code: Optional[str]
    img: Optional[str]
    # availability / status
    num_bikes_available: Optional[int]
    num_bikes_yb1: Optional[int]
    num_bikes_yb2: Optional[int]
    num_ebikes_available: Optional[int]
    num_empty_docks: Optional[int]
    num_forbidden_docks: Optional[int]
    availability_level: Optional[int]
    service_status: Optional[int]
    updated_at: datetime.datetime
    snapshot_time: Optional[datetime.datetime]

    def info_signature(self) -> Dict[str, Any]:
        """JSON-safe fingerprint of the reference fields (change detection)."""
        return {
            "name_tw": self.name_tw,
            "name_en": self.name_en,
            "name_cn": self.name_cn,
            "district_tw": self.district_tw,
            "district_en": self.district_en,
            "district_cn": self.district_cn,
            "address_tw": self.address_tw,
            "address_en": self.address_en,
            "address_cn": self.address_cn,
            "lat": self.lat,
            "lon": self.lon,
            "capacity": self.capacity,
            "station_type": self.station_type,
            "country_code": self.country_code,
            "area_code": self.area_code,
            "img": self.img,
        }

    def status_signature(self) -> Dict[str, Any]:
        """JSON-safe fingerprint of the availability fields.

        Deliberately excludes ``updated_at`` / ``snapshot_time`` (which advance
        on every upstream refresh even when the counts are unchanged) so status
        events are only (re-)emitted when the availability actually changes.
        """
        return {
            "num_bikes_available": self.num_bikes_available,
            "num_bikes_yb1": self.num_bikes_yb1,
            "num_bikes_yb2": self.num_bikes_yb2,
            "num_ebikes_available": self.num_ebikes_available,
            "num_empty_docks": self.num_empty_docks,
            "num_forbidden_docks": self.num_forbidden_docks,
            "availability_level": self.availability_level,
            "service_status": self.service_status,
        }


def parse_station(raw: Dict[str, Any]) -> ParsedStation:
    """Crack one raw YouBike 2.0 station object into a :class:`ParsedStation`."""
    detail: Dict[str, Any] = raw.get("available_spaces_detail") or {}
    updated_at = _parse_taipei(raw.get("updated_at")) or datetime.datetime.now(
        datetime.timezone.utc
    )

    return ParsedStation(
        station_id=str(raw.get("station_no")),
        name_tw=str(raw.get("name_tw") or ""),
        name_en=_clean_str(raw.get("name_en")),
        name_cn=_clean_str(raw.get("name_cn")),
        district_tw=_clean_str(raw.get("district_tw")),
        district_en=_clean_str(raw.get("district_en")),
        district_cn=_clean_str(raw.get("district_cn")),
        address_tw=_clean_str(raw.get("address_tw")),
        address_en=_clean_str(raw.get("address_en")),
        address_cn=_clean_str(raw.get("address_cn")),
        lat=_to_float(raw.get("lat")),
        lon=_to_float(raw.get("lng")),
        capacity=_to_int(raw.get("parking_spaces")),
        station_type=_to_int(raw.get("type")),
        country_code=_clean_str(raw.get("country_code")),
        area_code=_clean_str(raw.get("area_code")),
        img=_clean_str(raw.get("img")),
        num_bikes_available=_to_int(raw.get("available_spaces")),
        num_bikes_yb1=_to_int(detail.get("yb1")),
        num_bikes_yb2=_to_int(detail.get("yb2")),
        num_ebikes_available=_to_int(detail.get("eyb")),
        num_empty_docks=_to_int(raw.get("empty_spaces")),
        num_forbidden_docks=_to_int(raw.get("forbidden_spaces")),
        availability_level=_to_int(raw.get("available_spaces_level")),
        service_status=_to_int(raw.get("status")),
        updated_at=updated_at,
        snapshot_time=_parse_taipei(raw.get("time")),
    )
