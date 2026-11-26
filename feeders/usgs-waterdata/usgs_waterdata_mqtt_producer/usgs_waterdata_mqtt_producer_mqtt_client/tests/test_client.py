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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_waterdata_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_waterdata_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_waterdata_mqtt_producer_mqtt_client/src')))

import usgs_waterdata_mqtt_producer_data
from usgs_waterdata_mqtt_producer_data import ContinuousObservation
from test_continuousobservation import Test_ContinuousObservation
from usgs_waterdata_mqtt_producer_data import TimeSeries
from test_timeseries import Test_TimeSeries
from usgs_waterdata_mqtt_producer_data import MonitoringLocation
from test_monitoringlocation import Test_MonitoringLocation
from usgs_waterdata_mqtt_producer_data import Parameter
from test_parameter import Test_Parameter
from usgs_waterdata_mqtt_producer_mqtt_client import USGSWaterDataMqttMqttClient

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
async def test_usgs_waterdata_mqtt_usgs_water_data_mqtt_continuous_observation_py(mosquitto_broker):
    """Test publishing and receiving USGS.WaterData.mqtt.ContinuousObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ContinuousObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSWaterDataMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSWaterDataMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_water_data_mqtt_continuous_observation(mqtt_msg, cloud_event, data: usgs_waterdata_mqtt_producer_data.ContinuousObservation, topic_params: dict):
        """Handler for USGS.WaterData.mqtt.ContinuousObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.WaterData.ContinuousObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_water_data_mqtt_continuous_observation_async = on_usgs_water_data_mqtt_continuous_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_waterdata_mqtt/usgs_water_data_mqtt_continuous_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_water_data_mqtt_continuous_observation(
            topic=test_topic,
            time_series_id=f"test_time_series_id_{i}",
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
async def test_usgs_waterdata_mqtt_usgs_water_data_mqtt_time_series_py(mosquitto_broker):
    """Test publishing and receiving USGS.WaterData.mqtt.TimeSeries message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TimeSeries.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSWaterDataMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSWaterDataMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_water_data_mqtt_time_series(mqtt_msg, cloud_event, data: usgs_waterdata_mqtt_producer_data.TimeSeries, topic_params: dict):
        """Handler for USGS.WaterData.mqtt.TimeSeries messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.WaterData.TimeSeries"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_water_data_mqtt_time_series_async = on_usgs_water_data_mqtt_time_series
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_waterdata_mqtt/usgs_water_data_mqtt_time_series"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_water_data_mqtt_time_series(
            topic=test_topic,
            time_series_id=f"test_time_series_id_{i}",
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
async def test_usgs_waterdata_mqtt_usgs_water_data_mqtt_monitoring_location_py(mosquitto_broker):
    """Test publishing and receiving USGS.WaterData.mqtt.MonitoringLocation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MonitoringLocation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSWaterDataMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSWaterDataMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_water_data_mqtt_monitoring_location(mqtt_msg, cloud_event, data: usgs_waterdata_mqtt_producer_data.MonitoringLocation, topic_params: dict):
        """Handler for USGS.WaterData.mqtt.MonitoringLocation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.WaterData.MonitoringLocation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_water_data_mqtt_monitoring_location_async = on_usgs_water_data_mqtt_monitoring_location
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_waterdata_mqtt/usgs_water_data_mqtt_monitoring_location"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_water_data_mqtt_monitoring_location(
            topic=test_topic,
            time_series_id=f"test_time_series_id_{i}",
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
async def test_usgs_waterdata_mqtt_usgs_water_data_mqtt_parameter_py(mosquitto_broker):
    """Test publishing and receiving USGS.WaterData.mqtt.Parameter message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Parameter.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSWaterDataMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSWaterDataMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_water_data_mqtt_parameter(mqtt_msg, cloud_event, data: usgs_waterdata_mqtt_producer_data.Parameter, topic_params: dict):
        """Handler for USGS.WaterData.mqtt.Parameter messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.WaterData.Parameter"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_water_data_mqtt_parameter_async = on_usgs_water_data_mqtt_parameter
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_waterdata_mqtt/usgs_water_data_mqtt_parameter"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_water_data_mqtt_parameter(
            topic=test_topic,
            time_series_id=f"test_time_series_id_{i}",
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


