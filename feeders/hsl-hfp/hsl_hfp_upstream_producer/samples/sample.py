
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
from hsl_hfp_upstream_data import *
from hsl_hfp_upstream_mqtt_client.client import FiHslHfpUpstreamProducer, FiHslHfpUpstreamDispatcher

async def handle_fi_hsl_hfp_upstream_vp(mqtt_msg,fi_hsl_hfp_upstream_vp_data):
    """ Handles the fi.hsl.hfp.upstream.vp message """
    print(f"Received fi.hsl.hfp.upstream.vp on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_vp_data}")

async def handle_fi_hsl_hfp_upstream_due(mqtt_msg,fi_hsl_hfp_upstream_due_data):
    """ Handles the fi.hsl.hfp.upstream.due message """
    print(f"Received fi.hsl.hfp.upstream.due on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_due_data}")

async def handle_fi_hsl_hfp_upstream_arr(mqtt_msg,fi_hsl_hfp_upstream_arr_data):
    """ Handles the fi.hsl.hfp.upstream.arr message """
    print(f"Received fi.hsl.hfp.upstream.arr on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_arr_data}")

async def handle_fi_hsl_hfp_upstream_dep(mqtt_msg,fi_hsl_hfp_upstream_dep_data):
    """ Handles the fi.hsl.hfp.upstream.dep message """
    print(f"Received fi.hsl.hfp.upstream.dep on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_dep_data}")

async def handle_fi_hsl_hfp_upstream_ars(mqtt_msg,fi_hsl_hfp_upstream_ars_data):
    """ Handles the fi.hsl.hfp.upstream.ars message """
    print(f"Received fi.hsl.hfp.upstream.ars on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_ars_data}")

async def handle_fi_hsl_hfp_upstream_pde(mqtt_msg,fi_hsl_hfp_upstream_pde_data):
    """ Handles the fi.hsl.hfp.upstream.pde message """
    print(f"Received fi.hsl.hfp.upstream.pde on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_pde_data}")

async def handle_fi_hsl_hfp_upstream_pas(mqtt_msg,fi_hsl_hfp_upstream_pas_data):
    """ Handles the fi.hsl.hfp.upstream.pas message """
    print(f"Received fi.hsl.hfp.upstream.pas on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_pas_data}")

async def handle_fi_hsl_hfp_upstream_wait(mqtt_msg,fi_hsl_hfp_upstream_wait_data):
    """ Handles the fi.hsl.hfp.upstream.wait message """
    print(f"Received fi.hsl.hfp.upstream.wait on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_wait_data}")

async def handle_fi_hsl_hfp_upstream_doo(mqtt_msg,fi_hsl_hfp_upstream_doo_data):
    """ Handles the fi.hsl.hfp.upstream.doo message """
    print(f"Received fi.hsl.hfp.upstream.doo on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_doo_data}")

async def handle_fi_hsl_hfp_upstream_doc(mqtt_msg,fi_hsl_hfp_upstream_doc_data):
    """ Handles the fi.hsl.hfp.upstream.doc message """
    print(f"Received fi.hsl.hfp.upstream.doc on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_doc_data}")

async def handle_fi_hsl_hfp_upstream_vja(mqtt_msg,fi_hsl_hfp_upstream_vja_data):
    """ Handles the fi.hsl.hfp.upstream.vja message """
    print(f"Received fi.hsl.hfp.upstream.vja on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_vja_data}")

async def handle_fi_hsl_hfp_upstream_vjout(mqtt_msg,fi_hsl_hfp_upstream_vjout_data):
    """ Handles the fi.hsl.hfp.upstream.vjout message """
    print(f"Received fi.hsl.hfp.upstream.vjout on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_vjout_data}")

async def handle_fi_hsl_hfp_upstream_tlr(mqtt_msg,fi_hsl_hfp_upstream_tlr_data):
    """ Handles the fi.hsl.hfp.upstream.tlr message """
    print(f"Received fi.hsl.hfp.upstream.tlr on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_tlr_data}")

async def handle_fi_hsl_hfp_upstream_tla(mqtt_msg,fi_hsl_hfp_upstream_tla_data):
    """ Handles the fi.hsl.hfp.upstream.tla message """
    print(f"Received fi.hsl.hfp.upstream.tla on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_tla_data}")

async def handle_fi_hsl_hfp_upstream_da(mqtt_msg,fi_hsl_hfp_upstream_da_data):
    """ Handles the fi.hsl.hfp.upstream.da message """
    print(f"Received fi.hsl.hfp.upstream.da on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_da_data}")

async def handle_fi_hsl_hfp_upstream_dout(mqtt_msg,fi_hsl_hfp_upstream_dout_data):
    """ Handles the fi.hsl.hfp.upstream.dout message """
    print(f"Received fi.hsl.hfp.upstream.dout on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_dout_data}")

async def handle_fi_hsl_hfp_upstream_ba(mqtt_msg,fi_hsl_hfp_upstream_ba_data):
    """ Handles the fi.hsl.hfp.upstream.ba message """
    print(f"Received fi.hsl.hfp.upstream.ba on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_ba_data}")

async def handle_fi_hsl_hfp_upstream_bout(mqtt_msg,fi_hsl_hfp_upstream_bout_data):
    """ Handles the fi.hsl.hfp.upstream.bout message """
    print(f"Received fi.hsl.hfp.upstream.bout on topic {mqtt_msg.topic}")
    print(f"  Data: {fi_hsl_hfp_upstream_bout_data}")

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