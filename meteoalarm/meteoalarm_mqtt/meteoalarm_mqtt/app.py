"""MQTT feeder application for Meteoalarm → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from typing import Optional
from urllib.parse import urlparse

import aiohttp
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from meteoalarm.meteoalarm import DEFAULT_COUNTRIES, DEFAULT_POLL_INTERVAL, DEFAULT_STATE_FILE, MeteoalarmPoller, normalize_warning
from meteoalarm_mqtt_producer_mqtt_client.client import MeteoalarmWarningsMqttMqttClient

logger = logging.getLogger(__name__)


def _topic_segment(value: Optional[str]) -> str:
    text = (value or "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"


async def _poll_once(poller: MeteoalarmPoller, mqtt_client: MeteoalarmWarningsMqttMqttClient) -> tuple[int, int]:
    state = poller.load_state()
    count_new = 0
    count_updated = 0
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
        for country in poller.countries:
            raw_warnings = await poller.fetch_country(session, country)
            for item in raw_warnings:
                alert_obj = item.get("alert", item)
                warning = normalize_warning(alert_obj, country)
                if warning is None:
                    continue
                sent_str = warning.sent or ""
                prev_sent = state.get(warning.identifier)
                if prev_sent is not None and prev_sent >= sent_str:
                    continue
                if prev_sent is None:
                    count_new += 1
                else:
                    count_updated += 1
                await mqtt_client.publish_meteoalarm_warnings_mqtt_weather_warning(
                    country=_topic_segment(warning.country),
                    severity=_topic_segment(warning.severity),
                    awareness_type=_topic_segment(warning.awareness_type),
                    identifier=_topic_segment(warning.identifier),
                    data=warning,
                )
                state[warning.identifier] = sent_str
    poller.save_state(state)
    return count_new, count_updated


async def feed(
    poller: MeteoalarmPoller,
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
    mqtt_client = MeteoalarmWarningsMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            started = time.monotonic()
            try:
                count_new, count_updated = await _poll_once(poller, mqtt_client)
                logger.info("Published %d new and %d updated Meteoalarm warning(s)", count_new, count_updated)
            except Exception:
                logger.exception("Error fetching, parsing, or publishing Meteoalarm warnings")
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
    parser = argparse.ArgumentParser(description="Meteoalarm MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("METEOALARM_MQTT_STATE_FILE", DEFAULT_STATE_FILE.replace(".json", "_mqtt.json")))
    parser.add_argument("--poll-interval", type=int, default=int(os.getenv("METEOALARM_POLL_INTERVAL", str(DEFAULT_POLL_INTERVAL))))
    parser.add_argument("--countries", default=os.getenv("METEOALARM_COUNTRIES", ",".join(DEFAULT_COUNTRIES)))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    countries = [part.strip() for part in args.countries.split(",") if part.strip()]
    poller = MeteoalarmPoller(kafka_config=None, kafka_topic="mqtt", state_file=args.state_file, poll_interval=args.poll_interval, countries=countries)
    asyncio.run(feed(poller, host, port, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
