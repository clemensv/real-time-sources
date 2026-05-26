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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../jma_bosai_volcano_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../jma_bosai_volcano_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../jma_bosai_volcano_mqtt_producer_mqtt_client/src')))

import jma_bosai_volcano_mqtt_producer_data
from jma_bosai_volcano_mqtt_producer_data import Volcano
from test_jma_bosai_volcano_mqtt_producer_data_volcano import Test_Volcano
from jma_bosai_volcano_mqtt_producer_data import VolcanicWarning
from test_jma_bosai_volcano_mqtt_producer_data_volcanicwarning import Test_VolcanicWarning
from jma_bosai_volcano_mqtt_producer_data import VolcanicEruption
from test_jma_bosai_volcano_mqtt_producer_data_volcaniceruption import Test_VolcanicEruption
from jma_bosai_volcano_mqtt_producer_mqtt_client import JPJMAVolcanoMqttMqttClient

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
async def test_jp_jma_volcano_mqtt_jp_jma_volcano_mqtt_volcano_py(mosquitto_broker):
    """Test publishing and receiving JP.JMA.Volcano.mqtt.Volcano message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Volcano.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = JPJMAVolcanoMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = JPJMAVolcanoMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_jp_jma_volcano_mqtt_volcano(mqtt_msg, cloud_event, data: jma_bosai_volcano_mqtt_producer_data.Volcano, topic_params: dict):
        """Handler for JP.JMA.Volcano.mqtt.Volcano messages."""
        received_data.append(data)
        assert cloud_event['type'] == "JP.JMA.Volcano.Volcano"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.jp_jma_volcano_mqtt_volcano_async = on_jp_jma_volcano_mqtt_volcano
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/jp_jma_volcano_mqtt/jp_jma_volcano_mqtt_volcano"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_jp_jma_volcano_mqtt_volcano(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            volcano_code=f"test_volcano_code_{i}",
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
async def test_jp_jma_volcano_mqtt_jp_jma_volcano_mqtt_volcanic_warning_py(mosquitto_broker):
    """Test publishing and receiving JP.JMA.Volcano.mqtt.VolcanicWarning message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VolcanicWarning.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = JPJMAVolcanoMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = JPJMAVolcanoMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_jp_jma_volcano_mqtt_volcanic_warning(mqtt_msg, cloud_event, data: jma_bosai_volcano_mqtt_producer_data.VolcanicWarning, topic_params: dict):
        """Handler for JP.JMA.Volcano.mqtt.VolcanicWarning messages."""
        received_data.append(data)
        assert cloud_event['type'] == "JP.JMA.Volcano.VolcanicWarning"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.jp_jma_volcano_mqtt_volcanic_warning_async = on_jp_jma_volcano_mqtt_volcanic_warning
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/jp_jma_volcano_mqtt/jp_jma_volcano_mqtt_volcanic_warning"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_jp_jma_volcano_mqtt_volcanic_warning(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            volcano_code=f"test_volcano_code_{i}",
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
async def test_jp_jma_volcano_mqtt_jp_jma_volcano_mqtt_volcanic_eruption_py(mosquitto_broker):
    """Test publishing and receiving JP.JMA.Volcano.mqtt.VolcanicEruption message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VolcanicEruption.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = JPJMAVolcanoMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = JPJMAVolcanoMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_jp_jma_volcano_mqtt_volcanic_eruption(mqtt_msg, cloud_event, data: jma_bosai_volcano_mqtt_producer_data.VolcanicEruption, topic_params: dict):
        """Handler for JP.JMA.Volcano.mqtt.VolcanicEruption messages."""
        received_data.append(data)
        assert cloud_event['type'] == "JP.JMA.Volcano.VolcanicEruption"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.jp_jma_volcano_mqtt_volcanic_eruption_async = on_jp_jma_volcano_mqtt_volcanic_eruption
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/jp_jma_volcano_mqtt/jp_jma_volcano_mqtt_volcanic_eruption"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_jp_jma_volcano_mqtt_volcanic_eruption(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            volcano_code=f"test_volcano_code_{i}",
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


