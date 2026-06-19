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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gbfs_bikeshare_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gbfs_bikeshare_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gbfs_bikeshare_mqtt_producer_mqtt_client/src')))

import gbfs_bikeshare_mqtt_producer_data
from gbfs_bikeshare_mqtt_producer_data import SystemInformation
from test_systeminformation import Test_SystemInformation
from gbfs_bikeshare_mqtt_producer_data import StationInformation
from test_stationinformation import Test_StationInformation
from gbfs_bikeshare_mqtt_producer_data import StationStatus
from test_stationstatus import Test_StationStatus
from gbfs_bikeshare_mqtt_producer_data import FreeBikeStatus
from test_freebikestatus import Test_FreeBikeStatus
from gbfs_bikeshare_mqtt_producer_mqtt_client import OrgGbfsMqttSystemMqttClient
from gbfs_bikeshare_mqtt_producer_mqtt_client import OrgGbfsMqttStationsMqttClient
from gbfs_bikeshare_mqtt_producer_mqtt_client import OrgGbfsMqttFreeBikesMqttClient

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
async def test_org_gbfs_mqtt_system_org_gbfs_mqtt_system_information_py(mosquitto_broker):
    """Test publishing and receiving org.gbfs.mqtt.SystemInformation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SystemInformation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgGbfsMqttSystemMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgGbfsMqttSystemMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_gbfs_mqtt_system_information(mqtt_msg, cloud_event, data: gbfs_bikeshare_mqtt_producer_data.SystemInformation, topic_params: dict):
        """Handler for org.gbfs.mqtt.SystemInformation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.gbfs.SystemInformation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_gbfs_mqtt_system_information_async = on_org_gbfs_mqtt_system_information
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_gbfs_mqtt_system/org_gbfs_mqtt_system_information"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_gbfs_mqtt_system_information(
            topic=test_topic,
            feed_url=f"test_feed_url_{i}",
            system_id=f"test_system_id_{i}",
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
async def test_org_gbfs_mqtt_stations_org_gbfs_mqtt_station_information_py(mosquitto_broker):
    """Test publishing and receiving org.gbfs.mqtt.StationInformation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StationInformation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgGbfsMqttStationsMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgGbfsMqttStationsMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_gbfs_mqtt_station_information(mqtt_msg, cloud_event, data: gbfs_bikeshare_mqtt_producer_data.StationInformation, topic_params: dict):
        """Handler for org.gbfs.mqtt.StationInformation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.gbfs.StationInformation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_gbfs_mqtt_station_information_async = on_org_gbfs_mqtt_station_information
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_gbfs_mqtt_stations/org_gbfs_mqtt_station_information"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_gbfs_mqtt_station_information(
            topic=test_topic,
            feed_url=f"test_feed_url_{i}",
            system_id=f"test_system_id_{i}",
            station_id=f"test_station_id_{i}",
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
async def test_org_gbfs_mqtt_stations_org_gbfs_mqtt_station_status_py(mosquitto_broker):
    """Test publishing and receiving org.gbfs.mqtt.StationStatus message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StationStatus.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgGbfsMqttStationsMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgGbfsMqttStationsMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_gbfs_mqtt_station_status(mqtt_msg, cloud_event, data: gbfs_bikeshare_mqtt_producer_data.StationStatus, topic_params: dict):
        """Handler for org.gbfs.mqtt.StationStatus messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.gbfs.StationStatus"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_gbfs_mqtt_station_status_async = on_org_gbfs_mqtt_station_status
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_gbfs_mqtt_stations/org_gbfs_mqtt_station_status"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_gbfs_mqtt_station_status(
            topic=test_topic,
            feed_url=f"test_feed_url_{i}",
            system_id=f"test_system_id_{i}",
            station_id=f"test_station_id_{i}",
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
async def test_org_gbfs_mqtt_free_bikes_org_gbfs_mqtt_free_bike_status_py(mosquitto_broker):
    """Test publishing and receiving org.gbfs.mqtt.FreeBikeStatus message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FreeBikeStatus.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgGbfsMqttFreeBikesMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgGbfsMqttFreeBikesMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_gbfs_mqtt_free_bike_status(mqtt_msg, cloud_event, data: gbfs_bikeshare_mqtt_producer_data.FreeBikeStatus, topic_params: dict):
        """Handler for org.gbfs.mqtt.FreeBikeStatus messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.gbfs.FreeBikeStatus"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_gbfs_mqtt_free_bike_status_async = on_org_gbfs_mqtt_free_bike_status
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_gbfs_mqtt_free_bikes/org_gbfs_mqtt_free_bike_status"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_gbfs_mqtt_free_bike_status(
            topic=test_topic,
            feed_url=f"test_feed_url_{i}",
            system_id=f"test_system_id_{i}",
            bike_id=f"test_bike_id_{i}",
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


