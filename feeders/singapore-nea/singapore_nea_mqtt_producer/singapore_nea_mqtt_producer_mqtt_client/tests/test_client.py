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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../singapore_nea_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../singapore_nea_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../singapore_nea_mqtt_producer_mqtt_client/src')))

import singapore_nea_mqtt_producer_data
from singapore_nea_mqtt_producer_data import Station
from test_station import Test_Station
from singapore_nea_mqtt_producer_data import WeatherObservation
from test_weatherobservation import Test_WeatherObservation
from singapore_nea_mqtt_producer_data import Region
from test_region import Test_Region
from singapore_nea_mqtt_producer_data import PSIReading
from test_psireading import Test_PSIReading
from singapore_nea_mqtt_producer_data import PM25Reading
from test_pm25reading import Test_PM25Reading
from singapore_nea_mqtt_producer_mqtt_client import SGGovNEAWeatherMqttMqttClient
from singapore_nea_mqtt_producer_mqtt_client import SGGovNEAAirQualityMqttMqttClient

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
async def test_sg_gov_nea_weather_mqtt_sg_gov_nea_weather_station_mqtt_py(mosquitto_broker):
    """Test publishing and receiving SG.Gov.NEA.Weather.Station.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = SGGovNEAWeatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = SGGovNEAWeatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_sg_gov_nea_weather_station_mqtt(mqtt_msg, cloud_event, data: singapore_nea_mqtt_producer_data.Station, topic_params: dict):
        """Handler for SG.Gov.NEA.Weather.Station.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "SG.Gov.NEA.Weather.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.sg_gov_nea_weather_station_mqtt_async = on_sg_gov_nea_weather_station_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/sg_gov_nea_weather_mqtt/sg_gov_nea_weather_station_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_sg_gov_nea_weather_station_mqtt(
            topic=test_topic,
            station_id=f"test_station_id_{i}",
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
async def test_sg_gov_nea_weather_mqtt_sg_gov_nea_weather_weather_observation_mqtt_py(mosquitto_broker):
    """Test publishing and receiving SG.Gov.NEA.Weather.WeatherObservation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = SGGovNEAWeatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = SGGovNEAWeatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_sg_gov_nea_weather_weather_observation_mqtt(mqtt_msg, cloud_event, data: singapore_nea_mqtt_producer_data.WeatherObservation, topic_params: dict):
        """Handler for SG.Gov.NEA.Weather.WeatherObservation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "SG.Gov.NEA.Weather.WeatherObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.sg_gov_nea_weather_weather_observation_mqtt_async = on_sg_gov_nea_weather_weather_observation_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/sg_gov_nea_weather_mqtt/sg_gov_nea_weather_weather_observation_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_sg_gov_nea_weather_weather_observation_mqtt(
            topic=test_topic,
            station_id=f"test_station_id_{i}",
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
async def test_sg_gov_nea_airquality_mqtt_sg_gov_nea_air_quality_region_mqtt_py(mosquitto_broker):
    """Test publishing and receiving SG.Gov.NEA.AirQuality.Region.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Region.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = SGGovNEAAirQualityMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = SGGovNEAAirQualityMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_sg_gov_nea_air_quality_region_mqtt(mqtt_msg, cloud_event, data: singapore_nea_mqtt_producer_data.Region, topic_params: dict):
        """Handler for SG.Gov.NEA.AirQuality.Region.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "SG.Gov.NEA.AirQuality.Region"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.sg_gov_nea_air_quality_region_mqtt_async = on_sg_gov_nea_air_quality_region_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/sg_gov_nea_airquality_mqtt/sg_gov_nea_air_quality_region_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_sg_gov_nea_air_quality_region_mqtt(
            topic=test_topic,
            region=f"test_region_{i}",
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
async def test_sg_gov_nea_airquality_mqtt_sg_gov_nea_air_quality_psireading_mqtt_py(mosquitto_broker):
    """Test publishing and receiving SG.Gov.NEA.AirQuality.PSIReading.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PSIReading.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = SGGovNEAAirQualityMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = SGGovNEAAirQualityMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_sg_gov_nea_air_quality_psireading_mqtt(mqtt_msg, cloud_event, data: singapore_nea_mqtt_producer_data.PSIReading, topic_params: dict):
        """Handler for SG.Gov.NEA.AirQuality.PSIReading.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "SG.Gov.NEA.AirQuality.PSIReading"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.sg_gov_nea_air_quality_psireading_mqtt_async = on_sg_gov_nea_air_quality_psireading_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/sg_gov_nea_airquality_mqtt/sg_gov_nea_air_quality_psireading_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_sg_gov_nea_air_quality_psireading_mqtt(
            topic=test_topic,
            region=f"test_region_{i}",
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
async def test_sg_gov_nea_airquality_mqtt_sg_gov_nea_air_quality_pm25_reading_mqtt_py(mosquitto_broker):
    """Test publishing and receiving SG.Gov.NEA.AirQuality.PM25Reading.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PM25Reading.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = SGGovNEAAirQualityMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = SGGovNEAAirQualityMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_sg_gov_nea_air_quality_pm25_reading_mqtt(mqtt_msg, cloud_event, data: singapore_nea_mqtt_producer_data.PM25Reading, topic_params: dict):
        """Handler for SG.Gov.NEA.AirQuality.PM25Reading.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "SG.Gov.NEA.AirQuality.PM25Reading"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.sg_gov_nea_air_quality_pm25_reading_mqtt_async = on_sg_gov_nea_air_quality_pm25_reading_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/sg_gov_nea_airquality_mqtt/sg_gov_nea_air_quality_pm25_reading_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_sg_gov_nea_air_quality_pm25_reading_mqtt(
            topic=test_topic,
            region=f"test_region_{i}",
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


