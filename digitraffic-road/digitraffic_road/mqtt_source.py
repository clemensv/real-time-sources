"""Digitraffic Road MQTT source — Finnish road traffic data."""

import base64
import gzip
import json
import logging
import time
import uuid
from typing import Any, Callable, Dict, Optional, Set

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

DIGITRAFFIC_MQTT_HOST = "tie.digitraffic.fi"
DIGITRAFFIC_MQTT_PORT = 443

TOPIC_TMS = "tms-v2/#"
TOPIC_WEATHER = "weather-v2/#"
TOPIC_TRAFFIC_MESSAGE = "traffic-message-v3/simple/#"
TOPIC_MAINTENANCE = "maintenance-v2/routes/#"

# MQTT situation type to internal name
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

        client.tls_set()
        logger.info("Connecting to %s:%d ...", self.host, self.port)
        client.connect(self.host, self.port)
        client.loop_forever()

    # ── topic handlers ─────────────────────────────────────────────────

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
        # topic: traffic-message-v3/simple/{situationType}
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
        # topic: maintenance-v2/routes/{domain}
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
