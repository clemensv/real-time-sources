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
from usgs_iv_producer_data import Site
from usgs_iv_producer_data import SiteTimeseries
from usgs_iv_producer_data import OtherParameter
from usgs_iv_producer_data import Precipitation
from usgs_iv_producer_data import Streamflow
from usgs_iv_producer_data import GageHeight
from usgs_iv_producer_data import WaterTemperature
from usgs_iv_producer_data import DissolvedOxygen
from usgs_iv_producer_data import PH
from usgs_iv_producer_data import SpecificConductance
from usgs_iv_producer_data import Turbidity
from usgs_iv_producer_data import AirTemperature
from usgs_iv_producer_data import WindSpeed
from usgs_iv_producer_data import WindDirection
from usgs_iv_producer_data import RelativeHumidity
from usgs_iv_producer_data import BarometricPressure
from usgs_iv_producer_data import TurbidityFNU
from usgs_iv_producer_data import FDOM
from usgs_iv_producer_data import ReservoirStorage
from usgs_iv_producer_data import LakeElevationNGVD29
from usgs_iv_producer_data import WaterDepth
from usgs_iv_producer_data import EquipmentStatus
from usgs_iv_producer_data import TidallyFilteredDischarge
from usgs_iv_producer_data import WaterVelocity
from usgs_iv_producer_data import EstuaryElevationNGVD29
from usgs_iv_producer_data import LakeElevationNAVD88
from usgs_iv_producer_data import Salinity
from usgs_iv_producer_data import GateOpening

class USGSSitesEventProducer:
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

    def send_usgs_sites_site(self,_source_uri : str, _agency_cd : str, _site_no : str, data: Site, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Site], str]=None) -> None:
        """
        Sends the 'USGS.Sites.Site' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            data: (Site): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Site], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}'
        """
        kafka_key = "{agency_cd}/{site_no}".format(agency_cd=_agency_cd, site_no=_site_no)
        attributes = {
             "type":"USGS.Sites.Site",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}".format(agency_cd = _agency_cd,site_no = _site_no)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSSitesEventProducer':
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



class USGSSiteTimeseriesEventProducer:
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

    def send_usgs_sites_site_timeseries(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: SiteTimeseries, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SiteTimeseries], str]=None) -> None:
        """
        Sends the 'USGS.Sites.SiteTimeseries' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (SiteTimeseries): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SiteTimeseries], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.Sites.SiteTimeseries",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSSiteTimeseriesEventProducer':
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



class USGSInstantaneousValuesEventProducer:
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

    def send_usgs_instantaneous_values_other_parameter(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: OtherParameter, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, OtherParameter], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.OtherParameter' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (OtherParameter): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, OtherParameter], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.OtherParameter",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_precipitation(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Precipitation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Precipitation], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Precipitation' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Precipitation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Precipitation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.Precipitation",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_streamflow(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Streamflow, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Streamflow], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Streamflow' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Streamflow): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Streamflow], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.Streamflow",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_gage_height(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: GageHeight, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GageHeight], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.GageHeight' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (GageHeight): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GageHeight], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.GageHeight",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_water_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WaterTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.WaterTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_dissolved_oxygen(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: DissolvedOxygen, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DissolvedOxygen], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.DissolvedOxygen' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (DissolvedOxygen): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DissolvedOxygen], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.DissolvedOxygen",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_p_h(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: PH, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PH], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.pH' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (PH): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PH], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.pH",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_specific_conductance(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: SpecificConductance, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SpecificConductance], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.SpecificConductance' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (SpecificConductance): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SpecificConductance], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.SpecificConductance",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_turbidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Turbidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Turbidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Turbidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Turbidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Turbidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.Turbidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_air_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: AirTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.AirTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.AirTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_wind_speed(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WindSpeed, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindSpeed], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WindSpeed' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WindSpeed): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindSpeed], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.WindSpeed",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_wind_direction(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WindDirection, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindDirection], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WindDirection' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WindDirection): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindDirection], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.WindDirection",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_relative_humidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: RelativeHumidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RelativeHumidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.RelativeHumidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (RelativeHumidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RelativeHumidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.RelativeHumidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_barometric_pressure(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: BarometricPressure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BarometricPressure], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.BarometricPressure' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (BarometricPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BarometricPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.BarometricPressure",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_turbidity_fnu(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: TurbidityFNU, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TurbidityFNU], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.TurbidityFNU' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (TurbidityFNU): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TurbidityFNU], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.TurbidityFNU",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_f_dom(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: FDOM, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FDOM], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.fDOM' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (FDOM): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FDOM], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.fDOM",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_reservoir_storage(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: ReservoirStorage, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ReservoirStorage], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.ReservoirStorage' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (ReservoirStorage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ReservoirStorage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.ReservoirStorage",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_lake_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: LakeElevationNGVD29, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.LakeElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (LakeElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_water_depth(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterDepth, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterDepth], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WaterDepth' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterDepth): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterDepth], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.WaterDepth",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_equipment_status(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: EquipmentStatus, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EquipmentStatus], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.EquipmentStatus' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (EquipmentStatus): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EquipmentStatus], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.EquipmentStatus",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_tidally_filtered_discharge(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: TidallyFilteredDischarge, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TidallyFilteredDischarge], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.TidallyFilteredDischarge' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (TidallyFilteredDischarge): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TidallyFilteredDischarge], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.TidallyFilteredDischarge",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_water_velocity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterVelocity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterVelocity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WaterVelocity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterVelocity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterVelocity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.WaterVelocity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_estuary_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: EstuaryElevationNGVD29, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EstuaryElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.EstuaryElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (EstuaryElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EstuaryElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.EstuaryElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_lake_elevation_navd88(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: LakeElevationNAVD88, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNAVD88], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.LakeElevationNAVD88' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (LakeElevationNAVD88): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNAVD88], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNAVD88",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_salinity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Salinity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Salinity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.Salinity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_gate_opening(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: GateOpening, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GateOpening], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.GateOpening' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (GateOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GateOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}'
        """
        kafka_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=_agency_cd, site_no=_site_no, parameter_cd=_parameter_cd, timeseries_cd=_timeseries_cd)
        attributes = {
             "type":"USGS.InstantaneousValues.GateOpening",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSInstantaneousValuesEventProducer':
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



class USGSSitesMqttEventProducer:
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

    def send_usgs_sites_mqtt_site(self,_source_uri : str, _agency_cd : str, _site_no : str, data: Site, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Site], str]=None) -> None:
        """
        Sends the 'USGS.Sites.mqtt.Site' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            data: (Site): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Site], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.Sites.Site",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}".format(agency_cd = _agency_cd,site_no = _site_no)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSSitesMqttEventProducer':
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



class USGSSiteTimeseriesMqttEventProducer:
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

    def send_usgs_site_timeseries_mqtt_site_timeseries(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: SiteTimeseries, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SiteTimeseries], str]=None) -> None:
        """
        Sends the 'USGS.SiteTimeseries.mqtt.SiteTimeseries' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (SiteTimeseries): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SiteTimeseries], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.Sites.SiteTimeseries",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSSiteTimeseriesMqttEventProducer':
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



class USGSInstantaneousValuesMqttEventProducer:
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

    def send_usgs_instantaneous_values_mqtt_other_parameter(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: OtherParameter, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, OtherParameter], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.OtherParameter' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (OtherParameter): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, OtherParameter], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.OtherParameter",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_precipitation(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Precipitation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Precipitation], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.Precipitation' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Precipitation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Precipitation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Precipitation",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_streamflow(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Streamflow, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Streamflow], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.Streamflow' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Streamflow): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Streamflow], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Streamflow",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_gage_height(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: GageHeight, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GageHeight], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.GageHeight' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (GageHeight): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GageHeight], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.GageHeight",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_water_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.WaterTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WaterTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_dissolved_oxygen(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: DissolvedOxygen, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DissolvedOxygen], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.DissolvedOxygen' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (DissolvedOxygen): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DissolvedOxygen], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.DissolvedOxygen",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_p_h(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: PH, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PH], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.pH' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (PH): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PH], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.pH",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_specific_conductance(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: SpecificConductance, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SpecificConductance], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.SpecificConductance' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (SpecificConductance): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SpecificConductance], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.SpecificConductance",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_turbidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Turbidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Turbidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.Turbidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Turbidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Turbidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Turbidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_air_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: AirTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.AirTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.AirTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_wind_speed(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WindSpeed, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindSpeed], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.WindSpeed' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WindSpeed): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindSpeed], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WindSpeed",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_wind_direction(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WindDirection, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindDirection], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.WindDirection' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WindDirection): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindDirection], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WindDirection",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_relative_humidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: RelativeHumidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RelativeHumidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.RelativeHumidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (RelativeHumidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RelativeHumidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.RelativeHumidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_barometric_pressure(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: BarometricPressure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BarometricPressure], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.BarometricPressure' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (BarometricPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BarometricPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.BarometricPressure",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_turbidity_fnu(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: TurbidityFNU, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TurbidityFNU], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.TurbidityFNU' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (TurbidityFNU): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TurbidityFNU], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.TurbidityFNU",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_f_dom(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: FDOM, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FDOM], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.fDOM' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (FDOM): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FDOM], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.fDOM",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_reservoir_storage(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: ReservoirStorage, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ReservoirStorage], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.ReservoirStorage' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (ReservoirStorage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ReservoirStorage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.ReservoirStorage",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: LakeElevationNGVD29, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.LakeElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (LakeElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_water_depth(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterDepth, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterDepth], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.WaterDepth' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterDepth): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterDepth], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WaterDepth",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_equipment_status(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: EquipmentStatus, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EquipmentStatus], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.EquipmentStatus' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (EquipmentStatus): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EquipmentStatus], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.EquipmentStatus",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_tidally_filtered_discharge(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: TidallyFilteredDischarge, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TidallyFilteredDischarge], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (TidallyFilteredDischarge): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TidallyFilteredDischarge], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.TidallyFilteredDischarge",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_water_velocity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterVelocity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterVelocity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.WaterVelocity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterVelocity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterVelocity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WaterVelocity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: EstuaryElevationNGVD29, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EstuaryElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (EstuaryElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EstuaryElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.EstuaryElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_lake_elevation_navd88(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: LakeElevationNAVD88, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNAVD88], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.LakeElevationNAVD88' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (LakeElevationNAVD88): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNAVD88], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNAVD88",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_salinity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Salinity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.Salinity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Salinity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_mqtt_gate_opening(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: GateOpening, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GateOpening], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.mqtt.GateOpening' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (GateOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GateOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.GateOpening",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSInstantaneousValuesMqttEventProducer':
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



class USGSSitesAmqpEventProducer:
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

    def send_usgs_sites_amqp_site(self,_source_uri : str, _agency_cd : str, _site_no : str, data: Site, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Site], str]=None) -> None:
        """
        Sends the 'USGS.Sites.amqp.Site' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            data: (Site): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Site], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.Sites.Site",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}".format(agency_cd = _agency_cd,site_no = _site_no)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSSitesAmqpEventProducer':
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



class USGSSiteTimeseriesAmqpEventProducer:
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

    def send_usgs_site_timeseries_amqp_site_timeseries(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: SiteTimeseries, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SiteTimeseries], str]=None) -> None:
        """
        Sends the 'USGS.SiteTimeseries.amqp.SiteTimeseries' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (SiteTimeseries): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SiteTimeseries], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.Sites.SiteTimeseries",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSSiteTimeseriesAmqpEventProducer':
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



class USGSInstantaneousValuesAmqpEventProducer:
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

    def send_usgs_instantaneous_values_amqp_other_parameter(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: OtherParameter, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, OtherParameter], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.OtherParameter' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (OtherParameter): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, OtherParameter], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.OtherParameter",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_precipitation(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Precipitation, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Precipitation], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.Precipitation' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Precipitation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Precipitation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Precipitation",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_streamflow(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Streamflow, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Streamflow], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.Streamflow' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Streamflow): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Streamflow], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Streamflow",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_gage_height(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: GageHeight, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GageHeight], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.GageHeight' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (GageHeight): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GageHeight], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.GageHeight",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_water_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.WaterTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WaterTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_dissolved_oxygen(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: DissolvedOxygen, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DissolvedOxygen], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.DissolvedOxygen' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (DissolvedOxygen): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DissolvedOxygen], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.DissolvedOxygen",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_p_h(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: PH, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PH], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.pH' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (PH): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PH], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.pH",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_specific_conductance(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: SpecificConductance, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SpecificConductance], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.SpecificConductance' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (SpecificConductance): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SpecificConductance], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.SpecificConductance",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_turbidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Turbidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Turbidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.Turbidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Turbidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Turbidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Turbidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_air_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: AirTemperature, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.AirTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.AirTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_wind_speed(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WindSpeed, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindSpeed], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.WindSpeed' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WindSpeed): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindSpeed], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WindSpeed",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_wind_direction(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WindDirection, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindDirection], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.WindDirection' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WindDirection): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindDirection], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WindDirection",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_relative_humidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: RelativeHumidity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RelativeHumidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.RelativeHumidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (RelativeHumidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RelativeHumidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.RelativeHumidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_barometric_pressure(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: BarometricPressure, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BarometricPressure], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.BarometricPressure' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (BarometricPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BarometricPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.BarometricPressure",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_turbidity_fnu(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: TurbidityFNU, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TurbidityFNU], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.TurbidityFNU' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (TurbidityFNU): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TurbidityFNU], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.TurbidityFNU",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_f_dom(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: FDOM, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FDOM], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.fDOM' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (FDOM): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FDOM], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.fDOM",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_reservoir_storage(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: ReservoirStorage, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ReservoirStorage], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.ReservoirStorage' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (ReservoirStorage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ReservoirStorage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.ReservoirStorage",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_lake_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: LakeElevationNGVD29, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.LakeElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (LakeElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_water_depth(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterDepth, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterDepth], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.WaterDepth' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterDepth): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterDepth], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WaterDepth",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_equipment_status(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: EquipmentStatus, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EquipmentStatus], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.EquipmentStatus' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (EquipmentStatus): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EquipmentStatus], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.EquipmentStatus",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_tidally_filtered_discharge(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: TidallyFilteredDischarge, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TidallyFilteredDischarge], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.TidallyFilteredDischarge' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (TidallyFilteredDischarge): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TidallyFilteredDischarge], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.TidallyFilteredDischarge",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_water_velocity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: WaterVelocity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterVelocity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.WaterVelocity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (WaterVelocity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterVelocity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.WaterVelocity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_estuary_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: EstuaryElevationNGVD29, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EstuaryElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.EstuaryElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (EstuaryElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EstuaryElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.EstuaryElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_lake_elevation_navd88(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: LakeElevationNAVD88, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNAVD88], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.LakeElevationNAVD88' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (LakeElevationNAVD88): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNAVD88], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNAVD88",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_salinity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: Salinity, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.Salinity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.Salinity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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


    def send_usgs_instantaneous_values_amqp_gate_opening(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: GateOpening, content_type: str = "application/json", _time: typing.Optional[typing.Union[str, datetime]] = None, flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GateOpening], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.amqp.GateOpening' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            data: (GateOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            _time(typing.Optional[typing.Union[str, datetime]]): CloudEvents time override. Defaults to current UTC when no catalog time is used.
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GateOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
        """
        kafka_key = None
        attributes = {
             "type":"USGS.InstantaneousValues.GateOpening",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":None
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'USGSInstantaneousValuesAmqpEventProducer':
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

