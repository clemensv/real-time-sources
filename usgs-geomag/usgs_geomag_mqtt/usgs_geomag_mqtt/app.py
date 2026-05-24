"""MQTT feeder application for USGS Geomagnetism → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from usgs_geomag.usgs_geomag import DEFAULT_OBSERVATORIES, POLL_INTERVAL_SECONDS, USGSGeomagPoller
from usgs_geomag_mqtt_producer_mqtt_client.client import GovUsgsGeomagMqttMqttClient

logger = logging.getLogger(__name__)


def _load_state(path: str) -> Dict:
    try:
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data.setdefault("last_timestamps", {})
                    return data
    except Exception as exc:
        logger.warning("Could not load state %s: %s", path, exc)
    return {"last_timestamps": {}}


def _save_state(path: str, state: Dict) -> None:
    if not path:
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f)


async def _publish_observatories(client: GovUsgsGeomagMqttMqttClient, observatories: List[str]) -> None:
    features = USGSGeomagPoller.fetch_observatories()
    wanted = {code.upper() for code in observatories}
    for feature in features:
        obs = USGSGeomagPoller.parse_observatory(feature)
        if wanted and obs.iaga_code.upper() not in wanted:
            continue
        await client.publish_gov_usgs_geomag_mqtt_observatory(
            iaga_code=obs.iaga_code.lower(),
            data=obs,
        )


async def _publish_readings(
    client: GovUsgsGeomagMqttMqttClient,
    observatories: List[str],
    state: Dict,
) -> int:
    last_timestamps = state.setdefault("last_timestamps", {})
    now = datetime.now(timezone.utc)
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    default_start = (now - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    sent = 0
    for code in observatories:
        iaga_code = code.upper()
        start_time = last_timestamps.get(iaga_code, default_start)
        data = USGSGeomagPoller.fetch_variation_data(iaga_code, start_time, end_time)
        if data is None:
            continue
        latest_ts = last_timestamps.get(iaga_code)
        for reading in USGSGeomagPoller.parse_timeseries(iaga_code, data):
            reading_ts = reading.timestamp.isoformat()
            if latest_ts and reading_ts <= latest_ts:
                continue
            await client.publish_gov_usgs_geomag_mqtt_magnetic_field_reading(
                iaga_code=reading.iaga_code.lower(),
                data=reading,
            )
            latest_ts = reading_ts
            sent += 1
        if latest_ts:
            last_timestamps[iaga_code] = latest_ts
    return sent


async def feed(
    broker_host: str,
    broker_port: int,
    observatories: List[str],
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=client_id or "", protocol=MQTTv5)
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()
    mqtt_client = GovUsgsGeomagMqttMqttClient(client=paho_client, content_mode=content_mode, loop=asyncio.get_running_loop())
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)
    state = _load_state(state_file)
    try:
        await _publish_observatories(mqtt_client, observatories)
        while True:
            sent = await _publish_readings(mqtt_client, observatories, state)
            _save_state(state_file, state)
            logger.info("Published %d magnetic field readings", sent)
            if once:
                break
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme in ("mqtts", "ssl", "tls") else 1883), scheme in ("mqtts", "ssl", "tls")


def _parse_observatories(raw: str) -> List[str]:
    return [part.strip().upper() for part in raw.split(",") if part.strip()] or DEFAULT_OBSERVATORIES


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="USGS Geomagnetism MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--observatories", default=os.getenv("GEOMAG_OBSERVATORIES", ",".join(DEFAULT_OBSERVATORIES)))
    parser.add_argument("--state-file", default=os.getenv("GEOMAG_LAST_POLLED_FILE", ""))
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
        host,
        port,
        _parse_observatories(args.observatories),
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        state_file=args.state_file,
        once=args.once,
        content_mode=args.content_mode,
    ))
