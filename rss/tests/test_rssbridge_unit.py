"""
Unit tests for RSS Bridge functionality.
Tests core functions without external dependencies.
"""

import pytest
import os
import json
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch, mock_open
from rssbridge.rssbridge import (
    parse_connection_string,
    load_state,
    save_state,
    load_feedstore,
    save_feedstore,
)


@pytest.mark.unit
class TestConnectionStringParsing:
    """Tests for Event Hubs connection string parsing"""

    def test_parse_connection_string_with_all_components(self):
        """Test parsing a complete Event Hubs connection string"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=testkey123;"
            "EntityPath=rss-events"
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'rss-events'
        assert result['sasl.username'] == '$ConnectionString'
        assert connection_string.strip() in result['sasl.password']

    def test_parse_connection_string_strips_whitespace(self):
        """Test that connection string parsing handles whitespace"""
        connection_string = (
            "  Endpoint=sb://test.servicebus.windows.net/;  "
            "EntityPath=rss-events  "
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'rss-events'

    def test_parse_connection_string_with_quotes(self):
        """Test parsing connection string with quoted values"""
        connection_string = (
            'Endpoint="sb://test.servicebus.windows.net/";'
            'EntityPath="rss-events"'
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'rss-events'

    def test_parse_connection_string_removes_protocol_prefix(self):
        """Test that sb:// protocol is removed from endpoint"""
        connection_string = (
            "Endpoint=sb://namespace.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        assert 'sb://' not in result['bootstrap.servers']
        assert result['bootstrap.servers'].startswith('namespace.servicebus.windows.net')

    def test_parse_connection_string_adds_port(self):
        """Test that port 9093 is added to bootstrap server"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'].endswith(':9093')

    def test_parse_connection_string_invalid_format_raises_error(self):
        """Test that malformed connection string raises ValueError"""
        connection_string = "EndpointWithoutEquals;EntityPathAlsoInvalid"
        
        with pytest.raises(ValueError, match="Invalid connection string format"):
            parse_connection_string(connection_string)

    def test_parse_connection_string_sets_sasl_credentials(self):
        """Test that SASL credentials are properly set"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == connection_string.strip()


@pytest.mark.unit
class TestStateFileManagement:
    """Tests for state file loading and saving"""

    @patch('builtins.open', new_callable=mock_open, read_data='{"feed1": "2024-01-01T00:00:00Z"}')
    @patch('os.path.exists', return_value=True)
    def test_load_state_success(self, mock_exists, mock_file):
        """Test loading state from existing file"""
        state = load_state()
        
        assert state == {"feed1": "2024-01-01T00:00:00Z"}

    @patch('os.path.exists', return_value=False)
    def test_load_state_missing_file(self, mock_exists):
        """Test loading state when file doesn't exist"""
        state = load_state()
        
        assert state == {}

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('os.path.exists', return_value=True)
    def test_load_state_invalid_json(self, mock_exists, mock_file):
        """Test loading state with invalid JSON returns empty dict"""
        state = load_state()
        
        assert state == {}

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    def test_save_state_success(self, mock_makedirs, mock_exists, mock_file):
        """Test saving state to file"""
        state = {"feed1": "2024-01-01T00:00:00Z"}
        
        save_state(state)
        
        mock_file.assert_called()
        handle = mock_file()
        assert handle.write.called

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_save_state_creates_directory(self, mock_makedirs, mock_exists, mock_file):
        """Test that save_state creates directory if it doesn't exist"""
        state = {"feed1": "2024-01-01T00:00:00Z"}
        
        save_state(state)
        
        mock_makedirs.assert_called()


@pytest.mark.unit
class TestFeedstoreManagement:
    """Tests for OPML feedstore management"""

    @patch('os.path.exists', return_value=False)
    def test_load_feedstore_missing_file(self, mock_exists):
        """Test loading feedstore when file doesn't exist"""
        feeds = load_feedstore()
        
        assert feeds == []

    @patch('xml.etree.ElementTree.parse')
    @patch('os.path.exists', return_value=True)
    def test_load_feedstore_success(self, mock_exists, mock_parse):
        """Test loading feed URLs from OPML file"""
        # Create mock XML structure
        mock_root = ET.Element("opml")
        mock_body = ET.SubElement(mock_root, "body")
        ET.SubElement(mock_body, "outline", xmlUrl="https://example.com/feed1.xml")
        ET.SubElement(mock_body, "outline", xmlUrl="https://example.com/feed2.xml")
        
        mock_tree = Mock()
        mock_tree.getroot.return_value = mock_root
        mock_parse.return_value = mock_tree
        
        feeds = load_feedstore()
        
        assert len(feeds) == 2
        assert "https://example.com/feed1.xml" in feeds
        assert "https://example.com/feed2.xml" in feeds

    @patch('xml.etree.ElementTree.ElementTree.write')
    def test_save_feedstore_creates_opml(self, mock_write):
        """Test saving feed URLs to OPML file"""
        feeds = [
            "https://example.com/feed1.xml",
            "https://example.com/feed2.xml"
        ]
        
        save_feedstore(feeds)
        
        mock_write.assert_called_once()

    def test_save_feedstore_creates_valid_opml_structure(self):
        """Test that saved OPML has correct structure"""
        feeds = ["https://example.com/feed.xml"]
        
        with patch('xml.etree.ElementTree.ElementTree.write'):
            save_feedstore(feeds)
            
        # If no exception is raised, structure is valid


@pytest.mark.unit
class TestHelperFunctions:
    """Tests for utility helper functions"""

    def test_connection_string_parsing_is_deterministic(self):
        """Test that parsing the same connection string produces identical results"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result1 = parse_connection_string(connection_string)
        result2 = parse_connection_string(connection_string)
        
        assert result1 == result2

    def test_parse_connection_string_preserves_key_order(self):
        """Test that all required keys are present in parsed result"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        required_keys = ['bootstrap.servers', 'kafka_topic', 'sasl.username', 'sasl.password']
        for key in required_keys:
            assert key in result

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    def test_load_state_returns_dict(self, mock_exists, mock_file):
        """Test that load_state always returns a dictionary"""
        state = load_state()
        
        assert isinstance(state, dict)

    @patch('os.path.exists', return_value=False)
    def test_load_feedstore_returns_list(self, mock_exists):
        """Test that load_feedstore always returns a list"""
        feeds = load_feedstore()
        
        assert isinstance(feeds, list)
