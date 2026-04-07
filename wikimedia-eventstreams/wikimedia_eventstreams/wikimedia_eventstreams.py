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


STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
DEFAULT_TOPIC = "wikimedia-eventstreams"
DEFAULT_STATE_FILE = os.path.expanduser("~/.wikimedia_eventstreams_state.json")
DEFAULT_USER_AGENT = (
    "real-time-sources-wikimedia-eventstreams/0.1 "
    "(https://github.com/clemensv/real-time-sources)"
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


def build_stream_url(base_url: str, since: Optional[str]) -> str:
    """Build the EventStreams URL with an optional since parameter."""

    if not since:
        return base_url
    return f"{base_url}?{urlencode({'since': since})}"


def _serialize_optional_json(value: Any) -> Optional[str]:
    """Serialize variant upstream fields into a stable JSON string."""

    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False, sort_keys=True)


def _stringify_optional(value: Any) -> Optional[str]:
    """Convert identifier-like values to strings while preserving nulls."""

    if value is None:
        return None
    return str(value)


def normalize_recent_change(change: dict[str, Any]) -> dict[str, Any]:
    """Normalize a Wikimedia recentchange payload for the generated data class."""

    meta = change.get("meta", {})
    length = change.get("length") or {}
    revision = change.get("revision") or {}

    return {
        "event_id": _stringify_optional(meta.get("id")),
        "event_time": _stringify_optional(meta.get("dt")),
        "schema_uri": change.get("$schema"),
        "meta": {
            "uri": meta.get("uri"),
            "request_id": meta.get("request_id"),
            "id": _stringify_optional(meta.get("id")),
            "domain": meta.get("domain"),
            "stream": meta.get("stream"),
            "topic": meta.get("topic"),
            "partition": meta.get("partition"),
            "offset": _stringify_optional(meta.get("offset")),
            "dt": meta.get("dt"),
        },
        "id": _stringify_optional(change.get("id")),
        "type": change.get("type"),
        "namespace": change.get("namespace"),
        "title": change.get("title"),
        "title_url": change.get("title_url"),
        "comment": change.get("comment"),
        "timestamp": change.get("timestamp"),
        "user": change.get("user"),
        "bot": change.get("bot"),
        "minor": change.get("minor"),
        "patrolled": change.get("patrolled"),
        "length": {
            "old": length.get("old"),
            "new": length.get("new"),
        },
        "revision": {
            "old": _stringify_optional(revision.get("old")),
            "new": _stringify_optional(revision.get("new")),
        },
        "server_url": change.get("server_url"),
        "server_name": change.get("server_name"),
        "server_script_path": change.get("server_script_path"),
        "wiki": change.get("wiki"),
        "parsedcomment": change.get("parsedcomment"),
        "notify_url": change.get("notify_url"),
        "log_type": change.get("log_type"),
        "log_action": change.get("log_action"),
        "log_action_comment": change.get("log_action_comment"),
        "log_id": _stringify_optional(change.get("log_id")),
        "log_params_json": _serialize_optional_json(change.get("log_params")),
    }


@dataclass
class BridgeState:
    """Persisted resume state."""

    since: Optional[str]
    recent_event_ids: list[str]


class StateStore:
    """Stores resume timestamp and a bounded event ID cache."""

    def __init__(self, path: str, dedupe_size: int) -> None:
        self._path = Path(path)
        self._dedupe_size = dedupe_size

    def load(self) -> BridgeState:
        if not self._path.exists():
            return BridgeState(since=None, recent_event_ids=[])
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load state file %s: %s", self._path, exc)
            return BridgeState(since=None, recent_event_ids=[])

        recent_ids = [str(item) for item in payload.get("recent_event_ids", []) if item]
        return BridgeState(
            since=payload.get("since"),
            recent_event_ids=recent_ids[-self._dedupe_size :],
        )

    def save(self, state: BridgeState) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "since": state.since,
            "recent_event_ids": state.recent_event_ids[-self._dedupe_size :],
        }
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


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

        retry_delay = 1
        timeout = aiohttp.ClientTimeout(total=None, connect=30, sock_read=90)

        while True:
            url = build_stream_url(self._stream_url, self._since)
            headers = {
                "Accept": "application/json",
                "User-Agent": self._user_agent,
            }
            logger.info("Connecting to %s", url)
            try:
                async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                    await self._stream_once(session)
                retry_delay = 1
            except asyncio.CancelledError:
                raise
            except (aiohttp.ClientError, asyncio.TimeoutError, ConnectionError) as exc:
                logger.warning("Stream error: %s. Reconnecting in %ds.", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self._max_retry_delay)

    async def _stream_once(
        self,
        session: aiohttp.ClientSession,
        *,
        max_events: Optional[int] = None,
    ) -> int:
        """Read one streaming session until EOF or max_events."""

        processed = 0
        async with session.get(build_stream_url(self._stream_url, self._since)) as response:
            response.raise_for_status()
            async for raw_line in response.content:
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                payload = json.loads(line)
                if self._handle_event(payload):
                    processed += 1
                    if max_events is not None and processed >= max_events:
                        return processed
        return processed

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
            _event_time=str(event_time),
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

    resolved_topic = topic or DEFAULT_TOPIC
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
