# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from bluesky_producer_data import Post
from bluesky_producer_data import Like
from bluesky_producer_data import Repost
from bluesky_producer_data import Follow
from bluesky_producer_data import Block
from bluesky_producer_data import Profile

class BlueskyFirehoseEventProducer:
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

    def send_bluesky_feed_post(self,_firehoseurl : str, _did : str, data: Post, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Post], str]=None) -> None:
        """
        Sends the 'Bluesky.Feed.Post' event to the Kafka topic

        Args:
            _firehoseurl(str):  Value for placeholder firehoseurl in attribute source
            _did(str):  Value for placeholder did in attribute subject
            data: (Post): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Post], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"Bluesky.Feed.Post",
             "source":"{firehoseurl}".format(firehoseurl = _firehoseurl),
             "subject":"{did}".format(did = _did),
             "dataschema":"https://c98acd97-4363-4296-8323-b6ab21e53903.westcentralus.messagingcatalog.azure.net/schemagroups/f043d8c3-32c7-4c3e-8527-d79e0ac996e5/schemas/Bluesky.Feed.Post/versions/v1"
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


    def send_bluesky_feed_like(self,_firehoseurl : str, _did : str, data: Like, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Like], str]=None) -> None:
        """
        Sends the 'Bluesky.Feed.Like' event to the Kafka topic

        Args:
            _firehoseurl(str):  Value for placeholder firehoseurl in attribute source
            _did(str):  Value for placeholder did in attribute subject
            data: (Like): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Like], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"Bluesky.Feed.Like",
             "source":"{firehoseurl}".format(firehoseurl = _firehoseurl),
             "subject":"{did}".format(did = _did),
             "dataschema":"https://c98acd97-4363-4296-8323-b6ab21e53903.westcentralus.messagingcatalog.azure.net/schemagroups/f043d8c3-32c7-4c3e-8527-d79e0ac996e5/schemas/Bluesky.Feed.Like/versions/v2"
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


    def send_bluesky_feed_repost(self,_firehoseurl : str, _did : str, data: Repost, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Repost], str]=None) -> None:
        """
        Sends the 'Bluesky.Feed.Repost' event to the Kafka topic

        Args:
            _firehoseurl(str):  Value for placeholder firehoseurl in attribute source
            _did(str):  Value for placeholder did in attribute subject
            data: (Repost): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Repost], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"Bluesky.Feed.Repost",
             "source":"{firehoseurl}".format(firehoseurl = _firehoseurl),
             "subject":"{did}".format(did = _did),
             "dataschema":"https://c98acd97-4363-4296-8323-b6ab21e53903.westcentralus.messagingcatalog.azure.net/schemagroups/f043d8c3-32c7-4c3e-8527-d79e0ac996e5/schemas/Bluesky.Feed.Repost/versions/v1"
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


    def send_bluesky_graph_follow(self,_firehoseurl : str, _did : str, data: Follow, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Follow], str]=None) -> None:
        """
        Sends the 'Bluesky.Graph.Follow' event to the Kafka topic

        Args:
            _firehoseurl(str):  Value for placeholder firehoseurl in attribute source
            _did(str):  Value for placeholder did in attribute subject
            data: (Follow): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Follow], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"Bluesky.Graph.Follow",
             "source":"{firehoseurl}".format(firehoseurl = _firehoseurl),
             "subject":"{did}".format(did = _did),
             "dataschema":"https://c98acd97-4363-4296-8323-b6ab21e53903.westcentralus.messagingcatalog.azure.net/schemagroups/f043d8c3-32c7-4c3e-8527-d79e0ac996e5/schemas/Bluesky.Graph.Follow/versions/v1"
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


    def send_bluesky_graph_block(self,_firehoseurl : str, _did : str, data: Block, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Block], str]=None) -> None:
        """
        Sends the 'Bluesky.Graph.Block' event to the Kafka topic

        Args:
            _firehoseurl(str):  Value for placeholder firehoseurl in attribute source
            _did(str):  Value for placeholder did in attribute subject
            data: (Block): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Block], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"Bluesky.Graph.Block",
             "source":"{firehoseurl}".format(firehoseurl = _firehoseurl),
             "subject":"{did}".format(did = _did),
             "dataschema":"https://c98acd97-4363-4296-8323-b6ab21e53903.westcentralus.messagingcatalog.azure.net/schemagroups/f043d8c3-32c7-4c3e-8527-d79e0ac996e5/schemas/Bluesky.Graph.Block/versions/v1"
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


    def send_bluesky_actor_profile(self,_firehoseurl : str, _did : str, data: Profile, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Profile], str]=None) -> None:
        """
        Sends the 'Bluesky.Actor.Profile' event to the Kafka topic

        Args:
            _firehoseurl(str):  Value for placeholder firehoseurl in attribute source
            _did(str):  Value for placeholder did in attribute subject
            data: (Profile): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Profile], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"Bluesky.Actor.Profile",
             "source":"{firehoseurl}".format(firehoseurl = _firehoseurl),
             "subject":"{did}".format(did = _did),
             "dataschema":"https://c98acd97-4363-4296-8323-b6ab21e53903.westcentralus.messagingcatalog.azure.net/schemagroups/f043d8c3-32c7-4c3e-8527-d79e0ac996e5/schemas/Bluesky.Actor.Profile/versions/v2"
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'BlueskyFirehoseEventProducer':
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


