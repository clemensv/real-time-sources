"""NRW Hydrologie provider — real-time water levels from LANUV hydrologie portal.

Data source: https://hydrologie.nrw.de/
The portal publishes a static JSON file at /data/internet/layers/10/index.json
containing current water level readings for ~300 NRW gauges, regenerated every
~15 minutes.  This replaces the older daily-batch OpenHYGON ZIP approach.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

LAYER_URL = "https://hydrologie.nrw.de/data/internet/layers/10/index.json"


def _parse_iso_ts(ts: str) -> str:
    """Normalise ISO 8601 timestamp."""
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
    """Convert a value to float, returning 0.0 on failure."""
    if val is None or val == "":
        return 0.0
    try:
        return float(str(val).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


class NRWHygonProvider(BaseProvider):
    """Fetches real-time 15-min water levels from LANUV hydrologie.nrw.de."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "nrw_hygon"

    @property
    def description(self) -> str:
        return "NRW LANUV Hydrologie — ~300 gauges, 15-min real-time water levels"

    def _fetch(self) -> List[Dict[str, Any]]:
        """Download the layer-10 JSON (all Wasserstand stations + latest values)."""
        if self._cache is not None:
            return self._cache
        logger.info("Downloading NRW water level layer from %s", LAYER_URL)
        resp = self._session.get(LAYER_URL, timeout=30, verify=False)
        resp.raise_for_status()
        records = resp.json()
        logger.info("Received %d NRW station records", len(records))
        self._cache = records
        return records

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            station_no = rec.get("station_no", "")
            if not station_no:
                continue

            lat = _safe_float(rec.get("station_latitude"))
            lon = _safe_float(rec.get("station_longitude"))

            warn_cm = _safe_float(rec.get("LANUV_Info_1"))
            alarm_cm = _safe_float(rec.get("LANUV_Info_3"))

            results.append(StationData(
                station_id=f"nrw_{station_no}",
                station_name=rec.get("station_name", ""),
                water_body=rec.get("WTO_OBJECT", ""),
                provider=self.name,
                state="Nordrhein-Westfalen",
                region=rec.get("catchment_name", ""),
                latitude=lat,
                longitude=lon,
                station_type=rec.get("WEB_STATYPE", ""),
                warn_level_cm=warn_cm,
                alarm_level_cm=alarm_cm,
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            station_no = rec.get("station_no", "")
            ts_value = rec.get("ts_value")
            timestamp = rec.get("timestamp", "")
            if not station_no or ts_value is None or not timestamp:
                continue

            value = _safe_float(ts_value)
            ts = _parse_iso_ts(timestamp)
            if not ts:
                continue

            situation = 0
            classification = rec.get("classification")
            if classification == "HN7W":
                situation = 2
            elif classification == "N7W":
                situation = 1

            results.append(ObservationData(
                station_id=f"nrw_{station_no}",
                provider=self.name,
                water_level=value,
                water_level_unit=rec.get("ts_unitsymbol", "cm"),
                water_level_timestamp=ts,
                situation=situation,
            ))
        return results
