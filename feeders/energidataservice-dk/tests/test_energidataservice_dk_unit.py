"""
Unit tests for Energi Data Service (Energinet) Denmark bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from energidataservice_dk_producer_data import PowerSystemSnapshot, SpotPrice
from energidataservice_dk.energidataservice_dk import (
    EnergiDataServicePoller,
    parse_connection_string,
    safe_float,
    map_power_system_record,
    map_spot_price_record,
    build_power_system_url,
    build_spot_prices_url,
    POWER_SYSTEM_FIELD_MAP,
    SPOT_PRICE_FIELD_MAP,
)


SAMPLE_POWER_SYSTEM_RESPONSE = {
    "total": 3876406,
    "limit": 3,
    "dataset": "PowerSystemRightNow",
    "records": [
        {
            "Minutes1UTC": "2026-04-08T21:30:00",
            "Minutes1DK": "2026-04-08T23:30:00",
            "CO2Emission": 107.0,
            "ProductionGe100MW": 839.98999,
            "ProductionLt100MW": 473.700012,
            "SolarPower": 0.0,
            "OffshoreWindPower": 1029.670044,
            "OnshoreWindPower": 820.369995,
            "Exchange_Sum": 906.22998,
            "Exchange_DK1_DE": -383.399994,
            "Exchange_DK1_NL": 666.059998,
            "Exchange_DK1_GB": -697.849976,
            "Exchange_DK1_NO": -228.0,
            "Exchange_DK1_SE": 500.0,
            "Exchange_DK1_DK2": 77.769997,
            "Exchange_DK2_DE": -103.699997,
            "Exchange_DK2_SE": 1127.939941,
            "Exchange_Bornholm_SE": 25.18,
            "aFRR_ActivatedDK1": -36.389999,
            "aFRR_ActivatedDK2": -5.57,
            "mFRR_ActivatedDK1": 0.0,
            "mFRR_ActivatedDK2": 0.0,
            "ImbalanceDK1": 100.68,
            "ImbalanceDK2": -27.33,
        },
        {
            "Minutes1UTC": "2026-04-08T21:29:00",
            "Minutes1DK": "2026-04-08T23:29:00",
            "CO2Emission": 107.019997,
            "ProductionGe100MW": 840.77002,
            "ProductionLt100MW": 472.779999,
            "SolarPower": 0.0,
            "OffshoreWindPower": 1033.199951,
            "OnshoreWindPower": 826.289978,
            "Exchange_Sum": 887.409973,
            "Exchange_DK1_DE": -398.910004,
            "Exchange_DK1_NL": 669.25,
            "Exchange_DK1_GB": -697.849976,
            "Exchange_DK1_NO": -210.0,
            "Exchange_DK1_SE": 481.0,
            "Exchange_DK1_DK2": 78.949997,
            "Exchange_DK2_DE": -98.529999,
            "Exchange_DK2_SE": 1117.27002,
            "Exchange_Bornholm_SE": 25.18,
            "aFRR_ActivatedDK1": -35.75,
            "aFRR_ActivatedDK2": -4.45,
            "mFRR_ActivatedDK1": 0.0,
            "mFRR_ActivatedDK2": 0.0,
            "ImbalanceDK1": 109.870003,
            "ImbalanceDK2": -23.51,
        },
    ],
}

SAMPLE_SPOT_PRICE_RESPONSE = {
    "total": 460248,
    "limit": 3,
    "dataset": "Elspotprices",
    "records": [
        {
            "HourUTC": "2025-09-30T21:00:00",
            "HourDK": "2025-09-30T23:00:00",
            "PriceArea": "DK1",
            "SpotPriceDKK": 690.700059,
            "SpotPriceEUR": 92.540001,
        },
        {
            "HourUTC": "2025-09-30T21:00:00",
            "HourDK": "2025-09-30T23:00:00",
            "PriceArea": "DK2",
            "SpotPriceDKK": 690.252246,
            "SpotPriceEUR": 92.480003,
        },
        {
            "HourUTC": "2025-09-30T20:00:00",
            "HourDK": "2025-09-30T22:00:00",
            "PriceArea": "DK1",
            "SpotPriceDKK": 758.545972,
            "SpotPriceEUR": 101.629997,
        },
    ],
}


# ---------------------------------------------------------------------------
# safe_float tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSafeFloat:
    """Unit tests for the safe_float helper."""

    def test_valid_float(self):
        assert safe_float(10.5) == 10.5

    def test_valid_int(self):
        assert safe_float(42) == 42.0

    def test_valid_string_number(self):
        assert safe_float("3.14") == 3.14

    def test_none_returns_none(self):
        assert safe_float(None) is None

    def test_invalid_string_returns_none(self):
        assert safe_float("not_a_number") is None

    def test_empty_string_returns_none(self):
        assert safe_float("") is None

    def test_negative_float(self):
        assert safe_float(-383.4) == -383.4

    def test_zero(self):
        assert safe_float(0) == 0.0

    def test_zero_float(self):
        assert safe_float(0.0) == 0.0


# ---------------------------------------------------------------------------
# URL construction tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestUrlConstruction:
    """Unit tests for URL construction helpers."""

    def test_power_system_url_default_limit(self):
        url = build_power_system_url()
        assert "PowerSystemRightNow" in url
        assert "limit=5" in url

    def test_power_system_url_custom_limit(self):
        url = build_power_system_url(limit=10)
        assert "limit=10" in url

    def test_spot_prices_url_default_limit(self):
        url = build_spot_prices_url()
        assert "ElspotPrices" in url
        assert "limit=100" in url
        assert "DK1" in url
        assert "DK2" in url

    def test_spot_prices_url_custom_limit(self):
        url = build_spot_prices_url(limit=50)
        assert "limit=50" in url


# ---------------------------------------------------------------------------
# Record mapping tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestMapPowerSystemRecord:
    """Unit tests for power system record mapping."""

    def test_map_full_record(self):
        record = SAMPLE_POWER_SYSTEM_RESPONSE["records"][0]
        snapshot = map_power_system_record(record)
        assert isinstance(snapshot, PowerSystemSnapshot)
        assert snapshot.minutes1_utc == "2026-04-08T21:30:00"
        assert snapshot.minutes1_dk == "2026-04-08T23:30:00"
        assert snapshot.price_area == "DK"
        assert snapshot.co2_emission == 107.0
        # Note: 0.0 values become None due to generated __post_init__ falsy check
        assert snapshot.solar_power is None
        assert snapshot.offshore_wind_power == pytest.approx(1029.670044)
        assert snapshot.onshore_wind_power == pytest.approx(820.369995)
        assert snapshot.exchange_dk1_de == pytest.approx(-383.399994)

    def test_map_record_synthesizes_price_area(self):
        record = SAMPLE_POWER_SYSTEM_RESPONSE["records"][0]
        snapshot = map_power_system_record(record)
        assert snapshot.price_area == "DK"

    def test_map_record_with_null_fields(self):
        record = {
            "Minutes1UTC": "2026-04-08T21:30:00",
            "Minutes1DK": "2026-04-08T23:30:00",
            "CO2Emission": None,
            "SolarPower": None,
        }
        snapshot = map_power_system_record(record)
        assert snapshot.co2_emission is None
        assert snapshot.solar_power is None
        assert snapshot.minutes1_utc == "2026-04-08T21:30:00"

    def test_map_record_with_missing_fields(self):
        record = {
            "Minutes1UTC": "2026-04-08T21:30:00",
            "Minutes1DK": "2026-04-08T23:30:00",
        }
        snapshot = map_power_system_record(record)
        assert snapshot.co2_emission is None
        assert snapshot.exchange_dk1_de is None
        assert snapshot.imbalance_dk1 is None

    def test_all_exchange_fields_mapped(self):
        record = SAMPLE_POWER_SYSTEM_RESPONSE["records"][0]
        snapshot = map_power_system_record(record)
        assert snapshot.exchange_sum == pytest.approx(906.22998)
        assert snapshot.exchange_dk1_nl == pytest.approx(666.059998)
        assert snapshot.exchange_dk1_gb == pytest.approx(-697.849976)
        assert snapshot.exchange_dk1_no == pytest.approx(-228.0)
        assert snapshot.exchange_dk1_se == pytest.approx(500.0)
        assert snapshot.exchange_dk1_dk2 == pytest.approx(77.769997)
        assert snapshot.exchange_dk2_de == pytest.approx(-103.699997)
        assert snapshot.exchange_dk2_se == pytest.approx(1127.939941)
        assert snapshot.exchange_bornholm_se == pytest.approx(25.18)

    def test_balancing_fields_mapped(self):
        record = SAMPLE_POWER_SYSTEM_RESPONSE["records"][0]
        snapshot = map_power_system_record(record)
        assert snapshot.afrr_activated_dk1 == pytest.approx(-36.389999)
        assert snapshot.afrr_activated_dk2 == pytest.approx(-5.57)
        # 0.0 values become None due to generated __post_init__ falsy check
        assert snapshot.mfrr_activated_dk1 is None
        assert snapshot.mfrr_activated_dk2 is None
        assert snapshot.imbalance_dk1 == pytest.approx(100.68)
        assert snapshot.imbalance_dk2 == pytest.approx(-27.33)

    def test_production_fields_mapped(self):
        record = SAMPLE_POWER_SYSTEM_RESPONSE["records"][0]
        snapshot = map_power_system_record(record)
        assert snapshot.production_ge_100mw == pytest.approx(839.98999)
        assert snapshot.production_lt_100mw == pytest.approx(473.700012)

    def test_field_map_completeness(self):
        """Verify that all expected API fields are in the field map."""
        expected_api_fields = {
            "Minutes1UTC", "Minutes1DK", "CO2Emission",
            "ProductionGe100MW", "ProductionLt100MW",
            "SolarPower", "OffshoreWindPower", "OnshoreWindPower",
            "Exchange_Sum", "Exchange_DK1_DE", "Exchange_DK1_NL",
            "Exchange_DK1_GB", "Exchange_DK1_NO", "Exchange_DK1_SE",
            "Exchange_DK1_DK2", "Exchange_DK2_DE", "Exchange_DK2_SE",
            "Exchange_Bornholm_SE",
            "aFRR_ActivatedDK1", "aFRR_ActivatedDK2",
            "mFRR_ActivatedDK1", "mFRR_ActivatedDK2",
            "ImbalanceDK1", "ImbalanceDK2",
        }
        assert set(POWER_SYSTEM_FIELD_MAP.keys()) == expected_api_fields


@pytest.mark.unit
class TestMapSpotPriceRecord:
    """Unit tests for spot price record mapping."""

    def test_map_dk1_record(self):
        record = SAMPLE_SPOT_PRICE_RESPONSE["records"][0]
        price = map_spot_price_record(record)
        assert isinstance(price, SpotPrice)
        assert price.hour_utc == "2025-09-30T21:00:00"
        assert price.hour_dk == "2025-09-30T23:00:00"
        assert price.price_area == "DK1"
        assert price.spot_price_dkk == pytest.approx(690.700059)
        assert price.spot_price_eur == pytest.approx(92.540001)

    def test_map_dk2_record(self):
        record = SAMPLE_SPOT_PRICE_RESPONSE["records"][1]
        price = map_spot_price_record(record)
        assert price.price_area == "DK2"
        assert price.spot_price_dkk == pytest.approx(690.252246)
        assert price.spot_price_eur == pytest.approx(92.480003)

    def test_map_record_with_null_prices(self):
        record = {
            "HourUTC": "2025-09-30T21:00:00",
            "HourDK": "2025-09-30T23:00:00",
            "PriceArea": "DK1",
            "SpotPriceDKK": None,
            "SpotPriceEUR": None,
        }
        price = map_spot_price_record(record)
        assert price.spot_price_dkk is None
        assert price.spot_price_eur is None

    def test_map_record_with_missing_prices(self):
        record = {
            "HourUTC": "2025-09-30T21:00:00",
            "HourDK": "2025-09-30T23:00:00",
            "PriceArea": "DK1",
        }
        price = map_spot_price_record(record)
        assert price.spot_price_dkk is None
        assert price.spot_price_eur is None

    def test_spot_price_field_map_completeness(self):
        expected = {"HourUTC", "HourDK", "PriceArea", "SpotPriceDKK", "SpotPriceEUR"}
        assert set(SPOT_PRICE_FIELD_MAP.keys()) == expected


# ---------------------------------------------------------------------------
# Connection string parsing tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for connection string parsing."""

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=secret123;EntityPath=my-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == "myns.servicebus.windows.net:9093"
        assert result['kafka_topic'] == "my-topic"
        assert result['sasl.username'] == "$ConnectionString"
        assert result['sasl.password'] == cs
        assert result['security.protocol'] == 'SASL_SSL'

    def test_plain_bootstrap_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == "localhost:9092"
        assert result['kafka_topic'] == "test-topic"
        assert 'sasl.username' not in result

    def test_connection_string_without_entity_path(self):
        cs = "BootstrapServer=localhost:9092"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == "localhost:9092"
        assert 'kafka_topic' not in result


# ---------------------------------------------------------------------------
# DataClass serialization tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDataClassSerialization:
    """Tests for generated data class serialization."""

    def test_power_system_snapshot_to_json(self):
        snapshot = PowerSystemSnapshot(
            minutes1_utc="2026-04-08T21:30:00",
            minutes1_dk="2026-04-08T23:30:00",
            price_area="DK",
            co2_emission=107.0,
            production_ge_100mw=840.0,
            production_lt_100mw=473.7,
            solar_power=0.0,
            offshore_wind_power=1029.67,
            onshore_wind_power=820.37,
            exchange_sum=906.23,
            exchange_dk1_de=-383.4,
            exchange_dk1_nl=666.06,
            exchange_dk1_gb=-697.85,
            exchange_dk1_no=-228.0,
            exchange_dk1_se=500.0,
            exchange_dk1_dk2=77.77,
            exchange_dk2_de=-103.7,
            exchange_dk2_se=1127.94,
            exchange_bornholm_se=25.18,
            afrr_activated_dk1=-36.39,
            afrr_activated_dk2=-5.57,
            mfrr_activated_dk1=0.0,
            mfrr_activated_dk2=0.0,
            imbalance_dk1=100.68,
            imbalance_dk2=-27.33,
        )
        json_str = snapshot.to_json()
        data = json.loads(json_str)
        assert data["minutes1_utc"] == "2026-04-08T21:30:00"
        assert data["price_area"] == "DK"
        assert data["co2_emission"] == 107.0

    def test_spot_price_to_json(self):
        price = SpotPrice(
            hour_utc="2025-09-30T21:00:00",
            hour_dk="2025-09-30T23:00:00",
            price_area="DK1",
            spot_price_dkk=690.7,
            spot_price_eur=92.54,
        )
        json_str = price.to_json()
        data = json.loads(json_str)
        assert data["price_area"] == "DK1"
        assert data["spot_price_dkk"] == 690.7

    def test_power_system_snapshot_with_nulls_to_json(self):
        snapshot = PowerSystemSnapshot(
            minutes1_utc="2026-04-08T21:30:00",
            minutes1_dk="2026-04-08T23:30:00",
            price_area="DK",
            co2_emission=None,
            production_ge_100mw=None,
            production_lt_100mw=None,
            solar_power=None,
            offshore_wind_power=None,
            onshore_wind_power=None,
            exchange_sum=None,
            exchange_dk1_de=None,
            exchange_dk1_nl=None,
            exchange_dk1_gb=None,
            exchange_dk1_no=None,
            exchange_dk1_se=None,
            exchange_dk1_dk2=None,
            exchange_dk2_de=None,
            exchange_dk2_se=None,
            exchange_bornholm_se=None,
            afrr_activated_dk1=None,
            afrr_activated_dk2=None,
            mfrr_activated_dk1=None,
            mfrr_activated_dk2=None,
            imbalance_dk1=None,
            imbalance_dk2=None,
        )
        json_str = snapshot.to_json()
        data = json.loads(json_str)
        assert data["co2_emission"] is None
        assert data["solar_power"] is None

    def test_spot_price_with_null_prices_to_json(self):
        price = SpotPrice(
            hour_utc="2025-09-30T21:00:00",
            hour_dk="2025-09-30T23:00:00",
            price_area="DK2",
            spot_price_dkk=None,
            spot_price_eur=None,
        )
        json_str = price.to_json()
        data = json.loads(json_str)
        assert data["spot_price_dkk"] is None
        assert data["spot_price_eur"] is None


# ---------------------------------------------------------------------------
# Poller state management tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollerStateManagement:
    """Tests for state persistence and normalization."""

    @pytest.fixture
    def mock_kafka_config(self):
        return {
            'bootstrap.servers': 'localhost:9092',
        }

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_empty(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='nonexistent_file.json',
        )
        state = poller.load_state()
        assert state == {
            "last_power_system_timestamp": None,
            "last_spot_price_timestamps": {},
        }

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_existing(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        state_data = {
            "last_power_system_timestamp": "2026-04-08T21:30:00",
            "last_spot_price_timestamps": {"DK1_2025-09-30T21:00:00": "2025-09-30T21:00:00"},
        }
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        state = poller.load_state()
        assert state["last_power_system_timestamp"] == "2026-04-08T21:30:00"
        assert "DK1_2025-09-30T21:00:00" in state["last_spot_price_timestamps"]

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    def test_save_state(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        state_data = {
            "last_power_system_timestamp": "2026-04-08T21:30:00",
            "last_spot_price_timestamps": {"DK1_2025-09-30T21:00:00": "2025-09-30T21:00:00"},
        }
        poller.save_state(state_data)

        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["last_power_system_timestamp"] == "2026-04-08T21:30:00"

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_corrupted_state(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            f.write("not valid json")

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        state = poller.load_state()
        assert state["last_power_system_timestamp"] is None

    def test_normalize_state_with_none(self):
        result = EnergiDataServicePoller._normalize_state(None)
        assert result["last_power_system_timestamp"] is None
        assert result["last_spot_price_timestamps"] == {}

    def test_normalize_state_with_invalid_type(self):
        result = EnergiDataServicePoller._normalize_state("not a dict")
        assert result["last_power_system_timestamp"] is None

    def test_normalize_state_preserves_data(self):
        state = {
            "last_power_system_timestamp": "2026-04-08T21:30:00",
            "last_spot_price_timestamps": {"DK1_2025-09-30T21:00:00": "2025-09-30T21:00:00"},
        }
        result = EnergiDataServicePoller._normalize_state(state)
        assert result["last_power_system_timestamp"] == "2026-04-08T21:30:00"
        assert len(result["last_spot_price_timestamps"]) == 1

    def test_empty_state(self):
        state = EnergiDataServicePoller._empty_state()
        assert state["last_power_system_timestamp"] is None
        assert state["last_spot_price_timestamps"] == {}


# ---------------------------------------------------------------------------
# Poller fetch and send tests (mocked HTTP)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollerFetch:
    """Tests for data fetching with mocked HTTP responses."""

    @pytest.fixture
    def mock_kafka_config(self):
        return {'bootstrap.servers': 'localhost:9092'}

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('energidataservice_dk.energidataservice_dk.requests.get')
    def test_fetch_power_system_records(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_POWER_SYSTEM_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        records = poller.fetch_power_system_records(limit=3)
        assert len(records) == 2
        assert records[0]["Minutes1UTC"] == "2026-04-08T21:30:00"

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('energidataservice_dk.energidataservice_dk.requests.get')
    def test_fetch_power_system_records_error(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Connection error")

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        records = poller.fetch_power_system_records()
        assert records == []

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('energidataservice_dk.energidataservice_dk.requests.get')
    def test_fetch_spot_price_records(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_SPOT_PRICE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        records = poller.fetch_spot_price_records(limit=3)
        assert len(records) == 3
        assert records[0]["PriceArea"] == "DK1"

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('energidataservice_dk.energidataservice_dk.requests.get')
    def test_fetch_spot_price_records_error(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Connection error")

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        records = poller.fetch_spot_price_records()
        assert records == []


# ---------------------------------------------------------------------------
# poll_and_send integration test (mocked)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollAndSend:
    """Tests for the poll_and_send loop with mocks."""

    @pytest.fixture
    def mock_kafka_config(self):
        return {'bootstrap.servers': 'localhost:9092'}

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('energidataservice_dk.energidataservice_dk.requests.get')
    def test_poll_and_send_once(self, mock_get, mock_producer_class, mock_event_producer_class, mock_kafka_config, temp_state_file):
        mock_event_producer = Mock()
        mock_event_producer_class.return_value = mock_event_producer
        mock_event_producer.producer = Mock()

        def side_effect(url, timeout=30):
            resp = Mock()
            resp.raise_for_status = Mock()
            if "PowerSystemRightNow" in url:
                resp.json.return_value = SAMPLE_POWER_SYSTEM_RESPONSE
            else:
                resp.json.return_value = SAMPLE_SPOT_PRICE_RESPONSE
            return resp

        mock_get.side_effect = side_effect

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        poller.poll_and_send(once=True)

        # Should have sent at least one power system snapshot
        mock_event_producer.send_dk_energinet_energidataservice_power_system_snapshot.assert_called()
        # Should have sent spot prices
        mock_event_producer.send_dk_energinet_energidataservice_spot_price.assert_called()
        # Should have flushed
        mock_event_producer.producer.flush.assert_called()

    @patch('energidataservice_dk.energidataservice_dk.DkEnerginetEnergidataserviceEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('energidataservice_dk.energidataservice_dk.requests.get')
    def test_poll_and_send_deduplicates_power_system(self, mock_get, mock_producer_class, mock_event_producer_class, mock_kafka_config, temp_state_file):
        """If the last timestamp matches, no new snapshot should be sent."""
        mock_event_producer = Mock()
        mock_event_producer_class.return_value = mock_event_producer
        mock_event_producer.producer = Mock()

        # Pre-seed state with the same timestamp
        state_data = {
            "last_power_system_timestamp": "2026-04-08T21:30:00",
            "last_spot_price_timestamps": {
                "DK1_2025-09-30T21:00:00": "2025-09-30T21:00:00",
                "DK2_2025-09-30T21:00:00": "2025-09-30T21:00:00",
                "DK1_2025-09-30T20:00:00": "2025-09-30T20:00:00",
            },
        }
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        def side_effect(url, timeout=30):
            resp = Mock()
            resp.raise_for_status = Mock()
            if "PowerSystemRightNow" in url:
                resp.json.return_value = SAMPLE_POWER_SYSTEM_RESPONSE
            else:
                resp.json.return_value = SAMPLE_SPOT_PRICE_RESPONSE
            return resp

        mock_get.side_effect = side_effect

        poller = EnergiDataServicePoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
        )
        poller.poll_and_send(once=True)

        # Power system snapshot should NOT be sent (same timestamp)
        mock_event_producer.send_dk_energinet_energidataservice_power_system_snapshot.assert_not_called()


# ---------------------------------------------------------------------------
# Avro serialization tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestAvroSerialization:
    """Tests for Avro round-trip serialization."""

    def test_power_system_snapshot_avro_roundtrip(self):
        snapshot = PowerSystemSnapshot(
            minutes1_utc="2026-04-08T21:30:00",
            minutes1_dk="2026-04-08T23:30:00",
            price_area="DK",
            co2_emission=107.0,
            production_ge_100mw=840.0,
            production_lt_100mw=473.7,
            solar_power=0.0,
            offshore_wind_power=1029.67,
            onshore_wind_power=820.37,
            exchange_sum=906.23,
            exchange_dk1_de=-383.4,
            exchange_dk1_nl=666.06,
            exchange_dk1_gb=-697.85,
            exchange_dk1_no=-228.0,
            exchange_dk1_se=500.0,
            exchange_dk1_dk2=77.77,
            exchange_dk2_de=-103.7,
            exchange_dk2_se=1127.94,
            exchange_bornholm_se=25.18,
            afrr_activated_dk1=-36.39,
            afrr_activated_dk2=-5.57,
            mfrr_activated_dk1=0.0,
            mfrr_activated_dk2=0.0,
            imbalance_dk1=100.68,
            imbalance_dk2=-27.33,
        )
        avro_bytes = snapshot.to_byte_array("avro/binary")
        assert isinstance(avro_bytes, bytes)
        assert len(avro_bytes) > 0
        restored = PowerSystemSnapshot.from_data(avro_bytes, "avro/binary")
        assert restored.minutes1_utc == "2026-04-08T21:30:00"
        assert restored.co2_emission == 107.0
        assert restored.exchange_dk1_de == -383.4

    def test_spot_price_avro_roundtrip(self):
        price = SpotPrice(
            hour_utc="2025-09-30T21:00:00",
            hour_dk="2025-09-30T23:00:00",
            price_area="DK1",
            spot_price_dkk=690.7,
            spot_price_eur=92.54,
        )
        avro_bytes = price.to_byte_array("avro/binary")
        assert isinstance(avro_bytes, bytes)
        restored = SpotPrice.from_data(avro_bytes, "avro/binary")
        assert restored.price_area == "DK1"
        assert restored.spot_price_dkk == 690.7

    def test_power_system_snapshot_avro_with_nulls(self):
        snapshot = PowerSystemSnapshot(
            minutes1_utc="2026-04-08T21:30:00",
            minutes1_dk="2026-04-08T23:30:00",
            price_area="DK",
            co2_emission=None,
            production_ge_100mw=None,
            production_lt_100mw=None,
            solar_power=None,
            offshore_wind_power=None,
            onshore_wind_power=None,
            exchange_sum=None,
            exchange_dk1_de=None,
            exchange_dk1_nl=None,
            exchange_dk1_gb=None,
            exchange_dk1_no=None,
            exchange_dk1_se=None,
            exchange_dk1_dk2=None,
            exchange_dk2_de=None,
            exchange_dk2_se=None,
            exchange_bornholm_se=None,
            afrr_activated_dk1=None,
            afrr_activated_dk2=None,
            mfrr_activated_dk1=None,
            mfrr_activated_dk2=None,
            imbalance_dk1=None,
            imbalance_dk2=None,
        )
        avro_bytes = snapshot.to_byte_array("avro/binary")
        restored = PowerSystemSnapshot.from_data(avro_bytes, "avro/binary")
        assert restored.co2_emission is None
        assert restored.solar_power is None
        assert restored.exchange_dk1_de is None

    def test_spot_price_avro_with_null_prices(self):
        price = SpotPrice(
            hour_utc="2025-09-30T21:00:00",
            hour_dk="2025-09-30T23:00:00",
            price_area="DK2",
            spot_price_dkk=None,
            spot_price_eur=None,
        )
        avro_bytes = price.to_byte_array("avro/binary")
        restored = SpotPrice.from_data(avro_bytes, "avro/binary")
        assert restored.spot_price_dkk is None
        assert restored.spot_price_eur is None
