"""
Unit tests for Energy-Charts bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from energy_charts_producer_data import PublicPower, SpotPrice, GridSignal
from energy_charts.energy_charts import (
    EnergyChartsPoller,
    parse_connection_string,
    PRODUCTION_TYPE_MAP,
    API_BASE,
)


# ---------------------------------------------------------------------------
# Sample API responses
# ---------------------------------------------------------------------------

SAMPLE_PUBLIC_POWER = {
    "unix_seconds": [1700000000, 1700000900, 1700001800],
    "production_types": [
        {"name": "Wind onshore", "data": [5000.0, 5200.0, 5100.0]},
        {"name": "Solar", "data": [1200.0, 1300.0, None]},
        {"name": "Fossil gas", "data": [8000.0, 7800.0, 7900.0]},
        {"name": "Nuclear", "data": [None, None, None]},
        {"name": "Biomass", "data": [4500.0, 4500.0, 4500.0]},
        {"name": "Fossil brown coal / lignite", "data": [6000.0, 5800.0, 5900.0]},
        {"name": "Fossil hard coal", "data": [3000.0, 2900.0, 3100.0]},
        {"name": "Fossil oil", "data": [200.0, 180.0, 190.0]},
        {"name": "Fossil coal-derived gas", "data": [100.0, 90.0, 110.0]},
        {"name": "Geothermal", "data": [30.0, 30.0, 30.0]},
        {"name": "Hydro Run-of-River", "data": [1500.0, 1500.0, 1500.0]},
        {"name": "Hydro water reservoir", "data": [500.0, 500.0, 500.0]},
        {"name": "Hydro pumped storage", "data": [0.0, 200.0, 0.0]},
        {"name": "Hydro pumped storage consumption", "data": [-500.0, -300.0, -600.0]},
        {"name": "Cross border electricity trading", "data": [1000.0, -500.0, 200.0]},
        {"name": "Others", "data": [100.0, 100.0, 100.0]},
        {"name": "Waste", "data": [400.0, 400.0, 400.0]},
        {"name": "Wind offshore", "data": [2000.0, 2100.0, 2050.0]},
        {"name": "Load", "data": [50000.0, 49000.0, 48000.0]},
        {"name": "Residual load", "data": [30000.0, 28000.0, 29000.0]},
        {"name": "Renewable share of generation", "data": [45.0, 47.0, 46.0]},
        {"name": "Renewable share of load", "data": [40.0, 42.0, 41.0]},
    ],
    "deprecated": False,
}

SAMPLE_PRICE = {
    "license_info": "CC BY 4.0",
    "unix_seconds": [1700000000, 1700003600],
    "price": [85.50, 92.10],
    "unit": "EUR / MWh",
    "deprecated": False,
}

SAMPLE_SIGNAL = {
    "unix_seconds": [1700000000, 1700000900, 1700001800],
    "share": [44.3, 47.1, 46.0],
    "signal": [0, 0, 1],
    "substitute": False,
    "deprecated": False,
}


# ---------------------------------------------------------------------------
# Test parse_connection_string
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net;SharedAccessKeyName=mykey;SharedAccessKey=mysecret;EntityPath=mytopic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'mytopic'
        assert result['sasl.username'] == '$ConnectionString'
        assert 'sasl.password' in result
        assert result['security.protocol'] == 'SASL_SSL'

    def test_bootstrap_server_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_invalid_connection_string_empty(self):
        result = parse_connection_string("")
        assert 'bootstrap.servers' not in result

    def test_entity_path_extraction(self):
        cs = "BootstrapServer=broker:9092;EntityPath=my-energy-topic"
        result = parse_connection_string(cs)
        assert result['kafka_topic'] == 'my-energy-topic'


# ---------------------------------------------------------------------------
# Test PRODUCTION_TYPE_MAP
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestProductionTypeMap:

    def test_all_expected_types_present(self):
        expected = [
            "Wind onshore", "Wind offshore", "Solar", "Fossil gas",
            "Nuclear", "Biomass", "Load", "Residual load",
            "Renewable share of generation", "Renewable share of load",
            "Hydro pumped storage consumption", "Cross border electricity trading",
            "Hydro Run-of-River", "Fossil brown coal / lignite",
            "Fossil hard coal", "Fossil oil", "Fossil coal-derived gas",
            "Geothermal", "Hydro water reservoir", "Hydro pumped storage",
            "Others", "Waste",
        ]
        for name in expected:
            assert name in PRODUCTION_TYPE_MAP, f"Missing: {name}"

    def test_field_names_are_snake_case(self):
        for name, field in PRODUCTION_TYPE_MAP.items():
            assert field == field.lower(), f"{field} not lowercase"
            assert " " not in field, f"{field} contains spaces"

    def test_map_has_22_entries(self):
        assert len(PRODUCTION_TYPE_MAP) == 22


# ---------------------------------------------------------------------------
# Test parse_public_power
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParsePublicPower:

    def test_correct_count(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert len(records) == 3

    def test_country_set(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        for r in records:
            assert r.country == "de"

    def test_timestamp_is_utc(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[0].timestamp.tzinfo == timezone.utc

    def test_unix_seconds_preserved(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[0].unix_seconds == 1700000000
        assert records[1].unix_seconds == 1700000900

    def test_wind_onshore_values(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[0].wind_onshore_mw == 5000.0
        assert records[1].wind_onshore_mw == 5200.0

    def test_solar_null_handling(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[0].solar_mw == 1200.0
        assert records[2].solar_mw is None

    def test_nuclear_all_none(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        for r in records:
            assert r.nuclear_mw is None

    def test_negative_pumped_storage_consumption(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[0].hydro_pumped_storage_consumption_mw == -500.0

    def test_cross_border_negative(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[1].cross_border_electricity_trading_mw == -500.0

    def test_renewable_share_values(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[0].renewable_share_of_generation_pct == 45.0
        assert records[0].renewable_share_of_load_pct == 40.0

    def test_load_values(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert records[0].load_mw == 50000.0

    def test_empty_response(self):
        records = EnergyChartsPoller.parse_public_power({"unix_seconds": [], "production_types": []}, "de")
        assert len(records) == 0

    def test_missing_production_type_is_none(self):
        sparse = {
            "unix_seconds": [1700000000],
            "production_types": [
                {"name": "Solar", "data": [1000.0]},
            ],
        }
        records = EnergyChartsPoller.parse_public_power(sparse, "fr")
        assert records[0].solar_mw == 1000.0
        assert records[0].wind_onshore_mw is None
        assert records[0].fossil_gas_mw is None

    def test_unknown_production_type_ignored(self):
        data = {
            "unix_seconds": [1700000000],
            "production_types": [
                {"name": "FutureEnergy", "data": [999.0]},
                {"name": "Solar", "data": [1000.0]},
            ],
        }
        records = EnergyChartsPoller.parse_public_power(data, "de")
        assert len(records) == 1
        assert records[0].solar_mw == 1000.0

    def test_is_publicpower_instance(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        assert isinstance(records[0], PublicPower)

    def test_timestamp_conversion(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        expected = datetime.fromtimestamp(1700000000, tz=timezone.utc)
        assert records[0].timestamp == expected


# ---------------------------------------------------------------------------
# Test parse_price
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParsePrice:

    def test_correct_count(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        assert len(records) == 2

    def test_price_values(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        assert records[0].price_eur_per_mwh == 85.50
        assert records[1].price_eur_per_mwh == 92.10

    def test_bidding_zone_set(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        assert records[0].bidding_zone == "DE-LU"

    def test_country_set(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        assert records[0].country == "de"

    def test_unit_preserved(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        assert records[0].unit == "EUR / MWh"

    def test_timestamp_is_utc(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        assert records[0].timestamp.tzinfo == timezone.utc

    def test_empty_response(self):
        records = EnergyChartsPoller.parse_price({"unix_seconds": [], "price": []}, "de", "DE-LU")
        assert len(records) == 0

    def test_is_spotprice_instance(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        assert isinstance(records[0], SpotPrice)

    def test_null_unit(self):
        data = {"unix_seconds": [1700000000], "price": [50.0]}
        records = EnergyChartsPoller.parse_price(data, "de", "DE-LU")
        assert records[0].unit is None


# ---------------------------------------------------------------------------
# Test parse_signal
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseSignal:

    def test_correct_count(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        assert len(records) == 3

    def test_signal_values(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        assert records[0].signal == 0
        assert records[2].signal == 1

    def test_share_values(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        assert records[0].renewable_share_pct == 44.3
        assert records[1].renewable_share_pct == 47.1

    def test_country_set(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        assert records[0].country == "de"

    def test_substitute_false(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        assert records[0].substitute is False

    def test_substitute_true(self):
        data = dict(SAMPLE_SIGNAL)
        data["substitute"] = True
        records = EnergyChartsPoller.parse_signal(data, "de")
        assert records[0].substitute is True

    def test_substitute_non_bool(self):
        data = dict(SAMPLE_SIGNAL)
        data["substitute"] = "yes"
        records = EnergyChartsPoller.parse_signal(data, "de")
        assert records[0].substitute is None

    def test_timestamp_is_utc(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        assert records[0].timestamp.tzinfo == timezone.utc

    def test_empty_response(self):
        records = EnergyChartsPoller.parse_signal({"unix_seconds": [], "share": [], "signal": []}, "de")
        assert len(records) == 0

    def test_is_gridsignal_instance(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        assert isinstance(records[0], GridSignal)


# ---------------------------------------------------------------------------
# Test URL construction
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestURLConstruction:

    def test_public_power_url(self):
        session = Mock()
        session.get = Mock(return_value=Mock(status_code=200, json=lambda: {"unix_seconds": [], "production_types": []}))
        session.get.return_value.raise_for_status = Mock()
        EnergyChartsPoller.fetch_public_power(session, "fr")
        session.get.assert_called_once_with(f"{API_BASE}/public_power?country=fr", timeout=30)

    def test_price_url(self):
        session = Mock()
        session.get = Mock(return_value=Mock(status_code=200, json=lambda: {"unix_seconds": [], "price": []}))
        session.get.return_value.raise_for_status = Mock()
        EnergyChartsPoller.fetch_price(session, "AT")
        session.get.assert_called_once_with(f"{API_BASE}/price?bzn=AT", timeout=30)

    def test_signal_url(self):
        session = Mock()
        session.get = Mock(return_value=Mock(status_code=200, json=lambda: {"unix_seconds": [], "share": [], "signal": []}))
        session.get.return_value.raise_for_status = Mock()
        EnergyChartsPoller.fetch_signal(session, "de")
        session.get.assert_called_once_with(f"{API_BASE}/signal?country=de", timeout=30)


# ---------------------------------------------------------------------------
# Test deduplication
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDeduplication:

    @patch('energy_charts.energy_charts.InfoEnergyChartsEventProducer')
    @patch('confluent_kafka.Producer')
    def test_power_dedup(self, mock_kafka_producer, mock_event_producer):
        mock_instance = MagicMock()
        mock_event_producer.return_value = mock_instance
        mock_instance.producer = MagicMock()

        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.country = "de"
        poller.bidding_zone = "DE-LU"
        poller.kafka_topic = "test"
        poller.last_polled_file = ""
        poller.session = Mock()
        poller.producer = mock_instance
        poller._seen_power = set()
        poller._seen_price = set()
        poller._seen_signal = set()

        poller.session.get = Mock(return_value=Mock(
            status_code=200,
            json=lambda: SAMPLE_PUBLIC_POWER
        ))
        poller.session.get.return_value.raise_for_status = Mock()

        count1 = poller.emit_public_power()
        assert count1 == 3
        count2 = poller.emit_public_power()
        assert count2 == 0  # All deduped

    @patch('energy_charts.energy_charts.InfoEnergyChartsEventProducer')
    @patch('confluent_kafka.Producer')
    def test_price_dedup(self, mock_kafka_producer, mock_event_producer):
        mock_instance = MagicMock()
        mock_event_producer.return_value = mock_instance
        mock_instance.producer = MagicMock()

        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.country = "de"
        poller.bidding_zone = "DE-LU"
        poller.kafka_topic = "test"
        poller.last_polled_file = ""
        poller.session = Mock()
        poller.producer = mock_instance
        poller._seen_power = set()
        poller._seen_price = set()
        poller._seen_signal = set()

        poller.session.get = Mock(return_value=Mock(
            status_code=200,
            json=lambda: SAMPLE_PRICE
        ))
        poller.session.get.return_value.raise_for_status = Mock()

        count1 = poller.emit_price()
        assert count1 == 2
        count2 = poller.emit_price()
        assert count2 == 0

    @patch('energy_charts.energy_charts.InfoEnergyChartsEventProducer')
    @patch('confluent_kafka.Producer')
    def test_signal_dedup(self, mock_kafka_producer, mock_event_producer):
        mock_instance = MagicMock()
        mock_event_producer.return_value = mock_instance
        mock_instance.producer = MagicMock()

        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.country = "de"
        poller.bidding_zone = "DE-LU"
        poller.kafka_topic = "test"
        poller.last_polled_file = ""
        poller.session = Mock()
        poller.producer = mock_instance
        poller._seen_power = set()
        poller._seen_price = set()
        poller._seen_signal = set()

        poller.session.get = Mock(return_value=Mock(
            status_code=200,
            json=lambda: SAMPLE_SIGNAL
        ))
        poller.session.get.return_value.raise_for_status = Mock()

        count1 = poller.emit_signal()
        assert count1 == 3
        count2 = poller.emit_signal()
        assert count2 == 0


# ---------------------------------------------------------------------------
# Test state persistence
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStatePersistence:

    def test_save_and_load_state(self, tmp_path):
        state_file = str(tmp_path / "state.json")

        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.last_polled_file = state_file
        poller._seen_power = {100, 200, 300}
        poller._seen_price = {400, 500}
        poller._seen_signal = {600}
        poller._save_state()

        poller2 = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller2.last_polled_file = state_file
        poller2._seen_power = set()
        poller2._seen_price = set()
        poller2._seen_signal = set()
        poller2._load_state()

        assert poller2._seen_power == {100, 200, 300}
        assert poller2._seen_price == {400, 500}
        assert poller2._seen_signal == {600}

    def test_load_nonexistent_file(self, tmp_path):
        state_file = str(tmp_path / "nonexistent.json")
        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.last_polled_file = state_file
        poller._seen_power = set()
        poller._seen_price = set()
        poller._seen_signal = set()
        poller._load_state()  # Should not raise
        assert poller._seen_power == set()

    def test_load_corrupt_file(self, tmp_path):
        state_file = str(tmp_path / "corrupt.json")
        with open(state_file, "w") as f:
            f.write("not json")
        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.last_polled_file = state_file
        poller._seen_power = set()
        poller._seen_price = set()
        poller._seen_signal = set()
        poller._load_state()  # Should not raise
        assert poller._seen_power == set()

    def test_empty_state_file_path(self):
        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.last_polled_file = ""
        poller._seen_power = {1, 2, 3}
        poller._seen_price = set()
        poller._seen_signal = set()
        poller._save_state()  # Should not raise
        poller._load_state()  # Should not raise


# ---------------------------------------------------------------------------
# Test data class serialization
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDataClassSerialization:

    def test_public_power_to_json(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        json_str = records[0].to_json()
        parsed = json.loads(json_str)
        assert parsed["country"] == "de"
        assert parsed["wind_onshore_mw"] == 5000.0

    def test_spot_price_to_json(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        json_str = records[0].to_json()
        parsed = json.loads(json_str)
        assert parsed["bidding_zone"] == "DE-LU"
        assert parsed["price_eur_per_mwh"] == 85.50

    def test_grid_signal_to_json(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        json_str = records[0].to_json()
        parsed = json.loads(json_str)
        assert parsed["signal"] == 0
        assert parsed["renewable_share_pct"] == 44.3

    def test_public_power_roundtrip(self):
        records = EnergyChartsPoller.parse_public_power(SAMPLE_PUBLIC_POWER, "de")
        json_str = records[0].to_json()
        restored = PublicPower.from_json(json_str)
        assert restored.country == "de"
        assert restored.wind_onshore_mw == 5000.0

    def test_spot_price_roundtrip(self):
        records = EnergyChartsPoller.parse_price(SAMPLE_PRICE, "de", "DE-LU")
        json_str = records[0].to_json()
        restored = SpotPrice.from_json(json_str)
        assert restored.bidding_zone == "DE-LU"

    def test_grid_signal_roundtrip(self):
        records = EnergyChartsPoller.parse_signal(SAMPLE_SIGNAL, "de")
        json_str = records[0].to_json()
        parsed = json.loads(json_str)
        # Verify JSON preserves the 0 value correctly
        assert parsed["signal"] == 0
        assert parsed["country"] == "de"


# ---------------------------------------------------------------------------
# Test polling intervals
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollingIntervals:

    def test_power_interval(self):
        assert EnergyChartsPoller.POWER_POLL_INTERVAL == 900

    def test_price_interval(self):
        assert EnergyChartsPoller.PRICE_POLL_INTERVAL == 3600

    def test_signal_interval(self):
        assert EnergyChartsPoller.SIGNAL_POLL_INTERVAL == 900


# ---------------------------------------------------------------------------
# Test different countries
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDifferentCountries:

    def test_parse_for_france(self):
        data = {
            "unix_seconds": [1700000000],
            "production_types": [
                {"name": "Nuclear", "data": [40000.0]},
                {"name": "Solar", "data": [5000.0]},
            ],
        }
        records = EnergyChartsPoller.parse_public_power(data, "fr")
        assert records[0].country == "fr"
        assert records[0].nuclear_mw == 40000.0

    def test_parse_price_for_austria(self):
        data = {
            "unix_seconds": [1700000000],
            "price": [70.0],
            "unit": "EUR / MWh",
        }
        records = EnergyChartsPoller.parse_price(data, "at", "AT")
        assert records[0].country == "at"
        assert records[0].bidding_zone == "AT"


# ---------------------------------------------------------------------------
# Test error handling in emit methods
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEmitErrorHandling:

    def test_emit_power_handles_fetch_error(self):
        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.country = "de"
        poller.session = Mock()
        poller.session.get.side_effect = Exception("Network error")
        poller._seen_power = set()
        poller.producer = MagicMock()
        count = poller.emit_public_power()
        assert count == 0

    def test_emit_price_handles_fetch_error(self):
        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.bidding_zone = "DE-LU"
        poller.country = "de"
        poller.session = Mock()
        poller.session.get.side_effect = Exception("Network error")
        poller._seen_price = set()
        poller.producer = MagicMock()
        count = poller.emit_price()
        assert count == 0

    def test_emit_signal_handles_fetch_error(self):
        poller = EnergyChartsPoller.__new__(EnergyChartsPoller)
        poller.country = "de"
        poller.session = Mock()
        poller.session.get.side_effect = Exception("Network error")
        poller._seen_signal = set()
        poller.producer = MagicMock()
        count = poller.emit_signal()
        assert count == 0
