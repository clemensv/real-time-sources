"""Transport-agnostic acquisition layer for the GeoSphere Austria TAWES bridge."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import typing

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from geosphere_austria_producer_data import WeatherObservation, WeatherStation

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-geosphere-austria/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

METADATA_URL = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min/metadata"
OBSERVATIONS_URL = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min"
OBSERVATION_PARAMS = "TL,RF,RR,DD,FF,P,SO,GLOW"
DEFAULT_POLLING_INTERVAL = 600
DEFAULT_STATION_REFRESH_INTERVAL = 86400
DEFAULT_HTTP_RETRY_TOTAL = 3

PARAM_MAP = {
    "TL": "temperature",
    "RF": "humidity",
    "RR": "precipitation",
    "DD": "wind_direction",
    "FF": "wind_speed",
    "P": "pressure",
    "SO": "sunshine_duration",
    "GLOW": "global_radiation",
}


def create_retrying_session() -> requests.Session:
    """Create an HTTP session with bounded retries for transient upstream failures."""
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=DEFAULT_HTTP_RETRY_TOTAL,
        connect=DEFAULT_HTTP_RETRY_TOTAL,
        read=DEFAULT_HTTP_RETRY_TOTAL,
        status=DEFAULT_HTTP_RETRY_TOTAL,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_station_metadata(session: requests.Session) -> typing.List[typing.Dict]:
    """Fetch station metadata from the GeoSphere TAWES metadata endpoint."""
    resp = session.get(METADATA_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return [s for s in data.get("stations", []) if s.get("is_active", False)]


def parse_station(raw: typing.Dict) -> WeatherStation:
    """Convert a raw metadata dict to a WeatherStation data class."""
    bundesland = raw.get("bundesland") or raw.get("federal_state") or raw.get("state")
    return WeatherStation(
        station_id=str(raw["id"]),
        station_name=raw.get("name", ""),
        latitude=float(raw["lat"]),
        longitude=float(raw["lon"]),
        altitude=float(raw.get("altitude", 0.0)),
        state=raw.get("state") or None,
        bundesland=bundesland or None,
    )


def fetch_observations(
    session: requests.Session,
    station_ids: typing.List[str],
    batch_size: int = 50,
) -> typing.Tuple[typing.List[typing.Dict], str]:
    """Fetch current observations for all stations in batches."""
    all_features: typing.List[typing.Dict] = []
    timestamp = ""

    for i in range(0, len(station_ids), batch_size):
        batch = station_ids[i : i + batch_size]
        ids_param = ",".join(batch)
        try:
            resp = session.get(
                OBSERVATIONS_URL,
                params={
                    "parameters": OBSERVATION_PARAMS,
                    "station_ids": ids_param,
                    "output_format": "geojson",
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            logger.warning("Skipping observation batch %s after HTTP failure: %s", ids_param, exc)
            continue
        if data.get("timestamps"):
            timestamp = data["timestamps"][0]
        all_features.extend(data.get("features", []))

    return all_features, timestamp


def parse_observation(feature: typing.Dict, timestamp: str) -> typing.Optional[WeatherObservation]:
    """Convert a GeoJSON feature to a WeatherObservation data class."""
    props = feature.get("properties", {})
    station_id = str(props.get("station", ""))
    if not station_id:
        return None

    params = props.get("parameters", {})
    values: typing.Dict[str, typing.Optional[float]] = {}
    for api_key, field_name in PARAM_MAP.items():
        param = params.get(api_key)
        if param is not None:
            data_list = param.get("data", [None])
            val = data_list[0] if data_list else None
            values[field_name] = float(val) if val is not None else None
        else:
            values[field_name] = None

    obs = WeatherObservation(
        station_id=station_id,
        observation_time=timestamp,
        temperature=values.get("temperature"),
        humidity=values.get("humidity"),
        precipitation=values.get("precipitation"),
        wind_direction=values.get("wind_direction"),
        wind_speed=values.get("wind_speed"),
        pressure=values.get("pressure"),
        sunshine_duration=values.get("sunshine_duration"),
        global_radiation=values.get("global_radiation"),
    )
    for field_name in PARAM_MAP.values():
        original = values.get(field_name)
        if original is not None and getattr(obs, field_name) is None:
            setattr(obs, field_name, float(original))
    return obs


def observation_fingerprint(obs: WeatherObservation) -> str:
    """Create a dedup fingerprint for an observation."""
    raw = (
        f"{obs.station_id}|{obs.observation_time}|{obs.temperature}|"
        f"{obs.humidity}|{obs.precipitation}|{obs.wind_direction}|"
        f"{obs.wind_speed}|{obs.pressure}|{obs.sunshine_duration}|{obs.global_radiation}"
    )
    return hashlib.md5(raw.encode()).hexdigest()


def load_state(path: str) -> typing.Dict:
    """Load dedup state from disk."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_state(path: str, state: typing.Dict) -> None:
    """Persist dedup state to disk."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except IOError as exc:
        logger.warning("Failed to save state: %s", exc)


def station_bundesland_segment(station: WeatherStation) -> str:
    """Return a safe topic/route segment for the station's Bundesland."""
    raw = (station.bundesland or station.state or "unknown").strip()
    if not raw:
        return "unknown"
    for ch in ("/", "+", "#", " "):
        raw = raw.replace(ch, "-")
    return raw or "unknown"
