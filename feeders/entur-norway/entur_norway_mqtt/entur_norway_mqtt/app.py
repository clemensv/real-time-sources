"""MQTT feeder application for Entur Norway → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
import uuid
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from entur_norway.entur_norway import EnturNorwayBridge, _has_more_data
from entur_norway_mqtt_producer_mqtt_client.client import NoEnturMqttMqttClient
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

async def _publish_poll_cycle(
    bridge: EnturNorwayBridge,
    mqtt_client: NoEnturMqttMqttClient,
    *,
    first_run: bool,
    et_requestor_id: str,
    vm_requestor_id: str,
    sx_requestor_id: str,
    max_size: int,
) -> tuple[int, int, int]:
    et_req_id: Optional[str] = None if first_run else et_requestor_id
    et_count = 0
    more_et = True
    while more_et:
        et_root = await asyncio.to_thread(bridge.fetch_siri, "et", et_req_id, max_size)
        if et_root is None:
            break
        more_et = _has_more_data(et_root)
        et_req_id = et_requestor_id
        tasks = []
        for _op_day, _sj_id, evj in bridge.parse_et_journeys(et_root):
            tasks.append(asyncio.create_task(mqtt_client.publish_no_entur_mqtt_estimated_vehicle_journey(
                operating_day=evj.operating_day,
                service_journey_id=evj.service_journey_id,
                operator_ref=evj.operator_ref,
                line_ref=evj.line_ref,
                data=evj,
            )))
        if tasks:
            await asyncio.gather(*tasks)
            et_count += len(tasks)

    vm_req_id: Optional[str] = None if first_run else vm_requestor_id
    vm_count = 0
    more_vm = True
    while more_vm:
        vm_root = await asyncio.to_thread(bridge.fetch_siri, "vm", vm_req_id, max_size)
        if vm_root is None:
            break
        more_vm = _has_more_data(vm_root)
        vm_req_id = vm_requestor_id
        tasks = []
        for _op_day, _sj_id, mvj in bridge.parse_vm_journeys(vm_root):
            tasks.append(asyncio.create_task(mqtt_client.publish_no_entur_mqtt_monitored_vehicle_journey(
                operating_day=mvj.operating_day,
                service_journey_id=mvj.service_journey_id,
                operator_ref=mvj.operator_ref,
                line_ref=mvj.line_ref,
                data=mvj,
            )))
        if tasks:
            await asyncio.gather(*tasks)
            vm_count += len(tasks)

    sx_req_id: Optional[str] = None if first_run else sx_requestor_id
    sx_count = 0
    more_sx = True
    while more_sx:
        sx_root = await asyncio.to_thread(bridge.fetch_siri, "sx", sx_req_id, max_size)
        if sx_root is None:
            break
        more_sx = _has_more_data(sx_root)
        sx_req_id = sx_requestor_id
        tasks = []
        for _sit_num, sit in bridge.parse_sx_situations(sx_root):
            tasks.append(asyncio.create_task(mqtt_client.publish_no_entur_mqtt_pt_situation_element(
                situation_number=sit.situation_number,
                severity=sit.severity,
                data=sit,
            )))
        if tasks:
            await asyncio.gather(*tasks)
            sx_count += len(tasks)

    return et_count, vm_count, sx_count

async def feed(
    bridge: EnturNorwayBridge,
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    max_size: int,
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
    mqtt_client = NoEnturMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    await mqtt_client.connect(broker_host, broker_port)
    et_requestor_id = str(uuid.uuid4())
    vm_requestor_id = str(uuid.uuid4())
    sx_requestor_id = str(uuid.uuid4())
    first_run = True
    try:
        while True:
            started = time.monotonic()
            et_count, vm_count, sx_count = await _publish_poll_cycle(
                bridge,
                mqtt_client,
                first_run=first_run,
                et_requestor_id=et_requestor_id,
                vm_requestor_id=vm_requestor_id,
                sx_requestor_id=sx_requestor_id,
                max_size=max_size,
            )
            first_run = False
            elapsed = time.monotonic() - started
            logger.info("Published Entur ET=%d VM=%d SX=%d in %.1fs", et_count, vm_count, sx_count, elapsed)
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
    parser = argparse.ArgumentParser(description="Entur Norway MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "30")))
    parser.add_argument("--max-size", type=int, default=int(os.getenv("MAX_SIZE", "1000")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(EnturNorwayBridge(), host, port, args.polling_interval, args.max_size, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
