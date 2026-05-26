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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../digitraffic_road_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../digitraffic_road_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../digitraffic_road_mqtt_producer_mqtt_client/src')))

import digitraffic_road_mqtt_producer_data
from digitraffic_road_mqtt_producer_data import TmsSensorData
from test_digitraffic_road_mqtt_producer_data_tmssensordata import Test_TmsSensorData
from digitraffic_road_mqtt_producer_data import WeatherSensorData
from test_digitraffic_road_mqtt_producer_data_weathersensordata import Test_WeatherSensorData
from digitraffic_road_mqtt_producer_data import TrafficMessage
from test_digitraffic_road_mqtt_producer_data_trafficmessage import Test_TrafficMessage
from digitraffic_road_mqtt_producer_data import MaintenanceTracking
from test_digitraffic_road_mqtt_producer_data_maintenancetracking import Test_MaintenanceTracking
from digitraffic_road_mqtt_producer_data import TmsStation
from test_digitraffic_road_mqtt_producer_data_tmsstation import Test_TmsStation
from digitraffic_road_mqtt_producer_data import WeatherStation
from test_digitraffic_road_mqtt_producer_data_weatherstation import Test_WeatherStation
from digitraffic_road_mqtt_producer_data import MaintenanceTaskType
from test_digitraffic_road_mqtt_producer_data_maintenancetasktype import Test_MaintenanceTaskType
from digitraffic_road_mqtt_producer_mqtt_client import FiDigitrafficRoadMqttMqttClient

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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_tms_sensor_data_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.TmsSensorData message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TmsSensorData.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_tms_sensor_data(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.TmsSensorData, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.TmsSensorData messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.sensors.TmsSensorData"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_tms_sensor_data_async = on_fi_digitraffic_road_mqtt_tms_sensor_data
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_tms_sensor_data"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_tms_sensor_data(
            topic=test_topic,
            station_id=f"test_station_id_{i}",
            sensor_id=f"test_sensor_id_{i}",
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_weather_sensor_data_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.WeatherSensorData message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherSensorData.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_weather_sensor_data(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.WeatherSensorData, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.WeatherSensorData messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.sensors.WeatherSensorData"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_weather_sensor_data_async = on_fi_digitraffic_road_mqtt_weather_sensor_data
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_weather_sensor_data"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_weather_sensor_data(
            topic=test_topic,
            station_id=f"test_station_id_{i}",
            sensor_id=f"test_sensor_id_{i}",
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_traffic_announcement_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.TrafficAnnouncement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_traffic_announcement(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.TrafficMessage, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.TrafficAnnouncement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.messages.TrafficAnnouncement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_traffic_announcement_async = on_fi_digitraffic_road_mqtt_traffic_announcement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_traffic_announcement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_traffic_announcement(
            topic=test_topic,
            situation_id=f"test_situation_id_{i}",
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_road_work_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.RoadWork message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_road_work(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.TrafficMessage, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.RoadWork messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.messages.RoadWork"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_road_work_async = on_fi_digitraffic_road_mqtt_road_work
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_road_work"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_road_work(
            topic=test_topic,
            situation_id=f"test_situation_id_{i}",
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_weight_restriction_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.WeightRestriction message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_weight_restriction(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.TrafficMessage, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.WeightRestriction messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.messages.WeightRestriction"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_weight_restriction_async = on_fi_digitraffic_road_mqtt_weight_restriction
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_weight_restriction"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_weight_restriction(
            topic=test_topic,
            situation_id=f"test_situation_id_{i}",
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_exempted_transport_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.ExemptedTransport message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficMessage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_exempted_transport(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.TrafficMessage, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.ExemptedTransport messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.messages.ExemptedTransport"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_exempted_transport_async = on_fi_digitraffic_road_mqtt_exempted_transport
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_exempted_transport"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_exempted_transport(
            topic=test_topic,
            situation_id=f"test_situation_id_{i}",
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_maintenance_tracking_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.MaintenanceTracking message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MaintenanceTracking.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_maintenance_tracking(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.MaintenanceTracking, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.MaintenanceTracking messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.maintenance.MaintenanceTracking"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_maintenance_tracking_async = on_fi_digitraffic_road_mqtt_maintenance_tracking
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_maintenance_tracking"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_maintenance_tracking(
            topic=test_topic,
            domain=f"test_domain_{i}",
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_tms_station_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.TmsStation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TmsStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_tms_station(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.TmsStation, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.TmsStation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.stations.TmsStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_tms_station_async = on_fi_digitraffic_road_mqtt_tms_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_tms_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_tms_station(
            topic=test_topic,
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_weather_station_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.WeatherStation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_weather_station(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.WeatherStation, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.WeatherStation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.stations.WeatherStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_weather_station_async = on_fi_digitraffic_road_mqtt_weather_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_weather_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_weather_station(
            topic=test_topic,
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
async def test_fi_digitraffic_road_mqtt_fi_digitraffic_road_mqtt_maintenance_task_type_py(mosquitto_broker):
    """Test publishing and receiving fi.digitraffic.road.mqtt.MaintenanceTaskType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MaintenanceTaskType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FiDigitrafficRoadMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FiDigitrafficRoadMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fi_digitraffic_road_mqtt_maintenance_task_type(mqtt_msg, cloud_event, data: digitraffic_road_mqtt_producer_data.MaintenanceTaskType, topic_params: dict):
        """Handler for fi.digitraffic.road.mqtt.MaintenanceTaskType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fi_digitraffic_road_mqtt_maintenance_task_type_async = on_fi_digitraffic_road_mqtt_maintenance_task_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fi_digitraffic_road_mqtt/fi_digitraffic_road_mqtt_maintenance_task_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fi_digitraffic_road_mqtt_maintenance_task_type(
            topic=test_topic,
            task_id=f"test_task_id_{i}",
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


