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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../kiwis_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../kiwis_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../kiwis_mqtt_producer_mqtt_client/src')))

import kiwis_mqtt_producer_data
from kiwis_mqtt_producer_data import Station
from test_station import Test_Station
from kiwis_mqtt_producer_data import Timeseries
from test_timeseries import Test_Timeseries
from kiwis_mqtt_producer_data import TimeseriesValue
from test_timeseriesvalue import Test_TimeseriesValue
from kiwis_mqtt_producer_mqtt_client import OrgKiwisStationMqttMqttClient
from kiwis_mqtt_producer_mqtt_client import OrgKiwisTimeseriesMqttMqttClient

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
async def test_org_kiwis_station_mqtt_org_kiwis_station_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving org.kiwis.station.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgKiwisStationMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgKiwisStationMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_kiwis_station_mqtt_station(mqtt_msg, cloud_event, data: kiwis_mqtt_producer_data.Station, topic_params: dict):
        """Handler for org.kiwis.station.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.kiwis.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_kiwis_station_mqtt_station_async = on_org_kiwis_station_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_kiwis_station_mqtt/org_kiwis_station_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_kiwis_station_mqtt_station(
            topic=test_topic,
            base_url=f"test_base_url_{i}",
            kiwis_id=f"test_kiwis_id_{i}",
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
async def test_org_kiwis_timeseries_mqtt_org_kiwis_timeseries_mqtt_timeseries_py(mosquitto_broker):
    """Test publishing and receiving org.kiwis.timeseries.mqtt.Timeseries message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Timeseries.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgKiwisTimeseriesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgKiwisTimeseriesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_kiwis_timeseries_mqtt_timeseries(mqtt_msg, cloud_event, data: kiwis_mqtt_producer_data.Timeseries, topic_params: dict):
        """Handler for org.kiwis.timeseries.mqtt.Timeseries messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.kiwis.Timeseries"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_kiwis_timeseries_mqtt_timeseries_async = on_org_kiwis_timeseries_mqtt_timeseries
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_kiwis_timeseries_mqtt/org_kiwis_timeseries_mqtt_timeseries"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_kiwis_timeseries_mqtt_timeseries(
            topic=test_topic,
            base_url=f"test_base_url_{i}",
            kiwis_id=f"test_kiwis_id_{i}",
            ts_id=f"test_ts_id_{i}",
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
async def test_org_kiwis_timeseries_mqtt_org_kiwis_timeseries_mqtt_timeseries_value_py(mosquitto_broker):
    """Test publishing and receiving org.kiwis.timeseries.mqtt.TimeseriesValue message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TimeseriesValue.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgKiwisTimeseriesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgKiwisTimeseriesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_kiwis_timeseries_mqtt_timeseries_value(mqtt_msg, cloud_event, data: kiwis_mqtt_producer_data.TimeseriesValue, topic_params: dict):
        """Handler for org.kiwis.timeseries.mqtt.TimeseriesValue messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.kiwis.TimeseriesValue"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_kiwis_timeseries_mqtt_timeseries_value_async = on_org_kiwis_timeseries_mqtt_timeseries_value
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_kiwis_timeseries_mqtt/org_kiwis_timeseries_mqtt_timeseries_value"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_kiwis_timeseries_mqtt_timeseries_value(
            topic=test_topic,
            base_url=f"test_base_url_{i}",
            kiwis_id=f"test_kiwis_id_{i}",
            ts_id=f"test_ts_id_{i}",
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


