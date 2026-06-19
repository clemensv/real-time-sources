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
from noaa_ndbc_producer_data import BuoyObservation
from noaa_ndbc_producer_data import BuoyStation
from noaa_ndbc_producer_data import BuoySolarRadiationObservation
from noaa_ndbc_producer_data import BuoyOceanographicObservation
from noaa_ndbc_producer_data import BuoyDartMeasurement
from noaa_ndbc_producer_data import BuoyContinuousWindObservation
from noaa_ndbc_producer_data import BuoySupplementalMeasurement
from noaa_ndbc_producer_data import BuoyDetailedWaveSummary
from noaa_ndbc_producer_data import BuoyHourlyRainMeasurement

class MicrosoftOpenDataUSNOAANDBCEventProducer:
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

    def send_microsoft_open_data_us_noaa_ndbc_buoy_observation(self,_station_id : str, data: BuoyObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_station(self,_station_id : str, data: BuoyStation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyStation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyStation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyStation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_solar_radiation_observation(self,_station_id : str, data: BuoySolarRadiationObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoySolarRadiationObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoySolarRadiationObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoySolarRadiationObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_oceanographic_observation(self,_station_id : str, data: BuoyOceanographicObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyOceanographicObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyOceanographicObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyOceanographicObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_dart_measurement(self,_station_id : str, data: BuoyDartMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyDartMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyDartMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyDartMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_continuous_wind_observation(self,_station_id : str, data: BuoyContinuousWindObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyContinuousWindObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyContinuousWindObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyContinuousWindObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_supplemental_measurement(self,_station_id : str, data: BuoySupplementalMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoySupplementalMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoySupplementalMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoySupplementalMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_detailed_wave_summary(self,_station_id : str, data: BuoyDetailedWaveSummary, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyDetailedWaveSummary], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyDetailedWaveSummary): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyDetailedWaveSummary], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_buoy_hourly_rain_measurement(self,_station_id : str, data: BuoyHourlyRainMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyHourlyRainMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyHourlyRainMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyHourlyRainMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'MicrosoftOpenDataUSNOAANDBCEventProducer':
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



class MicrosoftOpenDataUSNOAANDBCMqttEventProducer:
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

    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation(self,_station_id : str, data: BuoyObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station(self,_station_id : str, data: BuoyStation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyStation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyStation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation(self,_station_id : str, data: BuoySolarRadiationObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoySolarRadiationObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoySolarRadiationObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoySolarRadiationObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation(self,_station_id : str, data: BuoyOceanographicObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyOceanographicObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyOceanographicObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyOceanographicObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement(self,_station_id : str, data: BuoyDartMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyDartMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyDartMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyDartMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation(self,_station_id : str, data: BuoyContinuousWindObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyContinuousWindObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyContinuousWindObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyContinuousWindObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement(self,_station_id : str, data: BuoySupplementalMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoySupplementalMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoySupplementalMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoySupplementalMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary(self,_station_id : str, data: BuoyDetailedWaveSummary, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyDetailedWaveSummary], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyDetailedWaveSummary): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyDetailedWaveSummary], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement(self,_station_id : str, data: BuoyHourlyRainMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyHourlyRainMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyHourlyRainMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyHourlyRainMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'MicrosoftOpenDataUSNOAANDBCMqttEventProducer':
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



class MicrosoftOpenDataUSNOAANDBCAmqpEventProducer:
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

    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_observation(self,_station_id : str, data: BuoyObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_station(self,_station_id : str, data: BuoyStation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyStation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyStation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyStation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_solar_radiation_observation(self,_station_id : str, data: BuoySolarRadiationObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoySolarRadiationObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySolarRadiationObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoySolarRadiationObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoySolarRadiationObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_oceanographic_observation(self,_station_id : str, data: BuoyOceanographicObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyOceanographicObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyOceanographicObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyOceanographicObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyOceanographicObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_dart_measurement(self,_station_id : str, data: BuoyDartMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyDartMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDartMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyDartMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyDartMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement",
             "source":"https://www.ndbc.noaa.gov",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_continuous_wind_observation(self,_station_id : str, data: BuoyContinuousWindObservation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyContinuousWindObservation], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyContinuousWindObservation' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyContinuousWindObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyContinuousWindObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_supplemental_measurement(self,_station_id : str, data: BuoySupplementalMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoySupplementalMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySupplementalMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoySupplementalMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoySupplementalMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_detailed_wave_summary(self,_station_id : str, data: BuoyDetailedWaveSummary, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyDetailedWaveSummary], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDetailedWaveSummary' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyDetailedWaveSummary): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyDetailedWaveSummary], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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


    def send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_hourly_rain_measurement(self,_station_id : str, data: BuoyHourlyRainMeasurement, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BuoyHourlyRainMeasurement], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyHourlyRainMeasurement' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (BuoyHourlyRainMeasurement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BuoyHourlyRainMeasurement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement",
             "source":"https://www.ndbc.noaa.gov/data/realtime2/",
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'MicrosoftOpenDataUSNOAANDBCAmqpEventProducer':
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

