

# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines

"""
Producer module for sending messages via AMQP 1.0 protocol.
"""

import sys
import typing
import uuid
import json
import re
import threading
import queue
import concurrent.futures
from datetime import datetime, timezone
from urllib.parse import quote_plus
from proton import Message, symbol
from proton.reactor import AtMostOnce
from proton.utils import BlockingConnection
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary, to_structured

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
from environment_canada_amqp_producer_data import Station
from environment_canada_amqp_producer_data import WeatherObservation

class CAGovECCCWeatherProducer:
    """
    Producer class to send messages in the `CA.Gov.ECCC.Weather` message group via AMQP 1.0 protocol.
    """
    
    def __init__(self, 
                 host: str,
                 address: str,
                 port: int = 5672,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 content_mode: typing.Literal['structured', 'binary'] = 'structured',
                 format_type: str = 'application/json',
                 ):
        """
        Initialize the AMQP producer
        
        Args:
            host (str): The AMQP broker hostname
            address (str): The AMQP address (queue or topic)
            port (int): The AMQP broker port (default: 5672)
            username (typing.Optional[str]): Optional username for SASL PLAIN authentication
            password (typing.Optional[str]): Optional password for SASL PLAIN authentication
            content_mode (typing.Literal['structured', 'binary']): CloudEvents content mode (default: 'structured')
            format_type (str): Content type format for structured mode (default: 'application/json')
        """
        self.host = host
        self.port = port
        self.address = address
        self.username = username
        self.password = password
        self.content_mode = content_mode
        self.format_type = format_type
        self._init_blocking_sender()

    def _init_blocking_sender(self) -> None:
        connection_url = self._build_connection_url()
        connection_timeout = 120 if self.username and self.password else 30
        # Artemis-class brokers can stall unsettled BlockingSender sends on
        # SASL PLAIN links; a pre-settled sender avoids the timeout loop.
        sender_options = AtMostOnce() if self.username and self.password else None
        self._blocking_sender_is_presettled = sender_options is not None
        self._connection = BlockingConnection(connection_url, timeout=connection_timeout)
        self._sender = self._connection.create_sender(self.address, options=sender_options)

    def _send_via_blocking_sender(self, amqp_msg: Message, timeout: float = 30.0) -> None:
        self._sender.send(amqp_msg, timeout=timeout)
        if self._blocking_sender_is_presettled:
            # BlockingSender.send() returns immediately for pre-settled
            # deliveries, so wait until Proton has drained the link queue
            # and flushed all pending bytes.
            self._connection.wait(
                lambda: (
                    self._sender.link.queued == 0 and
                    self._connection.conn.transport is not None and
                    self._connection.conn.transport.pending() == 0
                ),
                msg=f"Flushing sender {self._sender.link.name} transport",
                timeout=timeout,
            )
    
    def _build_connection_url(self) -> str:
        if self.username and self.password:
            user = quote_plus(self.username)
            pwd = quote_plus(self.password)
            return f"amqp://{user}:{pwd}@{self.host}:{self.port}"
        return f"amqp://{self.host}:{self.port}"

    def _serialize_payload(self, data: typing.Any, content_type: str) -> bytes:
        if data is None:
            return b''
        if hasattr(data, 'to_byte_array'):
            payload = data.to_byte_array(content_type)
        elif hasattr(data, 'to_dict'):
            payload = json.dumps(data.to_dict())
        elif isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            payload = json.dumps(data)
        # to_byte_array may return str for text content types (e.g. JSON);
        # we always emit bytes so the AMQP body is a binary section rather
        # than an AMQP string section containing escaped JSON.
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    @staticmethod
    def _coerce_amqp_timestamp(value: typing.Any) -> typing.Optional[int]:
        if value is None:
            return None
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return int(value.timestamp() * 1000)
        if isinstance(value, (int, float)):
            return int(value)
        text = str(value)
        normalized = text[:-1] + '+00:00' if text.endswith('Z') else text
        try:
            return int(datetime.fromisoformat(normalized).timestamp() * 1000)
        except ValueError:
            return None

    @staticmethod
    def _ce_headers_to_amqp_properties(headers: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """Translate cloudevents-sdk HTTP-style headers (``ce-foo``) into the
        CloudEvents AMQP 1.0 Protocol Binding (v1.0.2 §3.1) form
        (``cloudEvents:foo``). ``content-type`` is carried separately on the
        AMQP properties section and is therefore dropped here.
        """
        out: typing.Dict[str, typing.Any] = {}
        for k, v in (headers or {}).items():
            if v is None:
                continue
            lk = str(k)
            low = lk.lower()
            if low.startswith('ce-'):
                out['cloudEvents:' + lk[3:]] = v
            elif low == 'content-type':
                continue
            else:
                out[lk] = v
        return out

    
    
    def send_station(self,
        data: Station,
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send the `CA.Gov.ECCC.Weather.Station` message
        A reference record published by Environment and Climate Change Canada (ECCC). It lets consumers label, group, and route the live measurement or forecast events.
        
        Args:
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            data (Station): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "CA.Gov.ECCC.Weather.Station",
            "source":
            "https://api.weather.gc.ca",
            "subject":
            "{msc_id}".format(msc_id=_msc_id),
        }
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        amqp_creation_time = self._coerce_amqp_timestamp(attributes.get('time'))
        if amqp_creation_time is not None:
            amqp_msg.creation_time = amqp_creation_time

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)

        annotations = {}
        if annotations:
            if amqp_msg.annotations is None:
                amqp_msg.annotations = {}
            amqp_msg.annotations.update(annotations)
        
        # Send message
        self._send_via_blocking_sender(amqp_msg)
    
    def send_station_batch(self,
        data_array: typing.List[Station],
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `CA.Gov.ECCC.Weather.Station` messages
        
        Args:
            data_array (typing.List[Station]): Array of message data objects
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_station(
                data=data,
                _msc_id=_msc_id,
                _time=_time,
                content_type=content_type)
    
    
    def send_weather_observation(self,
        data: WeatherObservation,
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send the `CA.Gov.ECCC.Weather.WeatherObservation` message
        A current environmental measurement from Environment and Climate Change Canada (ECCC). It carries current weather observations when the upstream feed reports a new or refreshed value.
        
        Args:
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            data (WeatherObservation): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "CA.Gov.ECCC.Weather.WeatherObservation",
            "source":
            "https://api.weather.gc.ca",
            "subject":
            "{msc_id}".format(msc_id=_msc_id),
        }
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        amqp_creation_time = self._coerce_amqp_timestamp(attributes.get('time'))
        if amqp_creation_time is not None:
            amqp_msg.creation_time = amqp_creation_time

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)

        annotations = {}
        if annotations:
            if amqp_msg.annotations is None:
                amqp_msg.annotations = {}
            amqp_msg.annotations.update(annotations)
        
        # Send message
        self._send_via_blocking_sender(amqp_msg)
    
    def send_weather_observation_batch(self,
        data_array: typing.List[WeatherObservation],
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `CA.Gov.ECCC.Weather.WeatherObservation` messages
        
        Args:
            data_array (typing.List[WeatherObservation]): Array of message data objects
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_weather_observation(
                data=data,
                _msc_id=_msc_id,
                _time=_time,
                content_type=content_type)
    
    
    def close(self) -> None:
        """
        Close the producer and clean up resources
        """
        if hasattr(self, '_sender') and self._sender:
            try:
                self._sender.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._sender = None
        if hasattr(self, '_connection') and self._connection:
            try:
                self._connection.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._connection = None



class CAGovECCCWeatherMqttProducer:
    """
    Producer class to send messages in the `CA.Gov.ECCC.Weather.mqtt` message group via AMQP 1.0 protocol.
    """
    
    def __init__(self, 
                 host: str,
                 address: str,
                 port: int = 5672,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 content_mode: typing.Literal['structured', 'binary'] = 'structured',
                 format_type: str = 'application/json',
                 ):
        """
        Initialize the AMQP producer
        
        Args:
            host (str): The AMQP broker hostname
            address (str): The AMQP address (queue or topic)
            port (int): The AMQP broker port (default: 5672)
            username (typing.Optional[str]): Optional username for SASL PLAIN authentication
            password (typing.Optional[str]): Optional password for SASL PLAIN authentication
            content_mode (typing.Literal['structured', 'binary']): CloudEvents content mode (default: 'structured')
            format_type (str): Content type format for structured mode (default: 'application/json')
        """
        self.host = host
        self.port = port
        self.address = address
        self.username = username
        self.password = password
        self.content_mode = content_mode
        self.format_type = format_type
        self._init_blocking_sender()

    def _init_blocking_sender(self) -> None:
        connection_url = self._build_connection_url()
        connection_timeout = 120 if self.username and self.password else 30
        # Artemis-class brokers can stall unsettled BlockingSender sends on
        # SASL PLAIN links; a pre-settled sender avoids the timeout loop.
        sender_options = AtMostOnce() if self.username and self.password else None
        self._blocking_sender_is_presettled = sender_options is not None
        self._connection = BlockingConnection(connection_url, timeout=connection_timeout)
        self._sender = self._connection.create_sender(self.address, options=sender_options)

    def _send_via_blocking_sender(self, amqp_msg: Message, timeout: float = 30.0) -> None:
        self._sender.send(amqp_msg, timeout=timeout)
        if self._blocking_sender_is_presettled:
            # BlockingSender.send() returns immediately for pre-settled
            # deliveries, so wait until Proton has drained the link queue
            # and flushed all pending bytes.
            self._connection.wait(
                lambda: (
                    self._sender.link.queued == 0 and
                    self._connection.conn.transport is not None and
                    self._connection.conn.transport.pending() == 0
                ),
                msg=f"Flushing sender {self._sender.link.name} transport",
                timeout=timeout,
            )
    
    def _build_connection_url(self) -> str:
        if self.username and self.password:
            user = quote_plus(self.username)
            pwd = quote_plus(self.password)
            return f"amqp://{user}:{pwd}@{self.host}:{self.port}"
        return f"amqp://{self.host}:{self.port}"

    def _serialize_payload(self, data: typing.Any, content_type: str) -> bytes:
        if data is None:
            return b''
        if hasattr(data, 'to_byte_array'):
            payload = data.to_byte_array(content_type)
        elif hasattr(data, 'to_dict'):
            payload = json.dumps(data.to_dict())
        elif isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            payload = json.dumps(data)
        # to_byte_array may return str for text content types (e.g. JSON);
        # we always emit bytes so the AMQP body is a binary section rather
        # than an AMQP string section containing escaped JSON.
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    @staticmethod
    def _coerce_amqp_timestamp(value: typing.Any) -> typing.Optional[int]:
        if value is None:
            return None
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return int(value.timestamp() * 1000)
        if isinstance(value, (int, float)):
            return int(value)
        text = str(value)
        normalized = text[:-1] + '+00:00' if text.endswith('Z') else text
        try:
            return int(datetime.fromisoformat(normalized).timestamp() * 1000)
        except ValueError:
            return None

    @staticmethod
    def _ce_headers_to_amqp_properties(headers: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """Translate cloudevents-sdk HTTP-style headers (``ce-foo``) into the
        CloudEvents AMQP 1.0 Protocol Binding (v1.0.2 §3.1) form
        (``cloudEvents:foo``). ``content-type`` is carried separately on the
        AMQP properties section and is therefore dropped here.
        """
        out: typing.Dict[str, typing.Any] = {}
        for k, v in (headers or {}).items():
            if v is None:
                continue
            lk = str(k)
            low = lk.lower()
            if low.startswith('ce-'):
                out['cloudEvents:' + lk[3:]] = v
            elif low == 'content-type':
                continue
            else:
                out[lk] = v
        return out

    
    
    def send_station(self,
        data: Station,
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send the `CA.Gov.ECCC.Weather.mqtt.Station` message
        A reference record published by Environment and Climate Change Canada (ECCC). It lets consumers label, group, and route the live measurement or forecast events.
        
        Args:
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            data (Station): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "CA.Gov.ECCC.Weather.Station",
            "source":
            "https://api.weather.gc.ca",
            "subject":
            "{msc_id}".format(msc_id=_msc_id),
        }
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        amqp_creation_time = self._coerce_amqp_timestamp(attributes.get('time'))
        if amqp_creation_time is not None:
            amqp_msg.creation_time = amqp_creation_time

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)

        annotations = {}
        if annotations:
            if amqp_msg.annotations is None:
                amqp_msg.annotations = {}
            amqp_msg.annotations.update(annotations)
        
        # Send message
        self._send_via_blocking_sender(amqp_msg)
    
    def send_station_batch(self,
        data_array: typing.List[Station],
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `CA.Gov.ECCC.Weather.mqtt.Station` messages
        
        Args:
            data_array (typing.List[Station]): Array of message data objects
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_station(
                data=data,
                _msc_id=_msc_id,
                _time=_time,
                content_type=content_type)
    
    
    def send_weather_observation(self,
        data: WeatherObservation,
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send the `CA.Gov.ECCC.Weather.mqtt.WeatherObservation` message
        A current environmental measurement from Environment and Climate Change Canada (ECCC). It carries current weather observations when the upstream feed reports a new or refreshed value.
        
        Args:
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            data (WeatherObservation): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "CA.Gov.ECCC.Weather.WeatherObservation",
            "source":
            "https://api.weather.gc.ca",
            "subject":
            "{msc_id}".format(msc_id=_msc_id),
        }
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        amqp_creation_time = self._coerce_amqp_timestamp(attributes.get('time'))
        if amqp_creation_time is not None:
            amqp_msg.creation_time = amqp_creation_time

        app_properties = {}
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)

        annotations = {}
        if annotations:
            if amqp_msg.annotations is None:
                amqp_msg.annotations = {}
            amqp_msg.annotations.update(annotations)
        
        # Send message
        self._send_via_blocking_sender(amqp_msg)
    
    def send_weather_observation_batch(self,
        data_array: typing.List[WeatherObservation],
        _msc_id: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `CA.Gov.ECCC.Weather.mqtt.WeatherObservation` messages
        
        Args:
            data_array (typing.List[WeatherObservation]): Array of message data objects
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_weather_observation(
                data=data,
                _msc_id=_msc_id,
                _time=_time,
                content_type=content_type)
    
    
    def close(self) -> None:
        """
        Close the producer and clean up resources
        """
        if hasattr(self, '_sender') and self._sender:
            try:
                self._sender.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._sender = None
        if hasattr(self, '_connection') and self._connection:
            try:
                self._connection.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._connection = None



class CAGovECCCWeatherAmqpProducer:
    """
    Producer class to send messages in the `CA.Gov.ECCC.Weather.amqp` message group via AMQP 1.0 protocol.
    """
    
    def __init__(self, 
                 host: str,
                 address: str,
                 port: int = 5672,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 content_mode: typing.Literal['structured', 'binary'] = 'structured',
                 format_type: str = 'application/json',
                 ):
        """
        Initialize the AMQP producer
        
        Args:
            host (str): The AMQP broker hostname
            address (str): The AMQP address (queue or topic)
            port (int): The AMQP broker port (default: 5672)
            username (typing.Optional[str]): Optional username for SASL PLAIN authentication
            password (typing.Optional[str]): Optional password for SASL PLAIN authentication
            content_mode (typing.Literal['structured', 'binary']): CloudEvents content mode (default: 'structured')
            format_type (str): Content type format for structured mode (default: 'application/json')
        """
        self.host = host
        self.port = port
        self.address = address
        self.username = username
        self.password = password
        self.content_mode = content_mode
        self.format_type = format_type
        self._init_blocking_sender()

    def _init_blocking_sender(self) -> None:
        connection_url = self._build_connection_url()
        connection_timeout = 120 if self.username and self.password else 30
        # Artemis-class brokers can stall unsettled BlockingSender sends on
        # SASL PLAIN links; a pre-settled sender avoids the timeout loop.
        sender_options = AtMostOnce() if self.username and self.password else None
        self._blocking_sender_is_presettled = sender_options is not None
        self._connection = BlockingConnection(connection_url, timeout=connection_timeout)
        self._sender = self._connection.create_sender(self.address, options=sender_options)

    def _send_via_blocking_sender(self, amqp_msg: Message, timeout: float = 30.0) -> None:
        self._sender.send(amqp_msg, timeout=timeout)
        if self._blocking_sender_is_presettled:
            # BlockingSender.send() returns immediately for pre-settled
            # deliveries, so wait until Proton has drained the link queue
            # and flushed all pending bytes.
            self._connection.wait(
                lambda: (
                    self._sender.link.queued == 0 and
                    self._connection.conn.transport is not None and
                    self._connection.conn.transport.pending() == 0
                ),
                msg=f"Flushing sender {self._sender.link.name} transport",
                timeout=timeout,
            )
    
    def _build_connection_url(self) -> str:
        if self.username and self.password:
            user = quote_plus(self.username)
            pwd = quote_plus(self.password)
            return f"amqp://{user}:{pwd}@{self.host}:{self.port}"
        return f"amqp://{self.host}:{self.port}"

    def _serialize_payload(self, data: typing.Any, content_type: str) -> bytes:
        if data is None:
            return b''
        if hasattr(data, 'to_byte_array'):
            payload = data.to_byte_array(content_type)
        elif hasattr(data, 'to_dict'):
            payload = json.dumps(data.to_dict())
        elif isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            payload = json.dumps(data)
        # to_byte_array may return str for text content types (e.g. JSON);
        # we always emit bytes so the AMQP body is a binary section rather
        # than an AMQP string section containing escaped JSON.
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    @staticmethod
    def _coerce_amqp_timestamp(value: typing.Any) -> typing.Optional[int]:
        if value is None:
            return None
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return int(value.timestamp() * 1000)
        if isinstance(value, (int, float)):
            return int(value)
        text = str(value)
        normalized = text[:-1] + '+00:00' if text.endswith('Z') else text
        try:
            return int(datetime.fromisoformat(normalized).timestamp() * 1000)
        except ValueError:
            return None

    @staticmethod
    def _ce_headers_to_amqp_properties(headers: typing.Mapping[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        """Translate cloudevents-sdk HTTP-style headers (``ce-foo``) into the
        CloudEvents AMQP 1.0 Protocol Binding (v1.0.2 §3.1) form
        (``cloudEvents:foo``). ``content-type`` is carried separately on the
        AMQP properties section and is therefore dropped here.
        """
        out: typing.Dict[str, typing.Any] = {}
        for k, v in (headers or {}).items():
            if v is None:
                continue
            lk = str(k)
            low = lk.lower()
            if low.startswith('ce-'):
                out['cloudEvents:' + lk[3:]] = v
            elif low == 'content-type':
                continue
            else:
                out[lk] = v
        return out

    
    
    def send_station(self,
        data: Station,
        _msc_id: str,
        _province: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send the `CA.Gov.ECCC.Weather.amqp.Station` message
        A reference record published by Environment and Climate Change Canada (ECCC). It lets consumers label, group, and route the live measurement or forecast events.
        
        Args:
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _province (str): Value for AMQP protocol option placeholder province
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            data (Station): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "CA.Gov.ECCC.Weather.Station",
            "source":
            "https://api.weather.gc.ca",
            "subject":
            "{msc_id}".format(msc_id=_msc_id),
        }
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        amqp_creation_time = self._coerce_amqp_timestamp(attributes.get('time'))
        if amqp_creation_time is not None:
            amqp_msg.creation_time = amqp_creation_time
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{msc_id}".format(msc_id=_msc_id)

        app_properties = {}
        app_properties["province"] = "{province}".format(province=_province)
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)

        annotations = {}
        if annotations:
            if amqp_msg.annotations is None:
                amqp_msg.annotations = {}
            amqp_msg.annotations.update(annotations)
        
        # Send message
        self._send_via_blocking_sender(amqp_msg)
    
    def send_station_batch(self,
        data_array: typing.List[Station],
        _msc_id: str,
        _province: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `CA.Gov.ECCC.Weather.amqp.Station` messages
        
        Args:
            data_array (typing.List[Station]): Array of message data objects
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            _province (str): Value for AMQP protocol option placeholder province
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_station(
                data=data,
                _msc_id=_msc_id,
                _time=_time,
                _province=_province,
                content_type=content_type)
    
    
    def send_weather_observation(self,
        data: WeatherObservation,
        _msc_id: str,
        _province: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send the `CA.Gov.ECCC.Weather.amqp.WeatherObservation` message
        A current environmental measurement from Environment and Climate Change Canada (ECCC). It carries current weather observations when the upstream feed reports a new or refreshed value.
        
        Args:
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _province (str): Value for AMQP protocol option placeholder province
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            data (WeatherObservation): The message data object
            content_type (str): The content type of the message data (default: 'application/json')
        """
        # Build CloudEvent attributes
        attributes = {
            "type":
            "CA.Gov.ECCC.Weather.WeatherObservation",
            "source":
            "https://api.weather.gc.ca",
            "subject":
            "{msc_id}".format(msc_id=_msc_id),
        }
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        
        # Remove None values
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        # Serialize data
        byte_data = self._serialize_payload(data, content_type)
        
        # Create CloudEvent
        cloud_event = CloudEvent(attributes, byte_data)
        
        # Convert to AMQP message based on content mode
        if self.content_mode == 'structured':
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode('utf-8')
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode('utf-8')
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.format_type or headers.get('content-type')
        else:  # binary mode
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode('utf-8')
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._ce_headers_to_amqp_properties(headers)
        amqp_creation_time = self._coerce_amqp_timestamp(attributes.get('time'))
        if amqp_creation_time is not None:
            amqp_msg.creation_time = amqp_creation_time
        # Apply AMQP message properties declared in protocoloptions.properties.
        amqp_msg.subject = "{msc_id}".format(msc_id=_msc_id)

        app_properties = {}
        app_properties["province"] = "{province}".format(province=_province)
        if app_properties:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(app_properties)

        annotations = {}
        if annotations:
            if amqp_msg.annotations is None:
                amqp_msg.annotations = {}
            amqp_msg.annotations.update(annotations)
        
        # Send message
        self._send_via_blocking_sender(amqp_msg)
    
    def send_weather_observation_batch(self,
        data_array: typing.List[WeatherObservation],
        _msc_id: str,
        _province: str,
        _time: typing.Optional[typing.Union[str, datetime]] = None,
        content_type: str = 'application/json') -> None:
        """
        Send multiple `CA.Gov.ECCC.Weather.amqp.WeatherObservation` messages
        
        Args:
            data_array (typing.List[WeatherObservation]): Array of message data objects
            _msc_id (str): Value for placeholder msc_id in attribute subject
            _time (typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            _province (str): Value for AMQP protocol option placeholder province
            content_type (str): The content type of the message data
        """
        for data in data_array:
            self.send_weather_observation(
                data=data,
                _msc_id=_msc_id,
                _time=_time,
                _province=_province,
                content_type=content_type)
    
    
    def close(self) -> None:
        """
        Close the producer and clean up resources
        """
        if hasattr(self, '_sender') and self._sender:
            try:
                self._sender.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._sender = None
        if hasattr(self, '_connection') and self._connection:
            try:
                self._connection.close()
            except Exception:  # pragma: no cover - best-effort cleanup
                pass
            finally:
                self._connection = None

