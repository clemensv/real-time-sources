"""Sachsen LfULG provider — real-time water levels from ArcGIS REST service.

Data source: https://luis.sachsen.de/
The LfULG publishes an ArcGIS MapServer with all ~190 Saxon gauges at
/arcgis/rest/services/wasser/pegelnetz/MapServer/1/query returning current
water level and discharge readings as GeoJSON.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

QUERY_URL = (
    "https://luis.sachsen.de/arcgis/rest/services/wasser/pegelnetz/MapServer/1/query"
)
QUERY_PARAMS = {
    "f": "json",
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": "4326",
    "resultRecordCount": "500",
}


def _parse_de_ts(ts_str: str, tz_str: str = "") -> str:
    """Parse 'DD.MM.YYYY HH:MM' to ISO 8601."""
    if not ts_str:
        return ""
    try:
        dt = datetime.strptime(ts_str.strip(), "%d.%m.%Y %H:%M")
        offset_hours = 1
        if tz_str:
            try:
                offset_hours = int(tz_str.replace("+", "").split(":")[0])
            except ValueError:
                pass
        dt = dt.replace(tzinfo=timezone(timedelta(hours=offset_hours)))
        return dt.isoformat()
    except ValueError:
        return ts_str


def _safe_float(val: Any) -> float:
    if val is None or val == "" or val == "---":
        return 0.0
    try:
        return float(str(val).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


class SachsenLfULGProvider(BaseProvider):
    """Fetches real-time water levels from Sachsen ArcGIS REST service."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "sn_lfulg"

    @property
    def description(self) -> str:
        return "Sachsen LfULG — ~190 gauges, real-time water levels via ArcGIS"

    def _fetch(self) -> List[Dict[str, Any]]:
        if self._cache is not None:
            return self._cache
        logger.info("Downloading Sachsen gauge data from ArcGIS")
        resp = self._session.get(QUERY_URL, params=QUERY_PARAMS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        features = data.get("features", [])
        logger.info("Received %d Sachsen features", len(features))
        self._cache = features
        return features

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        features = self._fetch()
        results: List[StationData] = []
        for feat in features:
            attrs = feat.get("attributes", {})
            geom = feat.get("geometry", {})
            station_no = attrs.get("PEG_MSTNR", "")
            if not station_no:
                continue
            lat = _safe_float(geom.get("y"))
            lon = _safe_float(geom.get("x"))

            warn_cm = _safe_float(attrs.get("PEG_AS1"))
            alarm_cm = _safe_float(attrs.get("PEG_AS3"))

            results.append(StationData(
                station_id=f"sn_{station_no}",
                station_name=attrs.get("PEG_NAME", ""),
                water_body=attrs.get("WLV_GEWAESSER", ""),
                provider=self.name,
                state="Sachsen",
                region=attrs.get("PEG_ORDNUNG_BEZ", ""),
                latitude=lat,
                longitude=lon,
                warn_level_cm=warn_cm,
                alarm_level_cm=alarm_cm,
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        features = self._fetch()
        results: List[ObservationData] = []
        for feat in features:
            attrs = feat.get("attributes", {})
            station_no = attrs.get("PEG_MSTNR", "")
            if not station_no:
                continue

            w_value = attrs.get("PEG_WASSERSTAND")
            ts_str = attrs.get("PEG_WERTZEITSTEMPEL_CHAR", "")
            tz_str = attrs.get("ZEITZONE", "+01:00")
            if w_value is None or not ts_str:
                continue

            ts = _parse_de_ts(ts_str, tz_str)
            if not ts:
                continue

            discharge = _safe_float(attrs.get("PEG_DURCHFLUSS"))

            trend = 0
            tendenz = attrs.get("TENDENZ")
            if tendenz == "steigend":
                trend = 1
            elif tendenz == "fallend":
                trend = -1

            situation = 0
            status = attrs.get("PEG_STATUS", "")
            if status:
                try:
                    situation = int(status)
                except (ValueError, TypeError):
                    pass

            results.append(ObservationData(
                station_id=f"sn_{station_no}",
                provider=self.name,
                water_level=_safe_float(w_value),
                water_level_unit="cm",
                water_level_timestamp=ts,
                discharge=discharge,
                discharge_unit="m3/s",
                discharge_timestamp=ts,
                trend=trend,
                situation=situation,
            ))
        return results
