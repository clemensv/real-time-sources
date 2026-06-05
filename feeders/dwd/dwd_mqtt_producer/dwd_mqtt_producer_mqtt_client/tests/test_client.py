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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dwd_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dwd_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dwd_mqtt_producer_mqtt_client/src')))

import dwd_mqtt_producer_data
from dwd_mqtt_producer_data import StationMetadata
from test_stationmetadata import Test_StationMetadata
from dwd_mqtt_producer_data import AirTemperature10Min
from test_airtemperature10min import Test_AirTemperature10Min
from dwd_mqtt_producer_data import Precipitation10Min
from test_precipitation10min import Test_Precipitation10Min
from dwd_mqtt_producer_data import Wind10Min
from test_wind10min import Test_Wind10Min
from dwd_mqtt_producer_data import Solar10Min
from test_solar10min import Test_Solar10Min
from dwd_mqtt_producer_data import HourlyObservation
from test_hourlyobservation import Test_HourlyObservation
from dwd_mqtt_producer_data import ExtremeWind10Min
from test_extremewind10min import Test_ExtremeWind10Min
from dwd_mqtt_producer_data import ExtremeTemperature10Min
from test_extremetemperature10min import Test_ExtremeTemperature10Min
from dwd_mqtt_producer_data import Alert
from test_alert import Test_Alert
from dwd_mqtt_producer_data import RadarProductCatalog
from test_radarproductcatalog import Test_RadarProductCatalog
from dwd_mqtt_producer_data import RadarFileProduct
from test_radarfileproduct import Test_RadarFileProduct
from dwd_mqtt_producer_data import ForecastModelCatalog
from test_forecastmodelcatalog import Test_ForecastModelCatalog
from dwd_mqtt_producer_data import IconD2ForecastFile
from test_icond2forecastfile import Test_IconD2ForecastFile
from dwd_mqtt_producer_mqtt_client import DEDWDCDCMqttMqttClient
from dwd_mqtt_producer_mqtt_client import DEDWDWeatherMqttMqttClient
from dwd_mqtt_producer_mqtt_client import DEDWDRadarMqttMqttClient
from dwd_mqtt_producer_mqtt_client import DEDWDForecastMqttMqttClient

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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_station_metadata_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.StationMetadata message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StationMetadata.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_station_metadata(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.StationMetadata, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.StationMetadata messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.StationMetadata"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_station_metadata_async = on_de_dwd_cdc_mqtt_station_metadata
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_station_metadata"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_station_metadata(
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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_air_temperature10_min_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.AirTemperature10Min message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AirTemperature10Min.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_air_temperature10_min(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.AirTemperature10Min, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.AirTemperature10Min messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.AirTemperature10Min"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_air_temperature10_min_async = on_de_dwd_cdc_mqtt_air_temperature10_min
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_air_temperature10_min"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_air_temperature10_min(
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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_precipitation10_min_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.Precipitation10Min message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Precipitation10Min.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_precipitation10_min(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.Precipitation10Min, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.Precipitation10Min messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.Precipitation10Min"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_precipitation10_min_async = on_de_dwd_cdc_mqtt_precipitation10_min
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_precipitation10_min"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_precipitation10_min(
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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_wind10_min_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.Wind10Min message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Wind10Min.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_wind10_min(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.Wind10Min, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.Wind10Min messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.Wind10Min"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_wind10_min_async = on_de_dwd_cdc_mqtt_wind10_min
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_wind10_min"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_wind10_min(
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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_solar10_min_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.Solar10Min message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Solar10Min.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_solar10_min(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.Solar10Min, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.Solar10Min messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.Solar10Min"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_solar10_min_async = on_de_dwd_cdc_mqtt_solar10_min
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_solar10_min"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_solar10_min(
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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_hourly_observation_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.HourlyObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_HourlyObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_hourly_observation(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.HourlyObservation, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.HourlyObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.HourlyObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_hourly_observation_async = on_de_dwd_cdc_mqtt_hourly_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_hourly_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_hourly_observation(
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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_extreme_wind10_min_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.ExtremeWind10Min message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ExtremeWind10Min.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_extreme_wind10_min(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.ExtremeWind10Min, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.ExtremeWind10Min messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.ExtremeWind10Min"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_extreme_wind10_min_async = on_de_dwd_cdc_mqtt_extreme_wind10_min
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_extreme_wind10_min"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_extreme_wind10_min(
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
async def test_de_dwd_cdc_mqtt_de_dwd_cdc_mqtt_extreme_temperature10_min_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.CDC.mqtt.ExtremeTemperature10Min message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ExtremeTemperature10Min.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDCDCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDCDCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_cdc_mqtt_extreme_temperature10_min(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.ExtremeTemperature10Min, topic_params: dict):
        """Handler for DE.DWD.CDC.mqtt.ExtremeTemperature10Min messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.CDC.ExtremeTemperature10Min"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_cdc_mqtt_extreme_temperature10_min_async = on_de_dwd_cdc_mqtt_extreme_temperature10_min
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_cdc_mqtt/de_dwd_cdc_mqtt_extreme_temperature10_min"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_cdc_mqtt_extreme_temperature10_min(
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
async def test_de_dwd_weather_mqtt_de_dwd_weather_mqtt_alert_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.Weather.mqtt.Alert message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Alert.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDWeatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDWeatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_weather_mqtt_alert(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.Alert, topic_params: dict):
        """Handler for DE.DWD.Weather.mqtt.Alert messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.Weather.Alert"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_weather_mqtt_alert_async = on_de_dwd_weather_mqtt_alert
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_weather_mqtt/de_dwd_weather_mqtt_alert"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_weather_mqtt_alert(
            topic=test_topic,
            state=f"test_state_{i}",
            severity=f"test_severity_{i}",
            identifier=f"test_identifier_{i}",
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
async def test_de_dwd_radar_mqtt_de_dwd_radar_mqtt_radar_product_catalog_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.Radar.mqtt.RadarProductCatalog message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RadarProductCatalog.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDRadarMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDRadarMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_radar_mqtt_radar_product_catalog(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.RadarProductCatalog, topic_params: dict):
        """Handler for DE.DWD.Radar.mqtt.RadarProductCatalog messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.Radar.RadarProductCatalog"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_radar_mqtt_radar_product_catalog_async = on_de_dwd_radar_mqtt_radar_product_catalog
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_radar_mqtt/de_dwd_radar_mqtt_radar_product_catalog"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_radar_mqtt_radar_product_catalog(
            topic=test_topic,
            kind=f"test_kind_{i}",
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
async def test_de_dwd_radar_mqtt_de_dwd_radar_mqtt_radar_file_product_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.Radar.mqtt.RadarFileProduct message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RadarFileProduct.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDRadarMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDRadarMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_radar_mqtt_radar_file_product(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.RadarFileProduct, topic_params: dict):
        """Handler for DE.DWD.Radar.mqtt.RadarFileProduct messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.Radar.RadarFileProduct"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_radar_mqtt_radar_file_product_async = on_de_dwd_radar_mqtt_radar_file_product
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_radar_mqtt/de_dwd_radar_mqtt_radar_file_product"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_radar_mqtt_radar_file_product(
            topic=test_topic,
            product_type=f"test_product_type_{i}",
            file_id=f"test_file_id_{i}",
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
async def test_de_dwd_forecast_mqtt_de_dwd_forecast_mqtt_forecast_model_catalog_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.Forecast.mqtt.ForecastModelCatalog message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ForecastModelCatalog.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDForecastMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDForecastMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_forecast_mqtt_forecast_model_catalog(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.ForecastModelCatalog, topic_params: dict):
        """Handler for DE.DWD.Forecast.mqtt.ForecastModelCatalog messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.Forecast.ForecastModelCatalog"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_forecast_mqtt_forecast_model_catalog_async = on_de_dwd_forecast_mqtt_forecast_model_catalog
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_forecast_mqtt/de_dwd_forecast_mqtt_forecast_model_catalog"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_forecast_mqtt_forecast_model_catalog(
            topic=test_topic,
            kind=f"test_kind_{i}",
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
async def test_de_dwd_forecast_mqtt_de_dwd_forecast_mqtt_icon_d2_forecast_file_py(mosquitto_broker):
    """Test publishing and receiving DE.DWD.Forecast.mqtt.IconD2ForecastFile message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_IconD2ForecastFile.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DEDWDForecastMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DEDWDForecastMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_dwd_forecast_mqtt_icon_d2_forecast_file(mqtt_msg, cloud_event, data: dwd_mqtt_producer_data.IconD2ForecastFile, topic_params: dict):
        """Handler for DE.DWD.Forecast.mqtt.IconD2ForecastFile messages."""
        received_data.append(data)
        assert cloud_event['type'] == "DE.DWD.Forecast.IconD2ForecastFile"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_dwd_forecast_mqtt_icon_d2_forecast_file_async = on_de_dwd_forecast_mqtt_icon_d2_forecast_file
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_dwd_forecast_mqtt/de_dwd_forecast_mqtt_icon_d2_forecast_file"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_dwd_forecast_mqtt_icon_d2_forecast_file(
            topic=test_topic,
            variable=f"test_variable_{i}",
            file_id=f"test_file_id_{i}",
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


