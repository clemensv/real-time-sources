# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicleposition import VehiclePosition
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripupdate import TripUpdate
from gtfs_rt_producer_data.generaltransitfeed.alert.alert import Alert
from gtfs_rt_producer_data.generaltransitfeedstatic.agency import Agency
from gtfs_rt_producer_data.generaltransitfeedstatic.areas import Areas
from gtfs_rt_producer_data.generaltransitfeedstatic.attributions import Attributions
from gtfs_rt_producer_data.generaltransitfeedstatic.bookingrules import BookingRules
from gtfs_rt_producer_data.generaltransitfeedstatic.fareattributes import FareAttributes
from gtfs_rt_producer_data.generaltransitfeedstatic.farelegrules import FareLegRules
from gtfs_rt_producer_data.generaltransitfeedstatic.faremedia import FareMedia
from gtfs_rt_producer_data.generaltransitfeedstatic.fareproducts import FareProducts
from gtfs_rt_producer_data.generaltransitfeedstatic.farerules import FareRules
from gtfs_rt_producer_data.generaltransitfeedstatic.faretransferrules import FareTransferRules
from gtfs_rt_producer_data.generaltransitfeedstatic.feedinfo import FeedInfo
from gtfs_rt_producer_data.generaltransitfeedstatic.frequencies import Frequencies
from gtfs_rt_producer_data.generaltransitfeedstatic.levels import Levels
from gtfs_rt_producer_data.generaltransitfeedstatic.locationgeojson import LocationGeoJson
from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroups import LocationGroups
from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroupstores import LocationGroupStores
from gtfs_rt_producer_data.generaltransitfeedstatic.networks import Networks
from gtfs_rt_producer_data.generaltransitfeedstatic.pathways import Pathways
from gtfs_rt_producer_data.generaltransitfeedstatic.routenetworks import RouteNetworks
from gtfs_rt_producer_data.generaltransitfeedstatic.routes import Routes
from gtfs_rt_producer_data.generaltransitfeedstatic.shapes import Shapes
from gtfs_rt_producer_data.generaltransitfeedstatic.stopareas import StopAreas
from gtfs_rt_producer_data.generaltransitfeedstatic.stops import Stops
from gtfs_rt_producer_data.generaltransitfeedstatic.stoptimes import StopTimes
from gtfs_rt_producer_data.generaltransitfeedstatic.timeframes import Timeframes
from gtfs_rt_producer_data.generaltransitfeedstatic.transfers import Transfers
from gtfs_rt_producer_data.generaltransitfeedstatic.translations import Translations
from gtfs_rt_producer_data.generaltransitfeedstatic.trips import Trips

class GeneralTransitFeedRealTimeEventProducer:
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

    async def send_general_transit_feed_real_time_vehicle_position(self,_feedurl : str, _agencyid : str, data: VehiclePosition, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, VehiclePosition], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.RealTime.VehiclePosition' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (VehiclePosition): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, VehiclePosition], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.RealTime.VehiclePosition",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedRealTimeEventProducer':
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


    async def send_general_transit_feed_real_time_trip_update(self,_feedurl : str, _agencyid : str, data: TripUpdate, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, TripUpdate], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.RealTime.TripUpdate' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (TripUpdate): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, TripUpdate], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.RealTime.TripUpdate",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedRealTimeEventProducer':
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


    async def send_general_transit_feed_real_time_alert(self,_feedurl : str, _agencyid : str, data: Alert, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Alert], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.RealTime.Alert' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Alert): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Alert], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.RealTime.Alert",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedRealTimeEventProducer':
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



class GeneralTransitFeedStaticEventProducer:
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

    async def send_general_transit_feed_static_agency(self,_feedurl : str, _agencyid : str, data: Agency, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Agency], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Agency' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Agency): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Agency], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Agency",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_areas(self,_feedurl : str, _agencyid : str, data: Areas, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Areas], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Areas' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Areas): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Areas], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Areas",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_attributions(self,_feedurl : str, _agencyid : str, data: Attributions, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Attributions], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Attributions' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Attributions): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Attributions], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Attributions",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_booking_rules(self,_feedurl : str, _agencyid : str, data: BookingRules, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BookingRules], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.BookingRules' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (BookingRules): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BookingRules], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.BookingRules",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_fare_attributes(self,_feedurl : str, _agencyid : str, data: FareAttributes, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FareAttributes], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.FareAttributes' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (FareAttributes): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FareAttributes], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.FareAttributes",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_fare_leg_rules(self,_feedurl : str, _agencyid : str, data: FareLegRules, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FareLegRules], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.FareLegRules' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (FareLegRules): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FareLegRules], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.FareLegRules",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_fare_media(self,_feedurl : str, _agencyid : str, data: FareMedia, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FareMedia], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.FareMedia' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (FareMedia): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FareMedia], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.FareMedia",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_fare_products(self,_feedurl : str, _agencyid : str, data: FareProducts, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FareProducts], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.FareProducts' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (FareProducts): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FareProducts], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.FareProducts",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_fare_rules(self,_feedurl : str, _agencyid : str, data: FareRules, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FareRules], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.FareRules' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (FareRules): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FareRules], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.FareRules",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_fare_transfer_rules(self,_feedurl : str, _agencyid : str, data: FareTransferRules, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FareTransferRules], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.FareTransferRules' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (FareTransferRules): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FareTransferRules], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.FareTransferRules",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_feed_info(self,_feedurl : str, _agencyid : str, data: FeedInfo, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, FeedInfo], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.FeedInfo' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (FeedInfo): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, FeedInfo], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.FeedInfo",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_frequencies(self,_feedurl : str, _agencyid : str, data: Frequencies, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Frequencies], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Frequencies' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Frequencies): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Frequencies], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Frequencies",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_levels(self,_feedurl : str, _agencyid : str, data: Levels, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Levels], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Levels' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Levels): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Levels], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Levels",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_location_geo_json(self,_feedurl : str, _agencyid : str, data: LocationGeoJson, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LocationGeoJson], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.LocationGeoJson' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (LocationGeoJson): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LocationGeoJson], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.LocationGeoJson",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_location_groups(self,_feedurl : str, _agencyid : str, data: LocationGroups, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LocationGroups], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.LocationGroups' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (LocationGroups): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LocationGroups], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.LocationGroups",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_location_group_stores(self,_feedurl : str, _agencyid : str, data: LocationGroupStores, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LocationGroupStores], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.LocationGroupStores' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (LocationGroupStores): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LocationGroupStores], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.LocationGroupStores",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_networks(self,_feedurl : str, _agencyid : str, data: Networks, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Networks], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Networks' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Networks): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Networks], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Networks",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_pathways(self,_feedurl : str, _agencyid : str, data: Pathways, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Pathways], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Pathways' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Pathways): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Pathways], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Pathways",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_route_networks(self,_feedurl : str, _agencyid : str, data: RouteNetworks, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RouteNetworks], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.RouteNetworks' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (RouteNetworks): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RouteNetworks], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.RouteNetworks",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_routes(self,_feedurl : str, _agencyid : str, data: Routes, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Routes], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Routes' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Routes): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Routes], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Routes",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_shapes(self,_feedurl : str, _agencyid : str, data: Shapes, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Shapes], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Shapes' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Shapes): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Shapes], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Shapes",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_stop_areas(self,_feedurl : str, _agencyid : str, data: StopAreas, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, StopAreas], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.StopAreas' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (StopAreas): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, StopAreas], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.StopAreas",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_stops(self,_feedurl : str, _agencyid : str, data: Stops, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Stops], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Stops' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Stops): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Stops], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Stops",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_stop_times(self,_feedurl : str, _agencyid : str, data: StopTimes, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, StopTimes], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.StopTimes' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (StopTimes): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, StopTimes], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.StopTimes",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_timeframes(self,_feedurl : str, _agencyid : str, data: Timeframes, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Timeframes], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Timeframes' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Timeframes): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Timeframes], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Timeframes",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_transfers(self,_feedurl : str, _agencyid : str, data: Transfers, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Transfers], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Transfers' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Transfers): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Transfers], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Transfers",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_translations(self,_feedurl : str, _agencyid : str, data: Translations, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Translations], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Translations' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Translations): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Translations], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Translations",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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


    async def send_general_transit_feed_static_trips(self,_feedurl : str, _agencyid : str, data: Trips, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Trips], str]=None) -> None:
        """
        Sends the 'GeneralTransitFeed.Static.Trips' event to the Kafka topic

        Args:
            _feedurl(str):  Value for placeholder feedurl in attribute source
            _agencyid(str):  Value for placeholder agencyid in attribute subject
            data: (Trips): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Trips], str]): A function to map the CloudEvent contents to a Kafka key (default: None). 
                The default key mapper maps the CloudEvent type, source, and subject to the Kafka key
        """
        attributes = {
             "specversion":"1.0",
             "type":"GeneralTransitFeed.Static.Trips",
             "source":"{feedurl}".format(feedurl = _feedurl),
             "subject":"{agencyid}".format(agencyid = _agencyid)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=lambda x: self.__key_mapper(x, data, key_mapper))
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'GeneralTransitFeedStaticEventProducer':
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

