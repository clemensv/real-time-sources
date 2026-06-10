"""MQTT feeder application for GDACS → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from gdacs.gdacs import GDACS_RSS_URL, GDACSPoller
from gdacs_mqtt_producer_mqtt_client.client import GDACSAlertsMqttMqttClient
import json

def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {
        "api-version": "2018-02-01",
        "resource": audience or "https://eventgrid.azure.net/",
    }
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id

    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
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
        return resolved_client_id, str(username or ""), str(password or "")

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    return resolved_client_id, resolved_username, resolved_password

logger = logging.getLogger(__name__)

def _topic_segment(value: Optional[str]) -> str:
    text = (value or "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"

async def _poll_once(poller: GDACSPoller, mqtt_client: GDACSAlertsMqttMqttClient) -> tuple[int, int]:
    state = poller.load_state()
    xml_text = await poller.fetch_feed()
    alerts = poller.parse_feed(xml_text)
    count_new = 0
    count_updated = 0

    for alert in alerts:
        key = poller._state_key(alert)
        prev_version = state.get(key)
        current_version = alert.version if alert.version is not None else 0
        if prev_version is not None and prev_version >= current_version:
            continue
        if prev_version is None:
            count_new += 1
        else:
            count_updated += 1

        await mqtt_client.publish_gdacs_alerts_mqtt_disaster_alert(
            event_type=_topic_segment(alert.event_type),
            alert_color=_topic_segment(alert.alert_color),
            country=_topic_segment(alert.country),
            event_id=_topic_segment(alert.event_id),
            data=alert,
        )
        state[key] = current_version

    poller.save_state(state)
    return count_new, count_updated

async def feed(
    poller: GDACSPoller,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    content_mode: str = "binary",
    once: bool = False,
) -> None:
    resolved_client_id, resolved_username, resolved_password = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if resolved_username or resolved_password:
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls:
        paho_client.tls_set()
    mqtt_client = GDACSAlertsMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            started = time.monotonic()
            try:
                count_new, count_updated = await _poll_once(poller, mqtt_client)
                logger.info("Published %d new and %d updated GDACS alert(s)", count_new, count_updated)
            except Exception:
                logger.exception("Error fetching, parsing, or publishing GDACS alerts")
                if once:
                    raise
            if once:
                break
            await asyncio.sleep(max(0, poller.poll_interval - (time.monotonic() - started)))
    finally:
        await mqtt_client.disconnect()

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="GDACS MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("GDACS_MQTT_STATE_FILE", os.path.expanduser("~/.gdacs_mqtt_state.json")))
    parser.add_argument("--poll-interval", type=int, default=int(os.getenv("GDACS_POLL_INTERVAL", "300")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    poller = GDACSPoller(kafka_config=None, kafka_topic="mqtt", state_file=args.state_file, poll_interval=args.poll_interval)
    logger.info("Polling %s and publishing to MQTT %s:%d", GDACS_RSS_URL, host, port)
    asyncio.run(feed(poller, host, port, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
