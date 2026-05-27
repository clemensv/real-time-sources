"""Berlin SenUMVK provider — real-time water levels from wasserportal.berlin.de.

Data source: https://wasserportal.berlin.de/
The portal publishes an HTML page at /messwerte.php with inline OpenLayers
Feature objects containing all ~132 Berlin surface water gauge stations with
coordinates (UTM 33N), water level, and timestamps.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
import math
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

MESSWERTE_URL = "https://wasserportal.berlin.de/messwerte.php?anession_id=&station=&thession_id=ows&sression_id=ew"

# Extract ol.Feature blocks
_FEATURE_RE = re.compile(r"new ol\.Feature\(\{(.*?)\}\)", re.DOTALL)
_STRING_PROP_RE = re.compile(r"(\w+)\s*:\s*'([^']*)'")
_NUM_PROP_RE = re.compile(r"(\w+)\s*:\s*(-?[\d.]+)\s*[,}\n]")
_GEOM_RE = re.compile(r"new ol\.geom\.Point\(\[([^\]]+)\]")


def _utm33n_to_wgs84(easting: float, northing: float) -> tuple:
    """Approximate UTM zone 33N (EPSG:25833) to WGS84 conversion."""
    k0 = 0.9996
    a = 6378137.0
    e = 0.0818191908426
    e2 = e * e
    e_prime2 = e2 / (1 - e2)
    lon0 = math.radians(15.0)

    x = easting - 500000.0
    y = northing

    M = y / k0
    mu = M / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))

    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
    phi1 += (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
    phi1 += (151 * e1 ** 3 / 96) * math.sin(6 * mu)

    sin_phi1 = math.sin(phi1)
    cos_phi1 = math.cos(phi1)
    tan_phi1 = math.tan(phi1)
    N1 = a / math.sqrt(1 - e2 * sin_phi1 ** 2)
    T1 = tan_phi1 ** 2
    C1 = e_prime2 * cos_phi1 ** 2
    R1 = a * (1 - e2) / (1 - e2 * sin_phi1 ** 2) ** 1.5
    D = x / (N1 * k0)

    lat = phi1 - (N1 * tan_phi1 / R1) * (
        D ** 2 / 2 - (5 + 3 * T1 + 10 * C1 - 4 * C1 ** 2 - 9 * e_prime2) * D ** 4 / 24
        + (61 + 90 * T1 + 298 * C1 + 45 * T1 ** 2 - 252 * e_prime2 - 3 * C1 ** 2) * D ** 6 / 720
    )
    lon = lon0 + (D - (1 + 2 * T1 + C1) * D ** 3 / 6
                  + (5 - 2 * C1 + 28 * T1 - 3 * C1 ** 2 + 8 * e_prime2 + 24 * T1 ** 2) * D ** 5 / 120
                  ) / cos_phi1

    return math.degrees(lat), math.degrees(lon)


def _safe_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    try:
        return float(str(val).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


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


class BerlinProvider(BaseProvider):
    """Fetches real-time water levels from Berlin Wasserportal."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "be_senumvk"

    @property
    def description(self) -> str:
        return "Berlin SenUMVK — ~132 gauges, real-time water levels"

    def _fetch(self) -> List[Dict[str, Any]]:
        if self._cache is not None:
            return self._cache
        logger.info("Downloading Berlin messwerte from %s", MESSWERTE_URL)
        resp = self._session.get(MESSWERTE_URL, timeout=30)
        resp.raise_for_status()
        text = resp.text

        stations: List[Dict[str, Any]] = []
        seen: set = set()
        for m in _FEATURE_RE.finditer(text):
            feat_text = m.group(1)
            props: Dict[str, Any] = {}

            for sm in _STRING_PROP_RE.finditer(feat_text):
                props[sm.group(1)] = sm.group(2)

            for nm in _NUM_PROP_RE.finditer(feat_text):
                key = nm.group(1)
                if key not in props:
                    props[key] = nm.group(2)

            gm = _GEOM_RE.search(feat_text)
            if gm:
                props["_geom"] = gm.group(1)

            # Must have a pegel/pkz to be a station
            pkz = props.get("pkz", "")
            if not pkz or pkz in seen:
                continue
            seen.add(pkz)

            # Convert UTM33N to WGS84
            lat, lon = 0.0, 0.0
            geom_str = props.get("_geom", "")
            if geom_str:
                parts = geom_str.split(",")
                if len(parts) == 2:
                    easting = _safe_float(parts[0])
                    northing = _safe_float(parts[1])
                    if easting > 0 and northing > 0:
                        lat, lon = _utm33n_to_wgs84(easting, northing)

            stations.append({
                "pkz": pkz,
                "name": props.get("name", ""),
                "water_body": props.get("gewaesser", ""),
                "lat": lat,
                "lon": lon,
                "wert": props.get("wert", ""),
                "zeit": props.get("zeit", ""),
                "betreiber": props.get("betreiber", ""),
                "alarmklasse": props.get("alarmklasse", "0"),
            })

        logger.info("Parsed %d Berlin stations from messwerte page", len(stations))
        self._cache = stations
        return stations

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            results.append(StationData(
                station_id=f"be_{rec['pkz']}",
                station_name=rec["name"],
                water_body=rec["water_body"],
                provider=self.name,
                state="Berlin",
                latitude=rec["lat"],
                longitude=rec["lon"],
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            wert = rec.get("wert", "")
            zeit = rec.get("zeit", "")
            if not wert or not zeit:
                continue

            ts = _parse_de_ts(zeit)
            if not ts:
                continue

            situation = 0
            alarm = rec.get("alarmklasse", "0")
            try:
                situation = int(alarm)
            except (ValueError, TypeError):
                pass

            results.append(ObservationData(
                station_id=f"be_{rec['pkz']}",
                provider=self.name,
                water_level=_safe_float(wert),
                water_level_unit="cm",
                water_level_timestamp=ts,
                situation=situation,
            ))
        return results
