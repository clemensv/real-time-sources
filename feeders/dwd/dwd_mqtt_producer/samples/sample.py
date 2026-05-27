
"""
This is sample code to use the MQTT clients contained in this project.

The sample demonstrates both publishing and subscribing to MQTT messages with
the
producer and dispatcher functionality.

There is a handler for each defined message type. The handler is an async
function that takes the following parameters:
- mqtt_message: The paho.mqtt.client.MQTTMessage object (message context).
- cloud_event: The CloudEvent data (if using CloudEvents).
- message_data: The deserialized message data.The main function creates clients
for each message group that can both produce and consume messages.
It starts dispatchers to handle incoming messages and then publishes sample
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
from dwd_mqtt_producer_data import *
from dwd_mqtt_producer_mqtt_client.client import DEDWDCDCMqttProducer, DEDWDCDCMqttDispatcher

async def handle_de_dwd_cdc_mqtt_station_metadata(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_station_metadata_data):
    """ Handles the DE.DWD.CDC.mqtt.StationMetadata message """
    print(f"Received DE.DWD.CDC.mqtt.StationMetadata on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_station_metadata_data}")

async def handle_de_dwd_cdc_mqtt_air_temperature10_min(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_air_temperature10_min_data):
    """ Handles the DE.DWD.CDC.mqtt.AirTemperature10Min message """
    print(f"Received DE.DWD.CDC.mqtt.AirTemperature10Min on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_air_temperature10_min_data}")

async def handle_de_dwd_cdc_mqtt_precipitation10_min(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_precipitation10_min_data):
    """ Handles the DE.DWD.CDC.mqtt.Precipitation10Min message """
    print(f"Received DE.DWD.CDC.mqtt.Precipitation10Min on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_precipitation10_min_data}")

async def handle_de_dwd_cdc_mqtt_wind10_min(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_wind10_min_data):
    """ Handles the DE.DWD.CDC.mqtt.Wind10Min message """
    print(f"Received DE.DWD.CDC.mqtt.Wind10Min on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_wind10_min_data}")

async def handle_de_dwd_cdc_mqtt_solar10_min(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_solar10_min_data):
    """ Handles the DE.DWD.CDC.mqtt.Solar10Min message """
    print(f"Received DE.DWD.CDC.mqtt.Solar10Min on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_solar10_min_data}")

async def handle_de_dwd_cdc_mqtt_hourly_observation(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_hourly_observation_data):
    """ Handles the DE.DWD.CDC.mqtt.HourlyObservation message """
    print(f"Received DE.DWD.CDC.mqtt.HourlyObservation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_hourly_observation_data}")

async def handle_de_dwd_cdc_mqtt_extreme_wind10_min(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_extreme_wind10_min_data):
    """ Handles the DE.DWD.CDC.mqtt.ExtremeWind10Min message """
    print(f"Received DE.DWD.CDC.mqtt.ExtremeWind10Min on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_extreme_wind10_min_data}")

async def handle_de_dwd_cdc_mqtt_extreme_temperature10_min(mqtt_msg,cloud_event, de_dwd_cdc_mqtt_extreme_temperature10_min_data):
    """ Handles the DE.DWD.CDC.mqtt.ExtremeTemperature10Min message """
    print(f"Received DE.DWD.CDC.mqtt.ExtremeTemperature10Min on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_cdc_mqtt_extreme_temperature10_min_data}")
from dwd_mqtt_producer_mqtt_client.client import DEDWDWeatherMqttProducer, DEDWDWeatherMqttDispatcher

async def handle_de_dwd_weather_mqtt_alert(mqtt_msg,cloud_event, de_dwd_weather_mqtt_alert_data):
    """ Handles the DE.DWD.Weather.mqtt.Alert message """
    print(f"Received DE.DWD.Weather.mqtt.Alert on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_weather_mqtt_alert_data}")
from dwd_mqtt_producer_mqtt_client.client import DEDWDRadarMqttProducer, DEDWDRadarMqttDispatcher

async def handle_de_dwd_radar_mqtt_radar_product_catalog(mqtt_msg,cloud_event, de_dwd_radar_mqtt_radar_product_catalog_data):
    """ Handles the DE.DWD.Radar.mqtt.RadarProductCatalog message """
    print(f"Received DE.DWD.Radar.mqtt.RadarProductCatalog on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_radar_mqtt_radar_product_catalog_data}")

async def handle_de_dwd_radar_mqtt_radar_file_product(mqtt_msg,cloud_event, de_dwd_radar_mqtt_radar_file_product_data):
    """ Handles the DE.DWD.Radar.mqtt.RadarFileProduct message """
    print(f"Received DE.DWD.Radar.mqtt.RadarFileProduct on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_radar_mqtt_radar_file_product_data}")
from dwd_mqtt_producer_mqtt_client.client import DEDWDForecastMqttProducer, DEDWDForecastMqttDispatcher

async def handle_de_dwd_forecast_mqtt_forecast_model_catalog(mqtt_msg,cloud_event, de_dwd_forecast_mqtt_forecast_model_catalog_data):
    """ Handles the DE.DWD.Forecast.mqtt.ForecastModelCatalog message """
    print(f"Received DE.DWD.Forecast.mqtt.ForecastModelCatalog on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_forecast_mqtt_forecast_model_catalog_data}")

async def handle_de_dwd_forecast_mqtt_icon_d2_forecast_file(mqtt_msg,cloud_event, de_dwd_forecast_mqtt_icon_d2_forecast_file_data):
    """ Handles the DE.DWD.Forecast.mqtt.IconD2ForecastFile message """
    print(f"Received DE.DWD.Forecast.mqtt.IconD2ForecastFile on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {de_dwd_forecast_mqtt_icon_d2_forecast_file_data}")

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