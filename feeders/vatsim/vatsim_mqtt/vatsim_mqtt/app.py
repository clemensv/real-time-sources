"""MQTT feeder application for VATSIM → Unified Namespace."""

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

from vatsim.vatsim import VatsimBridge, _load_state, _save_state
from vatsim_mqtt_producer_mqtt_client.client import NetVatsimMqttMqttClient
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
        return resolved_client_id, str(username or ""), str(password or ""), None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props

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
    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        paho_client.tls_set()
    mqtt_client = NetVatsimMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
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
