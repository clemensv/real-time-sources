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
from noaa_producer_data import WaterLevel
from noaa_producer_data import Predictions
from noaa_producer_data import AirPressure
from noaa_producer_data import AirTemperature
from noaa_producer_data import WaterTemperature
from noaa_producer_data import Wind
from noaa_producer_data import Humidity
from noaa_producer_data import Conductivity
from noaa_producer_data import Salinity
from noaa_producer_data import Station
from noaa_producer_data import Visibility
from noaa_producer_data import Currents
from noaa_producer_data import CurrentPredictions

class MicrosoftOpenDataUSNOAAEventProducer:
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

    def send_microsoft_open_data_us_noaa_water_level(self,_station_id : str, data: WaterLevel, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterLevel], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.WaterLevel' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (WaterLevel): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterLevel], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterLevel",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_predictions(self,_station_id : str, data: Predictions, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Predictions], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Predictions' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Predictions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Predictions], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Predictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_air_pressure(self,_station_id : str, data: AirPressure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirPressure], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.AirPressure' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (AirPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirPressure",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_air_temperature(self,_station_id : str, data: AirTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.AirTemperature' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_water_temperature(self,_station_id : str, data: WaterTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.WaterTemperature' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_wind(self,_station_id : str, data: Wind, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Wind], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Wind' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Wind): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Wind], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Wind",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_humidity(self,_station_id : str, data: Humidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Humidity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Humidity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Humidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Humidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Humidity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_conductivity(self,_station_id : str, data: Conductivity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Conductivity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Conductivity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Conductivity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Conductivity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Conductivity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_salinity(self,_station_id : str, data: Salinity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Salinity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Salinity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_station(self,_station_id : str, data: Station, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Station], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Station' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Station): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Station], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Station",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_visibility(self,_datacontenttype: str, _dataschema: str, _station_id : str, data: Visibility, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Visibility], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Visibility' event to the Kafka topic

        Args:
            _datacontenttype(str) : CloudEvents attribute 'datacontenttype'
            _dataschema(str) : CloudEvents attribute 'dataschema'
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Visibility): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Visibility], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Visibility",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "datacontenttype":_datacontenttype,
             "subject":"{station_id}".format(station_id = _station_id),
             "time":None,
             "dataschema":_dataschema
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


    def send_microsoft_open_data_us_noaa_currents(self,_station_id : str, data: Currents, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Currents], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Currents' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Currents): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Currents], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Currents",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_current_predictions(self,_station_id : str, data: CurrentPredictions, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, CurrentPredictions], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.CurrentPredictions' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (CurrentPredictions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, CurrentPredictions], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.CurrentPredictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'MicrosoftOpenDataUSNOAAEventProducer':
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



class MicrosoftOpenDataUSNOAAMqttEventProducer:
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

    def send_microsoft_open_data_us_noaa_mqtt_water_level(self,_station_id : str, data: WaterLevel, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterLevel], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.WaterLevel' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (WaterLevel): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterLevel], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterLevel",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_predictions(self,_station_id : str, data: Predictions, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Predictions], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Predictions' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Predictions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Predictions], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Predictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_air_pressure(self,_station_id : str, data: AirPressure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirPressure], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.AirPressure' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (AirPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirPressure",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_air_temperature(self,_station_id : str, data: AirTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.AirTemperature' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_water_temperature(self,_station_id : str, data: WaterTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_wind(self,_station_id : str, data: Wind, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Wind], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Wind' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Wind): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Wind], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Wind",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_humidity(self,_station_id : str, data: Humidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Humidity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Humidity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Humidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Humidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Humidity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_conductivity(self,_station_id : str, data: Conductivity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Conductivity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Conductivity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Conductivity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Conductivity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Conductivity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_salinity(self,_station_id : str, data: Salinity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Salinity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Salinity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_station(self,_station_id : str, data: Station, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Station], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Station' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Station): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Station], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Station",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_visibility(self,_datacontenttype: str, _dataschema: str, _station_id : str, data: Visibility, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Visibility], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Visibility' event to the Kafka topic

        Args:
            _datacontenttype(str) : CloudEvents attribute 'datacontenttype'
            _dataschema(str) : CloudEvents attribute 'dataschema'
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Visibility): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Visibility], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Visibility",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "datacontenttype":_datacontenttype,
             "subject":"{station_id}".format(station_id = _station_id),
             "time":None,
             "dataschema":_dataschema
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


    def send_microsoft_open_data_us_noaa_mqtt_currents(self,_station_id : str, data: Currents, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Currents], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.Currents' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Currents): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Currents], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Currents",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_mqtt_current_predictions(self,_station_id : str, data: CurrentPredictions, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, CurrentPredictions], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (CurrentPredictions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, CurrentPredictions], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.CurrentPredictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'MicrosoftOpenDataUSNOAAMqttEventProducer':
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



class MicrosoftOpenDataUSNOAAAmqpEventProducer:
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

    def send_microsoft_open_data_us_noaa_amqp_water_level(self,_station_id : str, data: WaterLevel, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterLevel], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.WaterLevel' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (WaterLevel): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterLevel], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterLevel",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_predictions(self,_station_id : str, data: Predictions, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Predictions], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Predictions' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Predictions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Predictions], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Predictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_air_pressure(self,_station_id : str, data: AirPressure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirPressure], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.AirPressure' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (AirPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirPressure",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_air_temperature(self,_station_id : str, data: AirTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.AirTemperature' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_water_temperature(self,_station_id : str, data: WaterTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.WaterTemperature' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterTemperature",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_wind(self,_station_id : str, data: Wind, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Wind], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Wind' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Wind): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Wind], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Wind",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_humidity(self,_station_id : str, data: Humidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Humidity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Humidity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Humidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Humidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Humidity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_conductivity(self,_station_id : str, data: Conductivity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Conductivity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Conductivity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Conductivity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Conductivity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Conductivity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_salinity(self,_station_id : str, data: Salinity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Salinity' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Salinity",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_station(self,_station_id : str, data: Station, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Station], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Station' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Station): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Station], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Station",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_visibility(self,_datacontenttype: str, _dataschema: str, _station_id : str, data: Visibility, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Visibility], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Visibility' event to the Kafka topic

        Args:
            _datacontenttype(str) : CloudEvents attribute 'datacontenttype'
            _dataschema(str) : CloudEvents attribute 'dataschema'
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Visibility): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Visibility], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Visibility",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "datacontenttype":_datacontenttype,
             "subject":"{station_id}".format(station_id = _station_id),
             "time":None,
             "dataschema":_dataschema
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


    def send_microsoft_open_data_us_noaa_amqp_currents(self,_station_id : str, data: Currents, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Currents], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.Currents' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (Currents): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Currents], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Currents",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_microsoft_open_data_us_noaa_amqp_current_predictions(self,_station_id : str, data: CurrentPredictions, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, CurrentPredictions], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.amqp.CurrentPredictions' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (CurrentPredictions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, CurrentPredictions], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.CurrentPredictions",
             "source":"https://api.tidesandcurrents.noaa.gov",
             "subject":"{station_id}".format(station_id = _station_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'MicrosoftOpenDataUSNOAAAmqpEventProducer':
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

