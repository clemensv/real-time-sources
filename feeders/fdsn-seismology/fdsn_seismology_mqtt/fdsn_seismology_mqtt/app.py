from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties
import requests

from fdsn_seismology_core import get_active_nodes, load_mock_events, load_state, parse_node_filter, poll_nodes, save_state, should_publish_event
from fdsn_seismology_core.fdsn_client import EarthquakeRecord, prune_seen_events
from fdsn_seismology_mqtt_producer_data import Earthquake, Node
from fdsn_seismology_mqtt_producer_mqtt_client.client import OrgFdsnEventMqttMqttClient

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"



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



def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls



def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple[str, datetime]:
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

    credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
    scope = audience if audience.endswith("/.default") else f"{audience}/.default"
    token = credential.get_token(scope)
    return token.token, datetime.fromtimestamp(token.expires_on, tz=timezone.utc)


async def _entra_token_refresh_loop(
    paho_client: mqtt.Client,
    broker_host: str,
    broker_port: int,
    keepalive: int,
    audience: str,
    client_id: Optional[str],
    expires_at: datetime,
) -> None:
    while True:
        sleep_seconds = max(60.0, (expires_at - datetime.now(timezone.utc)).total_seconds() - 300.0)
        await asyncio.sleep(sleep_seconds)
        try:
            token, expires_at = _acquire_entra_token(audience, client_id)
            props = Properties(PacketTypes.CONNECT)
            props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
            props.AuthenticationData = token.encode("utf-8")
            try:
                paho_client.disconnect()
            except Exception:  # pylint: disable=broad-except
                pass
            paho_client.connect(
                broker_host,
                broker_port,
                keepalive=keepalive,
                clean_start=True,
                properties=props,
            )
            logger.info("Refreshed Entra JWT for MQTT broker")
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to refresh MQTT Entra JWT: %s", exc)
            await asyncio.sleep(60)


async def _publish_nodes(
    client: OrgFdsnEventMqttMqttClient,
    active_nodes: dict[str, dict[str, str | None]],
) -> None:
    for node_id, node in active_nodes.items():
        await client.publish_org_fdsn_event_mqtt_node(
            base_url=str(node["base_url"]),
            node_id=node_id,
            data=_build_node_data(node),
        )


async def feed(args: argparse.Namespace) -> None:
    active_nodes = get_active_nodes(parse_node_filter(args.nodes), parse_node_filter(args.exclude_nodes))
    if not active_nodes:
        raise RuntimeError("Node selection is empty after include/exclude filters.")

    broker_host, broker_port, tls = _parse_broker_url(args.broker_url)
    auth_mode = args.auth_mode
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=args.client_id or "",
        protocol=MQTTv5,
    )

    refresh_task: Optional[asyncio.Task] = None
    connect_properties: Optional[Properties] = None
    expires_at: Optional[datetime] = None
    if auth_mode == "entra":
        token, expires_at = _acquire_entra_token(args.entra_audience, args.entra_client_id)
        connect_properties = Properties(PacketTypes.CONNECT)
        connect_properties.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
        connect_properties.AuthenticationData = token.encode("utf-8")
    elif args.username:
        paho_client.username_pw_set(args.username, args.password or "")

    if tls or auth_mode == "entra":
        paho_client.tls_set()

    mqtt_client = OrgFdsnEventMqttMqttClient(
        client=paho_client,
        content_mode=args.content_mode,
        loop=asyncio.get_running_loop(),
    )

    if auth_mode == "entra":
        paho_client.connect(
            broker_host,
            broker_port,
            keepalive=60,
            clean_start=True,
            properties=connect_properties,
        )
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)

    if auth_mode == "entra" and expires_at is not None:
        refresh_task = asyncio.create_task(
            _entra_token_refresh_loop(
                paho_client,
                broker_host,
                broker_port,
                60,
                args.entra_audience,
                args.entra_client_id,
                expires_at,
            )
        )

    state = load_state(args.state_file)
    session = requests.Session()

    try:
        logger.info("Publishing %d FDSN node reference records", len(active_nodes))
        await _publish_nodes(mqtt_client, active_nodes)
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
                await mqtt_client.publish_org_fdsn_event_mqtt_earthquake(
                    node_url=event.node_url,
                    contributor=event.contributor,
                    event_id=event.event_id,
                    _time=event.time,
                    data=_build_earthquake_data(event),
                )
                state.seen_event_times[event.dedupe_key] = event.time
                published += 1
            prune_seen_events(state)
            save_state(args.state_file, state)
            logger.info("Published %d MQTT earthquake events from %d active node(s)", published, len(active_nodes))
            if args.once or args.mock:
                logger.info("--once mode: exiting after one polling cycle")
                break
            sleep_seconds = max(0.0, args.poll_interval - (time.time() - cycle_started))
            if sleep_seconds:
                await asyncio.sleep(sleep_seconds)
    finally:
        session.close()
        if refresh_task is not None:
            refresh_task.cancel()
        if auth_mode == "entra":
            paho_client.loop_stop()
            paho_client.disconnect()
        else:
            await mqtt_client.disconnect()



def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="FDSN Seismology MQTT bridge")
    parser.add_argument("command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL", "60")))
    parser.add_argument("--min-magnitude", type=float, default=float(os.getenv("MIN_MAGNITUDE", "0")))
    parser.add_argument("--nodes", default=os.getenv("NODES", ""))
    parser.add_argument("--exclude-nodes", default=os.getenv("EXCLUDE_NODES", ""))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.fdsn_seismology_state_mqtt.json")))
    parser.add_argument("--limit", type=int, default=int(os.getenv("FDSN_LIMIT", "500")))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    parser.add_argument("--once", action="store_true", default=_env_flag("ONCE_MODE", default=False))
    parser.add_argument("--mock", action="store_true", default=_env_flag("FDSN_MOCK", default=False),
                        help="Emit a deterministic canned earthquake corpus instead of polling live FDSN nodes (one cycle, then exit). Used by the Docker E2E flow test.")
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", "fdsn-seismology-mqtt"))
    parser.add_argument("--auth-mode", choices=("password", "entra"), default=os.getenv("MQTT_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE))
    parser.add_argument("--entra-client-id", default=_null_if_empty(os.getenv("MQTT_ENTRA_CLIENT_ID")))
    args = parser.parse_args()

    if args.command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(feed(args))


if __name__ == "__main__":
    main()
