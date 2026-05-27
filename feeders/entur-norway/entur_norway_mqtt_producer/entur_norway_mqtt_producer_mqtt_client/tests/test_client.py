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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entur_norway_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entur_norway_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entur_norway_mqtt_producer_mqtt_client/src')))

import entur_norway_mqtt_producer_data
from entur_norway_mqtt_producer_data import EstimatedVehicleJourney
from test_estimatedvehiclejourney import Test_EstimatedVehicleJourney
from entur_norway_mqtt_producer_data import MonitoredVehicleJourney
from test_monitoredvehiclejourney import Test_MonitoredVehicleJourney
from entur_norway_mqtt_producer_data import PtSituationElement
from test_ptsituationelement import Test_PtSituationElement
from entur_norway_mqtt_producer_mqtt_client import NoEnturMqttMqttClient

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
async def test_no_entur_mqtt_no_entur_mqtt_estimated_vehicle_journey_py(mosquitto_broker):
    """Test publishing and receiving no.entur.mqtt.EstimatedVehicleJourney message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_EstimatedVehicleJourney.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NoEnturMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NoEnturMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_no_entur_mqtt_estimated_vehicle_journey(mqtt_msg, cloud_event, data: entur_norway_mqtt_producer_data.EstimatedVehicleJourney, topic_params: dict):
        """Handler for no.entur.mqtt.EstimatedVehicleJourney messages."""
        received_data.append(data)
        assert cloud_event['type'] == "no.entur.EstimatedVehicleJourney"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.no_entur_mqtt_estimated_vehicle_journey_async = on_no_entur_mqtt_estimated_vehicle_journey
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/no_entur_mqtt/no_entur_mqtt_estimated_vehicle_journey"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_no_entur_mqtt_estimated_vehicle_journey(
            topic=test_topic,
            operating_day=f"test_operating_day_{i}",
            service_journey_id=f"test_service_journey_id_{i}",
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
async def test_no_entur_mqtt_no_entur_mqtt_monitored_vehicle_journey_py(mosquitto_broker):
    """Test publishing and receiving no.entur.mqtt.MonitoredVehicleJourney message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MonitoredVehicleJourney.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NoEnturMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NoEnturMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_no_entur_mqtt_monitored_vehicle_journey(mqtt_msg, cloud_event, data: entur_norway_mqtt_producer_data.MonitoredVehicleJourney, topic_params: dict):
        """Handler for no.entur.mqtt.MonitoredVehicleJourney messages."""
        received_data.append(data)
        assert cloud_event['type'] == "no.entur.MonitoredVehicleJourney"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.no_entur_mqtt_monitored_vehicle_journey_async = on_no_entur_mqtt_monitored_vehicle_journey
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/no_entur_mqtt/no_entur_mqtt_monitored_vehicle_journey"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_no_entur_mqtt_monitored_vehicle_journey(
            topic=test_topic,
            operating_day=f"test_operating_day_{i}",
            service_journey_id=f"test_service_journey_id_{i}",
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
async def test_no_entur_mqtt_no_entur_mqtt_pt_situation_element_py(mosquitto_broker):
    """Test publishing and receiving no.entur.mqtt.PtSituationElement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PtSituationElement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NoEnturMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NoEnturMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_no_entur_mqtt_pt_situation_element(mqtt_msg, cloud_event, data: entur_norway_mqtt_producer_data.PtSituationElement, topic_params: dict):
        """Handler for no.entur.mqtt.PtSituationElement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "no.entur.PtSituationElement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.no_entur_mqtt_pt_situation_element_async = on_no_entur_mqtt_pt_situation_element
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/no_entur_mqtt/no_entur_mqtt_pt_situation_element"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_no_entur_mqtt_pt_situation_element(
            topic=test_topic,
            situation_number=f"test_situation_number_{i}",
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


