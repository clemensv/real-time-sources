from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import Optional

from confluent_kafka import Producer

from openaq_core import OpenAQClient, build_kafka_config, build_mock_client, load_state, parse_bool, parse_csv, parse_kafka_connection_string, save_state, should_publish_measurement, slug_segment
from openaq_core.acquisition import LocationRecord, MeasurementRecord, SensorRecord
from openaq_producer_data import Location, Measurement, Sensor
from openaq_producer_data.org.openaq.parameternameenum import ParameterNameenum
from openaq_producer_kafka_producer.producer import OrgOpenaqLocationsKafkaEventProducer, OrgOpenaqSensorsKafkaEventProducer

logger = logging.getLogger(__name__)
DEFAULT_STATE_FILE = os.path.expanduser("~/.openaq_state.json")


def _enum(name: str) -> ParameterNameenum:
    return ParameterNameenum(name)


def build_location(r: LocationRecord) -> Location:
    return Location(**r.__dict__)


def build_sensor(r: SensorRecord) -> Sensor:
    data = dict(r.__dict__)
    data["parameter_name"] = _enum(r.parameter_name)
    return Sensor(**data)


def build_measurement(r: MeasurementRecord) -> Measurement:
    data = dict(r.__dict__)
    data["parameter_name"] = _enum(r.parameter_name)
    return Measurement(**data)


def _configured_ids(value: Optional[str]) -> list[int]:
    return [int(v) for v in parse_csv(value)]


def feed(args: argparse.Namespace) -> None:
    if args.connection_string:
        cfg = parse_kafka_connection_string(args.connection_string)
        bootstrap = cfg.get("bootstrap.servers")
        topic = cfg.get("kafka_topic") or args.kafka_topic
        sasl_username = cfg.get("sasl.username")
        sasl_password = cfg.get("sasl.password")
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password
    if not bootstrap:
        raise SystemExit("Kafka bootstrap servers must be provided through CLI args or CONNECTION_STRING.")
    if not topic:
        raise SystemExit("Kafka topic must be provided through CLI args or CONNECTION_STRING.")
    kafka_config = build_kafka_config(bootstrap, sasl_username, sasl_password, parse_bool(os.getenv("KAFKA_ENABLE_TLS"), True))
    producer = Producer(kafka_config)
    location_producer = OrgOpenaqLocationsKafkaEventProducer(producer, topic)
    sensor_producer = OrgOpenaqSensorsKafkaEventProducer(producer, topic)
    state = load_state(args.state_file)
    client = build_mock_client() if args.mock else OpenAQClient(args.openaq_api_key)
    if args.mock:
        args.once = True
    countries = [c.upper() for c in parse_csv(args.openaq_countries)]
    location_ids = _configured_ids(args.openaq_locations)
    last_reference_refresh = 0.0
    reference_refresh = max(300, args.reference_refresh_interval)
    locations_cache: list[LocationRecord] = []
    sensors_cache: dict[int, dict[int, SensorRecord]] = {}
    while True:
        cycle_started = time.time()
        if last_reference_refresh == 0.0 or cycle_started - last_reference_refresh >= reference_refresh:
            refreshed_locations: list[LocationRecord] = []
            refreshed_sensors: dict[int, dict[int, SensorRecord]] = {}
            try:
                for location in client.iter_locations(countries, location_ids, args.openaq_bbox, args.page_limit, args.max_pages):
                    refreshed_locations.append(location)
                    location_producer.send_org_openaq_kafka_location(_location_id=str(location.location_id), data=build_location(location), flush_producer=False)
                    sensor_map: dict[int, SensorRecord] = {}
                    for sensor in client.sensors_for_location(location):
                        sensor_map[sensor.sensor_id] = sensor
                        sensor_producer.send_org_openaq_kafka_sensor(_location_id=str(sensor.location_id), _sensor_id=str(sensor.sensor_id), data=build_sensor(sensor), flush_producer=False)
                    refreshed_sensors[location.location_id] = sensor_map
                location_producer.flush(timeout=120)
                sensor_producer.flush(timeout=120)
                locations_cache = refreshed_locations
                sensors_cache = refreshed_sensors
                last_reference_refresh = cycle_started
                logger.info("Refreshed %d OpenAQ locations and %d sensors", len(locations_cache), sum(len(s) for s in sensors_cache.values()))
            except Exception as exc:
                logger.warning("OpenAQ reference refresh failed: %s", exc)
                if not locations_cache:
                    raise
        for location in locations_cache:
            try:
                for measurement in client.latest_for_location(location, sensors_cache.get(location.location_id, {})):
                    if not should_publish_measurement(measurement, state):
                        continue
                    sensor_producer.send_org_openaq_kafka_measurement(_location_id=str(measurement.location_id), _sensor_id=str(measurement.sensor_id), data=build_measurement(measurement), flush_producer=False)
            except Exception as exc:
                logger.warning("OpenAQ latest poll failed for location %s: %s", location.location_id, exc)
        sensor_producer.flush(timeout=120)
        save_state(args.state_file, state)
        if args.once:
            logger.info("--once mode: exiting after first OpenAQ polling cycle")
            return
        elapsed = time.time() - cycle_started
        time.sleep(max(1, args.poll_interval - int(elapsed)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenAQ global air quality -> Kafka bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Poll OpenAQ API v3 and publish CloudEvents to Kafka")
    feed_parser.add_argument("--openaq-api-key", default=os.getenv("OPENAQ_API_KEY"), help="OpenAQ API key sent in X-API-Key header")
    feed_parser.add_argument("--openaq-countries", default=os.getenv("OPENAQ_COUNTRIES", "US"), help="Comma-separated ISO 3166-1 alpha-2 countries to poll")
    feed_parser.add_argument("--openaq-locations", default=os.getenv("OPENAQ_LOCATIONS"), help="Comma-separated OpenAQ location ids; overrides country discovery")
    feed_parser.add_argument("--openaq-bbox", default=os.getenv("OPENAQ_BBOX"), help="Optional WGS84 bbox minLon,minLat,maxLon,maxLat")
    feed_parser.add_argument("--page-limit", type=int, default=int(os.getenv("OPENAQ_PAGE_LIMIT", "25")))
    feed_parser.add_argument("--max-pages", type=int, default=int(os.getenv("OPENAQ_MAX_PAGES", "1")))
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC", "openaq"))
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("--connection-string", default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL", "900")))
    feed_parser.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "21600")))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument("--once", action="store_true", default=parse_bool(os.getenv("ONCE_MODE"), False))
    feed_parser.add_argument("--mock", action="store_true", default=parse_bool(os.getenv("OPENAQ_MOCK"), False), help="Emit deterministic synthetic OpenAQ events without network/API key")
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return
    try:
        feed(args)
    except KeyboardInterrupt:
        logger.info("Interrupted, exiting.")
    except Exception as exc:
        logger.error("OpenAQ Kafka bridge failed: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()

