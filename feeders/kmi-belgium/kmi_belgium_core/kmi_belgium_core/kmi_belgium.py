"""KMI Belgium Weather Observation Bridge - fetches automatic weather station observations from the Royal Meteorological Institute of Belgium."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

import requests

from kmi_belgium_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

KMI_AWS_WFS_URL = "https://opendata.meteo.be/service/aws/ows"
FEATURE_TYPE = "aws:aws_10min"
LATEST_FETCH_COUNT = 200
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-kmi-belgium/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)
OBSERVATION_FIELDS = (
    "precip_quantity",
    "temp_dry_shelter_avg",
    "temp_grass_pt100_avg",
    "temp_soil_avg",
    "temp_soil_avg_5cm",
    "temp_soil_avg_10cm",
    "temp_soil_avg_20cm",
    "temp_soil_avg_50cm",
    "wind_speed_10m",
    "wind_speed_avg_30m",
    "wind_direction",
    "wind_gusts_speed",
    "humidity_rel_shelter_avg",
    "pressure",
    "sun_duration",
    "short_wave_from_sky_avg",
    "sun_int_avg",
)


class KMIBelgiumAPI:
    """Client for the KMI/RMI automatic weather station WFS API."""

    def __init__(self, base_url: str = KMI_AWS_WFS_URL, polling_interval: int = 600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def get_observations(self, last_timestamp: str | None = None, count: int | None = None) -> list[dict[str, Any]]:
        """Fetch aws:aws_10min observations as GeoJSON features."""
        params: dict[str, str] = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeNames": FEATURE_TYPE,
            "outputFormat": "application/json",
            "sortBy": "timestamp D",
        }
        if count is not None:
            params["count"] = str(count)
        if last_timestamp:
            params["CQL_FILTER"] = f"timestamp >= '{last_timestamp}'"
        response = self.session.get(self.base_url, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()
        return payload.get("features", [])

    def get_latest_observations(self, count: int = LATEST_FETCH_COUNT) -> list[dict[str, Any]]:
        """Fetch the latest observation slice and keep only the newest timestamp batch."""
        features = self.get_observations(count=count)
        if not features:
            return []
        latest_timestamp = features[0].get("properties", {}).get("timestamp")
        if not latest_timestamp:
            return features
        return [
            feature
            for feature in features
            if feature.get("properties", {}).get("timestamp") == latest_timestamp
        ]

    @staticmethod
    def parse_station(feature: dict[str, Any]) -> Station:
        """Parse a GeoJSON feature into a Station event payload."""
        properties = feature.get("properties", {})
        longitude, latitude = KMIBelgiumAPI._coordinates(feature)
        station = Station(
            station_code=str(properties["code"]),
            latitude=latitude,
            longitude=longitude,
            region=None,
        )
        return station

    @staticmethod
    def parse_observation(feature: dict[str, Any]) -> WeatherObservation:
        """Parse a GeoJSON feature into a WeatherObservation event payload."""
        properties = feature.get("properties", {})
        observation = {
            "station_code": str(properties["code"]),
            "observation_time": _parse_timestamp(properties["timestamp"]),
        }
        for field_name in OBSERVATION_FIELDS:
            observation[field_name] = _to_float(properties.get(field_name))
        obs = WeatherObservation(**observation)  # type: ignore[arg-type]
        obs.region = None
        return obs

    @staticmethod
    def _coordinates(feature: dict[str, Any]) -> tuple[float, float]:
        geometry = feature.get("geometry") or {}
        coordinates = geometry.get("coordinates") or []
        if len(coordinates) < 2:
            raise ValueError("GeoJSON feature is missing [longitude, latitude] coordinates")
        return float(coordinates[0]), float(coordinates[1])


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None



def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)



def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

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



def extract_stations(features: list[dict[str, Any]]) -> list[Station]:
    """Extract unique stations from observation features."""
    stations: dict[str, Station] = {}
    for feature in features:
        station = KMIBelgiumAPI.parse_station(feature)
        stations.setdefault(station.station_code, station)
    return sorted(stations.values(), key=lambda station: station.station_code)
