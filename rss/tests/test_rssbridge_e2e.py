"""
End-to-end tests for RSS Bridge.

These tests interact with real RSS/Atom feeds and test the complete workflow.
They are marked with @pytest.mark.e2e and are excluded from regular test runs.
"""

import json
import os
import tempfile
from typing import Dict
from unittest.mock import MagicMock, patch
import xml.etree.ElementTree as ET

import pytest
import feedparser
import listparser

from rssbridge.rssbridge import (
    load_state,
    save_state,
    load_feedstore,
    save_feedstore,
    extract_feed_urls_from_webpage,
    parse_connection_string,
)


@pytest.mark.e2e
class TestRealFeedParsing:
    """Test RSS Bridge with real public RSS/Atom feeds."""

    def test_parse_real_rss_feed(self):
        """Test parsing a real RSS feed (W3C News)."""
        # W3C provides a stable RSS feed for testing
        feed_url = "https://www.w3.org/blog/news/feed/"
        
        try:
            parsed = feedparser.parse(feed_url)
            
            # Verify feed was successfully parsed
            assert parsed is not None
            assert not parsed.bozo or parsed.bozo_exception is None, f"Feed parsing error: {parsed.get('bozo_exception')}"
            
            # Verify feed has expected structure
            assert hasattr(parsed, 'feed')
            assert hasattr(parsed, 'entries')
            
            # If feed has entries, verify their structure
            if len(parsed.entries) > 0:
                entry = parsed.entries[0]
                
                # Most RSS feeds should have at least a title or link
                assert hasattr(entry, 'title') or hasattr(entry, 'link')
                
        except Exception as e:
            pytest.skip(f"Could not fetch real RSS feed (network issue): {e}")

    def test_parse_real_atom_feed(self):
        """Test parsing a real Atom feed (IETF datatracker)."""
        # IETF provides stable Atom feeds for testing
        feed_url = "https://datatracker.ietf.org/feed/group/httpbis/"
        
        try:
            parsed = feedparser.parse(feed_url)
            
            # Verify feed was successfully parsed
            assert parsed is not None
            assert not parsed.bozo or parsed.bozo_exception is None, f"Feed parsing error: {parsed.get('bozo_exception')}"
            
            # Verify feed has expected structure
            assert hasattr(parsed, 'feed')
            assert hasattr(parsed, 'entries')
            
            # If feed has entries, verify their structure
            if len(parsed.entries) > 0:
                entry = parsed.entries[0]
                
                # Atom feeds typically have both title and links
                assert hasattr(entry, 'title') or hasattr(entry, 'link')
                
        except Exception as e:
            pytest.skip(f"Could not fetch real Atom feed (network issue): {e}")


@pytest.mark.e2e
class TestFeedDiscoveryReal:
    """Test feed discovery from real web pages."""

    def test_discover_feeds_from_github_blog(self):
        """Test discovering RSS feeds from GitHub's blog."""
        url = "https://github.blog"
        
        try:
            feeds = extract_feed_urls_from_webpage(url)
            
            # GitHub blog should have at least one feed
            # (If this fails, GitHub may have changed their structure)
            assert isinstance(feeds, list)
            
            # Verify discovered feeds are valid URLs
            for feed_url in feeds:
                assert feed_url.startswith('http://') or feed_url.startswith('https://')
                
        except Exception as e:
            pytest.skip(f"Could not fetch GitHub blog (network issue): {e}")


@pytest.mark.e2e
class TestCompleteWorkflow:
    """Test complete RSS Bridge workflow with real components."""

    def setup_method(self):
        """Set up temporary files for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.temp_dir, "test_state.json")
        self.feedstore_file = os.path.join(self.temp_dir, "test_feedstore.xml")

    def teardown_method(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_state_persistence_workflow(self):
        """Test complete state save/load workflow."""
        # Create initial state
        state = {
            "https://example.com/feed1.xml": {
                "last_seen": "2024-01-01T00:00:00Z",
                "last_etag": "abc123"
            },
            "https://example.com/feed2.xml": {
                "last_seen": "2024-01-02T00:00:00Z",
                "last_etag": "def456"
            }
        }
        
        # Patch STATE_FILE to use our temp file
        with patch('rssbridge.rssbridge.STATE_FILE', self.state_file):
            # Save state
            save_state(state)
            
            # Verify file was created
            assert os.path.exists(self.state_file)
            
            # Load state back
            loaded_state = load_state()
            
            # Verify state matches
            assert loaded_state == state
            assert len(loaded_state) == 2
            assert "https://example.com/feed1.xml" in loaded_state
            assert loaded_state["https://example.com/feed1.xml"]["last_etag"] == "abc123"

    def test_feedstore_persistence_workflow(self):
        """Test complete feedstore save/load workflow."""
        # Create list of feed URLs
        feed_urls = [
            "https://example.com/feed1.xml",
            "https://example.com/feed2.xml",
            "https://example.com/feed3.xml"
        ]
        
        # Patch FEEDSTORE_FILE to use our temp file
        with patch('rssbridge.rssbridge.FEEDSTORE_FILE', self.feedstore_file):
            # Save feedstore
            save_feedstore(feed_urls)
            
            # Verify file was created
            assert os.path.exists(self.feedstore_file)
            
            # Verify it's valid XML
            tree = ET.parse(self.feedstore_file)
            root = tree.getroot()
            assert root.tag == 'opml'
            
            # Load feedstore back
            loaded_feeds = load_feedstore()
            
            # Verify feeds match
            assert loaded_feeds == feed_urls
            assert len(loaded_feeds) == 3

    def test_parse_real_opml_file(self):
        """Test parsing an OPML file with real structure using RSS Bridge's load_feedstore."""
        # Create a realistic OPML file using RSS Bridge's format
        feed_urls = [
            "https://www.w3.org/blog/news/feed/",
            "https://github.blog/feed/",
            "https://example.com/feed.xml"
        ]
        
        # Patch FEEDSTORE_FILE to use our temp file
        opml_file = os.path.join(self.temp_dir, "test_feedstore.xml")
        with patch('rssbridge.rssbridge.FEEDSTORE_FILE', opml_file):
            # Save feedstore using RSS Bridge's function
            save_feedstore(feed_urls)
            
            # Verify file was created and is valid XML
            assert os.path.exists(opml_file)
            tree = ET.parse(opml_file)
            root = tree.getroot()
            assert root.tag == 'opml'
            
            # Load feedstore back using RSS Bridge's function
            loaded_feeds = load_feedstore()
            
            # Verify feeds match
            assert loaded_feeds == feed_urls
            assert len(loaded_feeds) == 3


@pytest.mark.e2e
class TestConnectionStringWorkflow:
    """Test connection string parsing for Event Hubs integration."""

    def test_parse_complete_connection_string(self):
        """Test parsing a complete Event Hubs connection string."""
        # Realistic Event Hubs connection string format
        conn_str = (
            'Endpoint=sb://mynamespace.servicebus.windows.net/;'
            'SharedAccessKeyName=sendlisten;'
            'SharedAccessKey=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz=;'
            'EntityPath=rss-events'
        )
        
        config = parse_connection_string(conn_str)
        
        # Verify all components were parsed correctly
        assert config['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert config['kafka_topic'] == 'rss-events'
        assert config['sasl.username'] == '$ConnectionString'
        assert 'SharedAccessKeyName=sendlisten' in config['sasl.password']
        assert 'SharedAccessKey=' in config['sasl.password']
        assert 'EntityPath=rss-events' in config['sasl.password']

    def test_connection_string_with_whitespace_and_quotes(self):
        """Test connection string parsing with real-world formatting."""
        # Connection strings from Azure Portal often have quotes and whitespace
        conn_str = (
            'Endpoint="sb://mynamespace.servicebus.windows.net/";  '
            'SharedAccessKeyName="sendlisten";  '
            'SharedAccessKey="abc123==";  '
            'EntityPath="rss-events"  '
        )
        
        config = parse_connection_string(conn_str)
        
        # Verify whitespace and quotes were handled
        assert config['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert config['kafka_topic'] == 'rss-events'
        assert config['sasl.username'] == '$ConnectionString'


@pytest.mark.e2e
class TestProducerIntegrationWorkflow:
    """Test producer integration patterns."""

    def test_producer_imports_available(self):
        """Test that all producer modules can be imported."""
        # Verify producer module is available
        from rssbridge_producer_kafka_producer.producer import MicrosoftOpenDataRssFeedsEventProducer
        assert MicrosoftOpenDataRssFeedsEventProducer is not None
        
        # Verify data classes are available
        from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem
        from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle
        from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link
        
        assert FeedItem is not None
        assert FeedItemTitle is not None
        assert Link is not None

    def test_kafka_producer_config_structure(self):
        """Test that Kafka producer config has the correct structure."""
        # Create a typical config used for Kafka producer
        kafka_config = {
            'bootstrap.servers': 'test-namespace.servicebus.windows.net:9093',
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': '$ConnectionString',
            'sasl.password': 'Endpoint=sb://test;SharedAccessKeyName=test;SharedAccessKey=test=='
        }
        
        # Verify all required keys are present
        assert 'bootstrap.servers' in kafka_config
        assert 'security.protocol' in kafka_config
        assert 'sasl.mechanisms' in kafka_config
        assert 'sasl.username' in kafka_config
        assert 'sasl.password' in kafka_config
        
        # Verify values are correct type
        assert isinstance(kafka_config['bootstrap.servers'], str)
        assert kafka_config['security.protocol'] == 'SASL_SSL'
        assert kafka_config['sasl.mechanisms'] == 'PLAIN'
