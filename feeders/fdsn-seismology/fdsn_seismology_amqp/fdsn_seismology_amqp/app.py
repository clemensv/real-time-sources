from __future__ import annotations

import argparse
import logging
import os
import time
from urllib.parse import urlparse

import requests

from fdsn_seismology_amqp_producer_amqp_producer.producer import OrgFdsnEventAmqpProducer
from fdsn_seismology_amqp_producer_data import Earthquake, Node
from fdsn_seismology_core import get_active_nodes, load_mock_events, load_state, parse_node_filter, poll_nodes, save_state, should_publish_event
from fdsn_seismology_core.fdsn_client import EarthquakeRecord, prune_seen_events

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"



def _null_if_empty(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None



def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}



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
        time=event.time,
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



def _parse_broker_url(url: str) -> tuple[str, int, bool, str | None, str | None, str | None]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    address = parsed.path.lstrip("/") or None
    return (
        parsed.hostname or "localhost",
        parsed.port or (5671 if tls else 5672),
        tls,
        parsed.username or None,
        parsed.password or None,
        address,
    )



def _build_producer(args: argparse.Namespace) -> OrgFdsnEventAmqpProducer:
    host = args.host
    port = args.port
    address = args.address
    username = _null_if_empty(args.username)
    password = _null_if_empty(args.password)
    use_tls = args.tls

    if args.broker_url:
        host, port, parsed_tls, parsed_user, parsed_password, parsed_address = _parse_broker_url(args.broker_url)
        use_tls = parsed_tls
        username = username or parsed_user
        password = password or parsed_password
        address = address or parsed_address or "fdsn-seismology"

    if not address:
        address = "fdsn-seismology"

    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        return OrgFdsnEventAmqpProducer(
            host=host,
            address=address,
            port=port,
            content_mode=args.content_mode,
            credential=credential,
            entra_audience=args.entra_audience,
            use_tls=use_tls,
        )

    if args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP_AUTH_MODE=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return OrgFdsnEventAmqpProducer(
            host=host,
            address=address,
            port=port,
            content_mode=args.content_mode,
            sas_key_name=args.sas_key_name,
            sas_key=args.sas_key,
            use_tls=use_tls,
        )

    return OrgFdsnEventAmqpProducer(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        content_mode=args.content_mode,
        use_tls=use_tls,
    )



def _publish_nodes(
    producer: OrgFdsnEventAmqpProducer,
    active_nodes: dict[str, dict[str, str | None]],
) -> None:
    for node_id, node in active_nodes.items():
        producer.send_node(
            data=_build_node_data(node),
            _base_url=str(node["base_url"]),
            _node_id=node_id,
        )



def feed(args: argparse.Namespace) -> None:
    active_nodes = get_active_nodes(parse_node_filter(args.nodes), parse_node_filter(args.exclude_nodes))
    if not active_nodes:
        raise RuntimeError("Node selection is empty after include/exclude filters.")

    producer = _build_producer(args)
    state = load_state(args.state_file)
    session = requests.Session()

    try:
        logger.info("Publishing %d FDSN node reference records", len(active_nodes))
        _publish_nodes(producer, active_nodes)
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
                producer.send_earthquake(
                    data=_build_earthquake_data(event),
                    _node_url=event.node_url,
                    _contributor=event.contributor,
                    _event_id=event.event_id,
                    _time=event.time,
                )
                state.seen_event_times[event.dedupe_key] = event.time
                published += 1
            prune_seen_events(state)
            save_state(args.state_file, state)
            logger.info("Published %d AMQP earthquake events from %d active node(s)", published, len(active_nodes))
            if args.once or args.mock:
                logger.info("--once mode: exiting after one polling cycle")
                break
            sleep_seconds = max(0.0, args.poll_interval - (time.time() - cycle_started))
            if sleep_seconds:
                time.sleep(sleep_seconds)
    finally:
        session.close()
        try:
            producer.close()
        except Exception:  # pylint: disable=broad-except
            pass



def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="FDSN Seismology AMQP bridge")
    parser.add_argument("command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "5672")))
    parser.add_argument("--tls", action="store_true", default=_env_flag("AMQP_TLS", default=False))
    parser.add_argument("--address", default=_null_if_empty(os.getenv("AMQP_ADDRESS")) or "fdsn-seismology")
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--auth-mode", choices=("password", "sas", "entra"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--sas-key-name", default=_null_if_empty(os.getenv("AMQP_SAS_KEY_NAME")))
    parser.add_argument("--sas-key", default=_null_if_empty(os.getenv("AMQP_SAS_KEY")))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=_null_if_empty(os.getenv("AMQP_ENTRA_CLIENT_ID")))
    parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL", "60")))
    parser.add_argument("--min-magnitude", type=float, default=float(os.getenv("MIN_MAGNITUDE", "0")))
    parser.add_argument("--nodes", default=os.getenv("NODES", ""))
    parser.add_argument("--exclude-nodes", default=os.getenv("EXCLUDE_NODES", ""))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.fdsn_seismology_state_amqp.json")))
    parser.add_argument("--limit", type=int, default=int(os.getenv("FDSN_LIMIT", "500")))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--once", action="store_true", default=_env_flag("ONCE_MODE", default=False))
    parser.add_argument("--mock", action="store_true", default=_env_flag("FDSN_MOCK", default=False),
                        help="Emit a deterministic canned earthquake corpus instead of polling live FDSN nodes (one cycle, then exit). Used by the Docker E2E flow test.")
    args = parser.parse_args()

    if args.command != "feed":
        parser.error("only the 'feed' command is supported")
    feed(args)


if __name__ == "__main__":
    main()
