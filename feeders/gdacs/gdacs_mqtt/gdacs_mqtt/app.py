"""MQTT feeder application for GDACS → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from gdacs.gdacs import GDACS_RSS_URL, GDACSPoller
from gdacs_mqtt_producer_mqtt_client.client import GDACSAlertsMqttMqttClient

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
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id or "", protocol=MQTTv5)
    if username:
        paho_client.username_pw_set(username, password or "")
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
