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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_goes_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_goes_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_goes_mqtt_producer_mqtt_client/src')))

import noaa_goes_mqtt_producer_data
from noaa_goes_mqtt_producer_data import GoesXrayFlux
from test_goesxrayflux import Test_GoesXrayFlux
from noaa_goes_mqtt_producer_data import GoesProtonFlux
from test_goesprotonflux import Test_GoesProtonFlux
from noaa_goes_mqtt_producer_data import GoesElectronFlux
from test_goeselectronflux import Test_GoesElectronFlux
from noaa_goes_mqtt_producer_data import GoesMagnetometer
from test_goesmagnetometer import Test_GoesMagnetometer
from noaa_goes_mqtt_producer_data import SpaceWeatherAlert
from test_spaceweatheralert import Test_SpaceWeatherAlert
from noaa_goes_mqtt_producer_data import XrayFlare
from test_xrayflare import Test_XrayFlare
from noaa_goes_mqtt_producer_mqtt_client import MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient

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
async def test_microsoft_opendata_us_noaa_swpc_goes_mqtt_microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GoesXrayFlux.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt(mqtt_msg, cloud_event, data: noaa_goes_mqtt_producer_data.GoesXrayFlux, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt_async = on_microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_swpc_goes_mqtt/microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_swpc_goes_xray_flux_mqtt(
            topic=test_topic,
            satellite=f"test_satellite_{i}",
            energy=f"test_energy_{i}",
            time_tag=f"test_time_tag_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            event="test_event",
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
async def test_microsoft_opendata_us_noaa_swpc_goes_mqtt_microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GoesProtonFlux.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt(mqtt_msg, cloud_event, data: noaa_goes_mqtt_producer_data.GoesProtonFlux, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt_async = on_microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_swpc_goes_mqtt/microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_swpc_goes_proton_flux_mqtt(
            topic=test_topic,
            satellite=f"test_satellite_{i}",
            energy=f"test_energy_{i}",
            time_tag=f"test_time_tag_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            event="test_event",
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
async def test_microsoft_opendata_us_noaa_swpc_goes_mqtt_microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GoesElectronFlux.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt(mqtt_msg, cloud_event, data: noaa_goes_mqtt_producer_data.GoesElectronFlux, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt_async = on_microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_swpc_goes_mqtt/microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_swpc_goes_electron_flux_mqtt(
            topic=test_topic,
            satellite=f"test_satellite_{i}",
            energy=f"test_energy_{i}",
            time_tag=f"test_time_tag_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            event="test_event",
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
async def test_microsoft_opendata_us_noaa_swpc_goes_mqtt_microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GoesMagnetometer.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt(mqtt_msg, cloud_event, data: noaa_goes_mqtt_producer_data.GoesMagnetometer, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt_async = on_microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_swpc_goes_mqtt/microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_swpc_goes_magnetometer_mqtt(
            topic=test_topic,
            satellite=f"test_satellite_{i}",
            time_tag=f"test_time_tag_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            event="test_event",
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
async def test_microsoft_opendata_us_noaa_swpc_goes_mqtt_microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SpaceWeatherAlert.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt(mqtt_msg, cloud_event, data: noaa_goes_mqtt_producer_data.SpaceWeatherAlert, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt_async = on_microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_swpc_goes_mqtt/microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_swpc_space_weather_alert_mqtt(
            topic=test_topic,
            product_id=f"test_product_id_{i}",
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
async def test_microsoft_opendata_us_noaa_swpc_goes_mqtt_microsoft_open_data_us_noaa_swpc_xray_flare_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Microsoft.OpenData.US.NOAA.SWPC.XrayFlare.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_XrayFlare.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = MicrosoftOpenDataUSNOAASWPCGOESMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_microsoft_open_data_us_noaa_swpc_xray_flare_mqtt(mqtt_msg, cloud_event, data: noaa_goes_mqtt_producer_data.XrayFlare, topic_params: dict):
        """Handler for Microsoft.OpenData.US.NOAA.SWPC.XrayFlare.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Microsoft.OpenData.US.NOAA.SWPC.XrayFlare"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.microsoft_open_data_us_noaa_swpc_xray_flare_mqtt_async = on_microsoft_open_data_us_noaa_swpc_xray_flare_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/microsoft_opendata_us_noaa_swpc_goes_mqtt/microsoft_open_data_us_noaa_swpc_xray_flare_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_microsoft_open_data_us_noaa_swpc_xray_flare_mqtt(
            topic=test_topic,
            satellite=f"test_satellite_{i}",
            begin_time=f"test_begin_time_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            flare_class="test_flare_class",
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


