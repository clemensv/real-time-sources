"""OpenStreetMap Minutely Diffs bridge to Kafka."""

from __future__ import annotations

import argparse
import datetime
import gzip
import io
import json
import logging
import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Optional

import requests
from confluent_kafka import Producer

from wikimedia_osm_diffs_producer_data import MapChange, ReplicationState
from wikimedia_osm_diffs_producer_kafka_producer.producer import (
    OrgOpenStreetMapDiffsEventProducer,
    OrgOpenStreetMapDiffsStateEventProducer,
)


STATE_URL = "https://planet.openstreetmap.org/replication/minute/state.txt"
DIFF_BASE_URL = "https://planet.openstreetmap.org/replication/minute"
DEFAULT_TOPIC = "wikimedia-osm-diffs"
DEFAULT_STATE_FILE = os.path.expanduser("~/.wikimedia_osm_diffs_state.json")
DEFAULT_USER_AGENT = (
    "real-time-sources-wikimedia-osm-diffs/0.1 "
    "(https://github.com/clemensv/real-time-sources)"
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# State.txt parsing
# ---------------------------------------------------------------------------

def parse_state_txt(text: str) -> dict[str, Any]:
    """Parse an OSM replication state.txt into a dict with sequence_number and timestamp."""
    result: dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key == "sequenceNumber":
            result["sequence_number"] = int(value)
        elif key == "timestamp":
            ts_str = value.replace("\\:", ":")
            result["timestamp"] = datetime.datetime.fromisoformat(ts_str)
    return result


# ---------------------------------------------------------------------------
# Sequence number to URL path
# ---------------------------------------------------------------------------

def sequence_to_path(seq: int) -> str:
    """Convert a sequence number to the /NNN/NNN/NNN path segment."""
    a = seq // 1_000_000
    b = (seq % 1_000_000) // 1_000
    c = seq % 1_000
    return f"{a:03d}/{b:03d}/{c:03d}"


def sequence_to_url(seq: int, base_url: str = DIFF_BASE_URL) -> str:
    """Build the full diff .osc.gz URL for a given sequence number."""
    return f"{base_url}/{sequence_to_path(seq)}.osc.gz"


# ---------------------------------------------------------------------------
# OsmChange XML parsing
# ---------------------------------------------------------------------------

def parse_osmchange_xml(xml_bytes: bytes, sequence_number: int) -> list[dict[str, Any]]:
    """Parse OsmChange XML and return a list of change dicts."""
    root = ET.fromstring(xml_bytes)
    changes: list[dict[str, Any]] = []

    for action_elem in root:
        change_type = action_elem.tag
        if change_type not in ("create", "modify", "delete"):
            continue

        for elem in action_elem:
            element_type = elem.tag
            if element_type not in ("node", "way", "relation"):
                continue

            tags: dict[str, str] = {}
            for tag_elem in elem.findall("tag"):
                k = tag_elem.get("k", "")
                v = tag_elem.get("v", "")
                if k:
                    tags[k] = v

            ts_str = elem.get("timestamp", "")
            if ts_str:
                ts = datetime.datetime.fromisoformat(ts_str)
            else:
                ts = datetime.datetime.now(datetime.timezone.utc)

            uid_str = elem.get("uid")
            user_id = int(uid_str) if uid_str else None
            user_name = elem.get("user") or None

            lat_str = elem.get("lat")
            lon_str = elem.get("lon")
            latitude = float(lat_str) if lat_str else None
            longitude = float(lon_str) if lon_str else None

            change: dict[str, Any] = {
                "change_type": change_type,
                "element_type": element_type,
                "element_id": int(elem.get("id", "0")),
                "version": int(elem.get("version", "0")),
                "timestamp": ts,
                "changeset_id": int(elem.get("changeset", "0")),
                "user_name": user_name,
                "user_id": user_id,
                "latitude": latitude,
                "longitude": longitude,
                "tags": json.dumps(tags, separators=(",", ":"), ensure_ascii=False),
                "sequence_number": sequence_number,
            }
            changes.append(change)

    return changes


# ---------------------------------------------------------------------------
# Connection string parsing
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Bridge state
# ---------------------------------------------------------------------------

class StateStore:
    """Persisted bridge state for tracking the last processed sequence number."""

    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def load(self) -> Optional[int]:
        """Load the last processed sequence number, or None if no state."""
        if not self._path.exists():
            return None
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load state file %s: %s", self._path, exc)
            return None
        return payload.get("last_sequence_number")

    def save(self, last_sequence_number: int) -> None:
        """Persist the last processed sequence number."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"last_sequence_number": last_sequence_number}
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Bridge
# ---------------------------------------------------------------------------

class OsmDiffsBridge:
    """Poll OSM minutely diffs and emit MapChange events to Kafka."""

    def __init__(
        self,
        diffs_producer: OrgOpenStreetMapDiffsEventProducer,
        state_producer: OrgOpenStreetMapDiffsStateEventProducer,
        kafka_producer: Producer,
        *,
        state_store: StateStore,
        state_url: str = STATE_URL,
        diff_base_url: str = DIFF_BASE_URL,
        user_agent: str = DEFAULT_USER_AGENT,
        poll_interval: int = 60,
        max_retry_delay: int = 120,
    ) -> None:
        self._diffs_producer = diffs_producer
        self._state_producer = state_producer
        self._kafka_producer = kafka_producer
        self._state_store = state_store
        self._state_url = state_url
        self._diff_base_url = diff_base_url
        self._user_agent = user_agent
        self._poll_interval = poll_interval
        self._max_retry_delay = max_retry_delay
        self._last_sequence = state_store.load()
        self._total_events = 0
        self._session = requests.Session()
        self._session.headers["User-Agent"] = user_agent

    def run(self) -> None:
        """Run the polling loop until interrupted."""
        retry_delay = 1
        while True:
            try:
                self._poll_cycle()
                retry_delay = 1
                time.sleep(self._poll_interval)
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                logger.warning("Poll cycle error: %s. Retrying in %ds.", exc, retry_delay)
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self._max_retry_delay)

    def _poll_cycle(self) -> None:
        """Fetch the current state and process any new diffs."""
        state = self._fetch_state()
        if state is None:
            return

        current_seq = state["sequence_number"]
        current_ts = state["timestamp"]

        if self._last_sequence is not None and current_seq <= self._last_sequence:
            logger.debug("No new sequences (current=%d, last=%d)", current_seq, self._last_sequence)
            return

        start_seq = (self._last_sequence + 1) if self._last_sequence is not None else current_seq
        # Limit to at most 5 sequences per cycle to avoid unbounded catch-up
        start_seq = max(start_seq, current_seq - 4)

        for seq in range(start_seq, current_seq + 1):
            self._process_sequence(seq)

        # Emit replication state
        state_data = ReplicationState(
            sequence_number=current_seq,
            timestamp=current_ts,
        )
        self._state_producer.send_org_open_street_map_diffs_replication_state(
            data=state_data,
            flush_producer=False,
        )

        self._kafka_producer.flush()
        self._last_sequence = current_seq
        self._state_store.save(current_seq)
        logger.info(
            "Processed sequence %d (%d total events emitted)",
            current_seq,
            self._total_events,
        )

    def _fetch_state(self) -> Optional[dict[str, Any]]:
        """Fetch and parse the replication state.txt."""
        try:
            resp = self._session.get(self._state_url, timeout=30)
            resp.raise_for_status()
            return parse_state_txt(resp.text)
        except (requests.RequestException, ValueError, KeyError) as exc:
            logger.warning("Failed to fetch state: %s", exc)
            return None

    def _process_sequence(self, seq: int) -> None:
        """Download, decompress, parse, and emit events for one sequence."""
        url = sequence_to_url(seq, self._diff_base_url)
        try:
            resp = self._session.get(url, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as exc:
            logger.warning("Failed to download diff %d: %s", seq, exc)
            return

        try:
            xml_bytes = gzip.decompress(resp.content)
        except (gzip.BadGzipFile, OSError) as exc:
            logger.warning("Failed to decompress diff %d: %s", seq, exc)
            return

        changes = parse_osmchange_xml(xml_bytes, seq)
        for change in changes:
            data = MapChange.from_serializer_dict(change)
            self._diffs_producer.send_org_open_street_map_diffs_map_change(
                _element_type=change["element_type"],
                _element_id=str(change["element_id"]),
                data=data,
                flush_producer=False,
            )
            self._total_events += 1

    def flush(self) -> None:
        """Flush Kafka and persist state."""
        self._kafka_producer.flush()
        if self._last_sequence is not None:
            self._state_store.save(self._last_sequence)


# ---------------------------------------------------------------------------
# Kafka configuration
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_feed(args: argparse.Namespace) -> int:
    """Run the Kafka bridge."""
    kafka_config, topic = build_kafka_config(args)
    kafka_producer = Producer(kafka_config)
    diffs_producer = OrgOpenStreetMapDiffsEventProducer(kafka_producer, topic)
    state_producer = OrgOpenStreetMapDiffsStateEventProducer(kafka_producer, topic)
    state_store = StateStore(args.state_file)

    bridge = OsmDiffsBridge(
        diffs_producer,
        state_producer,
        kafka_producer,
        state_store=state_store,
        user_agent=args.user_agent,
        poll_interval=args.poll_interval,
        max_retry_delay=args.max_retry_delay,
    )

    try:
        bridge.run()
    finally:
        bridge.flush()

    return 0


def run_probe(args: argparse.Namespace) -> int:
    """Fetch and print the current state and a few changes."""
    session = requests.Session()
    session.headers["User-Agent"] = args.user_agent

    resp = session.get(STATE_URL, timeout=30)
    resp.raise_for_status()
    state = parse_state_txt(resp.text)
    print(json.dumps({"state": {
        "sequence_number": state["sequence_number"],
        "timestamp": state["timestamp"].isoformat(),
    }}, indent=2))

    seq = state["sequence_number"]
    url = sequence_to_url(seq)
    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    xml_bytes = gzip.decompress(resp.content)
    changes = parse_osmchange_xml(xml_bytes, seq)

    for change in changes[:args.max_events]:
        change_copy = dict(change)
        change_copy["timestamp"] = change_copy["timestamp"].isoformat()
        print(json.dumps(change_copy, indent=2, ensure_ascii=False))

    print(f"\nTotal changes in sequence {seq}: {len(changes)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(
        description="OpenStreetMap Minutely Diffs bridge to Kafka"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    feed_parser = subparsers.add_parser("feed", help="Stream OSM diffs to Kafka")
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
        default=os.getenv("OSM_DIFFS_STATE_FILE", DEFAULT_STATE_FILE),
    )
    feed_parser.add_argument(
        "--poll-interval",
        type=int,
        default=int(os.getenv("OSM_DIFFS_POLL_INTERVAL", "60")),
    )
    feed_parser.add_argument(
        "--max-retry-delay",
        type=int,
        default=int(os.getenv("OSM_DIFFS_MAX_RETRY_DELAY", "120")),
    )
    feed_parser.add_argument(
        "--user-agent",
        default=os.getenv("OSM_DIFFS_USER_AGENT", DEFAULT_USER_AGENT),
    )

    probe_parser = subparsers.add_parser("probe", help="Print current state and a few changes")
    probe_parser.add_argument(
        "--max-events",
        type=int,
        default=5,
    )
    probe_parser.add_argument(
        "--user-agent",
        default=os.getenv("OSM_DIFFS_USER_AGENT", DEFAULT_USER_AGENT),
    )

    return parser


def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if args.command == "probe":
        return run_probe(args)
    if args.command == "feed":
        return run_feed(args)

    parser.print_help()
    return 1
