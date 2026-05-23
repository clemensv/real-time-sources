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
import wikimedia_osm_diffs_mqtt_producer_data
from wikimedia_osm_diffs_mqtt_producer_data import MapChange
from wikimedia_osm_diffs_mqtt_producer_data import ReplicationState


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



def get_default_topic_mappings_org_openstreetmap_diffs_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the Org.OpenStreetMap.Diffs.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "Org.OpenStreetMap.Diffs.mqtt.Node": "osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change",
        "Org.OpenStreetMap.Diffs.mqtt.Way": "osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change",
        "Org.OpenStreetMap.Diffs.mqtt.Relation": "osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change",
        "Org.OpenStreetMap.Diffs.mqtt.ReplicationState": "osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state",
    }


def get_subscription_topics_org_openstreetmap_diffs_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_org_openstreetmap_diffs_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class OrgOpenStreetMapDiffsMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the Org.OpenStreetMap.Diffs.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_org_openstreetmap_diffs_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.org_open_street_map_diffs_mqtt_node_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wikimedia_osm_diffs_mqtt_producer_data.MapChange, Dict[str, str]], Awaitable[None]]] = None
        
        self.org_open_street_map_diffs_mqtt_way_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wikimedia_osm_diffs_mqtt_producer_data.MapChange, Dict[str, str]], Awaitable[None]]] = None
        
        self.org_open_street_map_diffs_mqtt_relation_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wikimedia_osm_diffs_mqtt_producer_data.MapChange, Dict[str, str]], Awaitable[None]]] = None
        
        self.org_open_street_map_diffs_mqtt_replication_state_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, wikimedia_osm_diffs_mqtt_producer_data.ReplicationState, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "Org.OpenStreetMap.Diffs.MapChange":
            if self.org_open_street_map_diffs_mqtt_node_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wikimedia_osm_diffs_mqtt_producer_data.MapChange.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Org.OpenStreetMap.Diffs.mqtt.Node")
                    await self.org_open_street_map_diffs_mqtt_node_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in org_open_street_map_diffs_mqtt_node handler: {e}")
            return
        
        if event_type == "Org.OpenStreetMap.Diffs.MapChange":
            if self.org_open_street_map_diffs_mqtt_way_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wikimedia_osm_diffs_mqtt_producer_data.MapChange.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Org.OpenStreetMap.Diffs.mqtt.Way")
                    await self.org_open_street_map_diffs_mqtt_way_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in org_open_street_map_diffs_mqtt_way handler: {e}")
            return
        
        if event_type == "Org.OpenStreetMap.Diffs.MapChange":
            if self.org_open_street_map_diffs_mqtt_relation_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wikimedia_osm_diffs_mqtt_producer_data.MapChange.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Org.OpenStreetMap.Diffs.mqtt.Relation")
                    await self.org_open_street_map_diffs_mqtt_relation_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in org_open_street_map_diffs_mqtt_relation handler: {e}")
            return
        
        if event_type == "Org.OpenStreetMap.Diffs.ReplicationState":
            if self.org_open_street_map_diffs_mqtt_replication_state_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = wikimedia_osm_diffs_mqtt_producer_data.ReplicationState.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Org.OpenStreetMap.Diffs.mqtt.ReplicationState")
                    await self.org_open_street_map_diffs_mqtt_replication_state_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in org_open_street_map_diffs_mqtt_replication_state handler: {e}")
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
            topics = get_subscription_topics_org_openstreetmap_diffs_mqtt(self._topic_mappings)
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
    
    async def publish_org_open_street_map_diffs_mqtt_node(self,
        geohash5: str,
        element_id: str,
        data: wikimedia_osm_diffs_mqtt_producer_data.MapChange,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Org.OpenStreetMap.Diffs.mqtt.Node' event to an MQTT topic.

        Args:
        
            geohash5: URI template variable for 'geohash5'
            element_id: URI template variable for 'element_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change"
        _topic_template_values: Dict[str, str] = {
            "geohash5": str(geohash5),
            "element_id": str(element_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Org.OpenStreetMap.Diffs.MapChange",
             "source":"https://planet.openstreetmap.org/replication/minute",
             "subject":"{geohash5}/{element_id}".format(geohash5 = geohash5,element_id = element_id)
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

        _effective_qos = 0 if qos is None else qos
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

    
    async def publish_org_open_street_map_diffs_mqtt_way(self,
        geohash5: str,
        element_id: str,
        data: wikimedia_osm_diffs_mqtt_producer_data.MapChange,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Org.OpenStreetMap.Diffs.mqtt.Way' event to an MQTT topic.

        Args:
        
            geohash5: URI template variable for 'geohash5'
            element_id: URI template variable for 'element_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change"
        _topic_template_values: Dict[str, str] = {
            "geohash5": str(geohash5),
            "element_id": str(element_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Org.OpenStreetMap.Diffs.MapChange",
             "source":"https://planet.openstreetmap.org/replication/minute",
             "subject":"{geohash5}/{element_id}".format(geohash5 = geohash5,element_id = element_id)
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

        _effective_qos = 0 if qos is None else qos
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

    
    async def publish_org_open_street_map_diffs_mqtt_relation(self,
        geohash5: str,
        element_id: str,
        data: wikimedia_osm_diffs_mqtt_producer_data.MapChange,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Org.OpenStreetMap.Diffs.mqtt.Relation' event to an MQTT topic.

        Args:
        
            geohash5: URI template variable for 'geohash5'
            element_id: URI template variable for 'element_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change"
        _topic_template_values: Dict[str, str] = {
            "geohash5": str(geohash5),
            "element_id": str(element_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Org.OpenStreetMap.Diffs.MapChange",
             "source":"https://planet.openstreetmap.org/replication/minute",
             "subject":"{geohash5}/{element_id}".format(geohash5 = geohash5,element_id = element_id)
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

        _effective_qos = 0 if qos is None else qos
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

    
    async def publish_org_open_street_map_diffs_mqtt_replication_state(self,
        data: wikimedia_osm_diffs_mqtt_producer_data.ReplicationState,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Org.OpenStreetMap.Diffs.mqtt.ReplicationState' event to an MQTT topic.

        Args:
        
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state"
        _topic_template_values: Dict[str, str] = {
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Org.OpenStreetMap.Diffs.ReplicationState",
             "source":"https://planet.openstreetmap.org/replication/minute",
             "subject":"replication-state"
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

    
