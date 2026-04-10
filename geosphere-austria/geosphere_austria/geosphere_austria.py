"""Bridge GeoSphere Austria TAWES 10-minute weather observations into Kafka as CloudEvents."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import time
import typing

import requests
from confluent_kafka import Producer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from geosphere_austria_producer_data import WeatherObservation, WeatherStation
from geosphere_austria_producer_kafka_producer.producer import AtGeosphereTawesEventProducer

logger = logging.getLogger(__name__)

METADATA_URL = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min/metadata"
OBSERVATIONS_URL = "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min"
OBSERVATION_PARAMS = "TL,RF,RR,DD,FF,P,SO,GLOW"
DEFAULT_TOPIC = "geosphere-austria-tawes"
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


def parse_connection_string(connection_string: str) -> typing.Tuple[typing.Dict[str, str], typing.Optional[str]]:
    """Parse a Kafka or Event Hubs connection string into a config dict and optional topic."""
    cs = connection_string.strip()
    parts = {kv.split("=", 1)[0].strip(): kv.split("=", 1)[1].strip().strip('"')
             for kv in cs.split(";") if "=" in kv}

    if "BootstrapServer" in parts:
        config: typing.Dict[str, str] = {"bootstrap.servers": parts["BootstrapServer"]}
        tls = os.environ.get("KAFKA_ENABLE_TLS", "true").lower()
        if tls == "false":
            config["security.protocol"] = "PLAINTEXT"
        topic = parts.get("EntityPath")
        return config, topic

    if "Endpoint" in parts:
        endpoint = parts["Endpoint"].replace("sb://", "").rstrip("/")
        config = {
            "bootstrap.servers": endpoint + ":9093",
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": "$ConnectionString",
            "sasl.password": cs,
        }
        topic = parts.get("EntityPath")
        return config, topic

    raise ValueError(f"Unrecognized connection string format: {cs[:80]}...")


def create_retrying_session() -> requests.Session:
    """Create an HTTP session with bounded retries for transient upstream failures."""
    session = requests.Session()
    session.headers.update({"User-Agent": "GitHub-Copilot-CLI/1.0"})
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
    return WeatherStation(
        station_id=str(raw["id"]),
        station_name=raw.get("name", ""),
        latitude=float(raw["lat"]),
        longitude=float(raw["lon"]),
        altitude=float(raw.get("altitude", 0.0)),
        state=raw.get("state") or None,
    )


def fetch_observations(
    session: requests.Session,
    station_ids: typing.List[str],
    batch_size: int = 50,
) -> typing.Tuple[typing.List[typing.Dict], str]:
    """Fetch current observations for all stations in batches.

    Returns a list of per-station observation dicts and the timestamp string.
    """
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

    # Use sentinel to avoid generated __post_init__ discarding 0.0 as falsy
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
    # Restore zero values that __post_init__ incorrectly nullified
    for field_name in PARAM_MAP.values():
        original = values.get(field_name)
        if original is not None and getattr(obs, field_name) is None:
            setattr(obs, field_name, float(original))
    return obs


def observation_fingerprint(obs: WeatherObservation) -> str:
    """Create a dedup fingerprint for an observation."""
    raw = f"{obs.station_id}|{obs.observation_time}|{obs.temperature}|{obs.humidity}|{obs.precipitation}|{obs.wind_direction}|{obs.wind_speed}|{obs.pressure}|{obs.sunshine_duration}|{obs.global_radiation}"
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


def send_station_events(
    producer: AtGeosphereTawesEventProducer,
    stations: typing.List[WeatherStation],
) -> int:
    """Emit WeatherStation reference events. Returns the count emitted."""
    for station in stations:
        producer.send_at_geosphere_tawes_weather_station(
            station.station_id, station, flush_producer=False
        )
    producer.producer.flush()
    return len(stations)


def send_observation_events(
    producer: AtGeosphereTawesEventProducer,
    observations: typing.List[WeatherObservation],
    state: typing.Dict,
) -> int:
    """Emit WeatherObservation events, deduplicating against state. Returns count emitted."""
    emitted = 0
    fingerprints = state.get("fingerprints", {})
    for obs in observations:
        fp = observation_fingerprint(obs)
        if fingerprints.get(obs.station_id) == fp:
            continue
        producer.send_at_geosphere_tawes_weather_observation(
            obs.station_id, obs, flush_producer=False
        )
        fingerprints[obs.station_id] = fp
        emitted += 1
    state["fingerprints"] = fingerprints
    producer.producer.flush()
    return emitted


def run_feed_cycle(
    producer: AtGeosphereTawesEventProducer,
    session: requests.Session,
    state: typing.Dict,
    station_refresh_due: bool = False,
    cached_stations: typing.Optional[typing.List[WeatherStation]] = None,
) -> typing.Tuple[int, int, typing.List[WeatherStation]]:
    """Run one full poll cycle: optionally refresh stations, then fetch and emit observations.

    Returns (stations_emitted, observations_emitted, stations_list).
    """
    stations_emitted = 0
    try:
        stations_raw = fetch_station_metadata(session)
        stations = [parse_station(s) for s in stations_raw]
        logger.info("Fetched %d active stations from metadata", len(stations))
    except requests.RequestException as exc:
        if not cached_stations:
            raise
        logger.warning("Station metadata refresh failed; continuing with cached stations: %s", exc)
        stations = cached_stations

    if station_refresh_due:
        stations_emitted = send_station_events(producer, stations)
        logger.info("Emitted %d station reference events", stations_emitted)

    station_ids = [s.station_id for s in stations]
    features, timestamp = fetch_observations(session, station_ids)
    logger.info("Fetched %d observation features for timestamp %s", len(features), timestamp)

    observations = []
    for feat in features:
        obs = parse_observation(feat, timestamp)
        if obs:
            observations.append(obs)

    obs_emitted = send_observation_events(producer, observations, state)
    logger.info("Emitted %d observation events (%d duplicates skipped)",
                obs_emitted, len(observations) - obs_emitted)

    return stations_emitted, obs_emitted, stations


def main() -> None:
    """Entry point for the GeoSphere Austria TAWES bridge."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    parser = argparse.ArgumentParser(description="GeoSphere Austria TAWES bridge")
    parser.add_argument("command", choices=["feed", "list"], default="feed", nargs="?")
    args = parser.parse_args()

    if args.command == "list":
        session = create_retrying_session()
        stations_raw = fetch_station_metadata(session)
        for s in stations_raw:
            print(f"{s['id']}: {s['name']} ({s.get('state', '?')})")
        return

    connection_string = os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logger.error("CONNECTION_STRING environment variable is required")
        return

    kafka_config, topic = parse_connection_string(connection_string)
    topic = topic or os.environ.get("KAFKA_TOPIC", DEFAULT_TOPIC)

    polling_interval = int(os.environ.get("POLLING_INTERVAL", str(DEFAULT_POLLING_INTERVAL)))
    station_refresh_interval = int(
        os.environ.get("STATION_REFRESH_INTERVAL", str(DEFAULT_STATION_REFRESH_INTERVAL))
    )
    state_file = os.environ.get("STATE_FILE", "geosphere_austria_state.json")

    kafka_producer = Producer(kafka_config)
    producer = AtGeosphereTawesEventProducer(kafka_producer, topic)
    session = create_retrying_session()
    state = load_state(state_file)
    last_station_refresh = 0.0
    cached_stations: typing.List[WeatherStation] = []

    logger.info(
        "Starting GeoSphere Austria TAWES bridge: topic=%s, poll=%ds, station_refresh=%ds",
        topic, polling_interval, station_refresh_interval,
    )

    while True:
        try:
            now = time.time()
            station_refresh_due = (now - last_station_refresh) >= station_refresh_interval
            stations_emitted, obs_emitted, cached_stations = run_feed_cycle(
                producer,
                session,
                state,
                station_refresh_due=station_refresh_due,
                cached_stations=cached_stations or None,
            )
            if station_refresh_due:
                last_station_refresh = now
            save_state(state_file, state)
        except requests.RequestException as exc:
            logger.error("HTTP error during feed cycle: %s", exc)
        except Exception:
            logger.exception("Unexpected error during feed cycle")

        logger.info("Sleeping %d seconds until next poll", polling_interval)
        time.sleep(polling_interval)


if __name__ == "__main__":
    main()
