# pylint: disable=line-too-long, trailing-whitespace, missing-module-docstring, missing-function-docstring, missing-class-docstring, redefined-outer-name, unused-argument, broad-exception-caught, broad-exception-raised, invalid-name, trailing-newlines, wrong-import-position, import-error, no-name-in-module

import os
import sys
import pytest
import pytest_asyncio
import asyncio
import datetime
import time
import paho.mqtt.client as mqtt
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fdsn_seismology_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fdsn_seismology_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fdsn_seismology_mqtt_producer_mqtt_client/src')))

import fdsn_seismology_mqtt_producer_data
from fdsn_seismology_mqtt_producer_data import Earthquake
from test_earthquake import Test_Earthquake
from fdsn_seismology_mqtt_producer_data import Node
from test_node import Test_Node
from fdsn_seismology_mqtt_producer_mqtt_client import OrgFdsnEventMqttMqttClient

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
async def test_org_fdsn_event_mqtt_org_fdsn_event_mqtt_earthquake_py(mosquitto_broker):
    """Test publishing and receiving org.fdsn.event.mqtt.Earthquake message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Earthquake.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgFdsnEventMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgFdsnEventMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_fdsn_event_mqtt_earthquake(mqtt_msg, cloud_event, data: fdsn_seismology_mqtt_producer_data.Earthquake, topic_params: dict):
        """Handler for org.fdsn.event.mqtt.Earthquake messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.fdsn.event.Earthquake"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_fdsn_event_mqtt_earthquake_async = on_org_fdsn_event_mqtt_earthquake
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_fdsn_event_mqtt/org_fdsn_event_mqtt_earthquake"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_fdsn_event_mqtt_earthquake(
            topic=test_topic,
            node_url=f"test_node_url_{i}",
            contributor=f"test_contributor_{i}",
            event_id=f"test_event_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
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



@pytest.mark.asyncio
async def test_org_fdsn_event_mqtt_org_fdsn_event_mqtt_node_py(mosquitto_broker):
    """Test publishing and receiving org.fdsn.event.mqtt.Node message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Node.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgFdsnEventMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgFdsnEventMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_fdsn_event_mqtt_node(mqtt_msg, cloud_event, data: fdsn_seismology_mqtt_producer_data.Node, topic_params: dict):
        """Handler for org.fdsn.event.mqtt.Node messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.fdsn.event.Node"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_fdsn_event_mqtt_node_async = on_org_fdsn_event_mqtt_node
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_fdsn_event_mqtt/org_fdsn_event_mqtt_node"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_fdsn_event_mqtt_node(
            topic=test_topic,
            base_url=f"test_base_url_{i}",
            node_id=f"test_node_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
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


