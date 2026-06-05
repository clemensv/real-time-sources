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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../french_road_traffic_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../french_road_traffic_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../french_road_traffic_mqtt_producer_mqtt_client/src')))

import french_road_traffic_mqtt_producer_data
from french_road_traffic_mqtt_producer_data import TrafficFlowMeasurement
from test_trafficflowmeasurement import Test_TrafficFlowMeasurement
from french_road_traffic_mqtt_producer_data import RoadEvent
from test_roadevent import Test_RoadEvent
from french_road_traffic_mqtt_producer_mqtt_client import FrGouvTransportBisonFuteTrafficFlowMqttMqttClient
from french_road_traffic_mqtt_producer_mqtt_client import FrGouvTransportBisonFuteRoadEventMqttMqttClient

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
async def test_fr_gouv_transport_bison_fute_traffic_flow_mqtt_fr_gouv_transport_bison_fute_traffic_flow_measurement_mqtt_py(mosquitto_broker):
    """Test publishing and receiving fr.gouv.transport.bison_fute.TrafficFlowMeasurement.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficFlowMeasurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FrGouvTransportBisonFuteTrafficFlowMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FrGouvTransportBisonFuteTrafficFlowMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fr_gouv_transport_bison_fute_traffic_flow_measurement_mqtt(mqtt_msg, cloud_event, data: french_road_traffic_mqtt_producer_data.TrafficFlowMeasurement, topic_params: dict):
        """Handler for fr.gouv.transport.bison_fute.TrafficFlowMeasurement.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fr.gouv.transport.bison_fute.TrafficFlowMeasurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fr_gouv_transport_bison_fute_traffic_flow_measurement_mqtt_async = on_fr_gouv_transport_bison_fute_traffic_flow_measurement_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fr_gouv_transport_bison_fute_traffic_flow_mqtt/fr_gouv_transport_bison_fute_traffic_flow_measurement_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fr_gouv_transport_bison_fute_traffic_flow_measurement_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            site_id=f"test_site_id_{i}",
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
async def test_fr_gouv_transport_bison_fute_road_event_mqtt_fr_gouv_transport_bison_fute_road_event_mqtt_py(mosquitto_broker):
    """Test publishing and receiving fr.gouv.transport.bison_fute.RoadEvent.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RoadEvent.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = FrGouvTransportBisonFuteRoadEventMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = FrGouvTransportBisonFuteRoadEventMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_fr_gouv_transport_bison_fute_road_event_mqtt(mqtt_msg, cloud_event, data: french_road_traffic_mqtt_producer_data.RoadEvent, topic_params: dict):
        """Handler for fr.gouv.transport.bison_fute.RoadEvent.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "fr.gouv.transport.bison_fute.RoadEvent"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.fr_gouv_transport_bison_fute_road_event_mqtt_async = on_fr_gouv_transport_bison_fute_road_event_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/fr_gouv_transport_bison_fute_road_event_mqtt/fr_gouv_transport_bison_fute_road_event_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_fr_gouv_transport_bison_fute_road_event_mqtt(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            situation_id=f"test_situation_id_{i}",
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


