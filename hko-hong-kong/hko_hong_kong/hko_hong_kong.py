"""HKO Hong Kong Weather Observation Bridge — fetches current weather from the Hong Kong Observatory."""

import argparse
import json
import sys
import os
import re
import time
import typing
import logging
import requests
from datetime import datetime, timezone
from confluent_kafka import Producer

from hko_hong_kong_producer_kafka_producer.producer import HKGovHKOWeatherEventProducer
from hko_hong_kong_producer_data import Station, WeatherObservation

logger = logging.getLogger(__name__)

HKO_API_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"


def slugify(name: str) -> str:
    """Convert a place name to a URL-safe slug identifier."""
    s = name.lower()
    s = s.replace("'", "")
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


class HKOWeatherAPI:
    """Client for the HKO open data weather API."""

    def __init__(self, base_url: str = HKO_API_URL, polling_interval: int = 600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()

    def get_current_weather(self) -> dict:
        """Fetch the rhrread (Regional Weather in Hong Kong) endpoint."""
        response = self.session.get(
            self.base_url, params={"dataType": "rhrread", "lang": "en"}, timeout=30
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def extract_places(data: dict) -> dict[str, Station]:
        """Extract all unique places from the rhrread response as Station reference data."""
        places: dict[str, dict] = {}

        for entry in data.get("temperature", {}).get("data", []):
            name = entry["place"]
            pid = slugify(name)
            if pid not in places:
                places[pid] = {"name": name, "types": set()}
            places[pid]["types"].add("temperature")

        for entry in data.get("rainfall", {}).get("data", []):
            name = entry["place"]
            pid = slugify(name)
            if pid not in places:
                places[pid] = {"name": name, "types": set()}
            places[pid]["types"].add("rainfall")

        for entry in data.get("humidity", {}).get("data", []):
            name = entry["place"]
            pid = slugify(name)
            if pid not in places:
                places[pid] = {"name": name, "types": set()}
            places[pid]["types"].add("humidity")

        for entry in data.get("uvindex", {}).get("data", []):
            name = entry["place"]
            pid = slugify(name)
            if pid not in places:
                places[pid] = {"name": name, "types": set()}
            places[pid]["types"].add("uvindex")

        stations: dict[str, Station] = {}
        for pid, info in places.items():
            stations[pid] = Station(
                place_id=pid,
                name=info["name"],
                data_types=",".join(sorted(info["types"])),
            )
        return stations

    @staticmethod
    def extract_observations(data: dict) -> list[WeatherObservation]:
        """Extract per-place observations from the rhrread response."""
        update_time_str = data.get("updateTime", "")
        try:
            update_time = datetime.fromisoformat(update_time_str)
        except (ValueError, TypeError):
            update_time = datetime.now(timezone.utc)

        temp_map: dict[str, float] = {}
        for entry in data.get("temperature", {}).get("data", []):
            temp_map[slugify(entry["place"])] = float(entry["value"])

        rain_map: dict[str, float] = {}
        for entry in data.get("rainfall", {}).get("data", []):
            rain_map[slugify(entry["place"])] = float(entry["max"])

        humidity_map: dict[str, int] = {}
        for entry in data.get("humidity", {}).get("data", []):
            humidity_map[slugify(entry["place"])] = int(entry["value"])

        uv_map: dict[str, tuple[float, str]] = {}
        for entry in data.get("uvindex", {}).get("data", []):
            uv_map[slugify(entry["place"])] = (
                float(entry.get("value", 0)),
                entry.get("desc", ""),
            )

        all_pids: set[str] = set()
        name_map: dict[str, str] = {}
        for section in ("temperature", "rainfall", "humidity", "uvindex"):
            for entry in data.get(section, {}).get("data", []):
                pid = slugify(entry["place"])
                all_pids.add(pid)
                name_map[pid] = entry["place"]

        observations = []
        for pid in sorted(all_pids):
            uv = uv_map.get(pid)
            obs = WeatherObservation(
                place_id=pid,
                place_name=name_map.get(pid, pid),
                observation_time=update_time,
                temperature=temp_map.get(pid),
                rainfall_max=rain_map.get(pid),
                humidity=humidity_map.get(pid),
                uv_index=uv[0] if uv else None,
                uv_description=uv[1] if uv else None,
            )
            observations.append(obs)
        return observations


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


def send_stations(api: HKOWeatherAPI, producer: HKGovHKOWeatherEventProducer) -> int:
    """Fetch current weather and emit station reference data."""
    data = api.get_current_weather()
    stations = api.extract_places(data)
    for pid, station in stations.items():
        producer.send_hk_gov_hko_weather_station(
            station.place_id, station, flush_producer=False,
        )
    producer.producer.flush()
    logger.info("Sent %d station reference events", len(stations))
    return len(stations)


def feed_observations(api: HKOWeatherAPI, producer: HKGovHKOWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch current weather and emit observation events."""
    data = api.get_current_weather()
    observations = api.extract_observations(data)
    sent = 0
    for obs in observations:
        reading_key = f"{obs.place_id}:{obs.observation_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        producer.send_hk_gov_hko_weather_weather_observation(
            obs.place_id, obs, flush_producer=False,
        )
        sent += 1
        previous_readings[reading_key] = obs.observation_time.isoformat()
    producer.producer.flush()
    return sent


def main():
    """Main entry point for the HKO Hong Kong Weather bridge."""
    parser = argparse.ArgumentParser(description="HKO Hong Kong Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "600")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.hko_hong_kong_state.json")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List places from current weather")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = HKOWeatherAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        data = api.get_current_weather()
        stations = api.extract_places(data)
        for pid, station in sorted(stations.items()):
            print(f"{station.place_id}: {station.name} [{station.data_types}]")
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
            args.topic = "hko-hong-kong"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "hko-hong-kong-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = HKGovHKOWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting HKO Hong Kong Weather bridge, polling every %d seconds", args.polling_interval)
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
