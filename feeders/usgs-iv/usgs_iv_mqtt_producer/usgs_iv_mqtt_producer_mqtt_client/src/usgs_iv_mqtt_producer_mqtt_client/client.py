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


def _apply_message_expiry(publish_kwargs: Dict[str, typing.Any], target_topic: str) -> None:
    if not _MQTT5_AVAILABLE:
        return
    expiry = 86400 if target_topic.endswith('/observation') else 2592000 if (target_topic.endswith('/info') or target_topic.endswith('/timeseries')) else None
    if expiry is None:
        return
    props = publish_kwargs.get("properties")
    if props is None:
        props = _MqttProperties(_MqttPacketTypes.PUBLISH)
        publish_kwargs["properties"] = props
    props.MessageExpiryInterval = expiry


async def _publish_and_wait(client: mqtt.Client, topic: str, payload: typing.Any, publish_kwargs: Dict[str, typing.Any]) -> None:
    info = client.publish(topic, payload, **publish_kwargs)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        raise RuntimeError(f"MQTT publish to {topic!r} failed to queue: rc={info.rc}")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, info.wait_for_publish)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        raise RuntimeError(f"MQTT publish to {topic!r} failed: rc={info.rc}")

from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent
import usgs_iv_mqtt_producer_data
from usgs_iv_mqtt_producer_data import Site
from usgs_iv_mqtt_producer_data import SiteTimeseries
from usgs_iv_mqtt_producer_data import OtherParameter
from usgs_iv_mqtt_producer_data import Precipitation
from usgs_iv_mqtt_producer_data import Streamflow
from usgs_iv_mqtt_producer_data import GageHeight
from usgs_iv_mqtt_producer_data import WaterTemperature
from usgs_iv_mqtt_producer_data import DissolvedOxygen
from usgs_iv_mqtt_producer_data import PH
from usgs_iv_mqtt_producer_data import SpecificConductance
from usgs_iv_mqtt_producer_data import Turbidity
from usgs_iv_mqtt_producer_data import AirTemperature
from usgs_iv_mqtt_producer_data import WindSpeed
from usgs_iv_mqtt_producer_data import WindDirection
from usgs_iv_mqtt_producer_data import RelativeHumidity
from usgs_iv_mqtt_producer_data import BarometricPressure
from usgs_iv_mqtt_producer_data import TurbidityFNU
from usgs_iv_mqtt_producer_data import FDOM
from usgs_iv_mqtt_producer_data import ReservoirStorage
from usgs_iv_mqtt_producer_data import LakeElevationNGVD29
from usgs_iv_mqtt_producer_data import WaterDepth
from usgs_iv_mqtt_producer_data import EquipmentStatus
from usgs_iv_mqtt_producer_data import TidallyFilteredDischarge
from usgs_iv_mqtt_producer_data import WaterVelocity
from usgs_iv_mqtt_producer_data import EstuaryElevationNGVD29
from usgs_iv_mqtt_producer_data import LakeElevationNAVD88
from usgs_iv_mqtt_producer_data import Salinity
from usgs_iv_mqtt_producer_data import GateOpening


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



def get_default_topic_mappings_usgs_sites_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the USGS.Sites.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "USGS.Sites.mqtt.Site": "hydro/us/usgs/usgs-iv/{site_no}/info",
    }


def get_subscription_topics_usgs_sites_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_usgs_sites_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class USGSSitesMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the USGS.Sites.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_usgs_sites_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.usgs_sites_mqtt_site_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.Site, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "USGS.Sites.Site":
            if self.usgs_sites_mqtt_site_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.Site.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.Sites.mqtt.Site")
                    await self.usgs_sites_mqtt_site_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_sites_mqtt_site handler: {e}")
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
            topics = get_subscription_topics_usgs_sites_mqtt(self._topic_mappings)
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
    
    async def publish_usgs_sites_mqtt_site(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        data: usgs_iv_mqtt_producer_data.Site,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.Sites.mqtt.Site' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/info"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.Sites.Site",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}".format(agency_cd = agency_cd,site_no = site_no)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    


def get_default_topic_mappings_usgs_sitetimeseries_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the USGS.SiteTimeseries.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "USGS.SiteTimeseries.mqtt.SiteTimeseries": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/timeseries",
    }


def get_subscription_topics_usgs_sitetimeseries_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_usgs_sitetimeseries_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class USGSSiteTimeseriesMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the USGS.SiteTimeseries.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_usgs_sitetimeseries_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.usgs_site_timeseries_mqtt_site_timeseries_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.SiteTimeseries, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "USGS.Sites.SiteTimeseries":
            if self.usgs_site_timeseries_mqtt_site_timeseries_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.SiteTimeseries.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.SiteTimeseries.mqtt.SiteTimeseries")
                    await self.usgs_site_timeseries_mqtt_site_timeseries_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_site_timeseries_mqtt_site_timeseries handler: {e}")
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
            topics = get_subscription_topics_usgs_sitetimeseries_mqtt(self._topic_mappings)
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
    
    async def publish_usgs_site_timeseries_mqtt_site_timeseries(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        data: usgs_iv_mqtt_producer_data.SiteTimeseries,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.SiteTimeseries.mqtt.SiteTimeseries' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/timeseries'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/timeseries"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.Sites.SiteTimeseries",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    


def get_default_topic_mappings_usgs_instantaneousvalues_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the USGS.InstantaneousValues.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "USGS.InstantaneousValues.mqtt.OtherParameter": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.Precipitation": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.Streamflow": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.GageHeight": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.WaterTemperature": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.DissolvedOxygen": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.pH": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.SpecificConductance": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.Turbidity": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.AirTemperature": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.WindSpeed": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.WindDirection": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.RelativeHumidity": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.BarometricPressure": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.TurbidityFNU": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.fDOM": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.ReservoirStorage": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.LakeElevationNGVD29": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.WaterDepth": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.EquipmentStatus": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.WaterVelocity": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.LakeElevationNAVD88": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.Salinity": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
        "USGS.InstantaneousValues.mqtt.GateOpening": "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation",
    }


def get_subscription_topics_usgs_instantaneousvalues_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_usgs_instantaneousvalues_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class USGSInstantaneousValuesMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the USGS.InstantaneousValues.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_usgs_instantaneousvalues_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.usgs_instantaneous_values_mqtt_other_parameter_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.OtherParameter, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_precipitation_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.Precipitation, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_streamflow_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.Streamflow, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_gage_height_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.GageHeight, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_water_temperature_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.WaterTemperature, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_dissolved_oxygen_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.DissolvedOxygen, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_p_h_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.PH, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_specific_conductance_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.SpecificConductance, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_turbidity_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.Turbidity, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_air_temperature_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.AirTemperature, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_wind_speed_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.WindSpeed, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_wind_direction_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.WindDirection, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_relative_humidity_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.RelativeHumidity, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_barometric_pressure_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.BarometricPressure, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_turbidity_fnu_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.TurbidityFNU, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_f_dom_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.FDOM, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_reservoir_storage_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.ReservoirStorage, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.LakeElevationNGVD29, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_water_depth_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.WaterDepth, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_equipment_status_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.EquipmentStatus, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_tidally_filtered_discharge_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.TidallyFilteredDischarge, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_water_velocity_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.WaterVelocity, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.EstuaryElevationNGVD29, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_lake_elevation_navd88_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.LakeElevationNAVD88, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_salinity_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.Salinity, Dict[str, str]], Awaitable[None]]] = None
        
        self.usgs_instantaneous_values_mqtt_gate_opening_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, usgs_iv_mqtt_producer_data.GateOpening, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "USGS.InstantaneousValues.OtherParameter":
            if self.usgs_instantaneous_values_mqtt_other_parameter_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.OtherParameter.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.OtherParameter")
                    await self.usgs_instantaneous_values_mqtt_other_parameter_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_other_parameter handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.Precipitation":
            if self.usgs_instantaneous_values_mqtt_precipitation_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.Precipitation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.Precipitation")
                    await self.usgs_instantaneous_values_mqtt_precipitation_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_precipitation handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.Streamflow":
            if self.usgs_instantaneous_values_mqtt_streamflow_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.Streamflow.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.Streamflow")
                    await self.usgs_instantaneous_values_mqtt_streamflow_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_streamflow handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.GageHeight":
            if self.usgs_instantaneous_values_mqtt_gage_height_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.GageHeight.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.GageHeight")
                    await self.usgs_instantaneous_values_mqtt_gage_height_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_gage_height handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.WaterTemperature":
            if self.usgs_instantaneous_values_mqtt_water_temperature_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.WaterTemperature.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.WaterTemperature")
                    await self.usgs_instantaneous_values_mqtt_water_temperature_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_water_temperature handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.DissolvedOxygen":
            if self.usgs_instantaneous_values_mqtt_dissolved_oxygen_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.DissolvedOxygen.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.DissolvedOxygen")
                    await self.usgs_instantaneous_values_mqtt_dissolved_oxygen_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_dissolved_oxygen handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.pH":
            if self.usgs_instantaneous_values_mqtt_p_h_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.PH.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.pH")
                    await self.usgs_instantaneous_values_mqtt_p_h_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_p_h handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.SpecificConductance":
            if self.usgs_instantaneous_values_mqtt_specific_conductance_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.SpecificConductance.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.SpecificConductance")
                    await self.usgs_instantaneous_values_mqtt_specific_conductance_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_specific_conductance handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.Turbidity":
            if self.usgs_instantaneous_values_mqtt_turbidity_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.Turbidity.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.Turbidity")
                    await self.usgs_instantaneous_values_mqtt_turbidity_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_turbidity handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.AirTemperature":
            if self.usgs_instantaneous_values_mqtt_air_temperature_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.AirTemperature.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.AirTemperature")
                    await self.usgs_instantaneous_values_mqtt_air_temperature_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_air_temperature handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.WindSpeed":
            if self.usgs_instantaneous_values_mqtt_wind_speed_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.WindSpeed.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.WindSpeed")
                    await self.usgs_instantaneous_values_mqtt_wind_speed_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_wind_speed handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.WindDirection":
            if self.usgs_instantaneous_values_mqtt_wind_direction_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.WindDirection.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.WindDirection")
                    await self.usgs_instantaneous_values_mqtt_wind_direction_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_wind_direction handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.RelativeHumidity":
            if self.usgs_instantaneous_values_mqtt_relative_humidity_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.RelativeHumidity.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.RelativeHumidity")
                    await self.usgs_instantaneous_values_mqtt_relative_humidity_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_relative_humidity handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.BarometricPressure":
            if self.usgs_instantaneous_values_mqtt_barometric_pressure_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.BarometricPressure.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.BarometricPressure")
                    await self.usgs_instantaneous_values_mqtt_barometric_pressure_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_barometric_pressure handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.TurbidityFNU":
            if self.usgs_instantaneous_values_mqtt_turbidity_fnu_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.TurbidityFNU.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.TurbidityFNU")
                    await self.usgs_instantaneous_values_mqtt_turbidity_fnu_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_turbidity_fnu handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.fDOM":
            if self.usgs_instantaneous_values_mqtt_f_dom_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.FDOM.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.fDOM")
                    await self.usgs_instantaneous_values_mqtt_f_dom_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_f_dom handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.ReservoirStorage":
            if self.usgs_instantaneous_values_mqtt_reservoir_storage_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.ReservoirStorage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.ReservoirStorage")
                    await self.usgs_instantaneous_values_mqtt_reservoir_storage_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_reservoir_storage handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.LakeElevationNGVD29":
            if self.usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.LakeElevationNGVD29.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.LakeElevationNGVD29")
                    await self.usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_lake_elevation_ngvd29 handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.WaterDepth":
            if self.usgs_instantaneous_values_mqtt_water_depth_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.WaterDepth.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.WaterDepth")
                    await self.usgs_instantaneous_values_mqtt_water_depth_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_water_depth handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.EquipmentStatus":
            if self.usgs_instantaneous_values_mqtt_equipment_status_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.EquipmentStatus.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.EquipmentStatus")
                    await self.usgs_instantaneous_values_mqtt_equipment_status_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_equipment_status handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.TidallyFilteredDischarge":
            if self.usgs_instantaneous_values_mqtt_tidally_filtered_discharge_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.TidallyFilteredDischarge.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge")
                    await self.usgs_instantaneous_values_mqtt_tidally_filtered_discharge_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_tidally_filtered_discharge handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.WaterVelocity":
            if self.usgs_instantaneous_values_mqtt_water_velocity_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.WaterVelocity.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.WaterVelocity")
                    await self.usgs_instantaneous_values_mqtt_water_velocity_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_water_velocity handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.EstuaryElevationNGVD29":
            if self.usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.EstuaryElevationNGVD29.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29")
                    await self.usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29 handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.LakeElevationNAVD88":
            if self.usgs_instantaneous_values_mqtt_lake_elevation_navd88_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.LakeElevationNAVD88.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.LakeElevationNAVD88")
                    await self.usgs_instantaneous_values_mqtt_lake_elevation_navd88_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_lake_elevation_navd88 handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.Salinity":
            if self.usgs_instantaneous_values_mqtt_salinity_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.Salinity.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.Salinity")
                    await self.usgs_instantaneous_values_mqtt_salinity_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_salinity handler: {e}")
            return
        
        if event_type == "USGS.InstantaneousValues.GateOpening":
            if self.usgs_instantaneous_values_mqtt_gate_opening_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = usgs_iv_mqtt_producer_data.GateOpening.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "USGS.InstantaneousValues.mqtt.GateOpening")
                    await self.usgs_instantaneous_values_mqtt_gate_opening_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in usgs_instantaneous_values_mqtt_gate_opening handler: {e}")
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
            topics = get_subscription_topics_usgs_instantaneousvalues_mqtt(self._topic_mappings)
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
    
    async def publish_usgs_instantaneous_values_mqtt_other_parameter(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.OtherParameter,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.OtherParameter' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.OtherParameter",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_precipitation(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.Precipitation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.Precipitation' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.Precipitation",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_streamflow(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.Streamflow,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.Streamflow' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.Streamflow",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_gage_height(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.GageHeight,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.GageHeight' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.GageHeight",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_water_temperature(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.WaterTemperature,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.WaterTemperature' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.WaterTemperature",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_dissolved_oxygen(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.DissolvedOxygen,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.DissolvedOxygen' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.DissolvedOxygen",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_p_h(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.PH,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.pH' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.pH",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_specific_conductance(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.SpecificConductance,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.SpecificConductance' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.SpecificConductance",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_turbidity(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.Turbidity,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.Turbidity' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.Turbidity",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_air_temperature(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.AirTemperature,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.AirTemperature' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.AirTemperature",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_wind_speed(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.WindSpeed,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.WindSpeed' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.WindSpeed",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_wind_direction(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.WindDirection,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.WindDirection' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.WindDirection",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_relative_humidity(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.RelativeHumidity,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.RelativeHumidity' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.RelativeHumidity",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_barometric_pressure(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.BarometricPressure,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.BarometricPressure' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.BarometricPressure",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_turbidity_fnu(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.TurbidityFNU,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.TurbidityFNU' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.TurbidityFNU",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_f_dom(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.FDOM,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.fDOM' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.fDOM",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_reservoir_storage(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.ReservoirStorage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.ReservoirStorage' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.ReservoirStorage",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.LakeElevationNGVD29,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.LakeElevationNGVD29' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNGVD29",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_water_depth(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.WaterDepth,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.WaterDepth' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.WaterDepth",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_equipment_status(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.EquipmentStatus,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.EquipmentStatus' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.EquipmentStatus",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_tidally_filtered_discharge(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.TidallyFilteredDischarge,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.TidallyFilteredDischarge",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_water_velocity(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.WaterVelocity,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.WaterVelocity' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.WaterVelocity",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.EstuaryElevationNGVD29,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.EstuaryElevationNGVD29",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_lake_elevation_navd88(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.LakeElevationNAVD88,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.LakeElevationNAVD88' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNAVD88",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_salinity(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.Salinity,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.Salinity' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.Salinity",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
    async def publish_usgs_instantaneous_values_mqtt_gate_opening(self,
        source_uri: str,
        agency_cd: str,
        site_no: str,
        parameter_cd: str,
        timeseries_cd: str,
        datetime: str,
        data: usgs_iv_mqtt_producer_data.GateOpening,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'USGS.InstantaneousValues.mqtt.GateOpening' event to an MQTT topic.

        Args:
        
            source_uri: URI template variable for 'source_uri'
            agency_cd: URI template variable for 'agency_cd'
            site_no: URI template variable for 'site_no'
            parameter_cd: URI template variable for 'parameter_cd'
            timeseries_cd: URI template variable for 'timeseries_cd'
            datetime: URI template variable for 'datetime'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation"
        _topic_template_values: Dict[str, str] = {
            "source_uri": str(source_uri),
            "agency_cd": str(agency_cd),
            "site_no": str(site_no),
            "parameter_cd": str(parameter_cd),
            "timeseries_cd": str(timeseries_cd),
            "datetime": str(datetime),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"USGS.InstantaneousValues.GateOpening",
             "source":"{source_uri}".format(source_uri = source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = agency_cd,site_no = site_no,parameter_cd = parameter_cd,timeseries_cd = timeseries_cd),
             "time":"{datetime}".format(datetime = datetime)
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

        _apply_message_expiry(publish_kwargs, target_topic)
        await _publish_and_wait(self.client, target_topic, payload, publish_kwargs)

    
