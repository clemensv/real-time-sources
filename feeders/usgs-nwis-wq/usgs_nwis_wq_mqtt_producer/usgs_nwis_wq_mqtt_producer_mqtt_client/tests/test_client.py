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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_nwis_wq_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_nwis_wq_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_nwis_wq_mqtt_producer_mqtt_client/src')))

import usgs_nwis_wq_mqtt_producer_data
from usgs_nwis_wq_mqtt_producer_data import MonitoringSite
from test_monitoringsite import Test_MonitoringSite
from usgs_nwis_wq_mqtt_producer_data import WaterQualityReading
from test_waterqualityreading import Test_WaterQualityReading
from usgs_nwis_wq_mqtt_producer_mqtt_client import USGSWaterQualitySitesMqttMqttClient
from usgs_nwis_wq_mqtt_producer_mqtt_client import USGSWaterQualityReadingsMqttMqttClient

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
async def test_usgs_waterquality_sites_mqtt_usgs_water_quality_sites_mqtt_monitoring_site_py(mosquitto_broker):
    """Test publishing and receiving USGS.WaterQuality.Sites.mqtt.MonitoringSite message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MonitoringSite.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSWaterQualitySitesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSWaterQualitySitesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_water_quality_sites_mqtt_monitoring_site(mqtt_msg, cloud_event, data: usgs_nwis_wq_mqtt_producer_data.MonitoringSite, topic_params: dict):
        """Handler for USGS.WaterQuality.Sites.mqtt.MonitoringSite messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.WaterQuality.Sites.MonitoringSite"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_water_quality_sites_mqtt_monitoring_site_async = on_usgs_water_quality_sites_mqtt_monitoring_site
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_waterquality_sites_mqtt/usgs_water_quality_sites_mqtt_monitoring_site"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_water_quality_sites_mqtt_monitoring_site(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            site_number=f"test_site_number_{i}",
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
async def test_usgs_waterquality_readings_mqtt_usgs_water_quality_readings_mqtt_water_quality_reading_py(mosquitto_broker):
    """Test publishing and receiving USGS.WaterQuality.Readings.mqtt.WaterQualityReading message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WaterQualityReading.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSWaterQualityReadingsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSWaterQualityReadingsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_water_quality_readings_mqtt_water_quality_reading(mqtt_msg, cloud_event, data: usgs_nwis_wq_mqtt_producer_data.WaterQualityReading, topic_params: dict):
        """Handler for USGS.WaterQuality.Readings.mqtt.WaterQualityReading messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.WaterQuality.Readings.WaterQualityReading"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_water_quality_readings_mqtt_water_quality_reading_async = on_usgs_water_quality_readings_mqtt_water_quality_reading
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_waterquality_readings_mqtt/usgs_water_quality_readings_mqtt_water_quality_reading"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_water_quality_readings_mqtt_water_quality_reading(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            site_number=f"test_site_number_{i}",
            parameter_code=f"test_parameter_code_{i}",
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


