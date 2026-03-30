"""Unit tests for UK EA Flood Monitoring data poller - no external dependencies."""

import pytest
from uk_ea_flood_monitoring.uk_ea_flood_monitoring import EAFloodMonitoringAPI


@pytest.mark.unit
class TestEAFloodMonitoringAPIInitialization:
    """Test EAFloodMonitoringAPI class initialization."""

    def test_init_creates_session(self):
        """Test that initialization creates a requests session."""
        api = EAFloodMonitoringAPI()
        assert api.session is not None
        assert hasattr(api.session, 'get')

    def test_init_creates_empty_measure_map(self):
        """Test that initialization creates an empty measure_to_station map."""
        api = EAFloodMonitoringAPI()
        assert api.measure_to_station == {}
        assert isinstance(api.measure_to_station, dict)


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing for Event Hubs/Kafka."""

    def test_parse_event_hubs_connection_string(self):
        """Test parsing a valid Event Hubs connection string."""
        api = EAFloodMonitoringAPI()
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
        api = EAFloodMonitoringAPI()
        connection_string = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic1"
        result = api.parse_connection_string(connection_string)

        assert 'test.servicebus.windows.net:9093' == result['bootstrap.servers']
        assert 'sb://' not in result['bootstrap.servers']

    def test_parse_connection_string_extracts_entity_path(self):
        """Test that entity path is correctly extracted as topic."""
        api = EAFloodMonitoringAPI()
        connection_string = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=mytopic"
        result = api.parse_connection_string(connection_string)

        assert result['kafka_topic'] == 'mytopic'

    def test_parse_connection_string_sets_sasl_credentials(self):
        """Test that SASL credentials are correctly set when SharedAccessKeyName is present."""
        api = EAFloodMonitoringAPI()
        connection_string = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=MyPolicy;SharedAccessKey=abc123;EntityPath=topic"
        result = api.parse_connection_string(connection_string)

        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == connection_string.strip()
        assert result['security.protocol'] == 'SASL_SSL'
        assert result['sasl.mechanism'] == 'PLAIN'

    def test_parse_connection_string_without_sasl(self):
        """Test that plain connection string without SharedAccessKeyName has no SASL config."""
        api = EAFloodMonitoringAPI()
        connection_string = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = api.parse_connection_string(connection_string)

        assert 'sasl.username' not in result
        assert 'security.protocol' not in result

    def test_parse_connection_string_with_whitespace(self):
        """Test parsing connection string with extra whitespace."""
        api = EAFloodMonitoringAPI()
        connection_string = "  Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic  "
        result = api.parse_connection_string(connection_string)

        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'topic'

    def test_parse_connection_string_invalid_format_raises_error(self):
        """Test that invalid connection string format raises ValueError."""
        api = EAFloodMonitoringAPI()
        invalid_connection_string = "EndpointWithoutEquals;EntityPathAlsoInvalid"

        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string(invalid_connection_string)


@pytest.mark.unit
class TestMeasureMap:
    """Test measure URI to station reference mapping."""

    def test_build_measure_map_single_station(self):
        """Test building measure map with a single station."""
        api = EAFloodMonitoringAPI()
        stations = [
            {
                "stationReference": "1029TH",
                "notation": "1029TH",
                "measures": [
                    {
                        "@id": "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD",
                        "parameter": "level"
                    }
                ]
            }
        ]
        result = api.build_measure_map(stations)
        assert "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD" in result
        assert result["http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD"] == "1029TH"

    def test_build_measure_map_multiple_measures(self):
        """Test building measure map with multiple measures per station."""
        api = EAFloodMonitoringAPI()
        stations = [
            {
                "stationReference": "1029TH",
                "notation": "1029TH",
                "measures": [
                    {"@id": "measure-1", "parameter": "level"},
                    {"@id": "measure-2", "parameter": "flow"}
                ]
            }
        ]
        result = api.build_measure_map(stations)
        assert len(result) == 2
        assert result["measure-1"] == "1029TH"
        assert result["measure-2"] == "1029TH"

    def test_build_measure_map_multiple_stations(self):
        """Test building measure map with multiple stations."""
        api = EAFloodMonitoringAPI()
        stations = [
            {
                "stationReference": "STATION1",
                "measures": [{"@id": "m1"}]
            },
            {
                "stationReference": "STATION2",
                "measures": [{"@id": "m2"}]
            }
        ]
        result = api.build_measure_map(stations)
        assert result["m1"] == "STATION1"
        assert result["m2"] == "STATION2"

    def test_build_measure_map_empty(self):
        """Test building measure map with no stations."""
        api = EAFloodMonitoringAPI()
        result = api.build_measure_map([])
        assert result == {}

    def test_build_measure_map_no_measures(self):
        """Test building measure map with station without measures."""
        api = EAFloodMonitoringAPI()
        stations = [{"stationReference": "STATION1"}]
        result = api.build_measure_map(stations)
        assert result == {}


@pytest.mark.unit
class TestAPIConstants:
    """Test API endpoint constants."""

    def test_stations_url_uses_https(self):
        """Test that stations URL uses HTTPS."""
        api = EAFloodMonitoringAPI()
        assert api.STATIONS_URL.startswith("https://")

    def test_readings_url_uses_https(self):
        """Test that readings URL uses HTTPS."""
        api = EAFloodMonitoringAPI()
        assert api.READINGS_URL.startswith("https://")

    def test_poll_interval_default(self):
        """Test default poll interval is 15 minutes."""
        assert EAFloodMonitoringAPI.POLL_INTERVAL_SECONDS == 900

    def test_api_has_required_methods(self):
        """Test that API has all required public methods."""
        api = EAFloodMonitoringAPI()
        assert hasattr(api, 'list_stations')
        assert hasattr(api, 'get_latest_readings')
        assert hasattr(api, 'build_measure_map')
        assert hasattr(api, 'parse_connection_string')
        assert hasattr(api, 'feed_stations')
