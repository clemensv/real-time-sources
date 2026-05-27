
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
from entsoe_mqtt_producer_data import *
from entsoe_mqtt_producer_mqtt_client.client import EuEntsoeTransparencyByDomainMqttProducer, EuEntsoeTransparencyByDomainMqttDispatcher

async def handle_eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices_data):
    """ Handles the eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices message """
    print(f"Received eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices_data}")

async def handle_eu_entsoe_transparency_by_domain_mqtt_actual_total_load(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_mqtt_actual_total_load_data):
    """ Handles the eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad message """
    print(f"Received eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_mqtt_actual_total_load_data}")

async def handle_eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin_data):
    """ Handles the eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin message """
    print(f"Received eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin_data}")

async def handle_eu_entsoe_transparency_by_domain_mqtt_generation_forecast(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_mqtt_generation_forecast_data):
    """ Handles the eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast message """
    print(f"Received eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_mqtt_generation_forecast_data}")

async def handle_eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information_data):
    """ Handles the eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation message """
    print(f"Received eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information_data}")

async def handle_eu_entsoe_transparency_by_domain_mqtt_actual_generation(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_mqtt_actual_generation_data):
    """ Handles the eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration message """
    print(f"Received eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_mqtt_actual_generation_data}")
from entsoe_mqtt_producer_mqtt_client.client import EuEntsoeTransparencyByDomainPsrTypeMqttProducer, EuEntsoeTransparencyByDomainPsrTypeMqttDispatcher

async def handle_eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type_data):
    """ Handles the eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType message """
    print(f"Received eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type_data}")

async def handle_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast_data):
    """ Handles the eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast message """
    print(f"Received eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast_data}")

async def handle_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation_data):
    """ Handles the eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration message """
    print(f"Received eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation_data}")

async def handle_eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type(mqtt_msg,cloud_event, eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type_data):
    """ Handles the eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType message """
    print(f"Received eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type_data}")
from entsoe_mqtt_producer_mqtt_client.client import EuEntsoeTransparencyCrossBorderMqttProducer, EuEntsoeTransparencyCrossBorderMqttDispatcher

async def handle_eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows(mqtt_msg,cloud_event, eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows_data):
    """ Handles the eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows message """
    print(f"Received eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows_data}")

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