# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from ndw_road_traffic_producer_data import PointMeasurementSite
from ndw_road_traffic_producer_data import RouteMeasurementSite
from ndw_road_traffic_producer_data import TrafficObservation
from ndw_road_traffic_producer_data import TravelTimeObservation
from ndw_road_traffic_producer_data import DripSign
from ndw_road_traffic_producer_data import DripDisplayState
from ndw_road_traffic_producer_data import MsiSign
from ndw_road_traffic_producer_data import MsiDisplayState
from ndw_road_traffic_producer_data import Roadwork
from ndw_road_traffic_producer_data import BridgeOpening
from ndw_road_traffic_producer_data import TemporaryClosure
from ndw_road_traffic_producer_data import TemporarySpeedLimit
from ndw_road_traffic_producer_data import SafetyRelatedMessage

class NLNDWAVGEventProducer:
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

    def send_nl_ndw_avg_point_measurement_site(self,_measurement_site_id : str, data: PointMeasurementSite, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PointMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.PointMeasurementSite' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (PointMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PointMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.PointMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
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


    def send_nl_ndw_avg_route_measurement_site(self,_measurement_site_id : str, data: RouteMeasurementSite, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RouteMeasurementSite], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.RouteMeasurementSite' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (RouteMeasurementSite): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RouteMeasurementSite], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.RouteMeasurementSite",
             "source":"https://opendata.ndw.nu/measurement_current.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
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


    def send_nl_ndw_avg_traffic_observation(self,_measurement_site_id : str, data: TrafficObservation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TrafficObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TrafficObservation' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TrafficObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TrafficObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.TrafficObservation",
             "source":"https://opendata.ndw.nu/trafficspeed.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
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


    def send_nl_ndw_avg_travel_time_observation(self,_measurement_site_id : str, data: TravelTimeObservation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TravelTimeObservation], str]=None) -> None:
        """
        Sends the 'NL.NDW.AVG.TravelTimeObservation' event to the Kafka topic

        Args:
            _measurement_site_id(str):  Value for placeholder measurement_site_id in attribute subject
            data: (TravelTimeObservation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TravelTimeObservation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'measurement-sites/{measurement_site_id}'
        """
        kafka_key = "measurement-sites/{measurement_site_id}".format(measurement_site_id=_measurement_site_id)
        attributes = {
             "type":"NL.NDW.AVG.TravelTimeObservation",
             "source":"https://opendata.ndw.nu/traveltime.xml.gz",
             "subject":"measurement-sites/{measurement_site_id}".format(measurement_site_id = _measurement_site_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWAVGEventProducer':
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



class NLNDWDRIPEventProducer:
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

    def send_nl_ndw_drip_drip_sign(self,_vms_controller_id : str, _vms_index : str, data: DripSign, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripSign' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'drips/{vms_controller_id}/{vms_index}'
        """
        kafka_key = "drips/{vms_controller_id}/{vms_index}".format(vms_controller_id=_vms_controller_id, vms_index=_vms_index)
        attributes = {
             "type":"NL.NDW.DRIP.DripSign",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
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


    def send_nl_ndw_drip_drip_display_state(self,_vms_controller_id : str, _vms_index : str, data: DripDisplayState, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DripDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.DRIP.DripDisplayState' event to the Kafka topic

        Args:
            _vms_controller_id(str):  Value for placeholder vms_controller_id in attribute subject
            _vms_index(str):  Value for placeholder vms_index in attribute subject
            data: (DripDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DripDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'drips/{vms_controller_id}/{vms_index}'
        """
        kafka_key = "drips/{vms_controller_id}/{vms_index}".format(vms_controller_id=_vms_controller_id, vms_index=_vms_index)
        attributes = {
             "type":"NL.NDW.DRIP.DripDisplayState",
             "source":"https://opendata.ndw.nu/dynamische_route_informatie_paneel.xml.gz",
             "subject":"drips/{vms_controller_id}/{vms_index}".format(vms_controller_id = _vms_controller_id,vms_index = _vms_index)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWDRIPEventProducer':
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



class NLNDWMSIEventProducer:
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

    def send_nl_ndw_msi_msi_sign(self,_sign_id : str, data: MsiSign, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiSign], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiSign' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiSign): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiSign], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'msi-signs/{sign_id}'
        """
        kafka_key = "msi-signs/{sign_id}".format(sign_id=_sign_id)
        attributes = {
             "type":"NL.NDW.MSI.MsiSign",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
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


    def send_nl_ndw_msi_msi_display_state(self,_sign_id : str, data: MsiDisplayState, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MsiDisplayState], str]=None) -> None:
        """
        Sends the 'NL.NDW.MSI.MsiDisplayState' event to the Kafka topic

        Args:
            _sign_id(str):  Value for placeholder sign_id in attribute subject
            data: (MsiDisplayState): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MsiDisplayState], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'msi-signs/{sign_id}'
        """
        kafka_key = "msi-signs/{sign_id}".format(sign_id=_sign_id)
        attributes = {
             "type":"NL.NDW.MSI.MsiDisplayState",
             "source":"https://opendata.ndw.nu/Matrixsignaalinformatie.xml.gz",
             "subject":"msi-signs/{sign_id}".format(sign_id = _sign_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWMSIEventProducer':
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



class NLNDWSituationsEventProducer:
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

    def send_nl_ndw_situations_roadwork(self,_situation_record_id : str, data: Roadwork, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Roadwork], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.Roadwork' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (Roadwork): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Roadwork], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.Roadwork",
             "source":"https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
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


    def send_nl_ndw_situations_bridge_opening(self,_situation_record_id : str, data: BridgeOpening, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BridgeOpening], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.BridgeOpening' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (BridgeOpening): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BridgeOpening], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.BridgeOpening",
             "source":"https://opendata.ndw.nu/planningsfeed_brugopeningen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
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


    def send_nl_ndw_situations_temporary_closure(self,_situation_record_id : str, data: TemporaryClosure, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporaryClosure], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporaryClosure' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporaryClosure): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporaryClosure], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.TemporaryClosure",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
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


    def send_nl_ndw_situations_temporary_speed_limit(self,_situation_record_id : str, data: TemporarySpeedLimit, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TemporarySpeedLimit], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.TemporarySpeedLimit' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (TemporarySpeedLimit): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TemporarySpeedLimit], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.TemporarySpeedLimit",
             "source":"https://opendata.ndw.nu/tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
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


    def send_nl_ndw_situations_safety_related_message(self,_situation_record_id : str, data: SafetyRelatedMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SafetyRelatedMessage], str]=None) -> None:
        """
        Sends the 'NL.NDW.Situations.SafetyRelatedMessage' event to the Kafka topic

        Args:
            _situation_record_id(str):  Value for placeholder situation_record_id in attribute subject
            data: (SafetyRelatedMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SafetyRelatedMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration 'situations/{situation_record_id}'
        """
        kafka_key = "situations/{situation_record_id}".format(situation_record_id=_situation_record_id)
        attributes = {
             "type":"NL.NDW.Situations.SafetyRelatedMessage",
             "source":"https://opendata.ndw.nu/veiligheidsgerelateerde_berichten_srti.xml.gz",
             "subject":"situations/{situation_record_id}".format(situation_record_id = _situation_record_id)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'NLNDWSituationsEventProducer':
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

