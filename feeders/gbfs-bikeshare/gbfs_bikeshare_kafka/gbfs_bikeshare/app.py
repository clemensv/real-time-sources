from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import Optional

from confluent_kafka import Producer

from gbfs_bikeshare_core import build_kafka_config, build_offline_client_and_feeds, load_state, parse_bool, parse_feed_configuration, parse_kafka_connection_string, save_state
from gbfs_bikeshare_core.acquisition import (
    GbfsSourceClient,
    StationInformationRecord,
    StationStatusRecord,
    SystemInformationRecord,
    FreeBikeStatusRecord,
    discover_sources,
    should_publish_free_bike_status,
    should_publish_station_status,
)
from gbfs_bikeshare_producer_data import FreeBikeStatus, StationInformation, StationStatus, SystemInformation
from gbfs_bikeshare_producer_kafka_producer.producer import (
    OrgGbfsKafkaStationsEventProducer as OrgGbfsStationsEventProducer,
    OrgGbfsKafkaSystemEventProducer as OrgGbfsSystemEventProducer,
    OrgGbfsKafkaFreeBikesEventProducer as OrgGbfsFreeBikesEventProducer,
)

logger = logging.getLogger(__name__)
DEFAULT_STATE_FILE = os.path.expanduser("~/.gbfs_bikeshare_state.json")


def _build_system_information(record: SystemInformationRecord) -> SystemInformation:
    return SystemInformation(
        system_id=record.system_id,
        name=record.name,
        operator=record.operator,
        url=record.url,
        timezone=record.timezone,
        language=record.language,
        phone_number=record.phone_number,
    )


def _build_station_information(record: StationInformationRecord) -> StationInformation:
    return StationInformation(
        system_id=record.system_id,
        station_id=record.station_id,
        name=record.name,
        short_name=record.short_name,
        lat=record.lat,
        lon=record.lon,
        capacity=record.capacity,
        region_id=record.region_id,
        address=record.address,
        post_code=record.post_code,
    )


def _build_station_status(record: StationStatusRecord) -> StationStatus:
    return StationStatus(
        system_id=record.system_id,
        station_id=record.station_id,
        num_bikes_available=record.num_bikes_available,
        num_docks_available=record.num_docks_available,
        num_ebikes_available=record.num_ebikes_available,
        is_installed=record.is_installed,
        is_renting=record.is_renting,
        is_returning=record.is_returning,
        last_reported=record.last_reported,
    )


def _build_free_bike_status(record: FreeBikeStatusRecord) -> FreeBikeStatus:
    return FreeBikeStatus(
        system_id=record.system_id,
        bike_id=record.bike_id,
        lat=record.lat,
        lon=record.lon,
        is_reserved=record.is_reserved,
        is_disabled=record.is_disabled,
        vehicle_type_id=record.vehicle_type_id,
        current_range_meters=record.current_range_meters,
        last_reported=record.last_reported,
    )


def feed(args: argparse.Namespace) -> None:
    mock_mode = getattr(args, "mock", False)
    configured_feeds = (
        [] if mock_mode else parse_feed_configuration(args.gbfs_feeds, args.gbfs_system_ids)
    )
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

    kafka_config = build_kafka_config(
        bootstrap_servers=bootstrap,
        sasl_username=sasl_username,
        sasl_password=sasl_password,
        tls_enabled=os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("0", "false", "no"),
    )
    producer = Producer(kafka_config)
    system_producer = OrgGbfsSystemEventProducer(producer, topic)
    stations_producer = OrgGbfsStationsEventProducer(producer, topic)
    free_bikes_producer = OrgGbfsFreeBikesEventProducer(producer, topic)
    state = load_state(args.state_file)
    if mock_mode:
        logger.info("--mock mode: using deterministic offline GBFS corpus (no network access)")
        client, configured_feeds = build_offline_client_and_feeds()
        args.once = True
    else:
        client = GbfsSourceClient()
    sources = discover_sources(client, configured_feeds)
    if not sources:
        raise SystemExit("No GBFS feeds could be discovered successfully.")

    logger.info("Discovered %d GBFS system(s)", len(sources))
    last_reference_refresh = 0.0
    reference_refresh = max(300, args.reference_refresh_interval)

    while True:
        cycle_started = time.time()
        if last_reference_refresh == 0.0 or cycle_started - last_reference_refresh >= reference_refresh:
            for source in sources:
                try:
                    system_payload = client.fetch_system_information(source)
                    if system_payload is not None:
                        system_record, feed_url = system_payload
                        system_producer.send_org_gbfs_kafka_system_information(
                            _feed_url=feed_url,
                            _system_id=system_record.system_id,
                            data=_build_system_information(system_record),
                            flush_producer=False,
                        )
                    stations, station_feed_url = client.fetch_station_information(source)
                    if station_feed_url:
                        for station in stations:
                            stations_producer.send_org_gbfs_kafka_station_information(
                                _feed_url=station_feed_url,
                                _system_id=station.system_id,
                                _station_id=station.station_id,
                                data=_build_station_information(station),
                                flush_producer=False,
                            )
                except Exception as exc:  # pylint: disable=broad-except
                    logger.warning("Reference refresh failed for %s: %s", source.autodiscovery_url, exc)
            producer.flush()
            last_reference_refresh = cycle_started

        for source in sources:
            try:
                station_statuses, station_status_feed_url, _ = client.fetch_station_status(source)
                if station_status_feed_url:
                    for status in station_statuses:
                        if not should_publish_station_status(status, state):
                            continue
                        stations_producer.send_org_gbfs_kafka_station_status(
                            _feed_url=station_status_feed_url,
                            _system_id=status.system_id,
                            _station_id=status.station_id,
                            data=_build_station_status(status),
                            flush_producer=False,
                        )
                free_bikes, free_bike_feed_url, _ = client.fetch_free_bike_status(source)
                if free_bike_feed_url:
                    for bike in free_bikes:
                        if not should_publish_free_bike_status(bike, state):
                            continue
                        free_bikes_producer.send_org_gbfs_kafka_free_bike_status(
                            _feed_url=free_bike_feed_url,
                            _system_id=bike.system_id,
                            _bike_id=bike.bike_id,
                            data=_build_free_bike_status(bike),
                            flush_producer=False,
                        )
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning("Telemetry poll failed for %s: %s", source.autodiscovery_url, exc)
        producer.flush()
        save_state(args.state_file, state)
        if args.once:
            logger.info("--once mode: exiting after first polling cycle")
            return
        elapsed = time.time() - cycle_started
        sleep_seconds = max(1, args.poll_interval - int(elapsed))
        logger.info("Polling cycle completed in %.1fs; sleeping %ss", elapsed, sleep_seconds)
        time.sleep(sleep_seconds)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GBFS bikeshare -> Kafka bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Poll GBFS feeds and publish CloudEvents to Kafka")
    feed_parser.add_argument("--gbfs-feeds", default=os.getenv("GBFS_FEEDS"), help="Comma-separated GBFS auto-discovery URLs, @file, or path to a file containing URLs")
    feed_parser.add_argument("--gbfs-system-ids", default=os.getenv("GBFS_SYSTEM_IDS"), help="Optional comma-separated system-id overrides aligned with GBFS_FEEDS")
    feed_parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"), help="Kafka bootstrap servers")
    feed_parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC", "gbfs-bikeshare"), help="Kafka topic name")
    feed_parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"), help="SASL PLAIN username")
    feed_parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"), help="SASL PLAIN password")
    feed_parser.add_argument("--connection-string", default=os.getenv("CONNECTION_STRING"), help="Kafka/Event Hubs/Fabric connection string")
    feed_parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL", "60")), help="Polling interval in seconds")
    feed_parser.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600")), help="Reference-data refresh interval in seconds")
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE), help="Path to the JSON dedupe state file")
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"), help="Exit after one polling cycle")
    feed_parser.add_argument("--mock", action="store_true", default=parse_bool(os.getenv("GBFS_MOCK"), default=False), help="Emit a deterministic offline GBFS corpus once (no network); for CI flow tests")
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
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("GBFS Kafka bridge failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
