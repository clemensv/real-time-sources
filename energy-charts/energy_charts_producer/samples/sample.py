
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

from energy_charts_producer_kafka_producer.producer import InfoEnergyChartsEventProducer

# imports for the data classes for each event

from energy_charts_producer_data.publicpower import PublicPower
from energy_charts_producer_data.spotprice import SpotPrice
from energy_charts_producer_data.gridsignal import GridSignal

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
        info_energy_charts_event_producer = InfoEnergyChartsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        info_energy_charts_event_producer = InfoEnergyChartsEventProducer(kafka_producer, topic, 'binary')

    # ---- info.energy_charts.PublicPower ----
    # TODO: Supply event data for the info.energy_charts.PublicPower event
    _public_power = PublicPower()

    # sends the 'info.energy_charts.PublicPower' event to Kafka topic.
    await info_energy_charts_event_producer.send_info_energy_charts_public_power(_country = 'TODO: replace me', data = _public_power)
    print(f"Sent 'info.energy_charts.PublicPower' event: {_public_power.to_json()}")

    # ---- info.energy_charts.SpotPrice ----
    # TODO: Supply event data for the info.energy_charts.SpotPrice event
    _spot_price = SpotPrice()

    # sends the 'info.energy_charts.SpotPrice' event to Kafka topic.
    await info_energy_charts_event_producer.send_info_energy_charts_spot_price(_country = 'TODO: replace me', data = _spot_price)
    print(f"Sent 'info.energy_charts.SpotPrice' event: {_spot_price.to_json()}")

    # ---- info.energy_charts.GridSignal ----
    # TODO: Supply event data for the info.energy_charts.GridSignal event
    _grid_signal = GridSignal()

    # sends the 'info.energy_charts.GridSignal' event to Kafka topic.
    await info_energy_charts_event_producer.send_info_energy_charts_grid_signal(_country = 'TODO: replace me', data = _grid_signal)
    print(f"Sent 'info.energy_charts.GridSignal' event: {_grid_signal.to_json()}")

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