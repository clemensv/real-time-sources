"""German Autobahn API bridge."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from confluent_kafka import Producer

try:
    from autobahn_core import (
        DEFAULT_KAFKA_TOPIC,
        DEFAULT_POLL_INTERVAL_SECONDS,
        DEFAULT_REQUEST_CONCURRENCY,
        DEFAULT_RESOURCES,
        DEFAULT_STATE_FILE,
        EVENT_FAMILIES,
        SELECTION_SENTINEL,
        USER_AGENT,
        AutobahnPoller as CoreAutobahnPoller,
        build_family_snapshot,
        determine_event_family,
        diff_items,
        load_generated_data_classes,
        merge_snapshots,
        normalize_road_ids,
        parse_charging_points,
        parse_connection_string,
        parse_resources_argument,
        parse_roads_argument,
    )
except ImportError:
    from autobahn_core.autobahn_core import (
        DEFAULT_KAFKA_TOPIC,
        DEFAULT_POLL_INTERVAL_SECONDS,
        DEFAULT_REQUEST_CONCURRENCY,
        DEFAULT_RESOURCES,
        DEFAULT_STATE_FILE,
        EVENT_FAMILIES,
        SELECTION_SENTINEL,
        USER_AGENT,
        AutobahnPoller as CoreAutobahnPoller,
        build_family_snapshot,
        determine_event_family,
        diff_items,
        load_generated_data_classes,
        merge_snapshots,
        normalize_road_ids,
        parse_charging_points,
        parse_connection_string,
        parse_resources_argument,
        parse_roads_argument,
    )


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


def _load_generated_producer_class() -> type[Any]:
    module = importlib.import_module("autobahn_producer_kafka_producer.producer")
    producers = [
        getattr(module, name)
        for name in dir(module)
        if name.endswith("EventProducer") and isinstance(getattr(module, name), type)
    ]
    for candidate in producers:
        if "Mqtt" not in candidate.__name__ and "Amqp" not in candidate.__name__:
            return candidate
    if producers:
        return producers[0]
    raise ImportError("Generated Autobahn producer client not found. Run ./generate_producer.ps1.")


class AutobahnPoller(CoreAutobahnPoller):
    """Kafka transport wrapper over the transport-neutral Autobahn poller."""

    def __init__(
        self,
        kafka_config: Optional[dict[str, str]] = None,
        kafka_topic: Optional[str] = None,
        state_file: Optional[str] = None,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
        resources: tuple[str, ...] = DEFAULT_RESOURCES,
        roads: Optional[list[str]] = None,
        request_concurrency: int = DEFAULT_REQUEST_CONCURRENCY,
    ) -> None:
        super().__init__(
            state_file=state_file,
            poll_interval_seconds=poll_interval_seconds,
            resources=resources,
            roads=roads,
            request_concurrency=request_concurrency,
        )
        self.kafka_topic = kafka_topic or DEFAULT_KAFKA_TOPIC
        self.data_classes: dict[str, type[Any]] = {}
        self.event_producer: Optional[Any] = None
        if kafka_config is not None:
            producer_class = _load_generated_producer_class()
            self.data_classes = load_generated_data_classes("autobahn_producer_data")
            kafka_producer = Producer(kafka_config)
            self.event_producer = producer_class(kafka_producer, self.kafka_topic)

    def _send_change(self, family: str, action: str, snapshot: dict[str, Any], event_time: str) -> None:
        if not self.event_producer:
            return
        config = EVENT_FAMILIES[family]
        data_kwargs = dict(snapshot)
        data_kwargs["event_time"] = event_time
        data_class = self.data_classes[config["schema"]]
        data = data_class(**data_kwargs)
        method_name = f"send_de_autobahn_{config['method_stem']}_{action}"
        method = getattr(self.event_producer, method_name)
        method(
            _identifier=snapshot["identifier"],
            _time=event_time,
            data=data,
            flush_producer=False,
        )

    async def poll_once(self, _session: Any = None, poll_time: Optional[datetime] = None) -> dict[str, dict[str, int]]:
        changes, detected_changes = await asyncio.to_thread(super().poll_once, poll_time or datetime.now(timezone.utc))
        for change in detected_changes:
            self._send_change(change.family, change.action, change.snapshot, change.event_time)
        if self.event_producer:
            self.event_producer.producer.flush()
        self.save_state()
        return changes

    async def poll_and_send(self, once: bool = False) -> None:
        while True:
            cycle_started = datetime.now(timezone.utc)
            changes = await self.poll_once(poll_time=cycle_started)
            summary = self.summarize_changes(changes)
            logger.info("Autobahn cycle complete: %s", summary or "no changes")
            if once:
                logger.info("--once mode: exiting after first polling cycle")
                return
            elapsed = datetime.now(timezone.utc) - cycle_started
            remaining = timedelta(seconds=self.poll_interval_seconds) - elapsed
            if remaining.total_seconds() > 0:
                await asyncio.sleep(remaining.total_seconds())


async def run_list_roads() -> None:
    poller = CoreAutobahnPoller()
    for road_id in await asyncio.to_thread(poller.fetch_roads):
        print(road_id)


def _resolve_argument(value: Optional[str], env_var: str, default: Optional[str] = None) -> Optional[str]:
    if value is not None:
        return value
    env_value = os.getenv(env_var)
    if env_value is not None:
        return env_value
    return default


def _resolve_int_argument(value: Optional[int], env_var: str, default: int) -> int:
    if value is not None:
        return value
    env_value = os.getenv(env_var)
    if env_value:
        try:
            return int(env_value)
        except ValueError as exc:
            raise ValueError(f"Environment variable {env_var} must be an integer") from exc
    return default


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    connection_string = _resolve_argument(args.connection_string, "CONNECTION_STRING")
    if connection_string:
        parsed = parse_connection_string(connection_string)
        kafka_bootstrap_servers = parsed.get("bootstrap.servers")
        entity_topic = parsed.get("kafka_topic")
        kafka_topic = entity_topic or args.kafka_topic or os.getenv("KAFKA_TOPIC") or DEFAULT_KAFKA_TOPIC
        sasl_username = parsed.get("sasl.username")
        sasl_password = parsed.get("sasl.password")
    else:
        kafka_bootstrap_servers = _resolve_argument(args.kafka_bootstrap_servers, "KAFKA_BOOTSTRAP_SERVERS")
        kafka_topic = _resolve_argument(args.kafka_topic, "KAFKA_TOPIC", DEFAULT_KAFKA_TOPIC)
        sasl_username = _resolve_argument(args.sasl_username, "SASL_USERNAME")
        sasl_password = _resolve_argument(args.sasl_password, "SASL_PASSWORD")

    if not kafka_bootstrap_servers:
        raise ValueError("Kafka bootstrap servers must be provided either directly or through CONNECTION_STRING.")

    kafka_config = {"bootstrap.servers": kafka_bootstrap_servers}
    tls_enabled = _resolve_argument(None, "KAFKA_ENABLE_TLS", "true").lower() not in {"false", "0", "no"}
    if sasl_username and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    return kafka_config, kafka_topic


def configure_logging(log_level: str) -> None:
    logging.getLogger().setLevel(getattr(logging, log_level.upper(), logging.INFO))


def main() -> None:
    parser = argparse.ArgumentParser(description="German Autobahn Traffic Bridge")
    subparsers = parser.add_subparsers(dest="subcommand")

    roads_parser = subparsers.add_parser("roads", help="List the available Autobahn road IDs")
    roads_parser.add_argument("--log-level", type=str, default=None, help="Logging level")

    feed_parser = subparsers.add_parser("feed", help="Poll the Autobahn API and publish changes to Kafka")
    feed_parser.add_argument("--state-file", type=str, default=None, help="File used to store ETags and last-seen snapshots")
    feed_parser.add_argument("--poll-interval", type=int, default=None, help="Polling interval in seconds")
    feed_parser.add_argument("--resources", type=str, default=None, help="Comma-separated resource list or *")
    feed_parser.add_argument("--roads", type=str, default=None, help="Comma-separated road list or *")
    feed_parser.add_argument("--request-concurrency", type=int, default=None, help="Maximum concurrent Autobahn API requests")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=None, help="Comma-separated Kafka bootstrap servers")
    feed_parser.add_argument("--kafka-topic", type=str, default=None, help="Kafka topic")
    feed_parser.add_argument("--sasl-username", type=str, default=None, help="SASL username")
    feed_parser.add_argument("--sasl-password", type=str, default=None, help="SASL password")
    feed_parser.add_argument("--connection-string", type=str, default=None, help="Event Hubs or Fabric Event Streams connection string")
    feed_parser.add_argument("--log-level", type=str, default=None, help="Logging level")
    feed_parser.add_argument("--once", action="store_true", help="Run a single polling cycle and exit (for scheduled hosts like Fabric notebooks)")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        return

    log_level = _resolve_argument(getattr(args, "log_level", None), "LOG_LEVEL", "INFO") or "INFO"
    configure_logging(log_level)

    if args.subcommand == "roads":
        asyncio.run(run_list_roads())
        return

    try:
        kafka_config, kafka_topic = build_kafka_config(args)
        resources = parse_resources_argument(_resolve_argument(args.resources, "AUTOBAHN_RESOURCES", SELECTION_SENTINEL) or SELECTION_SENTINEL)
        roads = parse_roads_argument(_resolve_argument(args.roads, "AUTOBAHN_ROADS", SELECTION_SENTINEL) or SELECTION_SENTINEL)
        poll_interval_seconds = _resolve_int_argument(args.poll_interval, "AUTOBAHN_POLL_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS)
        request_concurrency = _resolve_int_argument(args.request_concurrency, "AUTOBAHN_REQUEST_CONCURRENCY", DEFAULT_REQUEST_CONCURRENCY)
        state_file = _resolve_argument(args.state_file, "AUTOBAHN_STATE_FILE", DEFAULT_STATE_FILE)
    except ValueError as exc:
        logger.error("%s", exc)
        sys.exit(1)

    poller = AutobahnPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=state_file,
        poll_interval_seconds=poll_interval_seconds,
        resources=resources,
        roads=roads,
        request_concurrency=request_concurrency,
    )
    once_flag = bool(getattr(args, "once", False)) or os.getenv("ONCE_MODE", "").lower() in {"1", "true", "yes"}
    asyncio.run(poller.poll_and_send(once=once_flag))


if __name__ == "__main__":
    main()
