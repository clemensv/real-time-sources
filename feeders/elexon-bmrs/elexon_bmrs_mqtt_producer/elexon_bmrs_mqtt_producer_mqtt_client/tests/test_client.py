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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../elexon_bmrs_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../elexon_bmrs_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../elexon_bmrs_mqtt_producer_mqtt_client/src')))

import elexon_bmrs_mqtt_producer_data
from elexon_bmrs_mqtt_producer_data import GenerationMix
from test_generationmix import Test_GenerationMix
from elexon_bmrs_mqtt_producer_data import DemandOutturn
from test_demandoutturn import Test_DemandOutturn
from elexon_bmrs_mqtt_producer_data import Info
from test_info import Test_Info
from elexon_bmrs_mqtt_producer_mqtt_client import UKCoElexonBMRSMqttMqttClient

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
async def test_uk_co_elexon_bmrs_mqtt_uk_co_elexon_bmrs_mqtt_generation_mix_py(mosquitto_broker):
    """Test publishing and receiving UK.Co.Elexon.BMRS.mqtt.GenerationMix message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GenerationMix.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UKCoElexonBMRSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UKCoElexonBMRSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_co_elexon_bmrs_mqtt_generation_mix(mqtt_msg, cloud_event, data: elexon_bmrs_mqtt_producer_data.GenerationMix, topic_params: dict):
        """Handler for UK.Co.Elexon.BMRS.mqtt.GenerationMix messages."""
        received_data.append(data)
        assert cloud_event['type'] == "UK.Co.Elexon.BMRS.GenerationMix"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_co_elexon_bmrs_mqtt_generation_mix_async = on_uk_co_elexon_bmrs_mqtt_generation_mix
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_co_elexon_bmrs_mqtt/uk_co_elexon_bmrs_mqtt_generation_mix"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_co_elexon_bmrs_mqtt_generation_mix(
            topic=test_topic,
            settlement_period=f"test_settlement_period_{i}",
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
async def test_uk_co_elexon_bmrs_mqtt_uk_co_elexon_bmrs_mqtt_demand_outturn_py(mosquitto_broker):
    """Test publishing and receiving UK.Co.Elexon.BMRS.mqtt.DemandOutturn message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DemandOutturn.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UKCoElexonBMRSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UKCoElexonBMRSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_co_elexon_bmrs_mqtt_demand_outturn(mqtt_msg, cloud_event, data: elexon_bmrs_mqtt_producer_data.DemandOutturn, topic_params: dict):
        """Handler for UK.Co.Elexon.BMRS.mqtt.DemandOutturn messages."""
        received_data.append(data)
        assert cloud_event['type'] == "UK.Co.Elexon.BMRS.DemandOutturn"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_co_elexon_bmrs_mqtt_demand_outturn_async = on_uk_co_elexon_bmrs_mqtt_demand_outturn
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_co_elexon_bmrs_mqtt/uk_co_elexon_bmrs_mqtt_demand_outturn"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_co_elexon_bmrs_mqtt_demand_outturn(
            topic=test_topic,
            settlement_period=f"test_settlement_period_{i}",
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
async def test_uk_co_elexon_bmrs_mqtt_uk_co_elexon_bmrs_mqtt_info_py(mosquitto_broker):
    """Test publishing and receiving UK.Co.Elexon.BMRS.mqtt.Info message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Info.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UKCoElexonBMRSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UKCoElexonBMRSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_uk_co_elexon_bmrs_mqtt_info(mqtt_msg, cloud_event, data: elexon_bmrs_mqtt_producer_data.Info, topic_params: dict):
        """Handler for UK.Co.Elexon.BMRS.mqtt.Info messages."""
        received_data.append(data)
        assert cloud_event['type'] == "UK.Co.Elexon.BMRS.Info"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.uk_co_elexon_bmrs_mqtt_info_async = on_uk_co_elexon_bmrs_mqtt_info
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/uk_co_elexon_bmrs_mqtt/uk_co_elexon_bmrs_mqtt_info"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_uk_co_elexon_bmrs_mqtt_info(
            topic=test_topic,
            settlement_period=f"test_settlement_period_{i}",
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


