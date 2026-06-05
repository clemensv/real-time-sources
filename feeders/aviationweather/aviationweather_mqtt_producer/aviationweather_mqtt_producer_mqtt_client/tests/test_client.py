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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../aviationweather_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../aviationweather_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../aviationweather_mqtt_producer_mqtt_client/src')))

import aviationweather_mqtt_producer_data
from aviationweather_mqtt_producer_data import Station
from test_station import Test_Station
from aviationweather_mqtt_producer_data import Metar
from test_metar import Test_Metar
from aviationweather_mqtt_producer_data import Sigmet
from test_sigmet import Test_Sigmet
from aviationweather_mqtt_producer_mqtt_client import GovNoaaAviationweatherMqttMqttClient

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
async def test_gov_noaa_aviationweather_mqtt_gov_noaa_aviationweather_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving gov.noaa.aviationweather.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GovNoaaAviationweatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GovNoaaAviationweatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_gov_noaa_aviationweather_mqtt_station(mqtt_msg, cloud_event, data: aviationweather_mqtt_producer_data.Station, topic_params: dict):
        """Handler for gov.noaa.aviationweather.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "gov.noaa.aviationweather.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.gov_noaa_aviationweather_mqtt_station_async = on_gov_noaa_aviationweather_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/gov_noaa_aviationweather_mqtt/gov_noaa_aviationweather_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_gov_noaa_aviationweather_mqtt_station(
            topic=test_topic,
            icao_id=f"test_icao_id_{i}",
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
async def test_gov_noaa_aviationweather_mqtt_gov_noaa_aviationweather_mqtt_metar_py(mosquitto_broker):
    """Test publishing and receiving gov.noaa.aviationweather.mqtt.Metar message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Metar.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GovNoaaAviationweatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GovNoaaAviationweatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_gov_noaa_aviationweather_mqtt_metar(mqtt_msg, cloud_event, data: aviationweather_mqtt_producer_data.Metar, topic_params: dict):
        """Handler for gov.noaa.aviationweather.mqtt.Metar messages."""
        received_data.append(data)
        assert cloud_event['type'] == "gov.noaa.aviationweather.Metar"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.gov_noaa_aviationweather_mqtt_metar_async = on_gov_noaa_aviationweather_mqtt_metar
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/gov_noaa_aviationweather_mqtt/gov_noaa_aviationweather_mqtt_metar"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_gov_noaa_aviationweather_mqtt_metar(
            topic=test_topic,
            icao_id=f"test_icao_id_{i}",
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
async def test_gov_noaa_aviationweather_mqtt_gov_noaa_aviationweather_mqtt_sigmet_py(mosquitto_broker):
    """Test publishing and receiving gov.noaa.aviationweather.mqtt.Sigmet message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Sigmet.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GovNoaaAviationweatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GovNoaaAviationweatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_gov_noaa_aviationweather_mqtt_sigmet(mqtt_msg, cloud_event, data: aviationweather_mqtt_producer_data.Sigmet, topic_params: dict):
        """Handler for gov.noaa.aviationweather.mqtt.Sigmet messages."""
        received_data.append(data)
        assert cloud_event['type'] == "gov.noaa.aviationweather.Sigmet"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.gov_noaa_aviationweather_mqtt_sigmet_async = on_gov_noaa_aviationweather_mqtt_sigmet
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/gov_noaa_aviationweather_mqtt/gov_noaa_aviationweather_mqtt_sigmet"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_gov_noaa_aviationweather_mqtt_sigmet(
            topic=test_topic,
            region=f"test_region_{i}",
            sigmet_id=f"test_sigmet_id_{i}",
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


