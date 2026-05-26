
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

from noaa_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAEventProducer
from noaa_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAMqttEventProducer
from noaa_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAAmqpEventProducer

# imports for the data classes for each event

from noaa_producer_data.waterlevel import WaterLevel
from noaa_producer_data.predictions import Predictions
from noaa_producer_data.airpressure import AirPressure
from noaa_producer_data.airtemperature import AirTemperature
from noaa_producer_data.watertemperature import WaterTemperature
from noaa_producer_data.wind import Wind
from noaa_producer_data.humidity import Humidity
from noaa_producer_data.conductivity import Conductivity
from noaa_producer_data.salinity import Salinity
from noaa_producer_data.station import Station
from noaa_producer_data.visibility import Visibility
from noaa_producer_data.currents import Currents
from noaa_producer_data.currentpredictions import CurrentPredictions

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
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_water_level(_station_id = 'TODO: replace me', data = _water_level)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.WaterLevel' event: {_water_level.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Predictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Predictions event
    _predictions = Predictions()

    # sends the 'Microsoft.OpenData.US.NOAA.Predictions' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_predictions(_station_id = 'TODO: replace me', data = _predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Predictions' event: {_predictions.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.AirPressure ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.AirPressure event
    _air_pressure = AirPressure()

    # sends the 'Microsoft.OpenData.US.NOAA.AirPressure' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_air_pressure(_station_id = 'TODO: replace me', data = _air_pressure)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.AirPressure' event: {_air_pressure.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.AirTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.AirTemperature event
    _air_temperature = AirTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.AirTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_air_temperature(_station_id = 'TODO: replace me', data = _air_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.AirTemperature' event: {_air_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.WaterTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.WaterTemperature event
    _water_temperature = WaterTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.WaterTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_water_temperature(_station_id = 'TODO: replace me', data = _water_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.WaterTemperature' event: {_water_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Wind ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Wind event
    _wind = Wind()

    # sends the 'Microsoft.OpenData.US.NOAA.Wind' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_wind(_station_id = 'TODO: replace me', data = _wind)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Wind' event: {_wind.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Humidity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Humidity event
    _humidity = Humidity()

    # sends the 'Microsoft.OpenData.US.NOAA.Humidity' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_humidity(_station_id = 'TODO: replace me', data = _humidity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Humidity' event: {_humidity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Conductivity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Conductivity event
    _conductivity = Conductivity()

    # sends the 'Microsoft.OpenData.US.NOAA.Conductivity' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_conductivity(_station_id = 'TODO: replace me', data = _conductivity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Conductivity' event: {_conductivity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Salinity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Salinity event
    _salinity = Salinity()

    # sends the 'Microsoft.OpenData.US.NOAA.Salinity' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_salinity(_station_id = 'TODO: replace me', data = _salinity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Salinity' event: {_salinity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Station ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Station event
    _station = Station()

    # sends the 'Microsoft.OpenData.US.NOAA.Station' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_station(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Station' event: {_station.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Visibility ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Visibility event
    _visibility = Visibility()

    # sends the 'Microsoft.OpenData.US.NOAA.Visibility' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_visibility(_datacontenttype = 'TODO:replace',_time = datetime.now().isoformat(),_dataschema = 'TODO:replace',_station_id = 'TODO: replace me', data = _visibility)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Visibility' event: {_visibility.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.Currents ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.Currents event
    _currents = Currents()

    # sends the 'Microsoft.OpenData.US.NOAA.Currents' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_currents(_station_id = 'TODO: replace me', data = _currents)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.Currents' event: {_currents.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.CurrentPredictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.CurrentPredictions event
    _current_predictions = CurrentPredictions()

    # sends the 'Microsoft.OpenData.US.NOAA.CurrentPredictions' event to Kafka topic.
    await microsoft_open_data_usnoaaevent_producer.send_microsoft_open_data_us_noaa_current_predictions(_station_id = 'TODO: replace me', data = _current_predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.CurrentPredictions' event: {_current_predictions.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaamqtt_event_producer = MicrosoftOpenDataUSNOAAMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaamqtt_event_producer = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.mqtt.WaterLevel ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.WaterLevel event
    _water_level = WaterLevel()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.WaterLevel' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_water_level(_station_id = 'TODO: replace me', data = _water_level)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.WaterLevel' event: {_water_level.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Predictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Predictions event
    _predictions = Predictions()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Predictions' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_predictions(_station_id = 'TODO: replace me', data = _predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Predictions' event: {_predictions.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.AirPressure ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.AirPressure event
    _air_pressure = AirPressure()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.AirPressure' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_air_pressure(_station_id = 'TODO: replace me', data = _air_pressure)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.AirPressure' event: {_air_pressure.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.AirTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.AirTemperature event
    _air_temperature = AirTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.AirTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_air_temperature(_station_id = 'TODO: replace me', data = _air_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.AirTemperature' event: {_air_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature event
    _water_temperature = WaterTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_water_temperature(_station_id = 'TODO: replace me', data = _water_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature' event: {_water_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Wind ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Wind event
    _wind = Wind()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Wind' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_wind(_station_id = 'TODO: replace me', data = _wind)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Wind' event: {_wind.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Humidity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Humidity event
    _humidity = Humidity()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Humidity' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_humidity(_station_id = 'TODO: replace me', data = _humidity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Humidity' event: {_humidity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Conductivity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Conductivity event
    _conductivity = Conductivity()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Conductivity' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_conductivity(_station_id = 'TODO: replace me', data = _conductivity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Conductivity' event: {_conductivity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Salinity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Salinity event
    _salinity = Salinity()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Salinity' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_salinity(_station_id = 'TODO: replace me', data = _salinity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Salinity' event: {_salinity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Station ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Station event
    _station = Station()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Station' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_station(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Station' event: {_station.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Visibility ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Visibility event
    _visibility = Visibility()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Visibility' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_visibility(_datacontenttype = 'TODO:replace',_time = datetime.now().isoformat(),_dataschema = 'TODO:replace',_station_id = 'TODO: replace me', data = _visibility)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Visibility' event: {_visibility.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.Currents ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.Currents event
    _currents = Currents()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.Currents' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_currents(_station_id = 'TODO: replace me', data = _currents)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.Currents' event: {_currents.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions event
    _current_predictions = CurrentPredictions()

    # sends the 'Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions' event to Kafka topic.
    await microsoft_open_data_usnoaamqtt_event_producer.send_microsoft_open_data_us_noaa_mqtt_current_predictions(_station_id = 'TODO: replace me', data = _current_predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions' event: {_current_predictions.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaaamqp_event_producer = MicrosoftOpenDataUSNOAAAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaaamqp_event_producer = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.amqp.WaterLevel ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.WaterLevel event
    _water_level = WaterLevel()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.WaterLevel' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_water_level(_station_id = 'TODO: replace me', data = _water_level)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.WaterLevel' event: {_water_level.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Predictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Predictions event
    _predictions = Predictions()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Predictions' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_predictions(_station_id = 'TODO: replace me', data = _predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Predictions' event: {_predictions.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.AirPressure ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.AirPressure event
    _air_pressure = AirPressure()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.AirPressure' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_air_pressure(_station_id = 'TODO: replace me', data = _air_pressure)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.AirPressure' event: {_air_pressure.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.AirTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.AirTemperature event
    _air_temperature = AirTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.AirTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_air_temperature(_station_id = 'TODO: replace me', data = _air_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.AirTemperature' event: {_air_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.WaterTemperature ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.WaterTemperature event
    _water_temperature = WaterTemperature()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.WaterTemperature' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_water_temperature(_station_id = 'TODO: replace me', data = _water_temperature)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.WaterTemperature' event: {_water_temperature.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Wind ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Wind event
    _wind = Wind()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Wind' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_wind(_station_id = 'TODO: replace me', data = _wind)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Wind' event: {_wind.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Humidity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Humidity event
    _humidity = Humidity()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Humidity' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_humidity(_station_id = 'TODO: replace me', data = _humidity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Humidity' event: {_humidity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Conductivity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Conductivity event
    _conductivity = Conductivity()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Conductivity' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_conductivity(_station_id = 'TODO: replace me', data = _conductivity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Conductivity' event: {_conductivity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Salinity ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Salinity event
    _salinity = Salinity()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Salinity' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_salinity(_station_id = 'TODO: replace me', data = _salinity)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Salinity' event: {_salinity.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Station ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Station event
    _station = Station()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Station' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_station(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Station' event: {_station.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Visibility ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Visibility event
    _visibility = Visibility()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Visibility' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_visibility(_datacontenttype = 'TODO:replace',_time = datetime.now().isoformat(),_dataschema = 'TODO:replace',_station_id = 'TODO: replace me', data = _visibility)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Visibility' event: {_visibility.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.Currents ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.Currents event
    _currents = Currents()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.Currents' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_currents(_station_id = 'TODO: replace me', data = _currents)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.Currents' event: {_currents.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.amqp.CurrentPredictions ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.amqp.CurrentPredictions event
    _current_predictions = CurrentPredictions()

    # sends the 'Microsoft.OpenData.US.NOAA.amqp.CurrentPredictions' event to Kafka topic.
    await microsoft_open_data_usnoaaamqp_event_producer.send_microsoft_open_data_us_noaa_amqp_current_predictions(_station_id = 'TODO: replace me', data = _current_predictions)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.amqp.CurrentPredictions' event: {_current_predictions.to_json()}")

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