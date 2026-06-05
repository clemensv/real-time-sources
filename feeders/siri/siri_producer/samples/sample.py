
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

from siri_producer_kafka_producer.producer import OrgSiriKafkaEventProducer

# imports for the data classes for each event

from siri_producer_data.vehicleposition import VehiclePosition
from siri_producer_data.operator import Operator

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
        org_siri_kafka_event_producer = OrgSiriKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_siri_kafka_event_producer = OrgSiriKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.siri.kafka.VehiclePosition ----
    # TODO: Supply event data for the org.siri.kafka.VehiclePosition event
    _vehicle_position = VehiclePosition()

    # sends the 'org.siri.kafka.VehiclePosition' event to Kafka topic.
    await org_siri_kafka_event_producer.send_org_siri_kafka_vehicle_position(_feedurl = 'TODO: replace me', _operator_ref = 'TODO: replace me', _vehicle_ref = 'TODO: replace me', data = _vehicle_position)
    print(f"Sent 'org.siri.kafka.VehiclePosition' event: {_vehicle_position.to_json()}")

    # ---- org.siri.kafka.Operator ----
    # TODO: Supply event data for the org.siri.kafka.Operator event
    _operator = Operator()

    # sends the 'org.siri.kafka.Operator' event to Kafka topic.
    await org_siri_kafka_event_producer.send_org_siri_kafka_operator(_feedurl = 'TODO: replace me', _operator_ref = 'TODO: replace me', data = _operator)
    print(f"Sent 'org.siri.kafka.Operator' event: {_operator.to_json()}")

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