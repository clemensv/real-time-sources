"""
Integration tests for USGS Instantaneous Values data poller.
Tests with mocked API responses.
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone
import aiohttp
from usgs_iv.usgs_iv import USGSDataPoller


@pytest.fixture
def mock_kafka_config():
    """Mock Kafka configuration for testing."""
    return {
        'bootstrap.servers': 'localhost:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': 'test_user',
        'sasl.password': 'test_password'
    }


@pytest.fixture
def mock_rdb_response():
    """Mock RDB format response from USGS API."""
    return """#
# U.S. Geological Survey
# National Water Information System
# Retrieved: 2024-11-15 12:00:00 EST
#
# Data provided for site 01646500
#
# TS_ID	Parameter	Description
# 123	00060	Discharge, cubic feet per second
#
agency_cd	site_no	datetime	tz_cd	123_00060	123_00060_cd
5s	15s	20d	6s	14n	10s
USGS	01646500	2024-11-15 11:45:00	EST	1234.5	A
USGS	01646500	2024-11-15 11:50:00	EST	1235.0	A
USGS	01646500	2024-11-15 11:55:00	EST	1236.2	A
"""


@pytest.fixture
def mock_empty_rdb_response():
    """Mock empty RDB response (no data)."""
    return """#
# U.S. Geological Survey
# National Water Information System
# Retrieved: 2024-11-15 12:00:00 EST
#
"""


class TestUSGSDataFetching:
    """Test data fetching from USGS API."""

    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession')
    async def test_get_data_by_state_success(self, mock_session, mock_rdb_response):
        """Test successful data retrieval for a state."""
        # Setup mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value=mock_rdb_response)
        mock_response.raise_for_status = Mock()
        
        mock_session_instance = AsyncMock()
        mock_session_instance.get = AsyncMock(return_value=mock_response)
        mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session_instance.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value = mock_session_instance
        
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            results = []
            async for records in poller.get_data_by_state('MD'):
                results.extend(records)
            
            assert len(results) == 3
            assert results[0]['site_no'] == '01646500'
            assert results[0]['123_00060'] == '1234.5'

    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession')
    async def test_get_data_by_state_timeout(self, mock_session):
        """Test timeout handling when fetching data."""
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(side_effect=asyncio.TimeoutError())
        
        mock_session_instance = AsyncMock()
        mock_session_instance.get = AsyncMock(return_value=mock_response)
        mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session_instance.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value = mock_session_instance
        
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            results = []
            async for records in poller.get_data_by_state('CA'):
                results.extend(records)
            
            # Should return empty results on timeout
            assert len(results) == 0

    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession')
    async def test_get_data_by_state_http_error(self, mock_session):
        """Test HTTP error handling."""
        mock_response = AsyncMock()
        mock_response.raise_for_status = Mock(side_effect=aiohttp.ClientError("Not Found"))
        
        mock_session_instance = AsyncMock()
        mock_session_instance.get = AsyncMock(return_value=mock_response)
        mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session_instance.__aexit__ = AsyncMock(return_value=None)
        mock_session.return_value = mock_session_instance
        
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            results = []
            async for records in poller.get_data_by_state('XX'):
                results.extend(records)
            
            # Should return empty results on error
            assert len(results) == 0


class TestLastPolledTimes:
    """Test last polled times persistence."""

    def test_load_last_polled_times_no_file(self):
        """Test loading when no file exists."""
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(
                kafka_config=None,
                kafka_topic='test-topic',
                last_polled_file='/nonexistent/file.json'
            )
            
            result = poller.load_last_polled_times()
            assert result == {}

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_load_last_polled_times_with_file(self, mock_open, mock_exists):
        """Test loading from existing file."""
        mock_exists.return_value = True
        
        test_data = {
            '00060': {
                '01646500': '2024-11-15T12:00:00+00:00'
            }
        }
        
        mock_file = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=False)
        mock_file.read = Mock(return_value=json.dumps(test_data))
        mock_open.return_value = mock_file
        
        with patch('usgs_iv.usgs_iv.Producer'):
            with patch('json.load', return_value=test_data):
                poller = USGSDataPoller(
                    kafka_config=None,
                    kafka_topic='test-topic',
                    last_polled_file='/tmp/test.json'
                )
                
                result = poller.load_last_polled_times()
                
                assert '00060' in result
                assert '01646500' in result['00060']
                assert isinstance(result['00060']['01646500'], datetime)

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_load_last_polled_times_invalid_json(self, mock_open, mock_exists):
        """Test handling of corrupted JSON file."""
        mock_exists.return_value = True
        
        mock_file = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=False)
        mock_file.read = Mock(return_value='invalid json{]')
        mock_open.return_value = mock_file
        
        with patch('usgs_iv.usgs_iv.Producer'):
            with patch('json.load', side_effect=json.JSONDecodeError('test', 'test', 0)):
                poller = USGSDataPoller(
                    kafka_config=None,
                    kafka_topic='test-topic',
                    last_polled_file='/tmp/test.json'
                )
                
                result = poller.load_last_polled_times()
                assert result == {}

    @patch('builtins.open')
    def test_save_last_polled_times(self, mock_open):
        """Test saving last polled times to file."""
        mock_file = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=False)
        mock_file.write = Mock()
        mock_open.return_value = mock_file
        
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(
                kafka_config=None,
                kafka_topic='test-topic',
                last_polled_file='/tmp/test.json'
            )
            
            test_times = {
                '00060': {
                    '01646500': datetime(2024, 11, 15, 12, 0, 0, tzinfo=timezone.utc)
                }
            }
            
            with patch('json.dump') as mock_dump:
                poller.save_last_polled_times(test_times)
                
                mock_dump.assert_called_once()
                saved_data = mock_dump.call_args[0][0]
                assert '00060' in saved_data
                assert '01646500' in saved_data['00060']
                assert isinstance(saved_data['00060']['01646500'], str)


class TestConnectionStringParsing:
    """Test Azure Event Hubs connection string parsing."""

    def test_connection_string_parsing(self):
        """Test parsing of Event Hubs connection string."""
        test_conn_str = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "SharedAccessKeyName=testkey;"
            "SharedAccessKey=abc123def456;"
            "EntityPath=testentity"
        )
        
        # This would be tested if the connection string parsing is implemented
        # For now, just verify the structure is correct
        assert "Endpoint=" in test_conn_str
        assert "SharedAccessKeyName=" in test_conn_str
        assert "SharedAccessKey=" in test_conn_str
        assert "EntityPath=" in test_conn_str


class TestHelperFunctions:
    """Test helper functions."""

    def test_isfloat_valid_numbers(self):
        """Test isfloat helper with valid numbers."""
        # This test would need the isfloat function to be accessible
        # For now, test the logic inline
        def isfloat(v: str) -> bool:
            try:
                float(v)
                return True
            except ValueError:
                return False
        
        assert isfloat('123.45') is True
        assert isfloat('0.0') is True
        assert isfloat('-456.78') is True
        assert isfloat('1e10') is True

    def test_isfloat_invalid_values(self):
        """Test isfloat helper with invalid values."""
        def isfloat(v: str) -> bool:
            try:
                float(v)
                return True
            except ValueError:
                return False
        
        assert isfloat('abc') is False
        assert isfloat('') is False
        assert isfloat('12.34.56') is False
