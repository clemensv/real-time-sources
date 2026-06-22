"""MQTT feeder application for EAWS ALBINA → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import datetime
import logging
import os
import time
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from eaws_albina_core import DEFAULT_LANG, DEFAULT_REGIONS, POLL_INTERVAL_SECONDS, AlbinaPoller
from eaws_albina_mqtt_producer_mqtt_client.client import OrgEAWSALBINAMqttMqttClient
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

async def _publish_date(poller: AlbinaPoller, mqtt_client: OrgEAWSALBINAMqttMqttClient, date_str: str) -> int:
    state = poller.load_state()
    seen_keys = set(state.get("seen_keys", []))
    count = 0
    for region in poller.regions:
        url = poller.build_url(date_str, region, poller.lang)
        data = await asyncio.to_thread(poller.fetch_bulletin, url)
        if data is None:
            continue
        for event in poller.parse_bulletins(data, poller.lang):
            dedup_key = f"{event.region_id}:{event.publication_time.isoformat()}"
            if dedup_key in seen_keys:
                continue
            await mqtt_client.publish_org_eaws_albina_mqtt_avalanche_bulletin(
                region_id=event.region_id,
                country=event.country,
                danger_level=event.danger_level,
                data=event,
            )
            seen_keys.add(dedup_key)
            count += 1
    state["seen_keys"] = list(seen_keys)[-5000:]
    poller.save_state(state)
    return count

async def feed(
    poller: AlbinaPoller,
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
    mqtt_client = OrgEAWSALBINAMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)
    try:
        while True:
            started = time.monotonic()
            today = datetime.date.today()
            total = 0
            total += await _publish_date(poller, mqtt_client, today.isoformat())
            total += await _publish_date(poller, mqtt_client, (today - datetime.timedelta(days=1)).isoformat())
            elapsed = time.monotonic() - started
            logger.info("Published %d EAWS ALBINA bulletin(s) in %.1fs", total, elapsed)
            if once:
                break
            await asyncio.sleep(max(0, POLL_INTERVAL_SECONDS - elapsed))
    finally:
        await mqtt_client.disconnect()

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="EAWS ALBINA MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--last-polled-file", default=os.getenv("EAWS_ALBINA_MQTT_LAST_POLLED_FILE", os.path.expanduser("~/.eaws_albina_mqtt_state.json")))
    parser.add_argument("--regions", default=os.getenv("EAWS_ALBINA_REGIONS", ",".join(DEFAULT_REGIONS)))
    parser.add_argument("--lang", default=os.getenv("EAWS_ALBINA_LANG", DEFAULT_LANG))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    regions = [part.strip() for part in args.regions.split(",") if part.strip()]
    poller = AlbinaPoller(last_polled_file=args.last_polled_file, regions=regions, lang=args.lang)
    asyncio.run(feed(poller, host, port, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
