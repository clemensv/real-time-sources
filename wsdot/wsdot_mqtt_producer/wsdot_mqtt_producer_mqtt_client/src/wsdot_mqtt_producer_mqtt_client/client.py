# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import json
import re
import typing
from typing import Callable, Awaitable, Optional, Dict, List
import asyncio
import paho.mqtt.client as mqtt
try:
    # paho-mqtt 2.x exposes MQTT5 Properties for the PUBLISH packet type.
    from paho.mqtt.properties import Properties as _MqttProperties
    from paho.mqtt.packettypes import PacketTypes as _MqttPacketTypes
    _MQTT5_AVAILABLE = True
except Exception:  # pragma: no cover - paho < 2 fallback
    _MqttProperties = None  # type: ignore
    _MqttPacketTypes = None  # type: ignore
    _MQTT5_AVAILABLE = False
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent
import wsdot_mqtt_producer_data
from wsdot_mqtt_producer_data import TrafficFlowStation
from wsdot_mqtt_producer_data import TrafficFlowReading
from wsdot_mqtt_producer_data import TravelTimeRoute
from wsdot_mqtt_producer_data import MountainPassCondition
from wsdot_mqtt_producer_data import WeatherStation
from wsdot_mqtt_producer_data import WeatherReading
from wsdot_mqtt_producer_data import TollRate
from wsdot_mqtt_producer_data import CommercialVehicleRestriction
from wsdot_mqtt_producer_data import BorderCrossing
from wsdot_mqtt_producer_data import VesselLocation


# URI template regex pattern
_URI_TEMPLATE_PATTERN = re.compile(r'\{([A-Za-z0-9_]+)\}')


def _topic_to_mqtt_wildcard(topic: str) -> str:
    """Convert URI template placeholders to MQTT wildcards (+)."""
    return _URI_TEMPLATE_PATTERN.sub('+', topic)


def _apply_topic_template(topic_pattern: str, template_values: Optional[Dict[str, str]] = None) -> str:
    """Apply template values to a topic pattern."""
    if not template_values:
        return topic_pattern
    result = topic_pattern
    for key, value in template_values.items():
        result = result.replace('{' + key + '}', value)
    return result


def _build_topic_regex(topic_pattern: str) -> re.Pattern:
    """Build a regex pattern for matching topics and extracting template values."""
    # Escape regex special chars in the topic pattern
    escaped = re.escape(topic_pattern)
    # Restore placeholders (which were escaped to \{...\}) and convert to named groups
    pattern = re.sub(r'\\{([A-Za-z0-9_]+)\\}', r'(?P<\1>[^/]+)', escaped)
    return re.compile('^' + pattern + '$')


def _extract_topic_parameters(topic: str, pattern: re.Pattern) -> Dict[str, str]:
    """Extract URI template placeholder values from a topic."""
    match = pattern.match(topic)
    if match:
        return {k: v for k, v in match.groupdict().items() if v is not None}
    return {}


def _ce_headers_to_mqtt5_properties(headers: Dict[str, str]):
    """Map CloudEvents binary-mode HTTP-style headers onto MQTT 5 PUBLISH properties.

    Per the CloudEvents MQTT 5 protocol binding (binary mode):
      * ``datacontenttype`` becomes the MQTT 5 Content Type property.
      * Every other CloudEvents attribute becomes a User Property whose name
        is the bare attribute name (no ``ce-`` prefix).

    Returns ``None`` when paho's MQTT 5 properties API is unavailable so the
    caller can degrade gracefully without crashing.
    """
    if not _MQTT5_AVAILABLE or _MqttProperties is None or _MqttPacketTypes is None:
        return None
    props = _MqttProperties(_MqttPacketTypes.PUBLISH)
    user_properties: List[tuple] = []
    for raw_key, raw_value in (headers or {}).items():
        if raw_value is None:
            continue
        key = str(raw_key).lower()
        value = raw_value if isinstance(raw_value, str) else str(raw_value)
        if key in ("content-type", "datacontenttype"):
            try:
                props.ContentType = value
            except Exception:
                user_properties.append(("datacontenttype", value))
            continue
        if key.startswith("ce-"):
            key = key[3:]
        if key in ("data", "data_base64"):
            continue
        user_properties.append((key, value))
    if user_properties:
        props.UserProperty = user_properties
    return props


def _mqtt5_properties_to_ce_headers(properties) -> Dict[str, str]:
    """Inverse of :func:`_ce_headers_to_mqtt5_properties` for the receive path."""
    headers: Dict[str, str] = {}
    if properties is None:
        return headers
    content_type = getattr(properties, "ContentType", None)
    if content_type:
        headers["content-type"] = content_type
    user_props = getattr(properties, "UserProperty", None) or []
    for entry in user_props:
        try:
            k, v = entry
        except Exception:
            continue
        headers["ce-" + str(k).lower()] = str(v)
    return headers


class _ClientBase:
    """Base class for MQTT client with CloudEvent detection."""
    
    @staticmethod
    def _is_cloud_event(message: mqtt.MQTTMessage) -> bool:
        """Check if the MQTT message contains a CloudEvent (structured or binary)."""
        # Binary mode: MQTT 5 User Properties carry the CE attributes.
        try:
            props = getattr(message, "properties", None)
            user_props = getattr(props, "UserProperty", None) if props is not None else None
            if user_props:
                keys = {str(k).lower() for k, _ in user_props}
                if {"specversion", "type", "source", "id"}.issubset(keys):
                    return True
        except Exception:
            pass
        # Structured mode: JSON body with CE fields.
        try:
            if message.payload:
                if isinstance(message.payload, bytes):
                    payload_str = message.payload.decode('utf-8')
                    data = json.loads(payload_str)
                    return all(k in data for k in ['specversion', 'type', 'source', 'id'])
            return False
        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            return False

    @staticmethod
    def _cloud_event_from_message(message: mqtt.MQTTMessage) -> Optional[CloudEvent]:
        """Extract CloudEvent from MQTT message (structured or binary mode)."""
        # Binary mode first - rebuild a CloudEvent from MQTT 5 user properties.
        try:
            props = getattr(message, "properties", None)
            user_props = getattr(props, "UserProperty", None) if props is not None else None
            if user_props:
                attributes: Dict[str, str] = {}
                for entry in user_props:
                    try:
                        k, v = entry
                    except Exception:
                        continue
                    attributes[str(k).lower()] = str(v)
                if {"specversion", "type", "source", "id"}.issubset(attributes.keys()):
                    content_type = getattr(props, "ContentType", None)
                    if content_type:
                        attributes["datacontenttype"] = content_type
                    payload = message.payload
                    if isinstance(payload, bytes) and (content_type or "").lower().startswith("application/json"):
                        try:
                            payload = json.loads(payload.decode("utf-8"))
                        except Exception:
                            pass
                    return CloudEvent(attributes, payload)
        except Exception:
            pass
        # Fall back to structured mode (CE JSON in payload).
        try:
            if isinstance(message.payload, bytes):
                payload_str = message.payload.decode('utf-8')
                from cloudevents.http import from_json
                event = from_json(payload_str)
                return event
            return None
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, Exception):
            return None



def get_default_topic_mappings_us_wa_wsdot_traffic_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.traffic.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.traffic.TrafficFlowStation.mqtt": "traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/info",
        "us.wa.wsdot.traffic.TrafficFlowReading.mqtt": "traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/reading",
    }


def get_subscription_topics_us_wa_wsdot_traffic_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_traffic_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotTrafficMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.traffic.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_traffic_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_traffic_traffic_flow_station_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.TrafficFlowStation, Dict[str, str]], Awaitable[None]]] = None
        
        self.us_wa_wsdot_traffic_traffic_flow_reading_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.TrafficFlowReading, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.traffic.TrafficFlowStation":
            if self.us_wa_wsdot_traffic_traffic_flow_station_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.TrafficFlowStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.traffic.TrafficFlowStation.mqtt")
                    await self.us_wa_wsdot_traffic_traffic_flow_station_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_traffic_traffic_flow_station_mqtt handler: {e}")
            return
        
        if event_type == "us.wa.wsdot.traffic.TrafficFlowReading":
            if self.us_wa_wsdot_traffic_traffic_flow_reading_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.TrafficFlowReading.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.traffic.TrafficFlowReading.mqtt")
                    await self.us_wa_wsdot_traffic_traffic_flow_reading_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_traffic_traffic_flow_reading_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_traffic_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_traffic_traffic_flow_station_mqtt(self,
        feedurl: str,
        flow_data_id: str,
        region: str,
        data: wsdot_mqtt_producer_data.TrafficFlowStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.traffic.TrafficFlowStation.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            flow_data_id: URI template variable for 'flow_data_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/info"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "flow_data_id": str(flow_data_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.traffic.TrafficFlowStation",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{flow_data_id}".format(flow_data_id = flow_data_id)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = True if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    
    async def publish_us_wa_wsdot_traffic_traffic_flow_reading_mqtt(self,
        feedurl: str,
        flow_data_id: str,
        region: str,
        data: wsdot_mqtt_producer_data.TrafficFlowReading,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.traffic.TrafficFlowReading.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            flow_data_id: URI template variable for 'flow_data_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/reading'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/reading"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "flow_data_id": str(flow_data_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.traffic.TrafficFlowReading",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{flow_data_id}".format(flow_data_id = flow_data_id)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = False if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    


def get_default_topic_mappings_us_wa_wsdot_traveltimes_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.traveltimes.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt": "traffic/us/wsdot/wsdot/{region}/travel-times/{travel_time_id}/info",
    }


def get_subscription_topics_us_wa_wsdot_traveltimes_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_traveltimes_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotTraveltimesMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.traveltimes.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_traveltimes_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_traveltimes_travel_time_route_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.TravelTimeRoute, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.traveltimes.TravelTimeRoute":
            if self.us_wa_wsdot_traveltimes_travel_time_route_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.TravelTimeRoute.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt")
                    await self.us_wa_wsdot_traveltimes_travel_time_route_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_traveltimes_travel_time_route_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_traveltimes_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_traveltimes_travel_time_route_mqtt(self,
        feedurl: str,
        travel_time_id: str,
        region: str,
        data: wsdot_mqtt_producer_data.TravelTimeRoute,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            travel_time_id: URI template variable for 'travel_time_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/travel-times/{travel_time_id}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/travel-times/{travel_time_id}/info"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "travel_time_id": str(travel_time_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.traveltimes.TravelTimeRoute",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{travel_time_id}".format(travel_time_id = travel_time_id)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = True if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    


def get_default_topic_mappings_us_wa_wsdot_mountainpass_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.mountainpass.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.mountainpass.MountainPassCondition.mqtt": "traffic/us/wsdot/wsdot/{region}/mountain-passes/{mountain_pass_id}/info",
    }


def get_subscription_topics_us_wa_wsdot_mountainpass_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_mountainpass_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotMountainpassMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.mountainpass.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_mountainpass_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.MountainPassCondition, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.mountainpass.MountainPassCondition":
            if self.us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.MountainPassCondition.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.mountainpass.MountainPassCondition.mqtt")
                    await self.us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_mountainpass_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt(self,
        feedurl: str,
        mountain_pass_id: str,
        region: str,
        data: wsdot_mqtt_producer_data.MountainPassCondition,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.mountainpass.MountainPassCondition.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            mountain_pass_id: URI template variable for 'mountain_pass_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/mountain-passes/{mountain_pass_id}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/mountain-passes/{mountain_pass_id}/info"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "mountain_pass_id": str(mountain_pass_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.mountainpass.MountainPassCondition",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{mountain_pass_id}".format(mountain_pass_id = mountain_pass_id)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = True if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    


def get_default_topic_mappings_us_wa_wsdot_weather_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.weather.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.weather.WeatherStation.mqtt": "traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/info",
        "us.wa.wsdot.weather.WeatherReading.mqtt": "traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/reading",
    }


def get_subscription_topics_us_wa_wsdot_weather_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_weather_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotWeatherMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.weather.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_weather_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_weather_weather_station_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.WeatherStation, Dict[str, str]], Awaitable[None]]] = None
        
        self.us_wa_wsdot_weather_weather_reading_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.WeatherReading, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.weather.WeatherStation":
            if self.us_wa_wsdot_weather_weather_station_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.WeatherStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.weather.WeatherStation.mqtt")
                    await self.us_wa_wsdot_weather_weather_station_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_weather_weather_station_mqtt handler: {e}")
            return
        
        if event_type == "us.wa.wsdot.weather.WeatherReading":
            if self.us_wa_wsdot_weather_weather_reading_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.WeatherReading.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.weather.WeatherReading.mqtt")
                    await self.us_wa_wsdot_weather_weather_reading_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_weather_weather_reading_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_weather_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_weather_weather_station_mqtt(self,
        feedurl: str,
        station_id: str,
        region: str,
        data: wsdot_mqtt_producer_data.WeatherStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.weather.WeatherStation.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/info"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.weather.WeatherStation",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{station_id}".format(station_id = station_id)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = True if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    
    async def publish_us_wa_wsdot_weather_weather_reading_mqtt(self,
        feedurl: str,
        station_id: str,
        region: str,
        data: wsdot_mqtt_producer_data.WeatherReading,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.weather.WeatherReading.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/reading'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/reading"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.weather.WeatherReading",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{station_id}".format(station_id = station_id)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = False if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    


def get_default_topic_mappings_us_wa_wsdot_tolls_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.tolls.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.tolls.TollRate.mqtt": "traffic/us/wsdot/wsdot/{region}/tolls/{trip_name}/rate",
    }


def get_subscription_topics_us_wa_wsdot_tolls_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_tolls_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotTollsMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.tolls.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_tolls_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_tolls_toll_rate_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.TollRate, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.tolls.TollRate":
            if self.us_wa_wsdot_tolls_toll_rate_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.TollRate.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.tolls.TollRate.mqtt")
                    await self.us_wa_wsdot_tolls_toll_rate_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_tolls_toll_rate_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_tolls_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_tolls_toll_rate_mqtt(self,
        feedurl: str,
        trip_name: str,
        region: str,
        data: wsdot_mqtt_producer_data.TollRate,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.tolls.TollRate.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            trip_name: URI template variable for 'trip_name'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/tolls/{trip_name}/rate'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/tolls/{trip_name}/rate"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "trip_name": str(trip_name),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.tolls.TollRate",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{trip_name}".format(trip_name = trip_name)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = False if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    


def get_default_topic_mappings_us_wa_wsdot_cvrestrictions_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.cvrestrictions.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt": "traffic/us/wsdot/wsdot/{region}/bridges/{state_route_id}/{bridge_number}/info",
    }


def get_subscription_topics_us_wa_wsdot_cvrestrictions_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_cvrestrictions_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotCvrestrictionsMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.cvrestrictions.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_cvrestrictions_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.CommercialVehicleRestriction, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction":
            if self.us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.CommercialVehicleRestriction.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt")
                    await self.us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_cvrestrictions_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt(self,
        feedurl: str,
        state_route_id: str,
        bridge_number: str,
        region: str,
        data: wsdot_mqtt_producer_data.CommercialVehicleRestriction,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            state_route_id: URI template variable for 'state_route_id'
            bridge_number: URI template variable for 'bridge_number'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/bridges/{state_route_id}/{bridge_number}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/bridges/{state_route_id}/{bridge_number}/info"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "state_route_id": str(state_route_id),
            "bridge_number": str(bridge_number),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{state_route_id}/{bridge_number}".format(state_route_id = state_route_id,bridge_number = bridge_number)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = True if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    


def get_default_topic_mappings_us_wa_wsdot_border_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.border.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.border.BorderCrossing.mqtt": "traffic/us/wsdot/wsdot/{region}/border-crossings/{crossing_name}/info",
    }


def get_subscription_topics_us_wa_wsdot_border_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_border_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotBorderMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.border.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_border_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_border_border_crossing_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.BorderCrossing, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.border.BorderCrossing":
            if self.us_wa_wsdot_border_border_crossing_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.BorderCrossing.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.border.BorderCrossing.mqtt")
                    await self.us_wa_wsdot_border_border_crossing_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_border_border_crossing_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_border_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_border_border_crossing_mqtt(self,
        feedurl: str,
        crossing_name: str,
        region: str,
        data: wsdot_mqtt_producer_data.BorderCrossing,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.border.BorderCrossing.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            crossing_name: URI template variable for 'crossing_name'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/border-crossings/{crossing_name}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/border-crossings/{crossing_name}/info"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "crossing_name": str(crossing_name),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.border.BorderCrossing",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{crossing_name}".format(crossing_name = crossing_name)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = True if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    


def get_default_topic_mappings_us_wa_wsdot_ferries_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the us.wa.wsdot.ferries.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "us.wa.wsdot.ferries.VesselLocation.mqtt": "traffic/us/wsdot/wsdot/{region}/vessels/{vessel_id}/location",
    }


def get_subscription_topics_us_wa_wsdot_ferries_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_ferries_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class UsWaWsdotFerriesMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the us.wa.wsdot.ferries.mqtt message group."""
    
    def __init__(
        self, 
        client: mqtt.Client, 
        topic_mappings: Optional[Dict[str, str]] = None,
        content_mode: typing.Literal['structured', 'binary'] = 'structured', 
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Initialize the MQTT client.

        Args:
            client: Paho MQTT client instance
            topic_mappings: Optional dictionary mapping message identifiers to topic patterns.
                Topic patterns may be URI templates with placeholders like {placeholder}.
                For consumers, placeholders are converted to MQTT wildcards (+) for subscription.
                If not provided, uses default 1:1 mapping.
            content_mode: The content mode for CloudEvents ('structured' or 'binary')
            loop: Optional event loop to use for async operations. If None, will try to get the running loop.
        """
        self.client = client
        self.content_mode = content_mode
        self.loop = loop
        self._topic_mappings = topic_mappings or get_default_topic_mappings_us_wa_wsdot_ferries_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.us_wa_wsdot_ferries_vessel_location_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wsdot_mqtt_producer_data.VesselLocation, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message

    @property
    def topic_mappings(self) -> Dict[str, str]:
        """Get the current topic mappings."""
        return self._topic_mappings.copy()
    
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        """Internal MQTT message callback that dispatches to async handlers."""
        loop = self.loop
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._process_message(message), loop)
    
    async def _process_message(self, message: mqtt.MQTTMessage):
        """Process incoming MQTT message and dispatch to appropriate handler."""
        try:
            if self._is_cloud_event(message):
                cloud_event = self._cloud_event_from_message(message)
                if cloud_event:
                    await self._dispatch_cloud_event(message, cloud_event)
            else:
                # Handle plain MQTT messages (if needed)
                pass
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_topic_params(self, topic: str, message_id: str) -> Dict[str, str]:
        """Extract URI template placeholder values from a topic."""
        if message_id in self._topic_patterns:
            return _extract_topic_parameters(topic, self._topic_patterns[message_id])
        return {}
    
    async def _dispatch_cloud_event(self, mqtt_message: mqtt.MQTTMessage, cloud_event: CloudEvent):
        """Dispatch CloudEvent to the appropriate handler based on type."""
        event_type = cloud_event['type']
        
        
        if event_type == "us.wa.wsdot.ferries.VesselLocation":
            if self.us_wa_wsdot_ferries_vessel_location_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wsdot_mqtt_producer_data.VesselLocation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "us.wa.wsdot.ferries.VesselLocation.mqtt")
                    await self.us_wa_wsdot_ferries_vessel_location_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in us_wa_wsdot_ferries_vessel_location_mqtt handler: {e}")
            return
        
    
    async def subscribe(self, topics: Optional[typing.List[str]] = None, qos: int = 0):
        """
        Subscribe to MQTT topics.

        Args:
            topics: List of topic patterns to subscribe to. If None, subscribes to all 
                default topics with URI template placeholders replaced by MQTT wildcards.
            qos: Quality of Service level (0, 1, or 2)
        """
        if topics is None:
            topics = get_subscription_topics_us_wa_wsdot_ferries_mqtt(self._topic_mappings)
        for topic in topics:
            self.client.subscribe(topic, qos)
    
    async def unsubscribe(self, topics: typing.List[str]):
        """
        Unsubscribe from MQTT topics.

        Args:
            topics: List of topics to unsubscribe from
        """
        for topic in topics:
            self.client.unsubscribe(topic)
    
    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60):
        """
        Connect to MQTT broker.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
        """
        self.client.connect(broker, port, keepalive)
        self.client.loop_start()
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_us_wa_wsdot_ferries_vessel_location_mqtt(self,
        feedurl: str,
        vessel_id: str,
        region: str,
        data: wsdot_mqtt_producer_data.VesselLocation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'us.wa.wsdot.ferries.VesselLocation.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            vessel_id: URI template variable for 'vessel_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/us/wsdot/wsdot/{region}/vessels/{vessel_id}/location'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/us/wsdot/wsdot/{region}/vessels/{vessel_id}/location"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "vessel_id": str(vessel_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"us.wa.wsdot.ferries.VesselLocation",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{vessel_id}".format(vessel_id = vessel_id)
        }
        attributes["datacontenttype"] = content_type
        byte_data = data.to_byte_array(content_type) if data is not None else b''
        # to_byte_array returns str for text content types (e.g. JSON);
        # paho-mqtt will UTF-8 encode str payloads, but cloudevents-sdk's
        # to_binary/to_structured embed the str directly which then becomes
        # a JSON string literal containing the JSON document. Coerce to
        # bytes up-front so receivers can json.loads(payload) once.
        if isinstance(byte_data, str):
            byte_data = byte_data.encode('utf-8')
        event = CloudEvent(attributes, byte_data)

        _effective_qos = 1 if qos is None else qos
        _effective_retain = False if retain is None else retain

        publish_kwargs: Dict[str, typing.Any] = {
            "qos": _effective_qos,
            "retain": _effective_retain,
        }

        if self.content_mode == "structured":
            _headers, body = to_structured(event)
            payload = body
        else:
            headers, body = to_binary(event)
            payload = body
            mqtt5_props = _ce_headers_to_mqtt5_properties(dict(headers or {}))
            if mqtt5_props is not None:
                publish_kwargs["properties"] = mqtt5_props

        # Ensure the MQTT PUBLISH payload is bytes so it is sent as the
        # exact serialized representation; paho-mqtt would UTF-8 encode a
        # str, but a dict (from structured mode) would crash, and any
        # double-encoding upstream would land on the wire untouched.
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode('utf-8')
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')

        self.client.publish(target_topic, payload, **publish_kwargs)

    
