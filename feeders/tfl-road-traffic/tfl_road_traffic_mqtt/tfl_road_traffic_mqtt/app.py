"""TfL Road Traffic REST polling -> MQTT/UNS bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from tfl_road_traffic.tfl_road_traffic import (
    TFL_DISRUPTION_URL,
    TFL_ROAD_URL,
    TFL_STATUS_URL,
    _make_session,
    build_road_corridor,
    build_road_disruption,
    build_road_status,
    _uns_slug,
)
from tfl_road_traffic_mqtt_producer_data import RoadCorridor as MqttRoadCorridor
from tfl_road_traffic_mqtt_producer_data import RoadDisruption as MqttRoadDisruption
from tfl_road_traffic_mqtt_producer_data import RoadStatus as MqttRoadStatus
from tfl_road_traffic_mqtt_producer_mqtt_client.client import UkGovTflRoadMqttMqttClient

logger = logging.getLogger("tfl_road_traffic_mqtt")
SEVERITIES = ("serious", "severe", "moderate", "minor", "information", "closure")


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


def _fetch_list(session: Any, url: str) -> list[dict[str, Any]]:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        logger.warning("Unexpected TfL response type from %s: %s", url, type(data))
        return []
    return [item for item in data if isinstance(item, dict)]


def _mqtt_corridor(corridor: Any) -> MqttRoadCorridor:
    return MqttRoadCorridor.from_serializer_dict(corridor.to_serializer_dict())


def _mqtt_status(status: Any) -> MqttRoadStatus:
    return MqttRoadStatus.from_serializer_dict(status.to_serializer_dict())


def _mqtt_disruption(disruption: Any, road_id: str) -> MqttRoadDisruption:
    payload = disruption.to_serializer_dict()
    payload["road_id"] = road_id
    return MqttRoadDisruption.from_serializer_dict(payload)


def _disruption_road_ids(raw: dict[str, Any], fallback: str) -> list[str]:
    corridor_ids = raw.get("corridorIds")
    if isinstance(corridor_ids, list):
        road_ids = [_uns_slug(value) for value in corridor_ids if value]
        if road_ids:
            return list(dict.fromkeys(road_ids))
    return [fallback]


class TflRoadTrafficMqttBridge:
    def __init__(self, client: UkGovTflRoadMqttMqttClient, *, polling_interval: int = 60) -> None:
        self.client = client
        self.polling_interval = polling_interval
        self.session = _make_session()
        self._seen_disruptions: dict[str, str] = {}

    async def publish_corridor(self, raw: dict[str, Any]) -> bool:
        corridor = build_road_corridor(raw)
        if corridor is None:
            return False
        await self.client.publish_uk_gov_tfl_road_mqtt_road_corridor(
            road_id=corridor.road_id,
            data=_mqtt_corridor(corridor),
            qos=1,
            retain=True,
        )
        return True

    async def publish_status(self, raw: dict[str, Any]) -> bool:
        status = build_road_status(raw)
        if status is None:
            return False
        data = _mqtt_status(status)
        await self.client.publish_uk_gov_tfl_road_mqtt_road_status(
            road_id=status.road_id,
            data=data,
            qos=1,
            retain=True,
        )
        return True

    async def publish_disruption(self, raw: dict[str, Any], *, dedupe: bool = True) -> bool:
        raw_id = raw.get("id")
        last_modified = raw.get("lastModifiedTime", "")
        if dedupe and raw_id and self._seen_disruptions.get(str(raw_id)) == last_modified:
            return False
        disruption = build_road_disruption(raw)
        if disruption is None:
            return False
        method = getattr(self.client, f"publish_uk_gov_tfl_road_mqtt_road_disruption_{disruption.severity}")
        for road_id in _disruption_road_ids(raw, disruption.road_id):
            await method(
                road_id=road_id,
                severity=disruption.severity,
                disruption_id=disruption.disruption_id,
                data=_mqtt_disruption(disruption, road_id),
                qos=1,
                retain=False,
            )
        if dedupe and raw_id:
            self._seen_disruptions[str(raw_id)] = last_modified
        return True

    async def poll_once(self) -> dict[str, int]:
        counts = {"corridors": 0, "roads": 0, "disruptions": 0}
        corridors = await asyncio.to_thread(_fetch_list, self.session, TFL_ROAD_URL)
        for raw in corridors:
            if await self.publish_corridor(raw):
                counts["corridors"] += 1
        statuses = await asyncio.to_thread(_fetch_list, self.session, TFL_STATUS_URL)
        for raw in statuses:
            if await self.publish_status(raw):
                counts["roads"] += 1
        disruptions = await asyncio.to_thread(_fetch_list, self.session, TFL_DISRUPTION_URL)
        for raw in disruptions:
            if await self.publish_disruption(raw):
                counts["disruptions"] += 1
        logger.info("TfL Road Traffic MQTT cycle complete: %s", counts)
        return counts

    async def poll_and_publish(self, once: bool = False) -> None:
        while True:
            started = datetime.now(timezone.utc)
            await self.poll_once()
            if once:
                return
            elapsed = (datetime.now(timezone.utc) - started).total_seconds()
            await asyncio.sleep(max(0.0, self.polling_interval - elapsed))

    async def emit_mock_corpus(self) -> None:
        await self.publish_corridor({
            "id": "A2",
            "displayName": "A2",
            "statusSeverity": "Good",
            "statusSeverityDescription": "Mock corridor",
            "url": "/Road/a2",
        })
        await self.publish_status({
            "id": "A2",
            "displayName": "A2",
            "statusSeverity": "Moderate",
            "statusSeverityDescription": "Mock status",
            "url": "/Road/a2",
        })
        for index, severity in enumerate(SEVERITIES, start=1):
            raw = {
                "id": f"TIMS-MQTT-{index}",
                "category": "RealTime",
                "subCategory": "Mock",
                "severity": "Minimal" if severity == "minor" else severity,
                "ordinal": index,
                "url": f"/Road/all/Disruption/TIMS-MQTT-{index}",
                "comments": f"Mock {severity} disruption",
                "corridorIds": ["A2"],
                "lastModifiedTime": "2024-01-01T00:00:00+00:00",
                "status": "Active",
                "isActive": True,
                "hasClosures": severity == "closure",
            }
            await self.publish_disruption(raw, dedupe=False)


async def _connect_client(args: argparse.Namespace) -> UkGovTflRoadMqttMqttClient:
    broker_host, broker_port, tls_from_url, url_user, url_password = _parse_broker_url(args.mqtt_broker_url)
    tls_enabled = args.mqtt_enable_tls or tls_from_url or broker_port == 8883
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=args.mqtt_client_id or "tfl-road-traffic-mqtt",
        protocol=MQTTv5,
    )
    auth_mode = (args.mqtt_auth_mode or "anonymous").lower()
    username = args.mqtt_username or url_user
    password = args.mqtt_password or url_password
    if auth_mode == "userpass":
        paho_client.username_pw_set(username or "", password or "")
    elif auth_mode == "tls-cert":
        tls_enabled = True
    elif auth_mode == "entra":
        paho_client.username_pw_set(username or args.mqtt_client_id or "tfl-road-traffic-mqtt", "")
    if tls_enabled:
        if auth_mode == "tls-cert" and args.mqtt_client_cert:
            paho_client.tls_set(ca_certs=args.mqtt_ca_file, certfile=args.mqtt_client_cert, keyfile=args.mqtt_client_key)
        else:
            paho_client.tls_set(ca_certs=args.mqtt_ca_file)
    loop = asyncio.get_running_loop()
    client = UkGovTflRoadMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    logger.info("Connecting to MQTT broker %s:%s (tls=%s, auth=%s)", broker_host, broker_port, tls_enabled, auth_mode)
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        from paho.mqtt.packettypes import PacketTypes
        from paho.mqtt.properties import Properties
        credential = ManagedIdentityCredential(client_id=args.mqtt_entra_client_id) if args.mqtt_entra_client_id else DefaultAzureCredential()
        token = credential.get_token(args.mqtt_entra_audience)
        props = Properties(PacketTypes.CONNECT)
        props.AuthenticationMethod = "OAUTH2-JWT"
        props.AuthenticationData = token.token.encode("utf-8")
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=props)
        paho_client.loop_start()
    else:
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
    feed.add_argument("--mqtt-client-cert", default=os.getenv("MQTT_CLIENT_CERT"))
    feed.add_argument("--mqtt-client-key", default=os.getenv("MQTT_CLIENT_KEY"))
    feed.add_argument("--mqtt-ca-file", default=os.getenv("MQTT_CA_FILE"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed.add_argument("--mqtt-entra-client-id", default=os.getenv("MQTT_ENTRA_CLIENT_ID"))
    feed.add_argument("--mqtt-entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/"))
    feed.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    feed.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    feed.add_argument("--emit-mock-corpus", action="store_true", default=_env_bool("TFL_ROAD_TRAFFIC_MQTT_EMIT_MOCK_CORPUS", False))
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
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info("Shutting down")


if __name__ == "__main__":
    main()
