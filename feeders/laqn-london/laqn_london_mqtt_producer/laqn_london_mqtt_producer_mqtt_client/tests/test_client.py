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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../laqn_london_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../laqn_london_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../laqn_london_mqtt_producer_mqtt_client/src')))

import laqn_london_mqtt_producer_data
from laqn_london_mqtt_producer_data import Site
from test_laqn_london_mqtt_producer_data_site import Test_Site
from laqn_london_mqtt_producer_data import Measurement
from test_laqn_london_mqtt_producer_data_measurement import Test_Measurement
from laqn_london_mqtt_producer_data import DailyIndex
from test_laqn_london_mqtt_producer_data_dailyindex import Test_DailyIndex
from laqn_london_mqtt_producer_data import Species
from test_laqn_london_mqtt_producer_data_species import Test_Species
from laqn_london_mqtt_producer_mqtt_client import UkKclLaqnMqttMqttClient
from laqn_london_mqtt_producer_mqtt_client import UkKclLaqnSpeciesMqttMqttClient

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
async def test_uk_kcl_laqn_mqtt_uk_kcl_laqn_mqtt_site_py(mosquitto_broker):
    """Test publishing and receiving uk.kcl.laqn.mqtt.Site message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Site.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkKclLaqnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkKclLaqnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_kcl_laqn_mqtt_site(mqtt_msg, cloud_event, data: laqn_london_mqtt_producer_data.Site, topic_params: dict):
        """Handler for uk.kcl.laqn.mqtt.Site messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.kcl.laqn.Site"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_kcl_laqn_mqtt_site_async = on_uk_kcl_laqn_mqtt_site
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_kcl_laqn_mqtt/uk_kcl_laqn_mqtt_site"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_kcl_laqn_mqtt_site(
            topic=test_topic,
            site_code=f"test_site_code_{i}",
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
async def test_uk_kcl_laqn_mqtt_uk_kcl_laqn_mqtt_measurement_py(mosquitto_broker):
    """Test publishing and receiving uk.kcl.laqn.mqtt.Measurement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Measurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkKclLaqnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkKclLaqnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_kcl_laqn_mqtt_measurement(mqtt_msg, cloud_event, data: laqn_london_mqtt_producer_data.Measurement, topic_params: dict):
        """Handler for uk.kcl.laqn.mqtt.Measurement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.kcl.laqn.Measurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_kcl_laqn_mqtt_measurement_async = on_uk_kcl_laqn_mqtt_measurement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_kcl_laqn_mqtt/uk_kcl_laqn_mqtt_measurement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_kcl_laqn_mqtt_measurement(
            topic=test_topic,
            site_code=f"test_site_code_{i}",
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
async def test_uk_kcl_laqn_mqtt_uk_kcl_laqn_mqtt_daily_index_py(mosquitto_broker):
    """Test publishing and receiving uk.kcl.laqn.mqtt.DailyIndex message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DailyIndex.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkKclLaqnMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkKclLaqnMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_kcl_laqn_mqtt_daily_index(mqtt_msg, cloud_event, data: laqn_london_mqtt_producer_data.DailyIndex, topic_params: dict):
        """Handler for uk.kcl.laqn.mqtt.DailyIndex messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.kcl.laqn.DailyIndex"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_kcl_laqn_mqtt_daily_index_async = on_uk_kcl_laqn_mqtt_daily_index
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_kcl_laqn_mqtt/uk_kcl_laqn_mqtt_daily_index"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_kcl_laqn_mqtt_daily_index(
            topic=test_topic,
            site_code=f"test_site_code_{i}",
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
async def test_uk_kcl_laqn_species_mqtt_uk_kcl_laqn_species_mqtt_species_py(mosquitto_broker):
    """Test publishing and receiving uk.kcl.laqn.species.mqtt.Species message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Species.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UkKclLaqnSpeciesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UkKclLaqnSpeciesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_kcl_laqn_species_mqtt_species(mqtt_msg, cloud_event, data: laqn_london_mqtt_producer_data.Species, topic_params: dict):
        """Handler for uk.kcl.laqn.species.mqtt.Species messages."""
        received_data.append(data)
        assert cloud_event['type'] == "uk.kcl.laqn.Species"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_kcl_laqn_species_mqtt_species_async = on_uk_kcl_laqn_species_mqtt_species
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_kcl_laqn_species_mqtt/uk_kcl_laqn_species_mqtt_species"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_kcl_laqn_species_mqtt_species(
            topic=test_topic,
            species_code=f"test_species_code_{i}",
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


