
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

from bluesky-producer_kafka_producer.producer import BlueskyFirehoseEventProducer

# imports for the data classes for each event

from bluesky-producer_data.bluesky.feed.post import Post
from bluesky-producer_data.bluesky.feed.like import Like
from bluesky-producer_data.bluesky.feed.repost import Repost
from bluesky-producer_data.bluesky.graph.follow import Follow
from bluesky-producer_data.bluesky.graph.block import Block
from bluesky-producer_data.bluesky.actor.profile import Profile

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
        bluesky_firehose_event_producer = BlueskyFirehoseEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        bluesky_firehose_event_producer = BlueskyFirehoseEventProducer(kafka_producer, topic, 'binary')

    # ---- Bluesky.Feed.Post ----
    # TODO: Supply event data for the Bluesky.Feed.Post event
    _post = Post()

    # sends the 'Bluesky.Feed.Post' event to Kafka topic.
    await bluesky_firehose_event_producer.send_bluesky_feed_post(_firehoseurl = 'TODO: replace me', _did = 'TODO: replace me', data = _post)
    print(f"Sent 'Bluesky.Feed.Post' event: {_post.to_json()}")

    # ---- Bluesky.Feed.Like ----
    # TODO: Supply event data for the Bluesky.Feed.Like event
    _like = Like()

    # sends the 'Bluesky.Feed.Like' event to Kafka topic.
    await bluesky_firehose_event_producer.send_bluesky_feed_like(_firehoseurl = 'TODO: replace me', _did = 'TODO: replace me', data = _like)
    print(f"Sent 'Bluesky.Feed.Like' event: {_like.to_json()}")

    # ---- Bluesky.Feed.Repost ----
    # TODO: Supply event data for the Bluesky.Feed.Repost event
    _repost = Repost()

    # sends the 'Bluesky.Feed.Repost' event to Kafka topic.
    await bluesky_firehose_event_producer.send_bluesky_feed_repost(_firehoseurl = 'TODO: replace me', _did = 'TODO: replace me', data = _repost)
    print(f"Sent 'Bluesky.Feed.Repost' event: {_repost.to_json()}")

    # ---- Bluesky.Graph.Follow ----
    # TODO: Supply event data for the Bluesky.Graph.Follow event
    _follow = Follow()

    # sends the 'Bluesky.Graph.Follow' event to Kafka topic.
    await bluesky_firehose_event_producer.send_bluesky_graph_follow(_firehoseurl = 'TODO: replace me', _did = 'TODO: replace me', data = _follow)
    print(f"Sent 'Bluesky.Graph.Follow' event: {_follow.to_json()}")

    # ---- Bluesky.Graph.Block ----
    # TODO: Supply event data for the Bluesky.Graph.Block event
    _block = Block()

    # sends the 'Bluesky.Graph.Block' event to Kafka topic.
    await bluesky_firehose_event_producer.send_bluesky_graph_block(_firehoseurl = 'TODO: replace me', _did = 'TODO: replace me', data = _block)
    print(f"Sent 'Bluesky.Graph.Block' event: {_block.to_json()}")

    # ---- Bluesky.Actor.Profile ----
    # TODO: Supply event data for the Bluesky.Actor.Profile event
    _profile = Profile()

    # sends the 'Bluesky.Actor.Profile' event to Kafka topic.
    await bluesky_firehose_event_producer.send_bluesky_actor_profile(_firehoseurl = 'TODO: replace me', _did = 'TODO: replace me', data = _profile)
    print(f"Sent 'Bluesky.Actor.Profile' event: {_profile.to_json()}")

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