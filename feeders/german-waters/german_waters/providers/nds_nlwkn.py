"""Niedersachsen NLWKN provider — real-time water levels from NLWKN Pegelonline API.

Data source: https://www.pegelonline.nlwkn.niedersachsen.de/
API:         https://bis.azure-api.net/PegelonlineNeu/REST/
The NLWKN publishes an Azure-hosted REST API returning all ~200 Niedersachsen
gauges with 15-min real-time water level readings in a single JSON response.

License: Datenlizenz Deutschland – Namensnennung (dl-de/by-2-0)
"""

import logging
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

API_BASE = "https://bis.azure-api.net/PegelonlineNeu/REST"
API_KEY = "19094e54510d4e89b140ff2d3abf715f"

STATIONS_URL = f"{API_BASE}/stammdaten/stationen//allepegelmitaktuellemmesswert"


def _parse_ts(ts_text: str) -> str:
    """Parse 'DD.MM.YYYY HH:MM' to ISO 8601 with CET offset."""
    if not ts_text:
        return ""
    try:
        dt = datetime.strptime(ts_text.strip(), "%d.%m.%Y %H:%M")
        dt = dt.replace(tzinfo=timezone(timedelta(hours=1)))
        return dt.isoformat()
    except ValueError:
        return ts_text


class NiedersachsenProvider(BaseProvider):
    """Fetches real-time water levels from NLWKN Pegelonline API."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "nds_nlwkn"

    @property
    def description(self) -> str:
        return "Niedersachsen NLWKN — ~200 gauges, 15-min real-time water levels"

    def _fetch(self) -> List[Dict[str, Any]]:
        """Download all stations with current readings from the NLWKN API."""
        if self._cache is not None:
            return self._cache
        logger.info("Downloading NDS stations from NLWKN API")
        resp = self._session.get(
            STATIONS_URL,
            params={"subscription-key": API_KEY},
            timeout=30,
        )
        resp.raise_for_status()
        records = resp.json().get("getStammdatenResult", [])
        logger.info("Received %d NDS station records", len(records))
        self._cache = records
        return records

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            sta_id = rec.get("STA_ID")
            if sta_id is None:
                continue

            # NB: the API has Latitude/Longitude swapped
            lat = float(rec.get("Longitude", 0) or rec.get("WGS84Rechtswert", 0) or 0)
            lon = float(rec.get("Latitude", 0) or rec.get("WGS84Hochwert", 0) or 0)

            # Extract warn/alarm levels from nested Meldestufen
            warn_cm = 0.0
            alarm_cm = 0.0
            for param in rec.get("Parameter", []):
                for ds in param.get("Datenspuren", []):
                    for ms in ds.get("Meldestufen", []):
                        stufe = ms.get("Stufe", 0)
                        wert = ms.get("Wert", 0)
                        if stufe == 1 and wert:
                            warn_cm = float(wert)
                        elif stufe == 3 and wert:
                            alarm_cm = float(wert)
                    break  # only first Datenspur per parameter
                break  # only first parameter

            results.append(StationData(
                station_id=f"nds_{sta_id}",
                station_name=rec.get("Name", ""),
                water_body=rec.get("GewaesserName", ""),
                provider=self.name,
                state="Niedersachsen",
                latitude=lat,
                longitude=lon,
                altitude=rec.get("Hoehe", 0.0) or 0.0,
                station_type=rec.get("Stationsart_Text", "").strip(),
                warn_level_cm=warn_cm,
                alarm_level_cm=alarm_cm,
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            sta_id = rec.get("STA_ID")
            if sta_id is None:
                continue

            for param in rec.get("Parameter", []):
                for ds in param.get("Datenspuren", []):
                    value = ds.get("AktuellerMesswert")
                    ts_text = ds.get("AktuellerMesswert_Zeitpunkt", "")
                    if value is None or value == -888 or not ts_text:
                        continue

                    ts = _parse_ts(ts_text)
                    if not ts:
                        continue

                    situation = int(ds.get("AktuelleMeldeStufe", 0) or 0)

                    results.append(ObservationData(
                        station_id=f"nds_{sta_id}",
                        provider=self.name,
                        water_level=float(value),
                        water_level_unit="cm",
                        water_level_timestamp=ts,
                        situation=situation,
                    ))
                    break  # only first Datenspur (water level) per station
                break  # only first parameter
        return results
