"""Baden-Württemberg HVZ provider — real-time water levels from hvz.baden-wuerttemberg.de.

Data source: https://www.hvz.baden-wuerttemberg.de/
The HVZ publishes a JavaScript file at /js/hvz_peg_stmn.js containing all
~333 BW gauge station master data with current water levels, discharge, and
timestamps as a JS array (HVZ_Site.PEG_DB).  Column layout is defined in
/js/hvz_peg_var.js.

License: Datenlizenz Deutschland – Namensnennung (dl-de/by-2-0)
"""

import logging
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

DATA_URL = "https://www.hvz.baden-wuerttemberg.de/js/hvz_peg_stmn.js"

# Column indices from hvz_peg_var.js
POS_DASA = 0    # station ID
POS_NAME = 1    # station name
POS_GEW = 2     # water body (Gewässer)
POS_W = 4       # water level (cm)
POS_WD = 5      # W unit
POS_WZ = 6      # W timestamp
POS_Q = 7       # discharge
POS_QD = 8      # Q unit
POS_QZ = 9      # Q timestamp
POS_FILE = 11   # long name / location
POS_OST = 22    # longitude (geographic)
POS_NORD = 23   # latitude (geographic)
POS_HMO = 24    # HMO alarm threshold
POS_EZG = 25    # catchment area


def _parse_de_ts(ts_str: str) -> str:
    """Parse 'DD.MM.YYYY HH:MM MESZ/MEZ' to ISO 8601."""
    if not ts_str:
        return ""
    try:
        ts_str = ts_str.strip()
        is_cest = "MESZ" in ts_str
        ts_clean = ts_str.replace(" MESZ", "").replace(" MEZ", "").strip()
        dt = datetime.strptime(ts_clean, "%d.%m.%Y %H:%M")
        offset = timedelta(hours=2) if is_cest else timedelta(hours=1)
        dt = dt.replace(tzinfo=timezone(offset))
        return dt.isoformat()
    except ValueError:
        return ts_str


def _safe_float(val: Any) -> float:
    if val is None or val == "" or val == "---" or val == 0:
        return 0.0
    try:
        return float(str(val).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


def _parse_js_array(text: str) -> List[List[Any]]:
    """Extract the HVZ_Site.PEG_DB array from the JS file, parse as nested lists."""
    start = text.find("HVZ_Site.PEG_DB =")
    if start < 0:
        return []
    bracket_start = text.find("[", start)
    bracket_end = text.rfind("];")
    if bracket_start < 0 or bracket_end < 0:
        return []
    array_text = text[bracket_start:bracket_end + 1]

    # Replace JS single-quoted strings with double-quoted for JSON parsing.
    # The JS uses single-quoted strings; we convert carefully.
    # Strategy: use regex to find each inner array and parse it
    rows: List[List[Any]] = []
    # Each row is [...], separated by commas in outer array
    for m in re.finditer(r"\[([^\[\]]+)\]", array_text):
        row_text = m.group(1).strip()
        if not row_text:
            continue
        # Convert single quotes to double quotes for string values
        row_text = row_text.replace("'", '"')
        try:
            import json
            row = json.loads(f"[{row_text}]")
            rows.append(row)
        except Exception:
            continue
    return rows


class BadenWuerttembergProvider(BaseProvider):
    """Fetches real-time water levels from BW HVZ JS data files."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[List[Any]]] = None

    @property
    def name(self) -> str:
        return "bw_hvz"

    @property
    def description(self) -> str:
        return "Baden-Württemberg HVZ — ~333 gauges, real-time water levels"

    def _fetch(self) -> List[List[Any]]:
        if self._cache is not None:
            return self._cache
        logger.info("Downloading BW station data from %s", DATA_URL)
        resp = self._session.get(DATA_URL, timeout=30)
        resp.raise_for_status()
        rows = _parse_js_array(resp.text)
        # Filter out empty rows
        rows = [r for r in rows if len(r) > POS_NORD and r[POS_DASA]]
        logger.info("Parsed %d BW station records", len(rows))
        self._cache = rows
        return rows

    def invalidate(self) -> None:
        self._cache = None

    def _get(self, row: List[Any], idx: int) -> Any:
        if idx < len(row):
            return row[idx]
        return None

    def get_stations(self) -> List[StationData]:
        rows = self._fetch()
        results: List[StationData] = []
        for row in rows:
            station_id = str(self._get(row, POS_DASA) or "")
            if not station_id:
                continue
            lat = _safe_float(self._get(row, POS_NORD))
            lon = _safe_float(self._get(row, POS_OST))
            warn_cm = _safe_float(self._get(row, POS_HMO))

            results.append(StationData(
                station_id=f"bw_{station_id}",
                station_name=str(self._get(row, POS_NAME) or ""),
                water_body=str(self._get(row, POS_GEW) or ""),
                provider=self.name,
                state="Baden-Württemberg",
                latitude=lat,
                longitude=lon,
                warn_level_cm=warn_cm,
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        rows = self._fetch()
        results: List[ObservationData] = []
        for row in rows:
            station_id = str(self._get(row, POS_DASA) or "")
            if not station_id:
                continue
            w_val = self._get(row, POS_W)
            w_ts = str(self._get(row, POS_WZ) or "")
            if w_val is None or w_val == "" or not w_ts:
                continue

            ts = _parse_de_ts(w_ts)
            if not ts:
                continue

            discharge = _safe_float(self._get(row, POS_Q))
            discharge_ts = _parse_de_ts(str(self._get(row, POS_QZ) or ""))

            results.append(ObservationData(
                station_id=f"bw_{station_id}",
                provider=self.name,
                water_level=_safe_float(w_val),
                water_level_unit=str(self._get(row, POS_WD) or "cm"),
                water_level_timestamp=ts,
                discharge=discharge,
                discharge_unit=str(self._get(row, POS_QD) or "m3/s"),
                discharge_timestamp=discharge_ts,
            ))
        return results
