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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../datex2_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../datex2_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../datex2_mqtt_producer_mqtt_client/src')))

import datex2_mqtt_producer_data
from datex2_mqtt_producer_data import MeasurementSite
from test_measurementsite import Test_MeasurementSite
from datex2_mqtt_producer_data import TrafficMeasurement
from test_trafficmeasurement import Test_TrafficMeasurement
from datex2_mqtt_producer_data import SituationRecord
from test_situationrecord import Test_SituationRecord
from datex2_mqtt_producer_mqtt_client import OrgDatex2MeasuredMqttMqttClient
from datex2_mqtt_producer_mqtt_client import OrgDatex2SituationMqttMqttClient

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
async def test_org_datex2_measured_mqtt_org_datex2_measured_measurement_site_mqtt_py(mosquitto_broker):
    """Test publishing and receiving org.datex2.measured.MeasurementSite.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MeasurementSite.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgDatex2MeasuredMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgDatex2MeasuredMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_datex2_measured_measurement_site_mqtt(mqtt_msg, cloud_event, data: datex2_mqtt_producer_data.MeasurementSite, topic_params: dict):
        """Handler for org.datex2.measured.MeasurementSite.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.datex2.measured.MeasurementSite"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_datex2_measured_measurement_site_mqtt_async = on_org_datex2_measured_measurement_site_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_datex2_measured_mqtt/org_datex2_measured_measurement_site_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_datex2_measured_measurement_site_mqtt(
            topic=test_topic,
            feed_url=f"test_feed_url_{i}",
            supplier_id=f"test_supplier_id_{i}",
            measurement_site_id=f"test_measurement_site_id_{i}",
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
async def test_org_datex2_measured_mqtt_org_datex2_measured_traffic_measurement_mqtt_py(mosquitto_broker):
    """Test publishing and receiving org.datex2.measured.TrafficMeasurement.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TrafficMeasurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgDatex2MeasuredMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgDatex2MeasuredMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_datex2_measured_traffic_measurement_mqtt(mqtt_msg, cloud_event, data: datex2_mqtt_producer_data.TrafficMeasurement, topic_params: dict):
        """Handler for org.datex2.measured.TrafficMeasurement.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.datex2.measured.TrafficMeasurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_datex2_measured_traffic_measurement_mqtt_async = on_org_datex2_measured_traffic_measurement_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_datex2_measured_mqtt/org_datex2_measured_traffic_measurement_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_datex2_measured_traffic_measurement_mqtt(
            topic=test_topic,
            feed_url=f"test_feed_url_{i}",
            supplier_id=f"test_supplier_id_{i}",
            measurement_site_id=f"test_measurement_site_id_{i}",
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
async def test_org_datex2_situation_mqtt_org_datex2_situation_situation_record_mqtt_py(mosquitto_broker):
    """Test publishing and receiving org.datex2.situation.SituationRecord.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SituationRecord.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgDatex2SituationMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgDatex2SituationMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_datex2_situation_situation_record_mqtt(mqtt_msg, cloud_event, data: datex2_mqtt_producer_data.SituationRecord, topic_params: dict):
        """Handler for org.datex2.situation.SituationRecord.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.datex2.situation.SituationRecord"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_datex2_situation_situation_record_mqtt_async = on_org_datex2_situation_situation_record_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_datex2_situation_mqtt/org_datex2_situation_situation_record_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_datex2_situation_situation_record_mqtt(
            topic=test_topic,
            feed_url=f"test_feed_url_{i}",
            supplier_id=f"test_supplier_id_{i}",
            situation_record_id=f"test_situation_record_id_{i}",
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


