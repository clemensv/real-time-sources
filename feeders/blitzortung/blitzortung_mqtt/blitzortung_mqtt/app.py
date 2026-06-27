from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
import websockets
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from blitzortung_core.blitzortung import DEFAULT_BBOX, DEFAULT_USER_AGENT, DEFAULT_WS_URLS, normalize_stroke
from blitzortung_mqtt_producer_data import LightningStroke
from blitzortung_mqtt_producer_mqtt_client.client import BlitzortungLightningMqttMqttClient

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


class BlitzortungMqttBridge:
    def __init__(self, client: BlitzortungLightningMqttMqttClient, *, ws_urls=DEFAULT_WS_URLS, bbox=DEFAULT_BBOX, user_agent: str = DEFAULT_USER_AGENT) -> None:
        self.client = client
        self.ws_urls = list(ws_urls)
        self.bbox = bbox
        self.user_agent = user_agent
        self._count = 0

    async def run(self, max_events: Optional[int] = None) -> None:
        bbox_msg = json.dumps({"west": self.bbox[3], "east": self.bbox[1], "north": self.bbox[0], "south": self.bbox[2], "limit": 0})
        retry_delay = 1
        max_retry_delay = 60
        url_idx = 0
        while True:
            url = self.ws_urls[url_idx % len(self.ws_urls)]
            try:
                async with websockets.connect(url, user_agent_header=self.user_agent, max_size=2**22) as ws:
                    await ws.send(bbox_msg)
                    logger.info("Connected to Blitzortung WS at %s", url)
                    retry_delay = 1
                    async for raw in ws:
                        try:
                            envelope = json.loads(raw)
                        except (TypeError, ValueError):
                            continue
                        await self._dispatch_envelope(envelope)
                        if max_events and self._count >= max_events:
                            return
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.error("Blitzortung WS error: %s. Retrying in %ds", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)
                url_idx += 1

    async def _dispatch_envelope(self, envelope: Any) -> None:
        if isinstance(envelope, dict) and isinstance(envelope.get("strokes"), list):
            for raw in envelope["strokes"]:
                await self._publish_one(raw)
        elif isinstance(envelope, dict):
            await self._publish_one(envelope)
        elif isinstance(envelope, list):
            for raw in envelope:
                await self._publish_one(raw)

    async def _publish_one(self, raw: dict[str, Any]) -> None:
        try:
            data = LightningStroke.from_serializer_dict(normalize_stroke(raw))
        except (KeyError, TypeError, ValueError):
            return
        await self.client.publish_blitzortung_lightning_mqtt_lightning_stroke(
            source_id=str(data.source_id),
            geohash5=data.geohash5,
            geohash7=data.geohash7,
            stroke_id=data.stroke_id,
            _time=data.event_time,
            data=data,
            qos=0,
            retain=False,
        )
        self._count += 1


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme == "mqtts" else 1883), scheme == "mqtts"


async def _emit_mock_mqtt(client) -> None:
    """Emit synthetic lightning strokes for deterministic E2E testing."""
    from datetime import datetime, timezone
    base_time_ms = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
    for index in range(3):
        stroke_raw = {
            "src": 1, "id": 9_000_000_000 + index, "time": base_time_ms + index,
            "lat": 50.0 + index * 0.1, "lon": 8.0 + index * 0.1,
            "srv": 1, "del": 0, "dev": 1000.0, "sta": {"100": 0, "101": 1},
        }
        data = LightningStroke.from_serializer_dict(normalize_stroke(stroke_raw))
        await client.publish_blitzortung_lightning_mqtt_lightning_stroke(
            source_id=str(data.source_id),
            geohash5=data.geohash5,
            geohash7=data.geohash7,
            stroke_id=data.stroke_id,
            _time=data.event_time,
            data=data,
            qos=0,
            retain=False,
        )
    await asyncio.sleep(1)
    logger.info("Mock mode: emitted 3 synthetic Blitzortung strokes via MQTT")


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(
        username=args.mqtt_username,
        password=args.mqtt_password or "",
        client_id=args.mqtt_client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )
    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or entra_props is not None:
        paho_client.tls_set()
    loop = asyncio.get_running_loop()
    client = BlitzortungLightningMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)
    try:
        if getattr(args, 'mock', False):
            await _emit_mock_mqtt(client)
        else:
            await BlitzortungMqttBridge(client).run(max_events=args.max_events)
    finally:
        await client.disconnect()


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(description="Blitzortung -> MQTT bridge")
    sub = p.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Stream Blitzortung strokes to MQTT")
    feed.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true", default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--max-events", type=int, default=int(os.getenv("BLITZORTUNG_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true", default=os.getenv("BLITZORTUNG_MOCK", "").lower() in ("1", "true", "yes"))
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

