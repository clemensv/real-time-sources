# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from aviationweather_producer_data import Station
from aviationweather_producer_data import Metar
from aviationweather_producer_data import Sigmet

class GovNoaaAviationweatherEventProducer:
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

    def send_gov_noaa_aviationweather_station(self,_icao_id : str, data: Station, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Station], str]=None) -> None:
        """
        Sends the 'gov.noaa.aviationweather.Station' event to the Kafka topic

        Args:
            _icao_id(str):  Value for placeholder icao_id in attribute subject
            data: (Station): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Station], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{icao_id}'
        """
        kafka_key = "{icao_id}".format(icao_id=_icao_id)
        attributes = {
             "type":"gov.noaa.aviationweather.Station",
             "source":"https://aviationweather.gov",
             "subject":"{icao_id}".format(icao_id = _icao_id)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_gov_noaa_aviationweather_metar(self,_icao_id : str, data: Metar, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Metar], str]=None) -> None:
        """
        Sends the 'gov.noaa.aviationweather.Metar' event to the Kafka topic

        Args:
            _icao_id(str):  Value for placeholder icao_id in attribute subject
            data: (Metar): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Metar], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{icao_id}'
        """
        kafka_key = "{icao_id}".format(icao_id=_icao_id)
        attributes = {
             "type":"gov.noaa.aviationweather.Metar",
             "source":"https://aviationweather.gov",
             "subject":"{icao_id}".format(icao_id = _icao_id)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_gov_noaa_aviationweather_sigmet(self,_icao_id : str, data: Sigmet, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Sigmet], str]=None) -> None:
        """
        Sends the 'gov.noaa.aviationweather.Sigmet' event to the Kafka topic

        Args:
            _icao_id(str):  Value for placeholder icao_id in attribute subject
            data: (Sigmet): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Sigmet], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{icao_id}'
        """
        kafka_key = "{icao_id}".format(icao_id=_icao_id)
        attributes = {
             "type":"gov.noaa.aviationweather.Sigmet",
             "source":"https://aviationweather.gov",
             "subject":"{icao_id}".format(icao_id = _icao_id)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper, kafka_key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()
