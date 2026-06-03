from __future__ import annotations

import argparse
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

from digitraffic_road_amqp_producer_data import (
    MaintenanceTaskType,
    MaintenanceTracking,
    TmsSensorData,
    TmsStation,
    TrafficMessage,
    WeatherSensorData,
    WeatherStation,
)
from digitraffic_road_amqp_producer_amqp_producer.producer import FiDigitrafficRoadAmqpProducer

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


DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"

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


def _parse_amqp_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(
    producer_cls,
    *,
    host: str,
    port: int,
    address: str,
    use_tls: bool,
    content_mode: str,
    auth_mode: str,
    username: Optional[str],
    password: Optional[str],
    entra_audience: str,
    entra_client_id: Optional[str],
    sas_key_name: Optional[str],
    sas_key: Optional[str],
):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return producer_cls(
            host=host,
            address=address,
            port=port,
            content_mode=content_mode,
            credential=credential,
            entra_audience=entra_audience,
            use_tls=use_tls,
        )
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(
            host=host,
            address=address,
            port=port,
            content_mode=content_mode,
            sas_key_name=sas_key_name,
            sas_key=sas_key,
            use_tls=use_tls,
        )
    return producer_cls(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        content_mode=content_mode,
        use_tls=use_tls,
    )


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if not address:
        raise RuntimeError("AMQP address is required")
    logging.info("Connecting AMQP producer to %s:%s/%s auth=%s tls=%s", host, port, address, args.auth_mode, tls)
    return _build_amqp_producer(
        producer_cls,
        host=host,
        port=port,
        address=address,
        use_tls=tls,
        content_mode=args.content_mode,
        auth_mode=args.auth_mode,
        username=username,
        password=password,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name,
        sas_key=args.sas_key,
    )


class DigitrafficRoadAmqpBridge:
    def __init__(self, upstream_source: MQTTSource, producer: FiDigitrafficRoadAmqpProducer) -> None:
        self._upstream_source = upstream_source
        self._producer = producer

    def run(self, mock: bool = False) -> None:
        if mock:
            self.emit_mock_corpus()
            return
        self._emit_reference_data()
        self._upstream_source.stream(self._on_message)

    def emit_mock_corpus(self) -> None:
        now = int(datetime.now(timezone.utc).timestamp())
        now_iso = datetime.now(timezone.utc).isoformat()

        self._producer.send_tms_station(
            data=TmsStation.from_serializer_dict(
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
            ),
            _station_id="23001",
        )
        self._producer.send_weather_station(
            data=WeatherStation.from_serializer_dict(
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
            ),
            _station_id="1012",
        )
        self._producer.send_maintenance_task_type(
            data=MaintenanceTaskType.from_serializer_dict(
                {
                    "task_id": "SALTING",
                    "name_fi": "Suolaus",
                    "name_en": "Salting",
                    "name_sv": "Saltning",
                    "data_updated_time": now_iso,
                }
            ),
            _task_id="SALTING",
        )
        self._producer.send_tms_sensor_data(
            data=TmsSensorData.from_serializer_dict(
                {
                    "station_id": 23001,
                    "sensor_id": 5122,
                    "value": 108.0,
                    "time": now,
                    "start": now - 300,
                    "end": now,
                }
            ),
            _station_id="23001",
            _sensor_id="5122",
        )
        self._producer.send_weather_sensor_data(
            data=WeatherSensorData.from_serializer_dict(
                {
                    "station_id": 1012,
                    "sensor_id": 1,
                    "value": 2.9,
                    "time": now,
                }
            ),
            _station_id="1012",
            _sensor_id="1",
        )
        self._producer.send_traffic_announcement(
            data=TrafficMessage.from_serializer_dict(
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
            ),
            _situation_id="GUID_12345678",
        )
        self._producer.send_maintenance_tracking(
            data=MaintenanceTracking.from_serializer_dict(
                {
                    "domain": "state-roads",
                    "time": now,
                    "source": "Harja/Väylävirasto",
                    "tasks": ["SALTING"],
                    "x": 24.9384,
                    "y": 60.1699,
                    "direction": 90.0,
                }
            ),
            _domain="state-roads",
        )

    def _emit_reference_data(self) -> None:
        tms_response = requests.get(_TMS_STATIONS_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
        tms_response.raise_for_status()
        for feature in tms_response.json().get("features", []):
            flat = _flatten_station(feature)
            self._producer.send_tms_station(
                data=TmsStation.from_serializer_dict(_serializer_dict(TmsStation, flat)),
                _station_id=str(flat["station_id"]),
            )

        weather_response = requests.get(_WEATHER_STATIONS_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
        weather_response.raise_for_status()
        for feature in weather_response.json().get("features", []):
            flat = _flatten_station(feature)
            self._producer.send_weather_station(
                data=WeatherStation.from_serializer_dict(_serializer_dict(WeatherStation, flat)),
                _station_id=str(flat["station_id"]),
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
            self._producer.send_maintenance_task_type(
                data=MaintenanceTaskType.from_serializer_dict(flat),
                _task_id=flat["task_id"],
            )

    def _on_message(self, data_type: str, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
        if data_type == "tms":
            station_id = int(metadata["station_id"])
            sensor_id = int(metadata["sensor_id"])
            enriched = dict(payload)
            enriched["station_id"] = station_id
            enriched["sensor_id"] = sensor_id
            enriched.setdefault("start", None)
            enriched.setdefault("end", None)
            data = TmsSensorData.from_serializer_dict(_serializer_dict(TmsSensorData, enriched))
            self._producer.send_tms_sensor_data(data=data, _station_id=str(station_id), _sensor_id=str(sensor_id))
        elif data_type == "weather":
            station_id = int(metadata["station_id"])
            sensor_id = int(metadata["sensor_id"])
            enriched = dict(payload)
            enriched["station_id"] = station_id
            enriched["sensor_id"] = sensor_id
            data = WeatherSensorData.from_serializer_dict(_serializer_dict(WeatherSensorData, enriched))
            self._producer.send_weather_sensor_data(data=data, _station_id=str(station_id), _sensor_id=str(sensor_id))
        elif data_type in {"traffic-announcement", "road-work", "weight-restriction", "exempted-transport"}:
            flat = _flatten_traffic_message(str(metadata["situation_type"]), payload)
            data = TrafficMessage.from_serializer_dict(flat)
            if data_type == "traffic-announcement":
                self._producer.send_traffic_announcement(data=data, _situation_id=flat["situation_id"])
            elif data_type == "road-work":
                self._producer.send_road_work(data=data, _situation_id=flat["situation_id"])
            elif data_type == "weight-restriction":
                self._producer.send_weight_restriction(data=data, _situation_id=flat["situation_id"])
            else:
                self._producer.send_exempted_transport(data=data, _situation_id=flat["situation_id"])
        elif data_type == "maintenance":
            domain = str(metadata["domain"])
            enriched = dict(payload)
            enriched["domain"] = domain
            enriched.setdefault("direction", None)
            enriched.setdefault("source", None)
            data = MaintenanceTracking.from_serializer_dict(_serializer_dict(MaintenanceTracking, enriched))
            self._producer.send_maintenance_tracking(data=data, _domain=domain)
        else:
            logger.debug("Skipping unsupported data type: %s", data_type)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if os.getenv("PYTHONDEBUG") else logging.INFO)

    parser = argparse.ArgumentParser(description="Digitraffic Road -> AMQP 1.0 bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Bridge Digitraffic Road events to AMQP 1.0")
    add_amqp_arguments(feed_parser, "digitraffic-road")
    feed_parser.add_argument("--subscribe", default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather,traffic-messages,maintenance"))
    feed_parser.add_argument("--station-filter", default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"))
    feed_parser.add_argument("--mock", action="store_true", default=_env_bool("DIGITRAFFIC_ROAD_MOCK", False))

    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return

    subscribe_flags = _parse_subscribe(args.subscribe)
    station_filter = _parse_station_filter(args.station_filter)
    producer = create_amqp_producer(args, FiDigitrafficRoadAmqpProducer)
    source = MQTTSource(station_filter=station_filter, **subscribe_flags)
    bridge = DigitrafficRoadAmqpBridge(source, producer)

    try:
        bridge.run(mock=args.mock)
    finally:
        producer.close()


if __name__ == "__main__":
    main()
