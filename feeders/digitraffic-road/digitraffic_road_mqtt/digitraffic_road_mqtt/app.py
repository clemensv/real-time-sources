from __future__ import annotations

import argparse
import asyncio
import base64
import dataclasses
import gzip
import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, Set, Type, TypeVar
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
import requests
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

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

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-digitraffic-road/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

DIGITRAFFIC_MQTT_HOST = "tie.digitraffic.fi"
DIGITRAFFIC_MQTT_PORT = 443

TOPIC_TMS = "tms-v2/#"
TOPIC_WEATHER = "weather-v2/#"
TOPIC_TRAFFIC_MESSAGE = "traffic-message-v3/simple/#"
TOPIC_MAINTENANCE = "maintenance-v2/routes/#"

_SITUATION_TYPES = {
    "TRAFFIC_ANNOUNCEMENT": "traffic-announcement",
    "ROAD_WORK": "road-work",
    "WEIGHT_RESTRICTION": "weight-restriction",
    "EXEMPTED_TRANSPORT": "exempted-transport",
}


class MQTTSource:
    """Connects to Digitraffic Road MQTT and delivers parsed messages for all families."""

    def __init__(
        self,
        host: str = DIGITRAFFIC_MQTT_HOST,
        port: int = DIGITRAFFIC_MQTT_PORT,
        subscribe_tms: bool = True,
        subscribe_weather: bool = True,
        subscribe_traffic_messages: bool = True,
        subscribe_maintenance: bool = True,
        station_filter: Optional[Set[int]] = None,
        max_retry_delay: int = 60,
    ):
        self.host = host
        self.port = port
        self.subscribe_tms = subscribe_tms
        self.subscribe_weather = subscribe_weather
        self.subscribe_traffic_messages = subscribe_traffic_messages
        self.subscribe_maintenance = subscribe_maintenance
        self.station_filter = station_filter
        self.max_retry_delay = max_retry_delay
        self._callback: Optional[Callable[[str, Dict[str, Any], Dict[str, Any]], None]] = None
        self._retry_delay = 1

    def _get_topics(self) -> list:
        """Build list of MQTT topic subscriptions."""
        topics = []
        if self.station_filter:
            for sid in self.station_filter:
                if self.subscribe_tms:
                    topics.append(f"tms-v2/{sid}/+")
                if self.subscribe_weather:
                    topics.append(f"weather-v2/{sid}/+")
        else:
            if self.subscribe_tms:
                topics.append(TOPIC_TMS)
            if self.subscribe_weather:
                topics.append(TOPIC_WEATHER)
        if self.subscribe_traffic_messages:
            topics.append(TOPIC_TRAFFIC_MESSAGE)
        if self.subscribe_maintenance:
            topics.append(TOPIC_MAINTENANCE)
        return topics

    def stream(self, callback: Callable[[str, Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Connect and stream messages.

        Callback receives ``(data_type, metadata, payload)``.

        ``data_type`` is one of ``'tms'``, ``'weather'``, ``'traffic-announcement'``,
        ``'road-work'``, ``'weight-restriction'``, ``'exempted-transport'``, or
        ``'maintenance'``.

        ``metadata`` contains topic-derived keys:
        - sensors: ``{"station_id": int, "sensor_id": int}``
        - traffic messages: ``{"situation_type": str}``
        - maintenance: ``{"domain": str}``

        ``payload`` is the parsed JSON dict.

        Reconnects with exponential backoff on failure. Blocks until interrupted.
        """
        self._callback = callback
        self._retry_delay = 1

        while True:
            try:
                self._connect_and_loop()
            except KeyboardInterrupt:
                logger.info("Interrupted — stopping MQTT client.")
                break
            except Exception as e:
                logger.warning(
                    "MQTT connection error: %s. Reconnecting in %ds...",
                    e,
                    self._retry_delay,
                )
                time.sleep(self._retry_delay)
                self._retry_delay = min(self._retry_delay * 2, self.max_retry_delay)

    def _connect_and_loop(self) -> None:
        """Create MQTT client, connect, and run the network loop."""
        client_id = f"digitraffic-road-bridge; {uuid.uuid4()}"

        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            transport="websockets",
            client_id=client_id,
        )

        def on_connect(c, userdata, flags, reason_code, properties):
            if reason_code == 0:
                logger.info("MQTT connected to %s:%d", self.host, self.port)
                topics = self._get_topics()
                for t in topics:
                    c.subscribe(t)
                    logger.info("  Subscribed: %s", t)
                self._retry_delay = 1
            else:
                logger.error("MQTT connect failed: %s", reason_code)
                raise ConnectionError(f"MQTT connect failed: {reason_code}")

        def on_disconnect(c, userdata, flags, reason_code, properties):
            if reason_code != 0:
                logger.warning("MQTT disconnected unexpectedly: %s", reason_code)

        def on_message(c, userdata, msg):
            topic_parts = msg.topic.split("/")
            prefix = topic_parts[0]

            if prefix in ("tms-v2", "weather-v2"):
                self._handle_sensor(prefix, topic_parts, msg.payload)
            elif prefix == "traffic-message-v3":
                self._handle_traffic_message(topic_parts, msg.payload)
            elif prefix == "maintenance-v2":
                self._handle_maintenance(topic_parts, msg.payload)

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

        client.ws_set_options(headers={"User-Agent": USER_AGENT})
        client.tls_set()
        logger.info("Connecting to %s:%d ...", self.host, self.port)
        client.connect(self.host, self.port)
        client.loop_forever()

    def _handle_sensor(self, prefix: str, topic_parts: list, raw: bytes) -> None:
        """Parse tms-v2/{stationId}/{sensorId} or weather-v2/{stationId}/{sensorId}."""
        if len(topic_parts) != 3:
            return
        station_str, sensor_str = topic_parts[1], topic_parts[2]
        if station_str == "status":
            return
        try:
            station_id = int(station_str)
            sensor_id = int(sensor_str)
        except ValueError:
            return
        if self.station_filter and station_id not in self.station_filter:
            return
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.debug("Invalid sensor payload: %s", e)
            return
        data_type = "tms" if prefix == "tms-v2" else "weather"
        if self._callback:
            self._callback(data_type, {"station_id": station_id, "sensor_id": sensor_id}, payload)

    def _handle_traffic_message(self, topic_parts: list, raw: bytes) -> None:
        """Parse traffic-message-v3/simple/{situationType}. Payload is base64 + gzip."""
        if len(topic_parts) < 3:
            return
        mqtt_situation_type = topic_parts[2]
        if mqtt_situation_type == "status":
            return
        data_type = _SITUATION_TYPES.get(mqtt_situation_type)
        if not data_type:
            logger.debug("Unknown traffic-message situation type: %s", mqtt_situation_type)
            return
        try:
            decoded = base64.b64decode(raw)
            decompressed = gzip.decompress(decoded)
            payload = json.loads(decompressed.decode("utf-8"))
        except Exception as e:
            logger.debug("Failed to decode traffic-message payload: %s", e)
            return
        if self._callback:
            self._callback(data_type, {"situation_type": mqtt_situation_type}, payload)

    def _handle_maintenance(self, topic_parts: list, raw: bytes) -> None:
        """Parse maintenance-v2/routes/{domain}."""
        if len(topic_parts) < 3:
            return
        domain = topic_parts[2]
        if domain == "status":
            return
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.debug("Invalid maintenance payload: %s", e)
            return
        if self._callback:
            self._callback("maintenance", {"domain": domain}, payload)


DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

_SITUATION_TYPE_LABELS = {
    "TRAFFIC_ANNOUNCEMENT": "traffic announcement",
    "ROAD_WORK": "road work",
    "WEIGHT_RESTRICTION": "weight restriction",
    "EXEMPTED_TRANSPORT": "exempted transport",
}

_TMS_STATIONS_URL = "https://tie.digitraffic.fi/api/tms/v1/stations"
_WEATHER_STATIONS_URL = "https://tie.digitraffic.fi/api/weather/v1/stations"
_MAINTENANCE_TASKS_URL = "https://tie.digitraffic.fi/api/maintenance/v1/tracking/tasks"

T = TypeVar("T")


def _flatten_station(feature: Dict[str, Any]) -> Dict[str, Any]:
    props = feature.get("properties", {})
    coords = feature.get("geometry", {}).get("coordinates", [0.0, 0.0, 0.0])
    names = props.get("names", {})
    road = props.get("roadAddress", {})
    return {
        "station_id": props.get("id", 0),
        "name": props.get("name", ""),
        "tms_number": props.get("tmsNumber"),
        "names_fi": names.get("fi", ""),
        "names_sv": names.get("sv"),
        "names_en": names.get("en"),
        "longitude": coords[0] if len(coords) > 0 else 0.0,
        "latitude": coords[1] if len(coords) > 1 else 0.0,
        "altitude": coords[2] if len(coords) > 2 and coords[2] != 0.0 else None,
        "municipality": props.get("municipality", ""),
        "municipality_code": props.get("municipalityCode", 0),
        "province": props.get("province", ""),
        "province_code": props.get("provinceCode", 0),
        "road_number": road.get("roadNumber", 0),
        "road_section": road.get("roadSection", 0),
        "distance_from_section_start": road.get("distanceFromRoadSectionStart", 0),
        "carriageway": road.get("carriageway"),
        "side": road.get("side"),
        "contract_area": road.get("contractArea"),
        "contract_area_code": road.get("contractAreaCode"),
        "station_type": props.get("stationType", ""),
        "master": props.get("master"),
        "collection_status": props.get("collectionStatus", ""),
        "collection_interval": props.get("collectionInterval"),
        "state": props.get("state"),
        "free_flow_speed_1": props.get("freeFlowSpeed1"),
        "free_flow_speed_2": props.get("freeFlowSpeed2"),
        "bearing": props.get("bearing"),
        "start_time": props.get("startTime", ""),
        "livi_id": props.get("liviId"),
        "sensors": props.get("sensors", []),
        "data_updated_time": props.get("dataUpdatedTime"),
    }


def _flatten_traffic_message(situation_type_mqtt: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    props = payload.get("properties", payload)
    announcement = {}
    announcements = props.get("announcements", [])
    if announcements:
        announcement = announcements[0]

    situation_type_label = _SITUATION_TYPE_LABELS.get(situation_type_mqtt, situation_type_mqtt)

    td = announcement.get("timeAndDuration", {})
    location = announcement.get("location", {})
    contact = props.get("contact", {})
    geometry = payload.get("geometry", {})

    return {
        "situation_id": props.get("situationId", ""),
        "situation_type": situation_type_label,
        "traffic_announcement_type": props.get("trafficAnnouncementType"),
        "version": props.get("version", 0),
        "release_time": props.get("releaseTime", ""),
        "version_time": props.get("versionTime", ""),
        "title": announcement.get("title"),
        "language": announcement.get("language"),
        "sender": announcement.get("sender"),
        "location_description": location.get("description"),
        "start_time": td.get("startTime"),
        "end_time": td.get("endTime"),
        "features_json": json.dumps(announcement.get("features")) if announcement.get("features") else None,
        "road_work_phases_json": json.dumps(announcement.get("roadWorkPhases")) if announcement.get("roadWorkPhases") else None,
        "comment": announcement.get("comment"),
        "additional_information": announcement.get("additionalInformation"),
        "contact_phone": contact.get("phone"),
        "contact_email": contact.get("email"),
        "announcements_json": json.dumps(announcements) if announcements else None,
        "geometry_type": geometry.get("type"),
        "geometry_coordinates_json": json.dumps(geometry.get("coordinates")) if geometry.get("coordinates") else None,
    }


def _serializer_dict(data_cls: Type[T], payload: Dict[str, Any]) -> Dict[str, Any]:
    allowed = {field.name for field in dataclasses.fields(data_cls)}
    return {key: value for key, value in payload.items() if key in allowed}


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_station_filter(value: Optional[str]) -> Optional[Set[int]]:
    if not value:
        return None
    result = set()
    for token in value.split(","):
        token = token.strip()
        if token:
            result.add(int(token))
    return result or None


def _parse_subscribe(value: str) -> Dict[str, bool]:
    requested = {item.strip() for item in value.split(",") if item.strip()}
    known = {"tms", "weather", "traffic-messages", "maintenance"}
    unknown = requested - known
    if unknown:
        raise ValueError(f"Unknown subscribe values: {', '.join(sorted(unknown))}")
    return {
        "subscribe_tms": "tms" in requested,
        "subscribe_weather": "weather" in requested,
        "subscribe_traffic_messages": "traffic-messages" in requested,
        "subscribe_maintenance": "maintenance" in requested,
    }


def _parse_mqtt_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in {"mqtts", "ssl", "tls"}
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if tls else 1883)
    return host, port, tls, parsed.username or None, parsed.password or None


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple[str, datetime]:
    try:
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    except ImportError as exc:
        raise RuntimeError("azure-identity must be installed to use MQTT_AUTH_MODE=entra") from exc

    credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
    scope = audience if audience.endswith("/.default") else f"{audience}/.default"
    token = credential.get_token(scope)
    expires_at = datetime.fromtimestamp(token.expires_on, tz=timezone.utc)
    return token.token, expires_at


async def _entra_token_refresh_loop(
    paho_client: mqtt.Client,
    broker_host: str,
    broker_port: int,
    keepalive: int,
    audience: str,
    client_id: Optional[str],
    expires_at: datetime,
) -> None:
    while True:
        now = datetime.now(timezone.utc)
        sleep_seconds = max(60.0, (expires_at - now).total_seconds() - 300.0)
        await asyncio.sleep(sleep_seconds)
        try:
            new_token, expires_at = _acquire_entra_token(audience, client_id)
            props = Properties(PacketTypes.CONNECT)
            props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
            props.AuthenticationData = new_token.encode("utf-8")
            try:
                paho_client.disconnect()
            except Exception:
                pass
            try:
                paho_client.connect(
                    broker_host,
                    broker_port,
                    keepalive=keepalive,
                    clean_start=True,
                    properties=props,
                )
                logger.info("Refreshed Entra JWT and reconnected MQTT client (expires=%s)", expires_at.isoformat())
            except Exception as exc:
                logger.warning("Reconnect after token refresh failed: %s", exc)
        except Exception as exc:
            logger.error("Failed to refresh Entra JWT: %s", exc)
            await asyncio.sleep(60)


class DigitrafficRoadMqttBridge:
    def __init__(
        self,
        upstream_source: MQTTSource,
        mqtt_client: FiDigitrafficRoadMqttMqttClient,
        flush_interval: int = 500,
    ) -> None:
        self._upstream_source = upstream_source
        self._client = mqtt_client
        self._flush_interval = flush_interval
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._count = 0

    async def run(self, mock: bool = False) -> None:
        broker_host = getattr(self._client, "_broker_host", "localhost")
        broker_port = getattr(self._client, "_broker_port", 1883)
        self._client.loop = asyncio.get_running_loop()
        await self._client.connect(broker_host, broker_port)
        try:
            if mock:
                await self.emit_mock_corpus()
                await asyncio.sleep(2)
                return
            await self._emit_reference_data()
            self._loop = asyncio.get_event_loop()
            await self._loop.run_in_executor(None, self._source_thread)
        finally:
            await self._client.disconnect()

    async def emit_mock_corpus(self) -> None:
        now = int(datetime.now(timezone.utc).timestamp())
        now_iso = datetime.now(timezone.utc).isoformat()

        tms_station = TmsStation.from_serializer_dict(
            {
                "station_id": 23001,
                "name": "vt7_Rita",
                "tms_number": 1,
                "names_fi": "Tie 7 Porvoo, Rita",
                "names_sv": "Väg 7 Borgå, Rita",
                "names_en": "Road 7 Porvoo, Rita",
                "longitude": 25.689529,
                "latitude": 60.417002,
                "altitude": None,
                "municipality": "Porvoo",
                "municipality_code": 638,
                "province": "Uusimaa",
                "province_code": 1,
                "road_number": 7,
                "road_section": 10,
                "distance_from_section_start": 950,
                "carriageway": "DUAL_CARRIAGEWAY_RIGHT_IN_INCREASING_DIRECTION",
                "side": "LEFT",
                "station_type": "DSL_6",
                "collection_status": "GATHERING",
                "state": "OK",
                "free_flow_speed_1": 105.0,
                "free_flow_speed_2": 95.0,
                "bearing": 60,
                "start_time": "2001-11-07T00:00:00Z",
                "livi_id": "Livi968639",
                "sensors": [5122],
                "data_updated_time": now_iso,
            }
        )
        weather_station = WeatherStation.from_serializer_dict(
            {
                "station_id": 1012,
                "name": "kt51_Espoo_Kivenlahti",
                "names_fi": "Tie 51 Espoo, Kivenlahti",
                "names_sv": "Väg 51 Esbo, Stensvik",
                "names_en": "Road 51 Espoo, Kivenlahti",
                "longitude": 24.654321,
                "latitude": 60.152345,
                "altitude": None,
                "municipality": "Espoo",
                "municipality_code": 49,
                "province": "Uusimaa",
                "province_code": 1,
                "road_number": 51,
                "road_section": 3,
                "distance_from_section_start": 250,
                "carriageway": "MAIN",
                "side": "RIGHT",
                "contract_area": "Espoo 19-24",
                "contract_area_code": 142,
                "station_type": "WEATHER_STATION",
                "master": True,
                "collection_status": "GATHERING",
                "collection_interval": 300,
                "state": None,
                "start_time": "2005-01-01T00:00:00Z",
                "livi_id": "Livi1090115",
                "sensors": [1],
                "data_updated_time": now_iso,
            }
        )
        task_type = MaintenanceTaskType.from_serializer_dict(
            {
                "task_id": "SALTING",
                "name_fi": "Suolaus",
                "name_en": "Salting",
                "name_sv": "Saltning",
                "data_updated_time": now_iso,
            }
        )
        tms_data = TmsSensorData.from_serializer_dict(
            {
                "station_id": 23001,
                "sensor_id": 5122,
                "value": 108.0,
                "time": now,
                "start": now - 300,
                "end": now,
            }
        )
        weather_data = WeatherSensorData.from_serializer_dict(
            {
                "station_id": 1012,
                "sensor_id": 1,
                "value": 2.9,
                "time": now,
            }
        )
        traffic_message = TrafficMessage.from_serializer_dict(
            {
                "situation_id": "GUID_12345678",
                "situation_type": "traffic announcement",
                "traffic_announcement_type": "GENERAL",
                "version": 1,
                "release_time": now_iso,
                "version_time": now_iso,
                "title": "Mock traffic announcement",
                "language": "fi",
                "sender": "Digitraffic",
                "location_description": "Tie 7 Porvoo, Rita",
                "start_time": now_iso,
                "end_time": None,
                "features_json": json.dumps([{"name": "lane closure"}]),
                "road_work_phases_json": None,
                "comment": "Mock event",
                "additional_information": "Docker E2E corpus",
                "contact_phone": "+358000000000",
                "contact_email": "digitraffic@example.invalid",
                "announcements_json": json.dumps([{"title": "Mock traffic announcement"}]),
                "geometry_type": "Point",
                "geometry_coordinates_json": json.dumps([25.689529, 60.417002]),
            }
        )
        maintenance = MaintenanceTracking.from_serializer_dict(
            {
                "domain": "state-roads",
                "time": now,
                "source": "Harja/Väylävirasto",
                "tasks": ["SALTING"],
                "x": 24.9384,
                "y": 60.1699,
                "direction": 90.0,
            }
        )

        await self._client.publish_fi_digitraffic_road_mqtt_tms_station(station_id="23001", data=tms_station, qos=1, retain=True)
        await self._client.publish_fi_digitraffic_road_mqtt_weather_station(station_id="1012", data=weather_station, qos=1, retain=True)
        await self._client.publish_fi_digitraffic_road_mqtt_maintenance_task_type(task_id="SALTING", data=task_type, qos=1, retain=True)
        await self._client.publish_fi_digitraffic_road_mqtt_tms_sensor_data(station_id="23001", sensor_id="5122", data=tms_data)
        await self._client.publish_fi_digitraffic_road_mqtt_weather_sensor_data(station_id="1012", sensor_id="1", data=weather_data)
        await self._client.publish_fi_digitraffic_road_mqtt_traffic_announcement(situation_id="GUID_12345678", data=traffic_message)
        road_work_msg = TrafficMessage.from_serializer_dict({
            "situation_id": "GUID_ROADWORK1", "situation_type": "road work",
            "traffic_announcement_type": "ROAD_WORK", "version": 1,
            "release_time": now_iso, "version_time": now_iso, "title": "Mock road work",
            "language": "fi", "sender": "Digitraffic", "location_description": "Tie 7",
            "start_time": now_iso, "end_time": None, "features_json": None,
            "road_work_phases_json": None, "comment": None, "additional_information": None,
            "contact_phone": None, "contact_email": None, "announcements_json": None,
            "geometry_type": "Point", "geometry_coordinates_json": json.dumps([25.689529, 60.417002]),
        })
        await self._client.publish_fi_digitraffic_road_mqtt_road_work(situation_id="GUID_ROADWORK1", data=road_work_msg)
        weight_msg = TrafficMessage.from_serializer_dict({
            "situation_id": "GUID_WEIGHT1", "situation_type": "weight restriction",
            "traffic_announcement_type": "WEIGHT_RESTRICTION", "version": 1,
            "release_time": now_iso, "version_time": now_iso, "title": "Mock weight restriction",
            "language": "fi", "sender": "Digitraffic", "location_description": "Tie 7",
            "start_time": now_iso, "end_time": None, "features_json": None,
            "road_work_phases_json": None, "comment": None, "additional_information": None,
            "contact_phone": None, "contact_email": None, "announcements_json": None,
            "geometry_type": "Point", "geometry_coordinates_json": json.dumps([25.689529, 60.417002]),
        })
        await self._client.publish_fi_digitraffic_road_mqtt_weight_restriction(situation_id="GUID_WEIGHT1", data=weight_msg)
        exempted_msg = TrafficMessage.from_serializer_dict({
            "situation_id": "GUID_EXEMPT1", "situation_type": "exempted transport",
            "traffic_announcement_type": "EXEMPTED_TRANSPORT", "version": 1,
            "release_time": now_iso, "version_time": now_iso, "title": "Mock exempted transport",
            "language": "fi", "sender": "Digitraffic", "location_description": "Tie 7",
            "start_time": now_iso, "end_time": None, "features_json": None,
            "road_work_phases_json": None, "comment": None, "additional_information": None,
            "contact_phone": None, "contact_email": None, "announcements_json": None,
            "geometry_type": "Point", "geometry_coordinates_json": json.dumps([25.689529, 60.417002]),
        })
        await self._client.publish_fi_digitraffic_road_mqtt_exempted_transport(situation_id="GUID_EXEMPT1", data=exempted_msg)
        await self._client.publish_fi_digitraffic_road_mqtt_maintenance_tracking(domain="state-roads", data=maintenance)

    async def _emit_reference_data(self) -> None:
        tms_response = requests.get(_TMS_STATIONS_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
        tms_response.raise_for_status()
        for feature in tms_response.json().get("features", []):
            flat = _flatten_station(feature)
            await self._client.publish_fi_digitraffic_road_mqtt_tms_station(
                station_id=str(flat["station_id"]),
                data=TmsStation.from_serializer_dict(_serializer_dict(TmsStation, flat)),
                qos=1,
                retain=True,
            )

        weather_response = requests.get(_WEATHER_STATIONS_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
        weather_response.raise_for_status()
        for feature in weather_response.json().get("features", []):
            flat = _flatten_station(feature)
            await self._client.publish_fi_digitraffic_road_mqtt_weather_station(
                station_id=str(flat["station_id"]),
                data=WeatherStation.from_serializer_dict(_serializer_dict(WeatherStation, flat)),
                qos=1,
                retain=True,
            )

        tasks_response = requests.get(_MAINTENANCE_TASKS_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
        tasks_response.raise_for_status()
        for task in tasks_response.json():
            flat = {
                "task_id": task.get("id", ""),
                "name_fi": task.get("nameFi", ""),
                "name_en": task.get("nameEn", ""),
                "name_sv": task.get("nameSv", ""),
                "data_updated_time": task.get("dataUpdatedTime"),
            }
            await self._client.publish_fi_digitraffic_road_mqtt_maintenance_task_type(
                task_id=flat["task_id"],
                data=MaintenanceTaskType.from_serializer_dict(flat),
                qos=1,
                retain=True,
            )

    def _source_thread(self) -> None:
        self._upstream_source.stream(self._on_message_sync)

    def _on_message_sync(self, data_type: str, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
        if self._loop is None:
            raise RuntimeError("Asyncio loop is not available for MQTT publish dispatch")
        future = asyncio.run_coroutine_threadsafe(self._publish_message(data_type, metadata, payload), self._loop)
        future.add_done_callback(self._log_publish_failure)

    @staticmethod
    def _log_publish_failure(future: "asyncio.Future[Any]") -> None:
        try:
            future.result()
        except Exception as exc:
            logger.error("Failed to publish MQTT message: %s", exc)

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
            await self._client.publish_fi_digitraffic_road_mqtt_tms_sensor_data(
                station_id=str(station_id),
                sensor_id=str(sensor_id),
                data=data,
            )
        elif data_type == "weather":
            station_id = int(metadata["station_id"])
            sensor_id = int(metadata["sensor_id"])
            enriched = dict(payload)
            enriched["station_id"] = station_id
            enriched["sensor_id"] = sensor_id
            data = WeatherSensorData.from_serializer_dict(_serializer_dict(WeatherSensorData, enriched))
            await self._client.publish_fi_digitraffic_road_mqtt_weather_sensor_data(
                station_id=str(station_id),
                sensor_id=str(sensor_id),
                data=data,
            )
        elif data_type in {"traffic-announcement", "road-work", "weight-restriction", "exempted-transport"}:
            flat = _flatten_traffic_message(str(metadata["situation_type"]), payload)
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
        else:
            logger.debug("Skipping unsupported data type: %s", data_type)
            return

        self._count += 1
        if self._flush_interval > 0 and self._count % self._flush_interval == 0:
            await asyncio.sleep(0)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if os.getenv("PYTHONDEBUG") else logging.INFO)

    parser = argparse.ArgumentParser(description="Digitraffic Road -> MQTT/UNS bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Bridge Digitraffic Road events to MQTT")
    feed_parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", "0")) or None)
    feed_parser.add_argument("--enable-tls", action="store_true", default=_env_bool("MQTT_ENABLE_TLS", False))
    feed_parser.add_argument("--auth-mode", choices=["anonymous", "userpass", "entra"], default=os.getenv("MQTT_AUTH_MODE", "anonymous"))
    feed_parser.add_argument("--username", default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--entra-client-id", default=os.getenv("MQTT_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE))
    feed_parser.add_argument("--subscribe", default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather,traffic-messages,maintenance"))
    feed_parser.add_argument("--station-filter", default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"))
    feed_parser.add_argument("--mock", action="store_true", default=_env_bool("DIGITRAFFIC_ROAD_MOCK", False))

    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return

    subscribe_flags = _parse_subscribe(args.subscribe)
    station_filter = _parse_station_filter(args.station_filter)

    if args.broker_url:
        broker_host, broker_port, parsed_tls, parsed_user, parsed_password = _parse_mqtt_broker_url(args.broker_url)
        broker_port = args.port or broker_port
        enable_tls = parsed_tls or args.enable_tls or args.auth_mode == "entra"
        username = args.username or parsed_user
        password = args.password or parsed_password
    else:
        broker_host = "localhost"
        enable_tls = args.enable_tls or args.auth_mode == "entra"
        broker_port = args.port or (8883 if enable_tls else 1883)
        username = args.username
        password = args.password

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id="",
        protocol=MQTTv5,
    )
    if enable_tls:
        paho_client.tls_set()
    if args.auth_mode == "userpass" and username:
        paho_client.username_pw_set(username, password or "")

    mqtt_client = FiDigitrafficRoadMqttMqttClient(client=paho_client, content_mode="binary")
    mqtt_client._broker_host = broker_host
    mqtt_client._broker_port = broker_port

    if args.auth_mode == "entra":
        if username:
            paho_client.username_pw_set(username, "")
        refresh_task: Optional[asyncio.Task[Any]] = None

        async def connect_with_entra(broker: str, port: int = 1883, keepalive: int = 60) -> None:
            nonlocal refresh_task
            token, expires_at = _acquire_entra_token(args.entra_audience, args.entra_client_id)
            props = Properties(PacketTypes.CONNECT)
            props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
            props.AuthenticationData = token.encode("utf-8")
            paho_client.connect(broker, port, keepalive=keepalive, clean_start=True, properties=props)
            paho_client.loop_start()
            refresh_task = asyncio.create_task(
                _entra_token_refresh_loop(
                    paho_client,
                    broker,
                    port,
                    keepalive,
                    args.entra_audience,
                    args.entra_client_id,
                    expires_at,
                )
            )

        async def disconnect_with_entra() -> None:
            nonlocal refresh_task
            if refresh_task is not None:
                refresh_task.cancel()
                try:
                    await refresh_task
                except asyncio.CancelledError:
                    pass
            paho_client.loop_stop()
            paho_client.disconnect()

        mqtt_client.connect = connect_with_entra  # type: ignore[method-assign]
        mqtt_client.disconnect = disconnect_with_entra  # type: ignore[method-assign]

    upstream_source = MQTTSource(station_filter=station_filter, **subscribe_flags)
    bridge = DigitrafficRoadMqttBridge(upstream_source, mqtt_client)
    asyncio.run(bridge.run(mock=args.mock))


if __name__ == "__main__":
    main()
