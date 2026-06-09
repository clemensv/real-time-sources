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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../epa_uv_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../epa_uv_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../epa_uv_mqtt_producer_mqtt_client/src')))

import epa_uv_mqtt_producer_data
from epa_uv_mqtt_producer_data import HourlyForecast
from test_epa_uv_mqtt_producer_data_hourlyforecast import Test_HourlyForecast
from epa_uv_mqtt_producer_data import DailyForecast
from test_epa_uv_mqtt_producer_data_dailyforecast import Test_DailyForecast
from epa_uv_mqtt_producer_mqtt_client import USEPAUVIndexMqttMqttClient

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
async def test_us_epa_uvindex_mqtt_us_epa_uvindex_mqtt_hourly_forecast_py(mosquitto_broker):
    """Test publishing and receiving US.EPA.UVIndex.mqtt.HourlyForecast message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_HourlyForecast.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USEPAUVIndexMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USEPAUVIndexMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_epa_uvindex_mqtt_hourly_forecast(mqtt_msg, cloud_event, data: epa_uv_mqtt_producer_data.HourlyForecast, topic_params: dict):
        """Handler for US.EPA.UVIndex.mqtt.HourlyForecast messages."""
        received_data.append(data)
        assert cloud_event['type'] == "US.EPA.UVIndex.HourlyForecast"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_epa_uvindex_mqtt_hourly_forecast_async = on_us_epa_uvindex_mqtt_hourly_forecast
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_epa_uvindex_mqtt/us_epa_uvindex_mqtt_hourly_forecast"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_epa_uvindex_mqtt_hourly_forecast(
            topic=test_topic,
            location_id=f"test_location_id_{i}",
            data=test_data,
            content_type="application/json",
            state="test_state",
            city_slug="test_city_slug",
            forecast_hour="test_forecast_hour",
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
async def test_us_epa_uvindex_mqtt_us_epa_uvindex_mqtt_daily_forecast_py(mosquitto_broker):
    """Test publishing and receiving US.EPA.UVIndex.mqtt.DailyForecast message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DailyForecast.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USEPAUVIndexMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USEPAUVIndexMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_epa_uvindex_mqtt_daily_forecast(mqtt_msg, cloud_event, data: epa_uv_mqtt_producer_data.DailyForecast, topic_params: dict):
        """Handler for US.EPA.UVIndex.mqtt.DailyForecast messages."""
        received_data.append(data)
        assert cloud_event['type'] == "US.EPA.UVIndex.DailyForecast"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_epa_uvindex_mqtt_daily_forecast_async = on_us_epa_uvindex_mqtt_daily_forecast
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_epa_uvindex_mqtt/us_epa_uvindex_mqtt_daily_forecast"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_epa_uvindex_mqtt_daily_forecast(
            topic=test_topic,
            location_id=f"test_location_id_{i}",
            data=test_data,
            content_type="application/json",
            state="test_state",
            city_slug="test_city_slug",
            forecast_date="test_forecast_date",
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


