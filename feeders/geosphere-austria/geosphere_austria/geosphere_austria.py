"""Bridge GeoSphere Austria TAWES 10-minute weather observations into Kafka as CloudEvents."""

from __future__ import annotations

import argparse
import logging
import os
import time
import typing

import requests
from confluent_kafka import Producer

from geosphere_austria_producer_data import WeatherObservation, WeatherStation
from geosphere_austria_producer_kafka_producer.producer import AtGeosphereTawesEventProducer
from geosphere_austria_core import (
    create_retrying_session,
    fetch_station_metadata,
    parse_station,
    fetch_observations,
    parse_observation,
    observation_fingerprint,
    load_state,
    save_state,
    PARAM_MAP,
    station_bundesland_segment,
    DEFAULT_POLLING_INTERVAL,
    DEFAULT_STATION_REFRESH_INTERVAL,
    METADATA_URL,
    OBSERVATIONS_URL,
)

logger = logging.getLogger(__name__)

DEFAULT_TOPIC = "geosphere-austria-tawes"


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
    parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle (also via ONCE_MODE env var). "
             "Useful for scheduled execution in Fabric notebooks.",
    )
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
        if args.once:
            logger.info("--once mode: exiting after first polling cycle")
            break
        time.sleep(polling_interval)


if __name__ == "__main__":
    main()
