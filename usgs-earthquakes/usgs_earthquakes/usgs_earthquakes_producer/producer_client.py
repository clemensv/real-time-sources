# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import json
import typing
from confluent_kafka import Producer
from cloudevents.kafka import to_binary, to_structured
from cloudevents.http import CloudEvent
from usgs_earthquakes.usgs_earthquakes_producer.usgs.earthquakes.event import Event


class USGSEarthquakesEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode: typing.Literal['structured','binary']='structured'):
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

    def send_usgs_earthquakes_event(self, _source_uri: str, _net: str, _code: str, _event_time: str, data: Event, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Event], str]=None) -> None:
        """
        Sends the 'USGS.Earthquakes.Event' event to the Kafka topic

        Args:
            _source_uri(str): Value for placeholder source_uri in attribute source
            _net(str): Value for placeholder net in attribute subject
            _code(str): Value for placeholder code in attribute subject
            _event_time(str): Value for placeholder event_time in attribute time
            data: (Event): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Event], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type": "USGS.Earthquakes.Event",
             "source": "{source_uri}".format(source_uri=_source_uri),
             "subject": "{net}/{code}".format(net=_net, code=_code),
             "time": _event_time
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
        """Parse Azure Event Hubs connection string into Kafka config and topic."""
        config_dict = {
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': connection_string.strip()
        }
        kafka_topic = ''
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip('"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                kafka_topic = part.split('=', 1)[1].strip('"')
        return config_dict, kafka_topic

    @classmethod
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str] = None, content_mode: typing.Literal['structured','binary'] = 'structured'):
        """Factory method to create producer from Event Hubs connection string."""
        config, topic_name = cls.parse_connection_string(connection_string)
        if topic:
            topic_name = topic
        return cls(Producer(config), topic_name, content_mode)
