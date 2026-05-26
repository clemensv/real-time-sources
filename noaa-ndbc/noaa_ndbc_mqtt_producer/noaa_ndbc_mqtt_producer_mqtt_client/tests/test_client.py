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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_ndbc_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_ndbc_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_ndbc_mqtt_producer_mqtt_client/src')))

import noaa_ndbc_mqtt_producer_data
from noaa_ndbc_mqtt_producer_data import BuoyObservation
from test_noaa_ndbc_mqtt_producer_data_buoyobservation import Test_BuoyObservation
from noaa_ndbc_mqtt_producer_data import BuoyStation
from test_noaa_ndbc_mqtt_producer_data_buoystation import Test_BuoyStation
from noaa_ndbc_mqtt_producer_data import BuoySolarRadiationObservation
from test_noaa_ndbc_mqtt_producer_data_buoysolarradiationobservation import Test_BuoySolarRadiationObservation
from noaa_ndbc_mqtt_producer_data import BuoyOceanographicObservation
from test_noaa_ndbc_mqtt_producer_data_buoyoceanographicobservation import Test_BuoyOceanographicObservation
from noaa_ndbc_mqtt_producer_data import BuoyDartMeasurement
from test_noaa_ndbc_mqtt_producer_data_buoydartmeasurement import Test_BuoyDartMeasurement
from noaa_ndbc_mqtt_producer_data import BuoyContinuousWindObservation
from test_noaa_ndbc_mqtt_producer_data_buoycontinuouswindobservation import Test_BuoyContinuousWindObservation
from noaa_ndbc_mqtt_producer_data import BuoySupplementalMeasurement
from test_noaa_ndbc_mqtt_producer_data_buoysupplementalmeasurement import Test_BuoySupplementalMeasurement
from noaa_ndbc_mqtt_producer_data import BuoyDetailedWaveSummary
from test_noaa_ndbc_mqtt_producer_data_buoydetailedwavesummary import Test_BuoyDetailedWaveSummary
from noaa_ndbc_mqtt_producer_data import BuoyHourlyRainMeasurement
from test_noaa_ndbc_mqtt_producer_data_buoyhourlyrainmeasurement import Test_BuoyHourlyRainMeasurement
from noaa_ndbc_mqtt_producer_mqtt_client import MicrosoftOpenDataUSNOAANDBCMqttMqttClient

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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoyObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoyObservation, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_observation(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoyStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoyStation, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyStation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoyStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_station(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoySolarRadiationObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoySolarRadiationObservation, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySolarRadiationObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_solar_radiation_observation(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoyOceanographicObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoyOceanographicObservation, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyOceanographicObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_oceanographic_observation(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoyDartMeasurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoyDartMeasurement, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDartMeasurement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_dart_measurement(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoyContinuousWindObservation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoyContinuousWindObservation, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyContinuousWindObservation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_continuous_wind_observation(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoySupplementalMeasurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoySupplementalMeasurement, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoySupplementalMeasurement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_supplemental_measurement(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoyDetailedWaveSummary.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoyDetailedWaveSummary, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyDetailedWaveSummary messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_detailed_wave_summary(
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
async def test_microsoft_opendata_us_noaa_ndbc_mqtt_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BuoyHourlyRainMeasurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAANDBCMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement(mqtt_msg, cloud_event, data: noaa_ndbc_mqtt_producer_data.BuoyHourlyRainMeasurement, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.NDBC.mqtt.BuoyHourlyRainMeasurement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement_async = on_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_ndbc_mqtt/microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_ndbc_mqtt_buoy_hourly_rain_measurement(
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


