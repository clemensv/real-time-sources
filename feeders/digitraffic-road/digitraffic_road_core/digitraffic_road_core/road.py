"""Transport-neutral acquisition helpers for Digitraffic Road feeders."""

from __future__ import annotations

import base64
import gzip
import json
import logging
import os
import time
import uuid
from typing import Any, Callable, Dict, Optional, Set

import paho.mqtt.client as mqtt
import requests

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-digitraffic-road/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com")
    + ")"
)

DIGITRAFFIC_MQTT_HOST = "tie.digitraffic.fi"
DIGITRAFFIC_MQTT_PORT = 443
TOPIC_TMS = "tms-v2/#"
TOPIC_WEATHER = "weather-v2/#"
TOPIC_TRAFFIC_MESSAGE = "traffic-message-v3/simple/#"
TOPIC_MAINTENANCE = "maintenance-v2/routes/#"

_TMS_STATIONS_URL = "https://tie.digitraffic.fi/api/tms/v1/stations"
_WEATHER_STATIONS_URL = "https://tie.digitraffic.fi/api/weather/v1/stations"
_MAINTENANCE_TASKS_URL = "https://tie.digitraffic.fi/api/maintenance/v1/tracking/tasks"

_SITUATION_TYPES = {
    "TRAFFIC_ANNOUNCEMENT": "traffic-announcement",
    "ROAD_WORK": "road-work",
    "WEIGHT_RESTRICTION": "weight-restriction",
    "EXEMPTED_TRANSPORT": "exempted-transport",
}
_SITUATION_TYPE_LABELS = {
    "TRAFFIC_ANNOUNCEMENT": "traffic announcement",
    "ROAD_WORK": "road work",
    "WEIGHT_RESTRICTION": "weight restriction",
    "EXEMPTED_TRANSPORT": "exempted transport",
}


class MQTTSource:
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

    def _get_topics(self) -> list[str]:
        topics = []
        if self.station_filter:
            for station_id in self.station_filter:
                if self.subscribe_tms:
                    topics.append(f"tms-v2/{station_id}/+")
                if self.subscribe_weather:
                    topics.append(f"weather-v2/{station_id}/+")
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
            except Exception as exc:
                logger.warning("MQTT connection error: %s. Reconnecting in %ds...", exc, self._retry_delay)
                time.sleep(self._retry_delay)
                self._retry_delay = min(self._retry_delay * 2, self.max_retry_delay)

    def _connect_and_loop(self) -> None:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            transport="websockets",
            client_id=f"digitraffic-road-bridge; {uuid.uuid4()}",
        )

        def on_connect(c, userdata, flags, reason_code, properties):
            if reason_code == 0:
                logger.info("MQTT connected to %s:%d", self.host, self.port)
                for topic in self._get_topics():
                    c.subscribe(topic)
                    logger.info("  Subscribed: %s", topic)
                self._retry_delay = 1
            else:
                raise ConnectionError(f"MQTT connect failed: {reason_code}")

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
        client.on_message = on_message
        client.ws_set_options(headers={"User-Agent": USER_AGENT})
        client.tls_set()
        logger.info("Connecting to %s:%d ...", self.host, self.port)
        client.connect(self.host, self.port)
        client.loop_forever()

    def _handle_sensor(self, prefix: str, topic_parts: list[str], raw: bytes) -> None:
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
        except (json.JSONDecodeError, UnicodeDecodeError):
            return
        if self._callback:
            self._callback("tms" if prefix == "tms-v2" else "weather", {"station_id": station_id, "sensor_id": sensor_id}, payload)

    def _handle_traffic_message(self, topic_parts: list[str], raw: bytes) -> None:
        if len(topic_parts) < 3:
            return
        mqtt_situation_type = topic_parts[2]
        if mqtt_situation_type == "status":
            return
        data_type = _SITUATION_TYPES.get(mqtt_situation_type)
        if not data_type:
            return
        try:
            payload = json.loads(gzip.decompress(base64.b64decode(raw)).decode("utf-8"))
        except Exception:
            return
        if self._callback:
            self._callback(data_type, {"situation_type": mqtt_situation_type}, payload)

    def _handle_maintenance(self, topic_parts: list[str], raw: bytes) -> None:
        if len(topic_parts) < 3:
            return
        domain = topic_parts[2]
        if domain == "status":
            return
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return
        if self._callback:
            self._callback("maintenance", {"domain": domain}, payload)


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


def fetch_tms_station_payloads() -> list[Dict[str, Any]]:
    response = requests.get(_TMS_STATIONS_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
    response.raise_for_status()
    return [_flatten_station(feature) for feature in response.json().get("features", [])]


def fetch_weather_station_payloads() -> list[Dict[str, Any]]:
    response = requests.get(_WEATHER_STATIONS_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
    response.raise_for_status()
    return [_flatten_station(feature) for feature in response.json().get("features", [])]


def fetch_maintenance_task_payloads() -> list[Dict[str, Any]]:
    response = requests.get(_MAINTENANCE_TASKS_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()
    return [
        {
            "task_id": task.get("id", ""),
            "name_fi": task.get("nameFi", ""),
            "name_en": task.get("nameEn", ""),
            "name_sv": task.get("nameSv", ""),
            "data_updated_time": task.get("dataUpdatedTime"),
        }
        for task in response.json()
    ]


def flatten_traffic_message(situation_type_mqtt: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    props = payload.get("properties", payload)
    announcements = props.get("announcements", [])
    announcement = announcements[0] if announcements else {}
    td = announcement.get("timeAndDuration", {})
    location = announcement.get("location", {})
    contact = props.get("contact", {})
    geometry = payload.get("geometry", {})
    return {
        "situation_id": props.get("situationId", ""),
        "situation_type": _SITUATION_TYPE_LABELS.get(situation_type_mqtt, situation_type_mqtt),
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


def parse_station_filter(value: Optional[str]) -> Optional[Set[int]]:
    if not value:
        return None
    result = {int(token.strip()) for token in value.split(",") if token.strip()}
    return result or None


def parse_subscribe(value: str) -> Dict[str, bool]:
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
