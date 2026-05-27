
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
from tfl_road_traffic_mqtt_producer_data import *
from tfl_road_traffic_mqtt_producer_mqtt_client.client import UkGovTflRoadMqttProducer, UkGovTflRoadMqttDispatcher

async def handle_uk_gov_tfl_road_mqtt_road_corridor(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_corridor_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadCorridor message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadCorridor on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_corridor_data}")

async def handle_uk_gov_tfl_road_mqtt_road_status(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_status_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadStatus message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadStatus on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_status_data}")

async def handle_uk_gov_tfl_road_mqtt_road_disruption_serious(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_disruption_serious_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadDisruptionSerious message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadDisruptionSerious on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_disruption_serious_data}")

async def handle_uk_gov_tfl_road_mqtt_road_disruption_severe(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_disruption_severe_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadDisruptionSevere message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadDisruptionSevere on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_disruption_severe_data}")

async def handle_uk_gov_tfl_road_mqtt_road_disruption_moderate(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_disruption_moderate_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadDisruptionModerate message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadDisruptionModerate on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_disruption_moderate_data}")

async def handle_uk_gov_tfl_road_mqtt_road_disruption_minor(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_disruption_minor_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadDisruptionMinor message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadDisruptionMinor on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_disruption_minor_data}")

async def handle_uk_gov_tfl_road_mqtt_road_disruption_information(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_disruption_information_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadDisruptionInformation message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadDisruptionInformation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_disruption_information_data}")

async def handle_uk_gov_tfl_road_mqtt_road_disruption_closure(mqtt_msg,cloud_event, uk_gov_tfl_road_mqtt_road_disruption_closure_data):
    """ Handles the uk.gov.tfl.road.mqtt.RoadDisruptionClosure message """
    print(f"Received uk.gov.tfl.road.mqtt.RoadDisruptionClosure on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {uk_gov_tfl_road_mqtt_road_disruption_closure_data}")

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