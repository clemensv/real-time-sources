# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from rws_waterwebservices.rws_waterwebservices_producer.nl.rws.waterwebservices.station import Station
from rws_waterwebservices.rws_waterwebservices_producer.nl.rws.waterwebservices.water_level_observation import WaterLevelObservation

class NLRWSWaterwebservicesEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode:typing.Literal['structured','binary']='structured'):
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    def __key_mapper(self, x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str]) -> str:
        if key_mapper:
            return key_mapper(x, m)
        else:
            return f'{str(x.get("type"))}:{str(x.get("source"))}{("-"+str(x.get("subject"))) if x.get("subject") else ""}'

    def send_nl_rws_waterwebservices_station(self, data: Station, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Station], str]=None) -> None:
        attributes = {
             "type":"NL.RWS.Waterwebservices.Station",
             "source":"https://waterwebservices.rijkswaterstaat.nl"
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_nl_rws_waterwebservices_water_level_observation(self, data: WaterLevelObservation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterLevelObservation], str]=None) -> None:
        attributes = {
             "type":"NL.RWS.Waterwebservices.WaterLevelObservation",
             "source":"https://waterwebservices.rijkswaterstaat.nl"
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()
