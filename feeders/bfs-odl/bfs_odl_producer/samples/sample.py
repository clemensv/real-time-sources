
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

from bfs_odl_producer_kafka_producer.producer import DeBfsOdlEventProducer

# imports for the data classes for each event

from bfs_odl_producer_data.station import Station
from bfs_odl_producer_data.doseratemeasurement import DoseRateMeasurement

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
        de_bfs_odl_event_producer = DeBfsOdlEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        de_bfs_odl_event_producer = DeBfsOdlEventProducer(kafka_producer, topic, 'binary')

    # ---- de.bfs.odl.Station ----
    # TODO: Supply event data for the de.bfs.odl.Station event
    _station = Station()

    # sends the 'de.bfs.odl.Station' event to Kafka topic.
    await de_bfs_odl_event_producer.send_de_bfs_odl_station(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'de.bfs.odl.Station' event: {_station.to_json()}")

    # ---- de.bfs.odl.DoseRateMeasurement ----
    # TODO: Supply event data for the de.bfs.odl.DoseRateMeasurement event
    _dose_rate_measurement = DoseRateMeasurement()

    # sends the 'de.bfs.odl.DoseRateMeasurement' event to Kafka topic.
    await de_bfs_odl_event_producer.send_de_bfs_odl_dose_rate_measurement(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _dose_rate_measurement)
    print(f"Sent 'de.bfs.odl.DoseRateMeasurement' event: {_dose_rate_measurement.to_json()}")

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