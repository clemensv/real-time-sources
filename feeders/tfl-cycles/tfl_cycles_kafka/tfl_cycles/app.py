"""Kafka feeder application for TfL Santander Cycles (BikePoint).

Drives the upstream TfL BikePoint poller from :mod:`tfl_cycles_core` and emits
CloudEvents through the generated Kafka producer. Reference (StationInformation)
events are emitted first each cycle -- on startup, on any change to a station's
identity/location/capacity/lifecycle fields, and on a periodic refresh -- then
StationStatus telemetry is emitted for stations whose availability changed.
Both event types are keyed by the stable BikePoint ``station_id``.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from confluent_kafka import Producer

from tfl_cycles_core import (
    FEED_URL_ROOT,
    ParsedStation,
    TfLCyclesAPI,
    build_kafka_config,
    load_state,
    parse_bikepoint,
    parse_kafka_connection_string,
    save_state,
)
from tfl_cycles_producer_data import StationInformation, StationStatus
from tfl_cycles_producer_kafka_producer.producer import UKGovTfLCyclesKafkaStationsEventProducer

logger = logging.getLogger(__name__)


def _build_info(p: ParsedStation) -> StationInformation:
    return StationInformation(
        station_id=p.station_id,
        name=p.name,
        lat=float(p.lat) if p.lat is not None else 0.0,
        lon=float(p.lon) if p.lon is not None else 0.0,
        terminal_name=p.terminal_name,
        capacity=p.capacity,
        temporary=p.temporary,
        install_date=p.install_date,
        removal_date=p.removal_date,
    )


def _build_status(p: ParsedStation) -> StationStatus:
    return StationStatus(
        station_id=p.station_id,
        num_bikes_available=p.num_bikes_available if p.num_bikes_available is not None else 0,
        num_standard_bikes_available=p.num_standard_bikes_available,
        num_ebikes_available=p.num_ebikes_available,
        num_empty_docks=p.num_empty_docks if p.num_empty_docks is not None else 0,
        num_docks=p.num_docks,
        is_installed=p.is_installed if p.is_installed is not None else False,
        is_locked=p.is_locked if p.is_locked is not None else False,
        modified=p.modified,
    )


def feed(
    api: TfLCyclesAPI,
    kafka_config: Dict[str, str],
    kafka_topic: str,
    polling_interval: int,
    state_file: str = "",
    once: bool = False,
    reference_refresh_interval: int = 3600,
) -> None:
    """Feed BikePoint reference and availability CloudEvents to Kafka."""

    previous_status: Dict[str, Any] = load_state(state_file)
    previous_info: Dict[str, Any] = {}
    last_ref_emit = 0.0

    raw_producer = Producer(kafka_config)
    producer = UKGovTfLCyclesKafkaStationsEventProducer(raw_producer, kafka_topic)

    logger.info(
        "Starting TfL Santander Cycles feed to Kafka topic %s at bootstrap servers %s",
        kafka_topic,
        kafka_config.get("bootstrap.servers"),
    )

    while True:
        try:
            start_time = datetime.now(timezone.utc)
            bikepoints = api.list_bikepoints()
            parsed = [parse_bikepoint(bp) for bp in bikepoints]
            now_ts = time.time()
            reference_due = (now_ts - last_ref_emit) >= reference_refresh_interval

            info_count = 0
            for p in parsed:
                signature = p.info_signature()
                if reference_due or previous_info.get(p.station_id) != signature:
                    try:
                        producer.send_uk_gov_tf_l_cycles_kafka_station_information(
                            _feedurl=f"{FEED_URL_ROOT}/BikePoint/{p.station_id}",
                            _station_id=p.station_id,
                            data=_build_info(p),
                            flush_producer=False,
                        )
                        info_count += 1
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error sending station info for %s: %s", p.station_id, e)
                    previous_info[p.station_id] = signature
            if reference_due:
                last_ref_emit = now_ts

            status_count = 0
            for p in parsed:
                signature = p.status_signature()
                if previous_status.get(p.station_id) != signature:
                    try:
                        producer.send_uk_gov_tf_l_cycles_kafka_station_status(
                            _feedurl=f"{FEED_URL_ROOT}/BikePoint/{p.station_id}",
                            _station_id=p.station_id,
                            data=_build_status(p),
                            flush_producer=False,
                        )
                        status_count += 1
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error sending station status for %s: %s", p.station_id, e)
                    previous_status[p.station_id] = signature

            raw_producer.flush()
            save_state(state_file, previous_status)

            end_time = datetime.now(timezone.utc)
            effective = max(0, polling_interval - (end_time - start_time).total_seconds())
            logger.info(
                "Sent %s station info + %s status events in %.1fs. Waiting until %s.",
                info_count,
                status_count,
                (end_time - start_time).total_seconds(),
                (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
            )
            if once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            if effective > 0:
                time.sleep(effective)
        except KeyboardInterrupt:
            logger.info("Exiting...")
            break
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error occurred: %s", e)
            logger.info("Retrying in %d seconds...", polling_interval)
            time.sleep(polling_interval)
    raw_producer.flush()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TfL Santander Cycles -> Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed BikePoint reference and availability CloudEvents to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str,
                             default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                             help="Comma separated list of Kafka bootstrap servers")
    feed_parser.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"),
                             help="Kafka topic to send messages to")
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"),
                             help="Username for SASL PLAIN authentication")
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"),
                             help="Password for SASL PLAIN authentication")
    feed_parser.add_argument("-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"),
                             help="Microsoft Event Hubs or Fabric Event Stream connection string")
    polling_interval_default = int(os.getenv("POLLING_INTERVAL", "60"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=polling_interval_default,
                             help="Polling interval in seconds")
    feed_parser.add_argument("--reference-refresh-interval", type=int,
                             default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600")),
                             help="Seconds between full re-emissions of station reference data")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.tfl_cycles_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle (also via ONCE_MODE env var).")
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    if args.connection_string:
        cfg = parse_kafka_connection_string(args.connection_string)
        bootstrap = cfg.get("bootstrap.servers")
        topic = cfg.get("kafka_topic") or args.kafka_topic
        user = cfg.get("sasl.username")
        pwd = cfg.get("sasl.password")
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic
        user = args.sasl_username
        pwd = args.sasl_password

    if not bootstrap:
        print("Error: Kafka bootstrap servers must be provided either through CLI or connection string.")
        sys.exit(1)
    if not topic:
        print("Error: Kafka topic must be provided either through CLI or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config = build_kafka_config(
        bootstrap_servers=bootstrap,
        sasl_username=user,
        sasl_password=pwd,
        tls_enabled=tls_enabled,
    )

    api = TfLCyclesAPI()
    feed(api, kafka_config, topic, args.polling_interval, args.state_file, args.once,
         args.reference_refresh_interval)


if __name__ == "__main__":
    main()
