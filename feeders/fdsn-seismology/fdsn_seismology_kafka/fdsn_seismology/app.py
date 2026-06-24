from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import Any

import requests
from confluent_kafka import Producer

from fdsn_seismology_core import (
    NODE_CATALOG,
    get_active_nodes,
    load_mock_events,
    load_state,
    parse_node_filter,
    poll_nodes,
    save_state,
    should_publish_event,
)
from fdsn_seismology_core.fdsn_client import EarthquakeRecord, prune_seen_events
from fdsn_seismology_producer_data import Earthquake, Node
from fdsn_seismology_producer_kafka_producer.producer import OrgFdsnEventKafkaEventProducer
from datetime import datetime

logger = logging.getLogger(__name__)



def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}



def _null_if_empty(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None



def _build_node_data(node: dict[str, str | None]) -> Node:
    return Node(
        node_id=str(node["node_id"]),
        name=str(node["name"]),
        base_url=str(node["base_url"]),
        coverage=str(node["coverage"]),
        country=node.get("country"),
    )



def _build_earthquake_data(event: EarthquakeRecord) -> Earthquake:
    return Earthquake(
        event_id=event.event_id,
        time=datetime.fromisoformat(event.time),
        latitude=event.latitude,
        longitude=event.longitude,
        depth_km=event.depth_km,
        author=event.author,
        catalog=event.catalog,
        contributor=event.contributor,
        contributor_id=event.contributor_id,
        magnitude_type=event.magnitude_type,
        magnitude=event.magnitude,
        magnitude_author=event.magnitude_author,
        event_location_name=event.event_location_name,
        event_type=event.event_type,
        node_url=event.node_url,
    )



def _parse_connection_string(connection_string: str) -> tuple[dict[str, str], str | None]:
    parts: dict[str, str] = {}
    for part in connection_string.split(";"):
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        parts[key.strip()] = value.strip().strip('"')

    if "BootstrapServer" in parts:
        config: dict[str, str] = {
            "bootstrap.servers": parts["BootstrapServer"],
        }
        topic = parts.get("EntityPath")
        username = _null_if_empty(os.getenv("SASL_USERNAME"))
        password = _null_if_empty(os.getenv("SASL_PASSWORD"))
        tls_enabled = _env_flag("KAFKA_ENABLE_TLS", default=True)
        if username and password:
            config.update(
                {
                    "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                    "sasl.mechanisms": os.getenv("SASL_MECHANISM", "PLAIN"),
                    "sasl.username": username,
                    "sasl.password": password,
                }
            )
        elif tls_enabled:
            config["security.protocol"] = "SSL"
        else:
            config["security.protocol"] = "PLAINTEXT"
        return config, topic

    return OrgFdsnEventKafkaEventProducer.parse_connection_string(connection_string)



def _build_kafka_event_producer(content_mode: str) -> OrgFdsnEventKafkaEventProducer:
    connection_string = _null_if_empty(os.getenv("CONNECTION_STRING"))
    if connection_string:
        config, topic = _parse_connection_string(connection_string)
        override_topic = _null_if_empty(os.getenv("KAFKA_TOPIC"))
        return OrgFdsnEventKafkaEventProducer(Producer(config), override_topic or topic or "fdsn-seismology", content_mode)  # type: ignore[arg-type]

    bootstrap = _null_if_empty(os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    topic = _null_if_empty(os.getenv("KAFKA_TOPIC")) or "fdsn-seismology"
    if not bootstrap:
        raise RuntimeError("Set CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS before running the Kafka feeder.")

    tls_enabled = _env_flag("KAFKA_ENABLE_TLS", default=True)
    config: dict[str, Any] = {"bootstrap.servers": bootstrap}
    username = _null_if_empty(os.getenv("SASL_USERNAME"))
    password = _null_if_empty(os.getenv("SASL_PASSWORD"))
    if username and password:
        config.update(
            {
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.mechanisms": os.getenv("SASL_MECHANISM", "PLAIN"),
                "sasl.username": username,
                "sasl.password": password,
            }
        )
    else:
        config["security.protocol"] = "SSL" if tls_enabled else "PLAINTEXT"
    return OrgFdsnEventKafkaEventProducer(Producer(config), topic, content_mode)  # type: ignore[arg-type]



def _publish_nodes(
    producer: OrgFdsnEventKafkaEventProducer,
    active_nodes: dict[str, dict[str, str | None]],
) -> None:
    for node_id, node in active_nodes.items():
        producer.send_org_fdsn_event_kafka_node(
            _base_url=str(node["base_url"]),
            _node_id=node_id,
            data=_build_node_data(node),
            flush_producer=False,
        )
    producer.producer.flush()



def feed(args: argparse.Namespace) -> None:
    active_nodes = get_active_nodes(
        parse_node_filter(args.nodes),
        parse_node_filter(args.exclude_nodes),
        sources_file=args.fdsn_sources_file,
    )
    if not active_nodes:
        raise RuntimeError("Node selection is empty after include/exclude filters.")

    producer = _build_kafka_event_producer(args.content_mode)
    state = load_state(args.state_file)
    session = requests.Session()

    logger.info("Publishing %d FDSN node reference records", len(active_nodes))
    _publish_nodes(producer, active_nodes)

    try:
        while True:
            published = 0
            cycle_started = time.time()
            if args.mock:
                events = load_mock_events(active_nodes)
            else:
                events = poll_nodes(
                    session,
                    active_nodes,
                    state,
                    poll_interval_seconds=args.poll_interval,
                    min_magnitude=args.min_magnitude,
                    limit=args.limit,
                )
            for event in events:
                if not should_publish_event(event, state):
                    continue
                producer.send_org_fdsn_event_kafka_earthquake(
                    _node_url=event.node_url,
                    _contributor=event.contributor,
                    _event_id=event.event_id,
                    _time=event.time,
                    data=_build_earthquake_data(event),
                    flush_producer=False,
                )
                state.seen_event_times[event.dedupe_key] = event.time
                published += 1
            producer.producer.flush()
            prune_seen_events(state)
            save_state(args.state_file, state)
            logger.info("Published %d earthquake events from %d active node(s)", published, len(active_nodes))
            if args.once or args.mock:
                logger.info("--once mode: exiting after one polling cycle")
                break
            sleep_seconds = max(0.0, args.poll_interval - (time.time() - cycle_started))
            if sleep_seconds:
                time.sleep(sleep_seconds)
    finally:
        session.close()



def _print_nodes() -> None:
    for node_id, node in NODE_CATALOG.items():
        print(f"{node_id}\t{node['name']}\t{node['coverage']}\t{node['base_url']}")



def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="FDSN Seismology Kafka bridge")
    parser.add_argument("command", nargs="?", default="feed")
    parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL", "60")))
    parser.add_argument("--min-magnitude", type=float, default=float(os.getenv("MIN_MAGNITUDE", "0")))
    parser.add_argument("--nodes", default=os.getenv("FDSN_NODES") or os.getenv("NODES", ""))
    parser.add_argument("--exclude-nodes", default=os.getenv("FDSN_EXCLUDE_NODES") or os.getenv("EXCLUDE_NODES", ""))
    parser.add_argument("--fdsn-sources-file", default=os.getenv("FDSN_SOURCES_FILE", ""))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.fdsn_seismology_state.json")))
    parser.add_argument("--limit", type=int, default=int(os.getenv("FDSN_LIMIT", "500")))
    parser.add_argument("--content-mode", choices=("structured", "binary"), default=os.getenv("KAFKA_CONTENT_MODE", "structured"))
    parser.add_argument("--once", action="store_true", default=_env_flag("ONCE_MODE", default=False))
    parser.add_argument("--mock", action="store_true", default=_env_flag("FDSN_MOCK", default=False),
                        help="Emit a deterministic canned earthquake corpus instead of polling live FDSN nodes (one cycle, then exit). Used by the Docker E2E flow test.")
    args = parser.parse_args()

    if args.command == "list-nodes":
        _print_nodes()
        return
    if args.command != "feed":
        parser.error("supported commands are 'feed' and 'list-nodes'")

    try:
        feed(args)
    except KeyboardInterrupt:
        logger.info("Stopping feeder")
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("FDSN seismology Kafka feeder failed: %s", exc)
        raise


if __name__ == "__main__":
    main()
