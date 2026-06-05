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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bom_australia_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bom_australia_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bom_australia_mqtt_producer_mqtt_client/src')))

import bom_australia_mqtt_producer_data
from bom_australia_mqtt_producer_data import Station
from test_station import Test_Station
from bom_australia_mqtt_producer_data import WeatherObservation
from test_weatherobservation import Test_WeatherObservation
from bom_australia_mqtt_producer_data import WarningBulletin
from test_warningbulletin import Test_WarningBulletin
from bom_australia_mqtt_producer_mqtt_client import AUGovBOMWeatherMqttMqttClient
from bom_australia_mqtt_producer_mqtt_client import AUGovBOMWarningMqttMqttClient

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
async def test_au_gov_bom_weather_mqtt_au_gov_bom_weather_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving AU.Gov.BOM.Weather.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = AUGovBOMWeatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = AUGovBOMWeatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_au_gov_bom_weather_mqtt_station(mqtt_msg, cloud_event, data: bom_australia_mqtt_producer_data.Station, topic_params: dict):
        """Handler for AU.Gov.BOM.Weather.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "AU.Gov.BOM.Weather.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.au_gov_bom_weather_mqtt_station_async = on_au_gov_bom_weather_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/au_gov_bom_weather_mqtt/au_gov_bom_weather_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_au_gov_bom_weather_mqtt_station(
            topic=test_topic,
            station_wmo=f"test_station_wmo_{i}",
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
async def test_au_gov_bom_weather_mqtt_au_gov_bom_weather_mqtt_weather_observation_py(mosquitto_broker):
    """Test publishing and receiving AU.Gov.BOM.Weather.mqtt.WeatherObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = AUGovBOMWeatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = AUGovBOMWeatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_au_gov_bom_weather_mqtt_weather_observation(mqtt_msg, cloud_event, data: bom_australia_mqtt_producer_data.WeatherObservation, topic_params: dict):
        """Handler for AU.Gov.BOM.Weather.mqtt.WeatherObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "AU.Gov.BOM.Weather.WeatherObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.au_gov_bom_weather_mqtt_weather_observation_async = on_au_gov_bom_weather_mqtt_weather_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/au_gov_bom_weather_mqtt/au_gov_bom_weather_mqtt_weather_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_au_gov_bom_weather_mqtt_weather_observation(
            topic=test_topic,
            station_wmo=f"test_station_wmo_{i}",
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
async def test_au_gov_bom_warning_mqtt_au_gov_bom_warning_mqtt_warning_bulletin_py(mosquitto_broker):
    """Test publishing and receiving AU.Gov.BOM.Warning.mqtt.WarningBulletin message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WarningBulletin.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = AUGovBOMWarningMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = AUGovBOMWarningMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_au_gov_bom_warning_mqtt_warning_bulletin(mqtt_msg, cloud_event, data: bom_australia_mqtt_producer_data.WarningBulletin, topic_params: dict):
        """Handler for AU.Gov.BOM.Warning.mqtt.WarningBulletin messages."""
        received_data.append(data)
        assert cloud_event['type'] == "AU.Gov.BOM.Warning.WarningBulletin"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.au_gov_bom_warning_mqtt_warning_bulletin_async = on_au_gov_bom_warning_mqtt_warning_bulletin
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/au_gov_bom_warning_mqtt/au_gov_bom_warning_mqtt_warning_bulletin"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_au_gov_bom_warning_mqtt_warning_bulletin(
            topic=test_topic,
            state=f"test_state_{i}",
            severity=f"test_severity_{i}",
            warning_id=f"test_warning_id_{i}",
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


