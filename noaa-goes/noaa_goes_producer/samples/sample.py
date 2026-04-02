
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

from noaa_goes_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAASWPCEventProducer

# imports for the data classes for each event

from noaa_goes_producer_data.spaceweatheralert import SpaceWeatherAlert
from noaa_goes_producer_data.planetarykindex import PlanetaryKIndex
from noaa_goes_producer_data.solarwindsummary import SolarWindSummary

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
        microsoft_open_data_usnoaaswpcevent_producer = MicrosoftOpenDataUSNOAASWPCEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaswpcevent_producer = MicrosoftOpenDataUSNOAASWPCEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert event
    _space_weather_alert = SpaceWeatherAlert()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcevent_producer.send_microsoft_open_data_us_noaa_swpc_space_weather_alert(data = _space_weather_alert)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert' event: {_space_weather_alert.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex event
    _planetary_kindex = PlanetaryKIndex()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcevent_producer.send_microsoft_open_data_us_noaa_swpc_planetary_kindex(data = _planetary_kindex)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex' event: {_planetary_kindex.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary event
    _solar_wind_summary = SolarWindSummary()

    # sends the 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary' event to Kafka topic.
    await microsoft_open_data_usnoaaswpcevent_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_summary(data = _solar_wind_summary)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary' event: {_solar_wind_summary.to_json()}")

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