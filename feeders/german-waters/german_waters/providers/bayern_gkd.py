"""Bayern GKD (Gewässerkundlicher Dienst) provider — scrapes the public map page JSON.

Data source: https://www.gkd.bayern.de/de/fluesse/wasserstand
License: CC-BY 4.0 — Bayerisches Landesamt für Umwelt
"""

import json
import logging
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

WASSERSTAND_URL = "https://www.gkd.bayern.de/de/fluesse/wasserstand"
ABFLUSS_URL = "https://www.gkd.bayern.de/de/fluesse/abfluss"


def _parse_timestamp(ts: str) -> str:
    """Convert '31.03.2026 22:00' to ISO 8601 with Europe/Berlin semantics."""
    if not ts:
        return ""
    try:
        dt = datetime.strptime(ts, "%d.%m.%Y %H:%M")
        # GKD times are CET/CEST; assume UTC+1 as safe default
        from datetime import timedelta
        dt = dt.replace(tzinfo=timezone(timedelta(hours=1)))
        return dt.isoformat()
    except ValueError:
        return ts


def _extract_pointers(html: str) -> List[Dict[str, Any]]:
    """Extract the LfUMap.init({pointer:[...]}) array from the map page HTML."""
    m = re.search(r'LfUMap\.init\((\{.*?\})\);', html, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        return data.get("pointer", [])
    except (json.JSONDecodeError, KeyError):
        return []


class BayernGKDProvider(BaseProvider):
    """Fetches water level and discharge data from Bayern GKD map pages."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._ws_cache: Optional[List[Dict[str, Any]]] = None
        self._q_cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "bayern_gkd"

    @property
    def description(self) -> str:
        return "Bayern Gewässerkundlicher Dienst — ~664 gauges with water level and discharge"

    def _fetch_pointers(self, url: str) -> List[Dict[str, Any]]:
        resp = self._session.get(url, timeout=30)
        resp.raise_for_status()
        pointers = _extract_pointers(resp.text)
        logger.info("Fetched %d pointers from %s", len(pointers), url)
        return pointers

    def _ws_pointers(self) -> List[Dict[str, Any]]:
        if self._ws_cache is None:
            self._ws_cache = self._fetch_pointers(WASSERSTAND_URL)
        return self._ws_cache

    def _q_pointers(self) -> List[Dict[str, Any]]:
        if self._q_cache is None:
            self._q_cache = self._fetch_pointers(ABFLUSS_URL)
        return self._q_cache

    def invalidate(self) -> None:
        """Force re-fetch on next call."""
        self._ws_cache = None
        self._q_cache = None

    def get_stations(self) -> List[StationData]:
        pointers = self._ws_pointers()
        results: List[StationData] = []
        for p in pointers:
            station_id = p.get("p", "")
            if not station_id:
                continue
            results.append(StationData(
                station_id=f"by_{station_id}",
                station_name=p.get("n", ""),
                water_body=p.get("g", ""),
                provider=self.name,
                state="Bayern",
                latitude=float(p.get("lat", 0)),
                longitude=float(p.get("lon", 0)),
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        ws_pointers = self._ws_pointers()
        q_pointers = self._q_pointers()
        # Build discharge lookup by station ID
        q_map: Dict[str, Dict[str, Any]] = {p["p"]: p for p in q_pointers if "p" in p}

        results: List[ObservationData] = []
        for p in ws_pointers:
            station_id = p.get("p", "")
            if not station_id:
                continue
            wl_str = p.get("w", "")
            wl = 0.0
            if wl_str:
                try:
                    wl = float(wl_str.replace(",", "."))
                except ValueError:
                    pass
            wl_ts = _parse_timestamp(p.get("d", ""))

            discharge = 0.0
            discharge_ts = ""
            q_info = q_map.get(station_id)
            if q_info:
                q_str = q_info.get("w", "")
                if q_str:
                    try:
                        discharge = float(q_str.replace(",", "."))
                    except ValueError:
                        pass
                discharge_ts = _parse_timestamp(q_info.get("d", ""))

            if not wl_ts and not discharge_ts:
                continue

            results.append(ObservationData(
                station_id=f"by_{station_id}",
                provider=self.name,
                water_level=wl,
                water_level_unit="cm",
                water_level_timestamp=wl_ts,
                discharge=discharge,
                discharge_unit="m3/s",
                discharge_timestamp=discharge_ts,
            ))
        return results
