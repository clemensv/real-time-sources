from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from confluent_kafka import Producer

from uk_bods_siri_core import BODS_BULK_URL, BodsSiriClient, FeedConfig, build_kafka_config, load_state, parse_kafka_connection_string, save_state
from uk_bods_siri_producer_data import Operator, VehiclePosition
from uk_bods_siri_producer_kafka_producer.producer import UkGovDftBodsKafkaEventProducer

logger = logging.getLogger(__name__)


def _build_operator(operator_ref: str) -> Operator:
    return Operator(operator_ref=operator_ref)


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(value) if value else None


def _build_vehicle_position(position) -> VehiclePosition:
    return VehiclePosition(
        operator_ref=position.operator_ref,
        vehicle_ref=position.vehicle_ref,
        line_ref=position.line_ref,
        direction_ref=position.direction_ref,
        published_line_name=position.published_line_name,
        origin_ref=position.origin_ref,
        origin_name=position.origin_name,
        destination_ref=position.destination_ref,
        destination_name=position.destination_name,
        longitude=position.longitude,
        latitude=position.latitude,
        bearing=position.bearing,
        recorded_at_time=_parse_dt(position.recorded_at_time),
        valid_until_time=_parse_dt(position.valid_until_time),
        block_ref=position.block_ref,
        vehicle_journey_ref=position.vehicle_journey_ref,
        origin_aimed_departure_time=_parse_dt(position.origin_aimed_departure_time),
        data_frame_ref=position.data_frame_ref,
        dated_vehicle_journey_ref=position.dated_vehicle_journey_ref,
        item_identifier=position.item_identifier,
    )


def _flush_or_raise(producer: Producer, context: str) -> None:
    remaining = producer.flush(timeout=120)
    if remaining != 0:
        raise RuntimeError(f"Kafka flush failed while emitting {context}; {remaining} message(s) still pending")


async def feed(
    api: BodsSiriClient,
    kafka_config: Dict[str, str],
    kafka_topic: str,
    polling_interval: int,
    *,
    state_file: str = "",
    once: bool = False,
) -> None:
    previous_items = load_state(state_file)
    producer = Producer(kafka_config)
    bods_producer = UkGovDftBodsKafkaEventProducer(producer, kafka_topic)
    known_operators: set[str] = set()

    while True:
        try:
            start_time = datetime.now(timezone.utc)
            snapshot = api.load_snapshot()
            operator_set = set(snapshot.operators)
            if not known_operators or operator_set != known_operators:
                for index, operator_ref in enumerate(snapshot.operators, start=1):
                    bods_producer.send_uk_gov_dft_bods_kafka_operator(
                        _feedurl=BODS_BULK_URL,
                        _operator_ref=operator_ref,
                        data=_build_operator(operator_ref),
                        flush_producer=False,
                    )
                    if index % 100 == 0:
                        _flush_or_raise(producer, "operator reference records")
                _flush_or_raise(producer, "operator reference records")
                known_operators = operator_set
                logger.info("Emitted %d operator reference events", len(snapshot.operators))

            next_items = dict(previous_items)
            emitted = 0
            for position in snapshot.vehicle_positions:
                if previous_items.get(position.identity) == position.item_identifier:
                    continue
                bods_producer.send_uk_gov_dft_bods_kafka_vehicle_position(
                    _feedurl=BODS_BULK_URL,
                    _operator_ref=position.operator_ref,
                    _vehicle_ref=position.vehicle_ref,
                    data=_build_vehicle_position(position),
                    flush_producer=False,
                )
                next_items[position.identity] = position.item_identifier
                emitted += 1
            _flush_or_raise(producer, "vehicle position records")
            previous_items = next_items
            save_state(state_file, previous_items)

            end_time = datetime.now(timezone.utc)
            effective = max(0.0, polling_interval - (end_time - start_time).total_seconds())
            logger.info(
                "Emitted %d vehicle positions from %d operators in %.2f seconds. Sleeping until %s.",
                emitted,
                len(snapshot.operators),
                (end_time - start_time).total_seconds(),
                (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
            )
            if once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            if effective > 0:
                await asyncio.sleep(effective)
        except KeyboardInterrupt:
            logger.info("Exiting...")
            break
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error occurred: %s", exc)
            if once:
                raise
            await asyncio.sleep(polling_interval)
    producer.flush(timeout=120)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="UK BODS SIRI-VM → Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed operator metadata and vehicle positions as CloudEvents to Kafka")
    feed_parser.add_argument("--bods-api-key", type=str, default=os.getenv("BODS_API_KEY"), help="BODS API key")
    feed_parser.add_argument("--operators", type=str, default=os.getenv("OPERATORS"), help="Optional comma-separated NOC filter")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC", "uk-bods-siri"))
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "30")))
    feed_parser.add_argument("--state-file", type=str, default=os.getenv("STATE_FILE", os.path.expanduser("~/.uk_bods_siri_state.json")))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    operators = {token.strip() for token in (args.operators or "").split(",") if token.strip()} or None
    config = FeedConfig.from_env(
        bods_api_key=args.bods_api_key,
        polling_interval=args.polling_interval,
        operators=operators,
        state_file=args.state_file,
        once=args.once,
    )

    if args.connection_string:
        kafka_cfg = parse_kafka_connection_string(args.connection_string)
        entity_topic = kafka_cfg.pop("kafka_topic", None)
        bootstrap = kafka_cfg.get("bootstrap.servers") or args.kafka_bootstrap_servers
        topic = entity_topic or args.kafka_topic or "uk-bods-siri"
        user = kafka_cfg.get("sasl.username") or args.sasl_username
        pwd = kafka_cfg.get("sasl.password") or args.sasl_password
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic or "uk-bods-siri"
        user = args.sasl_username
        pwd = args.sasl_password

    if not bootstrap:
        print("Error: Kafka bootstrap servers must be provided either through CLI or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config = build_kafka_config(
        bootstrap_servers=bootstrap,
        sasl_username=user,
        sasl_password=pwd,
        tls_enabled=tls_enabled,
    )

    api = BodsSiriClient(api_key=config.bods_api_key, operators=config.operators)
    asyncio.run(
        feed(
            api,
            kafka_config,
            topic,
            config.polling_interval,
            state_file=config.state_file,
            once=config.once,
        )
    )


if __name__ == "__main__":
    main()
