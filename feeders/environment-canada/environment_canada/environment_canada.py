"""Environment Canada Weather Bridge — fetches SWOB real-time observations via the OGC API."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path

import requests
from confluent_kafka import Producer

from environment_canada_core import DEFAULT_LIMIT, EC_API_BASE, ECWeatherAPI, SWOB_REALTIME_URL, SWOB_STATIONS_URL, USER_AGENT, _load_state, _save_state
try:
    from environment_canada_producer_kafka_producer.producer import CAGovECCCWeatherEventProducer
except ModuleNotFoundError:
    sys.path.insert(
        0,
        str(
            Path(__file__).resolve().parents[1]
            / "environment_canada_producer"
            / "environment_canada_producer_kafka_producer"
            / "src"
        ),
    )
    from environment_canada_producer_kafka_producer.producer import CAGovECCCWeatherEventProducer

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

def send_stations(api: ECWeatherAPI, producer: CAGovECCCWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    features = api.get_stations()
    sent = 0
    for f in features:
        try:
            station = api.parse_station(f)
            if not station.msc_id:
                continue
            producer.send_ca_gov_eccc_weather_station(
                station.msc_id, station, flush_producer=False,
            )
            sent += 1
        except Exception as e:
            logger.warning("Failed to parse station: %s", e)
    producer.producer.flush()
    logger.info("Sent %d station reference events", sent)
    return sent


def feed_observations(api: ECWeatherAPI, producer: CAGovECCCWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch and emit observation events."""
    features = api.get_recent_observations()
    sent = 0
    for f in features:
        try:
            obs = api.parse_observation(f)
            if not obs:
                continue
            reading_key = f"{obs.msc_id}:{obs.observation_time.isoformat()}"
            if reading_key in previous_readings:
                continue
            producer.send_ca_gov_eccc_weather_weather_observation(
                obs.msc_id, obs, flush_producer=False,
            )
            sent += 1
            previous_readings[reading_key] = obs.observation_time.isoformat()
        except Exception as e:
            logger.warning("Failed to parse observation: %s", e)
    producer.producer.flush()
    return sent


def main():
    """Main entry point for the Environment Canada Weather bridge."""
    parser = argparse.ArgumentParser(description="Environment Canada Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "900")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.environment_canada_state.json")))
    parser.add_argument("--station-limit", type=int, default=int(os.environ.get("STATION_LIMIT", "500")))
    parser.add_argument("--obs-limit", type=int, default=int(os.environ.get("OBS_LIMIT", "500")))
    parser.add_argument("--once", action="store_true",
                        default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                        help="Exit after one polling cycle (also via ONCE_MODE env var). Useful for scheduled execution in Fabric notebooks.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List SWOB stations")
    feed_parser = subparsers.add_parser("feed", help="Feed data to Kafka")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes'),
                             help='Exit after one polling cycle (also via ONCE_MODE env var).')
    args = parser.parse_args()
    args.once = bool(
        getattr(args, "once", False)
        or "--once" in sys.argv
        or os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes")
    )
    logging.basicConfig(level=logging.INFO)
    api = ECWeatherAPI(polling_interval=args.polling_interval,
                       station_limit=args.station_limit, obs_limit=args.obs_limit)

    if args.command == "list":
        features = api.get_stations()
        for f in features:
            station = api.parse_station(f)
            print(f"{station.msc_id}: {station.name} [{station.province_territory}]")
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
            args.topic = "environment-canada"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "environment-canada-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = CAGovECCCWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting Environment Canada Weather bridge, polling every %d seconds", args.polling_interval)
        previous_readings = _load_state(args.state_file)
        send_stations(api, event_producer)
        while True:
            try:
                count = feed_observations(api, event_producer, previous_readings)
                _save_state(args.state_file, previous_readings)
                logger.info("Sent %d observation events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            if args.once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
