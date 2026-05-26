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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../xceed_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../xceed_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../xceed_mqtt_producer_mqtt_client/src')))

import xceed_mqtt_producer_data
from xceed_mqtt_producer_data import Event
from test_xceed_mqtt_producer_data_event import Test_Event
from xceed_mqtt_producer_data import EventAdmission
from test_xceed_mqtt_producer_data_eventadmission import Test_EventAdmission
from xceed_mqtt_producer_mqtt_client import XceedMqttMqttClient
from xceed_mqtt_producer_mqtt_client import XceedAdmissionsMqttMqttClient

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
async def test_xceed_mqtt_xceed_mqtt_event_py(mosquitto_broker):
    """Test publishing and receiving xceed.mqtt.Event message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Event.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = XceedMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = XceedMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_xceed_mqtt_event(mqtt_msg, cloud_event, data: xceed_mqtt_producer_data.Event, topic_params: dict):
        """Handler for xceed.mqtt.Event messages."""
        received_data.append(data)
        assert cloud_event['type'] == "xceed.Event"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.xceed_mqtt_event_async = on_xceed_mqtt_event
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/xceed_mqtt/xceed_mqtt_event"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_xceed_mqtt_event(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            event_id=f"test_event_id_{i}",
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
async def test_xceed_admissions_mqtt_xceed_admissions_mqtt_event_admission_py(mosquitto_broker):
    """Test publishing and receiving xceed.admissions.mqtt.EventAdmission message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_EventAdmission.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = XceedAdmissionsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = XceedAdmissionsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_xceed_admissions_mqtt_event_admission(mqtt_msg, cloud_event, data: xceed_mqtt_producer_data.EventAdmission, topic_params: dict):
        """Handler for xceed.admissions.mqtt.EventAdmission messages."""
        received_data.append(data)
        assert cloud_event['type'] == "xceed.EventAdmission"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.xceed_admissions_mqtt_event_admission_async = on_xceed_admissions_mqtt_event_admission
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/xceed_admissions_mqtt/xceed_admissions_mqtt_event_admission"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_xceed_admissions_mqtt_event_admission(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            event_id=f"test_event_id_{i}",
            admission_id=f"test_admission_id_{i}",
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


