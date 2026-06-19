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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../defra_aurn_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../defra_aurn_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../defra_aurn_mqtt_producer_mqtt_client/src')))

import defra_aurn_mqtt_producer_data
from defra_aurn_mqtt_producer_data import Station
from test_station import Test_Station
from defra_aurn_mqtt_producer_data import Timeseries
from test_timeseries import Test_Timeseries
from defra_aurn_mqtt_producer_data import Observation
from test_observation import Test_Observation
from defra_aurn_mqtt_producer_mqtt_client import UkGovDefraAurnStationsMqttMqttClient
from defra_aurn_mqtt_producer_mqtt_client import UkGovDefraAurnTimeseriesMqttMqttClient

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
async def test_uk_gov_defra_aurn_stations_mqtt_uk_gov_defra_aurn_stations_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.defra.aurn.Stations.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovDefraAurnStationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovDefraAurnStationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_defra_aurn_stations_mqtt_station(mqtt_msg, cloud_event, data: defra_aurn_mqtt_producer_data.Station, topic_params: dict):
        """Handler for uk.gov.defra.aurn.Stations.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.defra.aurn.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_defra_aurn_stations_mqtt_station_async = on_uk_gov_defra_aurn_stations_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_defra_aurn_stations_mqtt/uk_gov_defra_aurn_stations_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_defra_aurn_stations_mqtt_station(
            topic=test_topic,
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
async def test_uk_gov_defra_aurn_timeseries_mqtt_uk_gov_defra_aurn_timeseries_mqtt_timeseries_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.defra.aurn.Timeseries.mqtt.Timeseries message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Timeseries.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovDefraAurnTimeseriesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovDefraAurnTimeseriesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_defra_aurn_timeseries_mqtt_timeseries(mqtt_msg, cloud_event, data: defra_aurn_mqtt_producer_data.Timeseries, topic_params: dict):
        """Handler for uk.gov.defra.aurn.Timeseries.mqtt.Timeseries messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.defra.aurn.Timeseries"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_defra_aurn_timeseries_mqtt_timeseries_async = on_uk_gov_defra_aurn_timeseries_mqtt_timeseries
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_defra_aurn_timeseries_mqtt/uk_gov_defra_aurn_timeseries_mqtt_timeseries"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_defra_aurn_timeseries_mqtt_timeseries(
            topic=test_topic,
            timeseries_id=f"test_timeseries_id_{i}",
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
async def test_uk_gov_defra_aurn_timeseries_mqtt_uk_gov_defra_aurn_timeseries_mqtt_observation_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.defra.aurn.Timeseries.mqtt.Observation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Observation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovDefraAurnTimeseriesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovDefraAurnTimeseriesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_defra_aurn_timeseries_mqtt_observation(mqtt_msg, cloud_event, data: defra_aurn_mqtt_producer_data.Observation, topic_params: dict):
        """Handler for uk.gov.defra.aurn.Timeseries.mqtt.Observation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.defra.aurn.Observation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_defra_aurn_timeseries_mqtt_observation_async = on_uk_gov_defra_aurn_timeseries_mqtt_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_defra_aurn_timeseries_mqtt/uk_gov_defra_aurn_timeseries_mqtt_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_defra_aurn_timeseries_mqtt_observation(
            topic=test_topic,
            timeseries_id=f"test_timeseries_id_{i}",
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


