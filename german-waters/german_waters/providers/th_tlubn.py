"""Thüringen TLUBN provider — real-time water levels from hnz.thueringen.de.

Data source: https://hnz.thueringen.de/hw-portal/
The HNZ portal publishes a large HTML page with embedded Leaflet circleMarker
objects containing all ~136 Thüringen gauges with coordinates, water level,
discharge, and timestamps in tooltips.  Station names and water bodies are
fetched from per-station pages at /hw-portal/pegel/{id}_wq.html.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

PORTAL_URL = "https://hnz.thueringen.de/hw-portal/"
PEGEL_URL_TEMPLATE = "https://hnz.thueringen.de/hw-portal/pegel/{station_id}_wq.html"

# Month name mapping for German date parsing
_DE_MONTHS = {
    "Januar": 1, "Februar": 2, "März": 3, "April": 4, "Mai": 5, "Juni": 6,
    "Juli": 7, "August": 8, "September": 9, "Oktober": 10, "November": 11, "Dezember": 12,
    # UTF-8 mangled variants
    "MÃ¤rz": 3, "Marz": 3,
}

_COORD_RE = re.compile(r"L\.circleMarker\(\[([0-9.]+),\s*([0-9.]+)\]")
_STATION_ID_RE = re.compile(r"w_(\d+)")
_W_RE = re.compile(r"W:\s*(\d+)\s*cm")
_Q_RE = re.compile(r"Q:\s*([0-9,]+)\s*m")
_TS_RE = re.compile(r"am\s+(\d+)\.\s*(\w+)\s+(\d{4})\s+(\d{2}):(\d{2})")
_EXTERN_RE = re.compile(r"extern\s*:\s*true")


def _parse_de_month(month_str: str) -> int:
    """Parse a German month name to month number."""
    return _DE_MONTHS.get(month_str, 0)


def _safe_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    try:
        return float(str(val).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


class ThueringenProvider(BaseProvider):
    """Fetches real-time water levels from Thüringen HNZ portal."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None
        self._name_cache: Dict[str, Dict[str, str]] = {}

    @property
    def name(self) -> str:
        return "th_tlubn"

    @property
    def description(self) -> str:
        return "Thüringen TLUBN — ~136 gauges, real-time water levels"

    def _fetch(self) -> List[Dict[str, Any]]:
        if self._cache is not None:
            return self._cache
        logger.info("Downloading Thüringen HNZ portal from %s", PORTAL_URL)
        resp = self._session.get(PORTAL_URL, timeout=30)
        resp.raise_for_status()
        text = resp.text

        records: List[Dict[str, Any]] = []
        seen: set = set()

        # Split by "var pegelpunkt" to process each block independently
        blocks = text.split("var pegelpunkt")
        for block in blocks[1:]:
            # Skip external stations (links to other state portals)
            if _EXTERN_RE.search(block[:500]):
                continue

            coord_m = _COORD_RE.search(block)
            if not coord_m:
                continue

            sid_m = _STATION_ID_RE.search(block)
            if not sid_m:
                continue

            station_id = sid_m.group(1)
            if station_id in seen:
                continue
            seen.add(station_id)

            w_m = _W_RE.search(block)
            q_m = _Q_RE.search(block)
            ts_m = _TS_RE.search(block)

            w_val = float(w_m.group(1)) if w_m else 0.0
            q_val = _safe_float(q_m.group(1)) if q_m else 0.0

            ts = ""
            if ts_m:
                day, month_str, year, hour, minute = ts_m.groups()
                month = _parse_de_month(month_str)
                if month > 0:
                    try:
                        dt = datetime(int(year), month, int(day), int(hour), int(minute),
                                      tzinfo=timezone(timedelta(hours=1)))
                        ts = dt.isoformat()
                    except ValueError:
                        pass

            records.append({
                "station_id": station_id,
                "lat": float(coord_m.group(1)),
                "lon": float(coord_m.group(2)),
                "w": w_val,
                "q": q_val,
                "timestamp": ts,
            })

        logger.info("Parsed %d Thüringen stations from portal", len(records))
        self._cache = records
        return records

    def _fetch_station_name(self, station_id: str) -> Dict[str, str]:
        """Fetch station name and water body from per-station page."""
        if station_id in self._name_cache:
            return self._name_cache[station_id]
        result = {"name": station_id, "water_body": ""}
        try:
            url = PEGEL_URL_TEMPLATE.format(station_id=station_id)
            resp = self._session.get(url, timeout=10)
            if resp.status_code == 200:
                m = re.search(r"<h[1-3][^>]*>Pegel:\s*([^<]+)</h", resp.text)
                if m:
                    parts = m.group(1).strip().split(" / ", 1)
                    result["name"] = parts[0].strip()
                    if len(parts) > 1:
                        result["water_body"] = parts[1].strip()
        except Exception:
            pass
        self._name_cache[station_id] = result
        return result

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            station_id = rec["station_id"]
            info = self._fetch_station_name(station_id)
            results.append(StationData(
                station_id=f"th_{station_id}",
                station_name=info["name"],
                water_body=info["water_body"],
                provider=self.name,
                state="Thüringen",
                latitude=rec["lat"],
                longitude=rec["lon"],
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            if not rec["timestamp"]:
                continue
            results.append(ObservationData(
                station_id=f"th_{rec['station_id']}",
                provider=self.name,
                water_level=rec["w"],
                water_level_unit="cm",
                water_level_timestamp=rec["timestamp"],
                discharge=rec["q"],
                discharge_unit="m3/s",
                discharge_timestamp=rec["timestamp"] if rec["q"] > 0 else "",
            ))
        return results
