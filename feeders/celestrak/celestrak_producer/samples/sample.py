
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

from celestrak_producer_kafka_producer.producer import OrgCelestrakKafkaEventProducer

# imports for the data classes for each event

from celestrak_producer_data import SatelliteCatalogEntry
from celestrak_producer_data import OrbitMeanElements
from celestrak_producer_data import SupplementalOrbitMeanElements

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
        org_celestrak_kafka_event_producer = OrgCelestrakKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_celestrak_kafka_event_producer = OrgCelestrakKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.celestrak.kafka.SatelliteCatalogEntry ----
    # TODO: Supply event data for the org.celestrak.kafka.SatelliteCatalogEntry event
    _satellite_catalog_entry = SatelliteCatalogEntry()

    # sends the 'org.celestrak.kafka.SatelliteCatalogEntry' event to Kafka topic.
    await org_celestrak_kafka_event_producer.send_org_celestrak_kafka_satellite_catalog_entry(_feedurl = 'TODO: replace me', _norad_cat_id = 'TODO: replace me', data = _satellite_catalog_entry)
    print(f"Sent 'org.celestrak.kafka.SatelliteCatalogEntry' event: {_satellite_catalog_entry.to_json()}")

    # ---- org.celestrak.kafka.OrbitMeanElements ----
    # TODO: Supply event data for the org.celestrak.kafka.OrbitMeanElements event
    _orbit_mean_elements = OrbitMeanElements()

    # sends the 'org.celestrak.kafka.OrbitMeanElements' event to Kafka topic.
    await org_celestrak_kafka_event_producer.send_org_celestrak_kafka_orbit_mean_elements(_feedurl = 'TODO: replace me', _norad_cat_id = 'TODO: replace me', data = _orbit_mean_elements)
    print(f"Sent 'org.celestrak.kafka.OrbitMeanElements' event: {_orbit_mean_elements.to_json()}")

    # ---- org.celestrak.kafka.SupplementalOrbitMeanElements ----
    # TODO: Supply event data for the org.celestrak.kafka.SupplementalOrbitMeanElements event
    _supplemental_orbit_mean_elements = SupplementalOrbitMeanElements()

    # sends the 'org.celestrak.kafka.SupplementalOrbitMeanElements' event to Kafka topic.
    await org_celestrak_kafka_event_producer.send_org_celestrak_kafka_supplemental_orbit_mean_elements(_feedurl = 'TODO: replace me', _norad_cat_id = 'TODO: replace me', data = _supplemental_orbit_mean_elements)
    print(f"Sent 'org.celestrak.kafka.SupplementalOrbitMeanElements' event: {_supplemental_orbit_mean_elements.to_json()}")

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