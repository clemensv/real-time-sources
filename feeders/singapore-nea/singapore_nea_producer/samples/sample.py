
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

from singapore_nea_producer_kafka_producer.producer import SGGovNEAWeatherEventProducer
from singapore_nea_producer_kafka_producer.producer import SGGovNEAAirQualityEventProducer
from singapore_nea_producer_kafka_producer.producer import SGGovNEAWeatherMqttEventProducer
from singapore_nea_producer_kafka_producer.producer import SGGovNEAAirQualityMqttEventProducer
from singapore_nea_producer_kafka_producer.producer import SGGovNEAWeatherAmqpEventProducer
from singapore_nea_producer_kafka_producer.producer import SGGovNEAAirQualityAmqpEventProducer

# imports for the data classes for each event

from singapore_nea_producer_data import Station
from singapore_nea_producer_data import WeatherObservation
from singapore_nea_producer_data import Region
from singapore_nea_producer_data import PSIReading
from singapore_nea_producer_data import PM25Reading

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
        sggov_neaweather_event_producer = SGGovNEAWeatherEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        sggov_neaweather_event_producer = SGGovNEAWeatherEventProducer(kafka_producer, topic, 'binary')

    # ---- SG.Gov.NEA.Weather.Station ----
    # TODO: Supply event data for the SG.Gov.NEA.Weather.Station event
    _station = Station()

    # sends the 'SG.Gov.NEA.Weather.Station' event to Kafka topic.
    await sggov_neaweather_event_producer.send_sg_gov_nea_weather_station(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'SG.Gov.NEA.Weather.Station' event: {_station.to_json()}")

    # ---- SG.Gov.NEA.Weather.WeatherObservation ----
    # TODO: Supply event data for the SG.Gov.NEA.Weather.WeatherObservation event
    _weather_observation = WeatherObservation()

    # sends the 'SG.Gov.NEA.Weather.WeatherObservation' event to Kafka topic.
    await sggov_neaweather_event_producer.send_sg_gov_nea_weather_weather_observation(_station_id = 'TODO: replace me', data = _weather_observation)
    print(f"Sent 'SG.Gov.NEA.Weather.WeatherObservation' event: {_weather_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        sggov_neaair_quality_event_producer = SGGovNEAAirQualityEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        sggov_neaair_quality_event_producer = SGGovNEAAirQualityEventProducer(kafka_producer, topic, 'binary')

    # ---- SG.Gov.NEA.AirQuality.Region ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.Region event
    _region = Region()

    # sends the 'SG.Gov.NEA.AirQuality.Region' event to Kafka topic.
    await sggov_neaair_quality_event_producer.send_sg_gov_nea_air_quality_region(_region = 'TODO: replace me', data = _region)
    print(f"Sent 'SG.Gov.NEA.AirQuality.Region' event: {_region.to_json()}")

    # ---- SG.Gov.NEA.AirQuality.PSIReading ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.PSIReading event
    _psireading = PSIReading()

    # sends the 'SG.Gov.NEA.AirQuality.PSIReading' event to Kafka topic.
    await sggov_neaair_quality_event_producer.send_sg_gov_nea_air_quality_psireading(_region = 'TODO: replace me', data = _psireading)
    print(f"Sent 'SG.Gov.NEA.AirQuality.PSIReading' event: {_psireading.to_json()}")

    # ---- SG.Gov.NEA.AirQuality.PM25Reading ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.PM25Reading event
    _pm25_reading = PM25Reading()

    # sends the 'SG.Gov.NEA.AirQuality.PM25Reading' event to Kafka topic.
    await sggov_neaair_quality_event_producer.send_sg_gov_nea_air_quality_pm25_reading(_region = 'TODO: replace me', data = _pm25_reading)
    print(f"Sent 'SG.Gov.NEA.AirQuality.PM25Reading' event: {_pm25_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        sggov_neaweather_mqtt_event_producer = SGGovNEAWeatherMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        sggov_neaweather_mqtt_event_producer = SGGovNEAWeatherMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- SG.Gov.NEA.Weather.Station.mqtt ----
    # TODO: Supply event data for the SG.Gov.NEA.Weather.Station.mqtt event
    _station = Station()

    # sends the 'SG.Gov.NEA.Weather.Station.mqtt' event to Kafka topic.
    await sggov_neaweather_mqtt_event_producer.send_sg_gov_nea_weather_station_mqtt(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'SG.Gov.NEA.Weather.Station.mqtt' event: {_station.to_json()}")

    # ---- SG.Gov.NEA.Weather.WeatherObservation.mqtt ----
    # TODO: Supply event data for the SG.Gov.NEA.Weather.WeatherObservation.mqtt event
    _weather_observation = WeatherObservation()

    # sends the 'SG.Gov.NEA.Weather.WeatherObservation.mqtt' event to Kafka topic.
    await sggov_neaweather_mqtt_event_producer.send_sg_gov_nea_weather_weather_observation_mqtt(_station_id = 'TODO: replace me', data = _weather_observation)
    print(f"Sent 'SG.Gov.NEA.Weather.WeatherObservation.mqtt' event: {_weather_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        sggov_neaair_quality_mqtt_event_producer = SGGovNEAAirQualityMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        sggov_neaair_quality_mqtt_event_producer = SGGovNEAAirQualityMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- SG.Gov.NEA.AirQuality.Region.mqtt ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.Region.mqtt event
    _region = Region()

    # sends the 'SG.Gov.NEA.AirQuality.Region.mqtt' event to Kafka topic.
    await sggov_neaair_quality_mqtt_event_producer.send_sg_gov_nea_air_quality_region_mqtt(_region = 'TODO: replace me', data = _region)
    print(f"Sent 'SG.Gov.NEA.AirQuality.Region.mqtt' event: {_region.to_json()}")

    # ---- SG.Gov.NEA.AirQuality.PSIReading.mqtt ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.PSIReading.mqtt event
    _psireading = PSIReading()

    # sends the 'SG.Gov.NEA.AirQuality.PSIReading.mqtt' event to Kafka topic.
    await sggov_neaair_quality_mqtt_event_producer.send_sg_gov_nea_air_quality_psireading_mqtt(_region = 'TODO: replace me', data = _psireading)
    print(f"Sent 'SG.Gov.NEA.AirQuality.PSIReading.mqtt' event: {_psireading.to_json()}")

    # ---- SG.Gov.NEA.AirQuality.PM25Reading.mqtt ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.PM25Reading.mqtt event
    _pm25_reading = PM25Reading()

    # sends the 'SG.Gov.NEA.AirQuality.PM25Reading.mqtt' event to Kafka topic.
    await sggov_neaair_quality_mqtt_event_producer.send_sg_gov_nea_air_quality_pm25_reading_mqtt(_region = 'TODO: replace me', data = _pm25_reading)
    print(f"Sent 'SG.Gov.NEA.AirQuality.PM25Reading.mqtt' event: {_pm25_reading.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        sggov_neaweather_amqp_event_producer = SGGovNEAWeatherAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        sggov_neaweather_amqp_event_producer = SGGovNEAWeatherAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- SG.Gov.NEA.Weather.Station.amqp ----
    # TODO: Supply event data for the SG.Gov.NEA.Weather.Station.amqp event
    _station = Station()

    # sends the 'SG.Gov.NEA.Weather.Station.amqp' event to Kafka topic.
    await sggov_neaweather_amqp_event_producer.send_sg_gov_nea_weather_station_amqp(_station_id = 'TODO: replace me', data = _station)
    print(f"Sent 'SG.Gov.NEA.Weather.Station.amqp' event: {_station.to_json()}")

    # ---- SG.Gov.NEA.Weather.WeatherObservation.amqp ----
    # TODO: Supply event data for the SG.Gov.NEA.Weather.WeatherObservation.amqp event
    _weather_observation = WeatherObservation()

    # sends the 'SG.Gov.NEA.Weather.WeatherObservation.amqp' event to Kafka topic.
    await sggov_neaweather_amqp_event_producer.send_sg_gov_nea_weather_weather_observation_amqp(_station_id = 'TODO: replace me', data = _weather_observation)
    print(f"Sent 'SG.Gov.NEA.Weather.WeatherObservation.amqp' event: {_weather_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        sggov_neaair_quality_amqp_event_producer = SGGovNEAAirQualityAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        sggov_neaair_quality_amqp_event_producer = SGGovNEAAirQualityAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- SG.Gov.NEA.AirQuality.Region.amqp ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.Region.amqp event
    _region = Region()

    # sends the 'SG.Gov.NEA.AirQuality.Region.amqp' event to Kafka topic.
    await sggov_neaair_quality_amqp_event_producer.send_sg_gov_nea_air_quality_region_amqp(_region = 'TODO: replace me', data = _region)
    print(f"Sent 'SG.Gov.NEA.AirQuality.Region.amqp' event: {_region.to_json()}")

    # ---- SG.Gov.NEA.AirQuality.PSIReading.amqp ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.PSIReading.amqp event
    _psireading = PSIReading()

    # sends the 'SG.Gov.NEA.AirQuality.PSIReading.amqp' event to Kafka topic.
    await sggov_neaair_quality_amqp_event_producer.send_sg_gov_nea_air_quality_psireading_amqp(_region = 'TODO: replace me', data = _psireading)
    print(f"Sent 'SG.Gov.NEA.AirQuality.PSIReading.amqp' event: {_psireading.to_json()}")

    # ---- SG.Gov.NEA.AirQuality.PM25Reading.amqp ----
    # TODO: Supply event data for the SG.Gov.NEA.AirQuality.PM25Reading.amqp event
    _pm25_reading = PM25Reading()

    # sends the 'SG.Gov.NEA.AirQuality.PM25Reading.amqp' event to Kafka topic.
    await sggov_neaair_quality_amqp_event_producer.send_sg_gov_nea_air_quality_pm25_reading_amqp(_region = 'TODO: replace me', data = _pm25_reading)
    print(f"Sent 'SG.Gov.NEA.AirQuality.PM25Reading.amqp' event: {_pm25_reading.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c', '--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))