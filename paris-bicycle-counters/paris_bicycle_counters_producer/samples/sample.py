
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

from paris_bicycle_counters_producer_kafka_producer.producer import FRParisOpenDataVeloEventProducer

# imports for the data classes for each event

from paris_bicycle_counters_producer_data.counter import Counter
from paris_bicycle_counters_producer_data.bicyclecount import BicycleCount

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
        frparis_open_data_velo_event_producer = FRParisOpenDataVeloEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        frparis_open_data_velo_event_producer = FRParisOpenDataVeloEventProducer(kafka_producer, topic, 'binary')

    # ---- FR.Paris.OpenData.Velo.Counter ----
    # TODO: Supply event data for the FR.Paris.OpenData.Velo.Counter event
    _counter = Counter()

    # sends the 'FR.Paris.OpenData.Velo.Counter' event to Kafka topic.
    await frparis_open_data_velo_event_producer.send_fr_paris_open_data_velo_counter(_counter_id = 'TODO: replace me', data = _counter)
    print(f"Sent 'FR.Paris.OpenData.Velo.Counter' event: {_counter.to_json()}")

    # ---- FR.Paris.OpenData.Velo.BicycleCount ----
    # TODO: Supply event data for the FR.Paris.OpenData.Velo.BicycleCount event
    _bicycle_count = BicycleCount()

    # sends the 'FR.Paris.OpenData.Velo.BicycleCount' event to Kafka topic.
    await frparis_open_data_velo_event_producer.send_fr_paris_open_data_velo_bicycle_count(_counter_id = 'TODO: replace me', data = _bicycle_count)
    print(f"Sent 'FR.Paris.OpenData.Velo.BicycleCount' event: {_bicycle_count.to_json()}")

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