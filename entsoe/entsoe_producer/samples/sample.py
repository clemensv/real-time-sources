
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

from entsoe_producer_kafka_producer.producer import EuEntsoeTransparencyEventProducer

# imports for the data classes for each event

from entsoe_producer_data.eu.entsoe.transparency.actualgenerationpertype import ActualGenerationPerType
from entsoe_producer_data.eu.entsoe.transparency.dayaheadprices import DayAheadPrices
from entsoe_producer_data.eu.entsoe.transparency.actualtotalload import ActualTotalLoad

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
        eu_entsoe_transparency_event_producer = EuEntsoeTransparencyEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        eu_entsoe_transparency_event_producer = EuEntsoeTransparencyEventProducer(kafka_producer, topic, 'binary')

    # ---- eu.entsoe.transparency.ActualGenerationPerType ----
    # TODO: Supply event data for the eu.entsoe.transparency.ActualGenerationPerType event
    _actual_generation_per_type = ActualGenerationPerType()

    # sends the 'eu.entsoe.transparency.ActualGenerationPerType' event to Kafka topic.
    await eu_entsoe_transparency_event_producer.send_eu_entsoe_transparency_actual_generation_per_type(data = _actual_generation_per_type)
    print(f"Sent 'eu.entsoe.transparency.ActualGenerationPerType' event: {_actual_generation_per_type.to_json()}")

    # ---- eu.entsoe.transparency.DayAheadPrices ----
    # TODO: Supply event data for the eu.entsoe.transparency.DayAheadPrices event
    _day_ahead_prices = DayAheadPrices()

    # sends the 'eu.entsoe.transparency.DayAheadPrices' event to Kafka topic.
    await eu_entsoe_transparency_event_producer.send_eu_entsoe_transparency_day_ahead_prices(data = _day_ahead_prices)
    print(f"Sent 'eu.entsoe.transparency.DayAheadPrices' event: {_day_ahead_prices.to_json()}")

    # ---- eu.entsoe.transparency.ActualTotalLoad ----
    # TODO: Supply event data for the eu.entsoe.transparency.ActualTotalLoad event
    _actual_total_load = ActualTotalLoad()

    # sends the 'eu.entsoe.transparency.ActualTotalLoad' event to Kafka topic.
    await eu_entsoe_transparency_event_producer.send_eu_entsoe_transparency_actual_total_load(data = _actual_total_load)
    print(f"Sent 'eu.entsoe.transparency.ActualTotalLoad' event: {_actual_total_load.to_json()}")

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