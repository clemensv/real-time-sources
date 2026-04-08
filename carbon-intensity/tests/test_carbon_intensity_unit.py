"""
Unit tests for Carbon Intensity UK bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

from carbon_intensity_producer_data import Intensity, GenerationMix, RegionalIntensity
from carbon_intensity.carbon_intensity import (
    CarbonIntensityPoller,
    parse_connection_string,
    flatten_generation_mix,
    parse_api_datetime,
    FUEL_TYPES,
    API_BASE,
    POLL_INTERVAL_SECONDS,
)


# ---------------------------------------------------------------------------
# Sample API responses
# ---------------------------------------------------------------------------

SAMPLE_INTENSITY_RESPONSE = {
    "data": [{
        "from": "2026-04-06T09:30Z",
        "to": "2026-04-06T10:00Z",
        "intensity": {"forecast": 66, "actual": 68, "index": "low"}
    }]
}

SAMPLE_INTENSITY_NULL_ACTUAL = {
    "data": [{
        "from": "2026-04-06T10:00Z",
        "to": "2026-04-06T10:30Z",
        "intensity": {"forecast": 72, "actual": None, "index": "low"}
    }]
}

SAMPLE_GENERATION_RESPONSE = {
    "data": {
        "from": "2026-04-06T09:30Z",
        "to": "2026-04-06T10:00Z",
        "generationmix": [
            {"fuel": "biomass", "perc": 7.1},
            {"fuel": "coal", "perc": 0},
            {"fuel": "imports", "perc": 10.6},
            {"fuel": "gas", "perc": 40.0},
            {"fuel": "nuclear", "perc": 17.7},
            {"fuel": "other", "perc": 0},
            {"fuel": "hydro", "perc": 0},
            {"fuel": "solar", "perc": 0},
            {"fuel": "wind", "perc": 24.5},
        ]
    }
}

SAMPLE_REGIONAL_RESPONSE = {
    "data": [{
        "from": "2026-04-06T09:30Z",
        "to": "2026-04-06T10:00Z",
        "regions": [
            {
                "regionid": 1,
                "dnoregion": "Scottish Hydro Electric Power Distribution",
                "shortname": "North Scotland",
                "intensity": {"forecast": 0, "index": "very low"},
                "generationmix": [
                    {"fuel": "biomass", "perc": 0},
                    {"fuel": "coal", "perc": 0},
                    {"fuel": "imports", "perc": 0},
                    {"fuel": "gas", "perc": 0},
                    {"fuel": "nuclear", "perc": 0},
                    {"fuel": "other", "perc": 0},
                    {"fuel": "hydro", "perc": 0},
                    {"fuel": "solar", "perc": 0},
                    {"fuel": "wind", "perc": 100},
                ]
            },
            {
                "regionid": 2,
                "dnoregion": "SP Distribution",
                "shortname": "South Scotland",
                "intensity": {"forecast": 15, "index": "very low"},
                "generationmix": [
                    {"fuel": "biomass", "perc": 0.1},
                    {"fuel": "coal", "perc": 0},
                    {"fuel": "imports", "perc": 0.3},
                    {"fuel": "gas", "perc": 0},
                    {"fuel": "nuclear", "perc": 35.4},
                    {"fuel": "other", "perc": 0},
                    {"fuel": "hydro", "perc": 2.5},
                    {"fuel": "solar", "perc": 0},
                    {"fuel": "wind", "perc": 61.7},
                ]
            },
        ]
    }]
}


# ---------------------------------------------------------------------------
# parse_api_datetime
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseApiDatetime:

    def test_parse_z_suffix(self):
        dt = parse_api_datetime("2026-04-06T09:30Z")
        assert dt == datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc)

    def test_parse_offset(self):
        dt = parse_api_datetime("2026-04-06T09:30+00:00")
        assert dt == datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc)

    def test_parse_midnight(self):
        dt = parse_api_datetime("2026-01-01T00:00Z")
        assert dt == datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)

    def test_parse_end_of_day(self):
        dt = parse_api_datetime("2026-12-31T23:30Z")
        assert dt == datetime(2026, 12, 31, 23, 30, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# flatten_generation_mix
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFlattenGenerationMix:

    def test_full_mix(self):
        mix_list = [
            {"fuel": "biomass", "perc": 7.1},
            {"fuel": "coal", "perc": 0},
            {"fuel": "imports", "perc": 10.6},
            {"fuel": "gas", "perc": 40.0},
            {"fuel": "nuclear", "perc": 17.7},
            {"fuel": "other", "perc": 0},
            {"fuel": "hydro", "perc": 0},
            {"fuel": "solar", "perc": 0},
            {"fuel": "wind", "perc": 24.5},
        ]
        result = flatten_generation_mix(mix_list)
        assert result["biomass_pct"] == 7.1
        assert result["gas_pct"] == 40.0
        assert result["wind_pct"] == 24.5
        assert result["coal_pct"] == 0
        assert result["solar_pct"] == 0

    def test_missing_fuel_returns_none(self):
        result = flatten_generation_mix([{"fuel": "gas", "perc": 50}])
        assert result["gas_pct"] == 50
        assert result["wind_pct"] is None
        assert result["nuclear_pct"] is None

    def test_empty_mix(self):
        result = flatten_generation_mix([])
        for fuel in FUEL_TYPES:
            assert result[f"{fuel}_pct"] is None

    def test_all_fuel_keys_present(self):
        result = flatten_generation_mix([])
        assert set(result.keys()) == {f"{f}_pct" for f in FUEL_TYPES}

    def test_oil_fuel_included(self):
        mix_list = [{"fuel": "oil", "perc": 1.5}]
        result = flatten_generation_mix(mix_list)
        assert result["oil_pct"] == 1.5


# ---------------------------------------------------------------------------
# parse_connection_string
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=abc123;EntityPath=hub"
        result = parse_connection_string(cs)
        assert 'bootstrap.servers' in result
        assert result['kafka_topic'] == 'hub'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['security.protocol'] == 'SASL_SSL'

    def test_plain_bootstrap_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_bootstrap_server_with_port(self):
        cs = "BootstrapServer=broker:29092;EntityPath=my-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'broker:29092'

    def test_empty_string_returns_empty(self):
        result = parse_connection_string("")
        assert result == {}


# ---------------------------------------------------------------------------
# CarbonIntensityPoller — parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseIntensity:

    def test_parse_standard_response(self):
        intensity = CarbonIntensityPoller.parse_intensity(SAMPLE_INTENSITY_RESPONSE)
        assert intensity is not None
        assert intensity.forecast == 66
        assert intensity.actual == 68
        assert intensity.index == "low"
        assert intensity.period_from == datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc)
        assert intensity.period_to == datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc)

    def test_parse_null_actual(self):
        intensity = CarbonIntensityPoller.parse_intensity(SAMPLE_INTENSITY_NULL_ACTUAL)
        assert intensity is not None
        assert intensity.forecast == 72
        assert intensity.actual is None

    def test_parse_empty_data(self):
        assert CarbonIntensityPoller.parse_intensity({"data": []}) is None

    def test_parse_missing_data_key(self):
        assert CarbonIntensityPoller.parse_intensity({}) is None


@pytest.mark.unit
class TestParseGeneration:

    def test_parse_standard_response(self):
        gen = CarbonIntensityPoller.parse_generation(SAMPLE_GENERATION_RESPONSE)
        assert gen is not None
        assert gen.biomass_pct == 7.1
        assert gen.gas_pct == 40.0
        assert gen.wind_pct == 24.5
        assert gen.period_from == datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc)

    def test_parse_empty_data(self):
        assert CarbonIntensityPoller.parse_generation({"data": None}) is None

    def test_parse_missing_fuels(self):
        data = {"data": {
            "from": "2026-01-01T00:00Z",
            "to": "2026-01-01T00:30Z",
            "generationmix": [{"fuel": "gas", "perc": 100}],
        }}
        gen = CarbonIntensityPoller.parse_generation(data)
        assert gen is not None
        assert gen.gas_pct == 100
        assert gen.wind_pct is None


@pytest.mark.unit
class TestParseRegional:

    def test_parse_standard_response(self):
        regionals = CarbonIntensityPoller.parse_regional(SAMPLE_REGIONAL_RESPONSE)
        assert len(regionals) == 2
        r1 = regionals[0]
        assert r1.region_id == 1
        assert r1.shortname == "North Scotland"
        assert r1.dnoregion == "Scottish Hydro Electric Power Distribution"
        assert r1.forecast == 0
        assert r1.index == "very low"
        assert r1.wind_pct == 100
        assert r1.gas_pct == 0

    def test_parse_second_region(self):
        regionals = CarbonIntensityPoller.parse_regional(SAMPLE_REGIONAL_RESPONSE)
        r2 = regionals[1]
        assert r2.region_id == 2
        assert r2.shortname == "South Scotland"
        assert r2.nuclear_pct == 35.4
        assert r2.hydro_pct == 2.5

    def test_parse_empty_data(self):
        assert CarbonIntensityPoller.parse_regional({"data": []}) == []

    def test_parse_empty_regions(self):
        data = {"data": [{"from": "2026-01-01T00:00Z", "to": "2026-01-01T00:30Z", "regions": []}]}
        assert CarbonIntensityPoller.parse_regional(data) == []

    def test_regional_period_times(self):
        regionals = CarbonIntensityPoller.parse_regional(SAMPLE_REGIONAL_RESPONSE)
        for r in regionals:
            assert r.period_from == datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc)
            assert r.period_to == datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# CarbonIntensityPoller — state persistence
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStatePersistence:

    def test_load_state_missing_file(self, tmp_path):
        poller = self._make_poller(tmp_path)
        state = poller.load_state()
        assert state == {}

    def test_save_and_load_state(self, tmp_path):
        poller = self._make_poller(tmp_path)
        poller.save_state({"last_period_from": "2026-04-06T09:30:00+00:00"})
        state = poller.load_state()
        assert state["last_period_from"] == "2026-04-06T09:30:00+00:00"

    def test_save_creates_directory(self, tmp_path):
        state_file = str(tmp_path / "subdir" / "state.json")
        poller = self._make_poller(tmp_path, state_file=state_file)
        poller.save_state({"key": "value"})
        assert os.path.exists(state_file)

    @staticmethod
    def _make_poller(tmp_path, state_file=None):
        if state_file is None:
            state_file = str(tmp_path / "state.json")
        with patch('carbon_intensity.carbon_intensity.CarbonIntensityPoller.__init__', lambda self, **kw: None):
            poller = CarbonIntensityPoller.__new__(CarbonIntensityPoller)
            poller.last_polled_file = state_file
        return poller


# ---------------------------------------------------------------------------
# CarbonIntensityPoller — emit helpers (mock producer)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEmitHelpers:

    @pytest.fixture
    def poller(self):
        with patch('carbon_intensity.carbon_intensity.CarbonIntensityPoller.__init__', lambda self, **kw: None):
            p = CarbonIntensityPoller.__new__(CarbonIntensityPoller)
        p.producer = Mock()
        p.regional_producer = Mock()
        return p

    def test_emit_intensity(self, poller):
        intensity = Intensity(
            period_from=datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            forecast=66, actual=68, index="low",
        )
        poller.emit_intensity(intensity)
        poller.producer.send_uk_org_carbonintensity_intensity.assert_called_once()
        call_kwargs = poller.producer.send_uk_org_carbonintensity_intensity.call_args
        assert call_kwargs.kwargs['_period_from'] == "2026-04-06T09:30:00+00:00"

    def test_emit_generation_mix(self, poller):
        gen = GenerationMix(
            period_from=datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            biomass_pct=7.1, coal_pct=0, gas_pct=40.0, hydro_pct=0,
            imports_pct=10.6, nuclear_pct=17.7, oil_pct=0, other_pct=0,
            solar_pct=0, wind_pct=24.5,
        )
        poller.emit_generation_mix(gen)
        poller.producer.send_uk_org_carbonintensity_generation_mix.assert_called_once()

    def test_emit_regional(self, poller):
        regional = RegionalIntensity(
            region_id=1, dnoregion="TestDNO", shortname="Test",
            period_from=datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            forecast=0, index="very low",
            biomass_pct=0, coal_pct=0, gas_pct=0, hydro_pct=0,
            imports_pct=0, nuclear_pct=0, oil_pct=0, other_pct=0,
            solar_pct=0, wind_pct=100,
        )
        poller.emit_regional(regional)
        poller.regional_producer.send_uk_org_carbonintensity_regional_intensity.assert_called_once()
        call_kwargs = poller.regional_producer.send_uk_org_carbonintensity_regional_intensity.call_args
        assert call_kwargs.kwargs['_region_id'] == "1"


# ---------------------------------------------------------------------------
# CarbonIntensityPoller — poll_once
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollOnce:

    @pytest.fixture
    def poller(self):
        with patch('carbon_intensity.carbon_intensity.CarbonIntensityPoller.__init__', lambda self, **kw: None):
            p = CarbonIntensityPoller.__new__(CarbonIntensityPoller)
        p.producer = Mock()
        p.producer.producer = Mock()
        p.regional_producer = Mock()
        return p

    @patch.object(CarbonIntensityPoller, 'fetch_regional', return_value=SAMPLE_REGIONAL_RESPONSE)
    @patch.object(CarbonIntensityPoller, 'fetch_generation', return_value=SAMPLE_GENERATION_RESPONSE)
    @patch.object(CarbonIntensityPoller, 'fetch_intensity', return_value=SAMPLE_INTENSITY_RESPONSE)
    def test_poll_once_returns_period_from(self, mock_int, mock_gen, mock_reg, poller):
        result = poller.poll_once()
        assert result == "2026-04-06T09:30:00+00:00"

    @patch.object(CarbonIntensityPoller, 'fetch_regional', return_value=SAMPLE_REGIONAL_RESPONSE)
    @patch.object(CarbonIntensityPoller, 'fetch_generation', return_value=SAMPLE_GENERATION_RESPONSE)
    @patch.object(CarbonIntensityPoller, 'fetch_intensity', return_value=SAMPLE_INTENSITY_RESPONSE)
    def test_poll_once_emits_all_event_types(self, mock_int, mock_gen, mock_reg, poller):
        poller.poll_once()
        poller.producer.send_uk_org_carbonintensity_intensity.assert_called_once()
        poller.producer.send_uk_org_carbonintensity_generation_mix.assert_called_once()
        assert poller.regional_producer.send_uk_org_carbonintensity_regional_intensity.call_count == 2

    @patch.object(CarbonIntensityPoller, 'fetch_regional', return_value=None)
    @patch.object(CarbonIntensityPoller, 'fetch_generation', return_value=None)
    @patch.object(CarbonIntensityPoller, 'fetch_intensity', return_value=None)
    def test_poll_once_handles_api_failures(self, mock_int, mock_gen, mock_reg, poller):
        result = poller.poll_once()
        assert result is None
        poller.producer.send_uk_org_carbonintensity_intensity.assert_not_called()

    @patch.object(CarbonIntensityPoller, 'fetch_regional', return_value=None)
    @patch.object(CarbonIntensityPoller, 'fetch_generation', return_value=SAMPLE_GENERATION_RESPONSE)
    @patch.object(CarbonIntensityPoller, 'fetch_intensity', return_value=None)
    def test_poll_once_partial_success(self, mock_int, mock_gen, mock_reg, poller):
        result = poller.poll_once()
        assert result is None  # no intensity emitted
        poller.producer.send_uk_org_carbonintensity_generation_mix.assert_called_once()


# ---------------------------------------------------------------------------
# CarbonIntensityPoller — fetch methods (with requests-mock)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFetchMethods:

    @patch('carbon_intensity.carbon_intensity.requests.get')
    def test_fetch_intensity_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: SAMPLE_INTENSITY_RESPONSE)
        mock_get.return_value.raise_for_status = Mock()
        result = CarbonIntensityPoller.fetch_intensity()
        assert result == SAMPLE_INTENSITY_RESPONSE
        mock_get.assert_called_once_with(f"{API_BASE}/intensity", timeout=30)

    @patch('carbon_intensity.carbon_intensity.requests.get')
    def test_fetch_intensity_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        result = CarbonIntensityPoller.fetch_intensity()
        assert result is None

    @patch('carbon_intensity.carbon_intensity.requests.get')
    def test_fetch_generation_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: SAMPLE_GENERATION_RESPONSE)
        mock_get.return_value.raise_for_status = Mock()
        result = CarbonIntensityPoller.fetch_generation()
        assert result == SAMPLE_GENERATION_RESPONSE

    @patch('carbon_intensity.carbon_intensity.requests.get')
    def test_fetch_regional_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: SAMPLE_REGIONAL_RESPONSE)
        mock_get.return_value.raise_for_status = Mock()
        result = CarbonIntensityPoller.fetch_regional()
        assert result == SAMPLE_REGIONAL_RESPONSE


# ---------------------------------------------------------------------------
# Data classes — serialization
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDataClassSerialization:

    def test_intensity_to_json(self):
        intensity = Intensity(
            period_from=datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            forecast=66, actual=68, index="low",
        )
        json_str = intensity.to_json()
        parsed = json.loads(json_str)
        assert parsed["forecast"] == 66
        assert parsed["actual"] == 68
        assert parsed["index"] == "low"

    def test_intensity_nullable_actual(self):
        intensity = Intensity(
            period_from=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 30, tzinfo=timezone.utc),
            forecast=72, actual=None, index="low",
        )
        json_str = intensity.to_json()
        parsed = json.loads(json_str)
        assert parsed["actual"] is None

    def test_generation_mix_to_json(self):
        gen = GenerationMix(
            period_from=datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            biomass_pct=7.1, coal_pct=0, gas_pct=40.0, hydro_pct=0,
            imports_pct=10.6, nuclear_pct=17.7, oil_pct=0, other_pct=0,
            solar_pct=0, wind_pct=24.5,
        )
        json_str = gen.to_json()
        parsed = json.loads(json_str)
        assert parsed["gas_pct"] == 40.0
        assert parsed["wind_pct"] == 24.5

    def test_regional_intensity_to_json(self):
        reg = RegionalIntensity(
            region_id=1, dnoregion="TestDNO", shortname="Test",
            period_from=datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            forecast=0, index="very low",
            biomass_pct=0, coal_pct=0, gas_pct=0, hydro_pct=0,
            imports_pct=0, nuclear_pct=0, oil_pct=0, other_pct=0,
            solar_pct=0, wind_pct=100,
        )
        json_str = reg.to_json()
        parsed = json.loads(json_str)
        assert parsed["region_id"] == 1
        assert parsed["wind_pct"] == 100

    def test_intensity_from_data(self):
        data = {
            "period_from": "2026-04-06T09:30:00+00:00",
            "period_to": "2026-04-06T10:00:00+00:00",
            "forecast": 66, "actual": 68, "index": "low",
        }
        intensity = Intensity.from_data(data)
        assert intensity.forecast == 66

    def test_generation_mix_nullable_field(self):
        gen = GenerationMix(
            period_from=datetime(2026, 4, 6, 9, 30, tzinfo=timezone.utc),
            period_to=datetime(2026, 4, 6, 10, 0, tzinfo=timezone.utc),
            biomass_pct=None, coal_pct=None, gas_pct=None, hydro_pct=None,
            imports_pct=None, nuclear_pct=None, oil_pct=None, other_pct=None,
            solar_pct=None, wind_pct=None,
        )
        json_str = gen.to_json()
        parsed = json.loads(json_str)
        assert parsed["wind_pct"] is None


# ---------------------------------------------------------------------------
# Constants and config
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestConstants:

    def test_poll_interval(self):
        assert POLL_INTERVAL_SECONDS == 1800

    def test_api_base(self):
        assert API_BASE == "https://api.carbonintensity.org.uk"

    def test_fuel_types_count(self):
        assert len(FUEL_TYPES) == 10

    def test_fuel_types_contents(self):
        expected = {"biomass", "coal", "imports", "gas", "nuclear",
                    "other", "hydro", "solar", "wind", "oil"}
        assert set(FUEL_TYPES) == expected
