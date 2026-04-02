
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

from dwd_producer_kafka_producer.producer import DEDWDCDCEventProducer

# imports for the data classes for each event

from dwd_producer_data.de.dwd.cdc.stationmetadata import StationMetadata
from dwd_producer_data.de.dwd.cdc.airtemperature10min import AirTemperature10Min
from dwd_producer_data.de.dwd.cdc.precipitation10min import Precipitation10Min
from dwd_producer_data.de.dwd.cdc.wind10min import Wind10Min
from dwd_producer_data.de.dwd.cdc.solar10min import Solar10Min
from dwd_producer_data.de.dwd.cdc.hourlyobservation import HourlyObservation
from dwd_producer_data.de.dwd.cdc.de.dwd.weather.alert import Alert

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
        dedwdcdcevent_producer = DEDWDCDCEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        dedwdcdcevent_producer = DEDWDCDCEventProducer(kafka_producer, topic, 'binary')

    # ---- DE.DWD.CDC.StationMetadata ----
    # TODO: Supply event data for the DE.DWD.CDC.StationMetadata event
    _station_metadata = StationMetadata()

    # sends the 'DE.DWD.CDC.StationMetadata' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_station_metadata(data = _station_metadata)
    print(f"Sent 'DE.DWD.CDC.StationMetadata' event: {_station_metadata.to_json()}")

    # ---- DE.DWD.CDC.AirTemperature10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.AirTemperature10Min event
    _air_temperature10_min = AirTemperature10Min()

    # sends the 'DE.DWD.CDC.AirTemperature10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_air_temperature10_min(data = _air_temperature10_min)
    print(f"Sent 'DE.DWD.CDC.AirTemperature10Min' event: {_air_temperature10_min.to_json()}")

    # ---- DE.DWD.CDC.Precipitation10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.Precipitation10Min event
    _precipitation10_min = Precipitation10Min()

    # sends the 'DE.DWD.CDC.Precipitation10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_precipitation10_min(data = _precipitation10_min)
    print(f"Sent 'DE.DWD.CDC.Precipitation10Min' event: {_precipitation10_min.to_json()}")

    # ---- DE.DWD.CDC.Wind10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.Wind10Min event
    _wind10_min = Wind10Min()

    # sends the 'DE.DWD.CDC.Wind10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_wind10_min(data = _wind10_min)
    print(f"Sent 'DE.DWD.CDC.Wind10Min' event: {_wind10_min.to_json()}")

    # ---- DE.DWD.CDC.Solar10Min ----
    # TODO: Supply event data for the DE.DWD.CDC.Solar10Min event
    _solar10_min = Solar10Min()

    # sends the 'DE.DWD.CDC.Solar10Min' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_solar10_min(data = _solar10_min)
    print(f"Sent 'DE.DWD.CDC.Solar10Min' event: {_solar10_min.to_json()}")

    # ---- DE.DWD.CDC.HourlyObservation ----
    # TODO: Supply event data for the DE.DWD.CDC.HourlyObservation event
    _hourly_observation = HourlyObservation()

    # sends the 'DE.DWD.CDC.HourlyObservation' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_cdc_hourly_observation(data = _hourly_observation)
    print(f"Sent 'DE.DWD.CDC.HourlyObservation' event: {_hourly_observation.to_json()}")

    # ---- DE.DWD.Weather.Alert ----
    # TODO: Supply event data for the DE.DWD.Weather.Alert event
    _alert = Alert()

    # sends the 'DE.DWD.Weather.Alert' event to Kafka topic.
    await dedwdcdcevent_producer.send_de_dwd_weather_alert(data = _alert)
    print(f"Sent 'DE.DWD.Weather.Alert' event: {_alert.to_json()}")

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