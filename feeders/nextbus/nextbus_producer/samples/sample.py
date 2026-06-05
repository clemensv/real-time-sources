
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

from nextbus_producer_kafka_producer.producer import NextbusKafkaEventProducer

# imports for the data classes for each event

from nextbus_producer_data import VehiclePosition
from nextbus_producer_data import RouteConfig
from nextbus_producer_data import Schedule
from nextbus_producer_data import Message

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
        nextbus_kafka_event_producer = NextbusKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nextbus_kafka_event_producer = NextbusKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- nextbus.kafka.VehiclePosition ----
    # TODO: Supply event data for the nextbus.kafka.VehiclePosition event
    _vehicle_position = VehiclePosition()

    # sends the 'nextbus.kafka.VehiclePosition' event to Kafka topic.
    await nextbus_kafka_event_producer.send_nextbus_kafka_vehicle_position(_agency_id = 'TODO: replace me', _route_tag = 'TODO: replace me', _vehicle_id = 'TODO: replace me', data = _vehicle_position)
    print(f"Sent 'nextbus.kafka.VehiclePosition' event: {_vehicle_position.to_json()}")

    # ---- nextbus.kafka.RouteConfig ----
    # TODO: Supply event data for the nextbus.kafka.RouteConfig event
    _route_config = RouteConfig()

    # sends the 'nextbus.kafka.RouteConfig' event to Kafka topic.
    await nextbus_kafka_event_producer.send_nextbus_kafka_route_config(_agency_id = 'TODO: replace me', _route_tag = 'TODO: replace me', _stop_or_vehicle_id = 'TODO: replace me', data = _route_config)
    print(f"Sent 'nextbus.kafka.RouteConfig' event: {_route_config.to_json()}")

    # ---- nextbus.kafka.Schedule ----
    # TODO: Supply event data for the nextbus.kafka.Schedule event
    _schedule = Schedule()

    # sends the 'nextbus.kafka.Schedule' event to Kafka topic.
    await nextbus_kafka_event_producer.send_nextbus_kafka_schedule(_agency_id = 'TODO: replace me', _route_tag = 'TODO: replace me', _stop_or_vehicle_id = 'TODO: replace me', data = _schedule)
    print(f"Sent 'nextbus.kafka.Schedule' event: {_schedule.to_json()}")

    # ---- nextbus.kafka.Message ----
    # TODO: Supply event data for the nextbus.kafka.Message event
    _message = Message()

    # sends the 'nextbus.kafka.Message' event to Kafka topic.
    await nextbus_kafka_event_producer.send_nextbus_kafka_message(_agency_id = 'TODO: replace me', _route_tag = 'TODO: replace me', _stop_or_vehicle_id = 'TODO: replace me', data = _message)
    print(f"Sent 'nextbus.kafka.Message' event: {_message.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c', '--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))