
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

from uba_airdata_producer_kafka_producer.producer import DeUbaAirdataEventProducer
from uba_airdata_producer_kafka_producer.producer import DeUbaAirdataComponentsEventProducer

# imports for the data classes for each event

from uba_airdata_producer_data.station import Station
from uba_airdata_producer_data.measure import Measure
from uba_airdata_producer_data.component import Component

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
        de_uba_airdata_event_producer = DeUbaAirdataEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        de_uba_airdata_event_producer = DeUbaAirdataEventProducer(kafka_producer, topic, 'binary')

    # ---- de.uba.airdata.Station ----
    # TODO: Supply event data for the de.uba.airdata.Station event
    _station = Station()

    # sends the 'de.uba.airdata.Station' event to Kafka topic.
    await de_uba_airdata_event_producer.send_de_uba_airdata_station(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'de.uba.airdata.Station' event: {_station.to_json()}")

    # ---- de.uba.airdata.Measure ----
    # TODO: Supply event data for the de.uba.airdata.Measure event
    _measure = Measure()

    # sends the 'de.uba.airdata.Measure' event to Kafka topic.
    await de_uba_airdata_event_producer.send_de_uba_airdata_measure(_feedurl = 'TODO: replace me', _station_id = 'TODO: replace me', data = _measure)
    print(f"Sent 'de.uba.airdata.Measure' event: {_measure.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        de_uba_airdata_components_event_producer = DeUbaAirdataComponentsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        de_uba_airdata_components_event_producer = DeUbaAirdataComponentsEventProducer(kafka_producer, topic, 'binary')

    # ---- de.uba.airdata.components.Component ----
    # TODO: Supply event data for the de.uba.airdata.components.Component event
    _component = Component()

    # sends the 'de.uba.airdata.components.Component' event to Kafka topic.
    await de_uba_airdata_components_event_producer.send_de_uba_airdata_components_component(_feedurl = 'TODO: replace me', _component_id = 'TODO: replace me', data = _component)
    print(f"Sent 'de.uba.airdata.components.Component' event: {_component.to_json()}")

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