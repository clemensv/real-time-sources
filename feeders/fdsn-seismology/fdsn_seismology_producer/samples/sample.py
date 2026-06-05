
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

from fdsn_seismology_producer_kafka_producer.producer import OrgFdsnEventKafkaEventProducer

# imports for the data classes for each event

from fdsn_seismology_producer_data.earthquake import Earthquake
from fdsn_seismology_producer_data.node import Node

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
        org_fdsn_event_kafka_event_producer = OrgFdsnEventKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_fdsn_event_kafka_event_producer = OrgFdsnEventKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.fdsn.event.kafka.Earthquake ----
    # TODO: Supply event data for the org.fdsn.event.kafka.Earthquake event
    _earthquake = Earthquake()

    # sends the 'org.fdsn.event.kafka.Earthquake' event to Kafka topic.
    await org_fdsn_event_kafka_event_producer.send_org_fdsn_event_kafka_earthquake(_node_url = 'TODO: replace me', _contributor = 'TODO: replace me', _event_id = 'TODO: replace me', data = _earthquake)
    print(f"Sent 'org.fdsn.event.kafka.Earthquake' event: {_earthquake.to_json()}")

    # ---- org.fdsn.event.kafka.Node ----
    # TODO: Supply event data for the org.fdsn.event.kafka.Node event
    _node = Node()

    # sends the 'org.fdsn.event.kafka.Node' event to Kafka topic.
    await org_fdsn_event_kafka_event_producer.send_org_fdsn_event_kafka_node(_base_url = 'TODO: replace me', _node_id = 'TODO: replace me', data = _node)
    print(f"Sent 'org.fdsn.event.kafka.Node' event: {_node.to_json()}")

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