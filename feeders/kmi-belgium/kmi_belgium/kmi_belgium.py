"""KMI Belgium Weather Observation Bridge - fetches automatic weather station observations from the Royal Meteorological Institute of Belgium."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time

import requests
from confluent_kafka import Producer

from kmi_belgium_core import FEATURE_TYPE, KMI_AWS_WFS_URL, KMIBelgiumAPI, LATEST_FETCH_COUNT, OBSERVATION_FIELDS, USER_AGENT, _format_timestamp, _load_state, _parse_timestamp, _save_state, _to_float, extract_stations
from kmi_belgium_producer_kafka_producer.producer import BEGovKMIWeatherEventProducer

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

def send_stations(api: KMIBelgiumAPI, producer: BEGovKMIWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    features = api.get_latest_observations()
    stations = extract_stations(features)
    sent = 0
    for station in stations:
        producer.send_be_gov_kmi_weather_station(
            station.station_code, station, flush_producer=False,
        )
        sent += 1
    producer.producer.flush()
    logger.info("Sent %d station reference events", sent)
    return sent



def feed_observations(api: KMIBelgiumAPI, producer: BEGovKMIWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch observations and emit only new readings."""
    last_timestamp = previous_readings.get("__last_timestamp__")
    if last_timestamp:
        features = api.get_observations(last_timestamp=last_timestamp)
    else:
        features = api.get_latest_observations()

    sent = 0
    latest_observation_time: datetime | None = None

    for feature in features:
        obs = api.parse_observation(feature)
        if latest_observation_time is None or obs.observation_time > latest_observation_time:
            latest_observation_time = obs.observation_time
        reading_timestamp = _format_timestamp(obs.observation_time)
        reading_key = f"{obs.station_code}:{reading_timestamp}"
        if reading_key in previous_readings:
            continue
        producer.send_be_gov_kmi_weather_weather_observation(
            obs.station_code, obs, flush_producer=False,
        )
        sent += 1
        previous_readings[reading_key] = reading_timestamp

    if latest_observation_time is not None:
        previous_readings["__last_timestamp__"] = _format_timestamp(latest_observation_time)

    producer.producer.flush()
    return sent



def main():
    """Main entry point for the KMI Belgium Weather bridge."""
    parser = argparse.ArgumentParser(description="KMI Belgium Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "600")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.kmi_belgium_state.json")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List active stations")
    feed_parser = subparsers.add_parser("feed", help="Feed data to Kafka")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle (also via ONCE_MODE env var). "
                                  "Useful for scheduled execution in Fabric notebooks.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = KMIBelgiumAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        stations = extract_stations(api.get_latest_observations())
        for station in stations:
            logger.info("%s: [%s, %s]", station.station_code, station.latitude, station.longitude)
    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                logger.error("Error: --connection-string or KAFKA_BROKER required for feed mode")
                sys.exit(1)
            kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")
        if not args.topic:
            args.topic = "kmi-belgium"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "kmi-belgium-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = BEGovKMIWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting KMI Belgium Weather bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        send_stations(api, event_producer)
        while True:
            try:
                count = feed_observations(api, event_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            if getattr(args, "once", False):
                logger.info("--once mode: exiting after first polling cycle")
                break
            time.sleep(args.polling_interval)
    else:
        logger.info("%s", parser.format_help().rstrip())


if __name__ == "__main__":
    main()
