# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from entsoe_producer_data import DayAheadPrices
from entsoe_producer_data import ActualTotalLoad
from entsoe_producer_data import LoadForecastMargin
from entsoe_producer_data import GenerationForecast
from entsoe_producer_data import ReservoirFillingInformation
from entsoe_producer_data import ActualGeneration
from entsoe_producer_data import ActualGenerationPerType
from entsoe_producer_data import WindSolarForecast
from entsoe_producer_data import WindSolarGeneration
from entsoe_producer_data import InstalledGenerationCapacityPerType
from entsoe_producer_data import CrossBorderPhysicalFlows

class EuEntsoeTransparencyByDomainEventProducer:
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

    def send_eu_entsoe_transparency_day_ahead_prices(self,_in_domain : str, data: DayAheadPrices, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DayAheadPrices], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.DayAheadPrices' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            data: (DayAheadPrices): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DayAheadPrices], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}'
        """
        kafka_key = "{inDomain}".format(inDomain=_in_domain)
        attributes = {
             "type":"eu.entsoe.transparency.DayAheadPrices",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}".format(inDomain = _in_domain)
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


    def send_eu_entsoe_transparency_actual_total_load(self,_in_domain : str, data: ActualTotalLoad, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ActualTotalLoad], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.ActualTotalLoad' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            data: (ActualTotalLoad): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ActualTotalLoad], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}'
        """
        kafka_key = "{inDomain}".format(inDomain=_in_domain)
        attributes = {
             "type":"eu.entsoe.transparency.ActualTotalLoad",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}".format(inDomain = _in_domain)
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


    def send_eu_entsoe_transparency_load_forecast_margin(self,_in_domain : str, data: LoadForecastMargin, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LoadForecastMargin], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.LoadForecastMargin' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            data: (LoadForecastMargin): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LoadForecastMargin], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}'
        """
        kafka_key = "{inDomain}".format(inDomain=_in_domain)
        attributes = {
             "type":"eu.entsoe.transparency.LoadForecastMargin",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}".format(inDomain = _in_domain)
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


    def send_eu_entsoe_transparency_generation_forecast(self,_in_domain : str, data: GenerationForecast, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GenerationForecast], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.GenerationForecast' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            data: (GenerationForecast): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GenerationForecast], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}'
        """
        kafka_key = "{inDomain}".format(inDomain=_in_domain)
        attributes = {
             "type":"eu.entsoe.transparency.GenerationForecast",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}".format(inDomain = _in_domain)
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


    def send_eu_entsoe_transparency_reservoir_filling_information(self,_in_domain : str, data: ReservoirFillingInformation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ReservoirFillingInformation], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.ReservoirFillingInformation' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            data: (ReservoirFillingInformation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ReservoirFillingInformation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}'
        """
        kafka_key = "{inDomain}".format(inDomain=_in_domain)
        attributes = {
             "type":"eu.entsoe.transparency.ReservoirFillingInformation",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}".format(inDomain = _in_domain)
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


    def send_eu_entsoe_transparency_actual_generation(self,_in_domain : str, data: ActualGeneration, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ActualGeneration], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.ActualGeneration' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            data: (ActualGeneration): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ActualGeneration], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}'
        """
        kafka_key = "{inDomain}".format(inDomain=_in_domain)
        attributes = {
             "type":"eu.entsoe.transparency.ActualGeneration",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}".format(inDomain = _in_domain)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'EuEntsoeTransparencyByDomainEventProducer':
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



class EuEntsoeTransparencyByDomainPsrTypeEventProducer:
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

    def send_eu_entsoe_transparency_actual_generation_per_type(self,_in_domain : str, _psr_type : str, data: ActualGenerationPerType, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ActualGenerationPerType], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.ActualGenerationPerType' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            _psr_type(str):  Value for placeholder psrType in attribute subject
            data: (ActualGenerationPerType): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ActualGenerationPerType], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}/{psrType}'
        """
        kafka_key = "{inDomain}/{psrType}".format(inDomain=_in_domain, psrType=_psr_type)
        attributes = {
             "type":"eu.entsoe.transparency.ActualGenerationPerType",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}/{psrType}".format(inDomain = _in_domain,psrType = _psr_type)
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


    def send_eu_entsoe_transparency_wind_solar_forecast(self,_in_domain : str, _psr_type : str, data: WindSolarForecast, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindSolarForecast], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.WindSolarForecast' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            _psr_type(str):  Value for placeholder psrType in attribute subject
            data: (WindSolarForecast): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindSolarForecast], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}/{psrType}'
        """
        kafka_key = "{inDomain}/{psrType}".format(inDomain=_in_domain, psrType=_psr_type)
        attributes = {
             "type":"eu.entsoe.transparency.WindSolarForecast",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}/{psrType}".format(inDomain = _in_domain,psrType = _psr_type)
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


    def send_eu_entsoe_transparency_wind_solar_generation(self,_in_domain : str, _psr_type : str, data: WindSolarGeneration, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WindSolarGeneration], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.WindSolarGeneration' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            _psr_type(str):  Value for placeholder psrType in attribute subject
            data: (WindSolarGeneration): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WindSolarGeneration], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}/{psrType}'
        """
        kafka_key = "{inDomain}/{psrType}".format(inDomain=_in_domain, psrType=_psr_type)
        attributes = {
             "type":"eu.entsoe.transparency.WindSolarGeneration",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}/{psrType}".format(inDomain = _in_domain,psrType = _psr_type)
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


    def send_eu_entsoe_transparency_installed_generation_capacity_per_type(self,_in_domain : str, _psr_type : str, data: InstalledGenerationCapacityPerType, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, InstalledGenerationCapacityPerType], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.InstalledGenerationCapacityPerType' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            _psr_type(str):  Value for placeholder psrType in attribute subject
            data: (InstalledGenerationCapacityPerType): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, InstalledGenerationCapacityPerType], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}/{psrType}'
        """
        kafka_key = "{inDomain}/{psrType}".format(inDomain=_in_domain, psrType=_psr_type)
        attributes = {
             "type":"eu.entsoe.transparency.InstalledGenerationCapacityPerType",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}/{psrType}".format(inDomain = _in_domain,psrType = _psr_type)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'EuEntsoeTransparencyByDomainPsrTypeEventProducer':
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



class EuEntsoeTransparencyCrossBorderEventProducer:
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

    def send_eu_entsoe_transparency_cross_border_physical_flows(self,_in_domain : str, _out_domain : str, data: CrossBorderPhysicalFlows, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, CrossBorderPhysicalFlows], str]=None) -> None:
        """
        Sends the 'eu.entsoe.transparency.CrossBorderPhysicalFlows' event to the Kafka topic

        Args:
            _in_domain(str):  Value for placeholder inDomain in attribute subject
            _out_domain(str):  Value for placeholder outDomain in attribute subject
            data: (CrossBorderPhysicalFlows): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, CrossBorderPhysicalFlows], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{inDomain}/{outDomain}'
        """
        kafka_key = "{inDomain}/{outDomain}".format(inDomain=_in_domain, outDomain=_out_domain)
        attributes = {
             "type":"eu.entsoe.transparency.CrossBorderPhysicalFlows",
             "source":"https://transparency.entsoe.eu/api",
             "subject":"{inDomain}/{outDomain}".format(inDomain = _in_domain,outDomain = _out_domain)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'EuEntsoeTransparencyCrossBorderEventProducer':
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

