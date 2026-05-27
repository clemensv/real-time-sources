# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from dmi_producer_data import MetObsStation
from dmi_producer_data import MetObsObservation
from dmi_producer_data import OceanStation
from dmi_producer_data import TidewaterStation
from dmi_producer_data import OceanObservation
from dmi_producer_data import TidewaterPrediction
from dmi_producer_data import LightningSensor
from dmi_producer_data import LightningStrike

class DkDmiMetObsKafkaEventProducer:
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

    def send_dk_dmi_met_obs_kafka_station(self,_feedurl : str, _station_id : str, data: MetObsStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MetObsStation], str]=None) -> None:
        """
        Sends the 'dk.dmi.metObs.kafka.Station' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (MetObsStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MetObsStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"dk.dmi.metObs.MetObsStation",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_dk_dmi_met_obs_kafka_observation(self,_feedurl : str, _station_id : str, _parameter_id : str, data: MetObsObservation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MetObsObservation], str]=None) -> None:
        """
        Sends the 'dk.dmi.metObs.kafka.Observation' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _station_id(str):  Value for placeholder station_id in attribute subject
            _parameter_id(str):  Value for placeholder parameter_id in attribute subject
            data: (MetObsObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MetObsObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}/{parameter_id}'
        """
        kafka_key = "{station_id}/{parameter_id}".format(station_id=_station_id, parameter_id=_parameter_id)
        attributes = {
             "type":"dk.dmi.metObs.MetObsObservation",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{station_id}/{parameter_id}".format(station_id = _station_id,parameter_id = _parameter_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'DkDmiMetObsKafkaEventProducer':
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



class DkDmiOceanObsKafkaEventProducer:
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

    def send_dk_dmi_ocean_obs_kafka_station(self,_feedurl : str, _station_id : str, data: OceanStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, OceanStation], str]=None) -> None:
        """
        Sends the 'dk.dmi.oceanObs.kafka.Station' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (OceanStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, OceanStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"dk.dmi.oceanObs.OceanStation",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_dk_dmi_ocean_obs_kafka_tidewater_station(self,_feedurl : str, _station_id : str, data: TidewaterStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TidewaterStation], str]=None) -> None:
        """
        Sends the 'dk.dmi.oceanObs.kafka.TidewaterStation' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (TidewaterStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TidewaterStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"dk.dmi.oceanObs.TidewaterStation",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{station_id}".format(station_id = _station_id)
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


    def send_dk_dmi_ocean_obs_kafka_observation(self,_feedurl : str, _station_id : str, _parameter_id : str, data: OceanObservation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, OceanObservation], str]=None) -> None:
        """
        Sends the 'dk.dmi.oceanObs.kafka.Observation' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _station_id(str):  Value for placeholder station_id in attribute subject
            _parameter_id(str):  Value for placeholder parameter_id in attribute subject
            data: (OceanObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, OceanObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}/{parameter_id}'
        """
        kafka_key = "{station_id}/{parameter_id}".format(station_id=_station_id, parameter_id=_parameter_id)
        attributes = {
             "type":"dk.dmi.oceanObs.OceanObservation",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{station_id}/{parameter_id}".format(station_id = _station_id,parameter_id = _parameter_id)
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


    def send_dk_dmi_ocean_obs_kafka_tidewater_prediction(self,_feedurl : str, _station_id : str, data: TidewaterPrediction, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TidewaterPrediction], str]=None) -> None:
        """
        Sends the 'dk.dmi.oceanObs.kafka.TidewaterPrediction' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _station_id(str):  Value for placeholder station_id in attribute subject
            data: (TidewaterPrediction): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TidewaterPrediction], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}'
        """
        kafka_key = "{station_id}".format(station_id=_station_id)
        attributes = {
             "type":"dk.dmi.oceanObs.TidewaterPrediction",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{station_id}".format(station_id = _station_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'DkDmiOceanObsKafkaEventProducer':
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



class DkDmiLightningKafkaEventProducer:
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

    def send_dk_dmi_lightning_kafka_sensor(self,_feedurl : str, _sensor_id : str, data: LightningSensor, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LightningSensor], str]=None) -> None:
        """
        Sends the 'dk.dmi.lightning.kafka.Sensor' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _sensor_id(str):  Value for placeholder sensor_id in attribute subject
            data: (LightningSensor): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LightningSensor], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{sensor_id}'
        """
        kafka_key = "{sensor_id}".format(sensor_id=_sensor_id)
        attributes = {
             "type":"dk.dmi.lightning.LightningSensor",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{sensor_id}".format(sensor_id = _sensor_id)
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


    def send_dk_dmi_lightning_kafka_strike(self,_feedurl : str, _strike_id : str, data: LightningStrike, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LightningStrike], str]=None) -> None:
        """
        Sends the 'dk.dmi.lightning.kafka.Strike' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _strike_id(str):  Value for placeholder strike_id in attribute subject
            data: (LightningStrike): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LightningStrike], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{strike_id}'
        """
        kafka_key = "{strike_id}".format(strike_id=_strike_id)
        attributes = {
             "type":"dk.dmi.lightning.LightningStrike",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{strike_id}".format(strike_id = _strike_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'DkDmiLightningKafkaEventProducer':
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

