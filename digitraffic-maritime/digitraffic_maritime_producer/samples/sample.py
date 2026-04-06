
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

from digitraffic_maritime_producer_kafka_producer.producer import FiDigitrafficMarineAisEventProducer

# imports for the data classes for each event

from digitraffic_maritime_producer_data.vessellocation import VesselLocation
from digitraffic_maritime_producer_data.vesselmetadata import VesselMetadata

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
        fi_digitraffic_marine_ais_event_producer = FiDigitrafficMarineAisEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        fi_digitraffic_marine_ais_event_producer = FiDigitrafficMarineAisEventProducer(kafka_producer, topic, 'binary')

    # ---- fi.digitraffic.marine.ais.VesselLocation ----
    # TODO: Supply event data for the fi.digitraffic.marine.ais.VesselLocation event
    _vessel_location = VesselLocation()

    # sends the 'fi.digitraffic.marine.ais.VesselLocation' event to Kafka topic.
    await fi_digitraffic_marine_ais_event_producer.send_fi_digitraffic_marine_ais_vessel_location(_mmsi = 'TODO: replace me', data = _vessel_location)
    print(f"Sent 'fi.digitraffic.marine.ais.VesselLocation' event: {_vessel_location.to_json()}")

    # ---- fi.digitraffic.marine.ais.VesselMetadata ----
    # TODO: Supply event data for the fi.digitraffic.marine.ais.VesselMetadata event
    _vessel_metadata = VesselMetadata()

    # sends the 'fi.digitraffic.marine.ais.VesselMetadata' event to Kafka topic.
    await fi_digitraffic_marine_ais_event_producer.send_fi_digitraffic_marine_ais_vessel_metadata(_mmsi = 'TODO: replace me', data = _vessel_metadata)
    print(f"Sent 'fi.digitraffic.marine.ais.VesselMetadata' event: {_vessel_metadata.to_json()}")

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