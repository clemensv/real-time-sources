# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from nextbus_producer_data import VehiclePosition
from nextbus_producer_data import RouteConfig
from nextbus_producer_data import Schedule
from nextbus_producer_data import Message

class NextbusEventProducer:
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

    def send_nextbus_vehicle_position(self,_agency_id : str, _route_tag : str, _vehicle_id : str, _timestamp : str, data: VehiclePosition, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, VehiclePosition], str]=None) -> None:
        """
        Sends the 'nextbus.VehiclePosition' event to the Kafka topic

        Args:
            _agency_id(str):  Value for placeholder agency_id in attribute subject
            _route_tag(str):  Value for placeholder route_tag in attribute subject
            _vehicle_id(str):  Value for placeholder vehicle_id in attribute subject
            _timestamp(str):  Value for placeholder timestamp in attribute time
            data: (VehiclePosition): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, VehiclePosition], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_id}/{route_tag}'
        """
        kafka_key = "{agency_id}/{route_tag}".format(agency_id=_agency_id, route_tag=_route_tag)
        attributes = {
             "type":"nextbus.VehiclePosition",
             "source":"https://retro.umoiq.com/service/publicXMLFeed",
             "subject":"{agency_id}/{route_tag}/vehicle/{vehicle_id}".format(agency_id = _agency_id,route_tag = _route_tag,vehicle_id = _vehicle_id),
             "time":"{timestamp}".format(timestamp = _timestamp)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nextbus_route_config(self,_agency_id : str, _route_tag : str, _stop_or_vehicle_id : str, _timestamp : str, data: RouteConfig, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RouteConfig], str]=None) -> None:
        """
        Sends the 'nextbus.RouteConfig' event to the Kafka topic

        Args:
            _agency_id(str):  Value for placeholder agency_id in attribute subject
            _route_tag(str):  Value for placeholder route_tag in attribute subject
            _stop_or_vehicle_id(str):  Value for placeholder stop_or_vehicle_id in attribute subject
            _timestamp(str):  Value for placeholder timestamp in attribute time
            data: (RouteConfig): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RouteConfig], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_id}/{route_tag}'
        """
        kafka_key = "{agency_id}/{route_tag}".format(agency_id=_agency_id, route_tag=_route_tag)
        attributes = {
             "type":"nextbus.RouteConfig",
             "source":"https://retro.umoiq.com/service/publicXMLFeed",
             "subject":"{agency_id}/{route_tag}/route-config/{stop_or_vehicle_id}".format(agency_id = _agency_id,route_tag = _route_tag,stop_or_vehicle_id = _stop_or_vehicle_id),
             "time":"{timestamp}".format(timestamp = _timestamp)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nextbus_schedule(self,_agency_id : str, _route_tag : str, _stop_or_vehicle_id : str, _timestamp : str, data: Schedule, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Schedule], str]=None) -> None:
        """
        Sends the 'nextbus.Schedule' event to the Kafka topic

        Args:
            _agency_id(str):  Value for placeholder agency_id in attribute subject
            _route_tag(str):  Value for placeholder route_tag in attribute subject
            _stop_or_vehicle_id(str):  Value for placeholder stop_or_vehicle_id in attribute subject
            _timestamp(str):  Value for placeholder timestamp in attribute time
            data: (Schedule): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Schedule], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_id}/{route_tag}'
        """
        kafka_key = "{agency_id}/{route_tag}".format(agency_id=_agency_id, route_tag=_route_tag)
        attributes = {
             "type":"nextbus.Schedule",
             "source":"https://retro.umoiq.com/service/publicXMLFeed",
             "subject":"{agency_id}/{route_tag}/schedule/{stop_or_vehicle_id}".format(agency_id = _agency_id,route_tag = _route_tag,stop_or_vehicle_id = _stop_or_vehicle_id),
             "time":"{timestamp}".format(timestamp = _timestamp)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()


    def send_nextbus_message(self,_agency_id : str, _route_tag : str, _stop_or_vehicle_id : str, _timestamp : str, data: Message, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Message], str]=None) -> None:
        """
        Sends the 'nextbus.Message' event to the Kafka topic

        Args:
            _agency_id(str):  Value for placeholder agency_id in attribute subject
            _route_tag(str):  Value for placeholder route_tag in attribute subject
            _stop_or_vehicle_id(str):  Value for placeholder stop_or_vehicle_id in attribute subject
            _timestamp(str):  Value for placeholder timestamp in attribute time
            data: (Message): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Message], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{agency_id}/{route_tag}'
        """
        kafka_key = "{agency_id}/{route_tag}".format(agency_id=_agency_id, route_tag=_route_tag)
        attributes = {
             "type":"nextbus.Message",
             "source":"https://retro.umoiq.com/service/publicXMLFeed",
             "subject":"{agency_id}/{route_tag}/message/{stop_or_vehicle_id}".format(agency_id = _agency_id,route_tag = _route_tag,stop_or_vehicle_id = _stop_or_vehicle_id),
             "time":"{timestamp}".format(timestamp = _timestamp)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            # For binary mode, datacontenttype is already set in attributes above
            # The to_binary() function will create the ce_datacontenttype header
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NextbusEventProducer':
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

