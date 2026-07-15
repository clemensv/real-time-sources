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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../open_charge_map_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../open_charge_map_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../open_charge_map_mqtt_producer_mqtt_client/src')))

import open_charge_map_mqtt_producer_data
from open_charge_map_mqtt_producer_data import ChargingLocation
from test_charginglocation import Test_ChargingLocation
from open_charge_map_mqtt_producer_data import Operator
from test_operator import Test_Operator
from open_charge_map_mqtt_producer_data import ConnectionType
from test_connectiontype import Test_ConnectionType
from open_charge_map_mqtt_producer_data import CurrentType
from test_currenttype import Test_CurrentType
from open_charge_map_mqtt_producer_data import ChargerType
from test_chargertype import Test_ChargerType
from open_charge_map_mqtt_producer_data import Country
from test_country import Test_Country
from open_charge_map_mqtt_producer_data import DataProvider
from test_dataprovider import Test_DataProvider
from open_charge_map_mqtt_producer_data import StatusType
from test_statustype import Test_StatusType
from open_charge_map_mqtt_producer_data import UsageType
from test_usagetype import Test_UsageType
from open_charge_map_mqtt_producer_data import SubmissionStatusType
from test_submissionstatustype import Test_SubmissionStatusType
from open_charge_map_mqtt_producer_mqtt_client import IOOpenChargeMapLocationsMqttMqttClient
from open_charge_map_mqtt_producer_mqtt_client import IOOpenChargeMapReferenceMqttMqttClient

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
async def test_io_openchargemap_locations_mqtt_io_open_charge_map_mqtt_charging_location_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.ChargingLocation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargingLocation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapLocationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapLocationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_charging_location(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.ChargingLocation, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.ChargingLocation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.ChargingLocation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_charging_location_async = on_io_open_charge_map_mqtt_charging_location
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_locations_mqtt/io_open_charge_map_mqtt_charging_location"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_charging_location(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            poi_id=f"test_poi_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_operator_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.Operator message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Operator.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_operator(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.Operator, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.Operator messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.Operator"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_operator_async = on_io_open_charge_map_mqtt_operator
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_operator"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_operator(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_connection_type_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.ConnectionType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ConnectionType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_connection_type(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.ConnectionType, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.ConnectionType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.ConnectionType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_connection_type_async = on_io_open_charge_map_mqtt_connection_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_connection_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_connection_type(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_current_type_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.CurrentType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CurrentType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_current_type(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.CurrentType, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.CurrentType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.CurrentType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_current_type_async = on_io_open_charge_map_mqtt_current_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_current_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_current_type(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_charger_type_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.ChargerType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChargerType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_charger_type(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.ChargerType, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.ChargerType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.ChargerType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_charger_type_async = on_io_open_charge_map_mqtt_charger_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_charger_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_charger_type(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_country_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.Country message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Country.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_country(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.Country, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.Country messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.Country"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_country_async = on_io_open_charge_map_mqtt_country
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_country"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_country(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_data_provider_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.DataProvider message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DataProvider.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_data_provider(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.DataProvider, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.DataProvider messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.DataProvider"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_data_provider_async = on_io_open_charge_map_mqtt_data_provider
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_data_provider"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_data_provider(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_status_type_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.StatusType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StatusType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_status_type(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.StatusType, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.StatusType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.StatusType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_status_type_async = on_io_open_charge_map_mqtt_status_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_status_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_status_type(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_usage_type_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.UsageType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_UsageType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_usage_type(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.UsageType, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.UsageType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.UsageType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_usage_type_async = on_io_open_charge_map_mqtt_usage_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_usage_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_usage_type(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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
async def test_io_openchargemap_reference_mqtt_io_open_charge_map_mqtt_submission_status_type_py(mosquitto_broker):
    """Test publishing and receiving IO.OpenChargeMap.mqtt.SubmissionStatusType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SubmissionStatusType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOOpenChargeMapReferenceMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOOpenChargeMapReferenceMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_open_charge_map_mqtt_submission_status_type(mqtt_msg, cloud_event, data: open_charge_map_mqtt_producer_data.SubmissionStatusType, topic_params: dict):
        """Handler for IO.OpenChargeMap.mqtt.SubmissionStatusType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.OpenChargeMap.SubmissionStatusType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_open_charge_map_mqtt_submission_status_type_async = on_io_open_charge_map_mqtt_submission_status_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_openchargemap_reference_mqtt/io_open_charge_map_mqtt_submission_status_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_open_charge_map_mqtt_submission_status_type(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            reference_type=f"test_reference_type_{i}",
            reference_id=f"test_reference_id_{i}",
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


