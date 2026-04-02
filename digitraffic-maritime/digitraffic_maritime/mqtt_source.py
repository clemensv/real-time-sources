"""MQTT source for Digitraffic Marine AIS data with auto-reconnect."""

import json
import logging
import time
import uuid
from typing import Any, Callable, Dict, Optional

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

DIGITRAFFIC_MQTT_HOST = "meri.digitraffic.fi"
DIGITRAFFIC_MQTT_PORT = 443

TOPIC_LOCATION = "vessels-v2/+/location"
TOPIC_METADATA = "vessels-v2/+/metadata"


class MQTTSource:
    """Connects to Digitraffic Marine MQTT and delivers parsed JSON messages."""

    def __init__(self, host: str = DIGITRAFFIC_MQTT_HOST,
                 port: int = DIGITRAFFIC_MQTT_PORT,
                 subscribe_locations: bool = True,
                 subscribe_metadata: bool = True,
                 mmsi_filter: Optional[set] = None,
                 max_retry_delay: int = 60):
        self.host = host
        self.port = port
        self.subscribe_locations = subscribe_locations
        self.subscribe_metadata = subscribe_metadata
        self.mmsi_filter = mmsi_filter
        self.max_retry_delay = max_retry_delay
        self._callback: Optional[Callable[[str, int, Dict[str, Any]], None]] = None
        self._retry_delay = 1

    def _get_topics(self) -> list:
        """Build list of MQTT topic subscriptions."""
        topics = []
        if self.mmsi_filter:
            for mmsi in self.mmsi_filter:
                if self.subscribe_locations:
                    topics.append(f"vessels-v2/{mmsi}/location")
                if self.subscribe_metadata:
                    topics.append(f"vessels-v2/{mmsi}/metadata")
        else:
            if self.subscribe_locations:
                topics.append(TOPIC_LOCATION)
            if self.subscribe_metadata:
                topics.append(TOPIC_METADATA)
        return topics

    def stream(self, callback: Callable[[str, int, Dict[str, Any]], None]) -> None:
        """Connect and stream messages. Callback receives (topic_type, mmsi, payload).

        topic_type is 'location' or 'metadata'.
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
                logger.warning("MQTT connection error: %s. Reconnecting in %ds...",
                               e, self._retry_delay)
                time.sleep(self._retry_delay)
                self._retry_delay = min(self._retry_delay * 2, self.max_retry_delay)

    def _connect_and_loop(self) -> None:
        """Create MQTT client, connect, and run the network loop."""
        client_id = f"digitraffic-maritime-bridge; {uuid.uuid4()}"

        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            transport="websockets",
            client_id=client_id,
        )

        connected_event = _ConnectedEvent()

        def on_connect(c, userdata, flags, reason_code, properties):
            if reason_code == 0:
                logger.info("MQTT connected to %s:%d", self.host, self.port)
                topics = self._get_topics()
                for t in topics:
                    c.subscribe(t)
                    logger.info("  Subscribed: %s", t)
                self._retry_delay = 1
                connected_event.set()
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
            if len(topic_parts) != 3:
                return

            mmsi_str = topic_parts[1]
            topic_type = topic_parts[2]

            try:
                mmsi = int(mmsi_str)
            except ValueError:
                return

            if self._callback:
                self._callback(topic_type, mmsi, payload)

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

        client.tls_set()
        logger.info("Connecting to %s:%d ...", self.host, self.port)
        client.connect(self.host, self.port)
        client.loop_forever()


class _ConnectedEvent:
    """Simple flag to track connection state."""
    def __init__(self):
        self._connected = False

    def set(self):
        self._connected = True

    @property
    def is_set(self):
        return self._connected
