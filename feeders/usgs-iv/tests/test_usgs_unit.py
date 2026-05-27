"""
Unit tests for USGS Instantaneous Values data poller.
Tests that don't require external dependencies or API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
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


class TestUSGSDataPoller:
    """Test suite for USGSDataPoller initialization and configuration."""

    @patch('usgs_iv.usgs_iv.USGSSitesEventProducer')
    @patch('usgs_iv.usgs_iv.USGSInstantaneousValuesEventProducer')
    @patch('usgs_iv.usgs_iv.Producer')
    def test_init_with_kafka_config(self, mock_producer_class, mock_values_producer, mock_site_producer, mock_kafka_config):
        """Test USGSDataPoller initialization with Kafka configuration."""
        mock_producer_instance = Mock()
        mock_producer_class.return_value = mock_producer_instance
        
        poller = USGSDataPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='/tmp/test_last_polled.json',
            state='NY'
        )
        
        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == '/tmp/test_last_polled.json'
        assert poller.state == 'NY'
        assert poller.force_site_refresh is False
        assert poller.force_data_refresh is False
        
        mock_producer_class.assert_called_once_with(mock_kafka_config)
        mock_site_producer.assert_called_once_with(mock_producer_instance, 'test-topic')
        mock_values_producer.assert_called_once_with(mock_producer_instance, 'test-topic')

    def test_init_without_kafka_config(self):
        """Test USGSDataPoller initialization without Kafka configuration."""
        poller = USGSDataPoller(
            kafka_config=None,
            kafka_topic='test-topic',
            last_polled_file='/tmp/test_last_polled.json',
            state='CA'
        )
        
        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == '/tmp/test_last_polled.json'
        assert poller.state == 'CA'

    def test_init_with_force_flags(self, mock_kafka_config):
        """Test USGSDataPoller initialization with force refresh flags."""
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(
                kafka_config=mock_kafka_config,
                kafka_topic='test-topic',
                force_site_refresh=True,
                force_data_refresh=True
            )
            
            assert poller.force_site_refresh is True
            assert poller.force_data_refresh is True


class TestParameterMapping:
    """Test parameter code mapping to data types."""

    def test_parameters_dict_structure(self):
        """Test that PARAMETERS dict is properly structured."""
        assert hasattr(USGSDataPoller, 'PARAMETERS')
        assert isinstance(USGSDataPoller.PARAMETERS, dict)
        
        # Test a few key parameter codes
        assert USGSDataPoller.PARAMETERS['00060'] == 'Streamflow'
        assert USGSDataPoller.PARAMETERS['00065'] == 'GageHeight'
        assert USGSDataPoller.PARAMETERS['00010'] == 'WaterTemperature'
        assert USGSDataPoller.PARAMETERS['00045'] == 'Precipitation'

    def test_all_parameters_are_strings(self):
        """Test that all parameter codes and names are strings."""
        for code, name in USGSDataPoller.PARAMETERS.items():
            assert isinstance(code, str)
            assert isinstance(name, str)
            assert len(code) == 5  # USGS parameter codes are 5 digits


class TestTimezoneMapping:
    """Test USGS timezone abbreviation mapping."""

    def test_usgs_timezone_map_exists(self):
        """Test that timezone mapping dictionary exists."""
        from usgs_iv.usgs_iv import usgs_tz_map
        
        assert isinstance(usgs_tz_map, dict)
        assert len(usgs_tz_map) > 0

    def test_common_timezones_mapped(self):
        """Test that common US timezones are properly mapped."""
        from usgs_iv.usgs_iv import usgs_tz_map
        
        # Test Eastern
        assert usgs_tz_map['EST'] == 'America/New_York'
        assert usgs_tz_map['EDT'] == 'America/New_York'
        
        # Test Central
        assert usgs_tz_map['CST'] == 'America/Chicago'
        assert usgs_tz_map['CDT'] == 'America/Chicago'
        
        # Test Mountain
        assert usgs_tz_map['MST'] == 'America/Denver'
        assert usgs_tz_map['MDT'] == 'America/Denver'
        
        # Test Pacific
        assert usgs_tz_map['PST'] == 'America/Los_Angeles'
        assert usgs_tz_map['PDT'] == 'America/Los_Angeles'

    def test_special_timezones_mapped(self):
        """Test that special US territory timezones are mapped."""
        from usgs_iv.usgs_iv import usgs_tz_map
        
        assert usgs_tz_map['AKST'] == 'America/Anchorage'
        assert usgs_tz_map['HST'] == 'Pacific/Honolulu'
        assert usgs_tz_map['AST'] == 'America/Puerto_Rico'
        assert usgs_tz_map['ChST'] == 'Pacific/Guam'


class TestStateCodesList:
    """Test state codes configuration."""

    def test_state_codes_list_exists(self):
        """Test that state codes list exists and is properly structured."""
        from usgs_iv.usgs_iv import state_codes
        
        assert isinstance(state_codes, list)
        assert len(state_codes) > 50  # All 50 states plus territories

    def test_common_states_present(self):
        """Test that common state codes are present."""
        from usgs_iv.usgs_iv import state_codes
        
        assert 'CA' in state_codes
        assert 'NY' in state_codes
        assert 'TX' in state_codes
        assert 'FL' in state_codes
        assert 'WA' in state_codes

    def test_territories_present(self):
        """Test that US territories are present."""
        from usgs_iv.usgs_iv import state_codes
        
        assert 'PR' in state_codes  # Puerto Rico
        assert 'GU' in state_codes  # Guam
        assert 'VI' in state_codes  # Virgin Islands

    def test_all_codes_uppercase(self):
        """Test that all state codes are uppercase."""
        from usgs_iv.usgs_iv import state_codes
        
        for code in state_codes:
            assert code.isupper()
            assert len(code) == 2


class TestBaseURL:
    """Test USGS API base URL configuration."""

    def test_base_url_exists(self):
        """Test that BASE_URL is properly defined."""
        assert hasattr(USGSDataPoller, 'BASE_URL')
        assert USGSDataPoller.BASE_URL == "https://waterservices.usgs.gov/nwis/iv/"

    def test_base_url_is_https(self):
        """Test that BASE_URL uses HTTPS."""
        assert USGSDataPoller.BASE_URL.startswith('https://')


class TestRegexPatterns:
    """Test regex patterns used in the data poller."""

    def test_ts_param_regex_exists(self):
        """Test that TS_PARAM_REGEX pattern exists."""
        assert hasattr(USGSDataPoller, 'TS_PARAM_REGEX')

    def test_ts_param_regex_matches_valid_patterns(self):
        """Test that TS_PARAM_REGEX matches valid timeseries parameter codes."""
        import re
        pattern = USGSDataPoller.TS_PARAM_REGEX
        
        # Valid patterns: {ts_id}_{parameter_code}
        assert pattern.match('1_00060') is not None
        assert pattern.match('12_00065') is not None
        assert pattern.match('123_00010') is not None

    def test_ts_param_regex_rejects_invalid_patterns(self):
        """Test that TS_PARAM_REGEX rejects invalid patterns."""
        import re
        pattern = USGSDataPoller.TS_PARAM_REGEX
        
        assert pattern.match('invalid') is None
        assert pattern.match('_00060') is None
        assert pattern.match('1_') is None
        assert pattern.match('1_123') is None  # parameter code must be 5 digits
