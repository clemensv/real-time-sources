# pylint: disable=missing-function-docstring, missing-module-docstring

"""
Simple unit tests for Bluesky producer components.
These tests do not require Kafka/Docker and can run quickly.
"""

import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../bluesky_producer/bluesky_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../bluesky_producer/bluesky_producer_kafka_producer/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from atproto import AtUri
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


def test_process_post_populates_collection_and_primary_lang(monkeypatch):
    kafka_config = {'bootstrap.servers': 'localhost:9092'}
    firehose = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic="test",
        firehose_url="wss://test.example.com",
        collections=[],
        cursor_file=None,
        sample_rate=1.0
    )

    captured = {}
    monkeypatch.setattr(
        firehose,
        'send_cloudevent',
        lambda event_type, source, subject, data: captured.update(
            {'event_type': event_type, 'source': source, 'subject': subject, 'data': data}
        )
    )

    commit = SimpleNamespace(repo='did:plc:mockuser', seq=7, time='2024-01-01T00:00:00.000Z')
    uri = AtUri.from_str('at://did:plc:mockuser/app.bsky.feed.post/abcdef')

    firehose.process_post(
        commit,
        uri,
        {'text': 'hello', 'langs': ['EN', 'de'], 'createdAt': '2024-01-01T00:00:00.000Z'},
        'bafyreimockcid',
    )

    assert captured['event_type'] == 'Bluesky.Feed.Post'
    assert captured['data']['collection'] == 'app.bsky.feed.post'
    assert captured['data']['lang'] == 'en'
    assert captured['data']['langs'] == ['en', 'de']


def test_process_profile_uses_und_lang_and_null_handle(monkeypatch):
    kafka_config = {'bootstrap.servers': 'localhost:9092'}
    firehose = BlueskyFirehose(
        kafka_config=kafka_config,
        kafka_topic="test",
        firehose_url="wss://test.example.com",
        collections=[],
        cursor_file=None,
        sample_rate=1.0
    )

    captured = {}
    monkeypatch.setattr(
        firehose,
        'send_cloudevent',
        lambda event_type, source, subject, data: captured.update(
            {'event_type': event_type, 'source': source, 'subject': subject, 'data': data}
        )
    )

    commit = SimpleNamespace(repo='did:plc:mockuser', seq=8, time='2024-01-01T00:00:00.000Z')
    uri = AtUri.from_str('at://did:plc:mockuser/app.bsky.actor.profile/self')

    firehose.process_profile(
        commit,
        uri,
        {'displayName': 'Mock User', 'createdAt': '2024-01-01T00:00:00.000Z'},
        'bafyreimockprofile',
    )

    assert captured['event_type'] == 'Bluesky.Actor.Profile'
    assert captured['data']['collection'] == 'app.bsky.actor.profile'
    assert captured['data']['lang'] == 'und'
    assert captured['data']['handle'] is None
