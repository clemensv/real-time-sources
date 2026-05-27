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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bluesky_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bluesky_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bluesky_mqtt_producer_mqtt_client/src')))

import bluesky_mqtt_producer_data
from bluesky_mqtt_producer_data import Post
from test_bluesky_mqtt_producer_data_post import Test_Post
from bluesky_mqtt_producer_data import Like
from test_bluesky_mqtt_producer_data_like import Test_Like
from bluesky_mqtt_producer_data import Repost
from test_bluesky_mqtt_producer_data_repost import Test_Repost
from bluesky_mqtt_producer_data import Follow
from test_bluesky_mqtt_producer_data_follow import Test_Follow
from bluesky_mqtt_producer_data import Block
from test_bluesky_mqtt_producer_data_block import Test_Block
from bluesky_mqtt_producer_data import Profile
from test_bluesky_mqtt_producer_data_profile import Test_Profile
from bluesky_mqtt_producer_mqtt_client import BlueskyFirehoseMqttMqttClient

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
async def test_blueskyfirehose_mqtt_bluesky_feed_post_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Bluesky.Feed.Post.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Post.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BlueskyFirehoseMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BlueskyFirehoseMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_bluesky_feed_post_mqtt(mqtt_msg, cloud_event, data: bluesky_mqtt_producer_data.Post, topic_params: dict):
        """Handler for Bluesky.Feed.Post.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Bluesky.Feed.Post"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.bluesky_feed_post_mqtt_async = on_bluesky_feed_post_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/blueskyfirehose_mqtt/bluesky_feed_post_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_bluesky_feed_post_mqtt(
            topic=test_topic,
            firehoseurl=f"test_firehoseurl_{i}",
            did=f"test_did_{i}",
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
async def test_blueskyfirehose_mqtt_bluesky_feed_like_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Bluesky.Feed.Like.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Like.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BlueskyFirehoseMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BlueskyFirehoseMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_bluesky_feed_like_mqtt(mqtt_msg, cloud_event, data: bluesky_mqtt_producer_data.Like, topic_params: dict):
        """Handler for Bluesky.Feed.Like.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Bluesky.Feed.Like"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.bluesky_feed_like_mqtt_async = on_bluesky_feed_like_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/blueskyfirehose_mqtt/bluesky_feed_like_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_bluesky_feed_like_mqtt(
            topic=test_topic,
            firehoseurl=f"test_firehoseurl_{i}",
            did=f"test_did_{i}",
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
async def test_blueskyfirehose_mqtt_bluesky_feed_repost_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Bluesky.Feed.Repost.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Repost.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BlueskyFirehoseMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BlueskyFirehoseMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_bluesky_feed_repost_mqtt(mqtt_msg, cloud_event, data: bluesky_mqtt_producer_data.Repost, topic_params: dict):
        """Handler for Bluesky.Feed.Repost.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Bluesky.Feed.Repost"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.bluesky_feed_repost_mqtt_async = on_bluesky_feed_repost_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/blueskyfirehose_mqtt/bluesky_feed_repost_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_bluesky_feed_repost_mqtt(
            topic=test_topic,
            firehoseurl=f"test_firehoseurl_{i}",
            did=f"test_did_{i}",
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
async def test_blueskyfirehose_mqtt_bluesky_graph_follow_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Bluesky.Graph.Follow.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Follow.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BlueskyFirehoseMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BlueskyFirehoseMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_bluesky_graph_follow_mqtt(mqtt_msg, cloud_event, data: bluesky_mqtt_producer_data.Follow, topic_params: dict):
        """Handler for Bluesky.Graph.Follow.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Bluesky.Graph.Follow"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.bluesky_graph_follow_mqtt_async = on_bluesky_graph_follow_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/blueskyfirehose_mqtt/bluesky_graph_follow_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_bluesky_graph_follow_mqtt(
            topic=test_topic,
            firehoseurl=f"test_firehoseurl_{i}",
            did=f"test_did_{i}",
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
async def test_blueskyfirehose_mqtt_bluesky_graph_block_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Bluesky.Graph.Block.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Block.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BlueskyFirehoseMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BlueskyFirehoseMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_bluesky_graph_block_mqtt(mqtt_msg, cloud_event, data: bluesky_mqtt_producer_data.Block, topic_params: dict):
        """Handler for Bluesky.Graph.Block.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Bluesky.Graph.Block"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.bluesky_graph_block_mqtt_async = on_bluesky_graph_block_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/blueskyfirehose_mqtt/bluesky_graph_block_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_bluesky_graph_block_mqtt(
            topic=test_topic,
            firehoseurl=f"test_firehoseurl_{i}",
            did=f"test_did_{i}",
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
async def test_blueskyfirehose_mqtt_bluesky_actor_profile_mqtt_py(mosquitto_broker):
    """Test publishing and receiving Bluesky.Actor.Profile.mqtt message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Profile.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = BlueskyFirehoseMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = BlueskyFirehoseMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_bluesky_actor_profile_mqtt(mqtt_msg, cloud_event, data: bluesky_mqtt_producer_data.Profile, topic_params: dict):
        """Handler for Bluesky.Actor.Profile.mqtt messages."""
        received_data.append(data)
        assert cloud_event['type'] == "Bluesky.Actor.Profile"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.bluesky_actor_profile_mqtt_async = on_bluesky_actor_profile_mqtt
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/blueskyfirehose_mqtt/bluesky_actor_profile_mqtt"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_bluesky_actor_profile_mqtt(
            topic=test_topic,
            firehoseurl=f"test_firehoseurl_{i}",
            did=f"test_did_{i}",
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


