"""Brandenburg LfU provider — real-time water levels from pegelportal.brandenburg.de.

Data source: https://pegelportal.brandenburg.de/
The portal publishes a large HTML page with inline OpenLayers Feature objects
containing all ~270 Brandenburg gauge stations with current water levels,
discharge, timestamps, and coordinates in ETRS89/UTM33N.

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

PORTAL_URL = "https://pegelportal.brandenburg.de/"


def _utm33n_to_wgs84(easting: float, northing: float) -> tuple:
    """Approximate UTM zone 33N (EPSG:25833) to WGS84 conversion."""
    # Uses simplified Karney/Helmert inverse projection
    # Accuracy: ~1m, sufficient for station locations
    k0 = 0.9996
    a = 6378137.0
    e = 0.0818191908426
    e2 = e * e
    e_prime2 = e2 / (1 - e2)
    lon0 = math.radians(15.0)  # UTM zone 33 central meridian

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
    if val is None or val == "" or val == "-":
        return 0.0
    try:
        return float(str(val).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


def _parse_de_ts(datum: str, zeit: str) -> str:
    """Parse 'DD.MM.YYYY' + 'HH:MM' to ISO 8601."""
    if not datum or not zeit:
        return ""
    try:
        dt = datetime.strptime(f"{datum.strip()} {zeit.strip()}", "%d.%m.%Y %H:%M")
        dt = dt.replace(tzinfo=timezone(timedelta(hours=1)))
        return dt.isoformat()
    except ValueError:
        return ""


_FEATURE_RE = re.compile(r"new ol\.Feature\(\{(.*?)\}\)", re.DOTALL)
_STRING_PROP_RE = re.compile(r"(\w+)\s*:\s*'([^']*)'")
_NUM_PROP_RE = re.compile(r"(\w+)\s*:\s*(-?[\d.]+)\s*[,}]")
_GEOM_RE = re.compile(r"new ol\.geom\.Point\(\[([^\]]+)\]")


class BrandenburgProvider(BaseProvider):
    """Fetches real-time water levels from Brandenburg Pegelportal."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, str]]] = None

    @property
    def name(self) -> str:
        return "bb_lfu"

    @property
    def description(self) -> str:
        return "Brandenburg LfU — ~270 gauges, real-time water levels"

    def _fetch(self) -> List[Dict[str, str]]:
        if self._cache is not None:
            return self._cache
        logger.info("Downloading Brandenburg portal from %s", PORTAL_URL)
        resp = self._session.get(PORTAL_URL, timeout=60, allow_redirects=True)
        resp.raise_for_status()
        text = resp.text

        stations: List[Dict[str, str]] = []
        for m in _FEATURE_RE.finditer(text):
            feat_text = m.group(1)
            props: Dict[str, str] = {}
            for sm in _STRING_PROP_RE.finditer(feat_text):
                props[sm.group(1)] = sm.group(2)

            # Only pick actual station features ('bb' and 'bbalarm')
            pegel_type = props.get("pegel", "")
            if pegel_type not in ("bb", "bbalarm"):
                continue
            # Only Brandenburg-operated stations
            if props.get("pegelinbb") != "1":
                continue

            gm = _GEOM_RE.search(feat_text)
            if gm:
                props["_geom"] = gm.group(1)

            stations.append(props)

        logger.info("Parsed %d Brandenburg stations from portal", len(stations))
        self._cache = stations
        return stations

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            pkz = rec.get("pkz", "")
            if not pkz:
                continue

            lat, lon = 0.0, 0.0
            geom_str = rec.get("_geom", "")
            if geom_str:
                parts = geom_str.split(",")
                if len(parts) == 2:
                    easting = _safe_float(parts[0])
                    northing = _safe_float(parts[1])
                    if easting > 0 and northing > 0:
                        lat, lon = _utm33n_to_wgs84(easting, northing)

            results.append(StationData(
                station_id=f"bb_{pkz}",
                station_name=rec.get("name", ""),
                water_body=rec.get("gewaesser", ""),
                provider=self.name,
                state="Brandenburg",
                latitude=lat,
                longitude=lon,
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            pkz = rec.get("pkz", "")
            if not pkz:
                continue

            wert = rec.get("wert", "")
            datum = rec.get("datum", "")
            zeit = rec.get("zeit", "")
            if not wert or not datum or not zeit:
                continue

            ts = _parse_de_ts(datum, zeit)
            if not ts:
                continue

            discharge = _safe_float(rec.get("qwert"))

            trend = 0
            tendenz = rec.get("wstendenz", "")
            if tendenz == "1":
                trend = 1
            elif tendenz == "3":
                trend = -1

            situation = 0
            alarm = rec.get("alarmklasse", "0")
            try:
                situation = int(alarm)
            except (ValueError, TypeError):
                pass

            results.append(ObservationData(
                station_id=f"bb_{pkz}",
                provider=self.name,
                water_level=_safe_float(wert),
                water_level_unit="cm",
                water_level_timestamp=ts,
                discharge=discharge,
                discharge_unit="m3/s",
                discharge_timestamp=ts if discharge > 0 else "",
                trend=trend,
                situation=situation,
            ))
        return results
