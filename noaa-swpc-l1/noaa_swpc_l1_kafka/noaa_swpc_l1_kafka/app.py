"""Kafka feeder application.

Polls the NOAA SWPC propagated-solar-wind endpoint and emits one CloudEvent
per new row into a single Kafka topic. Partition key = spacecraft id, so
each spacecraft's stream is partition-ordered.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

from confluent_kafka import Producer

from noaa_swpc_l1_core import (
    FEED_URL,
    PropagatedSolarWindRow,
    SwpcL1API,
    build_kafka_config,
    load_state,
    parse_kafka_connection_string,
    save_state,
)
from noaa_swpc_l1_producer_data.gov.noaa.swpc.l1.propagatedsolarwind import (
    PropagatedSolarWind,
)
from noaa_swpc_l1_producer_data.gov.noaa.swpc.l1.spacecraftenum import SpacecraftEnum
from noaa_swpc_l1_producer_kafka_producer.producer import (
    GovNoaaSwpcL1KafkaEventProducer,
)

logger = logging.getLogger(__name__)


def _row_to_data(row: PropagatedSolarWindRow) -> PropagatedSolarWind:
    """Map the normalized row to the generated dataclass."""
    return PropagatedSolarWind(
        spacecraft=SpacecraftEnum(row.spacecraft),
        time_tag=row.time_tag,
        propagated_time_tag=row.propagated_time_tag,
        speed=row.speed,
        density=row.density,
        temperature=row.temperature,
        bx=row.bx,
        by=row.by,
        bz=row.bz,
        bt=row.bt,
        vx=row.vx,
        vy=row.vy,
        vz=row.vz,
    )


async def feed(
    api: SwpcL1API,
    kafka_config: dict,
    kafka_topic: str,
    *,
    spacecraft: str,
    polling_interval: int,
    state_file: str = "",
    once: bool = False,
    backfill_minutes: int = 5,
) -> None:
    """Feed propagated-solar-wind observations as CloudEvents to Kafka."""

    state = load_state(state_file)
    last_seen_iso: Optional[str] = state.get("last_time_tag")
    last_seen: Optional[datetime]
    if last_seen_iso:
        try:
            last_seen = datetime.fromisoformat(last_seen_iso)
        except ValueError:
            last_seen = None
    else:
        last_seen = None
    if last_seen is None:
        last_seen = datetime.now(timezone.utc) - timedelta(minutes=backfill_minutes)
        logger.info(
            "No prior state; starting from %s (last %d minutes)",
            last_seen.isoformat(),
            backfill_minutes,
        )

    producer = Producer(kafka_config)
    swpc_producer = GovNoaaSwpcL1KafkaEventProducer(
        producer, kafka_topic, content_mode="binary"
    )

    logger.info(
        "Starting Kafka feed to topic %s (bootstrap=%s, spacecraft=%s)",
        kafka_topic,
        kafka_config.get("bootstrap.servers"),
        spacecraft,
    )

    while True:
        try:
            start_time = datetime.now(timezone.utc)
            new_rows = list(api.fetch_new_rows(spacecraft, since=last_seen))
            count = 0
            for row in new_rows:
                try:
                    swpc_producer.send_gov_noaa_swpc_l1_kafka_propagated_solar_wind(
                        _feedurl=FEED_URL,
                        _spacecraft=row.spacecraft,
                        _time_tag=row.time_tag.isoformat(),
                        data=_row_to_data(row),
                        flush_producer=False,
                    )
                    count += 1
                    last_seen = row.time_tag
                except Exception as e:  # pylint: disable=broad-except
                    logger.error("Error sending row %s: %s", row.time_tag, e)
            producer.flush()
            if last_seen is not None:
                save_state(state_file, {"last_time_tag": last_seen.isoformat()})

            end_time = datetime.now(timezone.utc)
            effective = max(
                0,
                polling_interval - (end_time - start_time).total_seconds(),
            )
            logger.info(
                "Sent %s rows in %.2fs (last_time_tag=%s). Sleeping %.1fs.",
                count,
                (end_time - start_time).total_seconds(),
                last_seen.isoformat() if last_seen else "<none>",
                effective,
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
            logger.error("Polling error: %s — retrying in %ds", e, polling_interval)
            time.sleep(polling_interval)
    producer.flush()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NOAA SWPC L1 propagated solar wind → Apache Kafka bridge."
    )
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser(
        "feed", help="Feed propagated-solar-wind rows as CloudEvents to Kafka"
    )
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma separated list of Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        "--kafka-topic",
        type=str,
        default=os.getenv("KAFKA_TOPIC", "noaa-swpc-l1"),
        help="Kafka topic to send messages to (default: noaa-swpc-l1)",
    )
    feed_parser.add_argument(
        "--sasl-username",
        type=str,
        default=os.getenv("SASL_USERNAME"),
        help="Username for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "--sasl-password",
        type=str,
        default=os.getenv("SASL_PASSWORD"),
        help="Password for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "-c",
        "--connection-string",
        type=str,
        default=os.getenv("CONNECTION_STRING"),
        help="Microsoft Event Hubs or Fabric Event Stream connection string",
    )
    polling_interval_default = int(os.getenv("POLLING_INTERVAL", "60"))
    feed_parser.add_argument(
        "-i",
        "--polling-interval",
        type=int,
        default=polling_interval_default,
        help="Polling interval in seconds (default: 60)",
    )
    feed_parser.add_argument(
        "--spacecraft",
        type=str,
        default=os.getenv("SPACECRAFT", "dscovr"),
        choices=["dscovr", "ace"],
        help="Source spacecraft id stamped onto every event (default: dscovr)",
    )
    feed_parser.add_argument(
        "--backfill-minutes",
        type=int,
        default=int(os.getenv("BACKFILL_MINUTES", "5")),
        help="On cold start (no state file), how many recent minutes to emit (default: 5)",
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv(
            "STATE_FILE", os.path.expanduser("~/.noaa_swpc_l1_state.json")
        ),
    )
    feed_parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle (also via ONCE_MODE env var).",
    )
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
        print(
            "Error: Kafka bootstrap servers must be provided via CLI or connection string."
        )
        sys.exit(1)
    if not topic:
        print("Error: Kafka topic must be provided via CLI or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in (
        "false",
        "0",
        "no",
    )
    kafka_config = build_kafka_config(
        bootstrap_servers=bootstrap,
        sasl_username=user,
        sasl_password=pwd,
        tls_enabled=tls_enabled,
    )

    api = SwpcL1API()
    asyncio.run(
        feed(
            api,
            kafka_config,
            topic,
            spacecraft=args.spacecraft,
            polling_interval=args.polling_interval,
            state_file=args.state_file,
            once=args.once,
            backfill_minutes=args.backfill_minutes,
        )
    )


if __name__ == "__main__":
    main()
