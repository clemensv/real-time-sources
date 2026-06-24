from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from confluent_kafka import Producer

from siri_core import (
    SUPPORTED_PROVIDERS,
    SiriClient,
    SiriClientGroup,
    build_kafka_config,
    load_feed_configs,
    load_state,
    parse_csv_tokens,
    parse_data_types,
    parse_kafka_connection_string,
    save_state,
)
from siri_producer_data import Operator, VehiclePosition
from siri_producer_kafka_producer.producer import OrgSiriKafkaEventProducer

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
        recorded_at_time=_parse_dt(position.recorded_at_time),  # type: ignore[arg-type]
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
    api: SiriClient,
    kafka_config: Dict[str, str],
    kafka_topic: str,
    polling_interval: int,
    *,
    state_file: str = "",
    once: bool = False,
) -> None:
    previous_items = load_state(state_file)
    producer = Producer(kafka_config)
    event_producer = OrgSiriKafkaEventProducer(producer, kafka_topic)
    known_operators: set[str] = set()

    while True:
        try:
            start_time = datetime.now(timezone.utc)
            snapshot = api.load_snapshot()
            operator_set = set(snapshot.operators)
            if not known_operators or operator_set != known_operators:
                for index, operator_ref in enumerate(snapshot.operators, start=1):
                    event_producer.send_org_siri_kafka_operator(
                        _feedurl=snapshot.operator_feed_urls[operator_ref],
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
                event_producer.send_org_siri_kafka_vehicle_position(
                    _feedurl=position.feedurl,
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
    parser = argparse.ArgumentParser(description="SIRI VehicleMonitoring → Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed operator metadata and vehicle positions as CloudEvents to Kafka")
    feed_parser.add_argument("--provider", choices=SUPPORTED_PROVIDERS, default=os.getenv("SIRI_PROVIDER", "bods"))
    feed_parser.add_argument("--siri-url", type=str, default=os.getenv("SIRI_URL"))
    feed_parser.add_argument("--api-key", type=str, default=os.getenv("SIRI_API_KEY") or os.getenv("BODS_API_KEY"))
    feed_parser.add_argument("--headers", type=str, default=os.getenv("SIRI_HEADERS"))
    feed_parser.add_argument("--et-client-name", type=str, default=os.getenv("SIRI_ET_CLIENT_NAME"))
    feed_parser.add_argument("--operators", type=str, default=os.getenv("SIRI_OPERATORS") or os.getenv("OPERATORS"))
    feed_parser.add_argument("--data-types", type=str, default=os.getenv("SIRI_DATA_TYPES", "vm"))
    feed_parser.add_argument("--siri-sources-file", type=str, default=os.getenv("SIRI_SOURCES_FILE", ""))
    feed_parser.add_argument("--siri-sources", type=str, default=os.getenv("SIRI_SOURCES", ""))
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC", "siri"))
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "30")))
    feed_parser.add_argument("--state-file", type=str, default=os.getenv("STATE_FILE", os.path.expanduser("~/.siri_state.json")))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    configs = load_feed_configs(
        sources_file=args.siri_sources_file,
        selector=args.siri_sources,
        provider=args.provider,
        siri_url=args.siri_url,
        api_key=args.api_key,
        operators=parse_csv_tokens(args.operators),
        data_types=parse_data_types(args.data_types),
        polling_interval=args.polling_interval,
        state_file=args.state_file,
        once=args.once,
        request_headers=args.headers,
        et_client_name=args.et_client_name,
    )
    config = configs[0]

    if args.connection_string:
        kafka_cfg = parse_kafka_connection_string(args.connection_string)
        entity_topic = kafka_cfg.pop("kafka_topic", None)
        bootstrap = kafka_cfg.get("bootstrap.servers") or args.kafka_bootstrap_servers
        topic = entity_topic or args.kafka_topic or "siri"
        user = kafka_cfg.get("sasl.username") or args.sasl_username
        pwd = kafka_cfg.get("sasl.password") or args.sasl_password
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic or "siri"
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

    clients = tuple(
        SiriClient(
            provider=item.provider,
            siri_url=item.siri_url,
            api_key=item.api_key,
            operators=item.operators,
            data_types=item.data_types,
            request_headers=item.request_headers,
        )
        for item in configs
    )
    api = clients[0] if len(clients) == 1 else SiriClientGroup(clients)
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
