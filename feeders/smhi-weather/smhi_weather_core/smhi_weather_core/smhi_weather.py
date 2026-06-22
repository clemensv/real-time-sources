"""Transport-agnostic acquisition layer for the SMHI weather bridge."""

from __future__ import annotations

import json
import logging
import os
import typing
from datetime import datetime, timezone

import requests

from smhi_weather_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

SMHI_BASE_URL = "https://opendata-download-metobs.smhi.se/api/version/1.0"

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-smhi-weather/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

PARAM_AIR_TEMP = 1
PARAM_WIND_GUST = 21
PARAM_DEW_POINT = 39
PARAM_PRESSURE = 9
PARAM_HUMIDITY = 6
PARAM_PRECIP = 7
PARAM_WIND_DIR = 3
PARAM_WIND_SPEED = 4
PARAM_MAX_WIND_SPEED = 25
PARAM_VISIBILITY = 12
PARAM_CLOUD_COVER = 16
PARAM_PRESENT_WX = 13
PARAM_SUNSHINE = 10
PARAM_IRRADIANCE = 11
PARAM_PRECIP_INTENSITY = 38

ALL_PARAMS = [
    PARAM_AIR_TEMP, PARAM_WIND_GUST, PARAM_DEW_POINT, PARAM_PRESSURE,
    PARAM_HUMIDITY, PARAM_PRECIP, PARAM_WIND_DIR, PARAM_WIND_SPEED,
    PARAM_MAX_WIND_SPEED, PARAM_VISIBILITY, PARAM_CLOUD_COVER,
    PARAM_PRESENT_WX, PARAM_SUNSHINE, PARAM_IRRADIANCE, PARAM_PRECIP_INTENSITY,
]


def _to_int(v: typing.Any) -> typing.Optional[int]:
    if v is None:
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


class SMHIWeatherAPI:
    """Client for the SMHI open data meteorological observation API."""

    def __init__(self, base_url: str = SMHI_BASE_URL, polling_interval: int = 900):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def get_stations_for_parameter(self, parameter_id: int) -> list[dict]:
        """Fetch the station list for a given parameter."""
        url = f"{self.base_url}/parameter/{parameter_id}.json"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json().get("station", [])

    def get_bulk_latest(self, parameter_id: int) -> dict:
        """Fetch bulk latest-hour data for all stations for a given parameter."""
        url = f"{self.base_url}/parameter/{parameter_id}/station-set/all/period/latest-hour/data.json"
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def extract_lan(station_data: dict) -> typing.Optional[str]:
        """Extract the Swedish county code/name from a station payload."""
        for key in ("lan", "county", "countyCode", "countyName"):
            value = station_data.get(key)
            if value:
                return str(value)
        return None

    @staticmethod
    def parse_station(station_data: dict) -> Station:
        """Parse a station entry from the parameter station list."""
        summary = station_data.get("summary", "")
        lat = 0.0
        lon = 0.0
        parts = summary.split()
        for i, p in enumerate(parts):
            if p == "Latitud:" and i + 1 < len(parts):
                try:
                    lat = float(parts[i + 1])
                except ValueError:
                    pass
            elif p == "Longitud:" and i + 1 < len(parts):
                try:
                    lon = float(parts[i + 1])
                except ValueError:
                    pass

        title = station_data.get("title", "")
        name = title.split(" - ", 1)[-1] if " - " in title else title

        return Station(
            station_id=str(station_data["key"]),
            name=name,
            owner=station_data.get("owner", ""),
            owner_category=station_data.get("ownerCategory", ""),
            measuring_stations=station_data.get("measuringStations", ""),
            height=float(station_data.get("height", 0.0)),
            latitude=lat,
            longitude=lon,
            lan=SMHIWeatherAPI.extract_lan(station_data),
        )

    @staticmethod
    def parse_bulk_observations(bulk_data: dict) -> dict[str, dict]:
        """Parse bulk latest-hour data into a dict of station_id -> partial observation dict."""
        result: dict[str, dict] = {}
        for station_data in bulk_data.get("station", []):
            values = station_data.get("value", [])
            if not values:
                continue
            latest = values[-1]
            val = latest.get("value")
            if val is None:
                continue
            sid = str(station_data["key"])
            epoch_ms = latest["date"]
            ts = datetime.fromtimestamp(epoch_ms / 1000.0, tz=timezone.utc)
            quality = latest.get("quality", "")
            result[sid] = {
                "station_id": sid,
                "station_name": station_data.get("name", ""),
                "observation_time": ts,
                "quality": quality,
                "value": float(val),
                "lan": SMHIWeatherAPI.extract_lan(station_data),
            }
        return result


def merge_observations(
    param_data: dict[int, dict[str, dict]],
    station_lan_by_id: typing.Optional[dict[str, typing.Optional[str]]] = None,
) -> list[WeatherObservation]:
    """Merge per-parameter observations into WeatherObservation objects per station."""
    station_lan_by_id = station_lan_by_id or {}
    all_stations: set[str] = set()
    for pdata in param_data.values():
        all_stations.update(pdata.keys())

    observations = []
    for sid in all_stations:
        temp_data = param_data.get(PARAM_AIR_TEMP, {}).get(sid)
        if not temp_data:
            for pdata in param_data.values():
                if sid in pdata:
                    temp_data = pdata[sid]
                    break
        if not temp_data:
            continue

        obs = WeatherObservation(
            station_id=sid,
            station_name=temp_data.get("station_name", ""),
            observation_time=temp_data.get("observation_time", ""),
            air_temperature=param_data.get(PARAM_AIR_TEMP, {}).get(sid, {}).get("value"),
            wind_gust=param_data.get(PARAM_WIND_GUST, {}).get(sid, {}).get("value"),
            dew_point=param_data.get(PARAM_DEW_POINT, {}).get(sid, {}).get("value"),
            air_pressure=param_data.get(PARAM_PRESSURE, {}).get(sid, {}).get("value"),
            relative_humidity=_to_int(param_data.get(PARAM_HUMIDITY, {}).get(sid, {}).get("value")),
            precipitation_last_hour=param_data.get(PARAM_PRECIP, {}).get(sid, {}).get("value"),
            wind_direction=param_data.get(PARAM_WIND_DIR, {}).get(sid, {}).get("value"),
            wind_speed=param_data.get(PARAM_WIND_SPEED, {}).get(sid, {}).get("value"),
            max_wind_speed=param_data.get(PARAM_MAX_WIND_SPEED, {}).get(sid, {}).get("value"),
            visibility=param_data.get(PARAM_VISIBILITY, {}).get(sid, {}).get("value"),
            total_cloud_cover=_to_int(param_data.get(PARAM_CLOUD_COVER, {}).get(sid, {}).get("value")),
            present_weather=_to_int(param_data.get(PARAM_PRESENT_WX, {}).get(sid, {}).get("value")),
            sunshine_duration=param_data.get(PARAM_SUNSHINE, {}).get(sid, {}).get("value"),
            global_irradiance=param_data.get(PARAM_IRRADIANCE, {}).get(sid, {}).get("value"),
            precipitation_intensity=param_data.get(PARAM_PRECIP_INTENSITY, {}).get(sid, {}).get("value"),
            quality=temp_data.get("quality", ""),
            lan=temp_data.get("lan") or station_lan_by_id.get(sid),
        )
        observations.append(obs)
    return observations


def _load_state(state_file: str) -> dict:
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {k: data[k] for k in keys[-50000:]}
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


def observation_lan_segment(obs: WeatherObservation) -> str:
    """Return a safe topic/route segment for the observation's county (lan)."""
    raw = (str(obs.lan) if obs.lan is not None else "unknown").strip() or "unknown"
    for ch in ("/", "+", "#", " "):
        raw = raw.replace(ch, "-")
    return raw or "unknown"
