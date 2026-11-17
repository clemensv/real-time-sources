
"""
Sample usage of pegelonline_mqtt_producer_mqtt_client.

This example shows how to consume and publish MQTT messages with the generated
client. Each message group has a
`<Group>MqttClient` that wraps a paho-mqtt client and both dispatches received
messages to async handlers you register and exposes `publish_<message>`
coroutines to send messages.

Message handlers are async functions. CloudEvents message handlers receive
`(mqtt_message, cloud_event, data, topic_params)`; plain (non-CloudEvents)
message handlers receive `(mqtt_message, data, topic_params)` where:
  - mqtt_message: the paho.mqtt.client.MQTTMessage (raw message context),
  - cloud_event: the CloudEvent envelope (CloudEvents messages only),
  - data: the deserialized, strongly-typed message data,
  - topic_params: dict of URI-template placeholders extracted from the topic.

Configuration is read from the command line or these environment variables:
  - MQTT_BROKER_HOST: broker hostname (default: localhost),
  - MQTT_BROKER_PORT: broker port (default: 1883),
  - MQTT_USERNAME: username (optional),
  - MQTT_PASSWORD: password (optional).

    python sample.py --broker-host <host> --broker-port <port>

The sample connects, subscribes, publishes one example of each message, then
waits for incoming messages until interrupted (press Ctrl+C to stop).
"""

import argparse
import asyncio
import os
import signal

import paho.mqtt.client as mqtt

from pegelonline_mqtt_producer_data import *
from pegelonline_mqtt_producer_mqtt_client.client import DeWsvPegelonlineMqttMqttClient


async def handle_de_wsv_pegelonline_mqtt_station(mqtt_message, cloud_event, data, topic_params):
    """Handle the CloudEvents 'de.wsv.pegelonline.mqtt.Station' message."""
    print(f"Received de.wsv.pegelonline.mqtt.Station on topic {mqtt_message.topic}")
    print(f"  CloudEvent: id={cloud_event['id']} source={cloud_event['source']} type={cloud_event['type']}")
    print(f"  Data: {data}")
    if topic_params:
        print(f"  Topic params: {topic_params}")


async def handle_de_wsv_pegelonline_mqtt_current_measurement(mqtt_message, cloud_event, data, topic_params):
    """Handle the CloudEvents 'de.wsv.pegelonline.mqtt.CurrentMeasurement' message."""
    print(f"Received de.wsv.pegelonline.mqtt.CurrentMeasurement on topic {mqtt_message.topic}")
    print(f"  CloudEvent: id={cloud_event['id']} source={cloud_event['source']} type={cloud_event['type']}")
    print(f"  Data: {data}")
    if topic_params:
        print(f"  Topic params: {topic_params}")



def _make_paho_client(client_id):
    """Create a paho-mqtt client compatible with paho-mqtt 1.x and 2.x.

    The generated client callbacks use the VERSION1 callback signatures, so we
    request that API version when running on paho-mqtt 2.x.
    """
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=client_id)
    except (AttributeError, TypeError):
        return mqtt.Client(client_id=client_id)


async def publish_samples(clients):
    """Publish one example of each message type using generated test data."""
    client = clients["de.wsv.pegelonline.mqtt"]
    try:
        await client.publish_de_wsv_pegelonline_mqtt_station(
            feedurl="sample",
            station_id="sample",
            water_shortname="sample",
            data=Station.create_instance(),
        )
        print("Published de.wsv.pegelonline.mqtt.Station")
    except Exception as exc:
        print(f"Could not publish de.wsv.pegelonline.mqtt.Station: {exc}")
    try:
        await client.publish_de_wsv_pegelonline_mqtt_current_measurement(
            feedurl="sample",
            station_id="sample",
            water_shortname="sample",
            data=CurrentMeasurement.create_instance(),
        )
        print("Published de.wsv.pegelonline.mqtt.CurrentMeasurement")
    except Exception as exc:
        print(f"Could not publish de.wsv.pegelonline.mqtt.CurrentMeasurement: {exc}")


async def main(broker_host, broker_port, username=None, password=None):
    """Set up the client(s), connect, subscribe, publish samples, then listen."""
    loop = asyncio.get_running_loop()
    clients = {}

    
    _paho = _make_paho_client("sample-de_wsv_pegelonline_mqtt")
    if username:
        _paho.username_pw_set(username, password)
    _client = DeWsvPegelonlineMqttMqttClient(_paho, content_mode='structured', loop=loop)
    _client.de_wsv_pegelonline_mqtt_station_async = handle_de_wsv_pegelonline_mqtt_station
    _client.de_wsv_pegelonline_mqtt_current_measurement_async = handle_de_wsv_pegelonline_mqtt_current_measurement
    clients["de.wsv.pegelonline.mqtt"] = _client
    

    print(f"Connecting to {broker_host}:{broker_port} ...")
    for client in clients.values():
        await client.connect(broker_host, broker_port)
        await client.subscribe()
    print("Connected and subscribed.")

    # Give subscriptions a moment to take effect, then publish a sample of each message.
    await asyncio.sleep(1)
    await publish_samples(clients)

    stop_event = asyncio.Event()
    try:
        loop.add_signal_handler(signal.SIGINT, stop_event.set)
        loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    except NotImplementedError:
        # Signal handlers are not available on this platform (e.g. Windows).
        pass

    print("Listening for messages. Press Ctrl+C to stop.")
    try:
        await stop_event.wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass

    print("\nStopping...")
    for client in clients.values():
        await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Client sample")
    parser.add_argument('--broker-host', default=os.getenv('MQTT_BROKER_HOST', 'localhost'), help='MQTT broker hostname')
    parser.add_argument('--broker-port', type=int, default=int(os.getenv('MQTT_BROKER_PORT', '1883')), help='MQTT broker port')
    parser.add_argument('--username', default=os.getenv('MQTT_USERNAME'), help='MQTT username (optional)')
    parser.add_argument('--password', default=os.getenv('MQTT_PASSWORD'), help='MQTT password (optional)')

    args = parser.parse_args()

    try:
        asyncio.run(main(
            args.broker_host,
            args.broker_port,
            args.username,
            args.password
        ))
    except KeyboardInterrupt:
        print("\nStopped.")