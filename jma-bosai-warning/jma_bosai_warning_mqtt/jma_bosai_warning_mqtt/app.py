"""MQTT feeder application for JMA Bosai warnings → Unified Namespace."""

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

from jma_bosai_warning.jma_bosai_warning import (
    AREA_CATALOG_URL,
    WARNING_OFFICE_CODES,
    WARNING_URL_TEMPLATE,
    BridgeState,
    JmaBosaiWarningAPI,
    _cap_list,
    _load_state,
    _save_state,
    parse_weather_warning_payload,
)
from jma_bosai_warning_mqtt_producer_data import Office, WeatherWarning
from jma_bosai_warning_mqtt_producer_mqtt_client.client import JPJMAWarningMqttMqttClient

logger = logging.getLogger(__name__)


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
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id or "", protocol=MQTTv5)
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()
    mqtt_client = JPJMAWarningMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
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
            _save_state(state_file, state.as_dict())
            logger.info("Published %d JMA weather warning record(s)", emitted)
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
    api = JmaBosaiWarningAPI()
    logger.info("Polling JMA Bosai warning feeds and publishing to MQTT %s:%d", host, port)
    asyncio.run(feed(api, host, port, state_file=args.state_file, polling_interval_warning=args.polling_interval_warning, office_metadata_refresh_hours=args.office_metadata_refresh_hours, office_codes=office_codes, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
