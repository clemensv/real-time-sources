
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
from wsdot_mqtt_producer_data import *
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotTrafficMqttProducer, UsWaWsdotTrafficMqttDispatcher

async def handle_us_wa_wsdot_traffic_traffic_flow_station_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_traffic_traffic_flow_station_mqtt_data):
    """ Handles the us.wa.wsdot.traffic.TrafficFlowStation.mqtt message """
    print(f"Received us.wa.wsdot.traffic.TrafficFlowStation.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_traffic_traffic_flow_station_mqtt_data}")

async def handle_us_wa_wsdot_traffic_traffic_flow_reading_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_traffic_traffic_flow_reading_mqtt_data):
    """ Handles the us.wa.wsdot.traffic.TrafficFlowReading.mqtt message """
    print(f"Received us.wa.wsdot.traffic.TrafficFlowReading.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_traffic_traffic_flow_reading_mqtt_data}")
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotTraveltimesMqttProducer, UsWaWsdotTraveltimesMqttDispatcher

async def handle_us_wa_wsdot_traveltimes_travel_time_route_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_traveltimes_travel_time_route_mqtt_data):
    """ Handles the us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt message """
    print(f"Received us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_traveltimes_travel_time_route_mqtt_data}")
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotMountainpassMqttProducer, UsWaWsdotMountainpassMqttDispatcher

async def handle_us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt_data):
    """ Handles the us.wa.wsdot.mountainpass.MountainPassCondition.mqtt message """
    print(f"Received us.wa.wsdot.mountainpass.MountainPassCondition.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt_data}")
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotWeatherMqttProducer, UsWaWsdotWeatherMqttDispatcher

async def handle_us_wa_wsdot_weather_weather_station_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_weather_weather_station_mqtt_data):
    """ Handles the us.wa.wsdot.weather.WeatherStation.mqtt message """
    print(f"Received us.wa.wsdot.weather.WeatherStation.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_weather_weather_station_mqtt_data}")

async def handle_us_wa_wsdot_weather_weather_reading_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_weather_weather_reading_mqtt_data):
    """ Handles the us.wa.wsdot.weather.WeatherReading.mqtt message """
    print(f"Received us.wa.wsdot.weather.WeatherReading.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_weather_weather_reading_mqtt_data}")
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotTollsMqttProducer, UsWaWsdotTollsMqttDispatcher

async def handle_us_wa_wsdot_tolls_toll_rate_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_tolls_toll_rate_mqtt_data):
    """ Handles the us.wa.wsdot.tolls.TollRate.mqtt message """
    print(f"Received us.wa.wsdot.tolls.TollRate.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_tolls_toll_rate_mqtt_data}")
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotCvrestrictionsMqttProducer, UsWaWsdotCvrestrictionsMqttDispatcher

async def handle_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt_data):
    """ Handles the us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt message """
    print(f"Received us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt_data}")
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotBorderMqttProducer, UsWaWsdotBorderMqttDispatcher

async def handle_us_wa_wsdot_border_border_crossing_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_border_border_crossing_mqtt_data):
    """ Handles the us.wa.wsdot.border.BorderCrossing.mqtt message """
    print(f"Received us.wa.wsdot.border.BorderCrossing.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_border_border_crossing_mqtt_data}")
from wsdot_mqtt_producer_mqtt_client.client import UsWaWsdotFerriesMqttProducer, UsWaWsdotFerriesMqttDispatcher

async def handle_us_wa_wsdot_ferries_vessel_location_mqtt(mqtt_msg,cloud_event, us_wa_wsdot_ferries_vessel_location_mqtt_data):
    """ Handles the us.wa.wsdot.ferries.VesselLocation.mqtt message """
    print(f"Received us.wa.wsdot.ferries.VesselLocation.mqtt on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {us_wa_wsdot_ferries_vessel_location_mqtt_data}")

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