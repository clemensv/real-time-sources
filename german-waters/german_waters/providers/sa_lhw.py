"""Sachsen-Anhalt LHW provider — real-time water levels from hvz.lsaurl.de.

Data source: https://hvz.lsaurl.de/
The portal publishes a WISKI-Web JSON file at
/data/internet/layers/1030/index.json containing current water level readings
for ~214 gauges across Sachsen-Anhalt and neighboring stations.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

LAYER_URL = "https://hvz.lsaurl.de/data/internet/layers/1030/index.json"


def _parse_iso_ts(ts: str) -> str:
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts.strip())
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone(timedelta(hours=1)))
        return dt.isoformat()
    except ValueError:
        return ts


def _safe_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    try:
        return float(str(val).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


class SachsenAnhaltProvider(BaseProvider):
    """Fetches real-time water levels from LHW Sachsen-Anhalt WISKI portal."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "sa_lhw"

    @property
    def description(self) -> str:
        return "Sachsen-Anhalt LHW — ~100 state gauges, 15-min real-time water levels"

    def _fetch(self) -> List[Dict[str, Any]]:
        if self._cache is not None:
            return self._cache
        logger.info("Downloading SA water level layer from %s", LAYER_URL)
        resp = self._session.get(LAYER_URL, timeout=30)
        resp.raise_for_status()
        records = resp.json()
        # Filter to LHW-owned stations only (state gauges)
        records = [r for r in records if r.get("metadata_EIGENTUMSVERHALTNISSE") == "LHW"]
        logger.info("Received %d SA LHW station records", len(records))
        self._cache = records
        return records

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            station_no = rec.get("metadata_station_no", "")
            if not station_no:
                continue
            lat = _safe_float(rec.get("metadata_station_latitude"))
            lon = _safe_float(rec.get("metadata_station_longitude"))
            results.append(StationData(
                station_id=f"sa_{station_no}",
                station_name=rec.get("metadata_station_name", ""),
                water_body=rec.get("metadata_river_name", ""),
                provider=self.name,
                state="Sachsen-Anhalt",
                region=rec.get("metadata_web_area", ""),
                latitude=lat,
                longitude=lon,
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            station_no = rec.get("metadata_station_no", "")
            if not station_no:
                continue
            w_value = rec.get("L1_ts_value")
            w_ts = rec.get("L1_timestamp", "")
            if w_value is None or not w_ts:
                continue
            ts = _parse_iso_ts(w_ts)
            if not ts:
                continue

            discharge = _safe_float(rec.get("L9_ts_value"))
            discharge_ts = _parse_iso_ts(rec.get("L9_timestamp", ""))

            trend = 0
            tendenz = rec.get("L2_ts_value")
            if tendenz is not None:
                try:
                    trend = int(tendenz)
                except (ValueError, TypeError):
                    pass

            results.append(ObservationData(
                station_id=f"sa_{station_no}",
                provider=self.name,
                water_level=_safe_float(w_value),
                water_level_unit=rec.get("L1_ts_unitsymbol", "cm"),
                water_level_timestamp=ts,
                discharge=discharge,
                discharge_unit="m3/s",
                discharge_timestamp=discharge_ts,
                trend=trend,
            ))
        return results
