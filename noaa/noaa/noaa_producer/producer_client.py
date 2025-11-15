# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from noaa.noaa_producer.microsoft.opendata.us.noaa.waterlevel import WaterLevel
from noaa.noaa_producer.microsoft.opendata.us.noaa.predictions import Predictions
from noaa.noaa_producer.microsoft.opendata.us.noaa.airpressure import AirPressure
from noaa.noaa_producer.microsoft.opendata.us.noaa.airtemperature import AirTemperature
from noaa.noaa_producer.microsoft.opendata.us.noaa.watertemperature import WaterTemperature
from noaa.noaa_producer.microsoft.opendata.us.noaa.wind import Wind
from noaa.noaa_producer.microsoft.opendata.us.noaa.humidity import Humidity
from noaa.noaa_producer.microsoft.opendata.us.noaa.conductivity import Conductivity
from noaa.noaa_producer.microsoft.opendata.us.noaa.salinity import Salinity
from noaa.noaa_producer.microsoft.opendata.us.noaa.station import Station
from noaa.noaa_producer.microsoft.opendata.us.noaa.visibility import Visibility

class MicrosoftOpenDataUSNOAAEventProducer:
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

    def send_microsoft_open_data_us_noaa_water_level(self,data: WaterLevel, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterLevel], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.WaterLevel' event to the Kafka topic

        Args:
            data: (WaterLevel): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterLevel], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterLevel"
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


    def send_microsoft_open_data_us_noaa_predictions(self,data: Predictions, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Predictions], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Predictions' event to the Kafka topic

        Args:
            data: (Predictions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Predictions], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Predictions"
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


    def send_microsoft_open_data_us_noaa_air_pressure(self,data: AirPressure, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirPressure], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.AirPressure' event to the Kafka topic

        Args:
            data: (AirPressure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirPressure], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirPressure"
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


    def send_microsoft_open_data_us_noaa_air_temperature(self,data: AirTemperature, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AirTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.AirTemperature' event to the Kafka topic

        Args:
            data: (AirTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AirTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.AirTemperature"
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


    def send_microsoft_open_data_us_noaa_water_temperature(self,data: WaterTemperature, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WaterTemperature], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.WaterTemperature' event to the Kafka topic

        Args:
            data: (WaterTemperature): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WaterTemperature], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.WaterTemperature"
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


    def send_microsoft_open_data_us_noaa_wind(self,data: Wind, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Wind], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Wind' event to the Kafka topic

        Args:
            data: (Wind): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Wind], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Wind"
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


    def send_microsoft_open_data_us_noaa_humidity(self,data: Humidity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Humidity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Humidity' event to the Kafka topic

        Args:
            data: (Humidity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Humidity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Humidity"
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


    def send_microsoft_open_data_us_noaa_conductivity(self,data: Conductivity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Conductivity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Conductivity' event to the Kafka topic

        Args:
            data: (Conductivity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Conductivity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Conductivity"
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


    def send_microsoft_open_data_us_noaa_salinity(self,data: Salinity, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Salinity], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Salinity' event to the Kafka topic

        Args:
            data: (Salinity): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Salinity], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Salinity"
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


    def send_microsoft_open_data_us_noaa_station(self,data: Station, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Station], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Station' event to the Kafka topic

        Args:
            data: (Station): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Station], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Station"
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


    def send_microsoft_open_data_us_noaa_visibility(self,_datacontenttype: str, _subject: str, _time: str, _dataschema: str, data: Visibility, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Visibility], str]=None) -> None:
        """
        Sends the 'Microsoft.OpenData.US.NOAA.Visibility' event to the Kafka topic

        Args:
            _datacontenttype(str) : CloudEvents attribute 'datacontenttype'
            _subject(str) : CloudEvents attribute 'subject'
            _time(str) : CloudEvents attribute 'time'
            _dataschema(str) : CloudEvents attribute 'dataschema'
            data: (Visibility): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Visibility], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "type":"Microsoft.OpenData.US.NOAA.Visibility",
             "datacontenttype":_datacontenttype,
             "subject":_subject,
             "time":_time,
             "dataschema":_dataschema
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'MicrosoftOpenDataUSNOAAEventProducer':
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

