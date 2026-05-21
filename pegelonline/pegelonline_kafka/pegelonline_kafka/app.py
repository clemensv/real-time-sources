"""Kafka feeder application.

Drives the upstream PegelOnline poller from :mod:`pegelonline_core` and emits
CloudEvents through the generated Kafka producer. The CLI surface is
intentionally identical to what the pre-split single-file bridge exposed so
that container deployments and Fabric pipelines do not need to relearn their
environment variables.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from confluent_kafka import Producer

from pegelonline_core import (
    FEED_URL_ROOT,
    PegelOnlineAPI,
    build_kafka_config,
    load_state,
    parse_kafka_connection_string,
    save_state,
)
from pegelonline_producer_data.de.wsv.pegelonline.currentmeasurement import CurrentMeasurement
from pegelonline_producer_data.de.wsv.pegelonline.station import Station
from pegelonline_producer_data.de.wsv.pegelonline.water import Water
from pegelonline_producer_kafka_producer.producer import DeWsvPegelonlineKafkaEventProducer

logger = logging.getLogger(__name__)


def _build_station(raw: Dict[str, Any]) -> Station:
    water = raw.get("water") or {}
    return Station(
        station_id=raw.get("uuid"),
        number=raw.get("number"),
        shortname=raw.get("shortname"),
        longname=raw.get("longname"),
        km=raw.get("km") if raw.get("km") is not None else -1,
        agency=raw.get("agency"),
        longitude=raw.get("longitude") if raw.get("longitude") is not None else -1,
        latitude=raw.get("latitude") if raw.get("latitude") is not None else -1,
        water=Water(shortname=water.get("shortname"), longname=water.get("longname")),
    )


def _build_measurement(station_id: str, raw: Dict[str, Any]) -> CurrentMeasurement:
    return CurrentMeasurement(
        station_id=station_id,
        timestamp=raw["timestamp"],
        value=raw["value"],
        stateMnwMhw=raw["stateMnwMhw"],
        stateNswHsw=raw["stateNswHsw"],
    )


async def feed(
    api: PegelOnlineAPI,
    kafka_config: Dict[str, str],
    kafka_topic: str,
    polling_interval: int,
    state_file: str = "",
    once: bool = False,
) -> None:
    """Feed stations and measurements as CloudEvents to Kafka."""

    previous_readings: Dict[str, Dict[str, Any]] = load_state(state_file)

    producer = Producer(kafka_config)
    pegelonline_producer = DeWsvPegelonlineKafkaEventProducer(producer, kafka_topic)

    logger.info(
        "Starting to feed stations to Kafka topic %s at bootstrap servers %s",
        kafka_topic,
        kafka_config.get("bootstrap.servers"),
    )

    stations = api.list_stations()
    for station in stations:
        station_data = _build_station(station)
        pegelonline_producer.send_de_wsv_pegelonline_kafka_station(
            _feedurl=f"{FEED_URL_ROOT}/stations/{station['shortname']}",
            _station_id=station["uuid"],
            data=station_data,
            flush_producer=False,
        )
    producer.flush()
    logger.info("Finished sending station data updates to Kafka topic %s", kafka_topic)

    while True:
        try:
            count = 0
            start_time = datetime.now(timezone.utc)
            measurements = api.get_water_levels()
            for station_id, measurement in measurements.items():
                prior = previous_readings.get(station_id)
                if prior is None or measurement.get("timestamp") != prior.get("timestamp"):
                    count += 1
                    logger.debug("Sending current measurement for station %s", station_id)
                    try:
                        pegelonline_producer.send_de_wsv_pegelonline_kafka_current_measurement(
                            _feedurl=f"{FEED_URL_ROOT}/stations/{station_id}/W/currentmeasurement.json",
                            _station_id=station_id,
                            data=_build_measurement(station_id, measurement),
                            flush_producer=False,
                        )
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error sending to kafka: %s", e)
                    previous_readings[station_id] = measurement
            producer.flush()
            end_time = datetime.now(timezone.utc)
            effective = max(0, polling_interval - (end_time - start_time).total_seconds())
            logger.info(
                "Sent %s current measurements in %s seconds. Now waiting until %s.",
                count,
                (end_time - start_time).total_seconds(),
                (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
            )
            save_state(state_file, previous_readings)
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
    producer.flush()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PegelOnline → Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed stations and updates as CloudEvents to Kafka")
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
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.pegelonline_state.json")))
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

    api = PegelOnlineAPI()
    asyncio.run(feed(api, kafka_config, topic, args.polling_interval, args.state_file, args.once))


if __name__ == "__main__":
    main()
