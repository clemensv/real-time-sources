from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import threading
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from jma_bosai_volcano_core.jma_bosai_volcano import (
    DEFAULT_STATE_FILE,
    ERUPTION_URL,
    JMABosaiVolcanoSource,
    MockSource,
    VOLCANO_LIST_URL,
    WARNING_URL,
    _mock_enabled,
    load_state,
)
from jma_bosai_volcano_mqtt_producer_data import VolcanicEruption as MEruption
from jma_bosai_volcano_mqtt_producer_data import VolcanicWarning as MWarning
from jma_bosai_volcano_mqtt_producer_data import Volcano as MVolcano
from jma_bosai_volcano_mqtt_producer_data.conditionenum import ConditionEnum
from jma_bosai_volcano_mqtt_producer_data.eruptiontypeenum import EruptionTypeenum
from jma_bosai_volcano_mqtt_producer_mqtt_client.client import JPJMAVolcanoMqttMqttClient


def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id
    request = Request("http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params), headers={"Metadata": "true"})
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
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    from paho.mqtt.properties import Properties as _MqttConnProps
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props


def _to_volcano(record: dict) -> MVolcano:
    return MVolcano(**record)


def _to_warning(record: dict) -> MWarning:
    payload = dict(record)
    payload["condition"] = ConditionEnum[payload["condition"]]
    return MWarning(**payload)


def _to_eruption(record: dict) -> MEruption:
    payload = dict(record)
    if payload.get("eruption_type") is not None:
        payload["eruption_type"] = EruptionTypeenum[payload["eruption_type"]]
    return MEruption(**payload)


async def run(source: JMABosaiVolcanoSource, state: dict[str, object], state_file: str, refresh_hours: int, client: JPJMAVolcanoMqttMqttClient) -> None:
    if source.should_refresh_reference(state, refresh_hours):
        for record in source.build_reference_records():
            data = _to_volcano(record)
            await client.publish_jp_jma_volcano_mqtt_volcano(feedurl=VOLCANO_LIST_URL, prefecture=data.prefecture, volcano_code=data.volcano_code, event=data.event, data=data)
        source.commit_reference_refresh(state, state_file)
    pending = source.collect_pending_telemetry(state)
    for record in pending.warnings:
        data = _to_warning(record)
        await client.publish_jp_jma_volcano_mqtt_volcanic_warning(feedurl=WARNING_URL, prefecture=data.prefecture, volcano_code=data.volcano_code, event=data.event, data=data)
    for record in pending.eruptions:
        data = _to_eruption(record)
        await client.publish_jp_jma_volcano_mqtt_volcanic_eruption(feedurl=ERUPTION_URL, prefecture=data.prefecture, volcano_code=data.volcano_code, event=data.event, data=data)
    if pending.warning_keys or pending.eruption_keys:
        source.commit_telemetry_state(state, state_file, pending.warning_keys, pending.eruption_keys)


def parse_url(u):
    p = urlparse(u if "://" in u else "mqtt://" + u)
    t = (p.scheme or "mqtt").lower() in ("mqtts", "ssl", "tls")
    return p.hostname or "localhost", p.port or (8883 if t else 1883), t


async def feed(source, state_file, refresh_hours, h, p, tls=False, username=None, password=None, content_mode="binary", once=False, polling_interval=60):
    state = load_state(state_file)
    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=None,
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )
    pc = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if _entra_props is None and (resolved_username or resolved_password):
        pc.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        pc.tls_set()
    client = JPJMAVolcanoMqttMqttClient(client=pc, content_mode=content_mode, loop=asyncio.get_running_loop())
    if _entra_props is not None:
        connected = threading.Event()

        def _on_connack(_client, _userdata, _flags, reason_code, _props=None):
            if reason_code == 0:
                connected.set()

        pc.on_connect = _on_connack
        pc.connect(h, p, keepalive=60, clean_start=True, properties=_entra_props)
        pc.loop_start()
        if not await asyncio.get_running_loop().run_in_executor(None, lambda: connected.wait(30)):
            raise RuntimeError("MQTT CONNACK timeout after 30s")
    else:
        await client.connect(h, p)
    try:
        while True:
            await run(source, state, state_file, refresh_hours, client)
            if once:
                return
            await asyncio.sleep(polling_interval)
    finally:
        await client.disconnect()


def main():
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
    pa = argparse.ArgumentParser()
    pa.add_argument("feed_command", nargs="?", default="feed")
    pa.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    pa.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    pa.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    pa.add_argument("--content-mode", default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    pa.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    pa.add_argument("--metadata-refresh-hours", type=int, default=int(os.getenv("VOLCANO_METADATA_REFRESH_HOURS", "720")))
    pa.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    pa.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    a = pa.parse_args()
    h, p, t = parse_url(a.broker_url)
    source = MockSource() if _mock_enabled() else JMABosaiVolcanoSource()
    asyncio.run(feed(source, a.state_file, a.metadata_refresh_hours, h, p, tls=t, username=a.username or None, password=a.password or None, content_mode=a.content_mode, once=a.once or _mock_enabled(), polling_interval=a.polling_interval))
