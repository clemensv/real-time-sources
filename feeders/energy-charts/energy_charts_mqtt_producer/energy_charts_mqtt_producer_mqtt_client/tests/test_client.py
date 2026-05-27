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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../energy_charts_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../energy_charts_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../energy_charts_mqtt_producer_mqtt_client/src')))

import energy_charts_mqtt_producer_data
from energy_charts_mqtt_producer_data import PublicPower
from test_energy_charts_mqtt_producer_data_publicpower import Test_PublicPower
from energy_charts_mqtt_producer_data import SpotPrice
from test_energy_charts_mqtt_producer_data_spotprice import Test_SpotPrice
from energy_charts_mqtt_producer_data import GridSignal
from test_energy_charts_mqtt_producer_data_gridsignal import Test_GridSignal
from energy_charts_mqtt_producer_data import Info
from test_energy_charts_mqtt_producer_data_info import Test_Info
from energy_charts_mqtt_producer_mqtt_client import InfoEnergyChartsMqttMqttClient

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
async def test_info_energy_charts_mqtt_info_energy_charts_mqtt_public_power_py(mosquitto_broker):
    """Test publishing and receiving info.energy_charts.mqtt.PublicPower message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PublicPower.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = InfoEnergyChartsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = InfoEnergyChartsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_info_energy_charts_mqtt_public_power(mqtt_msg, cloud_event, data: energy_charts_mqtt_producer_data.PublicPower, topic_params: dict):
        """Handler for info.energy_charts.mqtt.PublicPower messages."""
        received_data.append(data)
        assert cloud_event['type'] == "info.energy_charts.PublicPower"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.info_energy_charts_mqtt_public_power_async = on_info_energy_charts_mqtt_public_power
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/info_energy_charts_mqtt/info_energy_charts_mqtt_public_power"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_info_energy_charts_mqtt_public_power(
            topic=test_topic,
            country=f"test_country_{i}",
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
async def test_info_energy_charts_mqtt_info_energy_charts_mqtt_spot_price_py(mosquitto_broker):
    """Test publishing and receiving info.energy_charts.mqtt.SpotPrice message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SpotPrice.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = InfoEnergyChartsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = InfoEnergyChartsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_info_energy_charts_mqtt_spot_price(mqtt_msg, cloud_event, data: energy_charts_mqtt_producer_data.SpotPrice, topic_params: dict):
        """Handler for info.energy_charts.mqtt.SpotPrice messages."""
        received_data.append(data)
        assert cloud_event['type'] == "info.energy_charts.SpotPrice"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.info_energy_charts_mqtt_spot_price_async = on_info_energy_charts_mqtt_spot_price
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/info_energy_charts_mqtt/info_energy_charts_mqtt_spot_price"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_info_energy_charts_mqtt_spot_price(
            topic=test_topic,
            country=f"test_country_{i}",
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
async def test_info_energy_charts_mqtt_info_energy_charts_mqtt_grid_signal_py(mosquitto_broker):
    """Test publishing and receiving info.energy_charts.mqtt.GridSignal message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GridSignal.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = InfoEnergyChartsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = InfoEnergyChartsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_info_energy_charts_mqtt_grid_signal(mqtt_msg, cloud_event, data: energy_charts_mqtt_producer_data.GridSignal, topic_params: dict):
        """Handler for info.energy_charts.mqtt.GridSignal messages."""
        received_data.append(data)
        assert cloud_event['type'] == "info.energy_charts.GridSignal"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.info_energy_charts_mqtt_grid_signal_async = on_info_energy_charts_mqtt_grid_signal
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/info_energy_charts_mqtt/info_energy_charts_mqtt_grid_signal"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_info_energy_charts_mqtt_grid_signal(
            topic=test_topic,
            country=f"test_country_{i}",
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
async def test_info_energy_charts_mqtt_info_energy_charts_mqtt_info_py(mosquitto_broker):
    """Test publishing and receiving info.energy_charts.mqtt.Info message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Info.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = InfoEnergyChartsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = InfoEnergyChartsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_info_energy_charts_mqtt_info(mqtt_msg, cloud_event, data: energy_charts_mqtt_producer_data.Info, topic_params: dict):
        """Handler for info.energy_charts.mqtt.Info messages."""
        received_data.append(data)
        assert cloud_event['type'] == "info.energy_charts.Info"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.info_energy_charts_mqtt_info_async = on_info_energy_charts_mqtt_info
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/info_energy_charts_mqtt/info_energy_charts_mqtt_info"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_info_energy_charts_mqtt_info(
            topic=test_topic,
            country=f"test_country_{i}",
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


