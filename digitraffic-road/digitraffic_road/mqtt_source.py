"""Digitraffic Road MQTT source — Finnish road TMS and weather sensor data."""

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


class MQTTSource:
    """Connects to Digitraffic Road MQTT and delivers parsed sensor messages."""

    def __init__(
        self,
        host: str = DIGITRAFFIC_MQTT_HOST,
        port: int = DIGITRAFFIC_MQTT_PORT,
        subscribe_tms: bool = True,
        subscribe_weather: bool = True,
        station_filter: Optional[Set[int]] = None,
        max_retry_delay: int = 60,
    ):
        self.host = host
        self.port = port
        self.subscribe_tms = subscribe_tms
        self.subscribe_weather = subscribe_weather
        self.station_filter = station_filter
        self.max_retry_delay = max_retry_delay
        self._callback: Optional[Callable[[str, int, int, Dict[str, Any]], None]] = None
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
        return topics

    def stream(self, callback: Callable[[str, int, int, Dict[str, Any]], None]) -> None:
        """Connect and stream messages. Callback receives (data_type, station_id, sensor_id, payload).

        data_type is 'tms' or 'weather'.
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
            try:
                payload = json.loads(msg.payload.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logger.debug("Invalid MQTT payload: %s", e)
                return

            topic_parts = msg.topic.split("/")
            # Expected: tms-v2/<stationId>/<sensorId> or weather-v2/<stationId>/<sensorId>
            # Also handle status topics like tms-v2/status
            if len(topic_parts) != 3:
                return

            prefix = topic_parts[0]
            station_str = topic_parts[1]
            sensor_str = topic_parts[2]

            # Skip status messages
            if station_str == "status":
                return

            try:
                station_id = int(station_str)
                sensor_id = int(sensor_str)
            except ValueError:
                return

            if prefix == "tms-v2":
                data_type = "tms"
            elif prefix == "weather-v2":
                data_type = "weather"
            else:
                return

            if self.station_filter and station_id not in self.station_filter:
                return

            if self._callback:
                self._callback(data_type, station_id, sensor_id, payload)

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

        client.tls_set()
        logger.info("Connecting to %s:%d ...", self.host, self.port)
        client.connect(self.host, self.port)
        client.loop_forever()
