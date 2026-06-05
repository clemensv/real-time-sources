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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entsoe_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entsoe_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entsoe_mqtt_producer_mqtt_client/src')))

import entsoe_mqtt_producer_data
from entsoe_mqtt_producer_data import DayAheadPrices
from test_dayaheadprices import Test_DayAheadPrices
from entsoe_mqtt_producer_data import ActualTotalLoad
from test_actualtotalload import Test_ActualTotalLoad
from entsoe_mqtt_producer_data import LoadForecastMargin
from test_loadforecastmargin import Test_LoadForecastMargin
from entsoe_mqtt_producer_data import GenerationForecast
from test_generationforecast import Test_GenerationForecast
from entsoe_mqtt_producer_data import ReservoirFillingInformation
from test_reservoirfillinginformation import Test_ReservoirFillingInformation
from entsoe_mqtt_producer_data import ActualGeneration
from test_actualgeneration import Test_ActualGeneration
from entsoe_mqtt_producer_data import ActualGenerationPerType
from test_actualgenerationpertype import Test_ActualGenerationPerType
from entsoe_mqtt_producer_data import WindSolarForecast
from test_windsolarforecast import Test_WindSolarForecast
from entsoe_mqtt_producer_data import WindSolarGeneration
from test_windsolargeneration import Test_WindSolarGeneration
from entsoe_mqtt_producer_data import InstalledGenerationCapacityPerType
from test_installedgenerationcapacitypertype import Test_InstalledGenerationCapacityPerType
from entsoe_mqtt_producer_data import CrossBorderPhysicalFlows
from test_crossborderphysicalflows import Test_CrossBorderPhysicalFlows
from entsoe_mqtt_producer_mqtt_client import EuEntsoeTransparencyByDomainMqttMqttClient
from entsoe_mqtt_producer_mqtt_client import EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient
from entsoe_mqtt_producer_mqtt_client import EuEntsoeTransparencyCrossBorderMqttMqttClient

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
async def test_eu_entsoe_transparency_bydomain_mqtt_eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DayAheadPrices.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.DayAheadPrices, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.DayAheadPrices"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices_async = on_eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomain_mqtt/eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_mqtt_day_ahead_prices(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
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
async def test_eu_entsoe_transparency_bydomain_mqtt_eu_entsoe_transparency_by_domain_mqtt_actual_total_load_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ActualTotalLoad.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_mqtt_actual_total_load(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.ActualTotalLoad, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.ActualTotalLoad"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_mqtt_actual_total_load_async = on_eu_entsoe_transparency_by_domain_mqtt_actual_total_load
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomain_mqtt/eu_entsoe_transparency_by_domain_mqtt_actual_total_load"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_mqtt_actual_total_load(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
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
async def test_eu_entsoe_transparency_bydomain_mqtt_eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LoadForecastMargin.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.LoadForecastMargin, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.LoadForecastMargin"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin_async = on_eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomain_mqtt/eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_mqtt_load_forecast_margin(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
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
async def test_eu_entsoe_transparency_bydomain_mqtt_eu_entsoe_transparency_by_domain_mqtt_generation_forecast_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GenerationForecast.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_mqtt_generation_forecast(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.GenerationForecast, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.GenerationForecast"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_mqtt_generation_forecast_async = on_eu_entsoe_transparency_by_domain_mqtt_generation_forecast
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomain_mqtt/eu_entsoe_transparency_by_domain_mqtt_generation_forecast"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_mqtt_generation_forecast(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
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
async def test_eu_entsoe_transparency_bydomain_mqtt_eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ReservoirFillingInformation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.ReservoirFillingInformation, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.ReservoirFillingInformation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information_async = on_eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomain_mqtt/eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_mqtt_reservoir_filling_information(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
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
async def test_eu_entsoe_transparency_bydomain_mqtt_eu_entsoe_transparency_by_domain_mqtt_actual_generation_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ActualGeneration.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_mqtt_actual_generation(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.ActualGeneration, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.ActualGeneration"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_mqtt_actual_generation_async = on_eu_entsoe_transparency_by_domain_mqtt_actual_generation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomain_mqtt/eu_entsoe_transparency_by_domain_mqtt_actual_generation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_mqtt_actual_generation(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
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
async def test_eu_entsoe_transparency_bydomainpsrtype_mqtt_eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ActualGenerationPerType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.ActualGenerationPerType, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.ActualGenerationPerType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type_async = on_eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomainpsrtype_mqtt/eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_actual_generation_per_type(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
            psr_type=f"test_psrType_{i}",
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
async def test_eu_entsoe_transparency_bydomainpsrtype_mqtt_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WindSolarForecast.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.WindSolarForecast, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.WindSolarForecast"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast_async = on_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomainpsrtype_mqtt/eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_forecast(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
            psr_type=f"test_psrType_{i}",
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
async def test_eu_entsoe_transparency_bydomainpsrtype_mqtt_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WindSolarGeneration.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.WindSolarGeneration, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.WindSolarGeneration"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation_async = on_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomainpsrtype_mqtt/eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_wind_solar_generation(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
            psr_type=f"test_psrType_{i}",
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
async def test_eu_entsoe_transparency_bydomainpsrtype_mqtt_eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_InstalledGenerationCapacityPerType.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyByDomainPsrTypeMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.InstalledGenerationCapacityPerType, topic_params: dict):
        """Handler for eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.InstalledGenerationCapacityPerType"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type_async = on_eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_bydomainpsrtype_mqtt/eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_by_domain_psr_type_mqtt_installed_generation_capacity_per_type(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
            psr_type=f"test_psrType_{i}",
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
async def test_eu_entsoe_transparency_crossborder_mqtt_eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows_py(mosquitto_broker):
    """Test publishing and receiving eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CrossBorderPhysicalFlows.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = EuEntsoeTransparencyCrossBorderMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = EuEntsoeTransparencyCrossBorderMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows(mqtt_msg, cloud_event, data: entsoe_mqtt_producer_data.CrossBorderPhysicalFlows, topic_params: dict):
        """Handler for eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows messages."""
        received_data.append(data)
        assert cloud_event['type'] == "eu.entsoe.transparency.CrossBorderPhysicalFlows"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows_async = on_eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/eu_entsoe_transparency_crossborder_mqtt/eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_eu_entsoe_transparency_cross_border_mqtt_cross_border_physical_flows(
            topic=test_topic,
            in_domain=f"test_inDomain_{i}",
            out_domain=f"test_outDomain_{i}",
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


