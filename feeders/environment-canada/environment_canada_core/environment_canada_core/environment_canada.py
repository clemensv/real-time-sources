"""Environment Canada Weather Bridge — fetches SWOB real-time observations via the OGC API."""

from __future__ import annotations

import json
import logging
import os
import sys
import typing
from datetime import datetime, timezone
from pathlib import Path

import requests

try:
    from environment_canada_producer_data import Station, WeatherObservation
except ModuleNotFoundError:
    sys.path.insert(
        0,
        str(
            Path(__file__).resolve().parents[2]
            / "environment_canada_producer"
            / "environment_canada_producer_data"
            / "src"
        ),
    )
    from environment_canada_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-environment-canada/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

EC_API_BASE = "https://api.weather.gc.ca/collections"
SWOB_STATIONS_URL = f"{EC_API_BASE}/swob-stations/items"
SWOB_REALTIME_URL = f"{EC_API_BASE}/swob-realtime/items"

DEFAULT_LIMIT = 500


class ECWeatherAPI:
    """Client for the Environment Canada OGC API (SWOB stations and realtime)."""

    def __init__(self, base_url: str = EC_API_BASE, polling_interval: int = 900,
                 station_limit: int = DEFAULT_LIMIT, obs_limit: int = DEFAULT_LIMIT):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.station_limit = station_limit
        self.obs_limit = obs_limit
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT

    def get_stations(self) -> list[dict]:
        """Fetch station metadata from swob-stations collection."""
        url = f"{self.base_url}/swob-stations/items"
        all_stations = []
        offset = 0
        while True:
            response = self.session.get(
                url, params={"f": "json", "limit": self.station_limit, "offset": offset},  # type: ignore[arg-type]
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            features = data.get("features", [])
            if not features:
                break
            all_stations.extend(features)
            if len(features) < self.station_limit:
                break
            offset += len(features)
        return all_stations

    def get_recent_observations(self) -> list[dict]:
        """Fetch recent SWOB realtime observations (last 2 hours)."""
        url = f"{self.base_url}/swob-realtime/items"
        from datetime import timedelta
        two_hours_ago = (datetime.now(timezone.utc) - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        all_obs = []
        offset = 0
        while True:
            response = self.session.get(
                url, params={  # type: ignore[arg-type]
                    "f": "json",
                    "limit": self.obs_limit,
                    "offset": offset,
                    "datetime": f"{two_hours_ago}/..",
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            features = data.get("features", [])
            if not features:
                break
            all_obs.extend(features)
            if len(features) < self.obs_limit:
                break
            offset += len(features)
        return all_obs

    @staticmethod
    def parse_station(feature: dict) -> Station:
        """Parse a swob-stations feature into a Station data class."""
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", []) if geom else []
        lon = float(coords[0]) if len(coords) > 0 else None
        lat = float(coords[1]) if len(coords) > 1 else None
        elev = float(coords[2]) if len(coords) > 2 else None
        province = props.get("province") or props.get("province_territory", "")

        return Station(
            msc_id=str(props.get("msc_id", "")),
            name=props.get("name", ""),
            iata_id=props.get("iata_id", ""),
            wmo_id=props.get("wmo_id"),
            province_territory=props.get("province_territory", ""),
            data_provider=props.get("data_provider", ""),
            dataset_network=props.get("dataset_network", ""),
            auto_man=props.get("auto_man", ""),
            latitude=lat,
            longitude=lon,
            elevation=elev,
            province=province,
        )

    @staticmethod
    def parse_observation(feature: dict) -> typing.Optional[WeatherObservation]:
        """Parse a swob-realtime feature into a WeatherObservation, extracting core fields."""
        props = feature.get("properties", {})
        msc_id = str(props.get("msc_id-value", props.get("clim_id-value", "")))
        if not msc_id:
            return None
        obs_time_str = props.get("obs_date_tm", "")
        if not obs_time_str:
            return None
        try:
            obs_time = datetime.fromisoformat(obs_time_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None

        station_name = props.get("stn_nam-value", "")

        def _float(key: str) -> typing.Optional[float]:
            v = props.get(key)
            if v is None:
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        def _int(key: str) -> typing.Optional[int]:
            v = props.get(key)
            if v is None:
                return None
            try:
                return int(v)
            except (ValueError, TypeError):
                return None

        province = (
            props.get("prov_state_terr-value")
            or props.get("province-value")
            or props.get("province_territory-value")
        )

        return WeatherObservation(
            msc_id=msc_id,
            station_name=station_name,
            observation_time=obs_time,
            air_temperature=_float("air_temp"),
            dew_point=_float("dwpt_temp"),
            relative_humidity=_int("rel_hum"),
            station_pressure=_float("stn_pres"),
            wind_speed=_float("avg_wnd_spd_10m_pst1mt"),
            wind_direction=_int("avg_wnd_dir_10m_pst1mt"),
            wind_gust=_float("max_wnd_spd_10m_pst1mt"),
            precipitation_1hr=_float("pcpn_amt_pst1hr"),
            mean_sea_level_pressure=_float("mslp"),
            visibility=_float("vis"),
            snow_depth=_float("snw_dpth"),
            total_cloud_cover=_int("tot_cld_amt"),
            pressure_tendency_3hr=_float("pres_tend_amt_pst3hrs"),
            max_temperature_24hr=_float("max_air_temp_pst24hrs"),
            min_temperature_24hr=_float("min_air_temp_pst24hrs"),
            wind_speed_1hr=_float("avg_wnd_spd_10m_pst1hr"),
            wind_gust_1hr=_float("max_wnd_spd_10m_pst1hr"),
            precipitation_24hr=_float("pcpn_amt_pst24hrs"),
            altimeter_setting=_float("altmetr_setng"),
            province=province,
        )

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
