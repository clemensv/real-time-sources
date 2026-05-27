"""Unit tests for Nepal BIPAD Hydrology bridge - no external dependencies."""

import pytest
from nepal_bipad_hydrology.nepal_bipad_hydrology import NepalBipadHydrologyAPI, _load_state, _save_state


@pytest.mark.unit
class TestAPIInitialization:
    """Test NepalBipadHydrologyAPI class initialization."""

    def test_init_default_base_url(self):
        api = NepalBipadHydrologyAPI()
        assert api.base_url == "https://bipadportal.gov.np/api/v1"

    def test_init_custom_base_url(self):
        api = NepalBipadHydrologyAPI(base_url="https://example.com/api/v1/")
        assert api.base_url == "https://example.com/api/v1"

    def test_init_default_page_size(self):
        api = NepalBipadHydrologyAPI()
        assert api.page_size == 100

    def test_init_custom_page_size(self):
        api = NepalBipadHydrologyAPI(page_size=50)
        assert api.page_size == 50

    def test_init_creates_session(self):
        api = NepalBipadHydrologyAPI()
        assert api.session is not None
        assert hasattr(api.session, 'get')


@pytest.mark.unit
class TestConnectionStringParsing:
    """Test connection string parsing for Event Hubs/Kafka."""

    def test_parse_event_hubs_connection_string(self):
        api = NepalBipadHydrologyAPI()
        cs = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = api.parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myeventhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert cs.strip() in result['sasl.password']

    def test_parse_connection_string_extracts_endpoint(self):
        api = NepalBipadHydrologyAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic1"
        result = api.parse_connection_string(cs)
        assert 'test.servicebus.windows.net:9093' == result['bootstrap.servers']

    def test_parse_connection_string_extracts_entity_path(self):
        api = NepalBipadHydrologyAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=mytopic"
        result = api.parse_connection_string(cs)
        assert result['kafka_topic'] == 'mytopic'

    def test_parse_connection_string_sets_sasl(self):
        api = NepalBipadHydrologyAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=MyPolicy;SharedAccessKey=abc123;EntityPath=topic"
        result = api.parse_connection_string(cs)
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == cs.strip()
        assert result['security.protocol'] == 'SASL_SSL'

    def test_parse_connection_string_without_sasl(self):
        api = NepalBipadHydrologyAPI()
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = api.parse_connection_string(cs)
        assert 'sasl.username' not in result

    def test_parse_bootstrap_server_style(self):
        api = NepalBipadHydrologyAPI()
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = api.parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'

    def test_parse_connection_string_invalid_raises_error(self):
        api = NepalBipadHydrologyAPI()
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string("EndpointWithoutEquals;EntityPathAlsoInvalid")


@pytest.mark.unit
class TestParseStation:
    """Test station record parsing and normalization."""

    def test_parse_station_basic(self):
        raw = {
            "id": 3,
            "title": "Babai at Chepang",
            "basin": "Babai",
            "point": {"type": "Point", "coordinates": [81.7135456, 28.3565601]},
            "waterLevel": 1.944,
            "dangerLevel": 6.8,
            "warningLevel": 5.5,
            "waterLevelOn": "2024-01-15T12:00:00+05:45",
            "status": "BELOW WARNING LEVEL",
            "elevation": 308,
            "steady": "STEADY",
            "description": "Old Station at 28.353056",
            "stationSeriesId": 649,
            "dataSource": "hydrology.gov.np",
            "ward": 4870,
            "municipality": 58002,
            "district": 65,
            "province": 5,
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert parsed["station_id"] == "3"
        assert parsed["title"] == "Babai at Chepang"
        assert parsed["basin"] == "Babai"
        assert parsed["latitude"] == pytest.approx(28.3565601)
        assert parsed["longitude"] == pytest.approx(81.7135456)
        assert parsed["elevation"] == 308
        assert parsed["danger_level"] == 6.8
        assert parsed["warning_level"] == 5.5
        assert parsed["data_source"] == "hydrology.gov.np"
        assert parsed["province"] == 5
        assert parsed["district"] == 65
        assert parsed["municipality"] == 58002
        assert parsed["ward"] == 4870

    def test_parse_station_null_elevation(self):
        raw = {
            "id": 162,
            "title": "Marin River",
            "basin": "Bagmati",
            "point": {"type": "Point", "coordinates": [85.5091, 27.225]},
            "elevation": None,
            "dangerLevel": 5.1,
            "warningLevel": 4.5,
            "dataSource": "hydrology.gov.np",
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert parsed["elevation"] is None

    def test_parse_station_null_danger_warning(self):
        raw = {
            "id": 100,
            "title": "Test Station",
            "basin": "Koshi",
            "point": {"type": "Point", "coordinates": [86.0, 27.0]},
            "dangerLevel": None,
            "warningLevel": None,
            "dataSource": "hydrology.gov.np",
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert parsed["danger_level"] is None
        assert parsed["warning_level"] is None

    def test_parse_station_null_admin_codes(self):
        raw = {
            "id": 200,
            "title": "Remote Station",
            "basin": "Karnali",
            "point": {"type": "Point", "coordinates": [81.0, 29.0]},
            "dataSource": "hydrology.gov.np",
            "province": None,
            "district": None,
            "municipality": None,
            "ward": None,
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert parsed["province"] is None
        assert parsed["district"] is None
        assert parsed["municipality"] is None
        assert parsed["ward"] is None

    def test_parse_station_missing_point(self):
        raw = {
            "id": 50,
            "title": "No Point",
            "basin": "Test",
            "point": None,
            "dataSource": "hydrology.gov.np",
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert parsed["latitude"] == 0.0
        assert parsed["longitude"] == 0.0

    def test_parse_station_empty_coordinates(self):
        raw = {
            "id": 51,
            "title": "Empty Coords",
            "basin": "Test",
            "point": {"type": "Point", "coordinates": []},
            "dataSource": "hydrology.gov.np",
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert parsed["latitude"] == 0.0
        assert parsed["longitude"] == 0.0

    def test_parse_station_id_as_string(self):
        raw = {
            "id": 42,
            "title": "Station 42",
            "basin": "Narayani",
            "point": {"type": "Point", "coordinates": [84.0, 27.5]},
            "dataSource": "hydrology.gov.np",
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert isinstance(parsed["station_id"], str)
        assert parsed["station_id"] == "42"

    def test_parse_station_null_description(self):
        raw = {
            "id": 60,
            "title": "Desc Test",
            "basin": "Bagmati",
            "point": {"type": "Point", "coordinates": [85.0, 27.0]},
            "description": None,
            "dataSource": "hydrology.gov.np",
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        assert parsed["description"] is None


@pytest.mark.unit
class TestParseReading:
    """Test water level reading parsing and normalization."""

    def test_parse_reading_basic(self):
        raw = {
            "id": 3,
            "title": "Babai at Chepang",
            "basin": "Babai",
            "waterLevel": 1.944,
            "dangerLevel": 6.8,
            "warningLevel": 5.5,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2024-01-15T12:00:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert parsed["station_id"] == "3"
        assert parsed["water_level"] == pytest.approx(1.944)
        assert parsed["danger_level"] == 6.8
        assert parsed["warning_level"] == 5.5
        assert parsed["status"] == "BELOW WARNING LEVEL"
        assert parsed["trend"] == "STEADY"
        assert parsed["water_level_on"] == "2024-01-15T12:00:00+05:45"

    def test_parse_reading_null_water_level(self):
        raw = {
            "id": 162,
            "title": "Marin River",
            "basin": "Bagmati",
            "waterLevel": None,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2021-07-14T07:40:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert parsed["water_level"] is None

    def test_parse_reading_null_danger_warning(self):
        raw = {
            "id": 10,
            "title": "Test",
            "basin": "Koshi",
            "waterLevel": 2.5,
            "dangerLevel": None,
            "warningLevel": None,
            "status": "BELOW WARNING LEVEL",
            "steady": "RISING",
            "waterLevelOn": "2024-06-01T10:00:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert parsed["danger_level"] is None
        assert parsed["warning_level"] is None

    def test_parse_reading_rising_trend(self):
        raw = {
            "id": 5,
            "title": "Rising Station",
            "basin": "Narayani",
            "waterLevel": 5.0,
            "status": "WARNING",
            "steady": "RISING",
            "waterLevelOn": "2024-07-01T08:00:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert parsed["trend"] == "RISING"
        assert parsed["status"] == "WARNING"

    def test_parse_reading_danger_status(self):
        raw = {
            "id": 7,
            "title": "Danger Station",
            "basin": "Karnali",
            "waterLevel": 10.0,
            "status": "DANGER",
            "steady": "FALLING",
            "waterLevelOn": "2024-08-01T12:00:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert parsed["status"] == "DANGER"
        assert parsed["trend"] == "FALLING"

    def test_parse_reading_maps_field_names(self):
        """Verify upstream camelCase is mapped to snake_case."""
        raw = {
            "id": 1,
            "title": "T",
            "basin": "B",
            "waterLevel": 1.0,
            "dangerLevel": 2.0,
            "warningLevel": 1.5,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2024-01-01T00:00:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert "water_level" in parsed
        assert "danger_level" in parsed
        assert "warning_level" in parsed
        assert "water_level_on" in parsed
        assert "trend" in parsed


@pytest.mark.unit
class TestDedupLogic:
    """Test deduplication key construction."""

    def test_dedup_key_format(self):
        """Dedup key should be station_id:water_level_on."""
        raw = {
            "id": 3,
            "title": "Babai at Chepang",
            "basin": "Babai",
            "waterLevel": 1.944,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2024-01-15T12:00:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        dedup_key = f"{parsed['station_id']}:{parsed['water_level_on']}"
        assert dedup_key == "3:2024-01-15T12:00:00+05:45"

    def test_dedup_different_timestamps_different_keys(self):
        r1 = NepalBipadHydrologyAPI.parse_reading({
            "id": 3, "title": "T", "basin": "B",
            "waterLevel": 1.0, "status": "S", "steady": "STEADY",
            "waterLevelOn": "2024-01-15T12:00:00+05:45",
        })
        r2 = NepalBipadHydrologyAPI.parse_reading({
            "id": 3, "title": "T", "basin": "B",
            "waterLevel": 1.5, "status": "S", "steady": "STEADY",
            "waterLevelOn": "2024-01-15T12:15:00+05:45",
        })
        key1 = f"{r1['station_id']}:{r1['water_level_on']}"
        key2 = f"{r2['station_id']}:{r2['water_level_on']}"
        assert key1 != key2

    def test_dedup_same_timestamp_same_key(self):
        r1 = NepalBipadHydrologyAPI.parse_reading({
            "id": 3, "title": "T", "basin": "B",
            "waterLevel": 1.0, "status": "S", "steady": "STEADY",
            "waterLevelOn": "2024-01-15T12:00:00+05:45",
        })
        r2 = NepalBipadHydrologyAPI.parse_reading({
            "id": 3, "title": "T", "basin": "B",
            "waterLevel": 1.0, "status": "S", "steady": "STEADY",
            "waterLevelOn": "2024-01-15T12:00:00+05:45",
        })
        key1 = f"{r1['station_id']}:{r1['water_level_on']}"
        key2 = f"{r2['station_id']}:{r2['water_level_on']}"
        assert key1 == key2


@pytest.mark.unit
class TestStateManagement:
    """Test state persistence."""

    def test_load_state_missing_file(self):
        result = _load_state("/nonexistent/path/state.json")
        assert result == {}

    def test_load_state_empty_path(self):
        result = _load_state("")
        assert result == {}

    def test_save_state_empty_path(self):
        # Should not raise
        _save_state("", {"key": "value"})

    def test_save_and_load_state(self, tmp_path):
        state_file = str(tmp_path / "test_state.json")
        data = {"3": "3:2024-01-15T12:00:00+05:45"}
        _save_state(state_file, data)
        loaded = _load_state(state_file)
        assert loaded == data


@pytest.mark.unit
class TestAPIEndpointURLs:
    """Test URL construction."""

    def test_default_base_url(self):
        api = NepalBipadHydrologyAPI()
        assert "bipadportal.gov.np" in api.base_url

    def test_custom_base_url_trailing_slash_stripped(self):
        api = NepalBipadHydrologyAPI(base_url="https://example.com/api/v1/")
        assert not api.base_url.endswith("/")

    def test_has_required_methods(self):
        api = NepalBipadHydrologyAPI()
        assert hasattr(api, 'fetch_all_stations')
        assert hasattr(api, 'parse_station')
        assert hasattr(api, 'parse_reading')
        assert hasattr(api, 'parse_connection_string')
        assert hasattr(api, 'feed_stations')


@pytest.mark.unit
class TestDataClassConstruction:
    """Test that parsed data can be used to construct generated data classes."""

    def test_river_station_construction(self):
        from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.riverstation import RiverStation
        raw = {
            "id": 3,
            "title": "Babai at Chepang",
            "basin": "Babai",
            "point": {"type": "Point", "coordinates": [81.7135456, 28.3565601]},
            "elevation": 308,
            "dangerLevel": 6.8,
            "warningLevel": 5.5,
            "description": "Old station",
            "dataSource": "hydrology.gov.np",
            "province": 5,
            "district": 65,
            "municipality": 58002,
            "ward": 4870,
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        station = RiverStation(**parsed)
        assert station.station_id == "3"
        assert station.title == "Babai at Chepang"
        assert station.basin == "Babai"
        assert station.elevation == 308
        assert station.danger_level == pytest.approx(6.8)

    def test_river_station_with_nulls(self):
        from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.riverstation import RiverStation
        raw = {
            "id": 100,
            "title": "Null Station",
            "basin": "Koshi",
            "point": {"type": "Point", "coordinates": [86.0, 27.0]},
            "elevation": None,
            "dangerLevel": None,
            "warningLevel": None,
            "description": None,
            "dataSource": "hydrology.gov.np",
            "province": None,
            "district": None,
            "municipality": None,
            "ward": None,
        }
        parsed = NepalBipadHydrologyAPI.parse_station(raw)
        station = RiverStation(**parsed)
        assert station.elevation is None
        assert station.danger_level is None
        assert station.warning_level is None
        assert station.province is None

    def test_water_level_reading_construction(self):
        from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.waterlevelreading import WaterLevelReading
        raw = {
            "id": 3,
            "title": "Babai at Chepang",
            "basin": "Babai",
            "waterLevel": 1.944,
            "dangerLevel": 6.8,
            "warningLevel": 5.5,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2024-01-15T12:00:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        reading = WaterLevelReading(**parsed)
        assert reading.station_id == "3"
        assert reading.water_level == pytest.approx(1.944)
        assert reading.status == "BELOW WARNING LEVEL"
        assert reading.trend == "STEADY"
        assert reading.water_level_on == "2024-01-15T12:00:00+05:45"

    def test_water_level_reading_null_water_level(self):
        from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.waterlevelreading import WaterLevelReading
        raw = {
            "id": 162,
            "title": "Marin River",
            "basin": "Bagmati",
            "waterLevel": None,
            "dangerLevel": 5.1,
            "warningLevel": 4.5,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2021-07-14T07:40:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        reading = WaterLevelReading(**parsed)
        assert reading.water_level is None
        assert reading.danger_level == pytest.approx(5.1)

    def test_river_station_serialization_roundtrip(self):
        from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.riverstation import RiverStation
        station = RiverStation(
            station_id="3",
            title="Test Station",
            basin="Babai",
            latitude=28.35,
            longitude=81.71,
            elevation=308,
            danger_level=6.8,
            warning_level=5.5,
            description="Test description",
            data_source="hydrology.gov.np",
            province=5,
            district=65,
            municipality=58002,
            ward=4870,
        )
        json_str = station.to_json()
        restored = RiverStation.from_json(json_str)
        assert restored.station_id == "3"
        assert restored.elevation == 308

    def test_water_level_reading_serialization_roundtrip(self):
        from nepal_bipad_hydrology_producer_data.np.gov.bipad.hydrology.waterlevelreading import WaterLevelReading
        reading = WaterLevelReading(
            station_id="3",
            title="Test",
            basin="Babai",
            water_level=1.944,
            danger_level=6.8,
            warning_level=5.5,
            status="BELOW WARNING LEVEL",
            trend="STEADY",
            water_level_on="2024-01-15T12:00:00+05:45",
        )
        json_str = reading.to_json()
        restored = WaterLevelReading.from_json(json_str)
        assert restored.station_id == "3"
        assert restored.water_level == pytest.approx(1.944)
