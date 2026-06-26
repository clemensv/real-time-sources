"""Transport-agnostic acquisition and state handling for Singapore NEA."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests

logger = logging.getLogger(__name__)

NEA_BASE_URL = "https://api.data.gov.sg/v1/environment"
AIR_QUALITY_REFERENCE_REFRESH_INTERVAL = 24 * 60 * 60

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-singapore-nea/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

ENDPOINTS = [
    "air-temperature",
    "rainfall",
    "relative-humidity",
    "wind-speed",
    "wind-direction",
]

FIELD_MAP = {
    "air-temperature": "air_temperature",
    "rainfall": "rainfall",
    "relative-humidity": "relative_humidity",
    "wind-speed": "wind_speed",
    "wind-direction": "wind_direction",
}


# ---------------------------------------------------------------------------
# Transport-neutral data classes
# ---------------------------------------------------------------------------

@dataclass
class StationData:
    """Transport-neutral representation of an NEA weather station."""
    station_id: str
    device_id: str
    name: str
    latitude: float
    longitude: float
    data_types: str


@dataclass
class WeatherObservationData:
    """Transport-neutral representation of an NEA weather observation."""
    station_id: str
    station_name: str
    observation_time: datetime
    air_temperature: Optional[float]
    rainfall: Optional[float]
    relative_humidity: Optional[float]
    wind_speed: Optional[float]
    wind_direction: Optional[float]


@dataclass
class RegionData:
    """Transport-neutral representation of an NEA air quality region."""
    region: str
    latitude: float
    longitude: float


@dataclass
class PSIReadingData:
    """Transport-neutral representation of an NEA PSI reading."""
    region: str
    timestamp: datetime
    update_timestamp: datetime
    psi_twenty_four_hourly: Optional[int]
    o3_sub_index: Optional[int]
    pm10_sub_index: Optional[int]
    pm10_twenty_four_hourly: Optional[int]
    pm25_sub_index: Optional[int]
    pm25_twenty_four_hourly: Optional[int]
    co_sub_index: Optional[int]
    co_eight_hour_max: Optional[int]
    so2_sub_index: Optional[int]
    so2_twenty_four_hourly: Optional[int]
    no2_one_hour_max: Optional[int]
    o3_eight_hour_max: Optional[int]


@dataclass
class PM25ReadingData:
    """Transport-neutral representation of an NEA PM2.5 reading."""
    region: str
    timestamp: datetime
    update_timestamp: datetime
    pm25_one_hourly: Optional[int]


# ---------------------------------------------------------------------------
# Weather API client
# ---------------------------------------------------------------------------

class NEAWeatherAPI:
    """Client for the Singapore NEA weather API on data.gov.sg."""

    def __init__(self, base_url: str = NEA_BASE_URL, polling_interval: int = 300):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def get_endpoint(self, endpoint: str) -> dict:
        """Fetch a single environment endpoint."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_all_stations(self) -> dict[str, StationData]:
        """Collect station metadata from all endpoints and merge."""
        station_types: dict[str, set[str]] = {}
        station_info: dict[str, dict] = {}

        for endpoint in ENDPOINTS:
            try:
                data = self.get_endpoint(endpoint)
                field = FIELD_MAP[endpoint]
                for sdata in data.get("metadata", {}).get("stations", []):
                    sid = sdata["id"]
                    if sid not in station_types:
                        station_types[sid] = set()
                        station_info[sid] = sdata
                    station_types[sid].add(field)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.warning("Failed to fetch stations from %s: %s", endpoint, exc)

        stations: dict[str, StationData] = {}
        for sid, info in station_info.items():
            loc = info.get("location", {})
            stations[sid] = StationData(
                station_id=sid,
                device_id=info.get("device_id", sid),
                name=info.get("name", ""),
                latitude=float(loc.get("latitude", 0.0)),
                longitude=float(loc.get("longitude", 0.0)),
                data_types=",".join(sorted(station_types.get(sid, set()))),
            )
        return stations

    @staticmethod
    def parse_readings(data: dict) -> tuple[str, dict[str, float]]:
        """Parse a single endpoint response into station/value pairs."""
        items = data.get("items", [])
        if not items:
            return "", {}
        item = items[0]
        timestamp = item.get("timestamp", "")
        readings: dict[str, float] = {}
        for reading in item.get("readings", []):
            readings[reading["station_id"]] = float(reading["value"])
        return timestamp, readings


def merge_observations(
    api: NEAWeatherAPI,
) -> tuple[dict[str, StationData], list[WeatherObservationData]]:
    """Fetch all weather endpoints and merge per-station observations."""
    stations = api.get_all_stations()
    param_data: dict[str, dict[str, float]] = {}
    latest_ts = ""

    for endpoint in ENDPOINTS:
        try:
            data = api.get_endpoint(endpoint)
            timestamp, readings = api.parse_readings(data)
            param_data[FIELD_MAP[endpoint]] = readings
            if timestamp and timestamp > latest_ts:
                latest_ts = timestamp
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.warning("Failed to fetch %s: %s", endpoint, exc)

    try:
        obs_time = datetime.fromisoformat(latest_ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        obs_time = datetime.now(timezone.utc)

    name_map = {sid: station.name for sid, station in stations.items()}
    all_station_ids: set[str] = set()
    for readings in param_data.values():
        all_station_ids.update(readings.keys())

    observations: list[WeatherObservationData] = []
    for station_id in sorted(all_station_ids):
        observations.append(
            WeatherObservationData(
                station_id=station_id,
                station_name=name_map.get(station_id, station_id),
                observation_time=obs_time,
                air_temperature=param_data.get("air_temperature", {}).get(station_id),
                rainfall=param_data.get("rainfall", {}).get(station_id),
                relative_humidity=param_data.get("relative_humidity", {}).get(station_id),
                wind_speed=param_data.get("wind_speed", {}).get(station_id),
                wind_direction=param_data.get("wind_direction", {}).get(station_id),
            )
        )
    return stations, observations


# ---------------------------------------------------------------------------
# Air quality API client
# ---------------------------------------------------------------------------

class NEAAirQualityAPI:
    """Client for Singapore NEA PSI and PM2.5 regional endpoints."""

    def __init__(
        self,
        base_url: str = NEA_BASE_URL,
        polling_interval: int = 3600,
    ):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def _get_endpoint(self, endpoint: str) -> dict:
        response = self.session.get(f"{self.base_url}/{endpoint}", timeout=30)
        response.raise_for_status()
        return response.json()

    def get_psi(self) -> dict:
        """Fetch the PSI endpoint."""
        return self._get_endpoint("psi")

    def get_pm25(self) -> dict:
        """Fetch the PM2.5 endpoint."""
        return self._get_endpoint("pm25")

    def get_regions(self) -> dict[str, RegionData]:
        """Fetch air quality region metadata."""
        data = self.get_psi()
        return self.extract_regions(data)

    @staticmethod
    def extract_regions(data: dict) -> dict[str, RegionData]:
        """Extract region metadata from a PSI or PM2.5 response."""
        regions: dict[str, RegionData] = {}
        for entry in data.get("region_metadata", []):
            label_location = entry.get("label_location", {})
            region_name = entry.get("name")
            if not region_name:
                continue
            regions[region_name] = RegionData(
                region=region_name,
                latitude=float(label_location.get("latitude", 0.0)),
                longitude=float(label_location.get("longitude", 0.0)),
            )
        return regions


def _parse_iso_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def _reading_value(region_readings: dict, region: str) -> Optional[int]:
    value = region_readings.get(region)
    return int(value) if value is not None else None


def fetch_psi_readings(
    api: NEAAirQualityAPI,
    previous_psi: dict,
) -> list[PSIReadingData]:
    """Fetch PSI readings, deduplicated by region and timestamp."""
    data = api.get_psi()
    items = data.get("items", [])
    if not items:
        return []

    item = items[0]
    timestamp = _parse_iso_datetime(item.get("timestamp"))
    update_timestamp = _parse_iso_datetime(item.get("update_timestamp"))
    readings = item.get("readings", {})
    regions = NEAAirQualityAPI.extract_regions(data)
    result: list[PSIReadingData] = []

    for region_name in sorted(regions.keys()):
        reading_key = f"{region_name}:{timestamp.isoformat()}"
        if reading_key in previous_psi:
            continue
        result.append(
            PSIReadingData(
                region=region_name,
                timestamp=timestamp,
                update_timestamp=update_timestamp,
                psi_twenty_four_hourly=_reading_value(
                    readings.get("psi_twenty_four_hourly", {}), region_name
                ),
                o3_sub_index=_reading_value(readings.get("o3_sub_index", {}), region_name),
                pm10_sub_index=_reading_value(readings.get("pm10_sub_index", {}), region_name),
                pm10_twenty_four_hourly=_reading_value(
                    readings.get("pm10_twenty_four_hourly", {}), region_name
                ),
                pm25_sub_index=_reading_value(readings.get("pm25_sub_index", {}), region_name),
                pm25_twenty_four_hourly=_reading_value(
                    readings.get("pm25_twenty_four_hourly", {}), region_name
                ),
                co_sub_index=_reading_value(readings.get("co_sub_index", {}), region_name),
                co_eight_hour_max=_reading_value(
                    readings.get("co_eight_hour_max", {}), region_name
                ),
                so2_sub_index=_reading_value(readings.get("so2_sub_index", {}), region_name),
                so2_twenty_four_hourly=_reading_value(
                    readings.get("so2_twenty_four_hourly", {}), region_name
                ),
                no2_one_hour_max=_reading_value(readings.get("no2_one_hour_max", {}), region_name),
                o3_eight_hour_max=_reading_value(
                    readings.get("o3_eight_hour_max", {}), region_name
                ),
            )
        )
        previous_psi[reading_key] = timestamp.isoformat()

    return result


def fetch_pm25_readings(
    api: NEAAirQualityAPI,
    previous_pm25: dict,
) -> list[PM25ReadingData]:
    """Fetch PM2.5 readings, deduplicated by region and timestamp."""
    data = api.get_pm25()
    items = data.get("items", [])
    if not items:
        return []

    item = items[0]
    timestamp = _parse_iso_datetime(item.get("timestamp"))
    update_timestamp = _parse_iso_datetime(item.get("update_timestamp"))
    readings = item.get("readings", {}).get("pm25_one_hourly", {})
    regions = NEAAirQualityAPI.extract_regions(data)
    result: list[PM25ReadingData] = []

    for region_name in sorted(regions.keys()):
        reading_key = f"{region_name}:{timestamp.isoformat()}"
        if reading_key in previous_pm25:
            continue
        result.append(
            PM25ReadingData(
                region=region_name,
                timestamp=timestamp,
                update_timestamp=update_timestamp,
                pm25_one_hourly=_reading_value(readings, region_name),
            )
        )
        previous_pm25[reading_key] = timestamp.isoformat()

    return result


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state(state_file: str) -> dict:
    """Load persisted dedupe state from disk."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as fh:
                return json.load(fh)
    except Exception as exc:  # pragma: no cover - defensive logging
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def save_state(state_file: str, data: dict) -> None:
    """Persist dedupe state to disk."""
    if not state_file:
        return
    try:
        if "weather" in data or "air_quality" in data:
            weather_state = data.get("weather", {})
            air_quality_state = data.get("air_quality", {})
            data = {
                "weather": _truncate_state_entries(weather_state),
                "air_quality": {
                    "psi": _truncate_state_entries(air_quality_state.get("psi", {})),
                    "pm25": _truncate_state_entries(air_quality_state.get("pm25", {})),
                },
            }
        else:
            data = _truncate_state_entries(data)
        with open(state_file, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except Exception as exc:  # pragma: no cover - defensive logging
        logging.warning("Could not save state to %s: %s", state_file, exc)


def _truncate_state_entries(data: dict) -> dict:
    """Keep persisted dedupe maps from growing without bound."""
    if not isinstance(data, dict) or len(data) <= 100000:
        return data
    keys = list(data.keys())
    return {key: data[key] for key in keys[-50000:]}


def split_state(state: dict) -> tuple[dict, dict, dict]:
    """Split persisted state into weather, PSI, and PM2.5 dedupe maps."""
    if "weather" in state or "air_quality" in state:
        weather_state = state.get("weather", {})
        air_quality_state = state.get("air_quality", {})
        return (
            weather_state,
            air_quality_state.get("psi", {}),
            air_quality_state.get("pm25", {}),
        )
    return state, {}, {}


def compose_state(weather_state: dict, psi_state: dict, pm25_state: dict) -> dict:
    """Compose the persisted state document."""
    return {
        "weather": weather_state,
        "air_quality": {
            "psi": psi_state,
            "pm25": pm25_state,
        },
    }


__all__ = [
    "NEA_BASE_URL",
    "AIR_QUALITY_REFERENCE_REFRESH_INTERVAL",
    "USER_AGENT",
    "ENDPOINTS",
    "FIELD_MAP",
    "StationData",
    "WeatherObservationData",
    "RegionData",
    "PSIReadingData",
    "PM25ReadingData",
    "NEAWeatherAPI",
    "NEAAirQualityAPI",
    "merge_observations",
    "fetch_psi_readings",
    "fetch_pm25_readings",
    "load_state",
    "save_state",
    "split_state",
    "compose_state",
]
