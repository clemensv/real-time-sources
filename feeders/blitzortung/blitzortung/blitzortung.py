"""Blitzortung live lightning bridge."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import websockets.sync.client as ws_client
from confluent_kafka import Producer

from blitzortung_core.blitzortung import (
    BridgeState,
    DEFAULT_BBOX,
    DEFAULT_SOURCE_MASK,
    DEFAULT_STATE_FILE,
    DEFAULT_TOPIC,
    DEFAULT_USER_AGENT,
    DEFAULT_WS_URLS,
    build_request,
    epoch_millis_to_iso8601,
    StateStore,
    iter_live_messages,
    normalize_stroke,
    parse_bbox,
    parse_bool,
    parse_connection_string,
    parse_ws_urls,
)
from blitzortung_producer_data import LightningStroke
from blitzortung_producer_kafka_producer.producer import BlitzortungLightningEventProducer

logger = logging.getLogger(__name__)


class BlitzortungBridge:
    """Connect the public Blitzortung live feed to Kafka."""

    def __init__(
        self,
        event_producer: BlitzortungLightningEventProducer,
        kafka_producer: Producer,
        *,
        state_store: StateStore,
        ws_urls: list[str],
        bbox: tuple[float, float, float, float],
        include_stations: bool = True,
        source_mask: int = DEFAULT_SOURCE_MASK,
        flush_interval: int = 250,
        max_retry_delay: int = 60,
        dedupe_size: int = 5000,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self._event_producer = event_producer
        self._kafka_producer = kafka_producer
        self._state_store = state_store
        self._ws_urls = ws_urls
        self._bbox = bbox
        self._include_stations = include_stations
        self._source_mask = source_mask
        self._flush_interval = flush_interval
        self._max_retry_delay = max_retry_delay
        self._user_agent = user_agent
        self._state = state_store.load()
        self._recent_keys = deque(self._state.recent_keys, maxlen=dedupe_size)
        self._recent_key_set = set(self._recent_keys)
        self._count_since_flush = 0
        self._total_strokes = 0

    def run(self) -> None:
        """Stream forever until interrupted."""

        try:
            for message in iter_live_messages(
                self._ws_urls,
                last_ids_provider=lambda: dict(self._state.last_ids),
                include_stations=self._include_stations,
                bbox=self._bbox,
                source_mask=self._source_mask,
                user_agent=self._user_agent,
                max_retry_delay=self._max_retry_delay,
                reason="feed",
            ):
                self._handle_message(message)
        finally:
            self.flush()

    def _handle_message(self, payload: dict[str, Any]) -> int:
        """Handle one websocket frame and emit any contained strokes."""

        strokes = payload.get("strokes")
        if not isinstance(strokes, list):
            return 0

        emitted = 0
        for stroke in strokes:
            if self._handle_stroke(stroke):
                emitted += 1
        return emitted

    def _handle_stroke(self, stroke: dict[str, Any]) -> bool:
        """Normalize, dedupe, emit, and checkpoint one stroke."""

        required_fields = ("src", "id", "time", "lat", "lon")
        if not all(field in stroke for field in required_fields):
            logger.debug("Skipping incomplete stroke payload: %s", stroke)
            return False

        identity = f"{int(stroke['src'])}/{stroke['id']}"
        if identity in self._recent_key_set:
            return False

        normalized = normalize_stroke(stroke)
        data = LightningStroke.from_serializer_dict(normalized)
        self._event_producer.send_blitzortung_lightning_lightning_stroke(
            _source_id=data.source_id,  # type: ignore[arg-type]
            _stroke_id=data.stroke_id,
            _time=data.event_time,
            data=data,
            flush_producer=False,
        )

        self._remember_stroke(identity, int(stroke["src"]), int(stroke["id"]))
        self._count_since_flush += 1
        self._total_strokes += 1

        if self._count_since_flush >= self._flush_interval:
            self.flush()
            logger.info("Flushed %d Blitzortung strokes", self._total_strokes)

        return True

    def _remember_stroke(self, identity: str, source_id: int, stroke_id: int) -> None:
        """Update dedupe and resume state after a successful emit."""

        if len(self._recent_keys) == self._recent_keys.maxlen:
            dropped = self._recent_keys[0]
            self._recent_key_set.discard(dropped)
        self._recent_keys.append(identity)
        self._recent_key_set.add(identity)

        source_key = str(source_id)
        previous = self._state.last_ids.get(source_key, 0)
        if stroke_id > previous:
            self._state.last_ids[source_key] = stroke_id

    def flush(self) -> None:
        """Flush Kafka and persist resume state."""

        self._kafka_producer.flush()
        self._state_store.save(
            BridgeState(
                last_ids=dict(self._state.last_ids),
                recent_keys=list(self._recent_keys),
            )
        )
        self._count_since_flush = 0

    def emit_mock_corpus(self, count: int = 3) -> int:
        """Emit synthetic lightning strokes for deterministic E2E testing.

        Builds raw upstream-shaped stroke frames and runs them through the
        same normalize, dedupe, and emit path as live data, then flushes, so
        the Docker Kafka flow test does not depend on sporadic live lightning
        activity. Returns the number of strokes emitted.
        """

        base_time_ms = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
        emitted = 0
        for index in range(count):
            stroke = {
                "src": self._source_mask,
                "id": 9_000_000_000 + index,
                "time": base_time_ms + index,
                "lat": 50.0 + index * 0.1,
                "lon": 8.0 + index * 0.1,
                "srv": 1,
                "del": 0,
                "dev": 1000.0,
                "sta": {"100": 0, "101": 1},
            }
            if self._handle_stroke(stroke):
                emitted += 1
        self.flush()
        logger.info("Mock mode: emitted %d synthetic Blitzortung strokes", emitted)
        return emitted


def probe_live_feed(
    *,
    ws_urls: list[str],
    bbox: tuple[float, float, float, float],
    include_stations: bool,
    source_mask: int,
    max_retry_delay: int,
    user_agent: str,
    max_strokes: int,
    duration: int,
) -> int:
    """Print normalized live strokes for diagnostics."""

    count = 0
    started = time.time()
    last_ids: dict[str, int] = {}

    for message in iter_live_messages(
        ws_urls,
        last_ids_provider=lambda: dict(last_ids),
        include_stations=include_stations,
        bbox=bbox,
        source_mask=source_mask,
        user_agent=user_agent,
        max_retry_delay=max_retry_delay,
        reason="probe",
    ):
        strokes = message.get("strokes")
        if not isinstance(strokes, list):
            continue

        for stroke in strokes:
            if not all(field in stroke for field in ("src", "id", "time", "lat", "lon")):
                continue
            normalized = normalize_stroke(stroke)
            print(json.dumps(normalized, ensure_ascii=False, sort_keys=True))
            last_ids[str(int(stroke["src"]))] = max(
                last_ids.get(str(int(stroke["src"])), 0),
                int(stroke["id"]),
            )
            count += 1

            if count >= max_strokes or time.time() - started >= duration:
                return count

    return count


def build_kafka_config(
    *,
    bootstrap: str,
    sasl_username: Optional[str],
    sasl_password: Optional[str],
    tls_enabled: bool,
) -> dict[str, str]:
    """Build Kafka producer configuration."""

    config: dict[str, str] = {"bootstrap.servers": bootstrap}
    if sasl_username and sasl_password:
        config.update(
            {
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )
    elif tls_enabled:
        config["security.protocol"] = "SSL"
    return config


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser(description="Blitzortung live lightning bridge")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Stream live strokes to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"))
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("--ws-urls", type=str, default=os.getenv("BLITZORTUNG_WS_URLS"))
    feed_parser.add_argument("--bbox", type=str, default=os.getenv("BLITZORTUNG_BBOX"))
    feed_parser.add_argument(
        "--include-stations",
        type=str,
        default=os.getenv("BLITZORTUNG_INCLUDE_STATIONS", "true"),
        help="Whether to request detector participation details (true/false).",
    )
    feed_parser.add_argument(
        "--source-mask",
        type=int,
        default=int(os.getenv("BLITZORTUNG_SOURCE_MASK", str(DEFAULT_SOURCE_MASK))),
    )
    feed_parser.add_argument(
        "--flush-interval",
        type=int,
        default=int(os.getenv("BLITZORTUNG_FLUSH_INTERVAL", "250")),
    )
    feed_parser.add_argument(
        "--max-retry-delay",
        type=int,
        default=int(os.getenv("BLITZORTUNG_MAX_RETRY_DELAY", "60")),
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv("BLITZORTUNG_STATE_FILE", DEFAULT_STATE_FILE),
    )
    feed_parser.add_argument(
        "--dedupe-size",
        type=int,
        default=int(os.getenv("BLITZORTUNG_DEDUPE_SIZE", "5000")),
    )
    feed_parser.add_argument(
        "--user-agent",
        type=str,
        default=os.getenv("BLITZORTUNG_USER_AGENT", DEFAULT_USER_AGENT),
    )
    feed_parser.add_argument(
        "--mock",
        action="store_true",
        default=parse_bool(os.getenv("BLITZORTUNG_MOCK"), default=False),
        help="Emit a synthetic corpus of strokes to Kafka and exit without "
             "connecting to the live Blitzortung feed (deterministic E2E tests).",
    )

    probe_parser = subparsers.add_parser("probe", help="Print live strokes without Kafka")
    probe_parser.add_argument("--ws-urls", type=str, default=os.getenv("BLITZORTUNG_WS_URLS"))
    probe_parser.add_argument("--bbox", type=str, default=os.getenv("BLITZORTUNG_BBOX"))
    probe_parser.add_argument(
        "--include-stations",
        type=str,
        default=os.getenv("BLITZORTUNG_INCLUDE_STATIONS", "true"),
    )
    probe_parser.add_argument(
        "--source-mask",
        type=int,
        default=int(os.getenv("BLITZORTUNG_SOURCE_MASK", str(DEFAULT_SOURCE_MASK))),
    )
    probe_parser.add_argument(
        "--max-retry-delay",
        type=int,
        default=int(os.getenv("BLITZORTUNG_MAX_RETRY_DELAY", "60")),
    )
    probe_parser.add_argument(
        "--user-agent",
        type=str,
        default=os.getenv("BLITZORTUNG_USER_AGENT", DEFAULT_USER_AGENT),
    )
    probe_parser.add_argument("--max-strokes", type=int, default=5)
    probe_parser.add_argument("--duration", type=int, default=20)

    args = parser.parse_args()

    if args.command == "probe":
        count = probe_live_feed(
            ws_urls=parse_ws_urls(args.ws_urls),
            bbox=parse_bbox(args.bbox),
            include_stations=parse_bool(args.include_stations, default=True),
            source_mask=args.source_mask,
            max_retry_delay=args.max_retry_delay,
            user_agent=args.user_agent,
            max_strokes=args.max_strokes,
            duration=args.duration,
        )
        logger.info("Printed %d live strokes", count)
        return 0

    if args.command == "feed":
        if args.connection_string:
            parsed = parse_connection_string(args.connection_string)
            bootstrap = parsed.get("bootstrap.servers")
            topic = parsed.get("kafka_topic")
            sasl_username = parsed.get("sasl.username")
            sasl_password = parsed.get("sasl.password")
        else:
            bootstrap = args.kafka_bootstrap_servers
            topic = args.kafka_topic or DEFAULT_TOPIC
            sasl_username = args.sasl_username
            sasl_password = args.sasl_password

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")
            return 1
        if not topic:
            print("Error: Kafka topic required (--kafka-topic or -c).")
            return 1

        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in {"false", "0", "no"}
        kafka_config = build_kafka_config(
            bootstrap=bootstrap,
            sasl_username=sasl_username,
            sasl_password=sasl_password,
            tls_enabled=tls_enabled,
        )
        kafka_producer = Producer(kafka_config)
        event_producer = BlitzortungLightningEventProducer(kafka_producer, topic)
        bridge = BlitzortungBridge(
            event_producer,
            kafka_producer,
            state_store=StateStore(args.state_file, dedupe_size=args.dedupe_size),
            ws_urls=parse_ws_urls(args.ws_urls),
            bbox=parse_bbox(args.bbox),
            include_stations=parse_bool(args.include_stations, default=True),
            source_mask=args.source_mask,
            flush_interval=args.flush_interval,
            max_retry_delay=args.max_retry_delay,
            dedupe_size=args.dedupe_size,
            user_agent=args.user_agent,
        )

        if args.mock:
            logger.info("Mock mode: emitting synthetic Blitzortung corpus and exiting")
            try:
                bridge.emit_mock_corpus()
            finally:
                bridge.flush()
            return 0

        try:
            bridge.run()
        except KeyboardInterrupt:
            logger.info("Interrupted, shutting down.")
        finally:
            bridge.flush()
        return 0

    parser.print_help()
    return 1

