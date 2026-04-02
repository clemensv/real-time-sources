
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

from waterinfo_vmm_producer_kafka_producer.producer import BEVlaanderenWaterinfoVMMEventProducer

# imports for the data classes for each event

from waterinfo_vmm_producer_data.station import Station
from waterinfo_vmm_producer_data.waterlevelreading import WaterLevelReading

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
        bevlaanderen_waterinfo_vmmevent_producer = BEVlaanderenWaterinfoVMMEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        bevlaanderen_waterinfo_vmmevent_producer = BEVlaanderenWaterinfoVMMEventProducer(kafka_producer, topic, 'binary')

    # ---- BE.Vlaanderen.Waterinfo.VMM.Station ----
    # TODO: Supply event data for the BE.Vlaanderen.Waterinfo.VMM.Station event
    _station = Station()

    # sends the 'BE.Vlaanderen.Waterinfo.VMM.Station' event to Kafka topic.
    await bevlaanderen_waterinfo_vmmevent_producer.send_be_vlaanderen_waterinfo_vmm_station(data = _station)
    print(f"Sent 'BE.Vlaanderen.Waterinfo.VMM.Station' event: {_station.to_json()}")

    # ---- BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading ----
    # TODO: Supply event data for the BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading event
    _water_level_reading = WaterLevelReading()

    # sends the 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' event to Kafka topic.
    await bevlaanderen_waterinfo_vmmevent_producer.send_be_vlaanderen_waterinfo_vmm_water_level_reading(data = _water_level_reading)
    print(f"Sent 'BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading' event: {_water_level_reading.to_json()}")

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