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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tokyo_docomo_bikeshare_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tokyo_docomo_bikeshare_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tokyo_docomo_bikeshare_mqtt_producer_mqtt_client/src')))

import tokyo_docomo_bikeshare_mqtt_producer_data
from tokyo_docomo_bikeshare_mqtt_producer_data import BikeshareSystem
from test_tokyo_docomo_bikeshare_mqtt_producer_data_bikesharesystem import Test_BikeshareSystem
from tokyo_docomo_bikeshare_mqtt_producer_data import BikeshareStation
from test_tokyo_docomo_bikeshare_mqtt_producer_data_bikesharestation import Test_BikeshareStation
from tokyo_docomo_bikeshare_mqtt_producer_data import BikeshareStationStatus
from test_tokyo_docomo_bikeshare_mqtt_producer_data_bikesharestationstatus import Test_BikeshareStationStatus
from tokyo_docomo_bikeshare_mqtt_producer_mqtt_client import JPODPTDocomoBikeshareSystemMqttMqttClient
from tokyo_docomo_bikeshare_mqtt_producer_mqtt_client import JPODPTDocomoBikeshareStationsMqttMqttClient

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
async def test_jp_odpt_docomobikeshare_system_mqtt_jp_odpt_docomo_bikeshare_bikeshare_system_mqtt_py(mosquitto_broker):
    """Test publishing and receiving JP.ODPT.DocomoBikeshare.BikeshareSystem.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BikeshareSystem.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = JPODPTDocomoBikeshareSystemMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = JPODPTDocomoBikeshareSystemMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_jp_odpt_docomo_bikeshare_bikeshare_system_mqtt(mqtt_msg, cloud_event, data: tokyo_docomo_bikeshare_mqtt_producer_data.BikeshareSystem, topic_params: dict):
        """Handler for JP.ODPT.DocomoBikeshare.BikeshareSystem.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "JP.ODPT.DocomoBikeshare.BikeshareSystem"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.jp_odpt_docomo_bikeshare_bikeshare_system_mqtt_async = on_jp_odpt_docomo_bikeshare_bikeshare_system_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/jp_odpt_docomobikeshare_system_mqtt/jp_odpt_docomo_bikeshare_bikeshare_system_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_jp_odpt_docomo_bikeshare_bikeshare_system_mqtt(
            topic=test_topic,
            system_id=f"test_system_id_{i}",
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
async def test_jp_odpt_docomobikeshare_stations_mqtt_jp_odpt_docomo_bikeshare_bikeshare_station_mqtt_py(mosquitto_broker):
    """Test publishing and receiving JP.ODPT.DocomoBikeshare.BikeshareStation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BikeshareStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = JPODPTDocomoBikeshareStationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = JPODPTDocomoBikeshareStationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_jp_odpt_docomo_bikeshare_bikeshare_station_mqtt(mqtt_msg, cloud_event, data: tokyo_docomo_bikeshare_mqtt_producer_data.BikeshareStation, topic_params: dict):
        """Handler for JP.ODPT.DocomoBikeshare.BikeshareStation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "JP.ODPT.DocomoBikeshare.BikeshareStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.jp_odpt_docomo_bikeshare_bikeshare_station_mqtt_async = on_jp_odpt_docomo_bikeshare_bikeshare_station_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/jp_odpt_docomobikeshare_stations_mqtt/jp_odpt_docomo_bikeshare_bikeshare_station_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_jp_odpt_docomo_bikeshare_bikeshare_station_mqtt(
            topic=test_topic,
            system_id=f"test_system_id_{i}",
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
async def test_jp_odpt_docomobikeshare_stations_mqtt_jp_odpt_docomo_bikeshare_bikeshare_station_status_mqtt_py(mosquitto_broker):
    """Test publishing and receiving JP.ODPT.DocomoBikeshare.BikeshareStationStatus.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BikeshareStationStatus.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = JPODPTDocomoBikeshareStationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = JPODPTDocomoBikeshareStationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_jp_odpt_docomo_bikeshare_bikeshare_station_status_mqtt(mqtt_msg, cloud_event, data: tokyo_docomo_bikeshare_mqtt_producer_data.BikeshareStationStatus, topic_params: dict):
        """Handler for JP.ODPT.DocomoBikeshare.BikeshareStationStatus.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "JP.ODPT.DocomoBikeshare.BikeshareStationStatus"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.jp_odpt_docomo_bikeshare_bikeshare_station_status_mqtt_async = on_jp_odpt_docomo_bikeshare_bikeshare_station_status_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/jp_odpt_docomobikeshare_stations_mqtt/jp_odpt_docomo_bikeshare_bikeshare_station_status_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_jp_odpt_docomo_bikeshare_bikeshare_station_status_mqtt(
            topic=test_topic,
            system_id=f"test_system_id_{i}",
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


