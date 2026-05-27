# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from autobahn_producer_data import RoadEvent
from autobahn_producer_data import WarningEvent
from autobahn_producer_data import ParkingLorry
from autobahn_producer_data import ChargingStation
from autobahn_producer_data import Webcam

class DEAutobahnEventProducer:
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

    def send_de_autobahn_roadwork_appeared(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.RoadworkAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.RoadworkAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_roadwork_updated(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.RoadworkUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.RoadworkUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_roadwork_resolved(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.RoadworkResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.RoadworkResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_short_term_roadwork_appeared(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ShortTermRoadworkAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ShortTermRoadworkAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_short_term_roadwork_updated(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ShortTermRoadworkUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ShortTermRoadworkUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_short_term_roadwork_resolved(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ShortTermRoadworkResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ShortTermRoadworkResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_warning_appeared(self,_identifier : str, _event_time : str, data: WarningEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WarningEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WarningAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (WarningEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WarningEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WarningAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_warning_updated(self,_identifier : str, _event_time : str, data: WarningEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WarningEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WarningUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (WarningEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WarningEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WarningUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_warning_resolved(self,_identifier : str, _event_time : str, data: WarningEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, WarningEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WarningResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (WarningEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, WarningEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WarningResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_closure_appeared(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ClosureAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ClosureAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_closure_updated(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ClosureUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ClosureUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_closure_resolved(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ClosureResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ClosureResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_entry_exit_closure_appeared(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.EntryExitClosureAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.EntryExitClosureAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_entry_exit_closure_updated(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.EntryExitClosureUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.EntryExitClosureUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_entry_exit_closure_resolved(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.EntryExitClosureResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.EntryExitClosureResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_weight_limit35_restriction_appeared(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WeightLimit35RestrictionAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WeightLimit35RestrictionAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_weight_limit35_restriction_updated(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WeightLimit35RestrictionUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WeightLimit35RestrictionUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_weight_limit35_restriction_resolved(self,_identifier : str, _event_time : str, data: RoadEvent, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, RoadEvent], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WeightLimit35RestrictionResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (RoadEvent): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, RoadEvent], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WeightLimit35RestrictionResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_parking_lorry_appeared(self,_identifier : str, _event_time : str, data: ParkingLorry, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ParkingLorry], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ParkingLorryAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ParkingLorry): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ParkingLorry], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ParkingLorryAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_parking_lorry_updated(self,_identifier : str, _event_time : str, data: ParkingLorry, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ParkingLorry], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ParkingLorryUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ParkingLorry): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ParkingLorry], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ParkingLorryUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_parking_lorry_resolved(self,_identifier : str, _event_time : str, data: ParkingLorry, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ParkingLorry], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ParkingLorryResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ParkingLorry): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ParkingLorry], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ParkingLorryResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_electric_charging_station_appeared(self,_identifier : str, _event_time : str, data: ChargingStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ChargingStation], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ElectricChargingStationAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ChargingStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ChargingStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ElectricChargingStationAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_electric_charging_station_updated(self,_identifier : str, _event_time : str, data: ChargingStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ChargingStation], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ElectricChargingStationUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ChargingStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ChargingStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ElectricChargingStationUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_electric_charging_station_resolved(self,_identifier : str, _event_time : str, data: ChargingStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ChargingStation], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.ElectricChargingStationResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ChargingStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ChargingStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.ElectricChargingStationResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_strong_electric_charging_station_appeared(self,_identifier : str, _event_time : str, data: ChargingStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ChargingStation], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.StrongElectricChargingStationAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ChargingStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ChargingStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.StrongElectricChargingStationAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_strong_electric_charging_station_updated(self,_identifier : str, _event_time : str, data: ChargingStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ChargingStation], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.StrongElectricChargingStationUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ChargingStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ChargingStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.StrongElectricChargingStationUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_strong_electric_charging_station_resolved(self,_identifier : str, _event_time : str, data: ChargingStation, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, ChargingStation], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.StrongElectricChargingStationResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (ChargingStation): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, ChargingStation], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.StrongElectricChargingStationResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_webcam_appeared(self,_identifier : str, _event_time : str, data: Webcam, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Webcam], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WebcamAppeared' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (Webcam): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Webcam], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WebcamAppeared",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_webcam_updated(self,_identifier : str, _event_time : str, data: Webcam, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Webcam], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WebcamUpdated' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (Webcam): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Webcam], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WebcamUpdated",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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


    def send_de_autobahn_webcam_resolved(self,_identifier : str, _event_time : str, data: Webcam, content_type: str = "application/json", flush_producer=True, key_mapper: typing.Callable[[CloudEvent, Webcam], str]=None) -> None:
        """
        Sends the 'DE.Autobahn.WebcamResolved' event to the Kafka topic

        Args:
            _identifier(str):  Value for placeholder identifier in attribute subject
            _event_time(str):  Value for placeholder event_time in attribute time
            data: (Webcam): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
            key_mapper(Callable[[CloudEvent, Webcam], str]): A function to map the CloudEvent contents to a Kafka key (default: None).
                The default key is derived from the xRegistry Kafka key declaration '{identifier}'
        """
        kafka_key = "{identifier}".format(identifier=_identifier)
        attributes = {
             "type":"DE.Autobahn.WebcamResolved",
             "source":"https://verkehr.autobahn.de/o/autobahn",
             "subject":"{identifier}".format(identifier = _identifier),
             "time":"{event_time}".format(event_time = _event_time)
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
    def from_connection_string(cls, connection_string: str, topic: typing.Optional[str]=None, content_mode: typing.Literal['structured','binary']='structured') -> 'DEAutobahnEventProducer':
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

