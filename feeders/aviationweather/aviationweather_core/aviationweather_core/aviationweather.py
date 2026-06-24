"""Transport-neutral acquisition and state handling for AviationWeather.gov."""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

import requests
from aviationweather_producer_data import Metar, Sigmet, Station

logger = logging.getLogger(__name__)

API_BASE = "https://aviationweather.gov/api/data"
DEFAULT_STATIONS = "KJFK,KLAX,KORD,KATL,EGLL,LFPG,EDDF,RJTT,YSSY,ZBAA"
METAR_POLL_INTERVAL = 60
SIGMET_POLL_INTERVAL = 120
STATION_REFRESH_HOURS = 24

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-aviationweather/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

__all__ = [
    "API_BASE",
    "DEFAULT_STATIONS",
    "METAR_POLL_INTERVAL",
    "SIGMET_POLL_INTERVAL",
    "STATION_REFRESH_HOURS",
    "USER_AGENT",
    "AviationWeatherPoller",
]


class AviationWeatherPoller:
    """Transport-neutral poller for AviationWeather.gov API."""

    def __init__(
        self,
        last_polled_file: str,
        station_ids: str = DEFAULT_STATIONS,
        metar_poll_interval: int = METAR_POLL_INTERVAL,
        sigmet_poll_interval: int = SIGMET_POLL_INTERVAL,
    ):
        self.last_polled_file = last_polled_file
        self.station_ids = station_ids
        self.metar_poll_interval = metar_poll_interval
        self.sigmet_poll_interval = sigmet_poll_interval

    # ------------------------------------------------------------------
    # Type coercion helpers
    # ------------------------------------------------------------------

    @staticmethod
    def epoch_to_iso(epoch_val) -> Optional[str]:
        """Convert a Unix epoch timestamp to an ISO 8601 UTC string."""
        if epoch_val is None:
            return None
        try:
            dt = datetime.fromtimestamp(int(epoch_val), tz=timezone.utc)
            return dt.isoformat()
        except (ValueError, TypeError, OSError):
            return None

    @staticmethod
    def safe_int(value) -> Optional[int]:
        """Safely convert a value to int, returning None on failure."""
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def safe_float(value) -> Optional[float]:
        """Safely convert a value to float, returning None on failure."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    # ------------------------------------------------------------------
    # HTTP fetch helpers
    # ------------------------------------------------------------------

    @staticmethod
    def fetch_metar_json(station_ids: str) -> List[dict]:
        """Fetch METAR observations from the AviationWeather.gov API."""
        try:
            url = f"{API_BASE}/metar?ids={station_ids}&format=json"
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except Exception as err:
            logger.warning("Error fetching METARs: %s", err)
            return []

    @staticmethod
    def fetch_station_json(station_ids: str) -> List[dict]:
        """Fetch station metadata from the AviationWeather.gov API."""
        try:
            url = f"{API_BASE}/stationinfo?ids={station_ids}&format=json"
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except Exception as err:
            logger.warning("Error fetching station info: %s", err)
            return []

    @staticmethod
    def fetch_airsigmet_json() -> List[dict]:
        """Fetch US domestic SIGMETs (AIRMETs/SIGMETs) from the API."""
        try:
            url = f"{API_BASE}/airsigmet?format=json"
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except Exception as err:
            logger.warning("Error fetching US SIGMETs: %s", err)
            return []

    @staticmethod
    def fetch_isigmet_json() -> List[dict]:
        """Fetch international SIGMETs from the API."""
        try:
            url = f"{API_BASE}/isigmet?format=json"
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except Exception as err:
            logger.warning("Error fetching international SIGMETs: %s", err)
            return []

    # ------------------------------------------------------------------
    # Parsers
    # ------------------------------------------------------------------

    @classmethod
    def parse_station(cls, raw: dict) -> Optional[Station]:
        """Parse a station info API response dict into a Station dataclass."""
        icao_id = raw.get("icaoId")
        if not icao_id:
            return None
        lat = cls.safe_float(raw.get("lat"))
        lon = cls.safe_float(raw.get("lon"))
        if lat is None or lon is None:
            return None
        name = raw.get("site") or raw.get("name") or icao_id
        site_type_list = raw.get("siteType")
        site_type = ",".join(site_type_list) if isinstance(site_type_list, list) else None
        return Station(
            icao_id=icao_id,
            iata_id=raw.get("iataId"),
            faa_id=raw.get("faaId"),
            wmo_id=raw.get("wmoId"),
            name=name,
            latitude=lat,
            longitude=lon,
            elevation=cls.safe_float(raw.get("elev")),
            state=raw.get("state"),
            country=raw.get("country"),
            site_type=site_type,
        )

    @classmethod
    def parse_metar(cls, raw: dict) -> Optional[Metar]:
        """Parse a METAR API response dict into a Metar dataclass."""
        icao_id = raw.get("icaoId")
        if not icao_id:
            return None
        raw_ob = raw.get("rawOb")
        if not raw_ob:
            return None
        obs_time = cls.epoch_to_iso(raw.get("obsTime"))
        if not obs_time:
            return None
        report_time = raw.get("reportTime")
        if isinstance(report_time, str):
            try:
                datetime.fromisoformat(report_time.replace("Z", "+00:00"))
            except ValueError:
                report_time = None
        clouds_raw = raw.get("clouds")
        clouds_str = json.dumps(clouds_raw) if clouds_raw is not None else None
        visib = raw.get("visib")
        return Metar(
            icao_id=icao_id,
            obs_time=obs_time,  # type: ignore[arg-type]
            report_time=report_time,  # type: ignore[arg-type]
            temp=cls.safe_float(raw.get("temp")),
            dewp=cls.safe_float(raw.get("dewp")),
            wdir=cls.safe_int(raw.get("wdir")),
            wspd=cls.safe_int(raw.get("wspd")),
            wgst=cls.safe_int(raw.get("wgst")),
            visib=str(visib) if visib is not None else None,
            altim=cls.safe_float(raw.get("altim")),
            slp=cls.safe_float(raw.get("slp")),
            qc_field=cls.safe_int(raw.get("qcField")),
            wx_string=raw.get("wxString"),
            metar_type=raw.get("metarType"),
            raw_ob=raw_ob,
            latitude=cls.safe_float(raw.get("lat")),
            longitude=cls.safe_float(raw.get("lon")),
            elevation=cls.safe_float(raw.get("elev")),
            flt_cat=raw.get("fltCat"),
            clouds=clouds_str,
            name=raw.get("name"),
        )

    @classmethod
    def parse_us_sigmet(cls, raw: dict) -> Optional[Sigmet]:
        """Parse a US domestic SIGMET API response dict into a Sigmet dataclass."""
        icao_id = raw.get("icaoId")
        series_id = raw.get("seriesId")
        if not icao_id or not series_id:
            return None
        valid_from = cls.epoch_to_iso(raw.get("validTimeFrom"))
        valid_to = cls.epoch_to_iso(raw.get("validTimeTo"))
        if not valid_from or not valid_to:
            return None
        coords_raw = raw.get("coords")
        movement_dir = raw.get("movementDir")
        movement_spd = raw.get("movementSpd")
        return Sigmet(
            icao_id=icao_id,
            series_id=series_id,
            valid_time_from=valid_from,  # type: ignore[arg-type]
            valid_time_to=valid_to,  # type: ignore[arg-type]
            hazard=raw.get("hazard"),
            qualifier=None,
            sigmet_type=raw.get("airSigmetType", "SIGMET"),
            altitude_hi=cls.safe_int(raw.get("altitudeHi1")),
            altitude_low=cls.safe_int(raw.get("altitudeLow1")),
            movement_dir=str(movement_dir) if movement_dir is not None else None,
            movement_spd=str(movement_spd) if movement_spd is not None else None,
            severity=cls.safe_int(raw.get("severity")),  # type: ignore[arg-type]
            raw_sigmet=raw.get("rawAirSigmet"),
            coords=json.dumps(coords_raw) if coords_raw is not None else None,
            sigmet_id=series_id.lower(),
            region=icao_id.lower(),
        )

    @classmethod
    def parse_intl_sigmet(cls, raw: dict) -> Optional[Sigmet]:
        """Parse an international SIGMET API response dict into a Sigmet dataclass."""
        icao_id = raw.get("icaoId")
        series_id = raw.get("seriesId")
        if not icao_id or not series_id:
            return None
        valid_from = cls.epoch_to_iso(raw.get("validTimeFrom"))
        valid_to = cls.epoch_to_iso(raw.get("validTimeTo"))
        if not valid_from or not valid_to:
            return None
        coords_raw = raw.get("coords")
        return Sigmet(
            icao_id=icao_id,
            series_id=series_id,
            valid_time_from=valid_from,  # type: ignore[arg-type]
            valid_time_to=valid_to,  # type: ignore[arg-type]
            hazard=raw.get("hazard"),
            qualifier=raw.get("qualifier"),
            sigmet_type="ISIGMET",
            altitude_hi=cls.safe_int(raw.get("top")),
            altitude_low=cls.safe_int(raw.get("base")),
            movement_dir=raw.get("dir"),
            movement_spd=raw.get("spd"),
            severity=None,
            raw_sigmet=raw.get("rawSigmet"),
            coords=json.dumps(coords_raw) if coords_raw is not None else None,
            sigmet_id=series_id.lower(),
            region=icao_id.lower(),
        )

    @staticmethod
    def sigmet_dedup_key(sigmet: Sigmet) -> str:
        """Generate a deduplication key for a SIGMET."""
        return f"{sigmet.icao_id}:{sigmet.series_id}:{sigmet.valid_time_from}:{sigmet.valid_time_to}"

    # ------------------------------------------------------------------
    # State persistence
    # ------------------------------------------------------------------

    def load_state(self) -> Dict:
        """Load the persisted state from disk."""
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    if isinstance(state, dict):
                        return {
                            "metar_timestamps": state.get("metar_timestamps", {}),
                            "sigmet_keys": state.get("sigmet_keys", []),
                        }
        except Exception:
            pass
        return {"metar_timestamps": {}, "sigmet_keys": []}

    def save_state(self, state: Dict) -> None:
        """Save the current state to disk for deduplication across restarts."""
        try:
            dir_name = os.path.dirname(self.last_polled_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(self.last_polled_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.warning("Error saving state: %s", e)
