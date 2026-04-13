
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

from ticketmaster_producer_kafka_producer.producer import TicketmasterEventsEventProducer
from ticketmaster_producer_kafka_producer.producer import TicketmasterReferenceEventProducer

# imports for the data classes for each event

from ticketmaster_producer_data.event import Event
from ticketmaster_producer_data.venue import Venue
from ticketmaster_producer_data.attraction import Attraction
from ticketmaster_producer_data.classification import Classification

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
        ticketmaster_events_event_producer = TicketmasterEventsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ticketmaster_events_event_producer = TicketmasterEventsEventProducer(kafka_producer, topic, 'binary')

    # ---- Ticketmaster.Events.Event ----
    # TODO: Supply event data for the Ticketmaster.Events.Event event
    _event = Event()

    # sends the 'Ticketmaster.Events.Event' event to Kafka topic.
    await ticketmaster_events_event_producer.send_ticketmaster_events_event(_event_id = 'TODO: replace me', _start_datetime_utc = 'TODO: replace me', data = _event)
    print(f"Sent 'Ticketmaster.Events.Event' event: {_event.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        ticketmaster_reference_event_producer = TicketmasterReferenceEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ticketmaster_reference_event_producer = TicketmasterReferenceEventProducer(kafka_producer, topic, 'binary')

    # ---- Ticketmaster.Reference.Venue ----
    # TODO: Supply event data for the Ticketmaster.Reference.Venue event
    _venue = Venue()

    # sends the 'Ticketmaster.Reference.Venue' event to Kafka topic.
    await ticketmaster_reference_event_producer.send_ticketmaster_reference_venue(_entity_id = 'TODO: replace me', data = _venue)
    print(f"Sent 'Ticketmaster.Reference.Venue' event: {_venue.to_json()}")

    # ---- Ticketmaster.Reference.Attraction ----
    # TODO: Supply event data for the Ticketmaster.Reference.Attraction event
    _attraction = Attraction()

    # sends the 'Ticketmaster.Reference.Attraction' event to Kafka topic.
    await ticketmaster_reference_event_producer.send_ticketmaster_reference_attraction(_entity_id = 'TODO: replace me', data = _attraction)
    print(f"Sent 'Ticketmaster.Reference.Attraction' event: {_attraction.to_json()}")

    # ---- Ticketmaster.Reference.Classification ----
    # TODO: Supply event data for the Ticketmaster.Reference.Classification event
    _classification = Classification()

    # sends the 'Ticketmaster.Reference.Classification' event to Kafka topic.
    await ticketmaster_reference_event_producer.send_ticketmaster_reference_classification(_entity_id = 'TODO: replace me', data = _classification)
    print(f"Sent 'Ticketmaster.Reference.Classification' event: {_classification.to_json()}")

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