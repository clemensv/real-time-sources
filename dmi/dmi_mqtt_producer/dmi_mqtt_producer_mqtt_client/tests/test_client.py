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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dmi_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dmi_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dmi_mqtt_producer_mqtt_client/src')))

import dmi_mqtt_producer_data
from dmi_mqtt_producer_data import MetObsStation
from test_dmi_mqtt_producer_data_metobsstation import Test_MetObsStation
from dmi_mqtt_producer_data import MetObsObservation
from test_dmi_mqtt_producer_data_metobsobservation import Test_MetObsObservation
from dmi_mqtt_producer_data import OceanStation
from test_dmi_mqtt_producer_data_oceanstation import Test_OceanStation
from dmi_mqtt_producer_data import TidewaterStation
from test_dmi_mqtt_producer_data_tidewaterstation import Test_TidewaterStation
from dmi_mqtt_producer_data import OceanObservation
from test_dmi_mqtt_producer_data_oceanobservation import Test_OceanObservation
from dmi_mqtt_producer_data import TidewaterPrediction
from test_dmi_mqtt_producer_data_tidewaterprediction import Test_TidewaterPrediction
from dmi_mqtt_producer_mqtt_client import DkDmiMetObsMqttMqttClient
from dmi_mqtt_producer_mqtt_client import DkDmiOceanObsMqttMqttClient

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
async def test_dk_dmi_metobs_mqtt_dk_dmi_met_obs_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving dk.dmi.metObs.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MetObsStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DkDmiMetObsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DkDmiMetObsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_dk_dmi_met_obs_mqtt_station(mqtt_msg, cloud_event, data: dmi_mqtt_producer_data.MetObsStation, topic_params: dict):
        """Handler for dk.dmi.metObs.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "dk.dmi.metObs.MetObsStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.dk_dmi_met_obs_mqtt_station_async = on_dk_dmi_met_obs_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/dk_dmi_metobs_mqtt/dk_dmi_met_obs_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_dk_dmi_met_obs_mqtt_station(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
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
async def test_dk_dmi_metobs_mqtt_dk_dmi_met_obs_mqtt_observation_py(mosquitto_broker):
    """Test publishing and receiving dk.dmi.metObs.mqtt.Observation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MetObsObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DkDmiMetObsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DkDmiMetObsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_dk_dmi_met_obs_mqtt_observation(mqtt_msg, cloud_event, data: dmi_mqtt_producer_data.MetObsObservation, topic_params: dict):
        """Handler for dk.dmi.metObs.mqtt.Observation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "dk.dmi.metObs.MetObsObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.dk_dmi_met_obs_mqtt_observation_async = on_dk_dmi_met_obs_mqtt_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/dk_dmi_metobs_mqtt/dk_dmi_met_obs_mqtt_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_dk_dmi_met_obs_mqtt_observation(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
            parameter_id=f"test_parameter_id_{i}",
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
async def test_dk_dmi_oceanobs_mqtt_dk_dmi_ocean_obs_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving dk.dmi.oceanObs.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_OceanStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DkDmiOceanObsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DkDmiOceanObsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_dk_dmi_ocean_obs_mqtt_station(mqtt_msg, cloud_event, data: dmi_mqtt_producer_data.OceanStation, topic_params: dict):
        """Handler for dk.dmi.oceanObs.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "dk.dmi.oceanObs.OceanStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.dk_dmi_ocean_obs_mqtt_station_async = on_dk_dmi_ocean_obs_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/dk_dmi_oceanobs_mqtt/dk_dmi_ocean_obs_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_dk_dmi_ocean_obs_mqtt_station(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
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
async def test_dk_dmi_oceanobs_mqtt_dk_dmi_ocean_obs_mqtt_tidewater_station_py(mosquitto_broker):
    """Test publishing and receiving dk.dmi.oceanObs.mqtt.TidewaterStation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TidewaterStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DkDmiOceanObsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DkDmiOceanObsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_dk_dmi_ocean_obs_mqtt_tidewater_station(mqtt_msg, cloud_event, data: dmi_mqtt_producer_data.TidewaterStation, topic_params: dict):
        """Handler for dk.dmi.oceanObs.mqtt.TidewaterStation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "dk.dmi.oceanObs.TidewaterStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.dk_dmi_ocean_obs_mqtt_tidewater_station_async = on_dk_dmi_ocean_obs_mqtt_tidewater_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/dk_dmi_oceanobs_mqtt/dk_dmi_ocean_obs_mqtt_tidewater_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_dk_dmi_ocean_obs_mqtt_tidewater_station(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
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
async def test_dk_dmi_oceanobs_mqtt_dk_dmi_ocean_obs_mqtt_observation_py(mosquitto_broker):
    """Test publishing and receiving dk.dmi.oceanObs.mqtt.Observation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_OceanObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DkDmiOceanObsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DkDmiOceanObsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_dk_dmi_ocean_obs_mqtt_observation(mqtt_msg, cloud_event, data: dmi_mqtt_producer_data.OceanObservation, topic_params: dict):
        """Handler for dk.dmi.oceanObs.mqtt.Observation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "dk.dmi.oceanObs.OceanObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.dk_dmi_ocean_obs_mqtt_observation_async = on_dk_dmi_ocean_obs_mqtt_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/dk_dmi_oceanobs_mqtt/dk_dmi_ocean_obs_mqtt_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_dk_dmi_ocean_obs_mqtt_observation(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
            parameter_id=f"test_parameter_id_{i}",
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
async def test_dk_dmi_oceanobs_mqtt_dk_dmi_ocean_obs_mqtt_tidewater_prediction_py(mosquitto_broker):
    """Test publishing and receiving dk.dmi.oceanObs.mqtt.TidewaterPrediction message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TidewaterPrediction.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DkDmiOceanObsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DkDmiOceanObsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_dk_dmi_ocean_obs_mqtt_tidewater_prediction(mqtt_msg, cloud_event, data: dmi_mqtt_producer_data.TidewaterPrediction, topic_params: dict):
        """Handler for dk.dmi.oceanObs.mqtt.TidewaterPrediction messages."""
        received_data.append(data)
        assert cloud_event['type'] == "dk.dmi.oceanObs.TidewaterPrediction"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.dk_dmi_ocean_obs_mqtt_tidewater_prediction_async = on_dk_dmi_ocean_obs_mqtt_tidewater_prediction
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/dk_dmi_oceanobs_mqtt/dk_dmi_ocean_obs_mqtt_tidewater_prediction"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_dk_dmi_ocean_obs_mqtt_tidewater_prediction(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
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


