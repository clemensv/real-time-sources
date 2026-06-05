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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../digitraffic_maritime_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../digitraffic_maritime_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../digitraffic_maritime_mqtt_producer_mqtt_client/src')))

import digitraffic_maritime_mqtt_producer_data
from digitraffic_maritime_mqtt_producer_data import VesselLocation
from test_vessellocation import Test_VesselLocation
from digitraffic_maritime_mqtt_producer_data import VesselMetadata
from test_vesselmetadata import Test_VesselMetadata
from digitraffic_maritime_mqtt_producer_data import PortCall
from test_portcall import Test_PortCall
from digitraffic_maritime_mqtt_producer_data import VesselDetails
from test_vesseldetails import Test_VesselDetails
from digitraffic_maritime_mqtt_producer_data import PortLocation
from test_portlocation import Test_PortLocation
from digitraffic_maritime_mqtt_producer_mqtt_client import FiDigitrafficMarineAisMqttMqttClient
from digitraffic_maritime_mqtt_producer_mqtt_client import FiDigitrafficMarinePortcallMqttMqttClient
from digitraffic_maritime_mqtt_producer_mqtt_client import FiDigitrafficMarinePortcallVesseldetailsMqttMqttClient
from digitraffic_maritime_mqtt_producer_mqtt_client import FiDigitrafficMarinePortcallPortlocationMqttMqttClient

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
async def test_fi_digitraffic_marine_ais_mqtt_fi_digitraffic_marine_ais_mqtt_location_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.marine.ais.mqtt.location message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VesselLocation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficMarineAisMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficMarineAisMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_marine_ais_mqtt_location(mqtt_msg, cloud_event, data: digitraffic_maritime_mqtt_producer_data.VesselLocation, topic_params: dict):
        """Handler for fi.digitraffic.marine.ais.mqtt.location messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.marine.ais.VesselLocation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_marine_ais_mqtt_location_async = on_fi_digitraffic_marine_ais_mqtt_location
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_marine_ais_mqtt/fi_digitraffic_marine_ais_mqtt_location"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_marine_ais_mqtt_location(
            topic=test_topic,
            mmsi=f"test_mmsi_{i}",
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
async def test_fi_digitraffic_marine_ais_mqtt_fi_digitraffic_marine_ais_mqtt_metadata_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.marine.ais.mqtt.metadata message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VesselMetadata.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficMarineAisMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficMarineAisMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_marine_ais_mqtt_metadata(mqtt_msg, cloud_event, data: digitraffic_maritime_mqtt_producer_data.VesselMetadata, topic_params: dict):
        """Handler for fi.digitraffic.marine.ais.mqtt.metadata messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.marine.ais.VesselMetadata"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_marine_ais_mqtt_metadata_async = on_fi_digitraffic_marine_ais_mqtt_metadata
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_marine_ais_mqtt/fi_digitraffic_marine_ais_mqtt_metadata"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_marine_ais_mqtt_metadata(
            topic=test_topic,
            mmsi=f"test_mmsi_{i}",
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
async def test_fi_digitraffic_marine_portcall_mqtt_fi_digitraffic_marine_portcall_mqtt_port_call_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.marine.portcall.mqtt.port_call message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PortCall.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficMarinePortcallMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficMarinePortcallMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_marine_portcall_mqtt_port_call(mqtt_msg, cloud_event, data: digitraffic_maritime_mqtt_producer_data.PortCall, topic_params: dict):
        """Handler for fi.digitraffic.marine.portcall.mqtt.port_call messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.marine.portcall.PortCall"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_marine_portcall_mqtt_port_call_async = on_fi_digitraffic_marine_portcall_mqtt_port_call
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_marine_portcall_mqtt/fi_digitraffic_marine_portcall_mqtt_port_call"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_marine_portcall_mqtt_port_call(
            topic=test_topic,
            port_call_id=f"test_port_call_id_{i}",
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
async def test_fi_digitraffic_marine_portcall_vesseldetails_mqtt_fi_digitraffic_marine_portcall_vesseldetails_mqtt_vessel_details_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.marine.portcall.vesseldetails.mqtt.vessel_details message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VesselDetails.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficMarinePortcallVesseldetailsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficMarinePortcallVesseldetailsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_marine_portcall_vesseldetails_mqtt_vessel_details(mqtt_msg, cloud_event, data: digitraffic_maritime_mqtt_producer_data.VesselDetails, topic_params: dict):
        """Handler for fi.digitraffic.marine.portcall.vesseldetails.mqtt.vessel_details messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.marine.portcall.VesselDetails"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_marine_portcall_vesseldetails_mqtt_vessel_details_async = on_fi_digitraffic_marine_portcall_vesseldetails_mqtt_vessel_details
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_marine_portcall_vesseldetails_mqtt/fi_digitraffic_marine_portcall_vesseldetails_mqtt_vessel_details"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_marine_portcall_vesseldetails_mqtt_vessel_details(
            topic=test_topic,
            vessel_id=f"test_vessel_id_{i}",
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
async def test_fi_digitraffic_marine_portcall_portlocation_mqtt_fi_digitraffic_marine_portcall_portlocation_mqtt_port_location_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.marine.portcall.portlocation.mqtt.port_location message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PortLocation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficMarinePortcallPortlocationMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficMarinePortcallPortlocationMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_marine_portcall_portlocation_mqtt_port_location(mqtt_msg, cloud_event, data: digitraffic_maritime_mqtt_producer_data.PortLocation, topic_params: dict):
        """Handler for fi.digitraffic.marine.portcall.portlocation.mqtt.port_location messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.marine.portcall.PortLocation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_marine_portcall_portlocation_mqtt_port_location_async = on_fi_digitraffic_marine_portcall_portlocation_mqtt_port_location
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_marine_portcall_portlocation_mqtt/fi_digitraffic_marine_portcall_portlocation_mqtt_port_location"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_marine_portcall_portlocation_mqtt_port_location(
            topic=test_topic,
            locode=f"test_locode_{i}",
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


