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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wikimedia_osm_diffs_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wikimedia_osm_diffs_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wikimedia_osm_diffs_mqtt_producer_mqtt_client/src')))

import wikimedia_osm_diffs_mqtt_producer_data
from wikimedia_osm_diffs_mqtt_producer_data import MapChange
from test_wikimedia_osm_diffs_mqtt_producer_data_mapchange import Test_MapChange
from wikimedia_osm_diffs_mqtt_producer_data import ReplicationState
from test_wikimedia_osm_diffs_mqtt_producer_data_replicationstate import Test_ReplicationState
from wikimedia_osm_diffs_mqtt_producer_mqtt_client import OrgOpenStreetMapDiffsMqttMqttClient

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
async def test_org_openstreetmap_diffs_mqtt_org_open_street_map_diffs_mqtt_node_py(mosquitto_broker):
    """Test publishing and receiving Org.OpenStreetMap.Diffs.mqtt.Node message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MapChange.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOpenStreetMapDiffsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOpenStreetMapDiffsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_open_street_map_diffs_mqtt_node(mqtt_msg, cloud_event, data: wikimedia_osm_diffs_mqtt_producer_data.MapChange, topic_params: dict):
        """Handler for Org.OpenStreetMap.Diffs.mqtt.Node messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Org.OpenStreetMap.Diffs.MapChange"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_open_street_map_diffs_mqtt_node_async = on_org_open_street_map_diffs_mqtt_node
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_openstreetmap_diffs_mqtt/org_open_street_map_diffs_mqtt_node"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_open_street_map_diffs_mqtt_node(
            topic=test_topic,
            geohash5=f"test_geohash5_{i}",
            element_id=f"test_element_id_{i}",
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
async def test_org_openstreetmap_diffs_mqtt_org_open_street_map_diffs_mqtt_way_py(mosquitto_broker):
    """Test publishing and receiving Org.OpenStreetMap.Diffs.mqtt.Way message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MapChange.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOpenStreetMapDiffsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOpenStreetMapDiffsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_open_street_map_diffs_mqtt_way(mqtt_msg, cloud_event, data: wikimedia_osm_diffs_mqtt_producer_data.MapChange, topic_params: dict):
        """Handler for Org.OpenStreetMap.Diffs.mqtt.Way messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Org.OpenStreetMap.Diffs.MapChange"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_open_street_map_diffs_mqtt_way_async = on_org_open_street_map_diffs_mqtt_way
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_openstreetmap_diffs_mqtt/org_open_street_map_diffs_mqtt_way"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_open_street_map_diffs_mqtt_way(
            topic=test_topic,
            geohash5=f"test_geohash5_{i}",
            element_id=f"test_element_id_{i}",
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
async def test_org_openstreetmap_diffs_mqtt_org_open_street_map_diffs_mqtt_relation_py(mosquitto_broker):
    """Test publishing and receiving Org.OpenStreetMap.Diffs.mqtt.Relation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_MapChange.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOpenStreetMapDiffsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOpenStreetMapDiffsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_open_street_map_diffs_mqtt_relation(mqtt_msg, cloud_event, data: wikimedia_osm_diffs_mqtt_producer_data.MapChange, topic_params: dict):
        """Handler for Org.OpenStreetMap.Diffs.mqtt.Relation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Org.OpenStreetMap.Diffs.MapChange"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_open_street_map_diffs_mqtt_relation_async = on_org_open_street_map_diffs_mqtt_relation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_openstreetmap_diffs_mqtt/org_open_street_map_diffs_mqtt_relation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_open_street_map_diffs_mqtt_relation(
            topic=test_topic,
            geohash5=f"test_geohash5_{i}",
            element_id=f"test_element_id_{i}",
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
async def test_org_openstreetmap_diffs_mqtt_org_open_street_map_diffs_mqtt_replication_state_py(mosquitto_broker):
    """Test publishing and receiving Org.OpenStreetMap.Diffs.mqtt.ReplicationState message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ReplicationState.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = OrgOpenStreetMapDiffsMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = OrgOpenStreetMapDiffsMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_org_open_street_map_diffs_mqtt_replication_state(mqtt_msg, cloud_event, data: wikimedia_osm_diffs_mqtt_producer_data.ReplicationState, topic_params: dict):
        """Handler for Org.OpenStreetMap.Diffs.mqtt.ReplicationState messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Org.OpenStreetMap.Diffs.ReplicationState"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.org_open_street_map_diffs_mqtt_replication_state_async = on_org_open_street_map_diffs_mqtt_replication_state
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/org_openstreetmap_diffs_mqtt/org_open_street_map_diffs_mqtt_replication_state"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_org_open_street_map_diffs_mqtt_replication_state(
            topic=test_topic,
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


