# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines
import sys
import json
import uuid
import typing
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Message
from cloudevents.kafka import to_binary, to_structured, KafkaMessage
from cloudevents.http import CloudEvent
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem

class MicrosoftOpenDataRssFeedsEventProducer:
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

    def __key_mapper(self, x: CloudEvent) -> str:
        """
        Maps a CloudEvent to a Kafka key

        Args:
            x (CloudEvent): The CloudEvent to map
        """
        return f'{str(x.get("type"))}:{str(x.get("source"))}{("-"+str(x.get("subject"))) if x.get("subject") else ""}'

    async def send_microsoft_open_data_rss_feeds_feed_item(self,_sourceurl : str, _item_id : str, data: FeedItem, content_type: str = "application/json", flush_producer=True) -> None:
        """
        Sends the 'Microsoft.OpenData.RssFeeds.FeedItem' event to the Kafka topic

        Args:
            _sourceurl(str):  Value for placeholder sourceurl in attribute source
            _item_id(str):  Value for placeholder item_id in attribute subject
            data: (FeedItem): The event data to be sent
            content_type (str): The content type that the event data shall be sent with
            flush_producer(bool): Whether to flush the producer after sending the event (default: True)
        """
        attributes = {
             "type":"Microsoft.OpenData.RssFeeds.FeedItem",
             "source":"{sourceurl}".format(sourceurl = _sourceurl),
             "subject":"{item_id}".format(item_id = _item_id)
        }
        attributes["datacontenttype"] = content_type
        event = CloudEvent.create(attributes, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: x.to_json(), key_mapper=self.__key_mapper)
            message.headers[b"content-type"] = b"application/cloudevents+json"
        else:
            content_type = "application/json"
            event["content-type"] = content_type
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array(content_type), key_mapper=self.__key_mapper)
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)
        if flush_producer:
            self.producer.flush()

