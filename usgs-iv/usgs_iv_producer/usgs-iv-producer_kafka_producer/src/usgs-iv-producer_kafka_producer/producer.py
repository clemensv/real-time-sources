# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from usgs-iv-producer_data import Site
from usgs-iv-producer_data import SiteTimeseries
from usgs-iv-producer_data import OtherParameter
from usgs-iv-producer_data import Precipitation
from usgs-iv-producer_data import Streamflow
from usgs-iv-producer_data import GageHeight
from usgs-iv-producer_data import WaterTemperature
from usgs-iv-producer_data import DissolvedOxygen
from usgs-iv-producer_data import PH
from usgs-iv-producer_data import SpecificConductance
from usgs-iv-producer_data import Turbidity
from usgs-iv-producer_data import AirTemperature
from usgs-iv-producer_data import WindSpeed
from usgs-iv-producer_data import WindDirection
from usgs-iv-producer_data import RelativeHumidity
from usgs-iv-producer_data import BarometricPressure
from usgs-iv-producer_data import TurbidityFNU
from usgs-iv-producer_data import FDOM
from usgs-iv-producer_data import ReservoirStorage
from usgs-iv-producer_data import LakeElevationNGVD29
from usgs-iv-producer_data import WaterDepth
from usgs-iv-producer_data import EquipmentStatus
from usgs-iv-producer_data import TidallyFilteredDischarge
from usgs-iv-producer_data import WaterVelocity
from usgs-iv-producer_data import EstuaryElevationNGVD29
from usgs-iv-producer_data import LakeElevationNAVD88
from usgs-iv-producer_data import Salinity
from usgs-iv-producer_data import GateOpening

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

    def __key_mapper(self, x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str]) -> str:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
        """
        if key_mapper:
            return key_mapper(x, m)
        else:
            return f'{str(x.get("type"))}:{str(x.get("source"))}{("-"+str(x.get("subject"))) if x.get("subject") else ""}'

    def send_usgs_sites_site(self,_source_uri : str, _agency_cd : str, _site_no : str, data: Site, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Site], str]=None) -> None:
        """
        Sends the 'USGS.Sites.Site' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            data: (Site): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Site], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.Sites.Site",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}".format(agency_cd = _agency_cd,site_no = _site_no)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_sites_site_timeseries(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, data: SiteTimeseries, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SiteTimeseries], str]=None) -> None:
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
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SiteTimeseries], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.Sites.SiteTimeseries",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


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

    def __key_mapper(self, x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str]) -> str:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
            m (Any): The event data
            key_mapper (Callable[[CloudEvent, Any], str]): The user's key mapper function
        """
        if key_mapper:
            return key_mapper(x, m)
        else:
            return f'{str(x.get("type"))}:{str(x.get("source"))}{("-"+str(x.get("subject"))) if x.get("subject") else ""}'

    def send_usgs_instantaneous_values_other_parameter(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: OtherParameter, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, OtherParameter], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.OtherParameter' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (OtherParameter): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, OtherParameter], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.OtherParameter",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_precipitation(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: Precipitation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Precipitation], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Precipitation' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (Precipitation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Precipitation], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.Precipitation",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_streamflow(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: Streamflow, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Streamflow], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Streamflow' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (Streamflow): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Streamflow], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.Streamflow",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_gage_height(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: GageHeight, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GageHeight], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.GageHeight' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (GageHeight): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GageHeight], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.GageHeight",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_water_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: WaterTemperature, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WaterTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.WaterTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_dissolved_oxygen(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: DissolvedOxygen, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DissolvedOxygen], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.DissolvedOxygen' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (DissolvedOxygen): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DissolvedOxygen], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.DissolvedOxygen",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_p_h(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: PH, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PH], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.pH' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (PH): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PH], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.pH",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_specific_conductance(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: SpecificConductance, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SpecificConductance], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.SpecificConductance' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (SpecificConductance): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SpecificConductance], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.SpecificConductance",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_turbidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: Turbidity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Turbidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Turbidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (Turbidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Turbidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.Turbidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_air_temperature(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: AirTemperature, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.AirTemperature' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.AirTemperature",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_wind_speed(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: WindSpeed, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindSpeed], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WindSpeed' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (WindSpeed): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindSpeed], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.WindSpeed",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_wind_direction(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: WindDirection, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindDirection], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WindDirection' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (WindDirection): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindDirection], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.WindDirection",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_relative_humidity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: RelativeHumidity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RelativeHumidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.RelativeHumidity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (RelativeHumidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RelativeHumidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.RelativeHumidity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_barometric_pressure(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: BarometricPressure, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BarometricPressure], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.BarometricPressure' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (BarometricPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BarometricPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.BarometricPressure",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_turbidity_fnu(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: TurbidityFNU, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TurbidityFNU], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.TurbidityFNU' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (TurbidityFNU): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TurbidityFNU], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.TurbidityFNU",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_f_dom(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: FDOM, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FDOM], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.fDOM' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (FDOM): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FDOM], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.fDOM",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_reservoir_storage(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: ReservoirStorage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ReservoirStorage], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.ReservoirStorage' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (ReservoirStorage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ReservoirStorage], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.ReservoirStorage",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_lake_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: LakeElevationNGVD29, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.LakeElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (LakeElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_water_depth(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: WaterDepth, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterDepth], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WaterDepth' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (WaterDepth): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterDepth], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.WaterDepth",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_equipment_status(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: EquipmentStatus, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EquipmentStatus], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.EquipmentStatus' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (EquipmentStatus): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EquipmentStatus], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.EquipmentStatus",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_tidally_filtered_discharge(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: TidallyFilteredDischarge, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TidallyFilteredDischarge], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.TidallyFilteredDischarge' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (TidallyFilteredDischarge): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TidallyFilteredDischarge], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.TidallyFilteredDischarge",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_water_velocity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: WaterVelocity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterVelocity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WaterVelocity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (WaterVelocity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterVelocity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.WaterVelocity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_estuary_elevation_ngvd29(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: EstuaryElevationNGVD29, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, EstuaryElevationNGVD29], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.EstuaryElevationNGVD29' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (EstuaryElevationNGVD29): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, EstuaryElevationNGVD29], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.EstuaryElevationNGVD29",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_lake_elevation_navd88(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: LakeElevationNAVD88, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LakeElevationNAVD88], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.LakeElevationNAVD88' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (LakeElevationNAVD88): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LakeElevationNAVD88], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.LakeElevationNAVD88",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_salinity(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: Salinity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Salinity' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.Salinity",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_usgs_instantaneous_values_gate_opening(self,_source_uri : str, _agency_cd : str, _site_no : str, _parameter_cd : str, _timeseries_cd : str, _datetime : str, data: GateOpening, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GateOpening], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.GateOpening' event to the Kafka topic

        Args:
            _source_uri(str):  Value for placeholder source_uri in attribute source
            _agency_cd(str):  Value for placeholder agency_cd in attribute subject
            _site_no(str):  Value for placeholder site_no in attribute subject
            _parameter_cd(str):  Value for placeholder parameter_cd in attribute subject
            _timeseries_cd(str):  Value for placeholder timeseries_cd in attribute subject
            _datetime(str):  Value for placeholder datetime in attribute time
            data: (GateOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GateOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.GateOpening",
             "source":"{source_uri}".format(source_uri = _source_uri),
             "subject":"{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd = _agency_cd,site_no = _site_no,parameter_cd = _parameter_cd,timeseries_cd = _timeseries_cd),
             "time":"{datetime}".format(datetime = _datetime)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


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

