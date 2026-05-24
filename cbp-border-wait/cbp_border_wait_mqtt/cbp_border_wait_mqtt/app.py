"""MQTT feeder application for US CBP Border Wait Times → Unified Namespace."""

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

from cbp_border_wait.cbp_border_wait import (
    CbpBorderWaitAPI,
    _load_state,
    _save_state,
)
from cbp_border_wait_mqtt_producer_mqtt_client.client import GovCbpBorderwaitMqttMqttClient

logger = logging.getLogger(__name__)


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


async def feed(
    api: CbpBorderWaitAPI,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    polling_interval: int = 3600,
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()
    mqtt_client = GovCbpBorderwaitMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=asyncio.get_running_loop(),
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)
    previous_timestamps = _load_state(state_file)
    try:
        while True:
            count = 0
            start_time = datetime.now(timezone.utc)
            raw_ports = api.fetch_ports()
            for raw in raw_ports:
                try:
                    port = api.parse_port(raw)
                    await mqtt_client.publish_gov_cbp_borderwait_mqtt_port(
                        port_number=port.port_number,
                        border_slug=port.border_slug,
                        data=port,
                    )
                    port_num = raw.get("port_number", "")
                    dedup_key = f"{raw.get('date', '')}T{raw.get('time', '')}"
                    wait_time = api.parse_wait_time(raw)
                    await mqtt_client.publish_gov_cbp_borderwait_mqtt_wait_time(
                        port_number=wait_time.port_number,
                        border_slug=wait_time.border_slug,
                        data=wait_time,
                    )
                    if previous_timestamps.get(port_num) != dedup_key:
                        previous_timestamps[port_num] = dedup_key
                    count += 1
                except Exception as exc:
                    logger.error("Error publishing CBP port %s: %s", raw.get("port_number", "?"), exc)
            _save_state(state_file, previous_timestamps)
            elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
            logger.info("Published %d wait-time updates in %.1f s", count, elapsed)
            if once:
                break
            await asyncio.sleep(max(0, polling_interval - elapsed))
    finally:
        await mqtt_client.disconnect()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="US CBP Border Wait Times MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", ""))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "3600")))
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
        CbpBorderWaitAPI(),
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        state_file=args.state_file,
        polling_interval=args.polling_interval,
        once=args.once,
        content_mode=args.content_mode,
    ))
