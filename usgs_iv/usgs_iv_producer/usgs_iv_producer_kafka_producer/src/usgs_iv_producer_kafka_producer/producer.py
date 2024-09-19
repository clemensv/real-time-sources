# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from usgs_iv_producer_data.usgs.instantaneousvalues.streamflow import Streamflow
from usgs_iv_producer_data.usgs.instantaneousvalues.gageheight import GageHeight
from usgs_iv_producer_data.usgs.instantaneousvalues.watertemperature import WaterTemperature
from usgs_iv_producer_data.usgs.instantaneousvalues.dissolvedoxygen import DissolvedOxygen
from usgs_iv_producer_data.usgs.instantaneousvalues.ph import PH
from usgs_iv_producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance
from usgs_iv_producer_data.usgs.instantaneousvalues.turbidity import Turbidity

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

    async def send_usgs_instantaneous_values_streamflow(self,data: Streamflow, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Streamflow], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Streamflow' event to the Kafka topic

        Args:
            data: (Streamflow): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Streamflow], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.Streamflow"
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


    async def send_usgs_instantaneous_values_gage_height(self,data: GageHeight, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GageHeight], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.GageHeight' event to the Kafka topic

        Args:
            data: (GageHeight): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GageHeight], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.GageHeight"
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


    async def send_usgs_instantaneous_values_water_temperature(self,data: WaterTemperature, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.WaterTemperature' event to the Kafka topic

        Args:
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.WaterTemperature"
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


    async def send_usgs_instantaneous_values_dissolved_oxygen(self,data: DissolvedOxygen, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DissolvedOxygen], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.DissolvedOxygen' event to the Kafka topic

        Args:
            data: (DissolvedOxygen): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DissolvedOxygen], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.DissolvedOxygen"
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


    async def send_usgs_instantaneous_values_p_h(self,data: PH, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PH], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.pH' event to the Kafka topic

        Args:
            data: (PH): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PH], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.pH"
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


    async def send_usgs_instantaneous_values_specific_conductance(self,data: SpecificConductance, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SpecificConductance], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.SpecificConductance' event to the Kafka topic

        Args:
            data: (SpecificConductance): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SpecificConductance], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.SpecificConductance"
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


    async def send_usgs_instantaneous_values_turbidity(self,data: Turbidity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Turbidity], str]=None) -> None:
        """
        Sends the 'USGS.InstantaneousValues.Turbidity' event to the Kafka topic

        Args:
            data: (Turbidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Turbidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"USGS.InstantaneousValues.Turbidity"
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

