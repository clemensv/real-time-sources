"""SMHI Weather Observation Bridge - fetches meteorological observations from the Swedish Meteorological and Hydrological Institute."""

import argparse
import sys
import os
import time
import typing
import logging
import requests
from confluent_kafka import Producer

from smhi_weather_producer_kafka_producer.producer import SEGovSMHIWeatherEventProducer
from smhi_weather_producer_data import Station, WeatherObservation
from smhi_weather_core import (
    SMHIWeatherAPI, SMHI_BASE_URL, USER_AGENT,
    PARAM_AIR_TEMP, PARAM_WIND_GUST, PARAM_DEW_POINT, PARAM_PRESSURE,
    PARAM_HUMIDITY, PARAM_PRECIP, PARAM_WIND_DIR, PARAM_WIND_SPEED,
    PARAM_MAX_WIND_SPEED, PARAM_VISIBILITY, PARAM_CLOUD_COVER,
    PARAM_PRESENT_WX, PARAM_SUNSHINE, PARAM_IRRADIANCE, PARAM_PRECIP_INTENSITY,
    ALL_PARAMS, merge_observations, _load_state, _save_state, observation_lan_segment,
)

logger = logging.getLogger(__name__)

_merge_observations = merge_observations


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


def send_stations(api: SMHIWeatherAPI, producer: SEGovSMHIWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    stations = api.get_stations_for_parameter(PARAM_AIR_TEMP)
    sent = 0
    for sdata in stations:
        try:
            station = api.parse_station(sdata)
            producer.send_se_gov_smhi_weather_station(
                station.station_id, station, flush_producer=False,
            )
            sent += 1
        except Exception as e:
            logger.warning("Failed to parse station %s: %s", sdata.get("key", "?"), e)
    producer.producer.flush()
    logger.info("Sent %d station reference events", sent)
    return sent


def feed_observations(api: SMHIWeatherAPI, producer: SEGovSMHIWeatherEventProducer,
                      previous_readings: dict) -> int:
    """Fetch latest observations for all parameters and emit merged observations."""
    station_lan_by_id: dict[str, typing.Optional[str]] = {}
    try:
        for station_data in api.get_stations_for_parameter(PARAM_AIR_TEMP):
            station_lan_by_id[str(station_data.get("key", ""))] = api.extract_lan(station_data)
    except Exception as e:
        logger.warning("Failed to fetch station county metadata: %s", e)

    param_data: dict[int, dict[str, dict]] = {}
    for param_id in ALL_PARAMS:
        try:
            bulk = api.get_bulk_latest(param_id)
            param_data[param_id] = api.parse_bulk_observations(bulk)
        except Exception as e:
            logger.warning("Failed to fetch parameter %d: %s", param_id, e)

    observations = merge_observations(param_data, station_lan_by_id=station_lan_by_id)
    sent = 0
    for obs in observations:
        reading_key = f"{obs.station_id}:{obs.observation_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        producer.send_se_gov_smhi_weather_weather_observation(
            obs.station_id, obs, flush_producer=False,
        )
        sent += 1
        previous_readings[reading_key] = obs.observation_time.isoformat()

    producer.producer.flush()
    return sent


def main():
    """Main entry point for the SMHI Weather bridge."""
    parser = argparse.ArgumentParser(description="SMHI Weather Observation Bridge")
    parser.add_argument("--connection-string", required=False,
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False, default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int, default=int(os.environ.get("POLLING_INTERVAL", "900")))
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE", os.path.expanduser("~/.smhi_weather_state.json")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List active stations")
    feed_parser = subparsers.add_parser("feed", help="Feed data to Kafka")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle (also via ONCE_MODE env var). Useful for scheduled execution in Fabric notebooks.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    api = SMHIWeatherAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        stations = api.get_stations_for_parameter(PARAM_AIR_TEMP)
        for sdata in stations:
            station = api.parse_station(sdata)
            print(f"{station.station_id}: {station.name} [{station.latitude}, {station.longitude}]")
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
            args.topic = "smhi-weather"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "smhi-weather-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = SEGovSMHIWeatherEventProducer(kafka_producer, args.topic)
        logger.info("Starting SMHI Weather bridge, polling every %d seconds", args.polling_interval)
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
