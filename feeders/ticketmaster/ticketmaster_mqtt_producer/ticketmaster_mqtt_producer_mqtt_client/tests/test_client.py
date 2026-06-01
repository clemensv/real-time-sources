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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ticketmaster_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ticketmaster_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ticketmaster_mqtt_producer_mqtt_client/src')))

import ticketmaster_mqtt_producer_data
from ticketmaster_mqtt_producer_data import Event
from test_ticketmaster_mqtt_producer_data_event import Test_Event
from ticketmaster_mqtt_producer_data import Venue
from test_ticketmaster_mqtt_producer_data_venue import Test_Venue
from ticketmaster_mqtt_producer_data import Attraction
from test_ticketmaster_mqtt_producer_data_attraction import Test_Attraction
from ticketmaster_mqtt_producer_data import Classification
from test_ticketmaster_mqtt_producer_data_classification import Test_Classification
from ticketmaster_mqtt_producer_data import Info
from test_ticketmaster_mqtt_producer_data_info import Test_Info
from ticketmaster_mqtt_producer_mqtt_client import TicketmasterEventsMqttMqttClient
from ticketmaster_mqtt_producer_mqtt_client import TicketmasterReferenceMqttMqttClient

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
async def test_ticketmaster_events_mqtt_ticketmaster_events_mqtt_event_py(mosquitto_broker):
    """Test publishing and receiving Ticketmaster.Events.mqtt.Event message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Event.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = TicketmasterEventsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = TicketmasterEventsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_ticketmaster_events_mqtt_event(mqtt_msg, cloud_event, data: ticketmaster_mqtt_producer_data.Event, topic_params: dict):
        """Handler for Ticketmaster.Events.mqtt.Event messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Ticketmaster.Events.Event"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.ticketmaster_events_mqtt_event_async = on_ticketmaster_events_mqtt_event
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/ticketmaster_events_mqtt/ticketmaster_events_mqtt_event"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_ticketmaster_events_mqtt_event(
            topic=test_topic,
            event_id=f"test_event_id_{i}",
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
async def test_ticketmaster_reference_mqtt_ticketmaster_reference_mqtt_venue_py(mosquitto_broker):
    """Test publishing and receiving Ticketmaster.Reference.mqtt.Venue message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Venue.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = TicketmasterReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = TicketmasterReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_ticketmaster_reference_mqtt_venue(mqtt_msg, cloud_event, data: ticketmaster_mqtt_producer_data.Venue, topic_params: dict):
        """Handler for Ticketmaster.Reference.mqtt.Venue messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Ticketmaster.Reference.Venue"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.ticketmaster_reference_mqtt_venue_async = on_ticketmaster_reference_mqtt_venue
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/ticketmaster_reference_mqtt/ticketmaster_reference_mqtt_venue"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_ticketmaster_reference_mqtt_venue(
            topic=test_topic,
            entity_id=f"test_entity_id_{i}",
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
async def test_ticketmaster_reference_mqtt_ticketmaster_reference_mqtt_attraction_py(mosquitto_broker):
    """Test publishing and receiving Ticketmaster.Reference.mqtt.Attraction message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Attraction.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = TicketmasterReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = TicketmasterReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_ticketmaster_reference_mqtt_attraction(mqtt_msg, cloud_event, data: ticketmaster_mqtt_producer_data.Attraction, topic_params: dict):
        """Handler for Ticketmaster.Reference.mqtt.Attraction messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Ticketmaster.Reference.Attraction"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.ticketmaster_reference_mqtt_attraction_async = on_ticketmaster_reference_mqtt_attraction
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/ticketmaster_reference_mqtt/ticketmaster_reference_mqtt_attraction"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_ticketmaster_reference_mqtt_attraction(
            topic=test_topic,
            entity_id=f"test_entity_id_{i}",
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
async def test_ticketmaster_reference_mqtt_ticketmaster_reference_mqtt_classification_py(mosquitto_broker):
    """Test publishing and receiving Ticketmaster.Reference.mqtt.Classification message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Classification.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = TicketmasterReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = TicketmasterReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_ticketmaster_reference_mqtt_classification(mqtt_msg, cloud_event, data: ticketmaster_mqtt_producer_data.Classification, topic_params: dict):
        """Handler for Ticketmaster.Reference.mqtt.Classification messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Ticketmaster.Reference.Classification"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.ticketmaster_reference_mqtt_classification_async = on_ticketmaster_reference_mqtt_classification
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/ticketmaster_reference_mqtt/ticketmaster_reference_mqtt_classification"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_ticketmaster_reference_mqtt_classification(
            topic=test_topic,
            entity_id=f"test_entity_id_{i}",
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
async def test_ticketmaster_reference_mqtt_ticketmaster_reference_mqtt_info_py(mosquitto_broker):
    """Test publishing and receiving Ticketmaster.Reference.mqtt.Info message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Info.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = TicketmasterReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = TicketmasterReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_ticketmaster_reference_mqtt_info(mqtt_msg, cloud_event, data: ticketmaster_mqtt_producer_data.Info, topic_params: dict):
        """Handler for Ticketmaster.Reference.mqtt.Info messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Ticketmaster.Reference.Info"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.ticketmaster_reference_mqtt_info_async = on_ticketmaster_reference_mqtt_info
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/ticketmaster_reference_mqtt/ticketmaster_reference_mqtt_info"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_ticketmaster_reference_mqtt_info(
            topic=test_topic,
            entity_id=f"test_entity_id_{i}",
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


