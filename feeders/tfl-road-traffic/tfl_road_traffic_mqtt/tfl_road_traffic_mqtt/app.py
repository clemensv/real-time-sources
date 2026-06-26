"""TfL Road Traffic REST polling -> MQTT/UNS bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from tfl_road_traffic_core.tfl_road_traffic import TflRoadTrafficSource, build_road_corridor_record, build_road_disruption_record, build_road_status_record
from tfl_road_traffic_mqtt_producer_data import RoadCorridor as MqttRoadCorridor
from tfl_road_traffic_mqtt_producer_data import RoadDisruption as MqttRoadDisruption
from tfl_road_traffic_mqtt_producer_data import RoadStatus as MqttRoadStatus
from tfl_road_traffic_mqtt_producer_mqtt_client.client import UkGovTflRoadMqttMqttClient

logger = logging.getLogger("tfl_road_traffic_mqtt")


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in {"mqtts", "ssl", "tls"}
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    return host, port, tls, parsed.username, parsed.password


class TflRoadTrafficMqttBridge(TflRoadTrafficSource):
    def __init__(self, client: UkGovTflRoadMqttMqttClient, *, polling_interval: int = 60) -> None:
        super().__init__(polling_interval=polling_interval)
        self.client = client

    async def publish_corridor(self, raw: dict) -> bool:
        record = build_road_corridor_record(raw)
        if record is None:
            return False
        data = MqttRoadCorridor(**record)
        await self.client.publish_uk_gov_tfl_road_mqtt_road_corridor(road_id=data.road_id, data=data, qos=1, retain=True)
        return True

    async def publish_status(self, raw: dict) -> bool:
        record = build_road_status_record(raw)
        if record is None:
            return False
        data = MqttRoadStatus(**record)
        await self.client.publish_uk_gov_tfl_road_mqtt_road_status(road_id=data.road_id, data=data, qos=1, retain=True)
        return True

    async def publish_disruption(self, raw: dict) -> bool:
        pending, candidate_state = self.pending_disruptions([raw])
        if not pending:
            return False
        for record in pending:
            data = MqttRoadDisruption(**record)
            method = getattr(self.client, f"publish_uk_gov_tfl_road_mqtt_road_disruption_{data.severity}")
            await method(road_id=data.road_id, severity=data.severity, disruption_id=data.disruption_id, data=data, qos=1, retain=False)
        self.commit_disruption_state(candidate_state)
        return True

    async def poll_once(self) -> dict[str, int]:
        counts = {"corridors": 0, "roads": 0, "disruptions": 0}
        corridors = self.fetch_corridors() or []
        for raw in corridors:
            if await self.publish_corridor(raw):
                counts["corridors"] += 1
        statuses = self.fetch_statuses() or []
        for raw in statuses:
            if await self.publish_status(raw):
                counts["roads"] += 1
        disruptions = self.fetch_disruptions() or []
        for raw in disruptions:
            if await self.publish_disruption(raw):
                counts["disruptions"] += 1
        logger.info("TfL Road Traffic MQTT cycle complete: %s", counts)
        return counts

    async def emit_mock_corpus(self) -> None:
        """Emit a small synthetic corpus for E2E testing without calling TfL API."""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        corridors = [
            {"id": "A1", "displayName": "A1", "statusSeverity": "Good", "statusSeverityDescription": "No issues", "bounds": "[[-0.1,51.5],[0.1,51.6]]", "envelope": "", "url": "https://tfl.gov.uk"},
            {"id": "M25", "displayName": "M25", "statusSeverity": "Serious", "statusSeverityDescription": "Severe delays", "bounds": "[[-0.5,51.3],[0.5,51.7]]", "envelope": "", "url": "https://tfl.gov.uk"},
        ]
        statuses = [
            {"id": "A1", "displayName": "A1", "statusSeverity": "Good", "statusSeverityDescription": "No issues"},
            {"id": "M25", "displayName": "M25", "statusSeverity": "Serious", "statusSeverityDescription": "Severe delays"},
        ]
        severities = ["serious", "severe", "moderate", "minor", "information", "closure"]
        disruptions = []
        for i, sev in enumerate(severities, start=1):
            disruptions.append({
                "id": f"TIMS-{i:05d}", "url": f"/Road/all/Disruption/TIMS-{i:05d}",
                "point": "51.5,-0.1", "severity": sev, "ordinal": 0,
                "category": "PlannedWork", "subCategory": "RoadWorks",
                "comments": f"Mock {sev} disruption", "currentUpdate": "Works ongoing",
                "currentUpdateDateTime": now.isoformat(),
                "corridorIds": ["A1"],
                "startDateTime": now.isoformat(), "location": "A1 Northbound",
                "isActive": True,
                "hasClosures": sev == "closure", "linkText": "", "linkUrl": "",
                "roadProject": None, "publishStartDate": now.isoformat(),
                "publishEndDate": None, "timeFrame": "Current", "geometry": None,
                "endDateTime": None, "lastModifiedTime": now.isoformat(),
                "levelOfInterest": "high", "recurringSchedules": [],
            })
        for raw in corridors:
            await self.publish_corridor(raw)
        for raw in statuses:
            await self.publish_status(raw)
        for raw in disruptions:
            await self.publish_disruption(raw)
        logger.info("Emitted mock corpus: %d corridors, %d statuses, %d disruptions", len(corridors), len(statuses), len(disruptions))

    async def poll_and_publish(self, once: bool = False) -> None:
        while True:
            await self.poll_once()
            if once:
                return
            await asyncio.sleep(self.polling_interval)


async def _connect_client(args: argparse.Namespace) -> UkGovTflRoadMqttMqttClient:
    broker_host, broker_port, tls_from_url, url_user, url_password = _parse_broker_url(args.mqtt_broker_url)
    tls_enabled = args.mqtt_enable_tls or tls_from_url or broker_port == 8883
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.mqtt_client_id or "tfl-road-traffic-mqtt", protocol=MQTTv5)
    auth_mode = (args.mqtt_auth_mode or "anonymous").lower()
    username = args.mqtt_username or url_user
    password = args.mqtt_password or url_password
    if auth_mode == "userpass":
        paho_client.username_pw_set(username or "", password or "")
    if tls_enabled:
        paho_client.tls_set(ca_certs=args.mqtt_ca_file)
    loop = asyncio.get_running_loop()
    client = UkGovTflRoadMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    await client.connect(broker_host, broker_port)
    return client


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TfL Road Traffic API -> MQTT/UNS bridge")
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed", help="Poll TfL and publish MQTT CloudEvents")
    feed.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true", default=_env_bool("MQTT_ENABLE_TLS", False))
    feed.add_argument("--mqtt-auth-mode", default=os.getenv("MQTT_AUTH_MODE", "anonymous"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-ca-file", default=os.getenv("MQTT_CA_FILE"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    feed.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    feed.add_argument("--emit-mock-corpus", action="store_true", default=_env_bool("TFL_MQTT_EMIT_MOCK_CORPUS", False))
    feed.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"))
    return parser


async def _run(args: argparse.Namespace) -> None:
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
    client = await _connect_client(args)
    try:
        bridge = TflRoadTrafficMqttBridge(client, polling_interval=args.polling_interval)
        if args.emit_mock_corpus:
            await bridge.emit_mock_corpus()
            await asyncio.sleep(1.0)
            return
        await bridge.poll_and_publish(once=args.once)
    finally:
        await client.disconnect()


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return
    asyncio.run(_run(args))
