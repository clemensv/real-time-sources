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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ndw_road_traffic_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ndw_road_traffic_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ndw_road_traffic_mqtt_producer_mqtt_client/src')))

import ndw_road_traffic_mqtt_producer_data
from ndw_road_traffic_mqtt_producer_data import PointMeasurementSite
from test_pointmeasurementsite import Test_PointMeasurementSite
from ndw_road_traffic_mqtt_producer_data import RouteMeasurementSite
from test_routemeasurementsite import Test_RouteMeasurementSite
from ndw_road_traffic_mqtt_producer_data import TrafficObservation
from test_trafficobservation import Test_TrafficObservation
from ndw_road_traffic_mqtt_producer_data import TravelTimeObservation
from test_traveltimeobservation import Test_TravelTimeObservation
from ndw_road_traffic_mqtt_producer_data import DripSign
from test_dripsign import Test_DripSign
from ndw_road_traffic_mqtt_producer_data import DripDisplayState
from test_dripdisplaystate import Test_DripDisplayState
from ndw_road_traffic_mqtt_producer_data import MsiSign
from test_msisign import Test_MsiSign
from ndw_road_traffic_mqtt_producer_data import MsiDisplayState
from test_msidisplaystate import Test_MsiDisplayState
from ndw_road_traffic_mqtt_producer_data import Roadwork
from test_roadwork import Test_Roadwork
from ndw_road_traffic_mqtt_producer_data import BridgeOpening
from test_bridgeopening import Test_BridgeOpening
from ndw_road_traffic_mqtt_producer_data import TemporaryClosure
from test_temporaryclosure import Test_TemporaryClosure
from ndw_road_traffic_mqtt_producer_data import TemporarySpeedLimit
from test_temporaryspeedlimit import Test_TemporarySpeedLimit
from ndw_road_traffic_mqtt_producer_data import SafetyRelatedMessage
from test_safetyrelatedmessage import Test_SafetyRelatedMessage
from ndw_road_traffic_mqtt_producer_mqtt_client import NLNDWAVGMqttMqttClient
from ndw_road_traffic_mqtt_producer_mqtt_client import NLNDWDRIPMqttMqttClient
from ndw_road_traffic_mqtt_producer_mqtt_client import NLNDWMSIMqttMqttClient
from ndw_road_traffic_mqtt_producer_mqtt_client import NLNDWSituationsMqttMqttClient

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
async def test_nl_ndw_avg_mqtt_nl_ndw_avg_point_measurement_site_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.AVG.PointMeasurementSite.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PointMeasurementSite.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWAVGMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWAVGMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_avg_point_measurement_site_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.PointMeasurementSite, topic_params: dict):
        """Handler for NL.NDW.AVG.PointMeasurementSite.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.AVG.PointMeasurementSite"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_avg_point_measurement_site_mqtt_async = on_nl_ndw_avg_point_measurement_site_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_avg_mqtt/nl_ndw_avg_point_measurement_site_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_avg_point_measurement_site_mqtt(
            topic=test_topic,
            measurement_site_id=f"test_measurement_site_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_avg_mqtt_nl_ndw_avg_route_measurement_site_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.AVG.RouteMeasurementSite.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RouteMeasurementSite.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWAVGMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWAVGMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_avg_route_measurement_site_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.RouteMeasurementSite, topic_params: dict):
        """Handler for NL.NDW.AVG.RouteMeasurementSite.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.AVG.RouteMeasurementSite"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_avg_route_measurement_site_mqtt_async = on_nl_ndw_avg_route_measurement_site_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_avg_mqtt/nl_ndw_avg_route_measurement_site_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_avg_route_measurement_site_mqtt(
            topic=test_topic,
            measurement_site_id=f"test_measurement_site_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_avg_mqtt_nl_ndw_avg_traffic_observation_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.AVG.TrafficObservation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWAVGMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWAVGMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_avg_traffic_observation_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.TrafficObservation, topic_params: dict):
        """Handler for NL.NDW.AVG.TrafficObservation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.AVG.TrafficObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_avg_traffic_observation_mqtt_async = on_nl_ndw_avg_traffic_observation_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_avg_mqtt/nl_ndw_avg_traffic_observation_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_avg_traffic_observation_mqtt(
            topic=test_topic,
            measurement_site_id=f"test_measurement_site_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_avg_mqtt_nl_ndw_avg_travel_time_observation_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.AVG.TravelTimeObservation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TravelTimeObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWAVGMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWAVGMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_avg_travel_time_observation_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.TravelTimeObservation, topic_params: dict):
        """Handler for NL.NDW.AVG.TravelTimeObservation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.AVG.TravelTimeObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_avg_travel_time_observation_mqtt_async = on_nl_ndw_avg_travel_time_observation_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_avg_mqtt/nl_ndw_avg_travel_time_observation_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_avg_travel_time_observation_mqtt(
            topic=test_topic,
            measurement_site_id=f"test_measurement_site_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_drip_mqtt_nl_ndw_drip_drip_sign_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.DRIP.DripSign.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DripSign.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWDRIPMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWDRIPMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_drip_drip_sign_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.DripSign, topic_params: dict):
        """Handler for NL.NDW.DRIP.DripSign.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.DRIP.DripSign"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_drip_drip_sign_mqtt_async = on_nl_ndw_drip_drip_sign_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_drip_mqtt/nl_ndw_drip_drip_sign_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_drip_drip_sign_mqtt(
            topic=test_topic,
            vms_controller_id=f"test_vms_controller_id_{i}",
            vms_index=f"test_vms_index_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_drip_mqtt_nl_ndw_drip_drip_display_state_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.DRIP.DripDisplayState.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DripDisplayState.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWDRIPMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWDRIPMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_drip_drip_display_state_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.DripDisplayState, topic_params: dict):
        """Handler for NL.NDW.DRIP.DripDisplayState.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.DRIP.DripDisplayState"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_drip_drip_display_state_mqtt_async = on_nl_ndw_drip_drip_display_state_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_drip_mqtt/nl_ndw_drip_drip_display_state_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_drip_drip_display_state_mqtt(
            topic=test_topic,
            vms_controller_id=f"test_vms_controller_id_{i}",
            vms_index=f"test_vms_index_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_msi_mqtt_nl_ndw_msi_msi_sign_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.MSI.MsiSign.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MsiSign.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWMSIMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWMSIMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_msi_msi_sign_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.MsiSign, topic_params: dict):
        """Handler for NL.NDW.MSI.MsiSign.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.MSI.MsiSign"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_msi_msi_sign_mqtt_async = on_nl_ndw_msi_msi_sign_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_msi_mqtt/nl_ndw_msi_msi_sign_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_msi_msi_sign_mqtt(
            topic=test_topic,
            sign_id=f"test_sign_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_msi_mqtt_nl_ndw_msi_msi_display_state_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.MSI.MsiDisplayState.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MsiDisplayState.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWMSIMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWMSIMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_msi_msi_display_state_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.MsiDisplayState, topic_params: dict):
        """Handler for NL.NDW.MSI.MsiDisplayState.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.MSI.MsiDisplayState"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_msi_msi_display_state_mqtt_async = on_nl_ndw_msi_msi_display_state_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_msi_mqtt/nl_ndw_msi_msi_display_state_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_msi_msi_display_state_mqtt(
            topic=test_topic,
            sign_id=f"test_sign_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_situations_mqtt_nl_ndw_situations_roadwork_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Situations.Roadwork.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Roadwork.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWSituationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWSituationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_situations_roadwork_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.Roadwork, topic_params: dict):
        """Handler for NL.NDW.Situations.Roadwork.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Situations.Roadwork"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_situations_roadwork_mqtt_async = on_nl_ndw_situations_roadwork_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_situations_mqtt/nl_ndw_situations_roadwork_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_situations_roadwork_mqtt(
            topic=test_topic,
            situation_record_id=f"test_situation_record_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_situations_mqtt_nl_ndw_situations_bridge_opening_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Situations.BridgeOpening.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BridgeOpening.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWSituationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWSituationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_situations_bridge_opening_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.BridgeOpening, topic_params: dict):
        """Handler for NL.NDW.Situations.BridgeOpening.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Situations.BridgeOpening"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_situations_bridge_opening_mqtt_async = on_nl_ndw_situations_bridge_opening_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_situations_mqtt/nl_ndw_situations_bridge_opening_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_situations_bridge_opening_mqtt(
            topic=test_topic,
            situation_record_id=f"test_situation_record_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_situations_mqtt_nl_ndw_situations_temporary_closure_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Situations.TemporaryClosure.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TemporaryClosure.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWSituationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWSituationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_situations_temporary_closure_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.TemporaryClosure, topic_params: dict):
        """Handler for NL.NDW.Situations.TemporaryClosure.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Situations.TemporaryClosure"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_situations_temporary_closure_mqtt_async = on_nl_ndw_situations_temporary_closure_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_situations_mqtt/nl_ndw_situations_temporary_closure_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_situations_temporary_closure_mqtt(
            topic=test_topic,
            situation_record_id=f"test_situation_record_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_situations_mqtt_nl_ndw_situations_temporary_speed_limit_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Situations.TemporarySpeedLimit.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TemporarySpeedLimit.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWSituationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWSituationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_situations_temporary_speed_limit_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.TemporarySpeedLimit, topic_params: dict):
        """Handler for NL.NDW.Situations.TemporarySpeedLimit.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Situations.TemporarySpeedLimit"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_situations_temporary_speed_limit_mqtt_async = on_nl_ndw_situations_temporary_speed_limit_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_situations_mqtt/nl_ndw_situations_temporary_speed_limit_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_situations_temporary_speed_limit_mqtt(
            topic=test_topic,
            situation_record_id=f"test_situation_record_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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
async def test_nl_ndw_situations_mqtt_nl_ndw_situations_safety_related_message_mqtt_py(mosquitto_broker):
    """Test publishing and receiving NL.NDW.Situations.SafetyRelatedMessage.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SafetyRelatedMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = NLNDWSituationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = NLNDWSituationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_nl_ndw_situations_safety_related_message_mqtt(mqtt_msg, cloud_event, data: ndw_road_traffic_mqtt_producer_data.SafetyRelatedMessage, topic_params: dict):
        """Handler for NL.NDW.Situations.SafetyRelatedMessage.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "NL.NDW.Situations.SafetyRelatedMessage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.nl_ndw_situations_safety_related_message_mqtt_async = on_nl_ndw_situations_safety_related_message_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/nl_ndw_situations_mqtt/nl_ndw_situations_safety_related_message_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_nl_ndw_situations_safety_related_message_mqtt(
            topic=test_topic,
            situation_record_id=f"test_situation_record_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            road="test_road",
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


