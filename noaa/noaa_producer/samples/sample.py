
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

from noaa-producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAEventProducer

# imports for the data classes for each event

from noaa-producer_data.microsoft.opendata.us.noaa.waterlevel import WaterLevel
from noaa-producer_data.microsoft.opendata.us.noaa.predictions import Predictions
from noaa-producer_data.microsoft.opendata.us.noaa.airpressure import AirPressure
from noaa-producer_data.microsoft.opendata.us.noaa.airtemperature import AirTemperature
from noaa-producer_data.microsoft.opendata.us.noaa.watertemperature import WaterTemperature
from noaa-producer_data.microsoft.opendata.us.noaa.wind import Wind
from noaa-producer_data.microsoft.opendata.us.noaa.humidity import Humidity
from noaa-producer_data.microsoft.opendata.us.noaa.conductivity import Conductivity
from noaa-producer_data.microsoft.opendata.us.noaa.salinity import Salinity
from noaa-producer_data.microsoft.opendata.us.noaa.station import Station
from noaa-producer_data.microsoft.opendata.us.noaa.visibility import Visibility
from noaa-producer_data.microsoft.opendata.us.noaa.currents import Currents
from noaa-producer_data.microsoft.opendata.us.noaa.currentpredictions import CurrentPredictions

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
        microsoft_open_data_usnoaaevent_producer = MicrosoftOpenDataUSNOAAEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaevent_producer = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.WaterLevel ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.WaterLevel event
    _water_level = WaterLevel()

    # sends the 'Microsoft.OpenData.US.NOAA.WaterLevel' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_water_level(data = _water_level)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.WaterLevel' event: {_water_level.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Predictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Predictions event
    _predictions = Predictions()

    # sends the 'Microsoft.OpenData.US.NOAA.Predictions' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_predictions(data = _predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Predictions' event: {_predictions.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.AirPressure ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.AirPressure event
    _air_pressure = AirPressure()

    # sends the 'Microsoft.OpenData.US.NOAA.AirPressure' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_air_pressure(data = _air_pressure)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.AirPressure' event: {_air_pressure.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.AirTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.AirTemperature event
    _air_temperature = AirTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.AirTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_air_temperature(data = _air_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.AirTemperature' event: {_air_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.WaterTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.WaterTemperature event
    _water_temperature = WaterTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.WaterTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_water_temperature(data = _water_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.WaterTemperature' event: {_water_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Wind ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Wind event
    _wind = Wind()

    # sends the 'Microsoft.OpenData.US.NOAA.Wind' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_wind(data = _wind)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Wind' event: {_wind.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Humidity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Humidity event
    _humidity = Humidity()

    # sends the 'Microsoft.OpenData.US.NOAA.Humidity' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_humidity(data = _humidity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Humidity' event: {_humidity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Conductivity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Conductivity event
    _conductivity = Conductivity()

    # sends the 'Microsoft.OpenData.US.NOAA.Conductivity' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_conductivity(data = _conductivity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Conductivity' event: {_conductivity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Salinity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Salinity event
    _salinity = Salinity()

    # sends the 'Microsoft.OpenData.US.NOAA.Salinity' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_salinity(data = _salinity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Salinity' event: {_salinity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Station ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Station event
    _station = Station()

    # sends the 'Microsoft.OpenData.US.NOAA.Station' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_station(data = _station)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Station' event: {_station.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Visibility ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Visibility event
    _visibility = Visibility()

    # sends the 'Microsoft.OpenData.US.NOAA.Visibility' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_visibility(_datacontenttype = 'TODO:replace',_subject = 'TODO:replace',_time = datetime.now().isoformat(),_dataschema = 'TODO:replace',data = _visibility)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Visibility' event: {_visibility.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Currents ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Currents event
    _currents = Currents()

    # sends the 'Microsoft.OpenData.US.NOAA.Currents' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_currents(data = _currents)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Currents' event: {_currents.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.CurrentPredictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.CurrentPredictions event
    _current_predictions = CurrentPredictions()

    # sends the 'Microsoft.OpenData.US.NOAA.CurrentPredictions' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_current_predictions(data = _current_predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.CurrentPredictions' event: {_current_predictions.to_json()}")

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