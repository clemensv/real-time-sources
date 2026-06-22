"""Singapore NEA Weather and Air Quality Bridge."""

import argparse
import logging
import os
import sys
import time

from confluent_kafka import Producer

from singapore_nea_producer_data import Station, WeatherObservation
from singapore_nea_producer_kafka_producer.producer import (
    SGGovNEAAirQualityEventProducer,
    SGGovNEAWeatherEventProducer,
)

from singapore_nea_core import (
    NEAWeatherAPI,
    merge_observations,
    load_state,
    save_state,
    split_state,
    compose_state,
    AIR_QUALITY_REFERENCE_REFRESH_INTERVAL,
)

from singapore_nea.air_quality import (
    NEAAirQualityAPI,
    fetch_and_send_pm25,
    fetch_and_send_psi,
    fetch_and_send_regions,
)

logger = logging.getLogger(__name__)


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


def send_stations(api: NEAWeatherAPI, producer: SGGovNEAWeatherEventProducer) -> int:
    """Fetch and emit station reference data."""
    station_data = api.get_all_stations()
    for station_id, sd in station_data.items():
        station = Station(
            station_id=sd.station_id,
            device_id=sd.device_id,
            name=sd.name,
            latitude=sd.latitude,
            longitude=sd.longitude,
            data_types=sd.data_types,
        )
        producer.send_sg_gov_nea_weather_station(station_id, station, flush_producer=False)
    producer.producer.flush()
    logger.info("Sent %d weather station reference events", len(station_data))
    return len(station_data)


def feed_observations(
    api: NEAWeatherAPI,
    producer: SGGovNEAWeatherEventProducer,
    previous_readings: dict,
) -> int:
    """Fetch and emit weather observation events."""
    _, observations = merge_observations(api)
    sent = 0
    for obs in observations:
        reading_key = f"{obs.station_id}:{obs.observation_time.isoformat()}"
        if reading_key in previous_readings:
            continue
        observation = WeatherObservation(
            station_id=obs.station_id,
            station_name=obs.station_name,
            observation_time=obs.observation_time,
            air_temperature=obs.air_temperature,
            rainfall=obs.rainfall,
            relative_humidity=obs.relative_humidity,
            wind_speed=obs.wind_speed,
            wind_direction=obs.wind_direction,
        )
        producer.send_sg_gov_nea_weather_weather_observation(
            obs.station_id,
            observation,
            flush_producer=False,
        )
        previous_readings[reading_key] = obs.observation_time.isoformat()
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
    parser.add_argument(
        "--once",
        action="store_true",
        default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle (also via ONCE_MODE env var). Useful for scheduled execution in Fabric notebooks.",
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
        SGGovNEAAirQualityEventProducer(kafka_producer, airquality_topic)
        if airquality_topic
        else None
    )

    previous_state = load_state(args.state_file)
    weather_state, psi_state, pm25_state = split_state(previous_state)

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

    did_weather = False
    did_airquality = not bool(airquality_event_producer)

    while True:
        now = time.monotonic()
        next_due = min(next_weather_poll, next_airquality_poll, next_airquality_region_refresh)
        if now < next_due:
            time.sleep(max(1, min(int(next_due - now), 30)))
            continue

        state_changed = False

        if now >= next_weather_poll:
            did_weather = True
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
            did_airquality = True
            next_airquality_poll = now + args.airquality_polling_interval
            try:
                psi_count = fetch_and_send_psi(
                    air_quality_api, airquality_event_producer, psi_state
                )
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
            save_state(args.state_file, compose_state(weather_state, psi_state, pm25_state))

        if args.once and did_weather and did_airquality:
            logger.info("--once mode: exiting after first polling cycle")
            break


if __name__ == "__main__":
    main()
