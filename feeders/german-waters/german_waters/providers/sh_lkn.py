"""Schleswig-Holstein HSI provider — real-time readings from hsi-sh.de.

Data source: https://hsi-sh.de/  (HTML page with embedded station data)
The HSI portal publishes a map page containing all active SH gauges with
their current water level readings, regenerated every ~15 minutes.
Only local Landespegel (station numbers starting with 11) are emitted;
federal stations are covered by pegelonline.

License: Datenlizenz Deutschland – Zero (dl-de/zero-2-0)
"""

import logging
import re
from datetime import timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

from german_waters.providers import BaseProvider, StationData, ObservationData

logger = logging.getLogger(__name__)

HSI_URL = "https://hsi-sh.de/"

# Regex to extract station tooltip blocks from the HSI page HTML.
# Each block has: station_no, name, water body, W reading, optional Q reading
_BLOCK_RE = re.compile(
    r"id='tooltip-content-(\d+)'[^>]*>.*?"
    r"class='sortclass[^']*'>([^<]+)</h1>.*?"
    r"tooltip-content__gewaesser'>([^<]+)</dd>.*?"
    r"tooltip-content__w'>([^<]*)</dd>",
    re.DOTALL,
)

# Parse "170 cm 31.03.2026 21:00" from the W field
_VALUE_RE = re.compile(
    r"(-?\d+(?:,\d+)?)\s*(cm)\s+(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}):(\d{2})"
)


class SchleswigHolsteinProvider(BaseProvider):
    """Fetches real-time water levels for SH Landespegel from hsi-sh.de."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "german-waters-bridge/1.0"
        self._cache: Optional[List[Dict[str, Any]]] = None

    @property
    def name(self) -> str:
        return "sh_lkn"

    @property
    def description(self) -> str:
        return "Schleswig-Holstein HSI — ~72 local gauges, 15-min real-time"

    def _fetch(self) -> List[Dict[str, Any]]:
        """Download and parse the HSI landing page for station data."""
        if self._cache is not None:
            return self._cache
        logger.info("Downloading SH HSI page from %s", HSI_URL)
        resp = self._session.get(HSI_URL, timeout=30)
        resp.raise_for_status()
        text = resp.text

        records: List[Dict[str, Any]] = []
        seen: set = set()
        for station_no, header, water, w_raw in _BLOCK_RE.findall(text):
            # Only emit local Landespegel (11xxxx); federal stations start with
            # other prefixes and are covered by the pegelonline bridge.
            if not station_no.startswith("11"):
                continue
            if station_no in seen:
                continue
            seen.add(station_no)

            name = header.strip()
            # Header format: "Wrist - 114134"
            if " - " in name:
                name = name.rsplit(" - ", 1)[0]

            w_raw = w_raw.strip()
            wm = _VALUE_RE.match(w_raw)
            value: Optional[float] = None
            timestamp = ""
            if wm:
                value = float(wm.group(1).replace(",", "."))
                timestamp = (
                    f"{wm.group(5)}-{wm.group(4)}-{wm.group(3)}"
                    f"T{wm.group(6)}:{wm.group(7)}:00+01:00"
                )

            records.append({
                "station_no": station_no,
                "name": name,
                "water": water.strip(),
                "value": value,
                "unit": "cm",
                "timestamp": timestamp,
            })

        logger.info("Parsed %d local SH stations from HSI page", len(records))
        self._cache = records
        return records

    def invalidate(self) -> None:
        self._cache = None

    def get_stations(self) -> List[StationData]:
        records = self._fetch()
        results: List[StationData] = []
        for rec in records:
            results.append(StationData(
                station_id=f"sh_{rec['station_no']}",
                station_name=rec["name"],
                water_body=rec["water"],
                provider=self.name,
                state="Schleswig-Holstein",
            ))
        return results

    def get_observations(self) -> List[ObservationData]:
        records = self._fetch()
        results: List[ObservationData] = []
        for rec in records:
            if rec["value"] is None or not rec["timestamp"]:
                continue
            results.append(ObservationData(
                station_id=f"sh_{rec['station_no']}",
                provider=self.name,
                water_level=rec["value"],
                water_level_unit=rec["unit"],
                water_level_timestamp=rec["timestamp"],
            ))
        return results
