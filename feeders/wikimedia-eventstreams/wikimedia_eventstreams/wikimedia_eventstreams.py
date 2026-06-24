"""Wikimedia EventStreams recentchange bridge."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode

import aiohttp
from confluent_kafka import Producer

from wikimedia_eventstreams_producer_data import RecentChange
from wikimedia_eventstreams_producer_kafka_producer.producer import (
    WikimediaEventStreamsEventProducer,
)
from wikimedia_eventstreams_core.wikimedia_eventstreams import (
    BridgeState,
    DEFAULT_STATE_FILE,
    DEFAULT_USER_AGENT,
    STREAM_URL,
    StateStore,
    build_stream_url,
    iter_recentchange_payloads,
    normalize_recent_change,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


def parse_connection_string(connection_string: str) -> dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""

    config_dict: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').strip().replace("sb://", "").replace("/", "")
                    + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"').strip()
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc

    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"

    return config_dict




class WikimediaRecentChangeBridge:
    """Connect Wikimedia EventStreams recentchange to Kafka."""

    def __init__(
        self,
        event_producer: WikimediaEventStreamsEventProducer,
        kafka_producer: Producer,
        *,
        state_store: StateStore,
        stream_url: str = STREAM_URL,
        user_agent: str = DEFAULT_USER_AGENT,
        flush_interval: int = 250,
        max_retry_delay: int = 60,
        dedupe_size: int = 5000,
    ) -> None:
        self._event_producer = event_producer
        self._kafka_producer = kafka_producer
        self._state_store = state_store
        self._stream_url = stream_url
        self._user_agent = user_agent
        self._flush_interval = flush_interval
        self._max_retry_delay = max_retry_delay
        self._dedupe_size = dedupe_size
        self._state = state_store.load()
        self._recent_event_ids = deque(self._state.recent_event_ids, maxlen=dedupe_size)
        self._recent_event_id_set = set(self._recent_event_ids)
        self._since = self._state.since
        self._count_since_flush = 0
        self._total_events = 0

    async def run(self) -> None:
        """Run until interrupted."""

        processed = 0
        async for payload in iter_recentchange_payloads(stream_url=self._stream_url, user_agent=self._user_agent, since_provider=lambda: self._since, max_retry_delay=self._max_retry_delay):
            if self._handle_event(payload):
                processed += 1


    def _handle_event(self, payload: dict[str, Any]) -> bool:
        """Normalize, dedupe, and emit one recentchange event."""

        meta = payload.get("meta")
        if not isinstance(meta, dict):
            logger.warning("Skipping payload without meta object")
            return False

        if meta.get("domain") == "canary":
            return False

        event_id = meta.get("id")
        event_time = meta.get("dt")
        if not event_id or not event_time:
            logger.warning("Skipping payload without meta.id or meta.dt")
            return False

        if event_id in self._recent_event_id_set:
            return False

        normalized = normalize_recent_change(payload)
        data = RecentChange.from_serializer_dict(normalized)
        self._event_producer.send_wikimedia_event_streams_recent_change(
            _event_id=str(event_id),
            _time=str(event_time),
            data=data,
            flush_producer=False,
        )

        self._remember_event_id(str(event_id))
        self._since = str(event_time)
        self._total_events += 1
        self._count_since_flush += 1

        if self._count_since_flush >= self._flush_interval:
            self.flush()
            logger.info("Flushed %d recentchange events", self._total_events)

        return True

    def flush(self) -> None:
        """Flush Kafka and persist state."""

        self._kafka_producer.flush()
        self._state_store.save(
            BridgeState(
                since=self._since,
                recent_event_ids=list(self._recent_event_ids),
            )
        )
        self._count_since_flush = 0

    def _remember_event_id(self, event_id: str) -> None:
        if event_id in self._recent_event_id_set:
            return
        if len(self._recent_event_ids) == self._dedupe_size:
            expired = self._recent_event_ids[0]
            self._recent_event_id_set.discard(expired)
        self._recent_event_ids.append(event_id)
        self._recent_event_id_set.add(event_id)


def build_kafka_config(args: argparse.Namespace) -> tuple[dict[str, str], str]:
    """Build Kafka config and resolve topic."""

    if args.connection_string:
        cfg = parse_connection_string(args.connection_string)
        bootstrap = cfg.get("bootstrap.servers")
        topic = cfg.get("kafka_topic")
        sasl_user = cfg.get("sasl.username")
        sasl_password = cfg.get("sasl.password")
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic
        sasl_user = args.sasl_username
        sasl_password = args.sasl_password

    if not bootstrap:
        raise ValueError("Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")

    resolved_topic = topic or "wikimedia-eventstreams"
    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: dict[str, str] = {"bootstrap.servers": bootstrap}
    if sasl_user and sasl_password:
        kafka_config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_user,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    return kafka_config, resolved_topic


async def run_probe(args: argparse.Namespace) -> int:
    """Print a few live recentchange events."""

    timeout = aiohttp.ClientTimeout(total=None, connect=30, sock_read=90)
    headers = {
        "Accept": "application/json",
        "User-Agent": args.user_agent,
    }
    deadline = time.monotonic() + args.duration
    printed = 0

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        async with session.get(STREAM_URL) as response:
            response.raise_for_status()
            async for raw_line in response.content:
                if time.monotonic() >= deadline:
                    break
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                payload = json.loads(line)
                if payload.get("meta", {}).get("domain") == "canary":
                    continue
                print(json.dumps(payload, indent=2, ensure_ascii=False))
                printed += 1
                if printed >= args.max_events:
                    break

    return 0


async def run_feed(args: argparse.Namespace) -> int:
    """Run the Kafka bridge."""

    kafka_config, topic = build_kafka_config(args)
    kafka_producer = Producer(kafka_config)
    event_producer = WikimediaEventStreamsEventProducer(kafka_producer, topic)
    state_store = StateStore(args.state_file, args.dedupe_size)
    bridge = WikimediaRecentChangeBridge(
        event_producer,
        kafka_producer,
        state_store=state_store,
        user_agent=args.user_agent,
        flush_interval=args.flush_interval,
        max_retry_delay=args.max_retry_delay,
        dedupe_size=args.dedupe_size,
    )

    try:
        await bridge.run()
    finally:
        bridge.flush()

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""

    parser = argparse.ArgumentParser(
        description="Wikimedia EventStreams recentchange bridge to Kafka"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    feed_parser = subparsers.add_parser("feed", help="Stream Wikimedia recentchange events to Kafka")
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    )
    feed_parser.add_argument(
        "--kafka-topic",
        default=os.getenv("KAFKA_TOPIC"),
    )
    feed_parser.add_argument(
        "--sasl-username",
        default=os.getenv("SASL_USERNAME"),
    )
    feed_parser.add_argument(
        "--sasl-password",
        default=os.getenv("SASL_PASSWORD"),
    )
    feed_parser.add_argument(
        "-c",
        "--connection-string",
        default=os.getenv("CONNECTION_STRING"),
    )
    feed_parser.add_argument(
        "--state-file",
        default=os.getenv("WIKIMEDIA_EVENTSTREAMS_STATE_FILE", DEFAULT_STATE_FILE),
    )
    feed_parser.add_argument(
        "--flush-interval",
        type=int,
        default=int(os.getenv("WIKIMEDIA_EVENTSTREAMS_FLUSH_INTERVAL", "250")),
    )
    feed_parser.add_argument(
        "--dedupe-size",
        type=int,
        default=int(os.getenv("WIKIMEDIA_EVENTSTREAMS_DEDUPE_SIZE", "5000")),
    )
    feed_parser.add_argument(
        "--max-retry-delay",
        type=int,
        default=int(os.getenv("WIKIMEDIA_EVENTSTREAMS_MAX_RETRY_DELAY", "60")),
    )
    feed_parser.add_argument(
        "--user-agent",
        default=os.getenv("WIKIMEDIA_EVENTSTREAMS_USER_AGENT", DEFAULT_USER_AGENT),
    )

    probe_parser = subparsers.add_parser("probe", help="Print a few live recentchange events")
    probe_parser.add_argument(
        "--duration",
        type=int,
        default=15,
    )
    probe_parser.add_argument(
        "--max-events",
        type=int,
        default=3,
    )
    probe_parser.add_argument(
        "--user-agent",
        default=os.getenv("WIKIMEDIA_EVENTSTREAMS_USER_AGENT", DEFAULT_USER_AGENT),
    )

    return parser


def main() -> int:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args()

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if args.command == "probe":
        return asyncio.run(run_probe(args))
    if args.command == "feed":
        return asyncio.run(run_feed(args))

    parser.print_help()
    return 1

