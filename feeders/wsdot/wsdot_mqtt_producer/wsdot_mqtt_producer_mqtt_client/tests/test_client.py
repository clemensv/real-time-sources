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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wsdot_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wsdot_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wsdot_mqtt_producer_mqtt_client/src')))

import wsdot_mqtt_producer_data
from wsdot_mqtt_producer_data import TrafficFlowStation
from test_trafficflowstation import Test_TrafficFlowStation
from wsdot_mqtt_producer_data import TrafficFlowReading
from test_trafficflowreading import Test_TrafficFlowReading
from wsdot_mqtt_producer_data import TravelTimeRoute
from test_traveltimeroute import Test_TravelTimeRoute
from wsdot_mqtt_producer_data import MountainPassCondition
from test_mountainpasscondition import Test_MountainPassCondition
from wsdot_mqtt_producer_data import WeatherStation
from test_weatherstation import Test_WeatherStation
from wsdot_mqtt_producer_data import WeatherReading
from test_weatherreading import Test_WeatherReading
from wsdot_mqtt_producer_data import TollRate
from test_tollrate import Test_TollRate
from wsdot_mqtt_producer_data import CommercialVehicleRestriction
from test_commercialvehiclerestriction import Test_CommercialVehicleRestriction
from wsdot_mqtt_producer_data import BorderCrossing
from test_bordercrossing import Test_BorderCrossing
from wsdot_mqtt_producer_data import VesselLocation
from test_vessellocation import Test_VesselLocation
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotTrafficMqttMqttClient
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotTraveltimesMqttMqttClient
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotMountainpassMqttMqttClient
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotWeatherMqttMqttClient
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotTollsMqttMqttClient
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotCvrestrictionsMqttMqttClient
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotBorderMqttMqttClient
from wsdot_mqtt_producer_mqtt_client import UsWaWsdotFerriesMqttMqttClient

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
async def test_us_wa_wsdot_traffic_mqtt_us_wa_wsdot_traffic_traffic_flow_station_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.traffic.TrafficFlowStation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficFlowStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotTrafficMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotTrafficMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_traffic_traffic_flow_station_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.TrafficFlowStation, topic_params: dict):
        """Handler for us.wa.wsdot.traffic.TrafficFlowStation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.traffic.TrafficFlowStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_traffic_traffic_flow_station_mqtt_async = on_us_wa_wsdot_traffic_traffic_flow_station_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_traffic_mqtt/us_wa_wsdot_traffic_traffic_flow_station_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_traffic_traffic_flow_station_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            flow_data_id=f"test_flow_data_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_traffic_mqtt_us_wa_wsdot_traffic_traffic_flow_reading_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.traffic.TrafficFlowReading.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficFlowReading.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotTrafficMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotTrafficMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_traffic_traffic_flow_reading_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.TrafficFlowReading, topic_params: dict):
        """Handler for us.wa.wsdot.traffic.TrafficFlowReading.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.traffic.TrafficFlowReading"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_traffic_traffic_flow_reading_mqtt_async = on_us_wa_wsdot_traffic_traffic_flow_reading_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_traffic_mqtt/us_wa_wsdot_traffic_traffic_flow_reading_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_traffic_traffic_flow_reading_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            flow_data_id=f"test_flow_data_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_traveltimes_mqtt_us_wa_wsdot_traveltimes_travel_time_route_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TravelTimeRoute.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotTraveltimesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotTraveltimesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_traveltimes_travel_time_route_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.TravelTimeRoute, topic_params: dict):
        """Handler for us.wa.wsdot.traveltimes.TravelTimeRoute.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.traveltimes.TravelTimeRoute"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_traveltimes_travel_time_route_mqtt_async = on_us_wa_wsdot_traveltimes_travel_time_route_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_traveltimes_mqtt/us_wa_wsdot_traveltimes_travel_time_route_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_traveltimes_travel_time_route_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            travel_time_id=f"test_travel_time_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_mountainpass_mqtt_us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.mountainpass.MountainPassCondition.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MountainPassCondition.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotMountainpassMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotMountainpassMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.MountainPassCondition, topic_params: dict):
        """Handler for us.wa.wsdot.mountainpass.MountainPassCondition.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.mountainpass.MountainPassCondition"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt_async = on_us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_mountainpass_mqtt/us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_mountainpass_mountain_pass_condition_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            mountain_pass_id=f"test_mountain_pass_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_weather_mqtt_us_wa_wsdot_weather_weather_station_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.weather.WeatherStation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherStation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotWeatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotWeatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_weather_weather_station_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.WeatherStation, topic_params: dict):
        """Handler for us.wa.wsdot.weather.WeatherStation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.weather.WeatherStation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_weather_weather_station_mqtt_async = on_us_wa_wsdot_weather_weather_station_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_weather_mqtt/us_wa_wsdot_weather_weather_station_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_weather_weather_station_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_weather_mqtt_us_wa_wsdot_weather_weather_reading_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.weather.WeatherReading.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WeatherReading.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotWeatherMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotWeatherMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_weather_weather_reading_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.WeatherReading, topic_params: dict):
        """Handler for us.wa.wsdot.weather.WeatherReading.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.weather.WeatherReading"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_weather_weather_reading_mqtt_async = on_us_wa_wsdot_weather_weather_reading_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_weather_mqtt/us_wa_wsdot_weather_weather_reading_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_weather_weather_reading_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_tolls_mqtt_us_wa_wsdot_tolls_toll_rate_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.tolls.TollRate.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TollRate.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotTollsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotTollsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_tolls_toll_rate_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.TollRate, topic_params: dict):
        """Handler for us.wa.wsdot.tolls.TollRate.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.tolls.TollRate"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_tolls_toll_rate_mqtt_async = on_us_wa_wsdot_tolls_toll_rate_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_tolls_mqtt/us_wa_wsdot_tolls_toll_rate_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_tolls_toll_rate_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            trip_name=f"test_trip_name_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_cvrestrictions_mqtt_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CommercialVehicleRestriction.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotCvrestrictionsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotCvrestrictionsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.CommercialVehicleRestriction, topic_params: dict):
        """Handler for us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt_async = on_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_cvrestrictions_mqtt/us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            state_route_id=f"test_state_route_id_{i}",
            bridge_number=f"test_bridge_number_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_border_mqtt_us_wa_wsdot_border_border_crossing_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.border.BorderCrossing.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BorderCrossing.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotBorderMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotBorderMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_border_border_crossing_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.BorderCrossing, topic_params: dict):
        """Handler for us.wa.wsdot.border.BorderCrossing.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.border.BorderCrossing"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_border_border_crossing_mqtt_async = on_us_wa_wsdot_border_border_crossing_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_border_mqtt/us_wa_wsdot_border_border_crossing_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_border_border_crossing_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            crossing_name=f"test_crossing_name_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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
async def test_us_wa_wsdot_ferries_mqtt_us_wa_wsdot_ferries_vessel_location_mqtt_py(mosquitto_broker):
    """Test publishing and receiving us.wa.wsdot.ferries.VesselLocation.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VesselLocation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = UsWaWsdotFerriesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = UsWaWsdotFerriesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_us_wa_wsdot_ferries_vessel_location_mqtt(mqtt_msg, cloud_event, data: wsdot_mqtt_producer_data.VesselLocation, topic_params: dict):
        """Handler for us.wa.wsdot.ferries.VesselLocation.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "us.wa.wsdot.ferries.VesselLocation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.us_wa_wsdot_ferries_vessel_location_mqtt_async = on_us_wa_wsdot_ferries_vessel_location_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/us_wa_wsdot_ferries_mqtt/us_wa_wsdot_ferries_vessel_location_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_us_wa_wsdot_ferries_vessel_location_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            vessel_id=f"test_vessel_id_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json",
            region="test_region",
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


