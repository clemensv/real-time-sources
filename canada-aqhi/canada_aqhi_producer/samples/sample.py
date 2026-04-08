
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

from canada_aqhi_producer_kafka_producer.producer import CaGcWeatherAqhiEventProducer

# imports for the data classes for each event

from canada_aqhi_producer_data.community import Community
from canada_aqhi_producer_data.observation import Observation
from canada_aqhi_producer_data.forecast import Forecast

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
        ca_gc_weather_aqhi_event_producer = CaGcWeatherAqhiEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        ca_gc_weather_aqhi_event_producer = CaGcWeatherAqhiEventProducer(kafka_producer, topic, 'binary')

    # ---- ca.gc.weather.aqhi.Community ----
    # TODO: Supply event data for the ca.gc.weather.aqhi.Community event
    _community = Community()

    # sends the 'ca.gc.weather.aqhi.Community' event to Kafka topic.
    await ca_gc_weather_aqhi_event_producer.send_ca_gc_weather_aqhi_community(_province = 'TODO: replace me', _community_name = 'TODO: replace me', data = _community)
    print(f"Sent 'ca.gc.weather.aqhi.Community' event: {_community.to_json()}")

    # ---- ca.gc.weather.aqhi.Observation ----
    # TODO: Supply event data for the ca.gc.weather.aqhi.Observation event
    _observation = Observation()

    # sends the 'ca.gc.weather.aqhi.Observation' event to Kafka topic.
    await ca_gc_weather_aqhi_event_producer.send_ca_gc_weather_aqhi_observation(_province = 'TODO: replace me', _community_name = 'TODO: replace me', data = _observation)
    print(f"Sent 'ca.gc.weather.aqhi.Observation' event: {_observation.to_json()}")

    # ---- ca.gc.weather.aqhi.Forecast ----
    # TODO: Supply event data for the ca.gc.weather.aqhi.Forecast event
    _forecast = Forecast()

    # sends the 'ca.gc.weather.aqhi.Forecast' event to Kafka topic.
    await ca_gc_weather_aqhi_event_producer.send_ca_gc_weather_aqhi_forecast(_province = 'TODO: replace me', _community_name = 'TODO: replace me', data = _forecast)
    print(f"Sent 'ca.gc.weather.aqhi.Forecast' event: {_forecast.to_json()}")

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