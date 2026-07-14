"""Normalization of raw TfL BikePoint ``Place`` objects into typed records.

The upstream ``GET /BikePoint`` endpoint carries both slow-moving reference
data (identity, location, capacity, lifecycle flags) and fast-moving telemetry
(bike/dock availability) on the *same* ``Place`` object, all encoded as
string-typed ``additionalProperties`` key/value entries. This module cracks
that representation once into a single :class:`ParsedStation` with native Python
types, and exposes stable dedup signatures so every transport variant can decide
independently when to (re-)emit reference and status CloudEvents.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


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


def _to_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in ("true", "1", "yes"):
        return True
    if text in ("false", "0", "no"):
        return False
    return None


def _epoch_ms_to_dt(value: Any) -> Optional[datetime.datetime]:
    """Convert a TfL epoch-milliseconds string (InstallDate/RemovalDate) to UTC.

    Empty strings and unparseable values yield ``None``; the upstream reports an
    empty ``RemovalDate`` for stations that have not been decommissioned.
    """
    ms = _to_int(value)
    if ms is None:
        return None
    try:
        return datetime.datetime.fromtimestamp(ms / 1000.0, tz=datetime.timezone.utc)
    except (OverflowError, OSError, ValueError):
        return None


def _parse_modified(value: Any) -> Optional[datetime.datetime]:
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed


@dataclass
class ParsedStation:
    """One TfL BikePoint cracked into native-typed reference + status fields."""

    # identity / reference
    station_id: str
    name: str
    lat: Optional[float]
    lon: Optional[float]
    terminal_name: Optional[str]
    capacity: Optional[int]
    temporary: Optional[bool]
    install_date: Optional[datetime.datetime]
    removal_date: Optional[datetime.datetime]
    # availability / status
    num_bikes_available: Optional[int]
    num_standard_bikes_available: Optional[int]
    num_ebikes_available: Optional[int]
    num_empty_docks: Optional[int]
    num_docks: Optional[int]
    is_installed: Optional[bool]
    is_locked: Optional[bool]
    modified: datetime.datetime

    def info_signature(self) -> Dict[str, Any]:
        """JSON-safe fingerprint of the reference fields (change detection)."""
        return {
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "terminal_name": self.terminal_name,
            "capacity": self.capacity,
            "temporary": self.temporary,
            "install_date": self.install_date.isoformat() if self.install_date else None,
            "removal_date": self.removal_date.isoformat() if self.removal_date else None,
        }

    def status_signature(self) -> Dict[str, Any]:
        """JSON-safe fingerprint of the availability fields.

        Deliberately excludes ``modified`` (which advances on every upstream
        refresh even when the counts are unchanged) so status events are only
        (re-)emitted when the availability actually changes.
        """
        return {
            "num_bikes_available": self.num_bikes_available,
            "num_standard_bikes_available": self.num_standard_bikes_available,
            "num_ebikes_available": self.num_ebikes_available,
            "num_empty_docks": self.num_empty_docks,
            "num_docks": self.num_docks,
            "is_installed": self.is_installed,
            "is_locked": self.is_locked,
        }


def parse_bikepoint(raw: Dict[str, Any]) -> ParsedStation:
    """Crack one raw TfL BikePoint ``Place`` object into a :class:`ParsedStation`."""
    props_list: List[Dict[str, Any]] = raw.get("additionalProperties") or []
    props: Dict[str, Any] = {}
    modifieds: List[datetime.datetime] = []
    for entry in props_list:
        key = entry.get("key")
        if key is not None:
            props[key] = entry.get("value")
        modified = _parse_modified(entry.get("modified"))
        if modified is not None:
            modifieds.append(modified)

    newest_modified = max(modifieds) if modifieds else datetime.datetime.now(datetime.timezone.utc)

    terminal_name = props.get("TerminalName")
    if isinstance(terminal_name, str) and not terminal_name.strip():
        terminal_name = None

    return ParsedStation(
        station_id=str(raw.get("id")),
        name=str(raw.get("commonName")) if raw.get("commonName") is not None else "",
        lat=_to_float(raw.get("lat")),
        lon=_to_float(raw.get("lon")),
        terminal_name=terminal_name,
        capacity=_to_int(props.get("NbDocks")),
        temporary=_to_bool(props.get("Temporary")),
        install_date=_epoch_ms_to_dt(props.get("InstallDate")),
        removal_date=_epoch_ms_to_dt(props.get("RemovalDate")),
        num_bikes_available=_to_int(props.get("NbBikes")),
        num_standard_bikes_available=_to_int(props.get("NbStandardBikes")),
        num_ebikes_available=_to_int(props.get("NbEBikes")),
        num_empty_docks=_to_int(props.get("NbEmptyDocks")),
        num_docks=_to_int(props.get("NbDocks")),
        is_installed=_to_bool(props.get("Installed")),
        is_locked=_to_bool(props.get("Locked")),
        modified=newest_modified,
    )
