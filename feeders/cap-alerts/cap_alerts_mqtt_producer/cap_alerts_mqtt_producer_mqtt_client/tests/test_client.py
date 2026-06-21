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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cap_alerts_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cap_alerts_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cap_alerts_mqtt_producer_mqtt_client/src')))

import cap_alerts_mqtt_producer_data
from cap_alerts_mqtt_producer_data import CapAlert
from test_capalert import Test_CapAlert
from cap_alerts_mqtt_producer_data import CapZone
from test_capzone import Test_CapZone
from cap_alerts_mqtt_producer_mqtt_client import OrgOasisCapAlertsAlertsMqttMqttClient
from cap_alerts_mqtt_producer_mqtt_client import OrgOasisCapAlertsZonesMqttMqttClient

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
async def test_org_oasis_cap_alerts_alerts_mqtt_org_oasis_cap_alerts_mqtt_cap_alert_py(mosquitto_broker):
    """Test publishing and receiving org.oasis.cap.alerts.mqtt.CapAlert message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CapAlert.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOasisCapAlertsAlertsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOasisCapAlertsAlertsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_oasis_cap_alerts_mqtt_cap_alert(mqtt_msg, cloud_event, data: cap_alerts_mqtt_producer_data.CapAlert, topic_params: dict):
        """Handler for org.oasis.cap.alerts.mqtt.CapAlert messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.oasis.cap.alerts.CapAlert"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_oasis_cap_alerts_mqtt_cap_alert_async = on_org_oasis_cap_alerts_mqtt_cap_alert
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_oasis_cap_alerts_alerts_mqtt/org_oasis_cap_alerts_mqtt_cap_alert"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_oasis_cap_alerts_mqtt_cap_alert(
            topic=test_topic,
            provider_url=f"test_provider_url_{i}",
            cap_source_id=f"test_cap_source_id_{i}",
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
async def test_org_oasis_cap_alerts_zones_mqtt_org_oasis_cap_alerts_mqtt_cap_zone_py(mosquitto_broker):
    """Test publishing and receiving org.oasis.cap.alerts.mqtt.CapZone message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CapZone.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOasisCapAlertsZonesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOasisCapAlertsZonesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_oasis_cap_alerts_mqtt_cap_zone(mqtt_msg, cloud_event, data: cap_alerts_mqtt_producer_data.CapZone, topic_params: dict):
        """Handler for org.oasis.cap.alerts.mqtt.CapZone messages."""
        received_data.append(data)
        assert cloud_event['type'] == "org.oasis.cap.alerts.CapZone"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_oasis_cap_alerts_mqtt_cap_zone_async = on_org_oasis_cap_alerts_mqtt_cap_zone
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_oasis_cap_alerts_zones_mqtt/org_oasis_cap_alerts_mqtt_cap_zone"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_oasis_cap_alerts_mqtt_cap_zone(
            topic=test_topic,
            provider_url=f"test_provider_url_{i}",
            cap_source_id=f"test_cap_source_id_{i}",
            zone_id=f"test_zone_id_{i}",
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


