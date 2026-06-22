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

DEFAULT_TOPIC = "wikimedia-osm-diffs"
from wikimedia_osm_diffs_core.wikimedia_osm_diffs import (
    DEFAULT_STATE_FILE,
    DEFAULT_USER_AGENT,
    DIFF_BASE_URL,
    STATE_URL,
    StateStore,
    build_session,
    fetch_sequence_changes,
    fetch_state,
    parse_osmchange_xml,
    parse_state_txt,
    sequence_to_path,
    sequence_to_url,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# State.txt parsing
# ---------------------------------------------------------------------------



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
        once: bool = False,
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
        self._once = once
        self._last_sequence = state_store.load()
        self._total_events = 0
        self._session = build_session(user_agent)

    def run(self) -> None:
        """Run the polling loop until interrupted."""
        retry_delay = 1
        while True:
            try:
                self._poll_cycle()
                retry_delay = 1
                if self._once:
                    logger.info("--once mode: exiting after first polling cycle")
                    return
                time.sleep(self._poll_interval)
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                logger.warning("Poll cycle error: %s. Retrying in %ds.", exc, retry_delay)
                if self._once:
                    logger.info("--once mode: exiting after error")
                    return
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self._max_retry_delay)

    def _poll_cycle(self) -> None:
        """Fetch the current state and process any new diffs."""
        state = fetch_state(self._session, self._state_url)
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
            source_url=sequence_to_url(current_seq, self._diff_base_url),
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

    def _process_sequence(self, seq: int) -> None:
        """Download, decompress, parse, and emit events for one sequence."""
        try:
            changes = fetch_sequence_changes(self._session, seq, self._diff_base_url)
        except requests.RequestException as exc:
            logger.warning("Failed to download diff %d: %s", seq, exc)
            return
        except (gzip.BadGzipFile, OSError) as exc:
            logger.warning("Failed to decompress diff %d: %s", seq, exc)
            return
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

def parse_connection_string(connection_string: str) -> dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config_dict: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').strip().replace("sb://", "").replace("/", "") + ":9093"
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
        once=args.once,
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
    feed_parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle (also via ONCE_MODE env var). Useful for scheduled execution in Fabric notebooks.",
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

