
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

from ireland_opw_waterlevel_producer_kafka_producer.producer import IeGovOpwWaterlevelEventProducer

# imports for the data classes for each event

from ireland_opw_waterlevel_producer_data.station import Station
from ireland_opw_waterlevel_producer_data.waterlevelreading import WaterLevelReading

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
        ie_gov_opw_waterlevel_event_producer = IeGovOpwWaterlevelEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ie_gov_opw_waterlevel_event_producer = IeGovOpwWaterlevelEventProducer(kafka_producer, topic, 'binary')

    # ---- ie.gov.opw.waterlevel.Station ----
    # TODO: Supply event data for the ie.gov.opw.waterlevel.Station event
    _station = Station()

    # sends the 'ie.gov.opw.waterlevel.Station' event to Kafka topic.
    await ie_gov_opw_waterlevel_event_producer.send_ie_gov_opw_waterlevel_station(_feedurl = 'TODO: replace me', _station_ref = 'TODO: replace me', data = _station)
    print(f"Sent 'ie.gov.opw.waterlevel.Station' event: {_station.to_json()}")

    # ---- ie.gov.opw.waterlevel.WaterLevelReading ----
    # TODO: Supply event data for the ie.gov.opw.waterlevel.WaterLevelReading event
    _water_level_reading = WaterLevelReading()

    # sends the 'ie.gov.opw.waterlevel.WaterLevelReading' event to Kafka topic.
    await ie_gov_opw_waterlevel_event_producer.send_ie_gov_opw_waterlevel_water_level_reading(_feedurl = 'TODO: replace me', _station_ref = 'TODO: replace me', data = _water_level_reading)
    print(f"Sent 'ie.gov.opw.waterlevel.WaterLevelReading' event: {_water_level_reading.to_json()}")

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