
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

from bom_australia_producer_kafka_producer.producer import AUGovBOMWeatherEventProducer
from bom_australia_producer_kafka_producer.producer import AUGovBOMWarningEventProducer

# imports for the data classes for each event

from bom_australia_producer_data.station import Station
from bom_australia_producer_data.weatherobservation import WeatherObservation
from bom_australia_producer_data.warningbulletin import WarningBulletin

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
        augov_bomweather_event_producer = AUGovBOMWeatherEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        augov_bomweather_event_producer = AUGovBOMWeatherEventProducer(kafka_producer, topic, 'binary')

    # ---- AU.Gov.BOM.Weather.Station ----
    # TODO: Supply event data for the AU.Gov.BOM.Weather.Station event
    _station = Station()

    # sends the 'AU.Gov.BOM.Weather.Station' event to Kafka topic.
    await augov_bomweather_event_producer.send_au_gov_bom_weather_station(_station_wmo = 'TODO: replace me', data = _station)
    print(f"Sent 'AU.Gov.BOM.Weather.Station' event: {_station.to_json()}")

    # ---- AU.Gov.BOM.Weather.WeatherObservation ----
    # TODO: Supply event data for the AU.Gov.BOM.Weather.WeatherObservation event
    _weather_observation = WeatherObservation()

    # sends the 'AU.Gov.BOM.Weather.WeatherObservation' event to Kafka topic.
    await augov_bomweather_event_producer.send_au_gov_bom_weather_weather_observation(_station_wmo = 'TODO: replace me', data = _weather_observation)
    print(f"Sent 'AU.Gov.BOM.Weather.WeatherObservation' event: {_weather_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        augov_bomwarning_event_producer = AUGovBOMWarningEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        augov_bomwarning_event_producer = AUGovBOMWarningEventProducer(kafka_producer, topic, 'binary')

    # ---- AU.Gov.BOM.Warning.WarningBulletin ----
    # TODO: Supply event data for the AU.Gov.BOM.Warning.WarningBulletin event
    _warning_bulletin = WarningBulletin()

    # sends the 'AU.Gov.BOM.Warning.WarningBulletin' event to Kafka topic.
    await augov_bomwarning_event_producer.send_au_gov_bom_warning_warning_bulletin(_warning_id = 'TODO: replace me', data = _warning_bulletin)
    print(f"Sent 'AU.Gov.BOM.Warning.WarningBulletin' event: {_warning_bulletin.to_json()}")

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