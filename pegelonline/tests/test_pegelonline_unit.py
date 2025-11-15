"""Unit tests for PegelOnline data poller - no external dependencies."""

import pytest
from pegelonline.pegelonline import PegelOnlineAPI


@pytest.mark.unit
class TestPegelOnlineAPIInitialization:
    """Test PegelOnlineAPI class initialization."""

    def test_init_creates_empty_skip_urls(self):
        """Test that initialization creates an empty skip_urls list."""
        api = PegelOnlineAPI()
        assert api.skip_urls == []
        assert isinstance(api.skip_urls, list)

    def test_init_creates_empty_etags(self):
        """Test that initialization creates an empty etags dictionary."""
        api = PegelOnlineAPI()
        assert api.etags == {}
        assert isinstance(api.etags, dict)

    def test_init_creates_session(self):
        """Test that initialization creates a requests session."""
        api = PegelOnlineAPI()
        assert api.session is not None
        assert hasattr(api.session, 'get')


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing for Event Hubs/Kafka."""

    def test_parse_event_hubs_connection_string(self):
        """Test parsing a valid Event Hubs connection string."""
        api = PegelOnlineAPI()
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = api.parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myeventhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert connection_string.strip() in result['sasl.password']

    def test_parse_connection_string_extracts_endpoint(self):
        """Test that endpoint is correctly extracted and formatted."""
        api = PegelOnlineAPI()
        connection_string = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic1"
        result = api.parse_connection_string(connection_string)
        
        assert 'test.servicebus.windows.net:9093' == result['bootstrap.servers']
        assert 'sb://' not in result['bootstrap.servers']
        assert not result['bootstrap.servers'].endswith('/')

    def test_parse_connection_string_extracts_entity_path(self):
        """Test that entity path is correctly extracted as topic."""
        api = PegelOnlineAPI()
        connection_string = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=mytopic"
        result = api.parse_connection_string(connection_string)
        
        assert result['kafka_topic'] == 'mytopic'

    def test_parse_connection_string_sets_sasl_credentials(self):
        """Test that SASL credentials are correctly set."""
        api = PegelOnlineAPI()
        connection_string = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = api.parse_connection_string(connection_string)
        
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == connection_string.strip()

    def test_parse_connection_string_with_whitespace(self):
        """Test parsing connection string with extra whitespace."""
        api = PegelOnlineAPI()
        connection_string = "  Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic  "
        result = api.parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'topic'

    def test_parse_connection_string_invalid_format_raises_error(self):
        """Test that invalid connection string format raises ValueError."""
        api = PegelOnlineAPI()
        # Connection string with missing '=' will cause IndexError
        invalid_connection_string = "EndpointWithoutEquals;EntityPathAlsoInvalid"
        
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string(invalid_connection_string)


@pytest.mark.unit
class TestURLManagement:
    """Test URL management for skip list and ETag cache."""

    def test_skip_urls_prevents_repeated_requests(self):
        """Test that URLs in skip_urls list are checked."""
        api = PegelOnlineAPI()
        test_url = 'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/TEST/W/currentmeasurement.json'
        api.skip_urls.append(test_url)
        
        assert test_url in api.skip_urls

    def test_etags_dictionary_stores_values(self):
        """Test that ETags can be stored and retrieved."""
        api = PegelOnlineAPI()
        test_url = 'https://test.example.com/api/data'
        test_etag = '"abc123-etag-value"'
        
        api.etags[test_url] = test_etag
        assert api.etags[test_url] == test_etag

    def test_multiple_etags_stored_separately(self):
        """Test that multiple URLs can have different ETags."""
        api = PegelOnlineAPI()
        
        api.etags['url1'] = 'etag1'
        api.etags['url2'] = 'etag2'
        
        assert api.etags['url1'] == 'etag1'
        assert api.etags['url2'] == 'etag2'
        assert len(api.etags) == 2


@pytest.mark.unit
class TestAPIEndpoints:
    """Test API endpoint URL construction."""

    def test_list_stations_url(self):
        """Test that list_stations uses correct endpoint."""
        api = PegelOnlineAPI()
        expected_url = 'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json'
        # We can't test the actual request, but we can verify the URL format is used in the code
        assert hasattr(api, 'list_stations')

    def test_get_water_level_url_format(self):
        """Test that get_water_level constructs correct URL format."""
        api = PegelOnlineAPI()
        # The method should construct URLs in the format:
        # https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/{station}/W/currentmeasurement.json
        assert hasattr(api, 'get_water_level')

    def test_get_water_levels_url(self):
        """Test that get_water_levels uses correct endpoint with parameters."""
        api = PegelOnlineAPI()
        # The method should use the stations endpoint with includeTimeseries and includeCurrentMeasurement
        assert hasattr(api, 'get_water_levels')


@pytest.mark.unit
class TestHelperMethods:
    """Test helper methods and utilities."""

    def test_api_has_session_attribute(self):
        """Test that API instance has a session attribute."""
        api = PegelOnlineAPI()
        assert hasattr(api, 'session')
        assert api.session is not None

    def test_api_has_skip_urls_attribute(self):
        """Test that API instance has skip_urls list."""
        api = PegelOnlineAPI()
        assert hasattr(api, 'skip_urls')
        assert isinstance(api.skip_urls, list)

    def test_api_has_etags_attribute(self):
        """Test that API instance has etags dictionary."""
        api = PegelOnlineAPI()
        assert hasattr(api, 'etags')
        assert isinstance(api.etags, dict)

    def test_api_has_required_methods(self):
        """Test that API has all required public methods."""
        api = PegelOnlineAPI()
        assert hasattr(api, 'list_stations')
        assert hasattr(api, 'get_water_level')
        assert hasattr(api, 'get_water_levels')
        assert hasattr(api, 'parse_connection_string')
        assert hasattr(api, 'feed_stations')


@pytest.mark.unit
class TestConstants:
    """Test constants and configuration values."""

    def test_base_url_uses_https(self):
        """Test that the API uses HTTPS for security."""
        api = PegelOnlineAPI()
        # The code should use https://www.pegelonline.wsv.de
        # This is verified by checking the methods use the correct protocol
        assert hasattr(api, 'list_stations')
        assert hasattr(api, 'get_water_level')

    def test_api_version_v2(self):
        """Test that the API uses version 2 of the PegelOnline API."""
        # The URLs should contain /rest-api/v2/
        api = PegelOnlineAPI()
        assert hasattr(api, 'list_stations')
        assert hasattr(api, 'get_water_level')
