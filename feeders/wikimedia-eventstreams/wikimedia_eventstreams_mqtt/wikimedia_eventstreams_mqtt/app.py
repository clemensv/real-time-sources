from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from wikimedia_eventstreams_core.wikimedia_eventstreams import (
    DEFAULT_USER_AGENT,
    STREAM_URL,
    iter_recentchange_payloads,
    normalize_recent_change,
)
from wikimedia_eventstreams_mqtt_producer_data import RecentChange
from wikimedia_eventstreams_mqtt_producer_mqtt_client.client import WikimediaEventStreamsMqttMqttClient

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


def _norm_segment(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value).strip().lower().replace("/", "_").replace("#", "_").replace("+", "_")


class WikimediaMqttBridge:
    def __init__(self, client: WikimediaEventStreamsMqttMqttClient, *, stream_url: str = STREAM_URL, user_agent: str = DEFAULT_USER_AGENT) -> None:
        self.client = client
        self.stream_url = stream_url
        self.user_agent = user_agent
        self._count = 0

    async def publish_event(self, payload: dict) -> bool:
        meta = payload.get("meta")
        if not isinstance(meta, dict) or meta.get("domain") == "canary":
            return False
        event_id = meta.get("id")
        event_time = meta.get("dt")
        wiki = payload.get("wiki")
        if not event_id or not event_time or not wiki:
            return False
        normalized = normalize_recent_change(payload)
        data = RecentChange.from_serializer_dict(normalized)
        await self.client.publish_wikimedia_event_streams_recent_change_mqtt(
            wiki=_norm_segment(wiki),
            namespace=_norm_segment(normalized["namespace"]),
            event_id=_norm_segment(str(event_id)),
            event_time=str(event_time),
            data=data,
            qos=0,
            retain=False,
        )
        self._count += 1
        return True

    async def run(self, max_events: Optional[int] = None) -> None:
        async for payload in iter_recentchange_payloads(stream_url=self.stream_url, user_agent=self.user_agent):
            try:
                await self.publish_event(payload)
            except Exception as exc:
                logger.warning("publish failed: %s", exc)
                continue
            if max_events and self._count >= max_events:
                return


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme == "mqtts" else 1883), scheme == "mqtts"


async def _emit_mock_mqtt(client: WikimediaEventStreamsMqttMqttClient) -> None:
    """Emit synthetic RecentChange events for deterministic E2E testing."""
    from datetime import datetime, timezone
    for i in range(4):
        data = RecentChange.from_serializer_dict({
            "wiki": "enwiki",
            "type": "edit",
            "namespace": "0",
            "title": f"Mock_Article_{i}",
            "comment": "mock edit",
            "user": "MockUser",
            "bot": False,
            "minor": False,
            "patrolled": False,
            "length_old": 100 + i,
            "length_new": 110 + i,
            "revision_old": 1000 + i,
            "revision_new": 1001 + i,
            "server_url": "https://en.wikipedia.org",
            "server_name": "en.wikipedia.org",
            "event_id": f"mock-{i:08d}",
            "event_time": datetime(2024, 1, 1, 0, 0, i, tzinfo=timezone.utc).isoformat(),
        })
        await client.publish_wikimedia_event_streams_recent_change_mqtt(
            wiki="enwiki",
            namespace="0",
            event_id=f"mock-{i:08d}",
            event_time=datetime(2024, 1, 1, 0, 0, i, tzinfo=timezone.utc).isoformat(),
            data=data,
            qos=0,
            retain=False,
        )
    await asyncio.sleep(1)
    logger.info("Mock mode: emitted 4 synthetic RecentChange events via MQTT")


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
    client = WikimediaEventStreamsMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)
    try:
        if getattr(args, 'mock', False):
            await _emit_mock_mqtt(client)
        else:
            await WikimediaMqttBridge(client, stream_url=args.stream_url, user_agent=args.user_agent).run(max_events=args.max_events)
    finally:
        await client.disconnect()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Wikimedia EventStreams -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream Wikimedia recentchange to MQTT")
    feed.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true", default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--stream-url", default=os.getenv("WIKIMEDIA_EVENTSTREAMS_URL", STREAM_URL))
    feed.add_argument("--user-agent", default=os.getenv("WIKIMEDIA_EVENTSTREAMS_USER_AGENT", DEFAULT_USER_AGENT))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("WIKIMEDIA_EVENTSTREAMS_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true", default=os.getenv("WIKIMEDIA_EVENTSTREAMS_MOCK", "").lower() in ("1", "true", "yes"))
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
