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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../irail_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../irail_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../irail_mqtt_producer_mqtt_client/src')))

import irail_mqtt_producer_data
from irail_mqtt_producer_data import Station
from test_irail_mqtt_producer_data_station import Test_Station
from irail_mqtt_producer_data import StationBoard
from test_irail_mqtt_producer_data_stationboard import Test_StationBoard
from irail_mqtt_producer_data import ArrivalBoard
from test_irail_mqtt_producer_data_arrivalboard import Test_ArrivalBoard
from irail_mqtt_producer_mqtt_client import BeIrailMqttMqttClient

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
async def test_be_irail_mqtt_be_irail_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving be.irail.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BeIrailMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BeIrailMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_be_irail_mqtt_station(mqtt_msg, cloud_event, data: irail_mqtt_producer_data.Station, topic_params: dict):
        """Handler for be.irail.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "be.irail.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.be_irail_mqtt_station_async = on_be_irail_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/be_irail_mqtt/be_irail_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_be_irail_mqtt_station(
            topic=test_topic,
            station_id=f"test_station_id_{i}",
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
async def test_be_irail_mqtt_be_irail_mqtt_station_board_py(mosquitto_broker):
    """Test publishing and receiving be.irail.mqtt.StationBoard message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StationBoard.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BeIrailMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BeIrailMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_be_irail_mqtt_station_board(mqtt_msg, cloud_event, data: irail_mqtt_producer_data.StationBoard, topic_params: dict):
        """Handler for be.irail.mqtt.StationBoard messages."""
        received_data.append(data)
        assert cloud_event['type'] == "be.irail.StationBoard"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.be_irail_mqtt_station_board_async = on_be_irail_mqtt_station_board
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/be_irail_mqtt/be_irail_mqtt_station_board"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_be_irail_mqtt_station_board(
            topic=test_topic,
            station_id=f"test_station_id_{i}",
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
async def test_be_irail_mqtt_be_irail_mqtt_arrival_board_py(mosquitto_broker):
    """Test publishing and receiving be.irail.mqtt.ArrivalBoard message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ArrivalBoard.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BeIrailMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BeIrailMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_be_irail_mqtt_arrival_board(mqtt_msg, cloud_event, data: irail_mqtt_producer_data.ArrivalBoard, topic_params: dict):
        """Handler for be.irail.mqtt.ArrivalBoard messages."""
        received_data.append(data)
        assert cloud_event['type'] == "be.irail.ArrivalBoard"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.be_irail_mqtt_arrival_board_async = on_be_irail_mqtt_arrival_board
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/be_irail_mqtt/be_irail_mqtt_arrival_board"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_be_irail_mqtt_arrival_board(
            topic=test_topic,
            station_id=f"test_station_id_{i}",
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


