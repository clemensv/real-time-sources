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
import autobahn_mqtt_producer_data
from autobahn_mqtt_producer_data import RoadEvent
from autobahn_mqtt_producer_data import WarningEvent
from autobahn_mqtt_producer_data import Webcam
from autobahn_mqtt_producer_data import ParkingLorry
from autobahn_mqtt_producer_data import ChargingStation


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



def get_default_topic_mappings_de_autobahn_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the DE.Autobahn.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "DE.Autobahn.RoadworkAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/appeared",
        "DE.Autobahn.RoadworkUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/updated",
        "DE.Autobahn.RoadworkResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/resolved",
        "DE.Autobahn.ShortTermRoadworkAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/appeared",
        "DE.Autobahn.ShortTermRoadworkUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/updated",
        "DE.Autobahn.ShortTermRoadworkResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/resolved",
        "DE.Autobahn.ClosureAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/closure/{identifier}/appeared",
        "DE.Autobahn.ClosureUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/closure/{identifier}/updated",
        "DE.Autobahn.ClosureResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/closure/{identifier}/resolved",
        "DE.Autobahn.EntryExitClosureAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/appeared",
        "DE.Autobahn.EntryExitClosureUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/updated",
        "DE.Autobahn.EntryExitClosureResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/resolved",
        "DE.Autobahn.WarningAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/warning/{identifier}/appeared",
        "DE.Autobahn.WarningUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/warning/{identifier}/updated",
        "DE.Autobahn.WarningResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/warning/{identifier}/resolved",
        "DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/appeared",
        "DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/updated",
        "DE.Autobahn.WeightLimit35RestrictionResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/resolved",
        "DE.Autobahn.WebcamAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/appeared",
        "DE.Autobahn.WebcamUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/updated",
        "DE.Autobahn.WebcamResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/resolved",
        "DE.Autobahn.ParkingLorryAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/appeared",
        "DE.Autobahn.ParkingLorryUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/updated",
        "DE.Autobahn.ParkingLorryResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/resolved",
        "DE.Autobahn.ElectricChargingStationAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/appeared",
        "DE.Autobahn.ElectricChargingStationUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/updated",
        "DE.Autobahn.ElectricChargingStationResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/resolved",
        "DE.Autobahn.StrongElectricChargingStationAppeared.mqtt": "traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/appeared",
        "DE.Autobahn.StrongElectricChargingStationUpdated.mqtt": "traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/updated",
        "DE.Autobahn.StrongElectricChargingStationResolved.mqtt": "traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/resolved",
    }


def get_subscription_topics_de_autobahn_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_de_autobahn_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class DEAutobahnMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the DE.Autobahn.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_de_autobahn_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.de_autobahn_roadwork_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_roadwork_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_roadwork_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_short_term_roadwork_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_short_term_roadwork_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_short_term_roadwork_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_closure_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_closure_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_closure_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_entry_exit_closure_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_entry_exit_closure_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_entry_exit_closure_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_warning_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.WarningEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_warning_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.WarningEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_warning_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.WarningEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_weight_limit35_restriction_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_weight_limit35_restriction_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_weight_limit35_restriction_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.RoadEvent, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_webcam_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.Webcam, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_webcam_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.Webcam, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_webcam_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.Webcam, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_parking_lorry_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ParkingLorry, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_parking_lorry_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ParkingLorry, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_parking_lorry_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ParkingLorry, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_electric_charging_station_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ChargingStation, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_electric_charging_station_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ChargingStation, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_electric_charging_station_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ChargingStation, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_strong_electric_charging_station_appeared_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ChargingStation, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_strong_electric_charging_station_updated_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ChargingStation, Dict[str, str]], Awaitable[None]]] = None
        
        self.de_autobahn_strong_electric_charging_station_resolved_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, autobahn_mqtt_producer_data.ChargingStation, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "DE.Autobahn.RoadworkAppeared":
            if self.de_autobahn_roadwork_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.RoadworkAppeared.mqtt")
                    await self.de_autobahn_roadwork_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_roadwork_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.RoadworkUpdated":
            if self.de_autobahn_roadwork_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.RoadworkUpdated.mqtt")
                    await self.de_autobahn_roadwork_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_roadwork_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.RoadworkResolved":
            if self.de_autobahn_roadwork_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.RoadworkResolved.mqtt")
                    await self.de_autobahn_roadwork_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_roadwork_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ShortTermRoadworkAppeared":
            if self.de_autobahn_short_term_roadwork_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ShortTermRoadworkAppeared.mqtt")
                    await self.de_autobahn_short_term_roadwork_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_short_term_roadwork_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ShortTermRoadworkUpdated":
            if self.de_autobahn_short_term_roadwork_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ShortTermRoadworkUpdated.mqtt")
                    await self.de_autobahn_short_term_roadwork_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_short_term_roadwork_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ShortTermRoadworkResolved":
            if self.de_autobahn_short_term_roadwork_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ShortTermRoadworkResolved.mqtt")
                    await self.de_autobahn_short_term_roadwork_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_short_term_roadwork_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ClosureAppeared":
            if self.de_autobahn_closure_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ClosureAppeared.mqtt")
                    await self.de_autobahn_closure_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_closure_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ClosureUpdated":
            if self.de_autobahn_closure_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ClosureUpdated.mqtt")
                    await self.de_autobahn_closure_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_closure_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ClosureResolved":
            if self.de_autobahn_closure_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ClosureResolved.mqtt")
                    await self.de_autobahn_closure_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_closure_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.EntryExitClosureAppeared":
            if self.de_autobahn_entry_exit_closure_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.EntryExitClosureAppeared.mqtt")
                    await self.de_autobahn_entry_exit_closure_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_entry_exit_closure_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.EntryExitClosureUpdated":
            if self.de_autobahn_entry_exit_closure_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.EntryExitClosureUpdated.mqtt")
                    await self.de_autobahn_entry_exit_closure_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_entry_exit_closure_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.EntryExitClosureResolved":
            if self.de_autobahn_entry_exit_closure_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.EntryExitClosureResolved.mqtt")
                    await self.de_autobahn_entry_exit_closure_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_entry_exit_closure_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WarningAppeared":
            if self.de_autobahn_warning_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.WarningEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WarningAppeared.mqtt")
                    await self.de_autobahn_warning_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_warning_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WarningUpdated":
            if self.de_autobahn_warning_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.WarningEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WarningUpdated.mqtt")
                    await self.de_autobahn_warning_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_warning_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WarningResolved":
            if self.de_autobahn_warning_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.WarningEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WarningResolved.mqtt")
                    await self.de_autobahn_warning_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_warning_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WeightLimit35RestrictionAppeared":
            if self.de_autobahn_weight_limit35_restriction_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt")
                    await self.de_autobahn_weight_limit35_restriction_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_weight_limit35_restriction_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WeightLimit35RestrictionUpdated":
            if self.de_autobahn_weight_limit35_restriction_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt")
                    await self.de_autobahn_weight_limit35_restriction_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_weight_limit35_restriction_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WeightLimit35RestrictionResolved":
            if self.de_autobahn_weight_limit35_restriction_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.RoadEvent.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WeightLimit35RestrictionResolved.mqtt")
                    await self.de_autobahn_weight_limit35_restriction_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_weight_limit35_restriction_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WebcamAppeared":
            if self.de_autobahn_webcam_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.Webcam.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WebcamAppeared.mqtt")
                    await self.de_autobahn_webcam_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_webcam_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WebcamUpdated":
            if self.de_autobahn_webcam_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.Webcam.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WebcamUpdated.mqtt")
                    await self.de_autobahn_webcam_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_webcam_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.WebcamResolved":
            if self.de_autobahn_webcam_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.Webcam.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.WebcamResolved.mqtt")
                    await self.de_autobahn_webcam_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_webcam_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ParkingLorryAppeared":
            if self.de_autobahn_parking_lorry_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ParkingLorry.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ParkingLorryAppeared.mqtt")
                    await self.de_autobahn_parking_lorry_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_parking_lorry_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ParkingLorryUpdated":
            if self.de_autobahn_parking_lorry_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ParkingLorry.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ParkingLorryUpdated.mqtt")
                    await self.de_autobahn_parking_lorry_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_parking_lorry_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ParkingLorryResolved":
            if self.de_autobahn_parking_lorry_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ParkingLorry.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ParkingLorryResolved.mqtt")
                    await self.de_autobahn_parking_lorry_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_parking_lorry_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ElectricChargingStationAppeared":
            if self.de_autobahn_electric_charging_station_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ChargingStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ElectricChargingStationAppeared.mqtt")
                    await self.de_autobahn_electric_charging_station_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_electric_charging_station_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ElectricChargingStationUpdated":
            if self.de_autobahn_electric_charging_station_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ChargingStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ElectricChargingStationUpdated.mqtt")
                    await self.de_autobahn_electric_charging_station_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_electric_charging_station_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.ElectricChargingStationResolved":
            if self.de_autobahn_electric_charging_station_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ChargingStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.ElectricChargingStationResolved.mqtt")
                    await self.de_autobahn_electric_charging_station_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_electric_charging_station_resolved_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.StrongElectricChargingStationAppeared":
            if self.de_autobahn_strong_electric_charging_station_appeared_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ChargingStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.StrongElectricChargingStationAppeared.mqtt")
                    await self.de_autobahn_strong_electric_charging_station_appeared_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_strong_electric_charging_station_appeared_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.StrongElectricChargingStationUpdated":
            if self.de_autobahn_strong_electric_charging_station_updated_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ChargingStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.StrongElectricChargingStationUpdated.mqtt")
                    await self.de_autobahn_strong_electric_charging_station_updated_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_strong_electric_charging_station_updated_mqtt handler: {e}")
            return
        
        if event_type == "DE.Autobahn.StrongElectricChargingStationResolved":
            if self.de_autobahn_strong_electric_charging_station_resolved_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = autobahn_mqtt_producer_data.ChargingStation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "DE.Autobahn.StrongElectricChargingStationResolved.mqtt")
                    await self.de_autobahn_strong_electric_charging_station_resolved_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in de_autobahn_strong_electric_charging_station_resolved_mqtt handler: {e}")
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
            topics = get_subscription_topics_de_autobahn_mqtt(self._topic_mappings)
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
    
    async def publish_de_autobahn_roadwork_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.RoadworkAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.RoadworkAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_roadwork_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.RoadworkUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.RoadworkUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_roadwork_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.RoadworkResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.RoadworkResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_short_term_roadwork_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ShortTermRoadworkAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ShortTermRoadworkAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_short_term_roadwork_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ShortTermRoadworkUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ShortTermRoadworkUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_short_term_roadwork_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ShortTermRoadworkResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ShortTermRoadworkResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_closure_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ClosureAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/closure/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/closure/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ClosureAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_closure_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ClosureUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/closure/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/closure/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ClosureUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_closure_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ClosureResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/closure/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/closure/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ClosureResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_entry_exit_closure_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.EntryExitClosureAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.EntryExitClosureAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_entry_exit_closure_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.EntryExitClosureUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.EntryExitClosureUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_entry_exit_closure_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.EntryExitClosureResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.EntryExitClosureResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_warning_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.WarningEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WarningAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/warning/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/warning/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WarningAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_warning_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.WarningEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WarningUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/warning/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/warning/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WarningUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_warning_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.WarningEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WarningResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/warning/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/warning/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WarningResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_weight_limit35_restriction_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WeightLimit35RestrictionAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_weight_limit35_restriction_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WeightLimit35RestrictionUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_weight_limit35_restriction_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.RoadEvent,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WeightLimit35RestrictionResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WeightLimit35RestrictionResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_webcam_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.Webcam,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WebcamAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WebcamAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_webcam_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.Webcam,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WebcamUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WebcamUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_webcam_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.Webcam,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.WebcamResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.WebcamResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_parking_lorry_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ParkingLorry,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ParkingLorryAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ParkingLorryAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_parking_lorry_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ParkingLorry,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ParkingLorryUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ParkingLorryUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_parking_lorry_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ParkingLorry,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ParkingLorryResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ParkingLorryResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_electric_charging_station_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ChargingStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ElectricChargingStationAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ElectricChargingStationAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_electric_charging_station_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ChargingStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ElectricChargingStationUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ElectricChargingStationUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_electric_charging_station_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ChargingStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.ElectricChargingStationResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.ElectricChargingStationResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_strong_electric_charging_station_appeared_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ChargingStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.StrongElectricChargingStationAppeared.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/appeared'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/appeared"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.StrongElectricChargingStationAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_strong_electric_charging_station_updated_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ChargingStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.StrongElectricChargingStationUpdated.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/updated'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/updated"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.StrongElectricChargingStationUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
    async def publish_de_autobahn_strong_electric_charging_station_resolved_mqtt(self,
        identifier: str,
        event_time: str,
        road: str,
        data: autobahn_mqtt_producer_data.ChargingStation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'DE.Autobahn.StrongElectricChargingStationResolved.mqtt' event to an MQTT topic.

        Args:
        
            identifier: URI template variable for 'identifier'
            event_time: URI template variable for 'event_time'
            road: URI template variable for 'road'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/resolved'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/resolved"
        _topic_template_values: Dict[str, str] = {
            "identifier": str(identifier),
            "event_time": str(event_time),
            "road": str(road),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"DE.Autobahn.StrongElectricChargingStationResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = identifier),
             "time":"{event_time}".format(event_time = event_time)
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

    
