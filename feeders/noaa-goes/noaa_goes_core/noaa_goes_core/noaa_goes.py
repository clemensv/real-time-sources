"""
Transport-neutral acquisition and state handling for the NOAA SWPC Space Weather bridge.

Polls the NOAA Space Weather Prediction Center (SWPC) and GOES satellite JSON
endpoints and returns raw-dict records ready for any transport layer.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-noaa-goes/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

__all__ = ["SWPCFetcher", "USER_AGENT"]


class SWPCFetcher:
    """
    Transport-neutral fetcher for NOAA SWPC and GOES endpoints.

    Provides poll_* methods that return raw dicts and state
    management (load_state / save_state) that any transport layer
    can use for deduplication.
    """

    ALERTS_URL = "https://services.swpc.noaa.gov/products/alerts.json"
    K_INDEX_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    SOLAR_WIND_SPEED_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json"
    SOLAR_WIND_MAG_FIELD_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json"
    PLASMA_URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
    MAG_URL = "https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json"
    XRAYS_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json"
    PROTONS_URL = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json"
    ELECTRONS_URL = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-3-day.json"
    MAGNETOMETERS_URL = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-7-day.json"
    FLARES_URL = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json"
    POLL_INTERVAL_SECONDS = 60

    def __init__(self, last_polled_file: str) -> None:
        self.last_polled_file = last_polled_file

    # ------------------------------------------------------------------ state

    def load_state(self) -> Dict:
        """Load deduplication state from the state file."""
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def save_state(self, state: Dict) -> None:
        """Persist deduplication state to the state file."""
        try:
            dir_path = os.path.dirname(self.last_polled_file)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(self.last_polled_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error("Error saving state: %s", e)

    # ---------------------------------------------------------- HTTP helpers

    def _get_json(self, url: str) -> Optional[list]:
        """Fetch a JSON URL and return a list (or None on error)."""
        try:
            response = requests.get(
                url, headers={"User-Agent": USER_AGENT}, timeout=30
            )
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                return [data]
            return []
        except Exception as err:
            logger.warning("Error fetching %s: %s", url, err)
            return None

    def _parse_csv_json(self, url: str) -> List[dict]:
        """Parse CSV-in-JSON (array of arrays with header row) into list of dicts."""
        result = self._get_json(url)
        if not result or len(result) < 2:
            return []
        headers = result[0]
        rows = []
        for row in result[1:]:
            if isinstance(row, list) and len(row) == len(headers):
                rows.append(dict(zip(headers, row)))
        return rows

    # ---------------------------------------------------------- poll methods

    def poll_alerts(self) -> List[dict]:
        """Return current SWPC space weather alerts."""
        result = self._get_json(self.ALERTS_URL)
        return result if result is not None else []

    def poll_k_index(self) -> List[dict]:
        """Return planetary K-index data rows."""
        result = self._get_json(self.K_INDEX_URL)
        if result is None:
            return []
        return [row for row in result if isinstance(row, dict)]

    def poll_solar_wind(self) -> List[dict]:
        """Return a single merged solar-wind summary dict."""
        try:
            speed_response = requests.get(
                self.SOLAR_WIND_SPEED_URL, headers={"User-Agent": USER_AGENT}, timeout=30
            )
            speed_response.raise_for_status()
            speed_data = speed_response.json()
            mag_response = requests.get(
                self.SOLAR_WIND_MAG_FIELD_URL, headers={"User-Agent": USER_AGENT}, timeout=30
            )
            mag_response.raise_for_status()
            mag_data = mag_response.json()
            if isinstance(speed_data, list) and speed_data:
                speed_data = speed_data[0]
            if isinstance(mag_data, list) and mag_data:
                mag_data = mag_data[0]
            timestamp = (
                speed_data.get("time_tag")
                or speed_data.get("TimeStamp")
                or mag_data.get("time_tag")
                or mag_data.get("TimeStamp")
                or ""
            )
            wind_speed = speed_data.get("proton_speed") or speed_data.get("WindSpeed") or 0
            bt = mag_data.get("bt") or mag_data.get("Bt") or 0
            bz = mag_data.get("bz_gsm") or mag_data.get("Bz") or 0
            return [{
                "timestamp": timestamp,
                "wind_speed": float(wind_speed) if wind_speed else 0.0,
                "bt": float(bt) if bt else 0.0,
                "bz": float(bz) if bz else 0.0,
            }]
        except Exception as err:
            logger.warning("Error fetching solar wind summary: %s", err)
            return []

    def poll_plasma(self) -> List[dict]:
        """Return solar-wind plasma rows (7-day)."""
        return self._parse_csv_json(self.PLASMA_URL)

    def poll_mag(self) -> List[dict]:
        """Return solar-wind magnetic field rows (7-day)."""
        return self._parse_csv_json(self.MAG_URL)

    def poll_goes_xrays(self) -> List[dict]:
        """Return GOES primary X-ray flux rows (7-day)."""
        result = self._get_json(self.XRAYS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_goes_protons(self) -> List[dict]:
        """Return GOES primary integral proton flux rows (7-day)."""
        result = self._get_json(self.PROTONS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_goes_electrons(self) -> List[dict]:
        """Return GOES primary integral electron flux rows (3-day)."""
        result = self._get_json(self.ELECTRONS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_goes_magnetometers(self) -> List[dict]:
        """Return GOES primary magnetometer rows (7-day)."""
        result = self._get_json(self.MAGNETOMETERS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_xray_flares(self) -> List[dict]:
        """Return GOES primary X-ray flare rows (7-day)."""
        result = self._get_json(self.FLARES_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    # -------------------------------------------------------- type helpers

    def _safe_float(self, val) -> Optional[float]:
        """Convert val to float, returning None on failure."""
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    def _safe_int(self, val) -> Optional[int]:
        """Convert val to int, returning None on failure."""
        if val is None:
            return None
        try:
            return int(val)
        except (ValueError, TypeError):
            return None
