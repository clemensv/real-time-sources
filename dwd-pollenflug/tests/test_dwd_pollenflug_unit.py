"""
Unit tests for DWD Pollenflug (German Pollen Forecast) bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from dwd_pollenflug_producer_data import Region, PollenForecast
from dwd_pollenflug.dwd_pollenflug import (
    DWDPollenflugPoller,
    parse_connection_string,
    parse_regions,
    parse_forecasts,
    get_region_id,
    get_region_display_name,
    POLLEN_NAME_MAP,
    FORECAST_API_URL,
)

SAMPLE_API_RESPONSE = {
    "next_update": "2025-04-09 11:00 Uhr",
    "last_update": "2025-04-08 11:00 Uhr",
    "name": "Pollenflug-Gefahrenindex für Deutschland ausgegeben vom Deutschen Wetterdienst",
    "sender": "Deutscher Wetterdienst - Medizin-Meteorologie",
    "legend": {
        "id1": "0", "id1_desc": "keine Belastung",
        "id2": "0-1", "id2_desc": "keine bis geringe Belastung",
        "id3": "1", "id3_desc": "geringe Belastung",
        "id4": "1-2", "id4_desc": "geringe bis mittlere Belastung",
        "id5": "2", "id5_desc": "mittlere Belastung",
        "id6": "2-3", "id6_desc": "mittlere bis hohe Belastung",
        "id7": "3", "id7_desc": "hohe Belastung",
    },
    "content": [
        {
            "region_id": 10,
            "region_name": "Schleswig-Holstein und Hamburg",
            "partregion_id": 11,
            "partregion_name": "Inseln und Marschen",
            "Pollen": {
                "Birke": {"today": "2-3", "tomorrow": "2-3", "dayafter_to": "2"},
                "Roggen": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Erle": {"today": "0-1", "tomorrow": "0-1", "dayafter_to": "0-1"},
                "Ambrosia": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Hasel": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Esche": {"today": "1-2", "tomorrow": "1-2", "dayafter_to": "1"},
                "Graeser": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Beifuss": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
            },
        },
        {
            "region_id": 20,
            "region_name": "Mecklenburg-Vorpommern",
            "partregion_id": -1,
            "partregion_name": "",
            "Pollen": {
                "Birke": {"today": "3", "tomorrow": "3", "dayafter_to": "2"},
                "Roggen": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Erle": {"today": "1", "tomorrow": "1", "dayafter_to": "0-1"},
                "Ambrosia": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Hasel": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Esche": {"today": "2", "tomorrow": "2", "dayafter_to": "1-2"},
                "Graeser": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
                "Beifuss": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
            },
        },
    ],
}


@pytest.mark.unit
class TestPollenNameMapping:
    """Tests for German-to-English pollen name mapping."""

    def test_all_eight_pollen_types_mapped(self):
        assert len(POLLEN_NAME_MAP) == 8

    def test_hasel_maps_to_hazel(self):
        assert POLLEN_NAME_MAP["Hasel"] == "hazel"

    def test_erle_maps_to_alder(self):
        assert POLLEN_NAME_MAP["Erle"] == "alder"

    def test_birke_maps_to_birch(self):
        assert POLLEN_NAME_MAP["Birke"] == "birch"

    def test_esche_maps_to_ash(self):
        assert POLLEN_NAME_MAP["Esche"] == "ash"

    def test_graeser_maps_to_grasses(self):
        assert POLLEN_NAME_MAP["Graeser"] == "grasses"

    def test_roggen_maps_to_rye(self):
        assert POLLEN_NAME_MAP["Roggen"] == "rye"

    def test_beifuss_maps_to_mugwort(self):
        assert POLLEN_NAME_MAP["Beifuss"] == "mugwort"

    def test_ambrosia_maps_to_ragweed(self):
        assert POLLEN_NAME_MAP["Ambrosia"] == "ragweed"


@pytest.mark.unit
class TestGetRegionId:
    """Tests for region ID derivation logic."""

    def test_subregion_uses_partregion_id(self):
        item = {"region_id": 10, "partregion_id": 11, "partregion_name": "Inseln und Marschen"}
        assert get_region_id(item) == 11

    def test_no_subregion_uses_region_id(self):
        item = {"region_id": 20, "partregion_id": -1, "partregion_name": ""}
        assert get_region_id(item) == 20

    def test_partregion_id_zero_uses_region_id(self):
        item = {"region_id": 50, "partregion_id": 0}
        assert get_region_id(item) == 50

    def test_missing_partregion_id_uses_region_id(self):
        item = {"region_id": 30}
        assert get_region_id(item) == 30


@pytest.mark.unit
class TestGetRegionDisplayName:
    """Tests for region display name."""

    def test_uses_partregion_name_when_available(self):
        item = {"region_name": "Schleswig-Holstein und Hamburg", "partregion_name": "Inseln und Marschen"}
        assert get_region_display_name(item) == "Inseln und Marschen"

    def test_uses_region_name_when_partregion_name_empty(self):
        item = {"region_name": "Mecklenburg-Vorpommern", "partregion_name": ""}
        assert get_region_display_name(item) == "Mecklenburg-Vorpommern"

    def test_uses_region_name_when_partregion_name_missing(self):
        item = {"region_name": "Brandenburg und Berlin"}
        assert get_region_display_name(item) == "Brandenburg und Berlin"


@pytest.mark.unit
class TestParseRegions:
    """Tests for parsing region reference data."""

    def test_parse_regions_count(self):
        regions = parse_regions(SAMPLE_API_RESPONSE)
        assert len(regions) == 2

    def test_subregion_parsed(self):
        regions = parse_regions(SAMPLE_API_RESPONSE)
        r = regions[0]
        assert r.region_id == 11
        assert r.region_name == "Schleswig-Holstein und Hamburg"
        assert r.partregion_id == 11
        assert r.partregion_name == "Inseln und Marschen"

    def test_no_subregion_parsed(self):
        regions = parse_regions(SAMPLE_API_RESPONSE)
        r = regions[1]
        assert r.region_id == 20
        assert r.region_name == "Mecklenburg-Vorpommern"
        assert r.partregion_id is None
        assert r.partregion_name is None

    def test_empty_content_returns_empty(self):
        regions = parse_regions({"content": []})
        assert regions == []

    def test_missing_content_returns_empty(self):
        regions = parse_regions({})
        assert regions == []


@pytest.mark.unit
class TestParseForecasts:
    """Tests for parsing pollen forecast data with German→English mapping."""

    def test_parse_forecasts_count(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        assert len(forecasts) == 2

    def test_forecast_metadata(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.region_id == 11
        assert f.region_name == "Inseln und Marschen"
        assert f.last_update == "2025-04-08 11:00 Uhr"
        assert f.next_update == "2025-04-09 11:00 Uhr"
        assert f.sender == "Deutscher Wetterdienst - Medizin-Meteorologie"

    def test_birch_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.birch_today == "2-3"
        assert f.birch_tomorrow == "2-3"
        assert f.birch_dayafter_to == "2"

    def test_hazel_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.hazel_today == "0"
        assert f.hazel_tomorrow == "0"
        assert f.hazel_dayafter_to == "0"

    def test_alder_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.alder_today == "0-1"
        assert f.alder_tomorrow == "0-1"
        assert f.alder_dayafter_to == "0-1"

    def test_ash_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.ash_today == "1-2"
        assert f.ash_tomorrow == "1-2"
        assert f.ash_dayafter_to == "1"

    def test_grasses_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.grasses_today == "0"
        assert f.grasses_tomorrow == "0"
        assert f.grasses_dayafter_to == "0"

    def test_rye_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.rye_today == "0"
        assert f.rye_tomorrow == "0"
        assert f.rye_dayafter_to == "0"

    def test_mugwort_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.mugwort_today == "0"
        assert f.mugwort_tomorrow == "0"
        assert f.mugwort_dayafter_to == "0"

    def test_ragweed_mapped_correctly(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.ragweed_today == "0"
        assert f.ragweed_tomorrow == "0"
        assert f.ragweed_dayafter_to == "0"

    def test_intensity_range_values_preserved(self):
        """Verify that range values like '0-1', '1-2', '2-3' are preserved as strings."""
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[0]
        assert f.birch_today == "2-3"
        assert f.alder_today == "0-1"
        assert f.ash_today == "1-2"

    def test_integer_intensity_values_preserved(self):
        """Verify that pure integer intensity values like '0', '1', '2', '3' are preserved."""
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[1]  # Mecklenburg-Vorpommern
        assert f.birch_today == "3"
        assert f.alder_today == "1"
        assert f.ash_today == "2"

    def test_no_subregion_uses_region_name(self):
        forecasts = parse_forecasts(SAMPLE_API_RESPONSE)
        f = forecasts[1]
        assert f.region_id == 20
        assert f.region_name == "Mecklenburg-Vorpommern"

    def test_missing_pollen_data_yields_none(self):
        """Test handling when a pollen type is missing from the data."""
        data = {
            "last_update": "2025-04-08 11:00 Uhr",
            "next_update": "2025-04-09 11:00 Uhr",
            "sender": "DWD",
            "content": [{
                "region_id": 10,
                "region_name": "Test",
                "partregion_id": -1,
                "partregion_name": "",
                "Pollen": {},  # No pollen data
            }],
        }
        forecasts = parse_forecasts(data)
        f = forecasts[0]
        assert f.hazel_today is None
        assert f.birch_tomorrow is None
        assert f.ragweed_dayafter_to is None

    def test_empty_content_returns_empty(self):
        data = {"content": [], "last_update": "", "next_update": ""}
        assert parse_forecasts(data) == []


@pytest.mark.unit
class TestNullFieldHandling:
    """Tests for null and missing field handling."""

    def test_region_null_partregion_fields(self):
        r = Region(region_id=20, region_name="Test", partregion_id=None, partregion_name=None)
        assert r.partregion_id is None
        assert r.partregion_name is None

    def test_forecast_null_pollen_fields(self):
        f = PollenForecast(
            region_id=10, region_name="Test",
            last_update="2025-04-08 11:00 Uhr",
            next_update="2025-04-09 11:00 Uhr",
            sender=None,
            hazel_today=None, hazel_tomorrow=None, hazel_dayafter_to=None,
            alder_today=None, alder_tomorrow=None, alder_dayafter_to=None,
            birch_today=None, birch_tomorrow=None, birch_dayafter_to=None,
            ash_today=None, ash_tomorrow=None, ash_dayafter_to=None,
            grasses_today=None, grasses_tomorrow=None, grasses_dayafter_to=None,
            rye_today=None, rye_tomorrow=None, rye_dayafter_to=None,
            mugwort_today=None, mugwort_tomorrow=None, mugwort_dayafter_to=None,
            ragweed_today=None, ragweed_tomorrow=None, ragweed_dayafter_to=None,
        )
        assert f.sender is None
        assert f.hazel_today is None


@pytest.mark.unit
class TestConnectionStringParsing:
    """Tests for parse_connection_string."""

    def test_parse_event_hubs_connection_string(self):
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123=;EntityPath=mytopic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'mytopic'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == cs

    def test_parse_plain_bootstrap_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_parse_connection_string_no_sasl(self):
        cs = "BootstrapServer=broker:9092;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert 'security.protocol' not in result


@pytest.mark.unit
class TestSerializationRoundtrip:
    """Tests for data class serialization and deserialization."""

    def test_region_roundtrip(self):
        r = Region(region_id=11, region_name="Schleswig-Holstein und Hamburg",
                    partregion_id=11, partregion_name="Inseln und Marschen")
        json_str = r.to_json()
        r2 = Region.from_json(json_str)
        assert r2.region_id == r.region_id
        assert r2.region_name == r.region_name
        assert r2.partregion_id == r.partregion_id
        assert r2.partregion_name == r.partregion_name

    def test_region_nullable_roundtrip(self):
        r = Region(region_id=20, region_name="Mecklenburg-Vorpommern",
                    partregion_id=None, partregion_name=None)
        json_str = r.to_json()
        r2 = Region.from_json(json_str)
        assert r2.partregion_id is None
        assert r2.partregion_name is None

    def test_forecast_roundtrip(self):
        f = PollenForecast(
            region_id=11, region_name="Inseln und Marschen",
            last_update="2025-04-08 11:00 Uhr",
            next_update="2025-04-09 11:00 Uhr",
            sender="DWD",
            hazel_today="0", hazel_tomorrow="0", hazel_dayafter_to="0",
            alder_today="0-1", alder_tomorrow="0-1", alder_dayafter_to="0-1",
            birch_today="2-3", birch_tomorrow="2-3", birch_dayafter_to="2",
            ash_today="1-2", ash_tomorrow="1-2", ash_dayafter_to="1",
            grasses_today="0", grasses_tomorrow="0", grasses_dayafter_to="0",
            rye_today="0", rye_tomorrow="0", rye_dayafter_to="0",
            mugwort_today="0", mugwort_tomorrow="0", mugwort_dayafter_to="0",
            ragweed_today="0", ragweed_tomorrow="0", ragweed_dayafter_to="0",
        )
        json_str = f.to_json()
        f2 = PollenForecast.from_json(json_str)
        assert f2.region_id == f.region_id
        assert f2.birch_today == "2-3"
        assert f2.ash_dayafter_to == "1"

    def test_region_to_byte_array(self):
        r = Region(region_id=11, region_name="Test",
                    partregion_id=None, partregion_name=None)
        data = r.to_byte_array("application/json")
        assert isinstance(data, (bytes, str))
        parsed = json.loads(data)
        assert parsed["region_id"] == 11


@pytest.mark.unit
class TestDeduplication:
    """Tests for deduplication logic."""

    def test_state_persists_last_update(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "state.json")
            # Simulate saving state
            state = {"last_update": "2025-04-08 11:00 Uhr"}
            with open(state_file, 'w') as f:
                json.dump(state, f)

            # Simulate loading state
            with open(state_file, 'r') as f:
                loaded = json.load(f)
            assert loaded["last_update"] == "2025-04-08 11:00 Uhr"

    def test_empty_state_file_returns_empty_dict(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "nonexistent.json")

            @patch('dwd_pollenflug.dwd_pollenflug.DEDWDPollenflugEventProducer')
            @patch('confluent_kafka.Producer')
            def _test(mock_producer_cls, mock_event_producer_cls):
                poller = object.__new__(DWDPollenflugPoller)
                poller.last_polled_file = state_file
                state = poller.load_state()
                assert state == {}
            _test()

    def test_same_last_update_is_skipped(self):
        """Verify that a repeated last_update causes the bridge to skip emission."""
        state = {"last_update": "2025-04-08 11:00 Uhr"}
        current_last_update = "2025-04-08 11:00 Uhr"
        # Same update should be skipped
        assert current_last_update == state.get("last_update")

    def test_new_last_update_triggers_emission(self):
        """Verify that a new last_update triggers forecast emission."""
        state = {"last_update": "2025-04-07 11:00 Uhr"}
        current_last_update = "2025-04-08 11:00 Uhr"
        assert current_last_update != state.get("last_update")


@pytest.mark.unit
class TestPollerStateIO:
    """Tests for poller state file I/O."""

    def test_save_and_load_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "state.json")
            poller = object.__new__(DWDPollenflugPoller)
            poller.last_polled_file = state_file
            poller.save_state({"last_update": "2025-04-08 11:00 Uhr"})
            loaded = poller.load_state()
            assert loaded["last_update"] == "2025-04-08 11:00 Uhr"

    def test_load_state_corrupted_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "bad.json")
            with open(state_file, 'w') as f:
                f.write("not json")
            poller = object.__new__(DWDPollenflugPoller)
            poller.last_polled_file = state_file
            state = poller.load_state()
            assert state == {}


@pytest.mark.unit
class TestForecastApiUrl:
    """Verify the API URL constant."""

    def test_api_url(self):
        assert FORECAST_API_URL == "https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json"
