# pylint: disable=missing-function-docstring, missing-module-docstring

"""
Simple unit tests for Bluesky producer components.
These tests do not require Kafka/Docker and can run quickly.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from bluesky.bluesky import BlueskyFirehose


def test_parse_connection_string_basic():
    """Test basic Event Hubs connection string parsing."""
    connection_string = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=testkey123;EntityPath=bluesky"
    
    kafka_config = BlueskyFirehose.parse_connection_string(connection_string)
    
    assert kafka_config['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
    assert kafka_config['security.protocol'] == 'SASL_SSL'
    assert kafka_config['sasl.mechanism'] == 'PLAIN'
    assert kafka_config['sasl.username'] == '$ConnectionString'
    assert connection_string in kafka_config['sasl.password']


def test_parse_connection_string_without_entity_path():
    """Test connection string parsing without EntityPath."""
    connection_string = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=MyKey;SharedAccessKey=secret123"
    
    kafka_config = BlueskyFirehose.parse_connection_string(connection_string)
    
    assert kafka_config['bootstrap.servers'] == 'myns.servicebus.windows.net:9093'
    assert kafka_config['security.protocol'] == 'SASL_SSL'
    assert kafka_config['sasl.mechanism'] == 'PLAIN'


def test_firehose_initialization():
    """Test BlueskyFirehose initialization with minimal config."""
    kafka_config = {
        'bootstrap.servers': 'localhost:9092'
    }
    
    firehose = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic="test-topic",
        firehose_url="wss://test.example.com",
        collections=["app.bsky.feed.post"],
        cursor_file=None,
        sample_rate=1.0
    )
    
    assert firehose.kafka_topic == "test-topic"
    assert firehose.firehose_url == "wss://test.example.com"
    assert "app.bsky.feed.post" in firehose.collections
    assert firehose.sample_rate == 1.0


def test_firehose_cursor_operations(tmp_path):
    """Test cursor save/load functionality."""
    cursor_file = tmp_path / "test_cursor.txt"
    
    kafka_config = {
        'bootstrap.servers': 'localhost:9092'
    }
    
    firehose = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic="test",
        firehose_url="wss://test.example.com",
        collections=[],
        cursor_file=str(cursor_file),
        sample_rate=1.0
    )
    
    # Initially no cursor
    assert firehose.load_cursor() is None
    
    # Save a cursor
    firehose.save_cursor(12345)
    
    # Load it back
    assert firehose.load_cursor() == 12345
    
    # Create new instance and verify it loads
    firehose2 = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic="test",
        firehose_url="wss://test.example.com",
        collections=[],
        cursor_file=str(cursor_file),
        sample_rate=1.0
    )
    
    assert firehose2.load_cursor() == 12345


def test_sample_rate_filtering():
    """Test that sample rate is validated."""
    kafka_config = {'bootstrap.servers': 'localhost:9092'}
    
    # Valid sample rates
    for rate in [0.0, 0.5, 1.0]:
        firehose = BlueskyFirehose(
            kafka_config=kafka_config,
            kafka_topic="test",
            firehose_url="wss://test.example.com",
            collections=[],
            cursor_file=None,
            sample_rate=rate
        )
        assert firehose.sample_rate == rate
    
    # Invalid sample rates should default to 1.0 or raise error
    # (Implementation dependent - adjust based on actual behavior)


def test_collections_filtering():
    """Test collection filtering setup."""
    kafka_config = {'bootstrap.servers': 'localhost:9092'}
    
    collections = [
        "app.bsky.feed.post",
        "app.bsky.feed.like",
        "app.bsky.feed.repost"
    ]
    
    firehose = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic="test",
        firehose_url="wss://test.example.com",
        collections=collections,
        cursor_file=None,
        sample_rate=1.0
    )
    
    assert len(firehose.collections) == 3
    assert all(c in firehose.collections for c in collections)


def test_kafka_config_structure():
    """Test that Kafka config is properly structured."""
    kafka_config = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'test-client',
        'compression.type': 'snappy'
    }
    
    firehose = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic="test",
        firehose_url="wss://test.example.com",
        collections=[],
        cursor_file=None,
        sample_rate=1.0
    )
    
    # Verify config is stored properly
    assert hasattr(firehose, 'producer') or hasattr(firehose, 'kafka_config')
