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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_mqtt_producer_mqtt_client/src')))

import noaa_mqtt_producer_data
from noaa_mqtt_producer_data import WaterLevel
from test_noaa_mqtt_producer_data_waterlevel import Test_WaterLevel
from noaa_mqtt_producer_data import Predictions
from test_noaa_mqtt_producer_data_predictions import Test_Predictions
from noaa_mqtt_producer_data import AirPressure
from test_noaa_mqtt_producer_data_airpressure import Test_AirPressure
from noaa_mqtt_producer_data import AirTemperature
from test_noaa_mqtt_producer_data_airtemperature import Test_AirTemperature
from noaa_mqtt_producer_data import WaterTemperature
from test_noaa_mqtt_producer_data_watertemperature import Test_WaterTemperature
from noaa_mqtt_producer_data import Wind
from test_noaa_mqtt_producer_data_wind import Test_Wind
from noaa_mqtt_producer_data import Humidity
from test_noaa_mqtt_producer_data_humidity import Test_Humidity
from noaa_mqtt_producer_data import Conductivity
from test_noaa_mqtt_producer_data_conductivity import Test_Conductivity
from noaa_mqtt_producer_data import Salinity
from test_noaa_mqtt_producer_data_salinity import Test_Salinity
from noaa_mqtt_producer_data import Station
from test_noaa_mqtt_producer_data_station import Test_Station
from noaa_mqtt_producer_data import Visibility
from test_noaa_mqtt_producer_data_visibility import Test_Visibility
from noaa_mqtt_producer_data import Currents
from test_noaa_mqtt_producer_data_currents import Test_Currents
from noaa_mqtt_producer_data import CurrentPredictions
from test_noaa_mqtt_producer_data_currentpredictions import Test_CurrentPredictions
from noaa_mqtt_producer_mqtt_client import MicrosoftOpenDataUSNOAAMqttMqttClient

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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_water_level_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.WaterLevel message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WaterLevel.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_water_level(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.WaterLevel, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.WaterLevel messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.WaterLevel"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_water_level_async = on_microsoft_open_data_us_noaa_mqtt_water_level
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_water_level"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_water_level(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_predictions_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Predictions message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Predictions.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_predictions(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Predictions, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Predictions messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Predictions"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_predictions_async = on_microsoft_open_data_us_noaa_mqtt_predictions
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_predictions"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_predictions(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_air_pressure_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.AirPressure message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AirPressure.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_air_pressure(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.AirPressure, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.AirPressure messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.AirPressure"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_air_pressure_async = on_microsoft_open_data_us_noaa_mqtt_air_pressure
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_air_pressure"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_air_pressure(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_air_temperature_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.AirTemperature message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AirTemperature.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_air_temperature(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.AirTemperature, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.AirTemperature messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.AirTemperature"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_air_temperature_async = on_microsoft_open_data_us_noaa_mqtt_air_temperature
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_air_temperature"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_air_temperature(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_water_temperature_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WaterTemperature.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_water_temperature(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.WaterTemperature, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.WaterTemperature messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.WaterTemperature"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_water_temperature_async = on_microsoft_open_data_us_noaa_mqtt_water_temperature
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_water_temperature"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_water_temperature(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_wind_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Wind message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Wind.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_wind(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Wind, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Wind messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Wind"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_wind_async = on_microsoft_open_data_us_noaa_mqtt_wind
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_wind"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_wind(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_humidity_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Humidity message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Humidity.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_humidity(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Humidity, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Humidity messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Humidity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_humidity_async = on_microsoft_open_data_us_noaa_mqtt_humidity
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_humidity"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_humidity(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_conductivity_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Conductivity message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Conductivity.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_conductivity(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Conductivity, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Conductivity messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Conductivity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_conductivity_async = on_microsoft_open_data_us_noaa_mqtt_conductivity
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_conductivity"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_conductivity(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_salinity_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Salinity message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Salinity.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_salinity(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Salinity, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Salinity messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Salinity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_salinity_async = on_microsoft_open_data_us_noaa_mqtt_salinity
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_salinity"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_salinity(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_station(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Station, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_station_async = on_microsoft_open_data_us_noaa_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_station(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_visibility_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Visibility message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Visibility.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_visibility(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Visibility, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Visibility messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Visibility"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_visibility_async = on_microsoft_open_data_us_noaa_mqtt_visibility
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_visibility"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_visibility(
            topic=test_topic,
            _datacontenttype=f"test_datacontenttype_{i}",
            station_id=f"test_station_id_{i}",
            _time=f"test_time_{i}",
            _dataschema=f"test_dataschema_{i}",
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_currents_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.Currents message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Currents.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_currents(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.Currents, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.Currents messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.Currents"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_currents_async = on_microsoft_open_data_us_noaa_mqtt_currents
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_currents"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_currents(
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
async def test_microsoft_opendata_us_noaa_mqtt_microsoft_open_data_us_noaa_mqtt_current_predictions_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CurrentPredictions.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAAMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAAMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_mqtt_current_predictions(mqtt_msg, cloud_event, data: noaa_mqtt_producer_data.CurrentPredictions, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.mqtt.CurrentPredictions messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.CurrentPredictions"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_mqtt_current_predictions_async = on_microsoft_open_data_us_noaa_mqtt_current_predictions
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_mqtt/microsoft_open_data_us_noaa_mqtt_current_predictions"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_mqtt_current_predictions(
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


