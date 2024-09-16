
"""
This is sample code to produce events to Apache Kafka with the producer clients
contained in this project. You will still need to supply event data in the
marked
placews below before the program can be run.

The script gets the configuration from the command line or uses the environment
variables. The following environment variables are recognized:

- KAFKA_PRODUCER_CONFIG: The Kafka producer configuration.
- KAFKA_TOPICS: The Kafka topics to send events to.
- FABRIC_CONNECTION_STRING: A Microsoft Fabric or Azure Event Hubs connection
string.

Alternatively, you can pass the configuration as command-line arguments.

- `--producer-config`: The Kafka producer configuration.
- `--topics`: The Kafka topics to send events to.
- `-c` or `--connection-string`: The Microsoft Fabric or Azure Event Hubs
connection string.
"""

import argparse
import os
import asyncio
import json
import uuid
from typing import Optional
from datetime import datetime
from confluent_kafka import Producer as KafkaProducer

# imports the producer clients for the message group(s)

from rssbridge_producer_kafka_producer.producer import MicrosoftOpenDataRssFeedsEventProducer

# imports for the data classes for each event

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem

async def main(connection_string: Optional[str], producer_config: Optional[str], topic: Optional[str]):
    """
    Main function to produce events to Apache Kafka

    Args:
        connection_string (Optional[str]): The Fabric connection string
        producer_config (Optional[str]): The Kafka producer configuration
        topic (Optional[str]): The Kafka topic to send events to
    """
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_rss_feeds_event_producer = MicrosoftOpenDataRssFeedsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_rss_feeds_event_producer = MicrosoftOpenDataRssFeedsEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.RssFeeds.FeedItem ----
    # TODO: Supply event data for the Microsoft.OpenData.RssFeeds.FeedItem event
    _feed_item = FeedItem()

    # sends the 'Microsoft.OpenData.RssFeeds.FeedItem' event to Kafka topic.
    await microsoft_open_data_rss_feeds_event_producer.send_microsoft_open_data_rss_feeds_feed_item(_sourceurl = 'TODO: replace me', _item_id = 'TODO: replace me', data = _feed_item)
    print(f"Sent 'Microsoft.OpenData.RssFeeds.FeedItem' event: {_feed_item.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c|--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))