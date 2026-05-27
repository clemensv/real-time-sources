"""MQTT feeder application for JMA Bosai earthquakes → Unified Namespace."""

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
import requests

from jma_bosai_quake.jma_bosai_quake import (
    DEFAULT_STATE_FILE,
    LIST_URL,
    SUPPORTED_BULLETIN_TYPES,
    JmaBosaiQuakeAPI,
    bulletin_type_from_filename,
)
from jma_bosai_quake_mqtt_producer_data import EarthquakeReport
from jma_bosai_quake_mqtt_producer_mqtt_client.client import JPJMAQuakeMqttMqttClient

logger = logging.getLogger(__name__)


async def _publish_once(api: JmaBosaiQuakeAPI, mqtt_client: JPJMAQuakeMqttMqttClient) -> int:
    reports = api.list_reports()
    pending_keys: list[tuple[str, int]] = []
    emitted = 0
    for entry in reversed(reports):
        bulletin_type = bulletin_type_from_filename(entry.get("json"))
        if bulletin_type not in SUPPORTED_BULLETIN_TYPES:
            logger.warning("Skipping unsupported JMA earthquake bulletin type %s from %s", bulletin_type or "<missing>", entry.get("json"))
            continue
        key = api.state_key(entry)
        if key in api.seen:
            continue
        detail = None
        try:
            detail = api.fetch_detail(entry.get("json", ""))
        except requests.RequestException as exc:
            logger.warning("Detail fetch failed for %s: %s", entry.get("json"), exc)
        try:
            data = api.normalize_report(entry, detail)
            mqtt_data = EarthquakeReport(**data.to_serializer_dict())
            await mqtt_client.publish_jp_jma_quake_mqtt_earthquake_report(
                feedurl=LIST_URL,
                prefecture=data.prefecture,
                magnitude_bucket=data.magnitude_bucket,
                event_id=data.event_id,
                serial=str(data.serial),
                data=mqtt_data,
            )
            pending_keys.append(key)
            emitted += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Skipping malformed earthquake report %s: %s", entry.get("eid"), exc)
    if pending_keys:
        api.mark_seen(pending_keys)
    return emitted


async def feed(
    api: JmaBosaiQuakeAPI,
    broker_host: str,
    broker_port: int,
    *,
    polling_interval: int,
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
    mqtt_client = JPJMAQuakeMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            started = time.monotonic()
            count = await _publish_once(api, mqtt_client)
            logger.info("Published %d JMA earthquake report(s)", count)
            if once:
                break
            await asyncio.sleep(max(0, polling_interval - (time.monotonic() - started)))
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="JMA Bosai earthquake MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("JMA_BOSAI_QUAKE_MQTT_STATE_FILE", os.getenv("STATE_FILE", DEFAULT_STATE_FILE)))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    api = JmaBosaiQuakeAPI(state_file=args.state_file)
    logger.info("Polling %s and publishing to MQTT %s:%d", LIST_URL, host, port)
    asyncio.run(feed(api, host, port, polling_interval=args.polling_interval, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
