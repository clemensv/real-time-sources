"""HKO Hong Kong Weather Observation Bridge — fetches current weather from the Hong Kong Observatory."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time

import requests
from confluent_kafka import Producer

from hko_hong_kong_core import HKOWeatherAPI, HKO_API_URL, USER_AGENT, _load_state, _save_state, slugify
from hko_hong_kong_producer_kafka_producer.producer import HKGovHKOWeatherEventProducer

logger = logging.getLogger(__name__)

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
    feed_parser = subparsers.add_parser("feed", help="Feed data to Kafka")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Run a single polling cycle and exit (also via ONCE_MODE env var; for scheduled hosts).")
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
        once = bool(getattr(args, "once", False))
        while True:
            try:
                count = feed_observations(api, event_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            if once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
