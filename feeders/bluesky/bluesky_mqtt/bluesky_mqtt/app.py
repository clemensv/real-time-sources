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

from bluesky_core.bluesky import DEFAULT_FIREHOSE_URL, USER_AGENT, iter_firehose_events, normalize_segment
from bluesky_mqtt_producer_data import Block, Follow, Like, Post, Profile, Repost
from bluesky_mqtt_producer_mqtt_client.client import BlueskyFirehoseMqttMqttClient

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


def _build_data(event):
    if event.event_type == 'Bluesky.Feed.Post':
        return Post(**event.payload)
    if event.event_type == 'Bluesky.Feed.Like':
        return Like(**event.payload)
    if event.event_type == 'Bluesky.Feed.Repost':
        return Repost(**event.payload)
    if event.event_type == 'Bluesky.Graph.Follow':
        return Follow(**event.payload)
    if event.event_type == 'Bluesky.Graph.Block':
        return Block(**event.payload)
    return Profile(**event.payload)


class BlueskyMqttBridge:
    def __init__(self, client: BlueskyFirehoseMqttMqttClient, *, firehose_url: str = DEFAULT_FIREHOSE_URL, collections: Optional[list[str]] = None) -> None:
        self.client = client
        self.firehose_url = firehose_url
        self.collections = collections
        self._count = 0

    async def run(self, max_events: Optional[int] = None) -> None:
        async for event in iter_firehose_events(firehose_url=self.firehose_url, collections=self.collections, user_agent=USER_AGENT):
            data = _build_data(event)
            method = getattr(self.client, 'publish_' + event.event_type.lower().replace('.', '_') + '_mqtt')
            await method(firehoseurl=self.firehose_url, did=normalize_segment(event.did), collection=normalize_segment(event.collection), lang=normalize_segment(event.lang), data=data, qos=0, retain=False)
            self._count += 1
            if max_events and self._count >= max_events:
                return


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme == "mqtts" else 1883), scheme == "mqtts"


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(username=args.mqtt_username, password=args.mqtt_password or '', client_id=args.mqtt_client_id or '', auth_mode=os.getenv('MQTT_AUTH_MODE'))
    paho_client = mqtt.Client(client_id=resolved_client_id or '', callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or entra_props is not None:
        paho_client.tls_set()
    loop = asyncio.get_running_loop()
    client = BlueskyFirehoseMqttMqttClient(client=paho_client, content_mode='binary', loop=loop)
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)
    collections = [c.strip() for c in args.collections.split(',') if c.strip()] if args.collections else None
    try:
        await BlueskyMqttBridge(client, firehose_url=args.firehose_url, collections=collections).run(max_events=args.max_events)
    finally:
        await client.disconnect()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    p = argparse.ArgumentParser(description='Bluesky firehose -> MQTT/UNS bridge')
    sub = p.add_subparsers(dest='command')
    feed = sub.add_parser('feed', help='Stream firehose to MQTT')
    feed.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL', 'mqtt://localhost:1883'))
    feed.add_argument('--mqtt-enable-tls', action='store_true', default=os.getenv('MQTT_ENABLE_TLS', 'false').lower() in ('true', '1', 'yes'))
    feed.add_argument('--mqtt-username', default=os.getenv('MQTT_USERNAME'))
    feed.add_argument('--mqtt-password', default=os.getenv('MQTT_PASSWORD'))
    feed.add_argument('--mqtt-client-id', default=os.getenv('MQTT_CLIENT_ID'))
    feed.add_argument('--firehose-url', default=os.getenv('BLUESKY_FIREHOSE_URL', DEFAULT_FIREHOSE_URL))
    feed.add_argument('--collections', default=os.getenv('BLUESKY_COLLECTIONS', ''))
    feed.add_argument('--max-events', type=int, default=int(os.getenv('BLUESKY_MAX_EVENTS', '0')) or None)
    args = p.parse_args()
    if args.command != 'feed':
        p.print_help()
        sys.exit(1)
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info('Shutting down')


if __name__ == '__main__':
    main()
