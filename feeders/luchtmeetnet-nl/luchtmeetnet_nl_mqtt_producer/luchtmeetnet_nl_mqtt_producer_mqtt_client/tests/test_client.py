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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../luchtmeetnet_nl_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../luchtmeetnet_nl_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../luchtmeetnet_nl_mqtt_producer_mqtt_client/src')))

import luchtmeetnet_nl_mqtt_producer_data
from luchtmeetnet_nl_mqtt_producer_data import Station
from test_station import Test_Station
from luchtmeetnet_nl_mqtt_producer_data import Measurement
from test_measurement import Test_Measurement
from luchtmeetnet_nl_mqtt_producer_data import LKI
from test_lki import Test_LKI
from luchtmeetnet_nl_mqtt_producer_data import Component
from test_component import Test_Component
from luchtmeetnet_nl_mqtt_producer_mqtt_client import NlRivmLuchtmeetnetMqttMqttClient
from luchtmeetnet_nl_mqtt_producer_mqtt_client import NlRivmLuchtmeetnetComponentsMqttMqttClient

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
async def test_nl_rivm_luchtmeetnet_mqtt_nl_rivm_luchtmeetnet_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving nl.rivm.luchtmeetnet.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NlRivmLuchtmeetnetMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NlRivmLuchtmeetnetMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_rivm_luchtmeetnet_mqtt_station(mqtt_msg, cloud_event, data: luchtmeetnet_nl_mqtt_producer_data.Station, topic_params: dict):
        """Handler for nl.rivm.luchtmeetnet.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "nl.rivm.luchtmeetnet.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_rivm_luchtmeetnet_mqtt_station_async = on_nl_rivm_luchtmeetnet_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_rivm_luchtmeetnet_mqtt/nl_rivm_luchtmeetnet_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_rivm_luchtmeetnet_mqtt_station(
            topic=test_topic,
            station_number=f"test_station_number_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
            formula="test_formula",
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
async def test_nl_rivm_luchtmeetnet_mqtt_nl_rivm_luchtmeetnet_mqtt_measurement_py(mosquitto_broker):
    """Test publishing and receiving nl.rivm.luchtmeetnet.mqtt.Measurement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Measurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NlRivmLuchtmeetnetMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NlRivmLuchtmeetnetMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_rivm_luchtmeetnet_mqtt_measurement(mqtt_msg, cloud_event, data: luchtmeetnet_nl_mqtt_producer_data.Measurement, topic_params: dict):
        """Handler for nl.rivm.luchtmeetnet.mqtt.Measurement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "nl.rivm.luchtmeetnet.Measurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_rivm_luchtmeetnet_mqtt_measurement_async = on_nl_rivm_luchtmeetnet_mqtt_measurement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_rivm_luchtmeetnet_mqtt/nl_rivm_luchtmeetnet_mqtt_measurement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_rivm_luchtmeetnet_mqtt_measurement(
            topic=test_topic,
            station_number=f"test_station_number_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
            formula="test_formula",
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
async def test_nl_rivm_luchtmeetnet_mqtt_nl_rivm_luchtmeetnet_mqtt_lki_py(mosquitto_broker):
    """Test publishing and receiving nl.rivm.luchtmeetnet.mqtt.LKI message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LKI.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NlRivmLuchtmeetnetMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NlRivmLuchtmeetnetMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_rivm_luchtmeetnet_mqtt_lki(mqtt_msg, cloud_event, data: luchtmeetnet_nl_mqtt_producer_data.LKI, topic_params: dict):
        """Handler for nl.rivm.luchtmeetnet.mqtt.LKI messages."""
        received_data.append(data)
        assert cloud_event['type'] == "nl.rivm.luchtmeetnet.LKI"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_rivm_luchtmeetnet_mqtt_lki_async = on_nl_rivm_luchtmeetnet_mqtt_lki
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_rivm_luchtmeetnet_mqtt/nl_rivm_luchtmeetnet_mqtt_lki"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_rivm_luchtmeetnet_mqtt_lki(
            topic=test_topic,
            station_number=f"test_station_number_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
            formula="test_formula",
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
async def test_nl_rivm_luchtmeetnet_components_mqtt_nl_rivm_luchtmeetnet_components_mqtt_component_py(mosquitto_broker):
    """Test publishing and receiving nl.rivm.luchtmeetnet.components.mqtt.Component message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Component.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NlRivmLuchtmeetnetComponentsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NlRivmLuchtmeetnetComponentsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_rivm_luchtmeetnet_components_mqtt_component(mqtt_msg, cloud_event, data: luchtmeetnet_nl_mqtt_producer_data.Component, topic_params: dict):
        """Handler for nl.rivm.luchtmeetnet.components.mqtt.Component messages."""
        received_data.append(data)
        assert cloud_event['type'] == "nl.rivm.luchtmeetnet.components.Component"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_rivm_luchtmeetnet_components_mqtt_component_async = on_nl_rivm_luchtmeetnet_components_mqtt_component
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_rivm_luchtmeetnet_components_mqtt/nl_rivm_luchtmeetnet_components_mqtt_component"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_rivm_luchtmeetnet_components_mqtt_component(
            topic=test_topic,
            formula=f"test_formula_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
            station_number="test_station_number",
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


