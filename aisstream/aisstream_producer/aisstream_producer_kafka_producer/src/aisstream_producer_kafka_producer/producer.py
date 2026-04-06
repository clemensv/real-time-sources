# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from aisstream_producer_data import PositionReport
from aisstream_producer_data import ShipStaticData
from aisstream_producer_data import StandardClassBPositionReport
from aisstream_producer_data import ExtendedClassBPositionReport
from aisstream_producer_data import AidsToNavigationReport
from aisstream_producer_data import StaticDataReport
from aisstream_producer_data import BaseStationReport
from aisstream_producer_data import SafetyBroadcastMessage
from aisstream_producer_data import StandardSearchAndRescueAircraftReport
from aisstream_producer_data import LongRangeAisBroadcastMessage
from aisstream_producer_data import AddressedSafetyMessage
from aisstream_producer_data import AddressedBinaryMessage
from aisstream_producer_data import AssignedModeCommand
from aisstream_producer_data import BinaryAcknowledge
from aisstream_producer_data import BinaryBroadcastMessage
from aisstream_producer_data import ChannelManagement
from aisstream_producer_data import CoordinatedUTCInquiry
from aisstream_producer_data import DataLinkManagementMessage
from aisstream_producer_data import GnssBroadcastBinaryMessage
from aisstream_producer_data import GroupAssignmentCommand
from aisstream_producer_data import Interrogation
from aisstream_producer_data import MultiSlotBinaryMessage
from aisstream_producer_data import SingleSlotBinaryMessage

class IOAISstreamEventProducer:
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

    def send_io_aisstream_position_report(self,_mmsi : str, data: PositionReport, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, PositionReport], str]=None) -> None:
        """
        Sends the 'IO.AISstream.PositionReport' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (PositionReport): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, PositionReport], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.PositionReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_ship_static_data(self,_mmsi : str, data: ShipStaticData, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ShipStaticData], str]=None) -> None:
        """
        Sends the 'IO.AISstream.ShipStaticData' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (ShipStaticData): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ShipStaticData], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.ShipStaticData",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_standard_class_bposition_report(self,_mmsi : str, data: StandardClassBPositionReport, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, StandardClassBPositionReport], str]=None) -> None:
        """
        Sends the 'IO.AISstream.StandardClassBPositionReport' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (StandardClassBPositionReport): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, StandardClassBPositionReport], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.StandardClassBPositionReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_extended_class_bposition_report(self,_mmsi : str, data: ExtendedClassBPositionReport, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ExtendedClassBPositionReport], str]=None) -> None:
        """
        Sends the 'IO.AISstream.ExtendedClassBPositionReport' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (ExtendedClassBPositionReport): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ExtendedClassBPositionReport], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.ExtendedClassBPositionReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_aids_to_navigation_report(self,_mmsi : str, data: AidsToNavigationReport, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AidsToNavigationReport], str]=None) -> None:
        """
        Sends the 'IO.AISstream.AidsToNavigationReport' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (AidsToNavigationReport): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AidsToNavigationReport], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.AidsToNavigationReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_static_data_report(self,_mmsi : str, data: StaticDataReport, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, StaticDataReport], str]=None) -> None:
        """
        Sends the 'IO.AISstream.StaticDataReport' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (StaticDataReport): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, StaticDataReport], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.StaticDataReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_base_station_report(self,_mmsi : str, data: BaseStationReport, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BaseStationReport], str]=None) -> None:
        """
        Sends the 'IO.AISstream.BaseStationReport' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (BaseStationReport): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BaseStationReport], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.BaseStationReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_safety_broadcast_message(self,_mmsi : str, data: SafetyBroadcastMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SafetyBroadcastMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.SafetyBroadcastMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (SafetyBroadcastMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SafetyBroadcastMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.SafetyBroadcastMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_standard_search_and_rescue_aircraft_report(self,_mmsi : str, data: StandardSearchAndRescueAircraftReport, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, StandardSearchAndRescueAircraftReport], str]=None) -> None:
        """
        Sends the 'IO.AISstream.StandardSearchAndRescueAircraftReport' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (StandardSearchAndRescueAircraftReport): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, StandardSearchAndRescueAircraftReport], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.StandardSearchAndRescueAircraftReport",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_long_range_ais_broadcast_message(self,_mmsi : str, data: LongRangeAisBroadcastMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, LongRangeAisBroadcastMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.LongRangeAisBroadcastMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (LongRangeAisBroadcastMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, LongRangeAisBroadcastMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.LongRangeAisBroadcastMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_addressed_safety_message(self,_mmsi : str, data: AddressedSafetyMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AddressedSafetyMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.AddressedSafetyMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (AddressedSafetyMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AddressedSafetyMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.AddressedSafetyMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_addressed_binary_message(self,_mmsi : str, data: AddressedBinaryMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AddressedBinaryMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.AddressedBinaryMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (AddressedBinaryMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AddressedBinaryMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.AddressedBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_assigned_mode_command(self,_mmsi : str, data: AssignedModeCommand, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, AssignedModeCommand], str]=None) -> None:
        """
        Sends the 'IO.AISstream.AssignedModeCommand' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (AssignedModeCommand): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, AssignedModeCommand], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.AssignedModeCommand",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_binary_acknowledge(self,_mmsi : str, data: BinaryAcknowledge, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BinaryAcknowledge], str]=None) -> None:
        """
        Sends the 'IO.AISstream.BinaryAcknowledge' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (BinaryAcknowledge): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BinaryAcknowledge], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.BinaryAcknowledge",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_binary_broadcast_message(self,_mmsi : str, data: BinaryBroadcastMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, BinaryBroadcastMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.BinaryBroadcastMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (BinaryBroadcastMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, BinaryBroadcastMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.BinaryBroadcastMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_channel_management(self,_mmsi : str, data: ChannelManagement, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ChannelManagement], str]=None) -> None:
        """
        Sends the 'IO.AISstream.ChannelManagement' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (ChannelManagement): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ChannelManagement], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.ChannelManagement",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_coordinated_utcinquiry(self,_mmsi : str, data: CoordinatedUTCInquiry, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, CoordinatedUTCInquiry], str]=None) -> None:
        """
        Sends the 'IO.AISstream.CoordinatedUTCInquiry' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (CoordinatedUTCInquiry): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, CoordinatedUTCInquiry], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.CoordinatedUTCInquiry",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_data_link_management_message(self,_mmsi : str, data: DataLinkManagementMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, DataLinkManagementMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.DataLinkManagementMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (DataLinkManagementMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, DataLinkManagementMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.DataLinkManagementMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_gnss_broadcast_binary_message(self,_mmsi : str, data: GnssBroadcastBinaryMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GnssBroadcastBinaryMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.GnssBroadcastBinaryMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (GnssBroadcastBinaryMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GnssBroadcastBinaryMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.GnssBroadcastBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_group_assignment_command(self,_mmsi : str, data: GroupAssignmentCommand, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, GroupAssignmentCommand], str]=None) -> None:
        """
        Sends the 'IO.AISstream.GroupAssignmentCommand' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (GroupAssignmentCommand): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, GroupAssignmentCommand], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.GroupAssignmentCommand",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_interrogation(self,_mmsi : str, data: Interrogation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Interrogation], str]=None) -> None:
        """
        Sends the 'IO.AISstream.Interrogation' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (Interrogation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Interrogation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.Interrogation",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_multi_slot_binary_message(self,_mmsi : str, data: MultiSlotBinaryMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, MultiSlotBinaryMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.MultiSlotBinaryMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (MultiSlotBinaryMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, MultiSlotBinaryMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.MultiSlotBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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


    def send_io_aisstream_single_slot_binary_message(self,_mmsi : str, data: SingleSlotBinaryMessage, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, SingleSlotBinaryMessage], str]=None) -> None:
        """
        Sends the 'IO.AISstream.SingleSlotBinaryMessage' event to the Kafka topic

        Args:
            _mmsi(str):  Value for placeholder mmsi in attribute subject
            data: (SingleSlotBinaryMessage): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, SingleSlotBinaryMessage], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{mmsi}'
        """
        kafka_key = "{mmsi}".format(mmsi=_mmsi)
        attributes = {
             "type":"IO.AISstream.SingleSlotBinaryMessage",
             "source":"wss://stream.aisstream.io/v0/stream",
             "subject":"{mmsi}".format(mmsi = _mmsi)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'IOAISstreamEventProducer':
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

