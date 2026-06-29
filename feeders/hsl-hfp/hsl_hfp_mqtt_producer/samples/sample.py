
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
from hsl_hfp_mqtt_producer_data import *
from hsl_hfp_mqtt_producer_mqtt_client.client import FiHslHfpMqttProducer, FiHslHfpMqttDispatcher

async def handle_fi_hsl_hfp_mqtt_vp(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_vp_data):
    """ Handles the fi.hsl.hfp.mqtt.vp message """
    print(f"Received fi.hsl.hfp.mqtt.vp on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_vp_data}")

async def handle_fi_hsl_hfp_mqtt_due(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_due_data):
    """ Handles the fi.hsl.hfp.mqtt.due message """
    print(f"Received fi.hsl.hfp.mqtt.due on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_due_data}")

async def handle_fi_hsl_hfp_mqtt_arr(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_arr_data):
    """ Handles the fi.hsl.hfp.mqtt.arr message """
    print(f"Received fi.hsl.hfp.mqtt.arr on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_arr_data}")

async def handle_fi_hsl_hfp_mqtt_dep(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_dep_data):
    """ Handles the fi.hsl.hfp.mqtt.dep message """
    print(f"Received fi.hsl.hfp.mqtt.dep on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_dep_data}")

async def handle_fi_hsl_hfp_mqtt_ars(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_ars_data):
    """ Handles the fi.hsl.hfp.mqtt.ars message """
    print(f"Received fi.hsl.hfp.mqtt.ars on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_ars_data}")

async def handle_fi_hsl_hfp_mqtt_pde(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_pde_data):
    """ Handles the fi.hsl.hfp.mqtt.pde message """
    print(f"Received fi.hsl.hfp.mqtt.pde on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_pde_data}")

async def handle_fi_hsl_hfp_mqtt_pas(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_pas_data):
    """ Handles the fi.hsl.hfp.mqtt.pas message """
    print(f"Received fi.hsl.hfp.mqtt.pas on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_pas_data}")

async def handle_fi_hsl_hfp_mqtt_wait(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_wait_data):
    """ Handles the fi.hsl.hfp.mqtt.wait message """
    print(f"Received fi.hsl.hfp.mqtt.wait on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_wait_data}")

async def handle_fi_hsl_hfp_mqtt_doo(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_doo_data):
    """ Handles the fi.hsl.hfp.mqtt.doo message """
    print(f"Received fi.hsl.hfp.mqtt.doo on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_doo_data}")

async def handle_fi_hsl_hfp_mqtt_doc(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_doc_data):
    """ Handles the fi.hsl.hfp.mqtt.doc message """
    print(f"Received fi.hsl.hfp.mqtt.doc on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_doc_data}")

async def handle_fi_hsl_hfp_mqtt_vja(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_vja_data):
    """ Handles the fi.hsl.hfp.mqtt.vja message """
    print(f"Received fi.hsl.hfp.mqtt.vja on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_vja_data}")

async def handle_fi_hsl_hfp_mqtt_vjout(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_vjout_data):
    """ Handles the fi.hsl.hfp.mqtt.vjout message """
    print(f"Received fi.hsl.hfp.mqtt.vjout on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_vjout_data}")

async def handle_fi_hsl_hfp_mqtt_tlr(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_tlr_data):
    """ Handles the fi.hsl.hfp.mqtt.tlr message """
    print(f"Received fi.hsl.hfp.mqtt.tlr on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_tlr_data}")

async def handle_fi_hsl_hfp_mqtt_tla(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_tla_data):
    """ Handles the fi.hsl.hfp.mqtt.tla message """
    print(f"Received fi.hsl.hfp.mqtt.tla on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_tla_data}")

async def handle_fi_hsl_hfp_mqtt_da(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_da_data):
    """ Handles the fi.hsl.hfp.mqtt.da message """
    print(f"Received fi.hsl.hfp.mqtt.da on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_da_data}")

async def handle_fi_hsl_hfp_mqtt_dout(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_dout_data):
    """ Handles the fi.hsl.hfp.mqtt.dout message """
    print(f"Received fi.hsl.hfp.mqtt.dout on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_dout_data}")

async def handle_fi_hsl_hfp_mqtt_ba(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_ba_data):
    """ Handles the fi.hsl.hfp.mqtt.ba message """
    print(f"Received fi.hsl.hfp.mqtt.ba on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_ba_data}")

async def handle_fi_hsl_hfp_mqtt_bout(mqtt_msg,cloud_event, fi_hsl_hfp_mqtt_bout_data):
    """ Handles the fi.hsl.hfp.mqtt.bout message """
    print(f"Received fi.hsl.hfp.mqtt.bout on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_hfp_mqtt_bout_data}")
from hsl_hfp_mqtt_producer_mqtt_client.client import FiHslGtfsOperatorMqttProducer, FiHslGtfsOperatorMqttDispatcher

async def handle_fi_hsl_gtfs_operator_mqtt_operator(mqtt_msg,cloud_event, fi_hsl_gtfs_operator_mqtt_operator_data):
    """ Handles the fi.hsl.gtfs.operator.mqtt.Operator message """
    print(f"Received fi.hsl.gtfs.operator.mqtt.Operator on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_gtfs_operator_mqtt_operator_data}")
from hsl_hfp_mqtt_producer_mqtt_client.client import FiHslGtfsRouteMqttProducer, FiHslGtfsRouteMqttDispatcher

async def handle_fi_hsl_gtfs_route_mqtt_route(mqtt_msg,cloud_event, fi_hsl_gtfs_route_mqtt_route_data):
    """ Handles the fi.hsl.gtfs.route.mqtt.Route message """
    print(f"Received fi.hsl.gtfs.route.mqtt.Route on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_gtfs_route_mqtt_route_data}")
from hsl_hfp_mqtt_producer_mqtt_client.client import FiHslGtfsStopMqttProducer, FiHslGtfsStopMqttDispatcher

async def handle_fi_hsl_gtfs_stop_mqtt_stop(mqtt_msg,cloud_event, fi_hsl_gtfs_stop_mqtt_stop_data):
    """ Handles the fi.hsl.gtfs.stop.mqtt.Stop message """
    print(f"Received fi.hsl.gtfs.stop.mqtt.Stop on topic {mqtt_msg.topic}")
    if cloud_event:
        print(f"  CloudEvent ID: {cloud_event.id}, Source: {cloud_event.source}")
    print(f"  Data: {fi_hsl_gtfs_stop_mqtt_stop_data}")

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