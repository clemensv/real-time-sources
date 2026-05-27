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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_mqtt_producer_mqtt_client/src')))

import autobahn_mqtt_producer_data
from autobahn_mqtt_producer_data import RoadEvent
from test_autobahn_mqtt_producer_data_roadevent import Test_RoadEvent
from autobahn_mqtt_producer_data import WarningEvent
from test_autobahn_mqtt_producer_data_warningevent import Test_WarningEvent
from autobahn_mqtt_producer_data import Webcam
from test_autobahn_mqtt_producer_data_webcam import Test_Webcam
from autobahn_mqtt_producer_data import ParkingLorry
from test_autobahn_mqtt_producer_data_parkinglorry import Test_ParkingLorry
from autobahn_mqtt_producer_data import ChargingStation
from test_autobahn_mqtt_producer_data_chargingstation import Test_ChargingStation
from autobahn_mqtt_producer_mqtt_client import DEAutobahnMqttMqttClient

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
async def test_de_autobahn_mqtt_de_autobahn_roadwork_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.RoadworkAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_roadwork_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.RoadworkAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.RoadworkAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_roadwork_appeared_mqtt_async = on_de_autobahn_roadwork_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_roadwork_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_roadwork_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_roadwork_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.RoadworkUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_roadwork_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.RoadworkUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.RoadworkUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_roadwork_updated_mqtt_async = on_de_autobahn_roadwork_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_roadwork_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_roadwork_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_roadwork_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.RoadworkResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_roadwork_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.RoadworkResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.RoadworkResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_roadwork_resolved_mqtt_async = on_de_autobahn_roadwork_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_roadwork_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_roadwork_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_short_term_roadwork_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ShortTermRoadworkAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_short_term_roadwork_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.ShortTermRoadworkAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ShortTermRoadworkAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_short_term_roadwork_appeared_mqtt_async = on_de_autobahn_short_term_roadwork_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_short_term_roadwork_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_short_term_roadwork_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_short_term_roadwork_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ShortTermRoadworkUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_short_term_roadwork_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.ShortTermRoadworkUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ShortTermRoadworkUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_short_term_roadwork_updated_mqtt_async = on_de_autobahn_short_term_roadwork_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_short_term_roadwork_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_short_term_roadwork_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_short_term_roadwork_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ShortTermRoadworkResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_short_term_roadwork_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.ShortTermRoadworkResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ShortTermRoadworkResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_short_term_roadwork_resolved_mqtt_async = on_de_autobahn_short_term_roadwork_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_short_term_roadwork_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_short_term_roadwork_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_closure_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ClosureAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_closure_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.ClosureAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ClosureAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_closure_appeared_mqtt_async = on_de_autobahn_closure_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_closure_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_closure_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_closure_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ClosureUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_closure_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.ClosureUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ClosureUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_closure_updated_mqtt_async = on_de_autobahn_closure_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_closure_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_closure_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_closure_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ClosureResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_closure_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.ClosureResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ClosureResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_closure_resolved_mqtt_async = on_de_autobahn_closure_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_closure_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_closure_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_entry_exit_closure_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.EntryExitClosureAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_entry_exit_closure_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.EntryExitClosureAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.EntryExitClosureAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_entry_exit_closure_appeared_mqtt_async = on_de_autobahn_entry_exit_closure_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_entry_exit_closure_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_entry_exit_closure_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_entry_exit_closure_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.EntryExitClosureUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_entry_exit_closure_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.EntryExitClosureUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.EntryExitClosureUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_entry_exit_closure_updated_mqtt_async = on_de_autobahn_entry_exit_closure_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_entry_exit_closure_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_entry_exit_closure_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_entry_exit_closure_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.EntryExitClosureResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_entry_exit_closure_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.EntryExitClosureResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.EntryExitClosureResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_entry_exit_closure_resolved_mqtt_async = on_de_autobahn_entry_exit_closure_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_entry_exit_closure_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_entry_exit_closure_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_warning_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WarningAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WarningEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_warning_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.WarningEvent, topic_params: dict):
        """Handler for DE.Autobahn.WarningAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WarningAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_warning_appeared_mqtt_async = on_de_autobahn_warning_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_warning_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_warning_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_warning_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WarningUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WarningEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_warning_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.WarningEvent, topic_params: dict):
        """Handler for DE.Autobahn.WarningUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WarningUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_warning_updated_mqtt_async = on_de_autobahn_warning_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_warning_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_warning_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_warning_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WarningResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WarningEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_warning_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.WarningEvent, topic_params: dict):
        """Handler for DE.Autobahn.WarningResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WarningResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_warning_resolved_mqtt_async = on_de_autobahn_warning_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_warning_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_warning_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_weight_limit35_restriction_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_weight_limit35_restriction_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WeightLimit35RestrictionAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_weight_limit35_restriction_appeared_mqtt_async = on_de_autobahn_weight_limit35_restriction_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_weight_limit35_restriction_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_weight_limit35_restriction_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_weight_limit35_restriction_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_weight_limit35_restriction_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WeightLimit35RestrictionUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_weight_limit35_restriction_updated_mqtt_async = on_de_autobahn_weight_limit35_restriction_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_weight_limit35_restriction_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_weight_limit35_restriction_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_weight_limit35_restriction_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WeightLimit35RestrictionResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_weight_limit35_restriction_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for DE.Autobahn.WeightLimit35RestrictionResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WeightLimit35RestrictionResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_weight_limit35_restriction_resolved_mqtt_async = on_de_autobahn_weight_limit35_restriction_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_weight_limit35_restriction_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_weight_limit35_restriction_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_webcam_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WebcamAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Webcam.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_webcam_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.Webcam, topic_params: dict):
        """Handler for DE.Autobahn.WebcamAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WebcamAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_webcam_appeared_mqtt_async = on_de_autobahn_webcam_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_webcam_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_webcam_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_webcam_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WebcamUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Webcam.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_webcam_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.Webcam, topic_params: dict):
        """Handler for DE.Autobahn.WebcamUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WebcamUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_webcam_updated_mqtt_async = on_de_autobahn_webcam_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_webcam_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_webcam_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_webcam_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.WebcamResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Webcam.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_webcam_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.Webcam, topic_params: dict):
        """Handler for DE.Autobahn.WebcamResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.WebcamResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_webcam_resolved_mqtt_async = on_de_autobahn_webcam_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_webcam_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_webcam_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_parking_lorry_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ParkingLorryAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ParkingLorry.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_parking_lorry_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ParkingLorry, topic_params: dict):
        """Handler for DE.Autobahn.ParkingLorryAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ParkingLorryAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_parking_lorry_appeared_mqtt_async = on_de_autobahn_parking_lorry_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_parking_lorry_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_parking_lorry_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_parking_lorry_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ParkingLorryUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ParkingLorry.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_parking_lorry_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ParkingLorry, topic_params: dict):
        """Handler for DE.Autobahn.ParkingLorryUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ParkingLorryUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_parking_lorry_updated_mqtt_async = on_de_autobahn_parking_lorry_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_parking_lorry_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_parking_lorry_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_parking_lorry_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ParkingLorryResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ParkingLorry.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_parking_lorry_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ParkingLorry, topic_params: dict):
        """Handler for DE.Autobahn.ParkingLorryResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ParkingLorryResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_parking_lorry_resolved_mqtt_async = on_de_autobahn_parking_lorry_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_parking_lorry_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_parking_lorry_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_electric_charging_station_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ElectricChargingStationAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargingStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_electric_charging_station_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ChargingStation, topic_params: dict):
        """Handler for DE.Autobahn.ElectricChargingStationAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ElectricChargingStationAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_electric_charging_station_appeared_mqtt_async = on_de_autobahn_electric_charging_station_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_electric_charging_station_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_electric_charging_station_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_electric_charging_station_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ElectricChargingStationUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargingStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_electric_charging_station_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ChargingStation, topic_params: dict):
        """Handler for DE.Autobahn.ElectricChargingStationUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ElectricChargingStationUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_electric_charging_station_updated_mqtt_async = on_de_autobahn_electric_charging_station_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_electric_charging_station_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_electric_charging_station_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_electric_charging_station_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.ElectricChargingStationResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargingStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_electric_charging_station_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ChargingStation, topic_params: dict):
        """Handler for DE.Autobahn.ElectricChargingStationResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.ElectricChargingStationResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_electric_charging_station_resolved_mqtt_async = on_de_autobahn_electric_charging_station_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_electric_charging_station_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_electric_charging_station_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_strong_electric_charging_station_appeared_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.StrongElectricChargingStationAppeared.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargingStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_strong_electric_charging_station_appeared_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ChargingStation, topic_params: dict):
        """Handler for DE.Autobahn.StrongElectricChargingStationAppeared.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.StrongElectricChargingStationAppeared"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_strong_electric_charging_station_appeared_mqtt_async = on_de_autobahn_strong_electric_charging_station_appeared_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_strong_electric_charging_station_appeared_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_strong_electric_charging_station_appeared_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_strong_electric_charging_station_updated_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.StrongElectricChargingStationUpdated.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargingStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_strong_electric_charging_station_updated_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ChargingStation, topic_params: dict):
        """Handler for DE.Autobahn.StrongElectricChargingStationUpdated.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.StrongElectricChargingStationUpdated"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_strong_electric_charging_station_updated_mqtt_async = on_de_autobahn_strong_electric_charging_station_updated_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_strong_electric_charging_station_updated_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_strong_electric_charging_station_updated_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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
async def test_de_autobahn_mqtt_de_autobahn_strong_electric_charging_station_resolved_mqtt_py(mosquitto_broker):
    """Test publishing and receiving DE.Autobahn.StrongElectricChargingStationResolved.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargingStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEAutobahnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEAutobahnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_autobahn_strong_electric_charging_station_resolved_mqtt(mqtt_msg, cloud_event, data: autobahn_mqtt_producer_data.ChargingStation, topic_params: dict):
        """Handler for DE.Autobahn.StrongElectricChargingStationResolved.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.Autobahn.StrongElectricChargingStationResolved"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_autobahn_strong_electric_charging_station_resolved_mqtt_async = on_de_autobahn_strong_electric_charging_station_resolved_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_autobahn_mqtt/de_autobahn_strong_electric_charging_station_resolved_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_autobahn_strong_electric_charging_station_resolved_mqtt(
            topic=test_topic,
            identifier=f"test_identifier_{i}",
            event_time=f"test_event_time_{i}",
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


