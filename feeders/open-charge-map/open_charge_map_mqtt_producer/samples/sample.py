
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
from open_charge_map_mqtt_producer_data import *
from open_charge_map_mqtt_producer_mqtt_client.client import IOOpenChargeMapLocationsMqttProducer, IOOpenChargeMapLocationsMqttDispatcher

async def handle_io_open_charge_map_mqtt_charging_location(mqtt_msg,cloud_event, io_open_charge_map_mqtt_charging_location_data):
    """ Handles the IO.OpenChargeMap.mqtt.ChargingLocation message """
    print(f"Received IO.OpenChargeMap.mqtt.ChargingLocation on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_charging_location_data}")
from open_charge_map_mqtt_producer_mqtt_client.client import IOOpenChargeMapReferenceMqttProducer, IOOpenChargeMapReferenceMqttDispatcher

async def handle_io_open_charge_map_mqtt_operator(mqtt_msg,cloud_event, io_open_charge_map_mqtt_operator_data):
    """ Handles the IO.OpenChargeMap.mqtt.Operator message """
    print(f"Received IO.OpenChargeMap.mqtt.Operator on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_operator_data}")

async def handle_io_open_charge_map_mqtt_connection_type(mqtt_msg,cloud_event, io_open_charge_map_mqtt_connection_type_data):
    """ Handles the IO.OpenChargeMap.mqtt.ConnectionType message """
    print(f"Received IO.OpenChargeMap.mqtt.ConnectionType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_connection_type_data}")

async def handle_io_open_charge_map_mqtt_current_type(mqtt_msg,cloud_event, io_open_charge_map_mqtt_current_type_data):
    """ Handles the IO.OpenChargeMap.mqtt.CurrentType message """
    print(f"Received IO.OpenChargeMap.mqtt.CurrentType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_current_type_data}")

async def handle_io_open_charge_map_mqtt_charger_type(mqtt_msg,cloud_event, io_open_charge_map_mqtt_charger_type_data):
    """ Handles the IO.OpenChargeMap.mqtt.ChargerType message """
    print(f"Received IO.OpenChargeMap.mqtt.ChargerType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_charger_type_data}")

async def handle_io_open_charge_map_mqtt_country(mqtt_msg,cloud_event, io_open_charge_map_mqtt_country_data):
    """ Handles the IO.OpenChargeMap.mqtt.Country message """
    print(f"Received IO.OpenChargeMap.mqtt.Country on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_country_data}")

async def handle_io_open_charge_map_mqtt_data_provider(mqtt_msg,cloud_event, io_open_charge_map_mqtt_data_provider_data):
    """ Handles the IO.OpenChargeMap.mqtt.DataProvider message """
    print(f"Received IO.OpenChargeMap.mqtt.DataProvider on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_data_provider_data}")

async def handle_io_open_charge_map_mqtt_status_type(mqtt_msg,cloud_event, io_open_charge_map_mqtt_status_type_data):
    """ Handles the IO.OpenChargeMap.mqtt.StatusType message """
    print(f"Received IO.OpenChargeMap.mqtt.StatusType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_status_type_data}")

async def handle_io_open_charge_map_mqtt_usage_type(mqtt_msg,cloud_event, io_open_charge_map_mqtt_usage_type_data):
    """ Handles the IO.OpenChargeMap.mqtt.UsageType message """
    print(f"Received IO.OpenChargeMap.mqtt.UsageType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_usage_type_data}")

async def handle_io_open_charge_map_mqtt_submission_status_type(mqtt_msg,cloud_event, io_open_charge_map_mqtt_submission_status_type_data):
    """ Handles the IO.OpenChargeMap.mqtt.SubmissionStatusType message """
    print(f"Received IO.OpenChargeMap.mqtt.SubmissionStatusType on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {io_open_charge_map_mqtt_submission_status_type_data}")

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