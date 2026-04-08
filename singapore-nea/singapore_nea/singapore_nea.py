"""Singapore NEA Weather and Air Quality Bridge."""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone

import requests
from confluent_kafka import Producer

from singapore_nea_producer_data import Station, WeatherObservation
from singapore_nea_producer_kafka_producer.producer import (
    SGGovNEAAirQualityEventProducer,
    SGGovNEAWeatherEventProducer,
)

from singapore_nea.air_quality import (
    NEAAirQualityAPI,
    fetch_and_send_pm25,
    fetch_and_send_psi,
    fetch_and_send_regions,
)

logger = logging.getLogger(__name__)

NEA_BASE_URL = "https://api.data.gov.sg/v1/environment"
AIR_QUALITY_REFERENCE_REFRESH_INTERVAL = 24 * 60 * 60

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
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.warning("Failed to fetch stations from %s: %s", endpoint, exc)

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


def merge_observations(api: NEAWeatherAPI) -> tuple[dict[str, Station], list[WeatherObservation]]:
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
        obs_time = datetime.fromisoformat(latest_ts)
    except (ValueError, TypeError):
        obs_time = datetime.now(timezone.utc)

    name_map = {sid: station.name for sid, station in stations.items()}
    all_station_ids = set()
    for readings in param_data.values():
        all_station_ids.update(readings.keys())

    observations: list[WeatherObservation] = []
    for station_id in sorted(all_station_ids):
        observations.append(
            WeatherObservation(
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


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config: dict[str, str] = {}
    for part in connection_string.split(";"):
        part = part.strip()
        if "=" not in part:
            continue
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
            with open(state_file, "r", encoding="utf-8") as file_handle:
                return json.load(file_handle)
    except Exception as exc:  # pragma: no cover - defensive logging
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict) -> None:
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
        with open(state_file, "w", encoding="utf-8") as file_handle:
            json.dump(data, file_handle)
    except Exception as exc:  # pragma: no cover - defensive logging
        logging.warning("Could not save state to %s: %s", state_file, exc)


def _truncate_state_entries(data: dict) -> dict:
    """Keep persisted dedupe maps from growing without bound."""
    if not isinstance(data, dict) or len(data) <= 100000:
        return data
    keys = list(data.keys())
    return {key: data[key] for key in keys[-50000:]}


def _split_state(state: dict) -> tuple[dict, dict, dict]:
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


def _compose_state(weather_state: dict, psi_state: dict, pm25_state: dict) -> dict:
    """Compose the persisted state document."""
    return {
        "weather": weather_state,
        "air_quality": {
            "psi": psi_state,
            "pm25": pm25_state,
        },
    }


def send_stations(api: NEAWeatherAPI, producer: SGGovNEAWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    stations = api.get_all_stations()
    for station_id, station in stations.items():
        producer.send_sg_gov_nea_weather_station(station_id, station, flush_producer=False)
    producer.producer.flush()
    logger.info("Sent %d weather station reference events", len(stations))
    return len(stations)


def feed_observations(
    api: NEAWeatherAPI, producer: SGGovNEAWeatherEventProducer, previous_readings: dict
) -> int:
    """Fetch and emit weather observation events."""
    _, observations = merge_observations(api)
    sent = 0
    for observation in observations:
        reading_key = f"{observation.station_id}:{observation.observation_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        producer.send_sg_gov_nea_weather_weather_observation(
            observation.station_id,
            observation,
            flush_producer=False,
        )
        previous_readings[reading_key] = observation.observation_time.isoformat()
        sent += 1
    producer.producer.flush()
    return sent


def _create_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    """Create Kafka producer configuration and resolve the weather topic."""
    if not args.connection_string:
        if not os.environ.get("KAFKA_BROKER"):
            print("Error: --connection-string or KAFKA_BROKER required for feed mode")
            sys.exit(1)
        kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
    else:
        kafka_config = parse_connection_string(args.connection_string)

    weather_topic = args.topic
    if "_entity_path" in kafka_config and not weather_topic:
        weather_topic = kafka_config.pop("_entity_path")
    elif "_entity_path" in kafka_config:
        kafka_config.pop("_entity_path")

    if not weather_topic:
        weather_topic = "singapore-nea"

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    if "sasl.username" in kafka_config:
        kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
    kafka_config["client.id"] = "singapore-nea-bridge"
    return kafka_config, weather_topic


def main():
    """Main entry point for the Singapore NEA bridge."""
    parser = argparse.ArgumentParser(description="Singapore NEA Weather and Air Quality Bridge")
    parser.add_argument(
        "--connection-string",
        required=False,
        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"),
    )
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument(
        "--airquality-topic",
        required=False,
        default=os.environ.get("AIRQUALITY_TOPIC", "singapore-nea-airquality"),
    )
    parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.environ.get("POLLING_INTERVAL", "300")),
    )
    parser.add_argument(
        "--airquality-polling-interval",
        type=int,
        default=int(os.environ.get("AIRQUALITY_POLLING_INTERVAL", "3600")),
    )
    parser.add_argument(
        "--state-file",
        type=str,
        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.singapore_nea_state.json")),
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List weather stations")
    subparsers.add_parser("list-air-quality", help="List air quality regions")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    weather_api = NEAWeatherAPI(polling_interval=args.polling_interval)
    air_quality_api = NEAAirQualityAPI(polling_interval=args.airquality_polling_interval)

    if args.command == "list":
        stations = weather_api.get_all_stations()
        for _, station in sorted(stations.items()):
            print(
                f"{station.station_id}: {station.name} "
                f"[{station.latitude}, {station.longitude}] ({station.data_types})"
            )
        return

    if args.command == "list-air-quality":
        regions = air_quality_api.get_regions()
        for _, region in sorted(regions.items()):
            print(f"{region.region}: [{region.latitude}, {region.longitude}]")
        return

    if args.command != "feed":
        parser.print_help()
        return

    kafka_config, weather_topic = _create_kafka_config(args)
    kafka_producer = Producer(kafka_config)
    weather_event_producer = SGGovNEAWeatherEventProducer(kafka_producer, weather_topic)
    airquality_topic = args.airquality_topic or None
    airquality_event_producer = (
        SGGovNEAAirQualityEventProducer(kafka_producer, airquality_topic) if airquality_topic else None
    )

    previous_state = _load_state(args.state_file)
    weather_state, psi_state, pm25_state = _split_state(previous_state)

    logger.info(
        "Starting Singapore NEA bridge. Weather every %d seconds; air quality every %d seconds",
        args.polling_interval,
        args.airquality_polling_interval,
    )
    send_stations(weather_api, weather_event_producer)
    if airquality_event_producer:
        fetch_and_send_regions(air_quality_api, airquality_event_producer)

    now = time.monotonic()
    next_weather_poll = now
    next_airquality_poll = now if airquality_event_producer else float("inf")
    next_airquality_region_refresh = (
        now + AIR_QUALITY_REFERENCE_REFRESH_INTERVAL if airquality_event_producer else float("inf")
    )

    while True:
        now = time.monotonic()
        next_due = min(next_weather_poll, next_airquality_poll, next_airquality_region_refresh)
        if now < next_due:
            time.sleep(max(1, min(int(next_due - now), 30)))
            continue

        state_changed = False

        if now >= next_weather_poll:
            next_weather_poll = now + args.polling_interval
            try:
                count = feed_observations(weather_api, weather_event_producer, weather_state)
                logger.info("Sent %d weather observation events", count)
                state_changed = True
            except Exception as exc:  # pragma: no cover - runtime safety
                logger.error("Error fetching/sending weather data: %s", exc)

        if airquality_event_producer and now >= next_airquality_region_refresh:
            next_airquality_region_refresh = now + AIR_QUALITY_REFERENCE_REFRESH_INTERVAL
            try:
                fetch_and_send_regions(air_quality_api, airquality_event_producer)
            except Exception as exc:  # pragma: no cover - runtime safety
                logger.error("Error refreshing air quality regions: %s", exc)

        if airquality_event_producer and now >= next_airquality_poll:
            next_airquality_poll = now + args.airquality_polling_interval
            try:
                psi_count = fetch_and_send_psi(air_quality_api, airquality_event_producer, psi_state)
                pm25_count = fetch_and_send_pm25(
                    air_quality_api,
                    airquality_event_producer,
                    pm25_state,
                )
                logger.info(
                    "Sent %d PSI readings and %d PM2.5 readings",
                    psi_count,
                    pm25_count,
                )
                state_changed = True
            except Exception as exc:  # pragma: no cover - runtime safety
                logger.error("Error fetching/sending air quality data: %s", exc)

        if state_changed:
            _save_state(args.state_file, _compose_state(weather_state, psi_state, pm25_state))


if __name__ == "__main__":
    main()
