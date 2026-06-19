# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import time
import json
import re
import uuid
import typing
from datetime import datetime, timezone
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent

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
from ndw_road_traffic_producer_data import PointMeasurementSite
from ndw_road_traffic_producer_data import RouteMeasurementSite
from ndw_road_traffic_producer_data import TrafficObservation
from ndw_road_traffic_producer_data import TravelTimeObservation
from ndw_road_traffic_producer_data import DripSign
from ndw_road_traffic_producer_data import DripDisplayState
from ndw_road_traffic_producer_data import MsiSign
from ndw_road_traffic_producer_data import MsiDisplayState
from ndw_road_traffic_producer_data import Roadwork
from ndw_road_traffic_producer_data import BridgeOpening
from ndw_road_traffic_producer_data import TemporaryClosure
from ndw_road_traffic_producer_data import TemporarySpeedLimit
from ndw_road_traffic_producer_data import SafetyRelatedMessage

class NLNDWAVGEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_avg_point_measurement_site(self,_measurement_site_id : str, data: PointMeasurementSite, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PointMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.PointMeasurementSite' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (PointMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PointMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.PointMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_route_measurement_site(self,_measurement_site_id : str, data: RouteMeasurementSite, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RouteMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.RouteMeasurementSite' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (RouteMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RouteMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.RouteMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_traffic_observation(self,_measurement_site_id : str, data: TrafficObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TrafficObservation' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TrafficObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.TrafficObservation",
             "source":"https://opendata.ndw.nu/trafficspeed.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_travel_time_observation(self,_measurement_site_id : str, data: TravelTimeObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TravelTimeObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TravelTimeObservation' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TravelTimeObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TravelTimeObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.TravelTimeObservation",
             "source":"https://opendata.ndw.nu/traveltime.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWAVGEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWDRIPEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_drip_drip_sign(self,_vms_controller_id : str, _vms_index : str, data: DripSign, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripSign' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'drips/{vms_controller_id}/{vms_index}'
        """
        kafka_key = "drips/{vms_controller_id}/{vms_index}".format(vms_controller_id=_vms_controller_id, vms_index=_vms_index)
        attributes = {
             "type":"NL.NDW.DRIP.DripSign",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_drip_drip_display_state(self,_vms_controller_id : str, _vms_index : str, data: DripDisplayState, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripDisplayState' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'drips/{vms_controller_id}/{vms_index}'
        """
        kafka_key = "drips/{vms_controller_id}/{vms_index}".format(vms_controller_id=_vms_controller_id, vms_index=_vms_index)
        attributes = {
             "type":"NL.NDW.DRIP.DripDisplayState",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWDRIPEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWMSIEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_msi_msi_sign(self,_sign_id : str, data: MsiSign, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiSign' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'msi-signs/{sign_id}'
        """
        kafka_key = "msi-signs/{sign_id}".format(sign_id=_sign_id)
        attributes = {
             "type":"NL.NDW.MSI.MsiSign",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_msi_msi_display_state(self,_sign_id : str, data: MsiDisplayState, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiDisplayState' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'msi-signs/{sign_id}'
        """
        kafka_key = "msi-signs/{sign_id}".format(sign_id=_sign_id)
        attributes = {
             "type":"NL.NDW.MSI.MsiDisplayState",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWMSIEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWSituationsEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_situations_roadwork(self,_situation_record_id : str, data: Roadwork, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Roadwork], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.Roadwork' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (Roadwork): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Roadwork], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.Roadwork",
             "source":"https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_bridge_opening(self,_situation_record_id : str, data: BridgeOpening, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BridgeOpening], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.BridgeOpening' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (BridgeOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BridgeOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.BridgeOpening",
             "source":"https://opendata.ndw.nu/planningsfeed_brugopeningen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_temporary_closure(self,_situation_record_id : str, data: TemporaryClosure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporaryClosure], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporaryClosure' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporaryClosure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporaryClosure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.TemporaryClosure",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_temporary_speed_limit(self,_situation_record_id : str, data: TemporarySpeedLimit, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporarySpeedLimit], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporarySpeedLimit' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporarySpeedLimit): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporarySpeedLimit], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.TemporarySpeedLimit",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_safety_related_message(self,_situation_record_id : str, data: SafetyRelatedMessage, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SafetyRelatedMessage], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.SafetyRelatedMessage' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (SafetyRelatedMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SafetyRelatedMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.SafetyRelatedMessage",
             "source":"https://opendata.ndw.nu/veiligheidsgerelateerde_berichten_srti.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWSituationsEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWAVGMqttEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_avg_point_measurement_site_mqtt(self,_measurement_site_id : str, data: PointMeasurementSite, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PointMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.PointMeasurementSite.mqtt' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (PointMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PointMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.PointMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_route_measurement_site_mqtt(self,_measurement_site_id : str, data: RouteMeasurementSite, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RouteMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.RouteMeasurementSite.mqtt' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (RouteMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RouteMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.RouteMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_traffic_observation_mqtt(self,_measurement_site_id : str, data: TrafficObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TrafficObservation.mqtt' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TrafficObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.TrafficObservation",
             "source":"https://opendata.ndw.nu/trafficspeed.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_travel_time_observation_mqtt(self,_measurement_site_id : str, data: TravelTimeObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TravelTimeObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TravelTimeObservation.mqtt' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TravelTimeObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TravelTimeObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.TravelTimeObservation",
             "source":"https://opendata.ndw.nu/traveltime.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWAVGMqttEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWDRIPMqttEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_drip_drip_sign_mqtt(self,_vms_controller_id : str, _vms_index : str, data: DripSign, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripSign.mqtt' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.DRIP.DripSign",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_drip_drip_display_state_mqtt(self,_vms_controller_id : str, _vms_index : str, data: DripDisplayState, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripDisplayState.mqtt' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.DRIP.DripDisplayState",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWDRIPMqttEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWMSIMqttEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_msi_msi_sign_mqtt(self,_sign_id : str, data: MsiSign, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiSign.mqtt' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.MSI.MsiSign",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_msi_msi_display_state_mqtt(self,_sign_id : str, data: MsiDisplayState, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiDisplayState.mqtt' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.MSI.MsiDisplayState",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWMSIMqttEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWSituationsMqttEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_situations_roadwork_mqtt(self,_situation_record_id : str, data: Roadwork, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Roadwork], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.Roadwork.mqtt' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (Roadwork): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Roadwork], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.Roadwork",
             "source":"https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_bridge_opening_mqtt(self,_situation_record_id : str, data: BridgeOpening, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BridgeOpening], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.BridgeOpening.mqtt' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (BridgeOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BridgeOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.BridgeOpening",
             "source":"https://opendata.ndw.nu/planningsfeed_brugopeningen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_temporary_closure_mqtt(self,_situation_record_id : str, data: TemporaryClosure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporaryClosure], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporaryClosure.mqtt' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporaryClosure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporaryClosure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.TemporaryClosure",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_temporary_speed_limit_mqtt(self,_situation_record_id : str, data: TemporarySpeedLimit, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporarySpeedLimit], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporarySpeedLimit.mqtt' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporarySpeedLimit): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporarySpeedLimit], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.TemporarySpeedLimit",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_safety_related_message_mqtt(self,_situation_record_id : str, data: SafetyRelatedMessage, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SafetyRelatedMessage], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.SafetyRelatedMessage.mqtt' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (SafetyRelatedMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SafetyRelatedMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.SafetyRelatedMessage",
             "source":"https://opendata.ndw.nu/veiligheidsgerelateerde_berichten_srti.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWSituationsMqttEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWAVGAmqpEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_avg_point_measurement_site_amqp(self,_measurement_site_id : str, data: PointMeasurementSite, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PointMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.PointMeasurementSite.amqp' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (PointMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PointMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.PointMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_route_measurement_site_amqp(self,_measurement_site_id : str, data: RouteMeasurementSite, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RouteMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.RouteMeasurementSite.amqp' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (RouteMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RouteMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.RouteMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_traffic_observation_amqp(self,_measurement_site_id : str, data: TrafficObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TrafficObservation.amqp' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TrafficObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.TrafficObservation",
             "source":"https://opendata.ndw.nu/trafficspeed.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_avg_travel_time_observation_amqp(self,_measurement_site_id : str, data: TravelTimeObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TravelTimeObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TravelTimeObservation.amqp' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TravelTimeObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TravelTimeObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.AVG.TravelTimeObservation",
             "source":"https://opendata.ndw.nu/traveltime.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWAVGAmqpEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWDRIPAmqpEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_drip_drip_sign_amqp(self,_vms_controller_id : str, _vms_index : str, data: DripSign, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripSign.amqp' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.DRIP.DripSign",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_drip_drip_display_state_amqp(self,_vms_controller_id : str, _vms_index : str, data: DripDisplayState, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripDisplayState.amqp' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.DRIP.DripDisplayState",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWDRIPAmqpEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWMSIAmqpEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_msi_msi_sign_amqp(self,_sign_id : str, data: MsiSign, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiSign.amqp' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.MSI.MsiSign",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_msi_msi_display_state_amqp(self,_sign_id : str, data: MsiDisplayState, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiDisplayState.amqp' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.MSI.MsiDisplayState",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWMSIAmqpEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)



class NLNDWSituationsAmqpEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        """
        Initializes the Kafka producer

        Args:
            producer (Producer): The Kafka producer client
            topic (str): The Kafka topic to send events to
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events
        """
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def __key_mapper(x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
            default_key (Optional[str]): The resolved key from the xRegistry model declaration
        """
        if key_mapper:
            return key_mapper(x, m)
        elif default_key is not None:
            return default_key
        return f"{x['type']}:{x['source']}-{x.get('subject', '')}"

    @staticmethod
    def __binary_data_marshaller(data: typing.Any) -> bytes:
        """Serialize dataclass payloads to bytes for Kafka binary mode."""
        payload = data.to_byte_array("application/json")
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return payload

    def send_nl_ndw_situations_roadwork_amqp(self,_situation_record_id : str, data: Roadwork, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Roadwork], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.Roadwork.amqp' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (Roadwork): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Roadwork], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.Roadwork",
             "source":"https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_bridge_opening_amqp(self,_situation_record_id : str, data: BridgeOpening, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BridgeOpening], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.BridgeOpening.amqp' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (BridgeOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BridgeOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.BridgeOpening",
             "source":"https://opendata.ndw.nu/planningsfeed_brugopeningen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_temporary_closure_amqp(self,_situation_record_id : str, data: TemporaryClosure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporaryClosure], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporaryClosure.amqp' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporaryClosure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporaryClosure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.TemporaryClosure",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_temporary_speed_limit_amqp(self,_situation_record_id : str, data: TemporarySpeedLimit, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporarySpeedLimit], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporarySpeedLimit.amqp' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporarySpeedLimit): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporarySpeedLimit], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.TemporarySpeedLimit",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nl_ndw_situations_safety_related_message_amqp(self,_situation_record_id : str, data: SafetyRelatedMessage, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SafetyRelatedMessage], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.SafetyRelatedMessage.amqp' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (SafetyRelatedMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SafetyRelatedMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"NL.NDW.Situations.SafetyRelatedMessage",
             "source":"https://opendata.ndw.nu/veiligheidsgerelateerde_berichten_srti.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
        }
        attributes["datacontenttype"] = content_type
        attributes["time"] = _resolve_cloudevents_time(_time, attributes.get("time"))
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: self.__binary_data_marshaller(x), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def flush(self, timeout: float = 30, retries: int = 3, backoff_factor: float = 2.0) -> None:
        """Flush pending messages with retry and exponential backoff.

        Brokers that drop idle connections (e.g. Azure Event Hubs, Confluent
        Cloud) can make a single ``flush()`` fail right after a reconnect, so a
        bare ``flush(timeout)`` is not resilient on its own. This retries the
        flush, sleeping ``backoff_factor ** attempt`` seconds between attempts,
        and raises ``RuntimeError`` if any messages remain unsent after all
        attempts.

        Args:
            timeout (float): Seconds to wait for each underlying flush attempt.
            retries (int): Maximum number of flush attempts.
            backoff_factor (float): Base of the exponential backoff between attempts.

        Raises:
            RuntimeError: If messages remain unsent after all retries.
        """
        for attempt in range(1, retries + 1):
            remaining = self.producer.flush(timeout)
            if remaining == 0:
                return
            if attempt < retries:
                time.sleep(backoff_factor ** attempt)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} message(s) unsent after {retries} attempt(s)."
                )

    @classmethod
    def parse_connection_string(cls, connection_string: str) -> typing.Tuple[typing.Dict[str, str], str]:
        """
        Parse the connection string and extract bootstrap server, topic name, username, and password.

        Args:
            connection_string (str): The connection string.

        Returns:
            Tuple[Dict[str, str], str]: Kafka config, topic name
        """
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = None
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').replace('sb://', '').replace('/', '')+':9093'
                elif 'EntityPath' in part:
                    kafka_topic = part.split('=')[1].strip('"')
        except IndexError as e:
            raise ValueError("Invalid connection string format") from e
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWSituationsAmqpEventProducer':
        """
        Create a Kafka producer from a connection string and a topic name.

        Args:
            connection_string (str): The connection string.
            topic (Optional[str]): The Kafka topic.
            content_mode (typing.Literal['structured','binary']): The content mode to use for sending events

        Returns:
            Producer: The Kafka producer
        """
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        if not topic_name:
            raise ValueError("Topic name not found in connection string")
        return cls(Producer(config), topic_name, content_mode)

