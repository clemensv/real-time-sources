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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_mqtt_producer_mqtt_client/src')))

import gtfs_mqtt_producer_data
from gtfs_mqtt_producer_data import VehiclePosition
from test_vehicleposition import Test_VehiclePosition
from gtfs_mqtt_producer_data import TripUpdate
from test_tripupdate import Test_TripUpdate
from gtfs_mqtt_producer_data import Alert
from test_alert import Test_Alert
from gtfs_mqtt_producer_data import Agency
from test_agency import Test_Agency
from gtfs_mqtt_producer_data import Areas
from test_areas import Test_Areas
from gtfs_mqtt_producer_data import Attributions
from test_attributions import Test_Attributions
from gtfs_mqtt_producer_data import BookingRules
from test_bookingrules import Test_BookingRules
from gtfs_mqtt_producer_data import FareAttributes
from test_fareattributes import Test_FareAttributes
from gtfs_mqtt_producer_data import FareLegRules
from test_farelegrules import Test_FareLegRules
from gtfs_mqtt_producer_data import FareMedia
from test_faremedia import Test_FareMedia
from gtfs_mqtt_producer_data import FareProducts
from test_fareproducts import Test_FareProducts
from gtfs_mqtt_producer_data import FareRules
from test_farerules import Test_FareRules
from gtfs_mqtt_producer_data import FareTransferRules
from test_faretransferrules import Test_FareTransferRules
from gtfs_mqtt_producer_data import FeedInfo
from test_feedinfo import Test_FeedInfo
from gtfs_mqtt_producer_data import Frequencies
from test_frequencies import Test_Frequencies
from gtfs_mqtt_producer_data import Levels
from test_levels import Test_Levels
from gtfs_mqtt_producer_data import LocationGeoJson
from test_locationgeojson import Test_LocationGeoJson
from gtfs_mqtt_producer_data import LocationGroups
from test_locationgroups import Test_LocationGroups
from gtfs_mqtt_producer_data import LocationGroupStores
from test_locationgroupstores import Test_LocationGroupStores
from gtfs_mqtt_producer_data import Networks
from test_networks import Test_Networks
from gtfs_mqtt_producer_data import Pathways
from test_pathways import Test_Pathways
from gtfs_mqtt_producer_data import RouteNetworks
from test_routenetworks import Test_RouteNetworks
from gtfs_mqtt_producer_data import Routes
from test_routes import Test_Routes
from gtfs_mqtt_producer_data import Shapes
from test_shapes import Test_Shapes
from gtfs_mqtt_producer_data import StopAreas
from test_stopareas import Test_StopAreas
from gtfs_mqtt_producer_data import Stops
from test_stops import Test_Stops
from gtfs_mqtt_producer_data import StopTimes
from test_stoptimes import Test_StopTimes
from gtfs_mqtt_producer_data import Timeframes
from test_timeframes import Test_Timeframes
from gtfs_mqtt_producer_data import Transfers
from test_transfers import Test_Transfers
from gtfs_mqtt_producer_data import Translations
from test_translations import Test_Translations
from gtfs_mqtt_producer_data import Trips
from test_trips import Test_Trips
from gtfs_mqtt_producer_mqtt_client import GeneralTransitFeedRealTimeMqttMqttClient
from gtfs_mqtt_producer_mqtt_client import GeneralTransitFeedStaticMqttMqttClient

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
async def test_generaltransitfeedrealtime_mqtt_general_transit_feed_real_time_vehicle_vehicle_position_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedRealTime.Vehicle.VehiclePosition.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_VehiclePosition.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedRealTimeMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedRealTimeMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_real_time_vehicle_vehicle_position_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.VehiclePosition, topic_params: dict):
        """Handler for GeneralTransitFeedRealTime.Vehicle.VehiclePosition.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedRealTime.Vehicle.VehiclePosition"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_real_time_vehicle_vehicle_position_mqtt_async = on_general_transit_feed_real_time_vehicle_vehicle_position_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedrealtime_mqtt/general_transit_feed_real_time_vehicle_vehicle_position_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_real_time_vehicle_vehicle_position_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedrealtime_mqtt_general_transit_feed_real_time_trip_trip_update_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedRealTime.Trip.TripUpdate.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TripUpdate.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedRealTimeMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedRealTimeMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_real_time_trip_trip_update_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.TripUpdate, topic_params: dict):
        """Handler for GeneralTransitFeedRealTime.Trip.TripUpdate.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedRealTime.Trip.TripUpdate"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_real_time_trip_trip_update_mqtt_async = on_general_transit_feed_real_time_trip_trip_update_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedrealtime_mqtt/general_transit_feed_real_time_trip_trip_update_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_real_time_trip_trip_update_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedrealtime_mqtt_general_transit_feed_real_time_alert_alert_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedRealTime.Alert.Alert.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Alert.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedRealTimeMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedRealTimeMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_real_time_alert_alert_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Alert, topic_params: dict):
        """Handler for GeneralTransitFeedRealTime.Alert.Alert.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedRealTime.Alert.Alert"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_real_time_alert_alert_mqtt_async = on_general_transit_feed_real_time_alert_alert_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedrealtime_mqtt/general_transit_feed_real_time_alert_alert_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_real_time_alert_alert_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_agency_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Agency.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Agency.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_agency_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Agency, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Agency.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Agency"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_agency_mqtt_async = on_general_transit_feed_static_agency_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_agency_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_agency_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_areas_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Areas.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Areas.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_areas_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Areas, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Areas.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Areas"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_areas_mqtt_async = on_general_transit_feed_static_areas_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_areas_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_areas_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_attributions_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Attributions.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Attributions.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_attributions_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Attributions, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Attributions.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Attributions"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_attributions_mqtt_async = on_general_transit_feed_static_attributions_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_attributions_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_attributions_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_booking_rules_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeed.BookingRules.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BookingRules.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_booking_rules_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.BookingRules, topic_params: dict):
        """Handler for GeneralTransitFeed.BookingRules.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeed.BookingRules"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_booking_rules_mqtt_async = on_general_transit_feed_booking_rules_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_booking_rules_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_booking_rules_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_fare_attributes_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.FareAttributes.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FareAttributes.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_fare_attributes_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.FareAttributes, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.FareAttributes.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.FareAttributes"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_fare_attributes_mqtt_async = on_general_transit_feed_static_fare_attributes_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_fare_attributes_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_fare_attributes_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_fare_leg_rules_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.FareLegRules.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FareLegRules.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_fare_leg_rules_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.FareLegRules, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.FareLegRules.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.FareLegRules"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_fare_leg_rules_mqtt_async = on_general_transit_feed_static_fare_leg_rules_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_fare_leg_rules_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_fare_leg_rules_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_fare_media_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.FareMedia.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FareMedia.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_fare_media_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.FareMedia, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.FareMedia.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.FareMedia"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_fare_media_mqtt_async = on_general_transit_feed_static_fare_media_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_fare_media_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_fare_media_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_fare_products_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.FareProducts.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FareProducts.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_fare_products_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.FareProducts, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.FareProducts.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.FareProducts"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_fare_products_mqtt_async = on_general_transit_feed_static_fare_products_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_fare_products_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_fare_products_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_fare_rules_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.FareRules.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FareRules.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_fare_rules_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.FareRules, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.FareRules.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.FareRules"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_fare_rules_mqtt_async = on_general_transit_feed_static_fare_rules_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_fare_rules_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_fare_rules_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_fare_transfer_rules_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.FareTransferRules.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FareTransferRules.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_fare_transfer_rules_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.FareTransferRules, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.FareTransferRules.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.FareTransferRules"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_fare_transfer_rules_mqtt_async = on_general_transit_feed_static_fare_transfer_rules_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_fare_transfer_rules_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_fare_transfer_rules_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_feed_info_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.FeedInfo.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FeedInfo.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_feed_info_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.FeedInfo, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.FeedInfo.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.FeedInfo"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_feed_info_mqtt_async = on_general_transit_feed_static_feed_info_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_feed_info_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_feed_info_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_frequencies_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Frequencies.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Frequencies.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_frequencies_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Frequencies, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Frequencies.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Frequencies"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_frequencies_mqtt_async = on_general_transit_feed_static_frequencies_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_frequencies_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_frequencies_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_levels_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Levels.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Levels.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_levels_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Levels, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Levels.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Levels"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_levels_mqtt_async = on_general_transit_feed_static_levels_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_levels_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_levels_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_location_geo_json_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.LocationGeoJson.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LocationGeoJson.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_location_geo_json_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.LocationGeoJson, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.LocationGeoJson.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.LocationGeoJson"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_location_geo_json_mqtt_async = on_general_transit_feed_static_location_geo_json_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_location_geo_json_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_location_geo_json_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_location_groups_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.LocationGroups.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LocationGroups.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_location_groups_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.LocationGroups, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.LocationGroups.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.LocationGroups"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_location_groups_mqtt_async = on_general_transit_feed_static_location_groups_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_location_groups_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_location_groups_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_location_group_stores_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.LocationGroupStores.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LocationGroupStores.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_location_group_stores_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.LocationGroupStores, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.LocationGroupStores.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.LocationGroupStores"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_location_group_stores_mqtt_async = on_general_transit_feed_static_location_group_stores_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_location_group_stores_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_location_group_stores_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_networks_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Networks.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Networks.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_networks_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Networks, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Networks.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Networks"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_networks_mqtt_async = on_general_transit_feed_static_networks_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_networks_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_networks_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_pathways_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Pathways.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Pathways.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_pathways_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Pathways, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Pathways.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Pathways"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_pathways_mqtt_async = on_general_transit_feed_static_pathways_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_pathways_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_pathways_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_route_networks_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.RouteNetworks.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RouteNetworks.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_route_networks_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.RouteNetworks, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.RouteNetworks.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.RouteNetworks"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_route_networks_mqtt_async = on_general_transit_feed_static_route_networks_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_route_networks_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_route_networks_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_routes_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Routes.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Routes.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_routes_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Routes, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Routes.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Routes"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_routes_mqtt_async = on_general_transit_feed_static_routes_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_routes_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_routes_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_shapes_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Shapes.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Shapes.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_shapes_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Shapes, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Shapes.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Shapes"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_shapes_mqtt_async = on_general_transit_feed_static_shapes_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_shapes_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_shapes_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_stop_areas_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.StopAreas.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StopAreas.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_stop_areas_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.StopAreas, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.StopAreas.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.StopAreas"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_stop_areas_mqtt_async = on_general_transit_feed_static_stop_areas_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_stop_areas_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_stop_areas_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_stops_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Stops.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Stops.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_stops_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Stops, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Stops.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Stops"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_stops_mqtt_async = on_general_transit_feed_static_stops_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_stops_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_stops_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_stop_times_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.StopTimes.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_StopTimes.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_stop_times_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.StopTimes, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.StopTimes.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.StopTimes"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_stop_times_mqtt_async = on_general_transit_feed_static_stop_times_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_stop_times_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_stop_times_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_timeframes_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Timeframes.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Timeframes.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_timeframes_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Timeframes, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Timeframes.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Timeframes"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_timeframes_mqtt_async = on_general_transit_feed_static_timeframes_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_timeframes_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_timeframes_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_transfers_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Transfers.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Transfers.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_transfers_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Transfers, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Transfers.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Transfers"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_transfers_mqtt_async = on_general_transit_feed_static_transfers_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_transfers_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_transfers_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_translations_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Translations.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Translations.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_translations_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Translations, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Translations.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Translations"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_translations_mqtt_async = on_general_transit_feed_static_translations_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_translations_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_translations_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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
async def test_generaltransitfeedstatic_mqtt_general_transit_feed_static_trips_mqtt_py(mosquitto_broker):
    """Test publishing and receiving GeneralTransitFeedStatic.Trips.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Trips.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = GeneralTransitFeedStaticMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = GeneralTransitFeedStaticMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_general_transit_feed_static_trips_mqtt(mqtt_msg, cloud_event, data: gtfs_mqtt_producer_data.Trips, topic_params: dict):
        """Handler for GeneralTransitFeedStatic.Trips.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "GeneralTransitFeedStatic.Trips"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.general_transit_feed_static_trips_mqtt_async = on_general_transit_feed_static_trips_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/generaltransitfeedstatic_mqtt/general_transit_feed_static_trips_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_general_transit_feed_static_trips_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            agencyid=f"test_agencyid_{i}",
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


