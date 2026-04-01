"""Hessen HLNUG provider — real-time water levels from WISKI-Web3 at hlnug.de.

Data source: https://www.hlnug.de/static/pegel/wiskiweb3/
The portal publishes a WISKI-Web3 JSON file at
data/internet/layers/10/index.json containing current water level readings
for ~186 Hessen gauges.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

LAYER_URL = "https://www.hlnug.de/static/pegel/wiskiweb3/data/internet/layers/10/index.json"
DISCHARGE_URL = "https://www.hlnug.de/static/pegel/wiskiweb3/data/internet/layers/20/index.json"


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


class HessenHLNUGProvider(BaseProvider):
    """Fetches real-time water levels from HLNUG WISKI-Web3 portal."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._w_cache: Optional[List[Dict[str, Any]]] = None
        self._q_cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "he_hlnug"

    @property
    def description(self) -> str:
        return "Hessen HLNUG — ~186 gauges, 15-min real-time water levels"

    def _fetch_layer(self, url: str) -> List[Dict[str, Any]]:
        logger.info("Downloading Hessen layer from %s", url)
        resp = self._session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _w_records(self) -> List[Dict[str, Any]]:
        if self._w_cache is None:
            self._w_cache = self._fetch_layer(LAYER_URL)
            logger.info("Received %d Hessen Wasserstand records", len(self._w_cache))
        return self._w_cache

    def _q_records(self) -> List[Dict[str, Any]]:
        if self._q_cache is None:
            try:
                self._q_cache = self._fetch_layer(DISCHARGE_URL)
                logger.info("Received %d Hessen Durchfluss records", len(self._q_cache))
            except Exception:
                self._q_cache = []
        return self._q_cache

    def invalidate(self) -> None:
        self._w_cache = None
        self._q_cache = None

    def get_stations(self) -> List[StationData]:
        records = self._w_records()
        results: List[StationData] = []
        for rec in records:
            station_no = rec.get("station_no", "")
            if not station_no:
                continue
            lat = _safe_float(rec.get("station_latitude"))
            lon = _safe_float(rec.get("station_longitude"))
            results.append(StationData(
                station_id=f"he_{station_no}",
                station_name=rec.get("station_name", ""),
                water_body=rec.get("WTO_OBJECT", rec.get("EXTERN-WATERS-NAME", "")),
                provider=self.name,
                state="Hessen",
                region=rec.get("hydrounit_name", ""),
                latitude=lat,
                longitude=lon,
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        w_records = self._w_records()
        q_records = self._q_records()
        q_map: Dict[str, Dict[str, Any]] = {}
        for rec in q_records:
            sno = rec.get("station_no", "")
            if sno:
                q_map[sno] = rec

        results: List[ObservationData] = []
        for rec in w_records:
            station_no = rec.get("station_no", "")
            ts_value = rec.get("ts_value")
            timestamp = rec.get("timestamp", "")
            if not station_no or ts_value is None or not timestamp:
                continue

            ts = _parse_iso_ts(timestamp)
            if not ts:
                continue

            discharge = 0.0
            discharge_ts = ""
            q_rec = q_map.get(station_no)
            if q_rec:
                discharge = _safe_float(q_rec.get("ts_value"))
                discharge_ts = _parse_iso_ts(q_rec.get("timestamp", ""))

            results.append(ObservationData(
                station_id=f"he_{station_no}",
                provider=self.name,
                water_level=_safe_float(ts_value),
                water_level_unit=rec.get("ts_unitsymbol", "cm"),
                water_level_timestamp=ts,
                discharge=discharge,
                discharge_unit="m3/s",
                discharge_timestamp=discharge_ts,
            ))
        return results
