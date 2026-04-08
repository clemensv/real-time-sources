
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

from laqn_london_producer_kafka_producer.producer import UkKclLaqnEventProducer
from laqn_london_producer_kafka_producer.producer import UkKclLaqnSpeciesEventProducer

# imports for the data classes for each event

from laqn_london_producer_data.site import Site
from laqn_london_producer_data.measurement import Measurement
from laqn_london_producer_data.dailyindex import DailyIndex
from laqn_london_producer_data.species import Species

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
        uk_kcl_laqn_event_producer = UkKclLaqnEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        uk_kcl_laqn_event_producer = UkKclLaqnEventProducer(kafka_producer, topic, 'binary')

    # ---- uk.kcl.laqn.Site ----
    # TODO: Supply event data for the uk.kcl.laqn.Site event
    _site = Site()

    # sends the 'uk.kcl.laqn.Site' event to Kafka topic.
    await uk_kcl_laqn_event_producer.send_uk_kcl_laqn_site(_site_code = 'TODO: replace me', data = _site)
    print(f"Sent 'uk.kcl.laqn.Site' event: {_site.to_json()}")

    # ---- uk.kcl.laqn.Measurement ----
    # TODO: Supply event data for the uk.kcl.laqn.Measurement event
    _measurement = Measurement()

    # sends the 'uk.kcl.laqn.Measurement' event to Kafka topic.
    await uk_kcl_laqn_event_producer.send_uk_kcl_laqn_measurement(_site_code = 'TODO: replace me', data = _measurement)
    print(f"Sent 'uk.kcl.laqn.Measurement' event: {_measurement.to_json()}")

    # ---- uk.kcl.laqn.DailyIndex ----
    # TODO: Supply event data for the uk.kcl.laqn.DailyIndex event
    _daily_index = DailyIndex()

    # sends the 'uk.kcl.laqn.DailyIndex' event to Kafka topic.
    await uk_kcl_laqn_event_producer.send_uk_kcl_laqn_daily_index(_site_code = 'TODO: replace me', data = _daily_index)
    print(f"Sent 'uk.kcl.laqn.DailyIndex' event: {_daily_index.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        uk_kcl_laqn_species_event_producer = UkKclLaqnSpeciesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        uk_kcl_laqn_species_event_producer = UkKclLaqnSpeciesEventProducer(kafka_producer, topic, 'binary')

    # ---- uk.kcl.laqn.Species ----
    # TODO: Supply event data for the uk.kcl.laqn.Species event
    _species = Species()

    # sends the 'uk.kcl.laqn.Species' event to Kafka topic.
    await uk_kcl_laqn_species_event_producer.send_uk_kcl_laqn_species(_species_code = 'TODO: replace me', data = _species)
    print(f"Sent 'uk.kcl.laqn.Species' event: {_species.to_json()}")

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