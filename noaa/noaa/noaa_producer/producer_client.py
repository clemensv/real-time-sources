# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
from typing import cast
import uuid
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from .microsoft.opendata.us.noaa.waterlevel import WaterLevel
from .microsoft.opendata.us.noaa.predictions import Predictions
from .microsoft.opendata.us.noaa.airpressure import AirPressure
from .microsoft.opendata.us.noaa.airtemperature import AirTemperature
from .microsoft.opendata.us.noaa.watertemperature import WaterTemperature
from .microsoft.opendata.us.noaa.wind import Wind
from .microsoft.opendata.us.noaa.humidity import Humidity
from .microsoft.opendata.us.noaa.conductivity import Conductivity
from .microsoft.opendata.us.noaa.salinity import Salinity
from .microsoft.opendata.us.noaa.station import Station
from .microsoft.opendata.us.noaa.visibility import Visibility
import dataclasses_json
import dataclasses

class MicrosoftOpendataUsNoaaEventProducer:
    def __init__(self, kafka_config, topic, content_mode='structured'):
        """ init """
        self.producer = Producer(kafka_config)
        self.topic = topic
        self.content_mode = content_mode
    
    def __key_mapper(self, x: CloudEvent) -> str:
        return f'{str(x.get("type"))}:{str(x.get("source"))}{("-"+str(x.get("subject"))) if x.get("subject") else ""}'

    
    def send_microsoft_opendata_us_noaa_waterlevel(self, data:WaterLevel, station:str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_waterlevel """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.WaterLevel",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event, key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_predictions(self, data:Predictions, station: str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_predictions """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.Predictions",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_airpressure(self, data:AirPressure, station: str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_airpressure """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.AirPressure",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_airtemperature(self, data:AirTemperature, station:str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_airtemperature """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.AirTemperature",            
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_watertemperature(self, data:WaterTemperature, station: str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_watertemperature """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.WaterTemperature",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_wind(self, data:Wind, station: str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_wind """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.Wind",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_humidity(self, data:Humidity, station:str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_humidity """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.Humidity",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_conductivity(self, data:Conductivity, station:str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_conductivity """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.Conductivity",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_salinity(self, data:Salinity, station:str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_salinity """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.Salinity",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_station(self, data:Station, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_station """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.Station",
            "source":"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event, key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

    def send_microsoft_opendata_us_noaa_visibility(self, data:Visibility,station:str, flush_producer:bool=True) -> None:
        """ send_microsoft_opendata_us_noaa_visibility """
        attributes = {
            "type":"Microsoft.OpenData.US.NOAA.Visibility",
            "source": f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station}.json"
        }
        event = CloudEvent.create(attributes, json.loads(data.to_json()))        
        if self.content_mode == "structured":
            message = to_structured(event,  key_mapper=self.__key_mapper)            
            message.headers["content-type"] = "application/cloudevents+json".encode("utf-8")
        else:
            content_type = "application/json"
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
            message.headers["content-type"] = content_type.encode("utf-8")
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

