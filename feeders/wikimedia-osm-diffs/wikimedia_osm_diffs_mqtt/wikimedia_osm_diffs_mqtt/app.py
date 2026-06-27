from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from wikimedia_osm_diffs_core.wikimedia_osm_diffs import (
    DEFAULT_STATE_FILE,
    DEFAULT_USER_AGENT,
    DIFF_BASE_URL,
    STATE_URL,
    StateStore,
    build_session,
    fetch_sequence_changes,
    fetch_state,
    sequence_to_url,
)
from wikimedia_osm_diffs_mqtt_producer_data import MapChange, ReplicationState
from wikimedia_osm_diffs_mqtt_producer_mqtt_client.client import OrgOpenStreetMapDiffsMqttMqttClient

logger = logging.getLogger(__name__)


def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id
    request = Request("http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params), headers={"Metadata": "true"})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)


def _resolve_mqtt_connection_settings(*, username=None, password=None, client_id=None, auth_mode=None):
    resolved_client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    auth_mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"
    if auth_mode != "entra":
        return resolved_client_id, str(username or ""), str(password or ""), None
    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")
    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    connect_props.AuthenticationMethod = "OAUTH2-JWT"
    connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, connect_props


class OsmDiffsMqttBridge:
    def __init__(self, client: OrgOpenStreetMapDiffsMqttMqttClient, *, state_store: Optional[StateStore] = None, state_url: str = STATE_URL, diff_base_url: str = DIFF_BASE_URL, user_agent: str = DEFAULT_USER_AGENT, poll_interval: int = 60, max_retry_delay: int = 120, once: bool = False) -> None:
        self.client = client
        self._state_store = state_store
        self._state_url = state_url
        self._diff_base_url = diff_base_url
        self._poll_interval = poll_interval
        self._max_retry_delay = max_retry_delay
        self._once = once
        self._last_sequence = state_store.load() if state_store else None
        self._session = build_session(user_agent)
        self._total_events = 0

    async def run(self) -> None:
        retry_delay = 1
        while True:
            try:
                await self._poll_cycle()
                retry_delay = 1
                if self._once:
                    return
                await asyncio.sleep(self._poll_interval)
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.warning("Poll cycle error: %s. Retrying in %ds.", exc, retry_delay)
                if self._once:
                    return
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self._max_retry_delay)

    async def _poll_cycle(self) -> None:
        state = fetch_state(self._session, self._state_url)
        if state is None:
            return
        current_seq = state["sequence_number"]
        current_ts = state["timestamp"]
        if self._last_sequence is not None and current_seq <= self._last_sequence:
            return
        start_seq = (self._last_sequence + 1) if self._last_sequence is not None else current_seq
        start_seq = max(start_seq, current_seq - 4)
        for seq in range(start_seq, current_seq + 1):
            await self._process_sequence(seq)
        await self._publish_replication_state(current_seq, current_ts)
        self._last_sequence = current_seq
        if self._state_store:
            self._state_store.save(current_seq)

    async def _process_sequence(self, seq: int) -> None:
        for change in fetch_sequence_changes(self._session, seq, self._diff_base_url):
            await self._publish_change(change)

    async def _publish_change(self, change: dict) -> None:
        data = MapChange.from_serializer_dict(change)
        publish = getattr(self.client, f"publish_org_open_street_map_diffs_mqtt_{change['element_type']}")
        await publish(geohash5=data.geohash5 or "nogeo", element_id=str(data.element_id), data=data, qos=0, retain=False)
        self._total_events += 1

    async def _publish_replication_state(self, seq: int, ts: datetime.datetime) -> None:
        state_data = ReplicationState(sequence_number=seq, timestamp=ts, source_url=sequence_to_url(seq, self._diff_base_url))
        await self.client.publish_org_open_street_map_diffs_mqtt_replication_state(data=state_data, qos=0, retain=True)


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme == "mqtts" else 1883), scheme == "mqtts"


async def _emit_mock_mqtt(client: OrgOpenStreetMapDiffsMqttMqttClient) -> None:
    """Emit synthetic MapChange + ReplicationState for deterministic E2E testing."""
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    # Emit 1 ReplicationState (retained)
    state = ReplicationState.from_serializer_dict({
        "sequence_number": 6000000,
        "timestamp": now.isoformat(),
        "source_url": "https://planet.openstreetmap.org/replication/minute",
    })
    await client.publish_org_open_street_map_diffs_mqtt_replication_state(
        data=state,
        qos=0,
        retain=True,
        _time=now.isoformat(),
    )
    # Emit 1 node (with coordinates → geohash5)
    node_change = MapChange.from_serializer_dict({
        "changeset_id": 150000001,
        "change_type": "create",
        "element_type": "node",
        "element_id": 10000001,
        "geohash5": "gcpvj",
        "version": 1,
        "timestamp": now.isoformat(),
        "user_id": 12345,
        "user_name": "mockuser",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "tags": {"name": "Mock Node"},
        "sequence_number": 6000000,
    })
    await client.publish_org_open_street_map_diffs_mqtt_node(
        geohash5="gcpvj",
        element_id="10000001",
        data=node_change,
        qos=0,
        retain=False,
        _time=now.isoformat(),
    )
    # Emit 1 way (no coordinates → nogeo)
    way_change = MapChange.from_serializer_dict({
        "changeset_id": 150000002,
        "change_type": "modify",
        "element_type": "way",
        "element_id": 20000001,
        "geohash5": "nogeo",
        "version": 2,
        "timestamp": now.isoformat(),
        "user_id": 12345,
        "user_name": "mockuser",
        "latitude": None,
        "longitude": None,
        "tags": {"highway": "residential"},
        "sequence_number": 6000000,
    })
    await client.publish_org_open_street_map_diffs_mqtt_way(
        geohash5="nogeo",
        element_id="20000001",
        data=way_change,
        qos=0,
        retain=False,
        _time=now.isoformat(),
    )
    # Emit 1 relation (no coordinates → nogeo)
    rel_change = MapChange.from_serializer_dict({
        "changeset_id": 150000003,
        "change_type": "delete",
        "element_type": "relation",
        "element_id": 30000001,
        "geohash5": "nogeo",
        "version": 3,
        "timestamp": now.isoformat(),
        "user_id": 12345,
        "user_name": "mockuser",
        "latitude": None,
        "longitude": None,
        "tags": {"type": "route"},
        "sequence_number": 6000000,
    })
    await client.publish_org_open_street_map_diffs_mqtt_relation(
        geohash5="nogeo",
        element_id="30000001",
        data=rel_change,
        qos=0,
        retain=False,
        _time=now.isoformat(),
    )
    await asyncio.sleep(1)
    logger.info("Mock mode: emitted 4 synthetic OSM diff events via MQTT")


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(username=args.mqtt_username, password=args.mqtt_password or "", client_id=args.mqtt_client_id or "", auth_mode=os.getenv("MQTT_AUTH_MODE"))
    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or entra_props is not None:
        paho_client.tls_set()
    loop = asyncio.get_running_loop()
    client = OrgOpenStreetMapDiffsMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)
    state_store = StateStore(args.state_file) if args.state_file else None
    try:
        if getattr(args, 'mock', False):
            await _emit_mock_mqtt(client)
        else:
            await OsmDiffsMqttBridge(client, state_store=state_store, state_url=args.state_url, diff_base_url=args.diff_base_url, poll_interval=args.poll_interval, once=args.once).run()
    finally:
        await client.disconnect()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="OSM minutely diffs -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream OSM diffs to MQTT")
    feed.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true", default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--state-url", default=os.getenv("OSM_DIFFS_STATE_URL", STATE_URL))
    feed.add_argument("--diff-base-url", default=os.getenv("OSM_DIFFS_BASE_URL", DIFF_BASE_URL))
    feed.add_argument("--state-file", default=os.getenv("OSM_DIFFS_STATE_FILE", DEFAULT_STATE_FILE))
    feed.add_argument("--poll-interval", type=int, default=int(os.getenv("OSM_DIFFS_POLL_INTERVAL", "60")))
    feed.add_argument("--once", action="store_true", default=os.getenv("OSM_DIFFS_ONCE", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mock", action="store_true", default=os.getenv("OSM_DIFFS_MOCK", "").lower() in ("1", "true", "yes"))
    args = p.parse_args()
    if args.command != "feed":
        p.print_help()
        sys.exit(1)
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info("Shutting down")


if __name__ == "__main__":
    main()
