
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
from digitraffic_road_mqtt_producer_data import *
from digitraffic_road_mqtt_producer_mqtt_client.client import FiDigitrafficRoadMqttProducer, FiDigitrafficRoadMqttDispatcher

async def handle_fi_digitraffic_road_mqtt_tms_sensor_data(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_tms_sensor_data_data):
    """ Handles the fi.digitraffic.road.mqtt.TmsSensorData message """
    print(f"Received fi.digitraffic.road.mqtt.TmsSensorData on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_tms_sensor_data_data}")

async def handle_fi_digitraffic_road_mqtt_weather_sensor_data(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_weather_sensor_data_data):
    """ Handles the fi.digitraffic.road.mqtt.WeatherSensorData message """
    print(f"Received fi.digitraffic.road.mqtt.WeatherSensorData on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_weather_sensor_data_data}")

async def handle_fi_digitraffic_road_mqtt_traffic_announcement(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_traffic_announcement_data):
    """ Handles the fi.digitraffic.road.mqtt.TrafficAnnouncement message """
    print(f"Received fi.digitraffic.road.mqtt.TrafficAnnouncement on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_traffic_announcement_data}")

async def handle_fi_digitraffic_road_mqtt_road_work(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_road_work_data):
    """ Handles the fi.digitraffic.road.mqtt.RoadWork message """
    print(f"Received fi.digitraffic.road.mqtt.RoadWork on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_road_work_data}")

async def handle_fi_digitraffic_road_mqtt_weight_restriction(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_weight_restriction_data):
    """ Handles the fi.digitraffic.road.mqtt.WeightRestriction message """
    print(f"Received fi.digitraffic.road.mqtt.WeightRestriction on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_weight_restriction_data}")

async def handle_fi_digitraffic_road_mqtt_exempted_transport(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_exempted_transport_data):
    """ Handles the fi.digitraffic.road.mqtt.ExemptedTransport message """
    print(f"Received fi.digitraffic.road.mqtt.ExemptedTransport on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_exempted_transport_data}")

async def handle_fi_digitraffic_road_mqtt_maintenance_tracking(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_maintenance_tracking_data):
    """ Handles the fi.digitraffic.road.mqtt.MaintenanceTracking message """
    print(f"Received fi.digitraffic.road.mqtt.MaintenanceTracking on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_maintenance_tracking_data}")

async def handle_fi_digitraffic_road_mqtt_tms_station(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_tms_station_data):
    """ Handles the fi.digitraffic.road.mqtt.TmsStation message """
    print(f"Received fi.digitraffic.road.mqtt.TmsStation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_tms_station_data}")

async def handle_fi_digitraffic_road_mqtt_weather_station(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_weather_station_data):
    """ Handles the fi.digitraffic.road.mqtt.WeatherStation message """
    print(f"Received fi.digitraffic.road.mqtt.WeatherStation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_weather_station_data}")

async def handle_fi_digitraffic_road_mqtt_maintenance_task_type(mqtt_msg,cloud_event, fi_digitraffic_road_mqtt_maintenance_task_type_data):
    """ Handles the fi.digitraffic.road.mqtt.MaintenanceTaskType message """
    print(f"Received fi.digitraffic.road.mqtt.MaintenanceTaskType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_digitraffic_road_mqtt_maintenance_task_type_data}")

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