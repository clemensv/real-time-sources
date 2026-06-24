from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import logging
import os
from typing import Any, Dict, Type, TypeVar
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from digitraffic_road_core import (
    MQTTSource,
    fetch_maintenance_task_payloads,
    fetch_tms_station_payloads,
    fetch_weather_station_payloads,
    flatten_traffic_message,
    parse_station_filter,
    parse_subscribe,
)
from digitraffic_road_mqtt_producer_data import (
    MaintenanceTaskType,
    MaintenanceTracking,
    TmsSensorData,
    TmsStation,
    TrafficMessage,
    WeatherSensorData,
    WeatherStation,
)
from digitraffic_road_mqtt_producer_mqtt_client.client import FiDigitrafficRoadMqttMqttClient

logger = logging.getLogger(__name__)
T = TypeVar("T")


def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
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
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    from paho.mqtt.properties import Properties as _MqttConnProps

    connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    connect_props.AuthenticationMethod = "OAUTH2-JWT"
    connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, connect_props


def _serializer_dict(data_cls: Type[T], payload: Dict[str, Any]) -> Dict[str, Any]:
    allowed = {field.name for field in dataclasses.fields(data_cls)}  # type: ignore[arg-type]
    return {key: value for key, value in payload.items() if key in allowed}


class DigitrafficRoadMqttBridge:
    def __init__(self, upstream_source: MQTTSource, client: FiDigitrafficRoadMqttMqttClient) -> None:
        self._upstream_source = upstream_source
        self._client = client
        self._loop: asyncio.AbstractEventLoop | None = None

    async def run(self) -> None:
        self._loop = asyncio.get_running_loop()
        await self._emit_reference_data()
        self._upstream_source.stream(self._on_message)

    async def _emit_reference_data(self) -> None:
        for flat in fetch_tms_station_payloads():
            data = TmsStation.from_serializer_dict(_serializer_dict(TmsStation, flat))
            await self._client.publish_fi_digitraffic_road_mqtt_tms_station(station_id=str(flat["station_id"]), data=data, qos=1, retain=True)
        for flat in fetch_weather_station_payloads():
            data = WeatherStation.from_serializer_dict(_serializer_dict(WeatherStation, flat))
            await self._client.publish_fi_digitraffic_road_mqtt_weather_station(station_id=str(flat["station_id"]), data=data, qos=1, retain=True)
        for flat in fetch_maintenance_task_payloads():
            data = MaintenanceTaskType.from_serializer_dict(flat)
            await self._client.publish_fi_digitraffic_road_mqtt_maintenance_task_type(task_id=flat["task_id"], data=data, qos=1, retain=True)

    def _on_message(self, data_type: str, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
        future = asyncio.run_coroutine_threadsafe(self._publish_message(data_type, metadata, payload), self._loop)  # type: ignore[arg-type]
        future.add_done_callback(self._log_publish_failure)  # type: ignore[arg-type]

    @staticmethod
    def _log_publish_failure(future: "asyncio.Future[Any]") -> None:
        try:
            future.result()
        except Exception as exc:  # pragma: no cover
            logger.warning("publish failed: %s", exc)

    async def _publish_message(self, data_type: str, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
        if data_type == "tms":
            station_id = int(metadata["station_id"])
            sensor_id = int(metadata["sensor_id"])
            enriched = dict(payload)
            enriched["station_id"] = station_id
            enriched["sensor_id"] = sensor_id
            enriched.setdefault("start", None)
            enriched.setdefault("end", None)
            data = TmsSensorData.from_serializer_dict(_serializer_dict(TmsSensorData, enriched))
            await self._client.publish_fi_digitraffic_road_mqtt_tms_sensor_data(station_id=str(station_id), sensor_id=str(sensor_id), data=data)
        elif data_type == "weather":
            station_id = int(metadata["station_id"])
            sensor_id = int(metadata["sensor_id"])
            enriched = dict(payload)
            enriched["station_id"] = station_id
            enriched["sensor_id"] = sensor_id
            data = WeatherSensorData.from_serializer_dict(_serializer_dict(WeatherSensorData, enriched))
            await self._client.publish_fi_digitraffic_road_mqtt_weather_sensor_data(station_id=str(station_id), sensor_id=str(sensor_id), data=data)
        elif data_type in {"traffic-announcement", "road-work", "weight-restriction", "exempted-transport"}:
            flat = flatten_traffic_message(str(metadata["situation_type"]), payload)
            data = TrafficMessage.from_serializer_dict(flat)
            if data_type == "traffic-announcement":
                await self._client.publish_fi_digitraffic_road_mqtt_traffic_announcement(situation_id=flat["situation_id"], data=data)
            elif data_type == "road-work":
                await self._client.publish_fi_digitraffic_road_mqtt_road_work(situation_id=flat["situation_id"], data=data)
            elif data_type == "weight-restriction":
                await self._client.publish_fi_digitraffic_road_mqtt_weight_restriction(situation_id=flat["situation_id"], data=data)
            else:
                await self._client.publish_fi_digitraffic_road_mqtt_exempted_transport(situation_id=flat["situation_id"], data=data)
        elif data_type == "maintenance":
            domain = str(metadata["domain"])
            enriched = dict(payload)
            enriched["domain"] = domain
            enriched.setdefault("direction", None)
            enriched.setdefault("source", None)
            data = MaintenanceTracking.from_serializer_dict(_serializer_dict(MaintenanceTracking, enriched))
            await self._client.publish_fi_digitraffic_road_mqtt_maintenance_tracking(domain=domain, data=data)


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme == "mqtts" else 1883), scheme == "mqtts"


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(
        username=args.mqtt_username,
        password=args.mqtt_password or "",
        client_id=args.mqtt_client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )
    paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or entra_props is not None:
        paho_client.tls_set()
    loop = asyncio.get_running_loop()
    client = FiDigitrafficRoadMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)
    if entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=entra_props)
        paho_client.loop_start()
    else:
        await client.connect(broker_host, broker_port)
    try:
        source = MQTTSource(station_filter=parse_station_filter(args.station_filter), **parse_subscribe(args.subscribe))  # type: ignore[arg-type]
        await DigitrafficRoadMqttBridge(source, client).run()
    finally:
        await client.disconnect()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if os.getenv("PYTHONDEBUG") else logging.INFO)
    parser = argparse.ArgumentParser(description="Digitraffic Road -> MQTT/UNS bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed")
    feed_parser.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed_parser.add_argument("--mqtt-enable-tls", action="store_true", default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed_parser.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--subscribe", default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather,traffic-messages,maintenance"))
    feed_parser.add_argument("--station-filter", default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"))
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
