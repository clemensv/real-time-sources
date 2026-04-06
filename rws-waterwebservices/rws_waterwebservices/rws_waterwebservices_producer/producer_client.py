# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import re
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

    def __key_mapper(self, x: CloudEvent, m: typing.Any, key_mapper: typing.Callable[[CloudEvent, typing.Any], str], default_key: typing.Optional[str] = None) -> typing.Optional[str]:
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
    def __resolve_template(template: str, data: typing.Any) -> str:
        if hasattr(data, "to_serializer_dict"):
            serialized = data.to_serializer_dict()
        elif isinstance(data, dict):
            serialized = data
        else:
            serialized = dict(getattr(data, "__dict__", {}))

        normalized = {}
        for key, value in serialized.items():
            normalized[key] = value
            normalized[key.lower()] = value
            normalized[key.replace("_", "").replace("-", "").lower()] = value

        def replace(match: re.Match[str]) -> str:
            placeholder = match.group(1)
            candidates = (
                placeholder,
                placeholder.lower(),
                placeholder.replace("_", "").replace("-", "").lower(),
            )
            for candidate in candidates:
                if candidate in normalized:
                    return str(normalized[candidate])
            if placeholder.lower() == "station_code":
                if "code" in normalized:
                    return str(normalized["code"])
                if "location_code" in normalized:
                    return str(normalized["location_code"])
            raise KeyError(f"Could not resolve placeholder '{placeholder}' for {type(data).__name__}")

        return re.sub(r"{([^{}]+)}", replace, template)

    def send_nl_rws_waterwebservices_station(self, data: Station, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Station], str]=None) -> None:
        kafka_key = self.__resolve_template("{station_code}", data)
        attributes = {
             "type":"NL.RWS.Waterwebservices.Station",
             "source":"https://waterwebservices.rijkswaterstaat.nl",

             "subject":self.__resolve_template("{station_code}", data)
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
    def send_nl_rws_waterwebservices_water_level_observation(self, data: WaterLevelObservation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterLevelObservation], str]=None) -> None:
        kafka_key = self.__resolve_template("{station_code}", data)
        attributes = {
             "type":"NL.RWS.Waterwebservices.WaterLevelObservation",
             "source":"https://waterwebservices.rijkswaterstaat.nl",

             "subject":self.__resolve_template("{station_code}", data)
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
