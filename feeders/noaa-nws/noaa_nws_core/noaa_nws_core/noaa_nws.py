"""Transport-neutral acquisition and state handling for NOAA NWS."""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

import requests

USER_AGENT: str = os.environ.get("USER_AGENT") or (
    "real-time-sources-noaa-nws/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

ALERTS_URL = "https://api.weather.gov/alerts/active"
ZONES_URL = "https://api.weather.gov/zones?type=forecast"
STATIONS_URL = "https://api.weather.gov/stations"
HEADERS: Dict[str, str] = {
    "User-Agent": USER_AGENT,
    "Accept": "application/geo+json",
}
POLL_INTERVAL_SECONDS = 60
OBSERVATION_INTERVAL_SECONDS = 300


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs-style connection string and extract Kafka parameters.

    Args:
        connection_string: The connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, sasl.username, sasl.password.
    """
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=")[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


class NWSFetcher:
    """
    Transport-neutral fetcher for NOAA NWS alerts, zones, stations, and observations.
    No Kafka, MQTT, or AMQP dependencies. Returns plain dicts suitable for
    constructing any transport's producer data classes.
    """

    def __init__(self, last_polled_file: str) -> None:
        self.last_polled_file = last_polled_file
        self.station_ids: List[str] = []
        self.station_context: Dict[str, Dict[str, Optional[str]]] = {}

    # ------------------------------------------------------------------
    # State persistence
    # ------------------------------------------------------------------

    def load_seen_alerts(self) -> Dict:
        """Load the set of previously seen alert IDs from the state file."""
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {"seen_ids": []}

    def save_seen_alerts(self, state: Dict) -> None:
        """Save the set of seen alert IDs to the state file."""
        try:
            parent = os.path.dirname(self.last_polled_file)
            os.makedirs(parent if parent else ".", exist_ok=True)
            with open(self.last_polled_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    # ------------------------------------------------------------------
    # Reference data
    # ------------------------------------------------------------------

    def fetch_zones(self) -> List[dict]:
        """
        Fetch all NWS forecast zones as reference data.

        Returns:
            List of zone dicts with keys: zone_id, name, type, state,
            forecast_office, timezone, radar_station.
        """
        zones: List[dict] = []
        url: Optional[str] = ZONES_URL
        try:
            while url:
                response = requests.get(url, headers=HEADERS, timeout=30)
                response.raise_for_status()
                data = response.json()
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    zones.append(
                        {
                            "zone_id": props.get("id", ""),
                            "name": props.get("name", ""),
                            "type": props.get("type", ""),
                            "state": props.get("state", ""),
                            "forecast_office": props.get("forecastOffice", ""),
                            "timezone": props.get("timeZone", ""),
                            "radar_station": props.get("radarStation", ""),
                        }
                    )
                pagination = data.get("pagination", {})
                url = pagination.get("next") if pagination else None
        except Exception as err:
            print(f"Error fetching NWS zones: {err}")
        return zones

    def fetch_observation_stations(self, max_stations: int = 2500) -> List[dict]:
        """
        Fetch NWS observation stations.

        Updates ``self.station_ids`` and ``self.station_context``.

        Returns:
            List of station dicts with keys: station_id, name, elevation_m,
            time_zone, forecast_zone, county, fire_weather_zone, state, zone_id.
        """
        stations: List[dict] = []
        url: Optional[str] = f"{STATIONS_URL}?limit=500"
        try:
            while url and len(stations) < max_stations:
                response = requests.get(url, headers=HEADERS, timeout=30)
                response.raise_for_status()
                data = response.json()
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    sid = props.get("stationIdentifier", "")
                    if not sid:
                        continue
                    elev = props.get("elevation", {})
                    elev_val = elev.get("value") if isinstance(elev, dict) else None
                    forecast_url = props.get("forecast", "")
                    forecast_zone = forecast_url.rsplit("/", 1)[-1] if forecast_url else None
                    state = forecast_zone[:2] if forecast_zone and len(forecast_zone) >= 2 else None
                    county_url = props.get("county", "")
                    county_zone = county_url.rsplit("/", 1)[-1] if county_url else None
                    fire_url = props.get("fireWeatherZone", "")
                    fire_zone = fire_url.rsplit("/", 1)[-1] if fire_url else None
                    station: dict = {
                        "station_id": sid,
                        "name": props.get("name", ""),
                        "elevation_m": float(elev_val) if elev_val is not None else None,
                        "time_zone": props.get("timeZone"),
                        "forecast_zone": forecast_zone,
                        "county": county_zone,
                        "fire_weather_zone": fire_zone,
                        "state": state,
                        "zone_id": forecast_zone,
                    }
                    stations.append(station)
                    self.station_context[sid] = {"state": state, "zone_id": forecast_zone}
                pagination = data.get("pagination", {})
                url = pagination.get("next") if pagination else None
        except Exception as err:
            print(f"Error fetching NWS stations: {err}")
        self.station_ids = [s["station_id"] for s in stations]
        return stations

    # ------------------------------------------------------------------
    # Telemetry
    # ------------------------------------------------------------------

    def poll_alerts(self) -> List[dict]:
        """
        Fetch active alerts from the NWS API.

        Returns:
            List of raw alert feature dicts from the GeoJSON response.
        """
        try:
            response = requests.get(ALERTS_URL, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("features", [])
        except Exception as err:
            print(f"Error fetching NWS alerts: {err}")
            return []

    @staticmethod
    def _extract_value(quantity: object) -> Optional[float]:
        """Extract the numeric value from a NWS quantity object."""
        if quantity is None:
            return None
        if isinstance(quantity, dict):
            v = quantity.get("value")
            return float(v) if v is not None else None
        return None

    def fetch_latest_observation(self, station_id: str) -> Optional[dict]:
        """
        Fetch the latest observation for a single station.

        Returns:
            Observation dict with keys matching WeatherObservation fields,
            or None if no observation is available.
        """
        url = f"{STATIONS_URL}/{station_id}/observations/latest"
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            props = data.get("properties", {})
            ts = props.get("timestamp")
            if not ts:
                return None
            ctx = self.station_context.get(station_id, {})
            return {
                "station_id": station_id,
                "timestamp": ts,
                "text_description": props.get("textDescription"),
                "temperature": self._extract_value(props.get("temperature")),
                "dewpoint": self._extract_value(props.get("dewpoint")),
                "wind_direction": self._extract_value(props.get("windDirection")),
                "wind_speed": self._extract_value(props.get("windSpeed")),
                "wind_gust": self._extract_value(props.get("windGust")),
                "barometric_pressure": self._extract_value(props.get("barometricPressure")),
                "sea_level_pressure": self._extract_value(props.get("seaLevelPressure")),
                "visibility": self._extract_value(props.get("visibility")),
                "relative_humidity": self._extract_value(props.get("relativeHumidity")),
                "wind_chill": self._extract_value(props.get("windChill")),
                "heat_index": self._extract_value(props.get("heatIndex")),
                "state": ctx.get("state"),
                "zone_id": ctx.get("zone_id"),
            }
        except Exception as err:
            print(f"Error fetching observation for {station_id}: {err}")
            return None
