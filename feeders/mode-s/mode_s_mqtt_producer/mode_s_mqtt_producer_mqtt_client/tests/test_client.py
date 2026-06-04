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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mode_s_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mode_s_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mode_s_mqtt_producer_mqtt_client/src')))

import mode_s_mqtt_producer_data
from mode_s_mqtt_producer_data import Record
from test_mode_s_mqtt_producer_data_record import Test_Record
from mode_s_mqtt_producer_mqtt_client import ModeSMqttMqttClient

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
async def test_mode_s_mqtt_mode_s_adsb_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Mode_S.ADSB.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Record.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = ModeSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = ModeSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_mode_s_adsb_mqtt(mqtt_msg, cloud_event, data: mode_s_mqtt_producer_data.Record, topic_params: dict):
        """Handler for Mode_S.ADSB.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Mode_S.ADSB"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.mode_s_adsb_mqtt_async = on_mode_s_adsb_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/mode_s_mqtt/mode_s_adsb_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_mode_s_adsb_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            icao24=f"test_icao24_{i}",
            receiver_id=f"test_receiver_id_{i}",
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
async def test_mode_s_mqtt_mode_s_altitude_reply_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Mode_S.AltitudeReply.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Record.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = ModeSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = ModeSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_mode_s_altitude_reply_mqtt(mqtt_msg, cloud_event, data: mode_s_mqtt_producer_data.Record, topic_params: dict):
        """Handler for Mode_S.AltitudeReply.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Mode_S.AltitudeReply"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.mode_s_altitude_reply_mqtt_async = on_mode_s_altitude_reply_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/mode_s_mqtt/mode_s_altitude_reply_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_mode_s_altitude_reply_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            icao24=f"test_icao24_{i}",
            receiver_id=f"test_receiver_id_{i}",
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
async def test_mode_s_mqtt_mode_s_identity_reply_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Mode_S.IdentityReply.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Record.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = ModeSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = ModeSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_mode_s_identity_reply_mqtt(mqtt_msg, cloud_event, data: mode_s_mqtt_producer_data.Record, topic_params: dict):
        """Handler for Mode_S.IdentityReply.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Mode_S.IdentityReply"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.mode_s_identity_reply_mqtt_async = on_mode_s_identity_reply_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/mode_s_mqtt/mode_s_identity_reply_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_mode_s_identity_reply_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            icao24=f"test_icao24_{i}",
            receiver_id=f"test_receiver_id_{i}",
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
async def test_mode_s_mqtt_mode_s_acquisition_reply_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Mode_S.AcquisitionReply.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Record.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = ModeSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = ModeSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_mode_s_acquisition_reply_mqtt(mqtt_msg, cloud_event, data: mode_s_mqtt_producer_data.Record, topic_params: dict):
        """Handler for Mode_S.AcquisitionReply.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Mode_S.AcquisitionReply"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.mode_s_acquisition_reply_mqtt_async = on_mode_s_acquisition_reply_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/mode_s_mqtt/mode_s_acquisition_reply_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_mode_s_acquisition_reply_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            icao24=f"test_icao24_{i}",
            receiver_id=f"test_receiver_id_{i}",
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
async def test_mode_s_mqtt_mode_s_comm_baltitude_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Mode_S.CommBAltitude.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Record.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = ModeSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = ModeSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_mode_s_comm_baltitude_mqtt(mqtt_msg, cloud_event, data: mode_s_mqtt_producer_data.Record, topic_params: dict):
        """Handler for Mode_S.CommBAltitude.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Mode_S.CommBAltitude"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.mode_s_comm_baltitude_mqtt_async = on_mode_s_comm_baltitude_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/mode_s_mqtt/mode_s_comm_baltitude_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_mode_s_comm_baltitude_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            icao24=f"test_icao24_{i}",
            receiver_id=f"test_receiver_id_{i}",
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
async def test_mode_s_mqtt_mode_s_comm_bidentity_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Mode_S.CommBIdentity.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Record.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = ModeSMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = ModeSMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_mode_s_comm_bidentity_mqtt(mqtt_msg, cloud_event, data: mode_s_mqtt_producer_data.Record, topic_params: dict):
        """Handler for Mode_S.CommBIdentity.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Mode_S.CommBIdentity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.mode_s_comm_bidentity_mqtt_async = on_mode_s_comm_bidentity_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/mode_s_mqtt/mode_s_comm_bidentity_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_mode_s_comm_bidentity_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            icao24=f"test_icao24_{i}",
            receiver_id=f"test_receiver_id_{i}",
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


