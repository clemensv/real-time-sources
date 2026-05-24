"""MQTT feeder application for Seattle Fire 911 → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from seattle_911.seattle_911 import DEFAULT_LOOKBACK_HOURS, DEFAULT_OVERLAP_MINUTES, DEFAULT_POLL_INTERVAL_SECONDS, SeattleFire911Bridge
from seattle_911_mqtt_producer_mqtt_client.client import USWASeattleFire911MqttMqttClient

logger = logging.getLogger(__name__)


def _uns_slug(value: str) -> str:
    raw = (value or "unknown").lower().strip()
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif ch in ("-", "_"):
            out.append(ch)
        else:
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


async def feed(
    bridge: SeattleFire911Bridge,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id or "", protocol=MQTTv5)
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()
    mqtt_client = USWASeattleFire911MqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            if bridge.last_seen_datetime:
                since = datetime.fromisoformat(bridge.last_seen_datetime) - timedelta(minutes=DEFAULT_OVERLAP_MINUTES)
            else:
                since = datetime.utcnow() - timedelta(hours=DEFAULT_LOOKBACK_HOURS)
            incidents = bridge.fetch_incidents(since=since)
            sent = 0
            newest: Optional[str] = bridge.last_seen_datetime
            sent_ids: list[str] = []
            for incident in incidents:
                if incident.incident_number in bridge.sent_incident_numbers:
                    newest = max(newest or "", incident.incident_datetime)
                    continue
                await mqtt_client.publish_us_wa_seattle_fire911_mqtt_incident(
                    incident_number=incident.incident_number,
                    incident_datetime_utc=incident.incident_datetime_utc.isoformat(),
                    incident_type_slug=incident.incident_type_slug,
                    data=incident,
                )
                sent_ids.append(incident.incident_number)
                newest = max(newest or "", incident.incident_datetime)
                sent += 1
            bridge._remember_incidents(sent_ids)
            if newest:
                bridge.last_seen_datetime = newest
            bridge.save_state()
            logger.info("Fetched %d incidents and published %d new MQTT incidents", len(incidents), sent)
            if once:
                break
            await asyncio.sleep(DEFAULT_POLL_INTERVAL_SECONDS)
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme in ("mqtts", "ssl", "tls") else 1883), scheme in ("mqtts", "ssl", "tls")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Seattle Fire 911 MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("SEATTLE_911_LAST_POLLED_FILE", ""))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(
        SeattleFire911Bridge(state_file=args.state_file),
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        once=args.once,
        content_mode=args.content_mode,
    ))
