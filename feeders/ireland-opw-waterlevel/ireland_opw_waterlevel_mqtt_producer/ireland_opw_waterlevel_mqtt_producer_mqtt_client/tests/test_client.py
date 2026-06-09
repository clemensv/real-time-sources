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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ireland_opw_waterlevel_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ireland_opw_waterlevel_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ireland_opw_waterlevel_mqtt_producer_mqtt_client/src')))

import ireland_opw_waterlevel_mqtt_producer_data
from ireland_opw_waterlevel_mqtt_producer_data import Station
from test_station import Test_Station
from ireland_opw_waterlevel_mqtt_producer_data import WaterLevelReading
from test_waterlevelreading import Test_WaterLevelReading
from ireland_opw_waterlevel_mqtt_producer_mqtt_client import IeGovOpwWaterlevelMqttMqttClient

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
async def test_ie_gov_opw_waterlevel_mqtt_ie_gov_opw_waterlevel_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving ie.gov.opw.waterlevel.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IeGovOpwWaterlevelMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IeGovOpwWaterlevelMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_ie_gov_opw_waterlevel_mqtt_station(mqtt_msg, cloud_event, data: ireland_opw_waterlevel_mqtt_producer_data.Station, topic_params: dict):
        """Handler for ie.gov.opw.waterlevel.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "ie.gov.opw.waterlevel.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.ie_gov_opw_waterlevel_mqtt_station_async = on_ie_gov_opw_waterlevel_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/ie_gov_opw_waterlevel_mqtt/ie_gov_opw_waterlevel_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_ie_gov_opw_waterlevel_mqtt_station(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_ref=f"test_station_ref_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            basin="test_basin",
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
async def test_ie_gov_opw_waterlevel_mqtt_ie_gov_opw_waterlevel_mqtt_water_level_reading_py(mosquitto_broker):
    """Test publishing and receiving ie.gov.opw.waterlevel.mqtt.WaterLevelReading message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WaterLevelReading.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IeGovOpwWaterlevelMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IeGovOpwWaterlevelMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_ie_gov_opw_waterlevel_mqtt_water_level_reading(mqtt_msg, cloud_event, data: ireland_opw_waterlevel_mqtt_producer_data.WaterLevelReading, topic_params: dict):
        """Handler for ie.gov.opw.waterlevel.mqtt.WaterLevelReading messages."""
        received_data.append(data)
        assert cloud_event['type'] == "ie.gov.opw.waterlevel.WaterLevelReading"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.ie_gov_opw_waterlevel_mqtt_water_level_reading_async = on_ie_gov_opw_waterlevel_mqtt_water_level_reading
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/ie_gov_opw_waterlevel_mqtt/ie_gov_opw_waterlevel_mqtt_water_level_reading"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_ie_gov_opw_waterlevel_mqtt_water_level_reading(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_ref=f"test_station_ref_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            basin="test_basin",
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


