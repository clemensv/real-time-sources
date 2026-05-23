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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tfl_road_traffic_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tfl_road_traffic_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tfl_road_traffic_mqtt_producer_mqtt_client/src')))

import tfl_road_traffic_mqtt_producer_data
from tfl_road_traffic_mqtt_producer_data import RoadCorridor
from test_tfl_road_traffic_mqtt_producer_data_roadcorridor import Test_RoadCorridor
from tfl_road_traffic_mqtt_producer_data import RoadStatus
from test_tfl_road_traffic_mqtt_producer_data_roadstatus import Test_RoadStatus
from tfl_road_traffic_mqtt_producer_data import RoadDisruption
from test_tfl_road_traffic_mqtt_producer_data_roaddisruption import Test_RoadDisruption
from tfl_road_traffic_mqtt_producer_mqtt_client import UkGovTflRoadMqttMqttClient

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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_corridor_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadCorridor message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadCorridor.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_corridor(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadCorridor, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadCorridor messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadCorridor"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_corridor_async = on_uk_gov_tfl_road_mqtt_road_corridor
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_corridor"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_corridor(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_status_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadStatus message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadStatus.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_status(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadStatus, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadStatus messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadStatus"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_status_async = on_uk_gov_tfl_road_mqtt_road_status
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_status"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_status(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_disruption_serious_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadDisruptionSerious message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadDisruption.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_disruption_serious(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadDisruption, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadDisruptionSerious messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadDisruption"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_disruption_serious_async = on_uk_gov_tfl_road_mqtt_road_disruption_serious
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_disruption_serious"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_disruption_serious(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
            severity=f"test_severity_{i}",
            disruption_id=f"test_disruption_id_{i}",
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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_disruption_severe_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadDisruptionSevere message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadDisruption.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_disruption_severe(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadDisruption, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadDisruptionSevere messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadDisruption"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_disruption_severe_async = on_uk_gov_tfl_road_mqtt_road_disruption_severe
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_disruption_severe"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_disruption_severe(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
            severity=f"test_severity_{i}",
            disruption_id=f"test_disruption_id_{i}",
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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_disruption_moderate_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadDisruptionModerate message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadDisruption.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_disruption_moderate(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadDisruption, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadDisruptionModerate messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadDisruption"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_disruption_moderate_async = on_uk_gov_tfl_road_mqtt_road_disruption_moderate
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_disruption_moderate"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_disruption_moderate(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
            severity=f"test_severity_{i}",
            disruption_id=f"test_disruption_id_{i}",
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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_disruption_minor_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadDisruptionMinor message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadDisruption.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_disruption_minor(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadDisruption, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadDisruptionMinor messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadDisruption"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_disruption_minor_async = on_uk_gov_tfl_road_mqtt_road_disruption_minor
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_disruption_minor"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_disruption_minor(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
            severity=f"test_severity_{i}",
            disruption_id=f"test_disruption_id_{i}",
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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_disruption_information_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadDisruptionInformation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadDisruption.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_disruption_information(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadDisruption, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadDisruptionInformation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadDisruption"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_disruption_information_async = on_uk_gov_tfl_road_mqtt_road_disruption_information
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_disruption_information"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_disruption_information(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
            severity=f"test_severity_{i}",
            disruption_id=f"test_disruption_id_{i}",
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
async def test_uk_gov_tfl_road_mqtt_uk_gov_tfl_road_mqtt_road_disruption_closure_py(mosquitto_broker):
    """Test publishing and receiving uk.gov.tfl.road.mqtt.RoadDisruptionClosure message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadDisruption.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkGovTflRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkGovTflRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_gov_tfl_road_mqtt_road_disruption_closure(mqtt_msg, cloud_event, data: tfl_road_traffic_mqtt_producer_data.RoadDisruption, topic_params: dict):
        """Handler for uk.gov.tfl.road.mqtt.RoadDisruptionClosure messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.gov.tfl.road.RoadDisruption"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_gov_tfl_road_mqtt_road_disruption_closure_async = on_uk_gov_tfl_road_mqtt_road_disruption_closure
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_gov_tfl_road_mqtt/uk_gov_tfl_road_mqtt_road_disruption_closure"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_gov_tfl_road_mqtt_road_disruption_closure(
            topic=test_topic,
            road_id=f"test_road_id_{i}",
            severity=f"test_severity_{i}",
            disruption_id=f"test_disruption_id_{i}",
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


