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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../aisstream_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../aisstream_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../aisstream_mqtt_producer_mqtt_client/src')))

import aisstream_mqtt_producer_data
from aisstream_mqtt_producer_data import PositionReport
from test_positionreport import Test_PositionReport
from aisstream_mqtt_producer_data import ShipStaticData
from test_shipstaticdata import Test_ShipStaticData
from aisstream_mqtt_producer_data import StandardClassBPositionReport
from test_standardclassbpositionreport import Test_StandardClassBPositionReport
from aisstream_mqtt_producer_data import ExtendedClassBPositionReport
from test_extendedclassbpositionreport import Test_ExtendedClassBPositionReport
from aisstream_mqtt_producer_data import AidsToNavigationReport
from test_aidstonavigationreport import Test_AidsToNavigationReport
from aisstream_mqtt_producer_data import StaticDataReport
from test_staticdatareport import Test_StaticDataReport
from aisstream_mqtt_producer_data import BaseStationReport
from test_basestationreport import Test_BaseStationReport
from aisstream_mqtt_producer_data import SafetyBroadcastMessage
from test_safetybroadcastmessage import Test_SafetyBroadcastMessage
from aisstream_mqtt_producer_data import StandardSearchAndRescueAircraftReport
from test_standardsearchandrescueaircraftreport import Test_StandardSearchAndRescueAircraftReport
from aisstream_mqtt_producer_data import LongRangeAisBroadcastMessage
from test_longrangeaisbroadcastmessage import Test_LongRangeAisBroadcastMessage
from aisstream_mqtt_producer_data import AddressedSafetyMessage
from test_addressedsafetymessage import Test_AddressedSafetyMessage
from aisstream_mqtt_producer_data import AddressedBinaryMessage
from test_addressedbinarymessage import Test_AddressedBinaryMessage
from aisstream_mqtt_producer_data import AssignedModeCommand
from test_assignedmodecommand import Test_AssignedModeCommand
from aisstream_mqtt_producer_data import BinaryAcknowledge
from test_binaryacknowledge import Test_BinaryAcknowledge
from aisstream_mqtt_producer_data import BinaryBroadcastMessage
from test_binarybroadcastmessage import Test_BinaryBroadcastMessage
from aisstream_mqtt_producer_data import ChannelManagement
from test_channelmanagement import Test_ChannelManagement
from aisstream_mqtt_producer_data import CoordinatedUTCInquiry
from test_coordinatedutcinquiry import Test_CoordinatedUTCInquiry
from aisstream_mqtt_producer_data import DataLinkManagementMessage
from test_datalinkmanagementmessage import Test_DataLinkManagementMessage
from aisstream_mqtt_producer_data import GnssBroadcastBinaryMessage
from test_gnssbroadcastbinarymessage import Test_GnssBroadcastBinaryMessage
from aisstream_mqtt_producer_data import GroupAssignmentCommand
from test_groupassignmentcommand import Test_GroupAssignmentCommand
from aisstream_mqtt_producer_data import Interrogation
from test_interrogation import Test_Interrogation
from aisstream_mqtt_producer_data import MultiSlotBinaryMessage
from test_multislotbinarymessage import Test_MultiSlotBinaryMessage
from aisstream_mqtt_producer_data import SingleSlotBinaryMessage
from test_singleslotbinarymessage import Test_SingleSlotBinaryMessage
from aisstream_mqtt_producer_mqtt_client import IOAISstreamMqttMqttClient

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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_position_report_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.PositionReport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PositionReport.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_position_report(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.PositionReport, topic_params: dict):
        """Handler for IO.AISstream.mqtt.PositionReport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.PositionReport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_position_report_async = on_io_aisstream_mqtt_position_report
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_position_report"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_position_report(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_ship_static_data_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.ShipStaticData message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ShipStaticData.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_ship_static_data(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.ShipStaticData, topic_params: dict):
        """Handler for IO.AISstream.mqtt.ShipStaticData messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.ShipStaticData"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_ship_static_data_async = on_io_aisstream_mqtt_ship_static_data
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_ship_static_data"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_ship_static_data(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_standard_class_bposition_report_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.StandardClassBPositionReport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StandardClassBPositionReport.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_standard_class_bposition_report(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.StandardClassBPositionReport, topic_params: dict):
        """Handler for IO.AISstream.mqtt.StandardClassBPositionReport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.StandardClassBPositionReport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_standard_class_bposition_report_async = on_io_aisstream_mqtt_standard_class_bposition_report
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_standard_class_bposition_report"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_standard_class_bposition_report(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_extended_class_bposition_report_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.ExtendedClassBPositionReport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ExtendedClassBPositionReport.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_extended_class_bposition_report(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.ExtendedClassBPositionReport, topic_params: dict):
        """Handler for IO.AISstream.mqtt.ExtendedClassBPositionReport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.ExtendedClassBPositionReport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_extended_class_bposition_report_async = on_io_aisstream_mqtt_extended_class_bposition_report
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_extended_class_bposition_report"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_extended_class_bposition_report(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_aids_to_navigation_report_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.AidsToNavigationReport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AidsToNavigationReport.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_aids_to_navigation_report(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.AidsToNavigationReport, topic_params: dict):
        """Handler for IO.AISstream.mqtt.AidsToNavigationReport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.AidsToNavigationReport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_aids_to_navigation_report_async = on_io_aisstream_mqtt_aids_to_navigation_report
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_aids_to_navigation_report"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_aids_to_navigation_report(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_static_data_report_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.StaticDataReport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StaticDataReport.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_static_data_report(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.StaticDataReport, topic_params: dict):
        """Handler for IO.AISstream.mqtt.StaticDataReport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.StaticDataReport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_static_data_report_async = on_io_aisstream_mqtt_static_data_report
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_static_data_report"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_static_data_report(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_base_station_report_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.BaseStationReport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BaseStationReport.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_base_station_report(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.BaseStationReport, topic_params: dict):
        """Handler for IO.AISstream.mqtt.BaseStationReport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.BaseStationReport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_base_station_report_async = on_io_aisstream_mqtt_base_station_report
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_base_station_report"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_base_station_report(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_safety_broadcast_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.SafetyBroadcastMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SafetyBroadcastMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_safety_broadcast_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.SafetyBroadcastMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.SafetyBroadcastMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.SafetyBroadcastMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_safety_broadcast_message_async = on_io_aisstream_mqtt_safety_broadcast_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_safety_broadcast_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_safety_broadcast_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_standard_search_and_rescue_aircraft_report_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StandardSearchAndRescueAircraftReport.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_standard_search_and_rescue_aircraft_report(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.StandardSearchAndRescueAircraftReport, topic_params: dict):
        """Handler for IO.AISstream.mqtt.StandardSearchAndRescueAircraftReport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.StandardSearchAndRescueAircraftReport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_standard_search_and_rescue_aircraft_report_async = on_io_aisstream_mqtt_standard_search_and_rescue_aircraft_report
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_standard_search_and_rescue_aircraft_report"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_standard_search_and_rescue_aircraft_report(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_long_range_ais_broadcast_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.LongRangeAisBroadcastMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LongRangeAisBroadcastMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_long_range_ais_broadcast_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.LongRangeAisBroadcastMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.LongRangeAisBroadcastMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.LongRangeAisBroadcastMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_long_range_ais_broadcast_message_async = on_io_aisstream_mqtt_long_range_ais_broadcast_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_long_range_ais_broadcast_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_long_range_ais_broadcast_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_addressed_safety_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.AddressedSafetyMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AddressedSafetyMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_addressed_safety_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.AddressedSafetyMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.AddressedSafetyMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.AddressedSafetyMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_addressed_safety_message_async = on_io_aisstream_mqtt_addressed_safety_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_addressed_safety_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_addressed_safety_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_addressed_binary_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.AddressedBinaryMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AddressedBinaryMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_addressed_binary_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.AddressedBinaryMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.AddressedBinaryMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.AddressedBinaryMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_addressed_binary_message_async = on_io_aisstream_mqtt_addressed_binary_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_addressed_binary_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_addressed_binary_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_assigned_mode_command_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.AssignedModeCommand message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AssignedModeCommand.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_assigned_mode_command(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.AssignedModeCommand, topic_params: dict):
        """Handler for IO.AISstream.mqtt.AssignedModeCommand messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.AssignedModeCommand"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_assigned_mode_command_async = on_io_aisstream_mqtt_assigned_mode_command
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_assigned_mode_command"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_assigned_mode_command(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_binary_acknowledge_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.BinaryAcknowledge message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BinaryAcknowledge.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_binary_acknowledge(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.BinaryAcknowledge, topic_params: dict):
        """Handler for IO.AISstream.mqtt.BinaryAcknowledge messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.BinaryAcknowledge"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_binary_acknowledge_async = on_io_aisstream_mqtt_binary_acknowledge
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_binary_acknowledge"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_binary_acknowledge(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_binary_broadcast_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.BinaryBroadcastMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BinaryBroadcastMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_binary_broadcast_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.BinaryBroadcastMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.BinaryBroadcastMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.BinaryBroadcastMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_binary_broadcast_message_async = on_io_aisstream_mqtt_binary_broadcast_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_binary_broadcast_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_binary_broadcast_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_channel_management_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.ChannelManagement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ChannelManagement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_channel_management(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.ChannelManagement, topic_params: dict):
        """Handler for IO.AISstream.mqtt.ChannelManagement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.ChannelManagement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_channel_management_async = on_io_aisstream_mqtt_channel_management
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_channel_management"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_channel_management(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_coordinated_utcinquiry_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.CoordinatedUTCInquiry message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CoordinatedUTCInquiry.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_coordinated_utcinquiry(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.CoordinatedUTCInquiry, topic_params: dict):
        """Handler for IO.AISstream.mqtt.CoordinatedUTCInquiry messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.CoordinatedUTCInquiry"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_coordinated_utcinquiry_async = on_io_aisstream_mqtt_coordinated_utcinquiry
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_coordinated_utcinquiry"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_coordinated_utcinquiry(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_data_link_management_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.DataLinkManagementMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DataLinkManagementMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_data_link_management_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.DataLinkManagementMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.DataLinkManagementMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.DataLinkManagementMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_data_link_management_message_async = on_io_aisstream_mqtt_data_link_management_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_data_link_management_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_data_link_management_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_gnss_broadcast_binary_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.GnssBroadcastBinaryMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GnssBroadcastBinaryMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_gnss_broadcast_binary_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.GnssBroadcastBinaryMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.GnssBroadcastBinaryMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.GnssBroadcastBinaryMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_gnss_broadcast_binary_message_async = on_io_aisstream_mqtt_gnss_broadcast_binary_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_gnss_broadcast_binary_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_gnss_broadcast_binary_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_group_assignment_command_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.GroupAssignmentCommand message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GroupAssignmentCommand.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_group_assignment_command(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.GroupAssignmentCommand, topic_params: dict):
        """Handler for IO.AISstream.mqtt.GroupAssignmentCommand messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.GroupAssignmentCommand"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_group_assignment_command_async = on_io_aisstream_mqtt_group_assignment_command
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_group_assignment_command"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_group_assignment_command(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_interrogation_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.Interrogation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Interrogation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_interrogation(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.Interrogation, topic_params: dict):
        """Handler for IO.AISstream.mqtt.Interrogation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.Interrogation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_interrogation_async = on_io_aisstream_mqtt_interrogation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_interrogation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_interrogation(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_multi_slot_binary_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.MultiSlotBinaryMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MultiSlotBinaryMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_multi_slot_binary_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.MultiSlotBinaryMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.MultiSlotBinaryMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.MultiSlotBinaryMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_multi_slot_binary_message_async = on_io_aisstream_mqtt_multi_slot_binary_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_multi_slot_binary_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_multi_slot_binary_message(
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
async def test_io_aisstream_mqtt_io_aisstream_mqtt_single_slot_binary_message_py(mosquitto_broker):
    """Test publishing and receiving IO.AISstream.mqtt.SingleSlotBinaryMessage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SingleSlotBinaryMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = IOAISstreamMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = IOAISstreamMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_io_aisstream_mqtt_single_slot_binary_message(mqtt_msg, cloud_event, data: aisstream_mqtt_producer_data.SingleSlotBinaryMessage, topic_params: dict):
        """Handler for IO.AISstream.mqtt.SingleSlotBinaryMessage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "IO.AISstream.SingleSlotBinaryMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.io_aisstream_mqtt_single_slot_binary_message_async = on_io_aisstream_mqtt_single_slot_binary_message
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/io_aisstream_mqtt/io_aisstream_mqtt_single_slot_binary_message"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_io_aisstream_mqtt_single_slot_binary_message(
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


