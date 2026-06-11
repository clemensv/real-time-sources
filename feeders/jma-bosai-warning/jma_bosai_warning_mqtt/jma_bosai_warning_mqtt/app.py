"""MQTT feeder application for JMA Bosai warnings → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from jma_bosai_warning.jma_bosai_warning import (
    AREA_CATALOG_URL,
    WARNING_OFFICE_CODES,
    WARNING_URL_TEMPLATE,
    TSUNAMI_LIST_URL,
    TSUNAMI_DETAIL_BASE,
    BridgeState,
    JmaBosaiWarningAPI,
    _cap_list,
    _load_state,
    _save_state,
    parse_weather_warning_payload,
    parse_tsunami_alert,
)
from jma_bosai_warning_mqtt_producer_data import Office, WeatherWarning, TsunamiAlert
from jma_bosai_warning_mqtt_producer_mqtt_client.client import JPJMAWarningMqttMqttClient
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

class MockAPI(JmaBosaiWarningAPI):
    def refresh_area_catalog(self) -> bool:
        self.area_catalog = {"offices": {"130000": {"name": "東京都", "enName": "Tokyo", "parent": None}}}
        self.area_names = {"130000": "東京都", "130010": "東京地方"}
        return True

    def fetch_warning_payload(self, office_code: str):
        return {"reportDatetime":"2026-01-01T00:00:00+09:00","timeSeries":[{"timeDefines":["2026-01-01T00:00:00+09:00"],"areas":[{"code":"130010","name":"東京地方","warnings":[{"code":"03","status":"警報"}]}]}]}

    def fetch_tsunami_list(self):
        return [{"eid":"20260101000000","ser":"1","json":"VTSE41.json","ift":"発表","rdt":"2026-01-01T00:01:00+09:00","ttl":"津波警報・注意報・予報"}]

    def fetch_tsunami_detail(self, filename: str):
        return {"Body":{"Tsunami":{"Forecast":[{"Area":{"Code":"100","Name":"東京湾内湾"},"Category":"津波警報"}]}}}

async def _publish_offices(api: JmaBosaiWarningAPI, mqtt_client: JPJMAWarningMqttMqttClient) -> int:
    count = 0
    for record in api.office_records():
        await mqtt_client.publish_jp_jma_warning_mqtt_office(
            feedurl=AREA_CATALOG_URL,
            prefecture=record["prefecture"],
            severity=record["severity"],
            office_code=record["office_code"],
            area_code=record["area_code"],
            event=record["event"],
            data=Office(**record),
        )
        count += 1
    return count

async def _publish_warning_cycle(api: JmaBosaiWarningAPI, mqtt_client: JPJMAWarningMqttMqttClient, state: BridgeState, office_codes: list[str]) -> int:
    pending: list[str] = []
    emitted = 0
    seen = set(state.seen_weather)
    for office_code in office_codes:
        try:
            records = parse_weather_warning_payload(office_code, api.fetch_warning_payload(office_code), api.area_names)
        except Exception as exc:
            logger.warning("Skipping warning office %s after fetch/parse failure: %s", office_code, exc)
            continue
        for record in records:
            dedupe_key = f"{record['office_code']}|{record['area_code']}|{record['report_datetime']}"
            if dedupe_key in seen:
                continue
            await mqtt_client.publish_jp_jma_warning_mqtt_weather_warning(
                feedurl=WARNING_URL_TEMPLATE.format(office_code=office_code),
                prefecture=record["prefecture"],
                severity=record["severity"],
                office_code=record["office_code"],
                area_code=record["area_code"],
                event=record["event"],
                data=WeatherWarning(**record),
            )
            pending.append(dedupe_key)
            emitted += 1
    state.seen_weather = _cap_list(state.seen_weather + pending)
    return emitted

async def _publish_tsunami_cycle(api: JmaBosaiWarningAPI, mqtt_client: JPJMAWarningMqttMqttClient, state: BridgeState) -> int:
    pending: list[str] = []
    emitted = 0
    seen = set(state.seen_tsunami)
    try:
        entries = api.fetch_tsunami_list()
    except Exception as exc:
        logger.warning("Skipping tsunami cycle after list fetch failure: %s", exc)
        return 0
    for entry in entries:
        try:
            detail = api.fetch_tsunami_detail(entry.get("json", ""))
        except Exception as exc:
            logger.warning("Could not fetch tsunami detail %s: %s", entry.get("json"), exc)
            detail = None
        record = parse_tsunami_alert(entry, detail)
        dedupe_key = f"{record['event_id']}|{record['serial']}"
        if dedupe_key in seen:
            continue
        await mqtt_client.publish_jp_jma_warning_mqtt_tsunami_alert(
            feedurl=record.get("detail_url") or TSUNAMI_LIST_URL,
            prefecture=record["prefecture"],
            severity=record["severity"],
            event_id=record["event_id"],
            serial=str(record["serial"]),
            data=TsunamiAlert(**record),
        )
        pending.append(dedupe_key)
        emitted += 1
    state.seen_tsunami = _cap_list(state.seen_tsunami + pending)
    return emitted

async def feed(
    api: JmaBosaiWarningAPI,
    broker_host: str,
    broker_port: int,
    *,
    state_file: str,
    polling_interval_warning: int,
    office_metadata_refresh_hours: int,
    office_codes: list[str],
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
    mqtt_client = JPJMAWarningMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)
    state = BridgeState.from_dict(_load_state(state_file))
    metadata_interval = max(1, office_metadata_refresh_hours) * 3600
    try:
        while True:
            started = time.monotonic()
            now_utc = datetime.now(timezone.utc)
            should_refresh = not state.last_metadata_refresh
            if state.last_metadata_refresh:
                try:
                    should_refresh = (now_utc - datetime.fromisoformat(state.last_metadata_refresh.replace("Z", "+00:00"))).total_seconds() >= metadata_interval
                except ValueError:
                    should_refresh = True
            if should_refresh:
                api.refresh_area_catalog()
                office_count = await _publish_offices(api, mqtt_client)
                state.last_metadata_refresh = now_utc.isoformat().replace("+00:00", "Z")
                _save_state(state_file, state.as_dict())
                logger.info("Published %d retained JMA office reference record(s)", office_count)
            emitted = await _publish_warning_cycle(api, mqtt_client, state, office_codes)
            tsunami_emitted = await _publish_tsunami_cycle(api, mqtt_client, state)
            _save_state(state_file, state.as_dict())
            logger.info("Published %d JMA weather warning and %d tsunami record(s)", emitted, tsunami_emitted)
            if once:
                break
            await asyncio.sleep(max(0, polling_interval_warning - (time.monotonic() - started)))
    finally:
        await mqtt_client.disconnect()

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="JMA Bosai warning MQTT/UNS bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("JMA_BOSAI_WARNING_MQTT_STATE_FILE", os.path.expanduser("~/.jma_bosai_warning_mqtt_state.json")))
    parser.add_argument("--polling-interval-warning", type=int, default=int(os.getenv("POLLING_INTERVAL_WARNING", "60")))
    parser.add_argument("--office-metadata-refresh-hours", type=int, default=int(os.getenv("OFFICE_METADATA_REFRESH_HOURS", "720")))
    parser.add_argument("--office-codes", default=os.getenv("JMA_WARNING_OFFICE_CODES", ",".join(WARNING_OFFICE_CODES)))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    office_codes = [part.strip() for part in args.office_codes.split(",") if part.strip()]
    host, port, tls = _parse_broker_url(args.broker_url)
    api = MockAPI() if os.getenv("JMA_BOSAI_WARNING_MOCK", "").lower() in ("1", "true", "yes") else JmaBosaiWarningAPI()
    logger.info("Polling JMA Bosai warning feeds and publishing to MQTT %s:%d", host, port)
    asyncio.run(feed(api, host, port, state_file=args.state_file, polling_interval_warning=args.polling_interval_warning, office_metadata_refresh_hours=args.office_metadata_refresh_hours, office_codes=office_codes, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
