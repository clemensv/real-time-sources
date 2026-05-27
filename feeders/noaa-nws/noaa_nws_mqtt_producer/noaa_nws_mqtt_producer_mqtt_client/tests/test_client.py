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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_nws_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_nws_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_nws_mqtt_producer_mqtt_client/src')))

import noaa_nws_mqtt_producer_data
from noaa_nws_mqtt_producer_data import WeatherAlert
from test_noaa_nws_mqtt_producer_data_weatheralert import Test_WeatherAlert
from noaa_nws_mqtt_producer_data import ObservationStation
from test_noaa_nws_mqtt_producer_data_observationstation import Test_ObservationStation
from noaa_nws_mqtt_producer_data import WeatherObservation
from test_noaa_nws_mqtt_producer_data_weatherobservation import Test_WeatherObservation
from noaa_nws_mqtt_producer_mqtt_client import MicrosoftOpenDataUSNOAANWSAlertsMqttMqttClient
from noaa_nws_mqtt_producer_mqtt_client import MicrosoftOpenDataUSNOAANWSObservationsMqttMqttClient

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
async def test_microsoft_opendata_us_noaa_nws_alerts_mqtt_microsoft_open_data_us_noaa_nws_alerts_mqtt_weather_alert_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NWS.Alerts.mqtt.WeatherAlert message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherAlert.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANWSAlertsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANWSAlertsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_nws_alerts_mqtt_weather_alert(mqtt_msg, cloud_event, data: noaa_nws_mqtt_producer_data.WeatherAlert, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NWS.Alerts.mqtt.WeatherAlert messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NWS.WeatherAlert"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_nws_alerts_mqtt_weather_alert_async = on_microsoft_open_data_us_noaa_nws_alerts_mqtt_weather_alert
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_nws_alerts_mqtt/microsoft_open_data_us_noaa_nws_alerts_mqtt_weather_alert"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_nws_alerts_mqtt_weather_alert(
            topic=test_topic,
            state=f"test_state_{i}",
            severity=f"test_severity_{i}",
            event_type=f"test_event_type_{i}",
            alert_id=f"test_alert_id_{i}",
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
async def test_microsoft_opendata_us_noaa_nws_observations_mqtt_microsoft_open_data_us_noaa_nws_observations_mqtt_observation_station_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NWS.Observations.mqtt.ObservationStation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ObservationStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANWSObservationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANWSObservationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_nws_observations_mqtt_observation_station(mqtt_msg, cloud_event, data: noaa_nws_mqtt_producer_data.ObservationStation, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NWS.Observations.mqtt.ObservationStation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NWS.ObservationStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_nws_observations_mqtt_observation_station_async = on_microsoft_open_data_us_noaa_nws_observations_mqtt_observation_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_nws_observations_mqtt/microsoft_open_data_us_noaa_nws_observations_mqtt_observation_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_nws_observations_mqtt_observation_station(
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
async def test_microsoft_opendata_us_noaa_nws_observations_mqtt_microsoft_open_data_us_noaa_nws_observations_mqtt_weather_observation_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NWS.Observations.mqtt.WeatherObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANWSObservationsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANWSObservationsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_nws_observations_mqtt_weather_observation(mqtt_msg, cloud_event, data: noaa_nws_mqtt_producer_data.WeatherObservation, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NWS.Observations.mqtt.WeatherObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NWS.WeatherObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_nws_observations_mqtt_weather_observation_async = on_microsoft_open_data_us_noaa_nws_observations_mqtt_weather_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_nws_observations_mqtt/microsoft_open_data_us_noaa_nws_observations_mqtt_weather_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_nws_observations_mqtt_weather_observation(
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


