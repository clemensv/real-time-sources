
"""
This is sample code to produce events to Apache Kafka with the producer clients
contained in this project.

There is a producer for each defined event type. The producer is a class that
provides methods to create and send events to the Kafka topics.

Producers are instantiated with the Kafka bootstrap servers and the topic to
which they will send events.

The main function initializes the producers and sends sample events to the Kafka
topics.

This sample uses a Kafka cluster with the necessary topics and configurations.
The script reads the configuration from the command line or uses the environment
variables. The following environment variables are recognized:

- BOOTSTRAP_SERVERS: The Kafka bootstrap servers.
- TOPICS: The Kafka topics to send events to.

Alternatively, you can pass the configuration as command-line arguments.

python sample.py --bootstrap-servers <bootstrap_servers> --topics <topics>
"""

import argparse
import os
import asyncio
from confluent_kafka import Producer
from datetime import datetime
from rssbridge_producer_kafka_producer.producer import MicrosoftOpenDataRssFeedsEventProducer
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem

async def main(producer_config, topics):
    """ Main function to produce events to Kafka """
    topic_list = topics.split(',')
    kafka_producer = Producer(json.loads(producer_config))
    producer_instance = MicrosoftOpenDataRssFeedsEventProducer(producer, topic_list[0], 'binary')
    event_data = ()
    await producer_instance.send_microsoft_opendata_rssfeeds_feeditem(_sourceurl = 'test', _item_id = 'test', data = event_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=True)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=True)

    args = parser.parse_args()

    asyncio.run(main(
        args.producer_config,
        args.topics
    ))