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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ndl_netherlands_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ndl_netherlands_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ndl_netherlands_mqtt_producer_mqtt_client/src')))

import ndl_netherlands_mqtt_producer_data
from ndl_netherlands_mqtt_producer_data import TrafficSpeed
from test_ndl_netherlands_mqtt_producer_data_trafficspeed import Test_TrafficSpeed
from ndl_netherlands_mqtt_producer_data import TravelTime
from test_ndl_netherlands_mqtt_producer_data_traveltime import Test_TravelTime
from ndl_netherlands_mqtt_producer_data import TrafficSituation
from test_ndl_netherlands_mqtt_producer_data_trafficsituation import Test_TrafficSituation
from ndl_netherlands_mqtt_producer_mqtt_client import NLNDWTrafficMeasurementsMqttMqttClient
from ndl_netherlands_mqtt_producer_mqtt_client import NLNDWTrafficSituationsMqttMqttClient

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
async def test_nl_ndw_traffic_measurements_mqtt_nl_ndw_traffic_traffic_speed_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Traffic.TrafficSpeed.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficSpeed.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWTrafficMeasurementsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWTrafficMeasurementsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_traffic_traffic_speed_mqtt(mqtt_msg, cloud_event, data: ndl_netherlands_mqtt_producer_data.TrafficSpeed, topic_params: dict):
        """Handler for NL.NDW.Traffic.TrafficSpeed.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Traffic.TrafficSpeed"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_traffic_traffic_speed_mqtt_async = on_nl_ndw_traffic_traffic_speed_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_traffic_measurements_mqtt/nl_ndw_traffic_traffic_speed_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_traffic_traffic_speed_mqtt(
            topic=test_topic,
            site_id=f"test_site_id_{i}",
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
async def test_nl_ndw_traffic_measurements_mqtt_nl_ndw_traffic_travel_time_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Traffic.TravelTime.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TravelTime.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWTrafficMeasurementsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWTrafficMeasurementsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_traffic_travel_time_mqtt(mqtt_msg, cloud_event, data: ndl_netherlands_mqtt_producer_data.TravelTime, topic_params: dict):
        """Handler for NL.NDW.Traffic.TravelTime.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Traffic.TravelTime"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_traffic_travel_time_mqtt_async = on_nl_ndw_traffic_travel_time_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_traffic_measurements_mqtt/nl_ndw_traffic_travel_time_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_traffic_travel_time_mqtt(
            topic=test_topic,
            site_id=f"test_site_id_{i}",
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
async def test_nl_ndw_traffic_situations_mqtt_nl_ndw_traffic_traffic_situation_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Traffic.TrafficSituation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficSituation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWTrafficSituationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWTrafficSituationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_traffic_traffic_situation_mqtt(mqtt_msg, cloud_event, data: ndl_netherlands_mqtt_producer_data.TrafficSituation, topic_params: dict):
        """Handler for NL.NDW.Traffic.TrafficSituation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Traffic.TrafficSituation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_traffic_traffic_situation_mqtt_async = on_nl_ndw_traffic_traffic_situation_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_traffic_situations_mqtt/nl_ndw_traffic_traffic_situation_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_traffic_traffic_situation_mqtt(
            topic=test_topic,
            situation_id=f"test_situation_id_{i}",
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


