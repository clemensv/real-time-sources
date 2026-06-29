"""HSL HFP -> Apache Kafka bridge.

Subscribes to the HSL HFP firehose via :mod:`hsl_hfp_core`, emits the operator,
route, and stop reference events first, then streams the vehicle, traffic-light,
and driver/block telemetry as CloudEvents into a single Kafka topic. Each event
keeps the upstream HFP payload verbatim; the CloudEvents envelope adds the
``fi.hsl.hfp.*`` / ``fi.hsl.gtfs.*`` type and the ``{operator_id}/{vehicle_number}``
subject and Kafka key.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Any, Dict, Optional

from confluent_kafka import Producer

from .config import (
    HFP_FEED_URL,
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)
from .runner import BridgeRunner
from hsl_hfp_producer_data import (
    DriverBlockEvent,
    Operator,
    Route,
    Stop,
    TrafficLightEvent,
    VehicleEvent,
)
from hsl_hfp_producer_kafka_producer.producer import (
    FiHslGtfsOperatorEventProducer,
    FiHslGtfsRouteEventProducer,
    FiHslGtfsStopEventProducer,
    FiHslHfpEventProducer,
)

logger = logging.getLogger(__name__)


class KafkaSink:
    """Builds Kafka producer data classes and emits them as CloudEvents.

    The manifest splits the four event identities -- vehicle telemetry plus the
    operator / route / stop reference catalogues -- into four Kafka endpoints,
    each with its own partition-key template, so ``xrcg`` emits one producer
    class per identity. They all share the single underlying confluent-kafka
    ``Producer`` and the single ``hsl-hfp`` topic; only the key template differs.
    """

    def __init__(self, producer: Producer, topic: str, content_mode: str, feed_url: str) -> None:
        self._producer = producer
        self._tele = FiHslHfpEventProducer(producer, topic, content_mode)  # type: ignore[arg-type]
        self._operator = FiHslGtfsOperatorEventProducer(producer, topic, content_mode)  # type: ignore[arg-type]
        self._route = FiHslGtfsRouteEventProducer(producer, topic, content_mode)  # type: ignore[arg-type]
        self._stop = FiHslGtfsStopEventProducer(producer, topic, content_mode)  # type: ignore[arg-type]
        self._feed = feed_url

    def send_operator(self, operator_id: str, kwargs: Dict[str, Any]) -> None:
        self._operator.send_fi_hsl_gtfs_operator_operator(
            _feedurl=self._feed, _operator_id=operator_id, data=Operator(**kwargs), flush_producer=False)

    def send_route(self, route_id: str, kwargs: Dict[str, Any]) -> None:
        self._route.send_fi_hsl_gtfs_route_route(
            _feedurl=self._feed, _route_id=route_id, data=Route(**kwargs), flush_producer=False)

    def send_stop(self, stop_id: str, kwargs: Dict[str, Any]) -> None:
        self._stop.send_fi_hsl_gtfs_stop_stop(
            _feedurl=self._feed, _stop_id=stop_id, data=Stop(**kwargs), flush_producer=False)

    def send_vehicle(self, event_type: str, params: Dict[str, Any],
                     kwargs: Dict[str, Any]) -> None:
        method = getattr(self._tele, f"send_fi_hsl_hfp_{event_type}")
        method(_feedurl=self._feed, _operator_id=params["operator_id"],
               _vehicle_number=params["vehicle_number"],
               data=VehicleEvent(**kwargs), flush_producer=False)

    def send_traffic_light(self, event_type: str, params: Dict[str, Any],
                           kwargs: Dict[str, Any]) -> None:
        method = getattr(self._tele, f"send_fi_hsl_hfp_{event_type}")
        method(_feedurl=self._feed, _operator_id=params["operator_id"],
               _vehicle_number=params["vehicle_number"],
               data=TrafficLightEvent(**kwargs), flush_producer=False)

    def send_driver_block(self, event_type: str, params: Dict[str, Any],
                          kwargs: Dict[str, Any]) -> None:
        method = getattr(self._tele, f"send_fi_hsl_hfp_{event_type}")
        method(_feedurl=self._feed, _operator_id=params["operator_id"],
               _vehicle_number=params["vehicle_number"],
               data=DriverBlockEvent(**kwargs), flush_producer=False)

    def flush(self) -> None:
        self._producer.flush()

    def poll(self) -> None:
        self._producer.poll(0)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HSL HFP -> Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Stream HFP telemetry as CloudEvents to Kafka")
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
    feed_parser.add_argument("--content-mode", type=str,
                             default=os.getenv("CONTENT_MODE", "structured"),
                             choices=["structured", "binary"],
                             help="CloudEvents content mode for Kafka (default: structured)")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Emit reference data and a bounded telemetry sample, then exit.")
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
        bootstrap_servers=bootstrap, sasl_username=user, sasl_password=pwd, tls_enabled=tls_enabled)

    config = FeedConfig.from_env()
    if args.once:
        config.once = True

    producer = Producer(kafka_config)
    sink = KafkaSink(producer, topic, args.content_mode, HFP_FEED_URL)
    runner = BridgeRunner(config, feed_url=HFP_FEED_URL)
    logger.info("Starting HSL HFP -> Kafka bridge (topic=%s, bootstrap=%s)", topic, bootstrap)
    runner.run(sink)


if __name__ == "__main__":
    main()
