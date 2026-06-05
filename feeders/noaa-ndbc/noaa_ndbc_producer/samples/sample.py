
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

from noaa_ndbc_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAANDBCEventProducer
from noaa_ndbc_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAANDBCMqttEventProducer
from noaa_ndbc_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAANDBCAmqpEventProducer

# imports for the data classes for each event

from noaa_ndbc_producer_data import BuoyObservation
from noaa_ndbc_producer_data import BuoyStation
from noaa_ndbc_producer_data import BuoySolarRadiationObservation
from noaa_ndbc_producer_data import BuoyOceanographicObservation
from noaa_ndbc_producer_data import BuoyDartMeasurement
from noaa_ndbc_producer_data import BuoyContinuousWindObservation
from noaa_ndbc_producer_data import BuoySupplementalMeasurement
from noaa_ndbc_producer_data import BuoyDetailedWaveSummary
from noaa_ndbc_producer_data import BuoyHourlyRainMeasurement

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
        microsoft_open_data_usnoaandbcevent_producer = MicrosoftOpenDataUSNOAANDBCEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaandbcevent_producer = MicrosoftOpenDataUSNOAANDBCEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation event
    _buoy_observation = BuoyObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_observation(_station_id = 'TODO: replace me', data = _buoy_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation' event: {_buoy_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoyStation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoyStation event
    _buoy_station = BuoyStation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyStation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_station(_station_id = 'TODO: replace me', data = _buoy_station)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoyStation' event: {_buoy_station.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation event
    _buoy_solar_radiation_observation = BuoySolarRadiationObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_solar_radiation_observation(_station_id = 'TODO: replace me', data = _buoy_solar_radiation_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation' event: {_buoy_solar_radiation_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation event
    _buoy_oceanographic_observation = BuoyOceanographicObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_oceanographic_observation(_station_id = 'TODO: replace me', data = _buoy_oceanographic_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation' event: {_buoy_oceanographic_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement event
    _buoy_dart_measurement = BuoyDartMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_dart_measurement(_station_id = 'TODO: replace me', data = _buoy_dart_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement' event: {_buoy_dart_measurement.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation event
    _buoy_continuous_wind_observation = BuoyContinuousWindObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_continuous_wind_observation(_station_id = 'TODO: replace me', data = _buoy_continuous_wind_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation' event: {_buoy_continuous_wind_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement event
    _buoy_supplemental_measurement = BuoySupplementalMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_supplemental_measurement(_station_id = 'TODO: replace me', data = _buoy_supplemental_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement' event: {_buoy_supplemental_measurement.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary event
    _buoy_detailed_wave_summary = BuoyDetailedWaveSummary()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_detailed_wave_summary(_station_id = 'TODO: replace me', data = _buoy_detailed_wave_summary)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary' event: {_buoy_detailed_wave_summary.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement event
    _buoy_hourly_rain_measurement = BuoyHourlyRainMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcevent_producer.send_microsoft_open_data_us_noaa_ndbc_buoy_hourly_rain_measurement(_station_id = 'TODO: replace me', data = _buoy_hourly_rain_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement' event: {_buoy_hourly_rain_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaandbcmqtt_event_producer = MicrosoftOpenDataUSNOAANDBCMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaandbcmqtt_event_producer = MicrosoftOpenDataUSNOAANDBCMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation event
    _buoy_observation = BuoyObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation(_station_id = 'TODO: replace me', data = _buoy_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation' event: {_buoy_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation event
    _buoy_station = BuoyStation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station(_station_id = 'TODO: replace me', data = _buoy_station)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation' event: {_buoy_station.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation event
    _buoy_solar_radiation_observation = BuoySolarRadiationObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation(_station_id = 'TODO: replace me', data = _buoy_solar_radiation_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation' event: {_buoy_solar_radiation_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation event
    _buoy_oceanographic_observation = BuoyOceanographicObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation(_station_id = 'TODO: replace me', data = _buoy_oceanographic_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation' event: {_buoy_oceanographic_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement event
    _buoy_dart_measurement = BuoyDartMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement(_station_id = 'TODO: replace me', data = _buoy_dart_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement' event: {_buoy_dart_measurement.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation event
    _buoy_continuous_wind_observation = BuoyContinuousWindObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation(_station_id = 'TODO: replace me', data = _buoy_continuous_wind_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation' event: {_buoy_continuous_wind_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement event
    _buoy_supplemental_measurement = BuoySupplementalMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement(_station_id = 'TODO: replace me', data = _buoy_supplemental_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement' event: {_buoy_supplemental_measurement.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary event
    _buoy_detailed_wave_summary = BuoyDetailedWaveSummary()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary(_station_id = 'TODO: replace me', data = _buoy_detailed_wave_summary)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary' event: {_buoy_detailed_wave_summary.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement event
    _buoy_hourly_rain_measurement = BuoyHourlyRainMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcmqtt_event_producer.send_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement(_station_id = 'TODO: replace me', data = _buoy_hourly_rain_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement' event: {_buoy_hourly_rain_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        microsoft_open_data_usnoaandbcamqp_event_producer = MicrosoftOpenDataUSNOAANDBCAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        microsoft_open_data_usnoaandbcamqp_event_producer = MicrosoftOpenDataUSNOAANDBCAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyObservation event
    _buoy_observation = BuoyObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_observation(_station_id = 'TODO: replace me', data = _buoy_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyObservation' event: {_buoy_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyStation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyStation event
    _buoy_station = BuoyStation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyStation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_station(_station_id = 'TODO: replace me', data = _buoy_station)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyStation' event: {_buoy_station.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySolarRadiationObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySolarRadiationObservation event
    _buoy_solar_radiation_observation = BuoySolarRadiationObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySolarRadiationObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_solar_radiation_observation(_station_id = 'TODO: replace me', data = _buoy_solar_radiation_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySolarRadiationObservation' event: {_buoy_solar_radiation_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyOceanographicObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyOceanographicObservation event
    _buoy_oceanographic_observation = BuoyOceanographicObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyOceanographicObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_oceanographic_observation(_station_id = 'TODO: replace me', data = _buoy_oceanographic_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyOceanographicObservation' event: {_buoy_oceanographic_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDartMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDartMeasurement event
    _buoy_dart_measurement = BuoyDartMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDartMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_dart_measurement(_station_id = 'TODO: replace me', data = _buoy_dart_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDartMeasurement' event: {_buoy_dart_measurement.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyContinuousWindObservation ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyContinuousWindObservation event
    _buoy_continuous_wind_observation = BuoyContinuousWindObservation()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyContinuousWindObservation' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_continuous_wind_observation(_station_id = 'TODO: replace me', data = _buoy_continuous_wind_observation)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyContinuousWindObservation' event: {_buoy_continuous_wind_observation.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySupplementalMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySupplementalMeasurement event
    _buoy_supplemental_measurement = BuoySupplementalMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySupplementalMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_supplemental_measurement(_station_id = 'TODO: replace me', data = _buoy_supplemental_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoySupplementalMeasurement' event: {_buoy_supplemental_measurement.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDetailedWaveSummary ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDetailedWaveSummary event
    _buoy_detailed_wave_summary = BuoyDetailedWaveSummary()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDetailedWaveSummary' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_detailed_wave_summary(_station_id = 'TODO: replace me', data = _buoy_detailed_wave_summary)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyDetailedWaveSummary' event: {_buoy_detailed_wave_summary.to_json()}")

    # ---- Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyHourlyRainMeasurement ----
    # TODO: Supply event data for the Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyHourlyRainMeasurement event
    _buoy_hourly_rain_measurement = BuoyHourlyRainMeasurement()

    # sends the 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyHourlyRainMeasurement' event to Kafka topic.
    await microsoft_open_data_usnoaandbcamqp_event_producer.send_microsoft_open_data_us_noaa_ndbc_amqp_buoy_hourly_rain_measurement(_station_id = 'TODO: replace me', data = _buoy_hourly_rain_measurement)
    print(f"Sent 'Microsoft.OpenData.US.NOAA.NDBC.amqp.BuoyHourlyRainMeasurement' event: {_buoy_hourly_rain_measurement.to_json()}")

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