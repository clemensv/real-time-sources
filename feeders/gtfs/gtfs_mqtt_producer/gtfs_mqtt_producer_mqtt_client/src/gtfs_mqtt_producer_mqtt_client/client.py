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
import gtfs_mqtt_producer_data
from gtfs_mqtt_producer_data import VehiclePosition
from gtfs_mqtt_producer_data import TripUpdate
from gtfs_mqtt_producer_data import Alert
from gtfs_mqtt_producer_data import Agency
from gtfs_mqtt_producer_data import Areas
from gtfs_mqtt_producer_data import Attributions
from gtfs_mqtt_producer_data import BookingRules
from gtfs_mqtt_producer_data import FareAttributes
from gtfs_mqtt_producer_data import FareLegRules
from gtfs_mqtt_producer_data import FareMedia
from gtfs_mqtt_producer_data import FareProducts
from gtfs_mqtt_producer_data import FareRules
from gtfs_mqtt_producer_data import FareTransferRules
from gtfs_mqtt_producer_data import FeedInfo
from gtfs_mqtt_producer_data import Frequencies
from gtfs_mqtt_producer_data import Levels
from gtfs_mqtt_producer_data import LocationGeoJson
from gtfs_mqtt_producer_data import LocationGroups
from gtfs_mqtt_producer_data import LocationGroupStores
from gtfs_mqtt_producer_data import Networks
from gtfs_mqtt_producer_data import Pathways
from gtfs_mqtt_producer_data import RouteNetworks
from gtfs_mqtt_producer_data import Routes
from gtfs_mqtt_producer_data import Shapes
from gtfs_mqtt_producer_data import StopAreas
from gtfs_mqtt_producer_data import Stops
from gtfs_mqtt_producer_data import StopTimes
from gtfs_mqtt_producer_data import Timeframes
from gtfs_mqtt_producer_data import Transfers
from gtfs_mqtt_producer_data import Translations
from gtfs_mqtt_producer_data import Trips


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



def get_default_topic_mappings_generaltransitfeedrealtime_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the GeneralTransitFeedRealTime.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "GeneralTransitFeedRealTime.Vehicle.VehiclePosition.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/{route_id}/vehicle/{vehicle_id}",
        "GeneralTransitFeedRealTime.Trip.TripUpdate.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/{route_id}/trip-update/{trip_id}",
        "GeneralTransitFeedRealTime.Alert.Alert.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/{route_id}/alert/{alert_id}",
    }


def get_subscription_topics_generaltransitfeedrealtime_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_generaltransitfeedrealtime_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class GeneralTransitFeedRealTimeMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the GeneralTransitFeedRealTime.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_generaltransitfeedrealtime_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        self._connect_waiter: Optional[asyncio.Future[None]] = None
        self._connected = False
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.general_transit_feed_real_time_vehicle_vehicle_position_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.VehiclePosition, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_real_time_trip_trip_update_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.TripUpdate, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_real_time_alert_alert_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Alert, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "GeneralTransitFeedRealTime.Vehicle.VehiclePosition":
            if self.general_transit_feed_real_time_vehicle_vehicle_position_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.VehiclePosition.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedRealTime.Vehicle.VehiclePosition.mqtt")
                    await self.general_transit_feed_real_time_vehicle_vehicle_position_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_real_time_vehicle_vehicle_position_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedRealTime.Trip.TripUpdate":
            if self.general_transit_feed_real_time_trip_trip_update_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.TripUpdate.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedRealTime.Trip.TripUpdate.mqtt")
                    await self.general_transit_feed_real_time_trip_trip_update_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_real_time_trip_trip_update_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedRealTime.Alert.Alert":
            if self.general_transit_feed_real_time_alert_alert_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Alert.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedRealTime.Alert.Alert.mqtt")
                    await self.general_transit_feed_real_time_alert_alert_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_real_time_alert_alert_mqtt handler: {e}")
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
            topics = get_subscription_topics_generaltransitfeedrealtime_mqtt(self._topic_mappings)
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
        Connect to MQTT broker and wait for authentication to complete.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds

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
    
    async def publish_general_transit_feed_real_time_vehicle_vehicle_position_mqtt(self,
        feedurl: str,
        agencyid: str,
        route_id: str,
        vehicle_id: str,
        data: gtfs_mqtt_producer_data.VehiclePosition,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedRealTime.Vehicle.VehiclePosition.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            route_id: URI template variable for 'route_id'
            vehicle_id: URI template variable for 'vehicle_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/{route_id}/vehicle/{vehicle_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/{route_id}/vehicle/{vehicle_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "route_id": str(route_id),
            "vehicle_id": str(vehicle_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedRealTime.Vehicle.VehiclePosition",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_real_time_trip_trip_update_mqtt(self,
        feedurl: str,
        agencyid: str,
        route_id: str,
        trip_id: str,
        data: gtfs_mqtt_producer_data.TripUpdate,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedRealTime.Trip.TripUpdate.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            route_id: URI template variable for 'route_id'
            trip_id: URI template variable for 'trip_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/{route_id}/trip-update/{trip_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/{route_id}/trip-update/{trip_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "route_id": str(route_id),
            "trip_id": str(trip_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedRealTime.Trip.TripUpdate",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_real_time_alert_alert_mqtt(self,
        feedurl: str,
        agencyid: str,
        route_id: str,
        alert_id: str,
        data: gtfs_mqtt_producer_data.Alert,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedRealTime.Alert.Alert.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            route_id: URI template variable for 'route_id'
            alert_id: URI template variable for 'alert_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/{route_id}/alert/{alert_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (False).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/{route_id}/alert/{alert_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "route_id": str(route_id),
            "alert_id": str(alert_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedRealTime.Alert.Alert",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    


def get_default_topic_mappings_generaltransitfeedstatic_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the GeneralTransitFeedStatic.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "GeneralTransitFeedStatic.Agency.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/agency/{row_id}",
        "GeneralTransitFeedStatic.Areas.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/areas/{row_id}",
        "GeneralTransitFeedStatic.Attributions.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/attributions/{row_id}",
        "GeneralTransitFeed.BookingRules.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/booking-rules/{row_id}",
        "GeneralTransitFeedStatic.FareAttributes.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/fare-attributes/{row_id}",
        "GeneralTransitFeedStatic.FareLegRules.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/fare-leg-rules/{row_id}",
        "GeneralTransitFeedStatic.FareMedia.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/fare-media/{row_id}",
        "GeneralTransitFeedStatic.FareProducts.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/fare-products/{row_id}",
        "GeneralTransitFeedStatic.FareRules.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/fare-rules/{row_id}",
        "GeneralTransitFeedStatic.FareTransferRules.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/fare-transfer-rules/{row_id}",
        "GeneralTransitFeedStatic.FeedInfo.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/feed-info/{row_id}",
        "GeneralTransitFeedStatic.Frequencies.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/frequencies/{row_id}",
        "GeneralTransitFeedStatic.Levels.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/levels/{row_id}",
        "GeneralTransitFeedStatic.LocationGeoJson.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/location-geo-json/{row_id}",
        "GeneralTransitFeedStatic.LocationGroups.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/location-groups/{row_id}",
        "GeneralTransitFeedStatic.LocationGroupStores.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/location-group-stores/{row_id}",
        "GeneralTransitFeedStatic.Networks.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/networks/{row_id}",
        "GeneralTransitFeedStatic.Pathways.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/pathways/{row_id}",
        "GeneralTransitFeedStatic.RouteNetworks.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/route-networks/{row_id}",
        "GeneralTransitFeedStatic.Routes.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/routes/{row_id}",
        "GeneralTransitFeedStatic.Shapes.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/shapes/{row_id}",
        "GeneralTransitFeedStatic.StopAreas.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/stop-areas/{row_id}",
        "GeneralTransitFeedStatic.Stops.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/stops/{row_id}",
        "GeneralTransitFeedStatic.StopTimes.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/stop-times/{row_id}",
        "GeneralTransitFeedStatic.Timeframes.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/timeframes/{row_id}",
        "GeneralTransitFeedStatic.Transfers.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/transfers/{row_id}",
        "GeneralTransitFeedStatic.Translations.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/translations/{row_id}",
        "GeneralTransitFeedStatic.Trips.mqtt": "transit/intl/gtfs/gtfs/{agencyid}/static/trips/{row_id}",
    }


def get_subscription_topics_generaltransitfeedstatic_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_generaltransitfeedstatic_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class GeneralTransitFeedStaticMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the GeneralTransitFeedStatic.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_generaltransitfeedstatic_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        self._connect_waiter: Optional[asyncio.Future[None]] = None
        self._connected = False
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.general_transit_feed_static_agency_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Agency, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_areas_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Areas, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_attributions_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Attributions, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_booking_rules_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.BookingRules, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_fare_attributes_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.FareAttributes, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_fare_leg_rules_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.FareLegRules, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_fare_media_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.FareMedia, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_fare_products_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.FareProducts, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_fare_rules_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.FareRules, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_fare_transfer_rules_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.FareTransferRules, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_feed_info_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.FeedInfo, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_frequencies_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Frequencies, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_levels_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Levels, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_location_geo_json_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.LocationGeoJson, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_location_groups_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.LocationGroups, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_location_group_stores_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.LocationGroupStores, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_networks_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Networks, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_pathways_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Pathways, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_route_networks_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.RouteNetworks, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_routes_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Routes, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_shapes_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Shapes, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_stop_areas_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.StopAreas, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_stops_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Stops, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_stop_times_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.StopTimes, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_timeframes_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Timeframes, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_transfers_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Transfers, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_translations_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Translations, Dict[str, str]], Awaitable[None]]] = None
        
        self.general_transit_feed_static_trips_mqtt_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, gtfs_mqtt_producer_data.Trips, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "GeneralTransitFeedStatic.Agency":
            if self.general_transit_feed_static_agency_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Agency.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Agency.mqtt")
                    await self.general_transit_feed_static_agency_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_agency_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Areas":
            if self.general_transit_feed_static_areas_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Areas.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Areas.mqtt")
                    await self.general_transit_feed_static_areas_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_areas_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Attributions":
            if self.general_transit_feed_static_attributions_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Attributions.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Attributions.mqtt")
                    await self.general_transit_feed_static_attributions_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_attributions_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeed.BookingRules":
            if self.general_transit_feed_booking_rules_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.BookingRules.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeed.BookingRules.mqtt")
                    await self.general_transit_feed_booking_rules_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_booking_rules_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.FareAttributes":
            if self.general_transit_feed_static_fare_attributes_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.FareAttributes.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.FareAttributes.mqtt")
                    await self.general_transit_feed_static_fare_attributes_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_fare_attributes_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.FareLegRules":
            if self.general_transit_feed_static_fare_leg_rules_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.FareLegRules.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.FareLegRules.mqtt")
                    await self.general_transit_feed_static_fare_leg_rules_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_fare_leg_rules_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.FareMedia":
            if self.general_transit_feed_static_fare_media_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.FareMedia.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.FareMedia.mqtt")
                    await self.general_transit_feed_static_fare_media_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_fare_media_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.FareProducts":
            if self.general_transit_feed_static_fare_products_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.FareProducts.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.FareProducts.mqtt")
                    await self.general_transit_feed_static_fare_products_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_fare_products_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.FareRules":
            if self.general_transit_feed_static_fare_rules_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.FareRules.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.FareRules.mqtt")
                    await self.general_transit_feed_static_fare_rules_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_fare_rules_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.FareTransferRules":
            if self.general_transit_feed_static_fare_transfer_rules_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.FareTransferRules.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.FareTransferRules.mqtt")
                    await self.general_transit_feed_static_fare_transfer_rules_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_fare_transfer_rules_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.FeedInfo":
            if self.general_transit_feed_static_feed_info_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.FeedInfo.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.FeedInfo.mqtt")
                    await self.general_transit_feed_static_feed_info_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_feed_info_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Frequencies":
            if self.general_transit_feed_static_frequencies_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Frequencies.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Frequencies.mqtt")
                    await self.general_transit_feed_static_frequencies_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_frequencies_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Levels":
            if self.general_transit_feed_static_levels_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Levels.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Levels.mqtt")
                    await self.general_transit_feed_static_levels_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_levels_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.LocationGeoJson":
            if self.general_transit_feed_static_location_geo_json_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.LocationGeoJson.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.LocationGeoJson.mqtt")
                    await self.general_transit_feed_static_location_geo_json_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_location_geo_json_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.LocationGroups":
            if self.general_transit_feed_static_location_groups_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.LocationGroups.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.LocationGroups.mqtt")
                    await self.general_transit_feed_static_location_groups_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_location_groups_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.LocationGroupStores":
            if self.general_transit_feed_static_location_group_stores_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.LocationGroupStores.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.LocationGroupStores.mqtt")
                    await self.general_transit_feed_static_location_group_stores_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_location_group_stores_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Networks":
            if self.general_transit_feed_static_networks_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Networks.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Networks.mqtt")
                    await self.general_transit_feed_static_networks_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_networks_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Pathways":
            if self.general_transit_feed_static_pathways_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Pathways.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Pathways.mqtt")
                    await self.general_transit_feed_static_pathways_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_pathways_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.RouteNetworks":
            if self.general_transit_feed_static_route_networks_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.RouteNetworks.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.RouteNetworks.mqtt")
                    await self.general_transit_feed_static_route_networks_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_route_networks_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Routes":
            if self.general_transit_feed_static_routes_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Routes.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Routes.mqtt")
                    await self.general_transit_feed_static_routes_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_routes_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Shapes":
            if self.general_transit_feed_static_shapes_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Shapes.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Shapes.mqtt")
                    await self.general_transit_feed_static_shapes_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_shapes_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.StopAreas":
            if self.general_transit_feed_static_stop_areas_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.StopAreas.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.StopAreas.mqtt")
                    await self.general_transit_feed_static_stop_areas_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_stop_areas_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Stops":
            if self.general_transit_feed_static_stops_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Stops.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Stops.mqtt")
                    await self.general_transit_feed_static_stops_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_stops_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.StopTimes":
            if self.general_transit_feed_static_stop_times_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.StopTimes.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.StopTimes.mqtt")
                    await self.general_transit_feed_static_stop_times_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_stop_times_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Timeframes":
            if self.general_transit_feed_static_timeframes_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Timeframes.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Timeframes.mqtt")
                    await self.general_transit_feed_static_timeframes_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_timeframes_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Transfers":
            if self.general_transit_feed_static_transfers_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Transfers.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Transfers.mqtt")
                    await self.general_transit_feed_static_transfers_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_transfers_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Translations":
            if self.general_transit_feed_static_translations_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Translations.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Translations.mqtt")
                    await self.general_transit_feed_static_translations_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_translations_mqtt handler: {e}")
            return
        
        if event_type == "GeneralTransitFeedStatic.Trips":
            if self.general_transit_feed_static_trips_mqtt_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = gtfs_mqtt_producer_data.Trips.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "GeneralTransitFeedStatic.Trips.mqtt")
                    await self.general_transit_feed_static_trips_mqtt_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in general_transit_feed_static_trips_mqtt handler: {e}")
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
            topics = get_subscription_topics_generaltransitfeedstatic_mqtt(self._topic_mappings)
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
        Connect to MQTT broker and wait for authentication to complete.

        Args:
            broker: Broker hostname or IP
            port: Broker port
            keepalive: Keepalive interval in seconds

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
    
    async def publish_general_transit_feed_static_agency_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Agency,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Agency.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/agency/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/agency/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Agency",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_areas_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Areas,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Areas.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/areas/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/areas/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Areas",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_attributions_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Attributions,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Attributions.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/attributions/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/attributions/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Attributions",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_booking_rules_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.BookingRules,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeed.BookingRules.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/booking-rules/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/booking-rules/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.BookingRules",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_fare_attributes_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.FareAttributes,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.FareAttributes.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/fare-attributes/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/fare-attributes/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.FareAttributes",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_fare_leg_rules_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.FareLegRules,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.FareLegRules.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/fare-leg-rules/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/fare-leg-rules/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.FareLegRules",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_fare_media_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.FareMedia,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.FareMedia.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/fare-media/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/fare-media/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.FareMedia",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_fare_products_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.FareProducts,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.FareProducts.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/fare-products/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/fare-products/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.FareProducts",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_fare_rules_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.FareRules,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.FareRules.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/fare-rules/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/fare-rules/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.FareRules",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_fare_transfer_rules_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.FareTransferRules,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.FareTransferRules.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/fare-transfer-rules/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/fare-transfer-rules/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.FareTransferRules",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_feed_info_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.FeedInfo,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.FeedInfo.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/feed-info/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/feed-info/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.FeedInfo",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_frequencies_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Frequencies,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Frequencies.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/frequencies/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/frequencies/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Frequencies",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_levels_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Levels,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Levels.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/levels/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/levels/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Levels",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_location_geo_json_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.LocationGeoJson,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.LocationGeoJson.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/location-geo-json/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/location-geo-json/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.LocationGeoJson",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_location_groups_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.LocationGroups,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.LocationGroups.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/location-groups/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/location-groups/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.LocationGroups",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_location_group_stores_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.LocationGroupStores,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.LocationGroupStores.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/location-group-stores/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/location-group-stores/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.LocationGroupStores",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_networks_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Networks,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Networks.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/networks/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/networks/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Networks",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_pathways_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Pathways,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Pathways.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/pathways/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/pathways/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Pathways",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_route_networks_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.RouteNetworks,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.RouteNetworks.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/route-networks/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/route-networks/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.RouteNetworks",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_routes_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Routes,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Routes.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/routes/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/routes/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Routes",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_shapes_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Shapes,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Shapes.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/shapes/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/shapes/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Shapes",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_stop_areas_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.StopAreas,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.StopAreas.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/stop-areas/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/stop-areas/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.StopAreas",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_stops_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Stops,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Stops.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/stops/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/stops/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Stops",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_stop_times_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.StopTimes,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.StopTimes.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/stop-times/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/stop-times/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.StopTimes",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_timeframes_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Timeframes,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Timeframes.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/timeframes/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/timeframes/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Timeframes",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_transfers_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Transfers,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Transfers.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/transfers/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/transfers/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Transfers",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_translations_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Translations,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Translations.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/translations/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/translations/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Translations",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
    async def publish_general_transit_feed_static_trips_mqtt(self,
        feedurl: str,
        agencyid: str,
        row_id: str,
        data: gtfs_mqtt_producer_data.Trips,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'GeneralTransitFeedStatic.Trips.mqtt' event to an MQTT topic.

        Args:
        
            feedurl: URI template variable for 'feedurl'
            agencyid: URI template variable for 'agencyid'
            row_id: URI template variable for 'row_id'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'transit/intl/gtfs/gtfs/{agencyid}/static/trips/{row_id}'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "transit/intl/gtfs/gtfs/{agencyid}/static/trips/{row_id}"
        _topic_template_values: Dict[str, str] = {
            "feedurl": str(feedurl),
            "agencyid": str(agencyid),
            "row_id": str(row_id),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeedStatic.Trips",
             "source":"{feedurl}".format(feedurl = feedurl),
             "subject":"{agencyid}".format(agencyid = agencyid)
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

    
