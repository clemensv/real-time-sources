"""MQTT feeder application for VATSIM → Unified Namespace."""

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

from vatsim.vatsim import VatsimBridge, _load_state, _save_state
from vatsim_mqtt_producer_mqtt_client.client import NetVatsimMqttMqttClient

logger = logging.getLogger(__name__)


async def _publish_poll_cycle(
    bridge: VatsimBridge,
    mqtt_client: NetVatsimMqttMqttClient,
    previous_pilots: dict[str, str],
    previous_controllers: dict[str, str],
) -> tuple[int, int]:
    data = await asyncio.to_thread(bridge.fetch_data)
    general = data.get("general", {})
    pilots = data.get("pilots", [])
    controllers = data.get("controllers", [])

    status = bridge.build_network_status(general, len(pilots), len(controllers))
    await mqtt_client.publish_net_vatsim_mqtt_facility_status(
        callsign=status.callsign,
        facility=status.facility,
        data=status,
    )

    tasks: list[asyncio.Task[None]] = []
    pilot_count = 0
    for raw_pilot in pilots:
        callsign = raw_pilot.get("callsign", "")
        if not callsign:
            continue
        fingerprint = bridge.pilot_fingerprint(raw_pilot)
        if previous_pilots.get(callsign) == fingerprint:
            continue
        try:
            pilot = bridge.parse_pilot(raw_pilot)
            tasks.append(asyncio.create_task(mqtt_client.publish_net_vatsim_mqtt_pilot_position(callsign=pilot.callsign, data=pilot)))
            pilot_count += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error publishing pilot %s: %s", callsign, exc)
        previous_pilots[callsign] = fingerprint

    controller_count = 0
    for raw_controller in controllers:
        callsign = raw_controller.get("callsign", "")
        if not callsign:
            continue
        fingerprint = bridge.controller_fingerprint(raw_controller)
        if previous_controllers.get(callsign) == fingerprint:
            continue
        try:
            controller = bridge.parse_controller(raw_controller)
            tasks.append(asyncio.create_task(mqtt_client.publish_net_vatsim_mqtt_controller_position(callsign=controller.callsign, data=controller)))
            controller_count += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error publishing controller %s: %s", callsign, exc)
        previous_controllers[callsign] = fingerprint

    if tasks:
        await asyncio.gather(*tasks)
    return pilot_count, controller_count


async def feed(
    bridge: VatsimBridge,
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    state_file: str,
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
    mqtt_client = NetVatsimMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    await mqtt_client.connect(broker_host, broker_port)
    state = _load_state(state_file)
    previous_pilots = state.get("pilots", {})
    previous_controllers = state.get("controllers", {})
    try:
        while True:
            started = time.monotonic()
            pilot_count, controller_count = await _publish_poll_cycle(bridge, mqtt_client, previous_pilots, previous_controllers)
            _save_state(state_file, {"pilots": previous_pilots, "controllers": previous_controllers})
            elapsed = time.monotonic() - started
            logger.info("Published VATSIM status, %d pilots, %d controllers in %.1fs", pilot_count, controller_count, elapsed)
            if once:
                break
            await asyncio.sleep(max(0, polling_interval - elapsed))
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="VATSIM MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.vatsim_mqtt_state.json")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(VatsimBridge(), host, port, args.polling_interval, args.state_file, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
