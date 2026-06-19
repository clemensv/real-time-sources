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
from tepco_denkiyoho_producer_data import SupplyCapacity
from tepco_denkiyoho_producer_data import PeakDemandForecast
from tepco_denkiyoho_producer_data import DemandActual
from tepco_denkiyoho_producer_data import DemandForecast
from tepco_denkiyoho_producer_data import Info

class JPTEPCODenkiyohoKafkaEventProducer:
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

    def send_jp_tepco_denkiyoho_kafka_supply_capacity(self,_feedurl : str, _area_code : str, data: SupplyCapacity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SupplyCapacity], str]=None) -> None:
        """
        Sends the 'JP.TEPCO.Denkiyoho.kafka.SupplyCapacity' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _area_code(str):  Value for placeholder area_code in attribute subject
            data: (SupplyCapacity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SupplyCapacity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{area_code}'
        """
        kafka_key = "{area_code}".format(area_code=_area_code)
        attributes = {
             "type":"JP.TEPCO.Denkiyoho.SupplyCapacity",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{area_code}".format(area_code = _area_code)
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


    def send_jp_tepco_denkiyoho_kafka_peak_demand_forecast(self,_feedurl : str, _area_code : str, data: PeakDemandForecast, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PeakDemandForecast], str]=None) -> None:
        """
        Sends the 'JP.TEPCO.Denkiyoho.kafka.PeakDemandForecast' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _area_code(str):  Value for placeholder area_code in attribute subject
            data: (PeakDemandForecast): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PeakDemandForecast], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{area_code}'
        """
        kafka_key = "{area_code}".format(area_code=_area_code)
        attributes = {
             "type":"JP.TEPCO.Denkiyoho.PeakDemandForecast",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{area_code}".format(area_code = _area_code)
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


    def send_jp_tepco_denkiyoho_kafka_demand_actual(self,_feedurl : str, _area_code : str, data: DemandActual, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DemandActual], str]=None) -> None:
        """
        Sends the 'JP.TEPCO.Denkiyoho.kafka.DemandActual' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _area_code(str):  Value for placeholder area_code in attribute subject
            data: (DemandActual): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DemandActual], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{area_code}'
        """
        kafka_key = "{area_code}".format(area_code=_area_code)
        attributes = {
             "type":"JP.TEPCO.Denkiyoho.DemandActual",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{area_code}".format(area_code = _area_code)
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


    def send_jp_tepco_denkiyoho_kafka_demand_forecast(self,_feedurl : str, _area_code : str, data: DemandForecast, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DemandForecast], str]=None) -> None:
        """
        Sends the 'JP.TEPCO.Denkiyoho.kafka.DemandForecast' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _area_code(str):  Value for placeholder area_code in attribute subject
            data: (DemandForecast): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DemandForecast], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{area_code}'
        """
        kafka_key = "{area_code}".format(area_code=_area_code)
        attributes = {
             "type":"JP.TEPCO.Denkiyoho.DemandForecast",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{area_code}".format(area_code = _area_code)
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


    def send_jp_tepco_denkiyoho_kafka_info(self,_area_code : str, data: Info, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Info], str]=None) -> None:
        """
        Sends the 'JP.TEPCO.Denkiyoho.kafka.Info' event to the Kafka topic

        Args:
            _area_code(str):  Value for placeholder area_code in attribute subject
            data: (Info): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Info], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{area_code}'
        """
        kafka_key = "{area_code}".format(area_code=_area_code)
        attributes = {
             "type":"JP.TEPCO.Denkiyoho.Info",
             "source":"https://github.com/clemensv/real-time-sources",
             "subject":"{area_code}".format(area_code = _area_code)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'JPTEPCODenkiyohoKafkaEventProducer':
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

