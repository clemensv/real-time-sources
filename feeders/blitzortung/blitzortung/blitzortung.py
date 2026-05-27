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

from blitzortung_producer_data import LightningStroke
from blitzortung_producer_kafka_producer.producer import BlitzortungLightningEventProducer


DEFAULT_WS_URLS = (
    "wss://live.lightningmaps.org:443/",
    "wss://live2.lightningmaps.org:443/",
)
DEFAULT_BBOX = (90.0, 180.0, -90.0, -180.0)
DEFAULT_TOPIC = "blitzortung"
DEFAULT_SOURCE_MASK = 4
DEFAULT_STATE_FILE = os.path.expanduser("~/.blitzortung_state.json")
DEFAULT_USER_AGENT = (
    "real-time-sources-blitzortung/0.1 "
    "(https://github.com/clemensv/real-time-sources)"
)


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
else:
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )

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


def parse_ws_urls(value: str | None) -> list[str]:
    """Parse a comma-separated websocket URL list."""

    if not value:
        return list(DEFAULT_WS_URLS)
    urls = [item.strip() for item in value.split(",") if item.strip()]
    if not urls:
        raise ValueError("At least one websocket URL is required")
    return urls


def parse_bbox(value: str | None) -> tuple[float, float, float, float]:
    """Parse upstream bounding box in north,east,south,west order."""

    if not value:
        return DEFAULT_BBOX

    parts = [float(item.strip()) for item in value.split(",")]
    if len(parts) != 4:
        raise ValueError("Bounding box must be north,east,south,west")

    north, east, south, west = parts
    if north < south:
        raise ValueError("Bounding box north must be >= south")
    if not (-90.0 <= south <= 90.0 and -90.0 <= north <= 90.0):
        raise ValueError("Latitude bounds must be between -90 and 90")
    if not (-180.0 <= west <= 180.0 and -180.0 <= east <= 180.0):
        raise ValueError("Longitude bounds must be between -180 and 180")
    return north, east, south, west


def parse_bool(value: str | bool | None, *, default: bool = False) -> bool:
    """Parse a conventional env-var boolean."""

    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"1", "true", "yes", "on"}


def epoch_millis_to_iso8601(timestamp_ms: int) -> str:
    """Convert epoch milliseconds to ISO-8601 UTC."""

    return (
        datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def build_request(
    last_ids: dict[str, int],
    *,
    include_stations: bool,
    bbox: tuple[float, float, float, float],
    source_mask: int,
    zoom: int = 5,
    reason: str = "feed",
    loop_count: int = 0,
    server_time: int = 0,
) -> str:
    """Build the public LightningMaps websocket request frame."""

    north, east, south, west = bbox
    payload = {
        "v": 24,
        "i": last_ids,
        "s": include_stations,
        "x": 0,
        "w": 0,
        "tx": 0,
        "tw": 0,
        "a": source_mask,
        "z": zoom,
        "b": True,
        "h": "",
        "l": loop_count,
        "t": server_time,
        "from_lightningmaps_org": True,
        "p": [north, east, south, west],
        "r": reason,
    }
    return json.dumps(payload, separators=(",", ":"))


def normalize_stroke(stroke: dict[str, Any]) -> dict[str, Any]:
    """Normalize one upstream stroke into the generated contract shape."""

    timestamp_ms = int(stroke["time"])
    station_map = stroke.get("sta")
    detector_participations: list[dict[str, int]] = []

    if isinstance(station_map, dict):
        for station_id, status in sorted(station_map.items(), key=lambda item: int(item[0])):
            detector_participations.append(
                {
                    "station_id": int(station_id),
                    "status": int(status),
                }
            )

    return {
        "source_id": int(stroke["src"]),
        "stroke_id": str(stroke["id"]),
        "event_time": epoch_millis_to_iso8601(timestamp_ms),
        "event_timestamp_ms": timestamp_ms,
        "latitude": float(stroke["lat"]),
        "longitude": float(stroke["lon"]),
        "server_id": int(stroke["srv"]) if stroke.get("srv") is not None else None,
        "server_delay_ms": int(stroke["del"]) if stroke.get("del") is not None else None,
        "accuracy_diameter_m": float(stroke["dev"]) if stroke.get("dev") is not None else None,
        "detector_participations": detector_participations,
    }


@dataclass
class BridgeState:
    """Persisted websocket resume and dedupe state."""

    last_ids: dict[str, int]
    recent_keys: list[str]


class StateStore:
    """Stores last seen per-source ids and a bounded recent-key cache."""

    def __init__(self, path: str, dedupe_size: int) -> None:
        self._path = Path(path)
        self._dedupe_size = dedupe_size

    def load(self) -> BridgeState:
        if not self._path.exists():
            return BridgeState(last_ids={}, recent_keys=[])
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load state file %s: %s", self._path, exc)
            return BridgeState(last_ids={}, recent_keys=[])

        last_ids = {
            str(key): int(value)
            for key, value in payload.get("last_ids", {}).items()
            if key is not None and value is not None
        }
        recent_keys = [str(item) for item in payload.get("recent_keys", []) if item]
        return BridgeState(last_ids=last_ids, recent_keys=recent_keys[-self._dedupe_size :])

    def save(self, state: BridgeState) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "last_ids": state.last_ids,
            "recent_keys": state.recent_keys[-self._dedupe_size :],
        }
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def iter_live_messages(
    urls: list[str],
    *,
    last_ids_provider,
    include_stations: bool,
    bbox: tuple[float, float, float, float],
    source_mask: int,
    user_agent: str,
    max_retry_delay: int,
    reason: str,
) -> Iterable[dict[str, Any]]:
    """Yield parsed websocket frames across reconnects."""

    retry_delay = 1
    attempt = 0

    while True:
        url = urls[attempt % len(urls)]
        attempt += 1
        try:
            logger.info("Connecting to %s", url)
            with ws_client.connect(
                url,
                open_timeout=20,
                close_timeout=10,
                user_agent_header=user_agent,
            ) as connection:
                connection.send(
                    build_request(
                        last_ids_provider(),
                        include_stations=include_stations,
                        bbox=bbox,
                        source_mask=source_mask,
                        reason=reason,
                    )
                )
                retry_delay = 1
                for raw in connection:
                    try:
                        yield json.loads(raw)
                    except json.JSONDecodeError as exc:
                        logger.debug("Skipping non-JSON websocket frame: %s", exc)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            logger.warning("Websocket error from %s: %s. Reconnecting in %ds.", url, exc, retry_delay)
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)


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
            _source_id=data.source_id,
            _stroke_id=data.stroke_id,
            _event_time=data.event_time,
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

        try:
            bridge.run()
        except KeyboardInterrupt:
            logger.info("Interrupted, shutting down.")
        finally:
            bridge.flush()
        return 0

    parser.print_help()
    return 1
