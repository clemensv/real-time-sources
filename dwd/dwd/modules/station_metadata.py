"""Station metadata module — emits DWD station reference data."""

import hashlib
import logging
from typing import Any, Dict, List

from dwd.modules.base import BaseModule
from dwd.parsers.csv_parser import MISSING_VALUES
from dwd.util.http_client import DWDHttpClient

logger = logging.getLogger(__name__)

# Station list paths (one per 10-min parameter category — they overlap, so we merge)
_STATION_LIST_PATHS = [
    "climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/now/zehn_now_tu_Beschreibung_Stationen.txt",
    "climate_environment/CDC/observations_germany/climate/10_minutes/precipitation/now/zehn_now_rr_Beschreibung_Stationen.txt",
    "climate_environment/CDC/observations_germany/climate/10_minutes/wind/now/zehn_now_ff_Beschreibung_Stationen.txt",
    "climate_environment/CDC/observations_germany/climate/10_minutes/solar/now/zehn_now_st_Beschreibung_Stationen.txt",
]


def _parse_station_list(text: str) -> List[Dict[str, Any]]:
    """Parse a DWD station list file.

    The first 6 fields (station_id, from, to, elevation, lat, lon) are
    space-separated single tokens. The remaining text contains station_name
    and state (Bundesland) separated by 2+ consecutive spaces.
    """
    import re
    lines = text.strip().splitlines()

    # Find the separator line (all dashes and spaces) to skip headers
    data_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and set(stripped) <= {"-", " "}:
            data_start = i + 1
            break
    if data_start == 0:
        data_start = 2

    stations: List[Dict[str, Any]] = []
    for line in lines[data_start:]:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 7:
            continue

        station_id = parts[0].lstrip("0") or "0"
        from_date = parts[1]
        to_date = parts[2]
        try:
            elevation = float(parts[3])
            latitude = float(parts[4])
            longitude = float(parts[5])
        except (ValueError, IndexError):
            continue

        # Reconstruct the text after the 6th numeric field
        # Find where longitude ends in the original line
        idx = 0
        for _ in range(6):
            idx = line.index(parts[_] if _ == 0 else parts[_], idx) + len(parts[_])
        remainder = line[idx:].strip()

        # Split by 2+ consecutive spaces to separate name, state, etc.
        text_parts = re.split(r'\s{2,}', remainder)
        text_parts = [p.strip() for p in text_parts if p.strip()]
        station_name = text_parts[0] if text_parts else ""
        state = text_parts[1] if len(text_parts) > 1 else ""

        stations.append({
            "station_id": station_id,
            "station_name": station_name,
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation,
            "state": state,
            "from_date": from_date,
            "to_date": to_date if to_date not in MISSING_VALUES else "",
        })

    return stations


class StationMetadataModule(BaseModule):
    """Fetches station lists from DWD and emits StationMetadata events."""

    def __init__(self, http_client: DWDHttpClient):
        self._http = http_client

    @property
    def name(self) -> str:
        return "station_metadata"

    @property
    def default_enabled(self) -> bool:
        return True

    @property
    def default_poll_interval(self) -> int:
        return 86400  # daily

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch station lists, merge, compare checksum, emit if changed."""
        all_stations: Dict[str, Dict[str, Any]] = {}
        for path in _STATION_LIST_PATHS:
            text = self._http.download_text(path)
            if text:
                for s in _parse_station_list(text):
                    all_stations[s["station_id"]] = s

        if not all_stations:
            logger.warning("No station data fetched from DWD")
            return []

        # Checksum to detect changes
        import json
        content_hash = hashlib.md5(
            json.dumps(sorted(all_stations.keys())).encode()
        ).hexdigest()

        prev_hash = state.get("checksum")
        if prev_hash == content_hash:
            logger.debug("Station list unchanged (%d stations)", len(all_stations))
            return []

        state["checksum"] = content_hash
        logger.info("Station list changed — emitting %d station metadata events", len(all_stations))

        events: List[Dict[str, Any]] = []
        for s in all_stations.values():
            events.append({"type": "station_metadata", "data": s})
        return events
