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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../openaq_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../openaq_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../openaq_mqtt_producer_mqtt_client/src')))

import openaq_mqtt_producer_data
from openaq_mqtt_producer_data import Location
from test_location import Test_Location
from openaq_mqtt_producer_data import Sensor
from test_sensor import Test_Sensor
from openaq_mqtt_producer_data import Measurement
from test_measurement import Test_Measurement
from openaq_mqtt_producer_mqtt_client import OrgOpenaqLocationsMqttMqttClient
from openaq_mqtt_producer_mqtt_client import OrgOpenaqSensorsMqttMqttClient

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
async def test_org_openaq_locations_mqtt_org_openaq_mqtt_location_py(mosquitto_broker):
    """Test publishing and receiving org.openaq.mqtt.Location message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Location.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOpenaqLocationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOpenaqLocationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_openaq_mqtt_location(mqtt_msg, cloud_event, data: openaq_mqtt_producer_data.Location, topic_params: dict):
        """Handler for org.openaq.mqtt.Location messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.openaq.Location"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_openaq_mqtt_location_async = on_org_openaq_mqtt_location
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_openaq_locations_mqtt/org_openaq_mqtt_location"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_openaq_mqtt_location(
            topic=test_topic,
            location_id=f"test_location_id_{i}",
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
async def test_org_openaq_sensors_mqtt_org_openaq_mqtt_sensor_py(mosquitto_broker):
    """Test publishing and receiving org.openaq.mqtt.Sensor message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Sensor.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOpenaqSensorsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOpenaqSensorsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_openaq_mqtt_sensor(mqtt_msg, cloud_event, data: openaq_mqtt_producer_data.Sensor, topic_params: dict):
        """Handler for org.openaq.mqtt.Sensor messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.openaq.Sensor"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_openaq_mqtt_sensor_async = on_org_openaq_mqtt_sensor
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_openaq_sensors_mqtt/org_openaq_mqtt_sensor"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_openaq_mqtt_sensor(
            topic=test_topic,
            location_id=f"test_location_id_{i}",
            sensor_id=f"test_sensor_id_{i}",
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
async def test_org_openaq_sensors_mqtt_org_openaq_mqtt_measurement_py(mosquitto_broker):
    """Test publishing and receiving org.openaq.mqtt.Measurement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Measurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOpenaqSensorsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOpenaqSensorsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_openaq_mqtt_measurement(mqtt_msg, cloud_event, data: openaq_mqtt_producer_data.Measurement, topic_params: dict):
        """Handler for org.openaq.mqtt.Measurement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.openaq.Measurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_openaq_mqtt_measurement_async = on_org_openaq_mqtt_measurement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_openaq_sensors_mqtt/org_openaq_mqtt_measurement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_openaq_mqtt_measurement(
            topic=test_topic,
            location_id=f"test_location_id_{i}",
            sensor_id=f"test_sensor_id_{i}",
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


