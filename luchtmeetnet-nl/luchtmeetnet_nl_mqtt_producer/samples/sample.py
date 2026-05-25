
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
from luchtmeetnet_nl_mqtt_producer_data import *
from luchtmeetnet_nl_mqtt_producer_mqtt_client.client import NlRivmLuchtmeetnetMqttProducer, NlRivmLuchtmeetnetMqttDispatcher

async def handle_nl_rivm_luchtmeetnet_mqtt_station(mqtt_msg,cloud_event, nl_rivm_luchtmeetnet_mqtt_station_data):
    """ Handles the nl.rivm.luchtmeetnet.mqtt.Station message """
    print(f"Received nl.rivm.luchtmeetnet.mqtt.Station on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {nl_rivm_luchtmeetnet_mqtt_station_data}")

async def handle_nl_rivm_luchtmeetnet_mqtt_measurement(mqtt_msg,cloud_event, nl_rivm_luchtmeetnet_mqtt_measurement_data):
    """ Handles the nl.rivm.luchtmeetnet.mqtt.Measurement message """
    print(f"Received nl.rivm.luchtmeetnet.mqtt.Measurement on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {nl_rivm_luchtmeetnet_mqtt_measurement_data}")

async def handle_nl_rivm_luchtmeetnet_mqtt_lki(mqtt_msg,cloud_event, nl_rivm_luchtmeetnet_mqtt_lki_data):
    """ Handles the nl.rivm.luchtmeetnet.mqtt.LKI message """
    print(f"Received nl.rivm.luchtmeetnet.mqtt.LKI on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {nl_rivm_luchtmeetnet_mqtt_lki_data}")
from luchtmeetnet_nl_mqtt_producer_mqtt_client.client import NlRivmLuchtmeetnetComponentsMqttProducer, NlRivmLuchtmeetnetComponentsMqttDispatcher

async def handle_nl_rivm_luchtmeetnet_components_mqtt_component(mqtt_msg,cloud_event, nl_rivm_luchtmeetnet_components_mqtt_component_data):
    """ Handles the nl.rivm.luchtmeetnet.components.mqtt.Component message """
    print(f"Received nl.rivm.luchtmeetnet.components.mqtt.Component on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {nl_rivm_luchtmeetnet_components_mqtt_component_data}")

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