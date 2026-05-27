
"""
This is sample code to use the MQTT client contained in this project.

The sample demonstrates both publishing and subscribing to MQTT messages with
the
producer and dispatcher functionality.

There is a handler for each defined message type. The handler is an async
function that takes the following parameters:
- mqtt_message: The paho.mqtt.client.MQTTMessage object (message context).
- cloud_event: The CloudEvent data (if using CloudEvents).
- message_data: The deserialized message data.The main function creates a client
that can both produce and consume messages.
It starts a dispatcher to handle incoming messages and then publishes sample
messages.

The script either reads the configuration from the command line or uses the
environment variables. The following environment variables are recognized:

- MQTT_BROKER_HOST: The MQTT broker hostname.
- MQTT_BROKER_PORT: The MQTT broker port (default: 1883).
- MQTT_TOPIC: The MQTT topic to publish/subscribe to.
- MQTT_USERNAME: The MQTT username (optional).
- MQTT_PASSWORD: The MQTT password (optional).

Alternatively, you can pass the configuration as command-line arguments.

python sample.py --broker-host <broker_host> --broker-port <broker_port> --topic
<topic>

The main function waits for a signal (Press Ctrl+C) to stop.
"""

import argparse
import asyncio
import os
import signal
from noaa_ndbc_mqtt_producer_data import *
from noaa_ndbc_mqtt_producer_mqtt_client.client import MicrosoftOpenDataUSNOAANDBCMqttProducer, MicrosoftOpenDataUSNOAANDBCMqttDispatcher

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary_data}")

async def handle_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement(mqtt_msg,cloud_event, microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement_data):
    """ Handles the Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement message """
    print(f"Received Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement_data}")

async def main(broker_host, broker_port, topic, username=None, password=None):
    """ Main function for MQTT client """
    print(f"Connecting to {broker_host}:{broker_port}...")
    print(f"Topic: {topic}")
    print("Press Ctrl+C to stop\n")
    
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, lambda: stop_event.set())
    loop.add_signal_handler(signal.SIGINT, lambda: stop_event.set())
    
    await stop_event.wait()
    print("\nStopping...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Client")
    parser.add_argument('--broker-host', default=os.getenv('MQTT_BROKER_HOST', 'localhost'), help='MQTT broker hostname')
    parser.add_argument('--broker-port', type=int, default=int(os.getenv('MQTT_BROKER_PORT', '1883')), help='MQTT broker port')
    parser.add_argument('--topic', default=os.getenv('MQTT_TOPIC', 'testtopic'), help='MQTT topic')
    parser.add_argument('--username', default=os.getenv('MQTT_USERNAME'), help='MQTT username (optional)')
    parser.add_argument('--password', default=os.getenv('MQTT_PASSWORD'), help='MQTT password (optional)')

    args = parser.parse_args()

    asyncio.run(main(
        args.broker_host,
        args.broker_port,
        args.topic,
        args.username,
        args.password
    ))