"""
Unit tests for GTFS Bridge functionality.
Tests core functions without external dependencies.
"""

import pytest
import os
import hashlib
import json
from unittest.mock import Mock, patch, mock_open
from datetime import datetime, timedelta
from gtfs_rt_bridge.gtfs_cli import (
    parse_connection_string,
    calculate_file_hashes,
    read_file_hashes,
    write_file_hashes,
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
            "EntityPath=gtfs-events"
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'gtfs-events'
        assert result['sasl.username'] == '$ConnectionString'
        assert connection_string.strip() in result['sasl.password']

    def test_parse_connection_string_strips_whitespace(self):
        """Test that connection string parsing handles whitespace"""
        connection_string = (
            "  Endpoint=sb://test.servicebus.windows.net/;  "
            "EntityPath=gtfs-events  "
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'gtfs-events'

    def test_parse_connection_string_with_quotes(self):
        """Test parsing connection string with quoted values"""
        connection_string = (
            'Endpoint="sb://test.servicebus.windows.net/";'
            'EntityPath="gtfs-events"'
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'gtfs-events'

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
class TestFileHashCalculation:
    """Tests for schedule file hash calculation"""

    @patch('gtfs_rt_bridge.gtfs_cli.ZipFile')
    def test_calculate_file_hashes_processes_txt_files(self, mock_zipfile):
        """Test that only .txt files are hashed"""
        mock_zip = Mock()
        mock_zip.namelist.return_value = ['agency.txt', 'routes.txt', 'readme.md', 'image.png']
        mock_zip.open.return_value.__enter__ = Mock(return_value=Mock(read=Mock(return_value=b'test content')))
        mock_zip.open.return_value.__exit__ = Mock(return_value=False)
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        result = calculate_file_hashes('/path/to/schedule.zip')
        
        assert 'agency.txt' in result
        assert 'routes.txt' in result
        assert 'readme.md' not in result
        assert 'image.png' not in result

    @patch('gtfs_rt_bridge.gtfs_cli.ZipFile')
    def test_calculate_file_hashes_computes_sha256(self, mock_zipfile):
        """Test that SHA-256 hashes are computed correctly"""
        test_content = b'test content for hashing'
        expected_hash = hashlib.sha256(test_content).hexdigest()
        
        mock_zip = Mock()
        mock_zip.namelist.return_value = ['test.txt']
        mock_zip.open.return_value.__enter__ = Mock(return_value=Mock(read=Mock(return_value=test_content)))
        mock_zip.open.return_value.__exit__ = Mock(return_value=False)
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        result = calculate_file_hashes('/path/to/schedule.zip')
        
        assert result['test.txt'] == expected_hash

    @patch('gtfs_rt_bridge.gtfs_cli.ZipFile')
    def test_calculate_file_hashes_handles_empty_zip(self, mock_zipfile):
        """Test handling of empty schedule file"""
        mock_zip = Mock()
        mock_zip.namelist.return_value = []
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        result = calculate_file_hashes('/path/to/empty.zip')
        
        assert result == {}


@pytest.mark.unit
class TestFileHashStorage:
    """Tests for file hash reading and writing"""

    @patch('builtins.open', new_callable=mock_open, read_data='{"agency.txt": "abc123"}')
    @patch('os.path.exists', return_value=True)
    def test_read_file_hashes_loads_existing_hashes(self, mock_exists, mock_file):
        """Test reading existing hash file"""
        result = read_file_hashes('/path/to/schedule.zip', None)
        
        assert result == {"agency.txt": "abc123"}

    @patch('os.path.exists', return_value=False)
    def test_read_file_hashes_returns_empty_dict_if_not_exists(self, mock_exists):
        """Test that missing hash file returns empty dict"""
        result = read_file_hashes('/path/to/schedule.zip', None)
        
        assert result == {}

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.expanduser', return_value='/home/user')
    def test_write_file_hashes_creates_json_file(self, mock_expanduser, mock_file):
        """Test writing hashes to JSON file"""
        hashes = {"agency.txt": "abc123", "routes.txt": "def456"}
        
        write_file_hashes('schedule.zip', hashes, None)
        
        mock_file.assert_called()
        handle = mock_file()
        # Check that json.dump was called (indirectly through write calls)
        assert handle.write.called

    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_hashes_uses_custom_cache_dir(self, mock_file):
        """Test that custom cache directory is used"""
        hashes = {"agency.txt": "abc123"}
        cache_dir = '/custom/cache'
        
        write_file_hashes('schedule.zip', hashes, cache_dir)
        
        # Verify the file was opened with the custom cache directory path
        call_args = mock_file.call_args[0][0]
        assert cache_dir in call_args


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
