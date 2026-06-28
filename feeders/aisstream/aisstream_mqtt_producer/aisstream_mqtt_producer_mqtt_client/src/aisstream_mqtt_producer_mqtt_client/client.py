# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import json
import re
import typing
from typing import Callable, Awaitable, Optional, Dict, List
import asyncio
from datetime import datetime, timezone
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
import aisstream_mqtt_producer_data
from aisstream_mqtt_producer_data import PositionReport
from aisstream_mqtt_producer_data import ShipStaticData
from aisstream_mqtt_producer_data import StandardClassBPositionReport
from aisstream_mqtt_producer_data import ExtendedClassBPositionReport
from aisstream_mqtt_producer_data import AidsToNavigationReport
from aisstream_mqtt_producer_data import StaticDataReport
from aisstream_mqtt_producer_data import BaseStationReport
from aisstream_mqtt_producer_data import SafetyBroadcastMessage
from aisstream_mqtt_producer_data import StandardSearchAndRescueAircraftReport
from aisstream_mqtt_producer_data import LongRangeAisBroadcastMessage
from aisstream_mqtt_producer_data import AddressedSafetyMessage
from aisstream_mqtt_producer_data import AddressedBinaryMessage
from aisstream_mqtt_producer_data import AssignedModeCommand
from aisstream_mqtt_producer_data import BinaryAcknowledge
from aisstream_mqtt_producer_data import BinaryBroadcastMessage
from aisstream_mqtt_producer_data import ChannelManagement
from aisstream_mqtt_producer_data import CoordinatedUTCInquiry
from aisstream_mqtt_producer_data import DataLinkManagementMessage
from aisstream_mqtt_producer_data import GnssBroadcastBinaryMessage
from aisstream_mqtt_producer_data import GroupAssignmentCommand
from aisstream_mqtt_producer_data import Interrogation
from aisstream_mqtt_producer_data import MultiSlotBinaryMessage
from aisstream_mqtt_producer_data import SingleSlotBinaryMessage


# URI template regex pattern
_URI_TEMPLATE_PATTERN = re.compile(r'\{([A-Za-z0-9_]+)\}')

_RFC3339_TIMESTAMP_PATTERN = re.compile(
    r'^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})?$'
)


def _normalize_cloudevents_time(value: typing.Any) -> typing.Optional[str]:
    """Validate and normalize CloudEvents ``time`` to RFC 3339."""
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat().replace('+00:00', 'Z')
    text = str(value).strip()
    if not text:
        raise ValueError("CloudEvents 'time' must be an RFC 3339 timestamp")
    if not _RFC3339_TIMESTAMP_PATTERN.fullmatch(text):
        raise ValueError("CloudEvents 'time' must be an RFC 3339 timestamp")
    normalized = text
    if normalized[10] == 't':
        normalized = normalized[:10] + 'T' + normalized[11:]
    if normalized.endswith('z'):
        normalized = normalized[:-1] + 'Z'
    if normalized.endswith('Z'):
        normalized = normalized[:-1] + '+00:00'
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("CloudEvents 'time' must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.isoformat().replace('+00:00', 'Z')


def _resolve_cloudevents_time(
    override: typing.Any = None,
    fallback: typing.Any = None,
) -> str:
    """Resolve CloudEvents ``time`` from override, fallback, or current UTC."""
    if override is not None:
        return _normalize_cloudevents_time(override)
    if fallback is not None:
        return _normalize_cloudevents_time(fallback)
    return _normalize_cloudevents_time(datetime.now(timezone.utc))


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



def get_default_topic_mappings_io_aisstream_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the IO.AISstream.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "IO.AISstream.mqtt.PositionReport": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report",
        "IO.AISstream.mqtt.ShipStaticData": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/ship-static-data",
        "IO.AISstream.mqtt.StandardClassBPositionReport": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-class-b-position-report",
        "IO.AISstream.mqtt.ExtendedClassBPositionReport": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/extended-class-b-position-report",
        "IO.AISstream.mqtt.AidsToNavigationReport": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aids-to-navigation-report",
        "IO.AISstream.mqtt.StaticDataReport": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static-data-report",
        "IO.AISstream.mqtt.BaseStationReport": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/base-station-report",
        "IO.AISstream.mqtt.SafetyBroadcastMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/safety-broadcast-message",
        "IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-search-and-rescue-aircraft-report",
        "IO.AISstream.mqtt.LongRangeAisBroadcastMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/long-range-ais-broadcast-message",
        "IO.AISstream.mqtt.AddressedSafetyMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-safety-message",
        "IO.AISstream.mqtt.AddressedBinaryMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-binary-message",
        "IO.AISstream.mqtt.AssignedModeCommand": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/assigned-mode-command",
        "IO.AISstream.mqtt.BinaryAcknowledge": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-acknowledge",
        "IO.AISstream.mqtt.BinaryBroadcastMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-broadcast-message",
        "IO.AISstream.mqtt.ChannelManagement": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/channel-management",
        "IO.AISstream.mqtt.CoordinatedUTCInquiry": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/coordinated-utc-inquiry",
        "IO.AISstream.mqtt.DataLinkManagementMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/data-link-management-message",
        "IO.AISstream.mqtt.GnssBroadcastBinaryMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/gnss-broadcast-binary-message",
        "IO.AISstream.mqtt.GroupAssignmentCommand": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/group-assignment-command",
        "IO.AISstream.mqtt.Interrogation": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/interrogation",
        "IO.AISstream.mqtt.MultiSlotBinaryMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/multi-slot-binary-message",
        "IO.AISstream.mqtt.SingleSlotBinaryMessage": "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/single-slot-binary-message",
    }


def get_subscription_topics_io_aisstream_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_io_aisstream_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class IOAISstreamMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the IO.AISstream.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_io_aisstream_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        self._connect_waiter: Optional[asyncio.Future[None]] = None
        self._connected = False
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.io_aisstream_mqtt_position_report_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.PositionReport, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_ship_static_data_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.ShipStaticData, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_standard_class_bposition_report_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.StandardClassBPositionReport, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_extended_class_bposition_report_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.ExtendedClassBPositionReport, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_aids_to_navigation_report_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.AidsToNavigationReport, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_static_data_report_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.StaticDataReport, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_base_station_report_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.BaseStationReport, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_safety_broadcast_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.SafetyBroadcastMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_standard_search_and_rescue_aircraft_report_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.StandardSearchAndRescueAircraftReport, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_long_range_ais_broadcast_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.LongRangeAisBroadcastMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_addressed_safety_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.AddressedSafetyMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_addressed_binary_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.AddressedBinaryMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_assigned_mode_command_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.AssignedModeCommand, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_binary_acknowledge_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.BinaryAcknowledge, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_binary_broadcast_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.BinaryBroadcastMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_channel_management_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.ChannelManagement, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_coordinated_utcinquiry_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.CoordinatedUTCInquiry, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_data_link_management_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.DataLinkManagementMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_gnss_broadcast_binary_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.GnssBroadcastBinaryMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_group_assignment_command_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.GroupAssignmentCommand, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_interrogation_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.Interrogation, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_multi_slot_binary_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.MultiSlotBinaryMessage, Dict[str, str]], Awaitable[None]]] = None
        
        self.io_aisstream_mqtt_single_slot_binary_message_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, aisstream_mqtt_producer_data.SingleSlotBinaryMessage, Dict[str, str]], Awaitable[None]]] = None
        
        
        # Attach message callback
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    @staticmethod
    def _mqtt_reason_code_value(reason_code) -> Optional[int]:
        """Best-effort numeric MQTT reason-code extraction across paho callback APIs."""
        if reason_code is None:
            return 0
        value = getattr(reason_code, "value", reason_code)
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _mqtt_reason_code_text(reason_code) -> str:
        """Best-effort textual MQTT reason-code rendering across paho callback APIs."""
        if reason_code is None:
            return "unknown"
        text = str(reason_code).strip()
        if text:
            return text
        code = _ClientBase._mqtt_reason_code_value(reason_code)
        return str(code) if code is not None else "unknown"

    def _resolve_connect_waiter(self, exc: Optional[BaseException] = None):
        waiter = self._connect_waiter
        self._connect_waiter = None
        if waiter is None or waiter.done():
            return
        if exc is None:
            self._connected = True
            waiter.set_result(None)
            return
        self._connected = False
        waiter.set_exception(exc)

    def _notify_connect_waiter(self, exc: Optional[BaseException] = None):
        if self.loop is None:
            return
        self.loop.call_soon_threadsafe(self._resolve_connect_waiter, exc)

    def _on_connect(self, client, userdata, flags, reason_code=0, properties=None):
        """Resolve a pending async connect once the broker replies."""
        if self._mqtt_reason_code_value(reason_code) == 0:
            self._notify_connect_waiter()
            return
        detail = self._mqtt_reason_code_text(reason_code)
        self._notify_connect_waiter(ConnectionError(f"MQTT connect failed: {detail}"))

    def _on_disconnect(self, client, userdata, *args):
        """Fail a pending async connect when the broker disconnects before success."""
        self._connected = False
        if self._connect_waiter is None:
            return
        reason_code = None
        if len(args) == 1:
            reason_code = args[0]
        elif len(args) == 2:
            reason_code = args[0]
        elif len(args) >= 3:
            reason_code = args[1]
        detail = self._mqtt_reason_code_text(reason_code)
        if self._mqtt_reason_code_value(reason_code) in (None, 0):
            detail = "connection closed before authentication completed"
        self._notify_connect_waiter(ConnectionError(f"MQTT connect failed: {detail}"))

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
        
        
        if event_type == "IO.AISstream.PositionReport":
            if self.io_aisstream_mqtt_position_report_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.PositionReport.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.PositionReport")
                    await self.io_aisstream_mqtt_position_report_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_position_report handler: {e}")
            return
        
        if event_type == "IO.AISstream.ShipStaticData":
            if self.io_aisstream_mqtt_ship_static_data_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.ShipStaticData.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.ShipStaticData")
                    await self.io_aisstream_mqtt_ship_static_data_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_ship_static_data handler: {e}")
            return
        
        if event_type == "IO.AISstream.StandardClassBPositionReport":
            if self.io_aisstream_mqtt_standard_class_bposition_report_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.StandardClassBPositionReport.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.StandardClassBPositionReport")
                    await self.io_aisstream_mqtt_standard_class_bposition_report_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_standard_class_bposition_report handler: {e}")
            return
        
        if event_type == "IO.AISstream.ExtendedClassBPositionReport":
            if self.io_aisstream_mqtt_extended_class_bposition_report_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.ExtendedClassBPositionReport.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.ExtendedClassBPositionReport")
                    await self.io_aisstream_mqtt_extended_class_bposition_report_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_extended_class_bposition_report handler: {e}")
            return
        
        if event_type == "IO.AISstream.AidsToNavigationReport":
            if self.io_aisstream_mqtt_aids_to_navigation_report_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.AidsToNavigationReport.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.AidsToNavigationReport")
                    await self.io_aisstream_mqtt_aids_to_navigation_report_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_aids_to_navigation_report handler: {e}")
            return
        
        if event_type == "IO.AISstream.StaticDataReport":
            if self.io_aisstream_mqtt_static_data_report_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.StaticDataReport.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.StaticDataReport")
                    await self.io_aisstream_mqtt_static_data_report_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_static_data_report handler: {e}")
            return
        
        if event_type == "IO.AISstream.BaseStationReport":
            if self.io_aisstream_mqtt_base_station_report_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.BaseStationReport.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.BaseStationReport")
                    await self.io_aisstream_mqtt_base_station_report_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_base_station_report handler: {e}")
            return
        
        if event_type == "IO.AISstream.SafetyBroadcastMessage":
            if self.io_aisstream_mqtt_safety_broadcast_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.SafetyBroadcastMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.SafetyBroadcastMessage")
                    await self.io_aisstream_mqtt_safety_broadcast_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_safety_broadcast_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.StandardSearchAndRescueAircraftReport":
            if self.io_aisstream_mqtt_standard_search_and_rescue_aircraft_report_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.StandardSearchAndRescueAircraftReport.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport")
                    await self.io_aisstream_mqtt_standard_search_and_rescue_aircraft_report_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_standard_search_and_rescue_aircraft_report handler: {e}")
            return
        
        if event_type == "IO.AISstream.LongRangeAisBroadcastMessage":
            if self.io_aisstream_mqtt_long_range_ais_broadcast_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.LongRangeAisBroadcastMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.LongRangeAisBroadcastMessage")
                    await self.io_aisstream_mqtt_long_range_ais_broadcast_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_long_range_ais_broadcast_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.AddressedSafetyMessage":
            if self.io_aisstream_mqtt_addressed_safety_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.AddressedSafetyMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.AddressedSafetyMessage")
                    await self.io_aisstream_mqtt_addressed_safety_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_addressed_safety_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.AddressedBinaryMessage":
            if self.io_aisstream_mqtt_addressed_binary_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.AddressedBinaryMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.AddressedBinaryMessage")
                    await self.io_aisstream_mqtt_addressed_binary_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_addressed_binary_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.AssignedModeCommand":
            if self.io_aisstream_mqtt_assigned_mode_command_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.AssignedModeCommand.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.AssignedModeCommand")
                    await self.io_aisstream_mqtt_assigned_mode_command_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_assigned_mode_command handler: {e}")
            return
        
        if event_type == "IO.AISstream.BinaryAcknowledge":
            if self.io_aisstream_mqtt_binary_acknowledge_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.BinaryAcknowledge.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.BinaryAcknowledge")
                    await self.io_aisstream_mqtt_binary_acknowledge_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_binary_acknowledge handler: {e}")
            return
        
        if event_type == "IO.AISstream.BinaryBroadcastMessage":
            if self.io_aisstream_mqtt_binary_broadcast_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.BinaryBroadcastMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.BinaryBroadcastMessage")
                    await self.io_aisstream_mqtt_binary_broadcast_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_binary_broadcast_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.ChannelManagement":
            if self.io_aisstream_mqtt_channel_management_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.ChannelManagement.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.ChannelManagement")
                    await self.io_aisstream_mqtt_channel_management_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_channel_management handler: {e}")
            return
        
        if event_type == "IO.AISstream.CoordinatedUTCInquiry":
            if self.io_aisstream_mqtt_coordinated_utcinquiry_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.CoordinatedUTCInquiry.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.CoordinatedUTCInquiry")
                    await self.io_aisstream_mqtt_coordinated_utcinquiry_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_coordinated_utcinquiry handler: {e}")
            return
        
        if event_type == "IO.AISstream.DataLinkManagementMessage":
            if self.io_aisstream_mqtt_data_link_management_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.DataLinkManagementMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.DataLinkManagementMessage")
                    await self.io_aisstream_mqtt_data_link_management_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_data_link_management_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.GnssBroadcastBinaryMessage":
            if self.io_aisstream_mqtt_gnss_broadcast_binary_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.GnssBroadcastBinaryMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.GnssBroadcastBinaryMessage")
                    await self.io_aisstream_mqtt_gnss_broadcast_binary_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_gnss_broadcast_binary_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.GroupAssignmentCommand":
            if self.io_aisstream_mqtt_group_assignment_command_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.GroupAssignmentCommand.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.GroupAssignmentCommand")
                    await self.io_aisstream_mqtt_group_assignment_command_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_group_assignment_command handler: {e}")
            return
        
        if event_type == "IO.AISstream.Interrogation":
            if self.io_aisstream_mqtt_interrogation_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.Interrogation.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.Interrogation")
                    await self.io_aisstream_mqtt_interrogation_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_interrogation handler: {e}")
            return
        
        if event_type == "IO.AISstream.MultiSlotBinaryMessage":
            if self.io_aisstream_mqtt_multi_slot_binary_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.MultiSlotBinaryMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.MultiSlotBinaryMessage")
                    await self.io_aisstream_mqtt_multi_slot_binary_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_multi_slot_binary_message handler: {e}")
            return
        
        if event_type == "IO.AISstream.SingleSlotBinaryMessage":
            if self.io_aisstream_mqtt_single_slot_binary_message_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = aisstream_mqtt_producer_data.SingleSlotBinaryMessage.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "IO.AISstream.mqtt.SingleSlotBinaryMessage")
                    await self.io_aisstream_mqtt_single_slot_binary_message_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in io_aisstream_mqtt_single_slot_binary_message handler: {e}")
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
            topics = get_subscription_topics_io_aisstream_mqtt(self._topic_mappings)
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

    @staticmethod
    def _build_enhanced_auth_properties(token, authentication_method: str = "OAUTH2-JWT", base=None):
        """Build MQTT v5 CONNECT properties carrying an OAuth2/Entra JWT via
        MQTT v5 Enhanced Authentication.

        Azure Event Grid Namespaces (and other Entra-secured MQTT v5 brokers)
        require the bearer token to be presented through the CONNECT
        ``Authentication Method`` / ``Authentication Data`` properties, NOT the
        username/password fields. Username/password silently fails CONNACK and
        ``publish()`` then queues messages locally without ever reaching the
        broker. See
        https://learn.microsoft.com/azure/event-grid/mqtt-client-microsoft-entra-token-and-rbac

        The paho client passed to this class MUST be created with
        ``protocol=mqtt.MQTTv5`` for these properties to be honored.
        """
        if not _MQTT5_AVAILABLE:
            raise RuntimeError(
                "MQTT v5 Enhanced Authentication (OAUTH2-JWT) requires "
                "paho-mqtt >= 2.0; install a newer paho-mqtt to use "
                "token-based auth."
            )
        connect_properties = base if base is not None else _MqttProperties(_MqttPacketTypes.CONNECT)
        connect_properties.AuthenticationMethod = authentication_method
        connect_properties.AuthenticationData = (
            token.encode("utf-8") if isinstance(token, str) else token
        )
        return connect_properties

    async def connect(self, broker: str, port: int = 1883, keepalive: int = 60,
                      token: Optional[str] = None,
                      authentication_method: str = "OAUTH2-JWT",
                      properties: Optional["_MqttProperties"] = None):
        """
        Connect to MQTT broker and wait for authentication to complete.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds
            token: Optional OAuth2/Entra bearer token (JWT). When provided, it is
                presented via MQTT v5 Enhanced Authentication
                (Authentication Method ``OAUTH2-JWT`` + Authentication Data) as
                required by Azure Event Grid Namespaces -- NOT as a password.
                Requires a paho client created with ``protocol=mqtt.MQTTv5``.
            authentication_method: MQTT v5 Authentication Method to advertise
                when ``token`` is supplied (default ``OAUTH2-JWT``).
            properties: Optional MQTT v5 CONNECT ``Properties`` to send. When
                ``token`` is also supplied, the enhanced-auth fields are set on
                these properties.

        Raises:
            ConnectionError: If the broker rejects the connection or disconnects before success
            TimeoutError: If the broker does not acknowledge the connection in time
        """
        if self._connect_waiter is not None and not self._connect_waiter.done():
            raise RuntimeError("MQTT connect already in progress")
        self.loop = asyncio.get_running_loop()
        waiter = self.loop.create_future()
        self._connect_waiter = waiter
        self._connected = False
        loop_started = False
        try:
            connect_properties = properties
            if token is not None:
                connect_properties = self._build_enhanced_auth_properties(
                    token, authentication_method, base=properties
                )
            if connect_properties is not None:
                self.client.connect(broker, port, keepalive, properties=connect_properties)
            else:
                self.client.connect(broker, port, keepalive)
            self.client.loop_start()
            loop_started = True
            timeout = float(keepalive) if keepalive and keepalive > 0 else 60.0
            await asyncio.wait_for(waiter, timeout=timeout)
        except Exception:
            if self._connect_waiter is waiter:
                self._connect_waiter = None
            self._connected = False
            if loop_started:
                await asyncio.to_thread(self.client.loop_stop)
            raise
    
    async def disconnect(self):
        """Disconnect from MQTT broker."""
        self._connected = False
        self.client.loop_stop()
        self.client.disconnect()

    # Producer methods
    
    async def publish_io_aisstream_mqtt_position_report(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.PositionReport,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.PositionReport' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.PositionReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_ship_static_data(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.ShipStaticData,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.ShipStaticData' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/ship-static-data'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/ship-static-data"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.ShipStaticData",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_standard_class_bposition_report(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.StandardClassBPositionReport,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.StandardClassBPositionReport' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-class-b-position-report'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-class-b-position-report"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.StandardClassBPositionReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_extended_class_bposition_report(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.ExtendedClassBPositionReport,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.ExtendedClassBPositionReport' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/extended-class-b-position-report'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/extended-class-b-position-report"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.ExtendedClassBPositionReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_aids_to_navigation_report(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.AidsToNavigationReport,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.AidsToNavigationReport' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aids-to-navigation-report'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aids-to-navigation-report"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.AidsToNavigationReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_static_data_report(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.StaticDataReport,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.StaticDataReport' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static-data-report'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static-data-report"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.StaticDataReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_base_station_report(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.BaseStationReport,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.BaseStationReport' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/base-station-report'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/base-station-report"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.BaseStationReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_safety_broadcast_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.SafetyBroadcastMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.SafetyBroadcastMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/safety-broadcast-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/safety-broadcast-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.SafetyBroadcastMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_standard_search_and_rescue_aircraft_report(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.StandardSearchAndRescueAircraftReport,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-search-and-rescue-aircraft-report'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-search-and-rescue-aircraft-report"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.StandardSearchAndRescueAircraftReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_long_range_ais_broadcast_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.LongRangeAisBroadcastMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.LongRangeAisBroadcastMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/long-range-ais-broadcast-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/long-range-ais-broadcast-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.LongRangeAisBroadcastMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_addressed_safety_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.AddressedSafetyMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.AddressedSafetyMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-safety-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-safety-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.AddressedSafetyMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_addressed_binary_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.AddressedBinaryMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.AddressedBinaryMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-binary-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-binary-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.AddressedBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_assigned_mode_command(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.AssignedModeCommand,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.AssignedModeCommand' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/assigned-mode-command'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/assigned-mode-command"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.AssignedModeCommand",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_binary_acknowledge(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.BinaryAcknowledge,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.BinaryAcknowledge' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-acknowledge'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-acknowledge"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.BinaryAcknowledge",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_binary_broadcast_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.BinaryBroadcastMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.BinaryBroadcastMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-broadcast-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-broadcast-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.BinaryBroadcastMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_channel_management(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.ChannelManagement,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.ChannelManagement' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/channel-management'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/channel-management"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.ChannelManagement",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_coordinated_utcinquiry(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.CoordinatedUTCInquiry,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.CoordinatedUTCInquiry' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/coordinated-utc-inquiry'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/coordinated-utc-inquiry"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.CoordinatedUTCInquiry",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_data_link_management_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.DataLinkManagementMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.DataLinkManagementMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/data-link-management-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/data-link-management-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.DataLinkManagementMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_gnss_broadcast_binary_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.GnssBroadcastBinaryMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.GnssBroadcastBinaryMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/gnss-broadcast-binary-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/gnss-broadcast-binary-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.GnssBroadcastBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_group_assignment_command(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.GroupAssignmentCommand,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.GroupAssignmentCommand' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/group-assignment-command'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/group-assignment-command"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.GroupAssignmentCommand",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_interrogation(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.Interrogation,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.Interrogation' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/interrogation'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/interrogation"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.Interrogation",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_multi_slot_binary_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.MultiSlotBinaryMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.MultiSlotBinaryMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/multi-slot-binary-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/multi-slot-binary-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.MultiSlotBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
    async def publish_io_aisstream_mqtt_single_slot_binary_message(self,
        mmsi: str,
        flag: str,
        ship_type: str,
        geohash5: str,
        data: aisstream_mqtt_producer_data.SingleSlotBinaryMessage,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'IO.AISstream.mqtt.SingleSlotBinaryMessage' event to an MQTT topic.

        Args:
        
            mmsi: URI template variable for 'mmsi'
            flag: URI template variable for 'flag'
            ship_type: URI template variable for 'ship_type'
            geohash5: URI template variable for 'geohash5'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/single-slot-binary-message'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (0).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/single-slot-binary-message"
        _topic_template_values: Dict[str, str] = {
            "mmsi": str(mmsi),
            "flag": str(flag),
            "ship_type": str(ship_type),
            "geohash5": str(geohash5),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"IO.AISstream.SingleSlotBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = mmsi)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
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

    
