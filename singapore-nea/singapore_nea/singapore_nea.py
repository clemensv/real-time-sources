"""Singapore NEA Weather Observation Bridge — fetches real-time weather from data.gov.sg."""

import argparse
import json
import sys
import os
import time
import typing
import logging
import requests
from datetime import datetime, timezone
from confluent_kafka import Producer

from singapore_nea_producer_kafka_producer.producer import SGGovNEAWeatherEventProducer
from singapore_nea_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

NEA_BASE_URL = "https://api.data.gov.sg/v1/environment"

ENDPOINTS = ["air-temperature", "rainfall", "relative-humidity", "wind-speed", "wind-direction"]

FIELD_MAP = {
    "air-temperature": "air_temperature",
    "rainfall": "rainfall",
    "relative-humidity": "relative_humidity",
    "wind-speed": "wind_speed",
    "wind-direction": "wind_direction",
}


class NEAWeatherAPI:
    """Client for the Singapore NEA weather API on data.gov.sg."""

    def __init__(self, base_url: str = NEA_BASE_URL, polling_interval: int = 300):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()

    def get_endpoint(self, endpoint: str) -> dict:
        """Fetch a single environment endpoint."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_all_stations(self) -> dict[str, Station]:
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
            except Exception as e:
                logger.warning("Failed to fetch stations from %s: %s", endpoint, e)

        stations: dict[str, Station] = {}
        for sid, info in station_info.items():
            loc = info.get("location", {})
            stations[sid] = Station(
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
        """Parse a single endpoint response into {station_id: value} + timestamp."""
        items = data.get("items", [])
        if not items:
            return "", {}
        item = items[0]
        timestamp = item.get("timestamp", "")
        readings: dict[str, float] = {}
        for r in item.get("readings", []):
            readings[r["station_id"]] = float(r["value"])
        return timestamp, readings


def merge_observations(api: NEAWeatherAPI) -> tuple[dict[str, Station], list[WeatherObservation]]:
    """Fetch all endpoints and merge per-station observations."""
    stations = api.get_all_stations()
    param_data: dict[str, dict[str, float]] = {}
    latest_ts = ""

    for endpoint in ENDPOINTS:
        try:
            data = api.get_endpoint(endpoint)
            ts, readings = api.parse_readings(data)
            field = FIELD_MAP[endpoint]
            param_data[field] = readings
            if ts and ts > latest_ts:
                latest_ts = ts
        except Exception as e:
            logger.warning("Failed to fetch %s: %s", endpoint, e)

    try:
        obs_time = datetime.fromisoformat(latest_ts)
    except (ValueError, TypeError):
        obs_time = datetime.now(timezone.utc)

    name_map = {sid: st.name for sid, st in stations.items()}
    all_sids = set()
    for readings in param_data.values():
        all_sids.update(readings.keys())

    observations = []
    for sid in sorted(all_sids):
        obs = WeatherObservation(
            station_id=sid,
            station_name=name_map.get(sid, sid),
            observation_time=obs_time,
            air_temperature=param_data.get("air_temperature", {}).get(sid),
            rainfall=param_data.get("rainfall", {}).get(sid),
            relative_humidity=param_data.get("relative_humidity", {}).get(sid),
            wind_speed=param_data.get("wind_speed", {}).get(sid),
            wind_direction=param_data.get("wind_direction", {}).get(sid),
        )
        observations.append(obs)
    return stations, observations


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config: dict[str, str] = {}
    for part in connection_string.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key == "Endpoint":
                config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "SharedAccessKeyName":
                config["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config["sasl.password"] = connection_string
            elif key == "BootstrapServer":
                config["bootstrap.servers"] = value
            elif key == "EntityPath":
                config["_entity_path"] = value
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


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


def send_stations(api: NEAWeatherAPI, producer: SGGovNEAWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    stations = api.get_all_stations()
    for sid, station in stations.items():
        producer.send_sg_gov_nea_weather_station(
            station.station_id, station, flush_producer=False,
        )
    producer.producer.flush()
    logger.info("Sent %d station reference events", len(stations))
    return len(stations)


def feed_observations(api: NEAWeatherAPI, producer: SGGovNEAWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch and emit observation events."""
    _, observations = merge_observations(api)
    sent = 0
    for obs in observations:
        reading_key = f"{obs.station_id}:{obs.observation_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        producer.send_sg_gov_nea_weather_weather_observation(
            obs.station_id, obs, flush_producer=False,
        )
        sent += 1
        previous_readings[reading_key] = obs.observation_time.isoformat()
    producer.producer.flush()
    return sent


def main():
    """Main entry point for the Singapore NEA Weather bridge."""
    parser = argparse.ArgumentParser(description="Singapore NEA Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "300")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.singapore_nea_state.json")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List stations")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = NEAWeatherAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        stations = api.get_all_stations()
        for sid, station in sorted(stations.items()):
            print(f"{station.station_id}: {station.name} [{station.latitude}, {station.longitude}] ({station.data_types})")
    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                print("Error: --connection-string or KAFKA_BROKER required for feed mode")
                sys.exit(1)
            kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")
        if not args.topic:
            args.topic = "singapore-nea"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "singapore-nea-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = SGGovNEAWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting Singapore NEA Weather bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        send_stations(api, event_producer)
        while True:
            try:
                count = feed_observations(api, event_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
