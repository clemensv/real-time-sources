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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hsl_hfp_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hsl_hfp_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hsl_hfp_mqtt_producer_mqtt_client/src')))

import hsl_hfp_mqtt_producer_data
from hsl_hfp_mqtt_producer_data import VehicleEvent
from test_vehicleevent import Test_VehicleEvent
from hsl_hfp_mqtt_producer_data import TrafficLightEvent
from test_trafficlightevent import Test_TrafficLightEvent
from hsl_hfp_mqtt_producer_data import DriverBlockEvent
from test_driverblockevent import Test_DriverBlockEvent
from hsl_hfp_mqtt_producer_data import Operator
from test_operator import Test_Operator
from hsl_hfp_mqtt_producer_data import Route
from test_route import Test_Route
from hsl_hfp_mqtt_producer_data import Stop
from test_stop import Test_Stop
from hsl_hfp_mqtt_producer_mqtt_client import FiHslHfpMqttMqttClient
from hsl_hfp_mqtt_producer_mqtt_client import FiHslGtfsOperatorMqttMqttClient
from hsl_hfp_mqtt_producer_mqtt_client import FiHslGtfsRouteMqttMqttClient
from hsl_hfp_mqtt_producer_mqtt_client import FiHslGtfsStopMqttMqttClient

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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_vp_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.vp message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_vp(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.vp messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.vp"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_vp_async = on_fi_hsl_hfp_mqtt_vp
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_vp"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_vp(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_due_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.due message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_due(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.due messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.due"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_due_async = on_fi_hsl_hfp_mqtt_due
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_due"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_due(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_arr_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.arr message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_arr(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.arr messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.arr"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_arr_async = on_fi_hsl_hfp_mqtt_arr
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_arr"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_arr(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_dep_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.dep message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_dep(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.dep messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.dep"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_dep_async = on_fi_hsl_hfp_mqtt_dep
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_dep"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_dep(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_ars_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.ars message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_ars(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.ars messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.ars"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_ars_async = on_fi_hsl_hfp_mqtt_ars
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_ars"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_ars(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_pde_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.pde message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_pde(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.pde messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.pde"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_pde_async = on_fi_hsl_hfp_mqtt_pde
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_pde"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_pde(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_pas_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.pas message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_pas(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.pas messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.pas"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_pas_async = on_fi_hsl_hfp_mqtt_pas
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_pas"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_pas(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_wait_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.wait message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_wait(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.wait messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.wait"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_wait_async = on_fi_hsl_hfp_mqtt_wait
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_wait"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_wait(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_doo_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.doo message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_doo(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.doo messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.doo"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_doo_async = on_fi_hsl_hfp_mqtt_doo
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_doo"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_doo(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_doc_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.doc message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_doc(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.doc messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.doc"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_doc_async = on_fi_hsl_hfp_mqtt_doc
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_doc"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_doc(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_vja_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.vja message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_vja(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.vja messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.vja"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_vja_async = on_fi_hsl_hfp_mqtt_vja
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_vja"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_vja(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_vjout_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.vjout message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehicleEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_vjout(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.VehicleEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.vjout messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.vjout"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_vjout_async = on_fi_hsl_hfp_mqtt_vjout
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_vjout"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_vjout(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_tlr_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.tlr message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficLightEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_tlr(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.TrafficLightEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.tlr messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.tlr"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_tlr_async = on_fi_hsl_hfp_mqtt_tlr
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_tlr"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_tlr(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_tla_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.tla message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficLightEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_tla(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.TrafficLightEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.tla messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.tla"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_tla_async = on_fi_hsl_hfp_mqtt_tla
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_tla"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_tla(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_da_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.da message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DriverBlockEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_da(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.DriverBlockEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.da messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.da"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_da_async = on_fi_hsl_hfp_mqtt_da
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_da"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_da(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_dout_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.dout message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DriverBlockEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_dout(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.DriverBlockEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.dout messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.dout"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_dout_async = on_fi_hsl_hfp_mqtt_dout
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_dout"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_dout(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_ba_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.ba message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DriverBlockEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_ba(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.DriverBlockEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.ba messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.ba"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_ba_async = on_fi_hsl_hfp_mqtt_ba
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_ba"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_ba(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_hfp_mqtt_fi_hsl_hfp_mqtt_bout_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.hfp.mqtt.bout message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DriverBlockEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslHfpMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslHfpMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_hfp_mqtt_bout(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.DriverBlockEvent, topic_params: dict):
        """Handler for fi.hsl.hfp.mqtt.bout messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.hfp.bout"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_hfp_mqtt_bout_async = on_fi_hsl_hfp_mqtt_bout
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_hfp_mqtt/fi_hsl_hfp_mqtt_bout"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_hfp_mqtt_bout(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
            vehicle_number=f"test_vehicle_number_{i}",
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
async def test_fi_hsl_gtfs_operator_mqtt_fi_hsl_gtfs_operator_mqtt_operator_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.gtfs.operator.mqtt.Operator message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Operator.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslGtfsOperatorMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslGtfsOperatorMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_gtfs_operator_mqtt_operator(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.Operator, topic_params: dict):
        """Handler for fi.hsl.gtfs.operator.mqtt.Operator messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.gtfs.Operator"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_gtfs_operator_mqtt_operator_async = on_fi_hsl_gtfs_operator_mqtt_operator
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_gtfs_operator_mqtt/fi_hsl_gtfs_operator_mqtt_operator"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_gtfs_operator_mqtt_operator(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            operator_id=f"test_operator_id_{i}",
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
async def test_fi_hsl_gtfs_route_mqtt_fi_hsl_gtfs_route_mqtt_route_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.gtfs.route.mqtt.Route message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Route.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslGtfsRouteMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslGtfsRouteMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_gtfs_route_mqtt_route(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.Route, topic_params: dict):
        """Handler for fi.hsl.gtfs.route.mqtt.Route messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.gtfs.Route"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_gtfs_route_mqtt_route_async = on_fi_hsl_gtfs_route_mqtt_route
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_gtfs_route_mqtt/fi_hsl_gtfs_route_mqtt_route"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_gtfs_route_mqtt_route(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            route_id=f"test_route_id_{i}",
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
async def test_fi_hsl_gtfs_stop_mqtt_fi_hsl_gtfs_stop_mqtt_stop_py(mosquitto_broker):
    """Test publishing and receiving fi.hsl.gtfs.stop.mqtt.Stop message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Stop.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiHslGtfsStopMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiHslGtfsStopMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_hsl_gtfs_stop_mqtt_stop(mqtt_msg, cloud_event, data: hsl_hfp_mqtt_producer_data.Stop, topic_params: dict):
        """Handler for fi.hsl.gtfs.stop.mqtt.Stop messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.hsl.gtfs.Stop"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_hsl_gtfs_stop_mqtt_stop_async = on_fi_hsl_gtfs_stop_mqtt_stop
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_hsl_gtfs_stop_mqtt/fi_hsl_gtfs_stop_mqtt_stop"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_hsl_gtfs_stop_mqtt_stop(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            stop_id=f"test_stop_id_{i}",
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


