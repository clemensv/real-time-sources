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
import noaa_mqtt_producer_data
from noaa_mqtt_producer_data import WaterLevel
from noaa_mqtt_producer_data import Predictions
from noaa_mqtt_producer_data import AirPressure
from noaa_mqtt_producer_data import AirTemperature
from noaa_mqtt_producer_data import WaterTemperature
from noaa_mqtt_producer_data import Wind
from noaa_mqtt_producer_data import Humidity
from noaa_mqtt_producer_data import Conductivity
from noaa_mqtt_producer_data import Salinity
from noaa_mqtt_producer_data import Station
from noaa_mqtt_producer_data import Visibility
from noaa_mqtt_producer_data import Currents
from noaa_mqtt_producer_data import CurrentPredictions


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



def get_default_topic_mappings_microsoft_opendata_us_noaa_mqtt() -> Dict[str, str]:
    """
    Get the default topic mappings for the Microsoft.OpenData.US.NOAA.mqtt message group.
    
    Returns:
        Dictionary mapping message identifiers to their default topic patterns.
    """
    return {
        "Microsoft.OpenData.US.NOAA.mqtt.WaterLevel": "maritime/us/noaa/noaa/{region}/{station_id}/water-level",
        "Microsoft.OpenData.US.NOAA.mqtt.Predictions": "maritime/us/noaa/noaa/{region}/{station_id}/predictions",
        "Microsoft.OpenData.US.NOAA.mqtt.AirPressure": "maritime/us/noaa/noaa/{region}/{station_id}/air-pressure",
        "Microsoft.OpenData.US.NOAA.mqtt.AirTemperature": "maritime/us/noaa/noaa/{region}/{station_id}/air-temperature",
        "Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature": "maritime/us/noaa/noaa/{region}/{station_id}/water-temperature",
        "Microsoft.OpenData.US.NOAA.mqtt.Wind": "maritime/us/noaa/noaa/{region}/{station_id}/wind",
        "Microsoft.OpenData.US.NOAA.mqtt.Humidity": "maritime/us/noaa/noaa/{region}/{station_id}/humidity",
        "Microsoft.OpenData.US.NOAA.mqtt.Conductivity": "maritime/us/noaa/noaa/{region}/{station_id}/conductivity",
        "Microsoft.OpenData.US.NOAA.mqtt.Salinity": "maritime/us/noaa/noaa/{region}/{station_id}/salinity",
        "Microsoft.OpenData.US.NOAA.mqtt.Station": "maritime/us/noaa/noaa/{region}/{station_id}/info",
        "Microsoft.OpenData.US.NOAA.mqtt.Visibility": "maritime/us/noaa/noaa/{region}/{station_id}/visibility",
        "Microsoft.OpenData.US.NOAA.mqtt.Currents": "maritime/us/noaa/noaa/{region}/{station_id}/currents",
        "Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions": "maritime/us/noaa/noaa/{region}/{station_id}/current-predictions",
    }


def get_subscription_topics_microsoft_opendata_us_noaa_mqtt(topic_mappings: Optional[Dict[str, str]] = None) -> List[str]:
    """
    Get subscription topics with URI template placeholders replaced by MQTT wildcards (+).
    
    Args:
        topic_mappings: Optional topic mappings. If None, uses default mappings.
        
    Returns:
        List of topic patterns suitable for MQTT subscription.
    """
    mappings = topic_mappings or get_default_topic_mappings_microsoft_opendata_us_noaa_mqtt()
    topics = []
    for topic in mappings.values():
        wildcard_topic = _topic_to_mqtt_wildcard(topic)
        if wildcard_topic not in topics:
            topics.append(wildcard_topic)
    return topics


class MicrosoftOpenDataUSNOAAMqttMqttClient(_ClientBase):
    """MQTT Client for producing and consuming messages in the Microsoft.OpenData.US.NOAA.mqtt message group."""
    
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
        self._topic_mappings = topic_mappings or get_default_topic_mappings_microsoft_opendata_us_noaa_mqtt()
        self._topic_patterns = {k: _build_topic_regex(v) for k, v in self._topic_mappings.items()}
        self._connect_waiter: Optional[asyncio.Future[None]] = None
        self._connected = False
        
        # Message handler callbacks (Dispatcher pattern)
        
        self.microsoft_open_data_us_noaa_mqtt_water_level_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.WaterLevel, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_predictions_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Predictions, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_air_pressure_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.AirPressure, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_air_temperature_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.AirTemperature, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_water_temperature_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.WaterTemperature, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_wind_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Wind, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_humidity_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Humidity, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_conductivity_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Conductivity, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_salinity_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Salinity, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_station_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Station, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_visibility_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Visibility, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_currents_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.Currents, Dict[str, str]], Awaitable[None]]] = None
        
        self.microsoft_open_data_us_noaa_mqtt_current_predictions_async: Optional[Callable[[mqtt.MQTTMessage, CloudEvent, noaa_mqtt_producer_data.CurrentPredictions, Dict[str, str]], Awaitable[None]]] = None
        
        
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
        
        
        if event_type == "Microsoft.OpenData.US.NOAA.WaterLevel":
            if self.microsoft_open_data_us_noaa_mqtt_water_level_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.WaterLevel.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.WaterLevel")
                    await self.microsoft_open_data_us_noaa_mqtt_water_level_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_water_level handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Predictions":
            if self.microsoft_open_data_us_noaa_mqtt_predictions_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Predictions.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Predictions")
                    await self.microsoft_open_data_us_noaa_mqtt_predictions_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_predictions handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.AirPressure":
            if self.microsoft_open_data_us_noaa_mqtt_air_pressure_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.AirPressure.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.AirPressure")
                    await self.microsoft_open_data_us_noaa_mqtt_air_pressure_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_air_pressure handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.AirTemperature":
            if self.microsoft_open_data_us_noaa_mqtt_air_temperature_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.AirTemperature.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.AirTemperature")
                    await self.microsoft_open_data_us_noaa_mqtt_air_temperature_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_air_temperature handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.WaterTemperature":
            if self.microsoft_open_data_us_noaa_mqtt_water_temperature_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.WaterTemperature.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature")
                    await self.microsoft_open_data_us_noaa_mqtt_water_temperature_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_water_temperature handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Wind":
            if self.microsoft_open_data_us_noaa_mqtt_wind_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Wind.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Wind")
                    await self.microsoft_open_data_us_noaa_mqtt_wind_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_wind handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Humidity":
            if self.microsoft_open_data_us_noaa_mqtt_humidity_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Humidity.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Humidity")
                    await self.microsoft_open_data_us_noaa_mqtt_humidity_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_humidity handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Conductivity":
            if self.microsoft_open_data_us_noaa_mqtt_conductivity_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Conductivity.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Conductivity")
                    await self.microsoft_open_data_us_noaa_mqtt_conductivity_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_conductivity handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Salinity":
            if self.microsoft_open_data_us_noaa_mqtt_salinity_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Salinity.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Salinity")
                    await self.microsoft_open_data_us_noaa_mqtt_salinity_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_salinity handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Station":
            if self.microsoft_open_data_us_noaa_mqtt_station_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Station.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Station")
                    await self.microsoft_open_data_us_noaa_mqtt_station_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_station handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Visibility":
            if self.microsoft_open_data_us_noaa_mqtt_visibility_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Visibility.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Visibility")
                    await self.microsoft_open_data_us_noaa_mqtt_visibility_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_visibility handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.Currents":
            if self.microsoft_open_data_us_noaa_mqtt_currents_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.Currents.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.Currents")
                    await self.microsoft_open_data_us_noaa_mqtt_currents_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_currents handler: {e}")
            return
        
        if event_type == "Microsoft.OpenData.US.NOAA.CurrentPredictions":
            if self.microsoft_open_data_us_noaa_mqtt_current_predictions_async:
                try:
                    content_type = cloud_event.get_attributes().get('datacontenttype', 'application/json')
                    # CloudEvent.data is now a dict or string, not bytes
                    data = noaa_mqtt_producer_data.CurrentPredictions.from_data(cloud_event.data, content_type)
                    topic_params = self._extract_topic_params(mqtt_message.topic, "Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions")
                    await self.microsoft_open_data_us_noaa_mqtt_current_predictions_async(mqtt_message, cloud_event, data, topic_params)
                except Exception as e:
                    print(f"Error in microsoft_open_data_us_noaa_mqtt_current_predictions handler: {e}")
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
            topics = get_subscription_topics_microsoft_opendata_us_noaa_mqtt(self._topic_mappings)
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
    
    async def publish_microsoft_open_data_us_noaa_mqtt_water_level(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.WaterLevel,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.WaterLevel' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/water-level'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/water-level"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterLevel",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_predictions(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Predictions,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Predictions' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/predictions'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/predictions"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Predictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_air_pressure(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.AirPressure,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.AirPressure' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/air-pressure'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/air-pressure"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirPressure",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_air_temperature(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.AirTemperature,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.AirTemperature' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/air-temperature'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/air-temperature"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_water_temperature(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.WaterTemperature,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/water-temperature'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/water-temperature"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_wind(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Wind,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Wind' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/wind'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/wind"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Wind",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_humidity(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Humidity,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Humidity' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/humidity'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/humidity"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Humidity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_conductivity(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Conductivity,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Conductivity' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/conductivity'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/conductivity"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Conductivity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_salinity(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Salinity,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Salinity' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/salinity'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/salinity"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Salinity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_station(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Station,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Station' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/info'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/info"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Station",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_visibility(self,_datacontenttype: str,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Visibility,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Visibility' event to an MQTT topic.

        Args:
        _datacontenttype: CloudEvents attribute 'datacontenttype'
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/visibility'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/visibility"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Visibility",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "datacontenttype":_datacontenttype,
             "subject":"{station_id}".format(station_id = station_id),
             "time":None,
             "dataschema":_dataschema
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_currents(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.Currents,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.Currents' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/currents'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/currents"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Currents",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
    async def publish_microsoft_open_data_us_noaa_mqtt_current_predictions(self,
        station_id: str,
        region: str,
        data: noaa_mqtt_producer_data.CurrentPredictions,
        topic: Optional[str] = None,
        qos: Optional[int] = None,
        retain: Optional[bool] = None,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = "application/json") -> None:
        """
        Publish the 'Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions' event to an MQTT topic.

        Args:
        
            station_id: URI template variable for 'station_id'
            region: URI template variable for 'region'
            data: The event data to be published.
            topic: Optional topic override. If not provided, uses default topic 'maritime/us/noaa/noaa/{region}/{station_id}/current-predictions'
                with URI template placeholders substituted from the keyword arguments.
            qos: Optional MQTT QoS override. If not provided, uses the message default (1).
            retain: Optional MQTT retain flag override. If not provided, uses the message default (True).
            _time: Optional CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type: The content type for the event data.
        """
        target_topic = topic if topic is not None else "maritime/us/noaa/noaa/{region}/{station_id}/current-predictions"
        _topic_template_values: Dict[str, str] = {
            "station_id": str(station_id),
            "region": str(region),
        }
        if _topic_template_values:
            target_topic = _apply_topic_template(target_topic, _topic_template_values)

        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.CurrentPredictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = station_id)
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

    
