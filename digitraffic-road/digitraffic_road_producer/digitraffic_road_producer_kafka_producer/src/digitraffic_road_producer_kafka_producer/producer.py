# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from digitraffic_road_producer_data import TmsSensorData
from digitraffic_road_producer_data import WeatherSensorData
from digitraffic_road_producer_data import TrafficMessage
from digitraffic_road_producer_data import MaintenanceTracking

class FiDigitrafficRoadSensorsEventProducer:
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

    def send_fi_digitraffic_road_sensors_tms_sensor_data(self,_station_id : str, _sensor_id : str, data: TmsSensorData, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TmsSensorData], str]=None) -> None:
        """
        Sends the 'fi.digitraffic.road.sensors.TmsSensorData' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            _sensor_id(str):  Value for placeholder sensor_id in attribute subject
            data: (TmsSensorData): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TmsSensorData], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}/{sensor_id}'
        """
        kafka_key = "{station_id}/{sensor_id}".format(station_id=_station_id, sensor_id=_sensor_id)
        attributes = {
             "type":"fi.digitraffic.road.sensors.TmsSensorData",
             "source":"wss://tie.digitraffic.fi/mqtt",
             "subject":"{station_id}/{sensor_id}".format(station_id = _station_id,sensor_id = _sensor_id)
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


    def send_fi_digitraffic_road_sensors_weather_sensor_data(self,_station_id : str, _sensor_id : str, data: WeatherSensorData, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WeatherSensorData], str]=None) -> None:
        """
        Sends the 'fi.digitraffic.road.sensors.WeatherSensorData' event to the Kafka topic

        Args:
            _station_id(str):  Value for placeholder station_id in attribute subject
            _sensor_id(str):  Value for placeholder sensor_id in attribute subject
            data: (WeatherSensorData): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WeatherSensorData], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{station_id}/{sensor_id}'
        """
        kafka_key = "{station_id}/{sensor_id}".format(station_id=_station_id, sensor_id=_sensor_id)
        attributes = {
             "type":"fi.digitraffic.road.sensors.WeatherSensorData",
             "source":"wss://tie.digitraffic.fi/mqtt",
             "subject":"{station_id}/{sensor_id}".format(station_id = _station_id,sensor_id = _sensor_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'FiDigitrafficRoadSensorsEventProducer':
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



class FiDigitrafficRoadMessagesEventProducer:
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

    def send_fi_digitraffic_road_messages_traffic_announcement(self,_situation_id : str, data: TrafficMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficMessage], str]=None) -> None:
        """
        Sends the 'fi.digitraffic.road.messages.TrafficAnnouncement' event to the Kafka topic

        Args:
            _situation_id(str):  Value for placeholder situation_id in attribute subject
            data: (TrafficMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{situation_id}'
        """
        kafka_key = "{situation_id}".format(situation_id=_situation_id)
        attributes = {
             "type":"fi.digitraffic.road.messages.TrafficAnnouncement",
             "source":"wss://tie.digitraffic.fi/mqtt",
             "subject":"{situation_id}".format(situation_id = _situation_id)
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


    def send_fi_digitraffic_road_messages_road_work(self,_situation_id : str, data: TrafficMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficMessage], str]=None) -> None:
        """
        Sends the 'fi.digitraffic.road.messages.RoadWork' event to the Kafka topic

        Args:
            _situation_id(str):  Value for placeholder situation_id in attribute subject
            data: (TrafficMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{situation_id}'
        """
        kafka_key = "{situation_id}".format(situation_id=_situation_id)
        attributes = {
             "type":"fi.digitraffic.road.messages.RoadWork",
             "source":"wss://tie.digitraffic.fi/mqtt",
             "subject":"{situation_id}".format(situation_id = _situation_id)
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


    def send_fi_digitraffic_road_messages_weight_restriction(self,_situation_id : str, data: TrafficMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficMessage], str]=None) -> None:
        """
        Sends the 'fi.digitraffic.road.messages.WeightRestriction' event to the Kafka topic

        Args:
            _situation_id(str):  Value for placeholder situation_id in attribute subject
            data: (TrafficMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{situation_id}'
        """
        kafka_key = "{situation_id}".format(situation_id=_situation_id)
        attributes = {
             "type":"fi.digitraffic.road.messages.WeightRestriction",
             "source":"wss://tie.digitraffic.fi/mqtt",
             "subject":"{situation_id}".format(situation_id = _situation_id)
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


    def send_fi_digitraffic_road_messages_exempted_transport(self,_situation_id : str, data: TrafficMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficMessage], str]=None) -> None:
        """
        Sends the 'fi.digitraffic.road.messages.ExemptedTransport' event to the Kafka topic

        Args:
            _situation_id(str):  Value for placeholder situation_id in attribute subject
            data: (TrafficMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{situation_id}'
        """
        kafka_key = "{situation_id}".format(situation_id=_situation_id)
        attributes = {
             "type":"fi.digitraffic.road.messages.ExemptedTransport",
             "source":"wss://tie.digitraffic.fi/mqtt",
             "subject":"{situation_id}".format(situation_id = _situation_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'FiDigitrafficRoadMessagesEventProducer':
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



class FiDigitrafficRoadMaintenanceEventProducer:
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

    def send_fi_digitraffic_road_maintenance_maintenance_tracking(self,_domain : str, data: MaintenanceTracking, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MaintenanceTracking], str]=None) -> None:
        """
        Sends the 'fi.digitraffic.road.maintenance.MaintenanceTracking' event to the Kafka topic

        Args:
            _domain(str):  Value for placeholder domain in attribute subject
            data: (MaintenanceTracking): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MaintenanceTracking], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{domain}'
        """
        kafka_key = "{domain}".format(domain=_domain)
        attributes = {
             "type":"fi.digitraffic.road.maintenance.MaintenanceTracking",
             "source":"wss://tie.digitraffic.fi/mqtt",
             "subject":"{domain}".format(domain = _domain)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'FiDigitrafficRoadMaintenanceEventProducer':
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

