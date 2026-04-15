# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from ticketmaster_producer_data import Event
from ticketmaster_producer_data import Venue
from ticketmaster_producer_data import Attraction
from ticketmaster_producer_data import Classification

class TicketmasterEventsEventProducer:
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

    def send_ticketmaster_events_event(self,_event_id : str, _start_datetime_utc : str, data: Event, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Event], str]=None) -> None:
        """
        Sends the 'Ticketmaster.Events.Event' event to the Kafka topic

        Args:
            _event_id(str):  Value for placeholder event_id in attribute subject
            _start_datetime_utc(str):  Value for placeholder start_datetime_utc in attribute time
            data: (Event): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Event], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{event_id}'
        """
        kafka_key = "{event_id}".format(event_id=_event_id)
        attributes = {
             "type":"Ticketmaster.Events.Event",
             "source":"https://app.ticketmaster.com/discovery/v2/events",
             "subject":"{event_id}".format(event_id = _event_id),
             "time":"{start_datetime_utc}".format(start_datetime_utc = _start_datetime_utc)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'TicketmasterEventsEventProducer':
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



class TicketmasterReferenceEventProducer:
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

    def send_ticketmaster_reference_venue(self,_entity_id : str, data: Venue, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Venue], str]=None) -> None:
        """
        Sends the 'Ticketmaster.Reference.Venue' event to the Kafka topic

        Args:
            _entity_id(str):  Value for placeholder entity_id in attribute subject
            data: (Venue): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Venue], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{entity_id}'
        """
        kafka_key = "{entity_id}".format(entity_id=_entity_id)
        attributes = {
             "type":"Ticketmaster.Reference.Venue",
             "source":"https://app.ticketmaster.com/discovery/v2/venues",
             "subject":"{entity_id}".format(entity_id = _entity_id)
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


    def send_ticketmaster_reference_attraction(self,_entity_id : str, data: Attraction, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Attraction], str]=None) -> None:
        """
        Sends the 'Ticketmaster.Reference.Attraction' event to the Kafka topic

        Args:
            _entity_id(str):  Value for placeholder entity_id in attribute subject
            data: (Attraction): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Attraction], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{entity_id}'
        """
        kafka_key = "{entity_id}".format(entity_id=_entity_id)
        attributes = {
             "type":"Ticketmaster.Reference.Attraction",
             "source":"https://app.ticketmaster.com/discovery/v2/attractions",
             "subject":"{entity_id}".format(entity_id = _entity_id)
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


    def send_ticketmaster_reference_classification(self,_entity_id : str, data: Classification, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Classification], str]=None) -> None:
        """
        Sends the 'Ticketmaster.Reference.Classification' event to the Kafka topic

        Args:
            _entity_id(str):  Value for placeholder entity_id in attribute subject
            data: (Classification): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Classification], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{entity_id}'
        """
        kafka_key = "{entity_id}".format(entity_id=_entity_id)
        attributes = {
             "type":"Ticketmaster.Reference.Classification",
             "source":"https://app.ticketmaster.com/discovery/v2/classifications",
             "subject":"{entity_id}".format(entity_id = _entity_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'TicketmasterReferenceEventProducer':
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

