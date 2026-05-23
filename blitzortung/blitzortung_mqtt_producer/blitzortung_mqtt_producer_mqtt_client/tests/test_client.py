# pylint: disable=line-too-long, trailing-whitespace, missing-module-docstring, missing-function-docstring, missing-class-docstring, redefined-outer-name, unused-argument, broad-exception-caught, broad-exception-raised, invalid-name, trailing-newlines, wrong-import-position, import-error, no-name-in-module

import os
import sys
import pytest
import pytest_asyncio
import asyncio
import time
import paho.mqtt.client as mqtt
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../blitzortung_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../blitzortung_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../blitzortung_mqtt_producer_mqtt_client/src')))

import blitzortung_mqtt_producer_data
from blitzortung_mqtt_producer_data import LightningStroke
from test_blitzortung_mqtt_producer_data_lightningstroke import Test_LightningStroke
from blitzortung_mqtt_producer_mqtt_client import BlitzortungLightningMqttMqttClient

@pytest_asyncio.fixture
async def mosquitto_broker():
    """Start Mosquitto MQTT broker in container."""
    container = DockerContainer("eclipse-mosquitto:2.0")
    container.with_exposed_ports(1883)
    container.with_command("mosquitto -c /mosquitto-no-auth.conf")
    
    container.start()
    
    try:
        # Wait for Mosquitto to start
        wait_for_logs(container, "mosquitto version .* running", timeout=10)
        await asyncio.sleep(2)  # Additional stabilization time
        
        # Get mapped port
        broker_port = container.get_exposed_port(1883)
        broker_host = "localhost"
        
        yield broker_host, broker_port
    finally:
        container.stop()



@pytest.mark.asyncio
async def test_blitzortung_lightning_mqtt_blitzortung_lightning_mqtt_lightning_stroke_py(mosquitto_broker):
    """Test publishing and receiving Blitzortung.Lightning.mqtt.LightningStroke message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LightningStroke.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BlitzortungLightningMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BlitzortungLightningMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_blitzortung_lightning_mqtt_lightning_stroke(mqtt_msg, cloud_event, data: blitzortung_mqtt_producer_data.LightningStroke, topic_params: dict):
        """Handler for Blitzortung.Lightning.mqtt.LightningStroke messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Blitzortung.Lightning.mqtt.LightningStroke"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.blitzortung_lightning_mqtt_lightning_stroke_async = on_blitzortung_lightning_mqtt_lightning_stroke
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/blitzortung_lightning_mqtt/blitzortung_lightning_mqtt_lightning_stroke"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_blitzortung_lightning_mqtt_lightning_stroke(
            topic=test_topic,
            geohash5=f"test_geohash5_{i}",
            geohash7=f"test_geohash7_{i}",
            stroke_id=f"test_stroke_id_{i}",
            event_time=f"test_event_time_{i}",
            data=test_data,
            content_type="application/json"
        )
    
    # Wait for all 5 messages to be received (with timeout)
    try:
        await asyncio.wait_for(received_event.wait(), timeout=10.0)
    except asyncio.TimeoutError:
        pytest.fail(f"Did not receive all 5 messages within timeout, got {len(received_data)}")
    
    # Verify all 5 messages received
    assert len(received_data) == 5, f"Expected 5 messages, got {len(received_data)}"
    
    # Cleanup
    await subscriber_client.disconnect()
    await publisher_client.disconnect()


