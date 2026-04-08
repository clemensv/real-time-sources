
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

from luchtmeetnet_nl_producer_kafka_producer.producer import NlRivmLuchtmeetnetEventProducer
from luchtmeetnet_nl_producer_kafka_producer.producer import NlRivmLuchtmeetnetComponentsEventProducer

# imports for the data classes for each event

from luchtmeetnet_nl_producer_data.station import Station
from luchtmeetnet_nl_producer_data.measurement import Measurement
from luchtmeetnet_nl_producer_data.lki import LKI
from luchtmeetnet_nl_producer_data.component import Component

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
        nl_rivm_luchtmeetnet_event_producer = NlRivmLuchtmeetnetEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nl_rivm_luchtmeetnet_event_producer = NlRivmLuchtmeetnetEventProducer(kafka_producer, topic, 'binary')

    # ---- nl.rivm.luchtmeetnet.Station ----
    # TODO: Supply event data for the nl.rivm.luchtmeetnet.Station event
    _station = Station()

    # sends the 'nl.rivm.luchtmeetnet.Station' event to Kafka topic.
    await nl_rivm_luchtmeetnet_event_producer.send_nl_rivm_luchtmeetnet_station(_station_number = 'TODO: replace me', data = _station)
    print(f"Sent 'nl.rivm.luchtmeetnet.Station' event: {_station.to_json()}")

    # ---- nl.rivm.luchtmeetnet.Measurement ----
    # TODO: Supply event data for the nl.rivm.luchtmeetnet.Measurement event
    _measurement = Measurement()

    # sends the 'nl.rivm.luchtmeetnet.Measurement' event to Kafka topic.
    await nl_rivm_luchtmeetnet_event_producer.send_nl_rivm_luchtmeetnet_measurement(_station_number = 'TODO: replace me', data = _measurement)
    print(f"Sent 'nl.rivm.luchtmeetnet.Measurement' event: {_measurement.to_json()}")

    # ---- nl.rivm.luchtmeetnet.LKI ----
    # TODO: Supply event data for the nl.rivm.luchtmeetnet.LKI event
    _lki = LKI()

    # sends the 'nl.rivm.luchtmeetnet.LKI' event to Kafka topic.
    await nl_rivm_luchtmeetnet_event_producer.send_nl_rivm_luchtmeetnet_lki(_station_number = 'TODO: replace me', data = _lki)
    print(f"Sent 'nl.rivm.luchtmeetnet.LKI' event: {_lki.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nl_rivm_luchtmeetnet_components_event_producer = NlRivmLuchtmeetnetComponentsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nl_rivm_luchtmeetnet_components_event_producer = NlRivmLuchtmeetnetComponentsEventProducer(kafka_producer, topic, 'binary')

    # ---- nl.rivm.luchtmeetnet.components.Component ----
    # TODO: Supply event data for the nl.rivm.luchtmeetnet.components.Component event
    _component = Component()

    # sends the 'nl.rivm.luchtmeetnet.components.Component' event to Kafka topic.
    await nl_rivm_luchtmeetnet_components_event_producer.send_nl_rivm_luchtmeetnet_components_component(_formula = 'TODO: replace me', data = _component)
    print(f"Sent 'nl.rivm.luchtmeetnet.components.Component' event: {_component.to_json()}")

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