"""Mecklenburg-Vorpommern LUNG provider — real-time water levels from pegelportal-mv.de.

Data source: https://pegelportal-mv.de/
The portal publishes an HTML table at /pegel_list.html containing all ~237
Land MV gauge stations with current water level, discharge, timestamps, and
alarm stage.  Station coordinates are not available in the table; only pixel
positions on the map image.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

LIST_URL = "https://pegelportal-mv.de/pegel_list.html"

# Each row: <tr><td class='info'>Name</td><td>water body</td><td>timestamp</td><td>W</td><td>Q</td><td>alarm img</td><td>link with station ID</td>...
_ROW_RE = re.compile(
    r"<tr>\s*"
    r"<td[^>]*>([^<]+)</td>\s*"           # station name
    r"<td>([^<]*)</td>\s*"                 # water body
    r"<td>([^<]*)</td>\s*"                 # timestamp
    r"<td>([^<]*)</td>\s*"                 # W (cm)
    r"<td>([^<]*)</td>\s*"                 # Q (m³/s)
    r"<td>.*?</td>\s*"                     # alarm image
    r"<td>.*?href='(\d+\.\d+)\.html'",    # station ID from verlauf link
    re.DOTALL,
)


def _parse_de_ts(ts_str: str) -> str:
    """Parse 'DD.MM.YYYY HH:MM' to ISO 8601."""
    if not ts_str or not ts_str.strip():
        return ""
    try:
        dt = datetime.strptime(ts_str.strip(), "%d.%m.%Y %H:%M")
        dt = dt.replace(tzinfo=timezone(timedelta(hours=1)))
        return dt.isoformat()
    except ValueError:
        return ""


def _safe_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    try:
        return float(str(val).strip().replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


class MecklenburgVorpommernProvider(BaseProvider):
    """Fetches real-time water levels from MV Pegelportal HTML table."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "mv_lung"

    @property
    def description(self) -> str:
        return "Mecklenburg-Vorpommern LUNG — ~237 gauges, real-time water levels"

    def _fetch(self) -> List[Dict[str, Any]]:
        if self._cache is not None:
            return self._cache
        logger.info("Downloading MV station list from %s", LIST_URL)
        resp = self._session.get(LIST_URL, timeout=30)
        resp.raise_for_status()
        text = resp.text

        records: List[Dict[str, Any]] = []
        seen: set = set()
        for m in _ROW_RE.finditer(text):
            name, water_body, ts_str, w_str, q_str, station_id = m.groups()
            if station_id in seen:
                continue
            seen.add(station_id)

            name_clean = name.strip()
            water_clean = water_body.strip()

            # Extract alarm stage from nearby img title if present
            alarm = ""
            alarm_m = re.search(
                r"title='Pegel-Stufe\s+(\d+)'",
                text[m.start():m.end() + 200],
            )
            if alarm_m:
                alarm = alarm_m.group(1)

            records.append({
                "station_id": station_id.strip(),
                "name": name_clean,
                "water_body": water_clean,
                "timestamp": ts_str.strip(),
                "w": w_str.strip(),
                "q": q_str.strip(),
                "alarm": alarm,
            })

        logger.info("Parsed %d MV station records", len(records))
        self._cache = records
        return records

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            results.append(StationData(
                station_id=f"mv_{rec['station_id']}",
                station_name=rec["name"],
                water_body=rec["water_body"],
                provider=self.name,
                state="Mecklenburg-Vorpommern",
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            w_val = rec.get("w", "")
            ts_str = rec.get("timestamp", "")
            if not w_val or not ts_str:
                continue

            ts = _parse_de_ts(ts_str)
            if not ts:
                continue

            situation = 0
            alarm = rec.get("alarm", "")
            if alarm:
                try:
                    situation = int(re.sub(r'[^0-9]', '', alarm) or "0")
                except ValueError:
                    pass

            results.append(ObservationData(
                station_id=f"mv_{rec['station_id']}",
                provider=self.name,
                water_level=_safe_float(w_val),
                water_level_unit="cm",
                water_level_timestamp=ts,
                discharge=_safe_float(rec.get("q")),
                discharge_unit="m3/s",
                discharge_timestamp=ts if _safe_float(rec.get("q")) > 0 else "",
                situation=situation,
            ))
        return results
