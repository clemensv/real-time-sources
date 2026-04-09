"""
Unit tests for Elexon BMRS (GB Electricity Market) bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock
from elexon_bmrs_producer_data import GenerationMix, DemandOutturn
from elexon_bmrs.elexon_bmrs import (
    ElexonBMRSPoller,
    parse_connection_string,
    FUEL_TYPE_FIELD_MAP,
)


SAMPLE_GENERATION_RESPONSE = [
    {
        "startTime": "2026-04-07T21:00:00Z",
        "settlementPeriod": 45,
        "data": [
            {"fuelType": "BIOMASS", "generation": 2046},
            {"fuelType": "CCGT", "generation": 3948},
            {"fuelType": "COAL", "generation": 0},
            {"fuelType": "INTELEC", "generation": 998},
            {"fuelType": "INTFR", "generation": 1506},
            {"fuelType": "INTIFA2", "generation": 992},
            {"fuelType": "INTNEM", "generation": 138},
            {"fuelType": "INTNSL", "generation": 712},
            {"fuelType": "NPSHYD", "generation": 529},
            {"fuelType": "NUCLEAR", "generation": 5074},
            {"fuelType": "OCGT", "generation": 5},
            {"fuelType": "OIL", "generation": 0},
            {"fuelType": "OTHER", "generation": 445},
            {"fuelType": "PS", "generation": 862},
            {"fuelType": "WIND", "generation": 11233},
        ],
    },
    {
        "startTime": "2026-04-07T21:30:00Z",
        "settlementPeriod": 46,
        "data": [
            {"fuelType": "BIOMASS", "generation": 2052},
            {"fuelType": "CCGT", "generation": 3981},
            {"fuelType": "COAL", "generation": 0},
            {"fuelType": "NUCLEAR", "generation": 5070},
            {"fuelType": "WIND", "generation": 11100},
        ],
    },
]

SAMPLE_DEMAND_RESPONSE = {
    "metadata": {"datasets": ["INDO", "ITSDO"]},
    "data": [
        {
            "publishTime": "2026-03-11T00:30:00Z",
            "startTime": "2026-03-11T00:00:00Z",
            "settlementDate": "2026-03-11",
            "settlementPeriod": 1,
            "initialDemandOutturn": 22416,
            "initialTransmissionSystemDemandOutturn": 27678,
        },
        {
            "publishTime": "2026-03-11T01:00:00Z",
            "startTime": "2026-03-11T00:30:00Z",
            "settlementDate": "2026-03-11",
            "settlementPeriod": 2,
            "initialDemandOutturn": 23267,
            "initialTransmissionSystemDemandOutturn": 28328,
        },
    ],
}


@pytest.mark.unit
class TestFuelTypeFieldMap:
    """Unit tests for the FUEL_TYPE_FIELD_MAP constant"""

    def test_biomass_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["BIOMASS"] == "biomass_mw"

    def test_ccgt_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["CCGT"] == "ccgt_mw"

    def test_coal_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["COAL"] == "coal_mw"

    def test_nuclear_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["NUCLEAR"] == "nuclear_mw"

    def test_wind_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["WIND"] == "wind_mw"

    def test_ocgt_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["OCGT"] == "ocgt_mw"

    def test_oil_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["OIL"] == "oil_mw"

    def test_npshyd_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["NPSHYD"] == "npshyd_mw"

    def test_ps_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["PS"] == "ps_mw"

    def test_intfr_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["INTFR"] == "intfr_mw"

    def test_intned_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["INTNED"] == "intned_mw"

    def test_intnem_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["INTNEM"] == "intnem_mw"

    def test_intelec_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["INTELEC"] == "intelec_mw"

    def test_intifa2_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["INTIFA2"] == "intifa2_mw"

    def test_intnsl_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["INTNSL"] == "intnsl_mw"

    def test_intvkl_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["INTVKL"] == "intvkl_mw"

    def test_other_mapping(self):
        assert FUEL_TYPE_FIELD_MAP["OTHER"] == "other_mw"

    def test_total_fuel_types(self):
        assert len(FUEL_TYPE_FIELD_MAP) == 17


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for connection string parsing"""

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == cs
        assert result["security.protocol"] == "SASL_SSL"

    def test_bootstrap_server_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "test-topic"
        assert "sasl.username" not in result

    def test_empty_connection_string(self):
        result = parse_connection_string("")
        assert result == {}

    def test_missing_entity_path(self):
        cs = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123"
        result = parse_connection_string(cs)
        assert "kafka_topic" not in result
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"

    def test_connection_string_no_sasl_when_bootstrap_only(self):
        cs = "BootstrapServer=broker1:9092;EntityPath=my-topic"
        result = parse_connection_string(cs)
        assert "security.protocol" not in result
        assert "sasl.mechanism" not in result


@pytest.mark.unit
class TestElexonBMRSPoller:
    """Unit tests for the ElexonBMRSPoller class"""

    @pytest.fixture
    def mock_kafka_config(self):
        return {
            "bootstrap.servers": "localhost:9092",
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL",
            "sasl.username": "test_user",
            "sasl.password": "test_password",
        }

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_init(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test ElexonBMRSPoller initialization"""
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = ElexonBMRSPoller(
            kafka_config=mock_kafka_config,
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        assert poller.kafka_topic == "test-topic"
        assert poller.last_polled_file == temp_state_file
        mock_producer_class.assert_called_once_with(mock_kafka_config)

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_load_state_empty(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        """Test loading state when no state file exists"""
        poller = ElexonBMRSPoller(
            kafka_config=mock_kafka_config,
            kafka_topic="test-topic",
            last_polled_file="nonexistent_bmrs_state.json",
        )

        state = poller.load_state()
        assert state == {"generation": {}, "demand": {}}

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_load_state_existing(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test loading state from existing state file"""
        state_data = {
            "generation": {"45_2026-04-07T21:00:00+00:00": "2026-04-07T21:00:00+00:00"},
            "demand": {"1_2026-03-11T00:00:00+00:00": "2026-03-11T00:00:00+00:00"},
        }
        with open(temp_state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f)

        poller = ElexonBMRSPoller(
            kafka_config=mock_kafka_config,
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        state = poller.load_state()
        assert "45_2026-04-07T21:00:00+00:00" in state["generation"]
        assert "1_2026-03-11T00:00:00+00:00" in state["demand"]

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_load_state_corrupt_json(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test loading state from corrupt state file"""
        with open(temp_state_file, "w", encoding="utf-8") as f:
            f.write("not valid json{{{")

        poller = ElexonBMRSPoller(
            kafka_config=mock_kafka_config,
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        state = poller.load_state()
        assert state == {"generation": {}, "demand": {}}

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_save_state(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Test saving state to state file"""
        poller = ElexonBMRSPoller(
            kafka_config=mock_kafka_config,
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        state_data = {
            "generation": {"45_2026-04-07T21:00:00+00:00": "2026-04-07T21:00:00+00:00"},
            "demand": {"1_2026-03-11T00:00:00+00:00": "2026-03-11T00:00:00+00:00"},
        }
        poller.save_state(state_data)

        with open(temp_state_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert saved["generation"]["45_2026-04-07T21:00:00+00:00"] == "2026-04-07T21:00:00+00:00"
        assert saved["demand"]["1_2026-03-11T00:00:00+00:00"] == "2026-03-11T00:00:00+00:00"


@pytest.mark.unit
class TestParseGenerationResponse:
    """Unit tests for generation response parsing"""

    def test_parse_full_response(self):
        """Test parsing a complete generation response"""
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert len(results) == 2

    def test_first_record_settlement_period(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].settlement_period == 45

    def test_first_record_start_time(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].start_time == datetime(2026, 4, 7, 21, 0, 0, tzinfo=timezone.utc)

    def test_first_record_biomass(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].biomass_mw == 2046.0

    def test_first_record_ccgt(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].ccgt_mw == 3948.0

    def test_first_record_coal(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].coal_mw == 0.0

    def test_first_record_nuclear(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].nuclear_mw == 5074.0

    def test_first_record_wind(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].wind_mw == 11233.0

    def test_first_record_ocgt(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].ocgt_mw == 5.0

    def test_first_record_oil(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].oil_mw == 0.0

    def test_first_record_npshyd(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].npshyd_mw == 529.0

    def test_first_record_ps(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].ps_mw == 862.0

    def test_first_record_intfr(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].intfr_mw == 1506.0

    def test_first_record_intifa2(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].intifa2_mw == 992.0

    def test_first_record_intnsl(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].intnsl_mw == 712.0

    def test_first_record_intelec(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].intelec_mw == 998.0

    def test_first_record_intnem(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].intnem_mw == 138.0

    def test_first_record_other(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[0].other_mw == 445.0

    def test_first_record_missing_fuel_types_are_none(self):
        """Fuel types not in the API response should be None"""
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        # INTNED and INTVKL are not in the first record
        assert results[0].intned_mw is None
        assert results[0].intvkl_mw is None

    def test_second_record_partial_data(self):
        """Second record with fewer fuel types should still parse"""
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert results[1].settlement_period == 46
        assert results[1].biomass_mw == 2052.0
        assert results[1].ccgt_mw == 3981.0
        assert results[1].nuclear_mw == 5070.0
        assert results[1].wind_mw == 11100.0
        # Missing fuel types should be None
        assert results[1].ocgt_mw is None
        assert results[1].oil_mw is None
        assert results[1].npshyd_mw is None

    def test_empty_response(self):
        results = ElexonBMRSPoller.parse_generation_response([])
        assert results == []

    def test_non_list_response(self):
        results = ElexonBMRSPoller.parse_generation_response("not a list")
        assert results == []

    def test_record_missing_settlement_period(self):
        data = [{"startTime": "2026-04-07T21:00:00Z", "data": []}]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert results == []

    def test_record_missing_start_time(self):
        data = [{"settlementPeriod": 45, "data": []}]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert results == []

    def test_record_invalid_start_time(self):
        data = [{"startTime": "not-a-date", "settlementPeriod": 45, "data": []}]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert results == []

    def test_empty_data_array(self):
        data = [{"startTime": "2026-04-07T21:00:00Z", "settlementPeriod": 45, "data": []}]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert len(results) == 1
        assert results[0].biomass_mw is None
        assert results[0].wind_mw is None

    def test_unknown_fuel_type_ignored(self):
        data = [{
            "startTime": "2026-04-07T21:00:00Z",
            "settlementPeriod": 45,
            "data": [
                {"fuelType": "UNKNOWN_FUEL", "generation": 999},
                {"fuelType": "WIND", "generation": 5000},
            ],
        }]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert len(results) == 1
        assert results[0].wind_mw == 5000.0

    def test_null_generation_value(self):
        data = [{
            "startTime": "2026-04-07T21:00:00Z",
            "settlementPeriod": 45,
            "data": [{"fuelType": "WIND", "generation": None}],
        }]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert results[0].wind_mw is None

    def test_generation_mix_is_dataclass(self):
        results = ElexonBMRSPoller.parse_generation_response(SAMPLE_GENERATION_RESPONSE)
        assert isinstance(results[0], GenerationMix)


@pytest.mark.unit
class TestParseDemandResponse:
    """Unit tests for demand response parsing"""

    def test_parse_full_response(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert len(results) == 2

    def test_first_record_settlement_period(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert results[0].settlement_period == 1

    def test_first_record_settlement_date(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert results[0].settlement_date == "2026-03-11"

    def test_first_record_start_time(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert results[0].start_time == datetime(2026, 3, 11, 0, 0, 0, tzinfo=timezone.utc)

    def test_first_record_publish_time(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert results[0].publish_time == datetime(2026, 3, 11, 0, 30, 0, tzinfo=timezone.utc)

    def test_first_record_demand_outturn(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert results[0].initial_demand_outturn_mw == 22416.0

    def test_first_record_transmission_demand(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert results[0].initial_transmission_system_demand_outturn_mw == 27678.0

    def test_second_record_values(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert results[1].settlement_period == 2
        assert results[1].initial_demand_outturn_mw == 23267.0

    def test_empty_data_array(self):
        results = ElexonBMRSPoller.parse_demand_response({"metadata": {}, "data": []})
        assert results == []

    def test_non_dict_response(self):
        results = ElexonBMRSPoller.parse_demand_response("not a dict")
        assert results == []

    def test_missing_settlement_period(self):
        data = {"data": [{"startTime": "2026-03-11T00:00:00Z", "settlementDate": "2026-03-11"}]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert results == []

    def test_missing_settlement_date(self):
        data = {"data": [{"startTime": "2026-03-11T00:00:00Z", "settlementPeriod": 1}]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert results == []

    def test_missing_start_time(self):
        data = {"data": [{"settlementPeriod": 1, "settlementDate": "2026-03-11"}]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert results == []

    def test_null_demand_values(self):
        data = {"data": [{
            "publishTime": "2026-03-11T00:30:00Z",
            "startTime": "2026-03-11T00:00:00Z",
            "settlementDate": "2026-03-11",
            "settlementPeriod": 1,
            "initialDemandOutturn": None,
            "initialTransmissionSystemDemandOutturn": None,
        }]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert len(results) == 1
        assert results[0].initial_demand_outturn_mw is None
        assert results[0].initial_transmission_system_demand_outturn_mw is None

    def test_missing_publish_time(self):
        data = {"data": [{
            "startTime": "2026-03-11T00:00:00Z",
            "settlementDate": "2026-03-11",
            "settlementPeriod": 1,
            "initialDemandOutturn": 22000,
            "initialTransmissionSystemDemandOutturn": 27000,
        }]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert results[0].publish_time is None

    def test_demand_outturn_is_dataclass(self):
        results = ElexonBMRSPoller.parse_demand_response(SAMPLE_DEMAND_RESPONSE)
        assert isinstance(results[0], DemandOutturn)

    def test_parse_list_response_format(self):
        """Test parsing when the API returns a raw list instead of wrapped object"""
        raw_list = SAMPLE_DEMAND_RESPONSE["data"]
        results = ElexonBMRSPoller.parse_demand_response(raw_list)
        assert len(results) == 2
        assert results[0].settlement_period == 1


@pytest.mark.unit
class TestGenerationMixDataClass:
    """Unit tests for the GenerationMix data class"""

    def test_create_instance(self):
        mix = GenerationMix(
            settlement_period=45,
            start_time=datetime(2026, 4, 7, 21, 0, 0, tzinfo=timezone.utc),
            biomass_mw=2046.0,
            ccgt_mw=3948.0,
            coal_mw=0.0,
            nuclear_mw=5074.0,
            wind_mw=11233.0,
            ocgt_mw=5.0,
            oil_mw=0.0,
            npshyd_mw=529.0,
            ps_mw=862.0,
            intfr_mw=1506.0,
            intned_mw=None,
            intnem_mw=138.0,
            intelec_mw=998.0,
            intifa2_mw=992.0,
            intnsl_mw=712.0,
            intvkl_mw=None,
            other_mw=445.0,
        )
        assert mix.settlement_period == 45
        assert mix.wind_mw == 11233.0
        assert mix.intned_mw is None

    def test_to_json(self):
        mix = GenerationMix(
            settlement_period=45,
            start_time=datetime(2026, 4, 7, 21, 0, 0, tzinfo=timezone.utc),
            biomass_mw=2046.0,
            ccgt_mw=None,
            coal_mw=None,
            nuclear_mw=None,
            wind_mw=None,
            ocgt_mw=None,
            oil_mw=None,
            npshyd_mw=None,
            ps_mw=None,
            intfr_mw=None,
            intned_mw=None,
            intnem_mw=None,
            intelec_mw=None,
            intifa2_mw=None,
            intnsl_mw=None,
            intvkl_mw=None,
            other_mw=None,
        )
        json_str = mix.to_json()
        data = json.loads(json_str)
        assert data["settlement_period"] == 45
        assert data["biomass_mw"] == 2046.0

    def test_from_serializer_dict(self):
        d = {
            "settlement_period": 45,
            "start_time": datetime(2026, 4, 7, 21, 0, 0, tzinfo=timezone.utc),
            "biomass_mw": 2046.0,
            "ccgt_mw": 3948.0,
            "coal_mw": 0.0,
            "nuclear_mw": 5074.0,
            "wind_mw": 11233.0,
            "ocgt_mw": 5.0,
            "oil_mw": 0.0,
            "npshyd_mw": 529.0,
            "ps_mw": 862.0,
            "intfr_mw": 1506.0,
            "intned_mw": None,
            "intnem_mw": 138.0,
            "intelec_mw": 998.0,
            "intifa2_mw": 992.0,
            "intnsl_mw": 712.0,
            "intvkl_mw": None,
            "other_mw": 445.0,
        }
        mix = GenerationMix.from_serializer_dict(d)
        assert mix.settlement_period == 45
        assert mix.wind_mw == 11233.0


@pytest.mark.unit
class TestDemandOutturnDataClass:
    """Unit tests for the DemandOutturn data class"""

    def test_create_instance(self):
        demand = DemandOutturn(
            settlement_period=1,
            settlement_date="2026-03-11",
            start_time=datetime(2026, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
            publish_time=datetime(2026, 3, 11, 0, 30, 0, tzinfo=timezone.utc),
            initial_demand_outturn_mw=22416.0,
            initial_transmission_system_demand_outturn_mw=27678.0,
        )
        assert demand.settlement_period == 1
        assert demand.settlement_date == "2026-03-11"
        assert demand.initial_demand_outturn_mw == 22416.0

    def test_to_json(self):
        demand = DemandOutturn(
            settlement_period=1,
            settlement_date="2026-03-11",
            start_time=datetime(2026, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
            publish_time=None,
            initial_demand_outturn_mw=22416.0,
            initial_transmission_system_demand_outturn_mw=27678.0,
        )
        json_str = demand.to_json()
        data = json.loads(json_str)
        assert data["settlement_period"] == 1
        assert data["initial_demand_outturn_mw"] == 22416.0

    def test_from_serializer_dict(self):
        d = {
            "settlement_period": 1,
            "settlement_date": "2026-03-11",
            "start_time": datetime(2026, 3, 11, 0, 0, 0, tzinfo=timezone.utc),
            "publish_time": datetime(2026, 3, 11, 0, 30, 0, tzinfo=timezone.utc),
            "initial_demand_outturn_mw": 22416.0,
            "initial_transmission_system_demand_outturn_mw": 27678.0,
        }
        demand = DemandOutturn.from_serializer_dict(d)
        assert demand.settlement_period == 1
        assert demand.initial_transmission_system_demand_outturn_mw == 27678.0


@pytest.mark.unit
class TestPollAndSend:
    """Unit tests for the poll_and_send method"""

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_poll_sends_generation_events(self, mock_producer_class, mock_event_producer, temp_state_file):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_ep = Mock()
        mock_ep.producer = Mock()
        mock_event_producer.return_value = mock_ep

        poller = ElexonBMRSPoller(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        with patch.object(poller, "fetch_generation", return_value=SAMPLE_GENERATION_RESPONSE), \
             patch.object(poller, "fetch_demand", return_value=None):
            poller.poll_and_send(once=True)

        assert mock_ep.send_uk_co_elexon_bmrs_generation_mix.call_count == 2

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_poll_sends_demand_events(self, mock_producer_class, mock_event_producer, temp_state_file):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_ep = Mock()
        mock_ep.producer = Mock()
        mock_event_producer.return_value = mock_ep

        poller = ElexonBMRSPoller(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        with patch.object(poller, "fetch_generation", return_value=None), \
             patch.object(poller, "fetch_demand", return_value=SAMPLE_DEMAND_RESPONSE):
            poller.poll_and_send(once=True)

        assert mock_ep.send_uk_co_elexon_bmrs_demand_outturn.call_count == 2

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_dedup_prevents_resend(self, mock_producer_class, mock_event_producer, temp_state_file):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_ep = Mock()
        mock_ep.producer = Mock()
        mock_event_producer.return_value = mock_ep

        poller = ElexonBMRSPoller(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        # First poll
        with patch.object(poller, "fetch_generation", return_value=SAMPLE_GENERATION_RESPONSE), \
             patch.object(poller, "fetch_demand", return_value=None):
            poller.poll_and_send(once=True)
        first_count = mock_ep.send_uk_co_elexon_bmrs_generation_mix.call_count

        # Second poll - same data should be deduped
        with patch.object(poller, "fetch_generation", return_value=SAMPLE_GENERATION_RESPONSE), \
             patch.object(poller, "fetch_demand", return_value=None):
            poller.poll_and_send(once=True)
        second_count = mock_ep.send_uk_co_elexon_bmrs_generation_mix.call_count

        assert first_count == 2
        assert second_count == 2  # no additional calls

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_poll_handles_fetch_error(self, mock_producer_class, mock_event_producer, temp_state_file):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_ep = Mock()
        mock_ep.producer = Mock()
        mock_event_producer.return_value = mock_ep

        poller = ElexonBMRSPoller(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        with patch.object(poller, "fetch_generation", return_value=None), \
             patch.object(poller, "fetch_demand", return_value=None):
            poller.poll_and_send(once=True)

        mock_ep.send_uk_co_elexon_bmrs_generation_mix.assert_not_called()
        mock_ep.send_uk_co_elexon_bmrs_demand_outturn.assert_not_called()

    @patch("elexon_bmrs.elexon_bmrs.UKCoElexonBMRSEventProducer")
    @patch("confluent_kafka.Producer")
    def test_poll_settlement_period_key(self, mock_producer_class, mock_event_producer, temp_state_file):
        """Verify the settlement_period is passed as the key argument"""
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_ep = Mock()
        mock_ep.producer = Mock()
        mock_event_producer.return_value = mock_ep

        poller = ElexonBMRSPoller(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
        )

        with patch.object(poller, "fetch_generation", return_value=SAMPLE_GENERATION_RESPONSE[:1]), \
             patch.object(poller, "fetch_demand", return_value=None):
            poller.poll_and_send(once=True)

        call_args = mock_ep.send_uk_co_elexon_bmrs_generation_mix.call_args
        assert call_args.kwargs["_settlement_period"] == "45"


@pytest.mark.unit
class TestURLConstants:
    """Tests for API URL constants"""

    def test_generation_url(self):
        assert "generation/outturn/summary" in ElexonBMRSPoller.GENERATION_URL

    def test_demand_url(self):
        assert "demand/outturn" in ElexonBMRSPoller.DEMAND_URL

    def test_poll_interval(self):
        assert ElexonBMRSPoller.POLL_INTERVAL_SECONDS == 1800

    def test_generation_url_base(self):
        assert ElexonBMRSPoller.GENERATION_URL.startswith("https://data.elexon.co.uk/bmrs/api/v1/")

    def test_demand_url_base(self):
        assert ElexonBMRSPoller.DEMAND_URL.startswith("https://data.elexon.co.uk/bmrs/api/v1/")


@pytest.mark.unit
class TestEdgeCases:
    """Edge case tests"""

    def test_parse_generation_non_dict_record(self):
        data = [42, "string", None]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert results == []

    def test_parse_generation_non_dict_fuel_entry(self):
        data = [{
            "startTime": "2026-04-07T21:00:00Z",
            "settlementPeriod": 45,
            "data": ["not a dict", 42],
        }]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert len(results) == 1
        assert results[0].wind_mw is None

    def test_parse_demand_non_dict_record(self):
        data = {"data": [42, "string"]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert results == []

    def test_parse_generation_case_insensitive_fuel_type(self):
        """Fuel types are uppercased before mapping"""
        data = [{
            "startTime": "2026-04-07T21:00:00Z",
            "settlementPeriod": 45,
            "data": [{"fuelType": "wind", "generation": 5000}],
        }]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert results[0].wind_mw == 5000.0

    def test_parse_generation_missing_data_key(self):
        data = [{"startTime": "2026-04-07T21:00:00Z", "settlementPeriod": 45}]
        results = ElexonBMRSPoller.parse_generation_response(data)
        assert len(results) == 1
        assert results[0].wind_mw is None

    def test_parse_demand_invalid_start_time(self):
        data = {"data": [{
            "publishTime": "2026-03-11T00:30:00Z",
            "startTime": "invalid-date",
            "settlementDate": "2026-03-11",
            "settlementPeriod": 1,
            "initialDemandOutturn": 22416,
            "initialTransmissionSystemDemandOutturn": 27678,
        }]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert results == []

    def test_parse_demand_invalid_publish_time(self):
        data = {"data": [{
            "publishTime": "not-valid",
            "startTime": "2026-03-11T00:00:00Z",
            "settlementDate": "2026-03-11",
            "settlementPeriod": 1,
            "initialDemandOutturn": 22416,
            "initialTransmissionSystemDemandOutturn": 27678,
        }]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert len(results) == 1
        assert results[0].publish_time is None

    def test_parse_demand_missing_demand_fields(self):
        data = {"data": [{
            "startTime": "2026-03-11T00:00:00Z",
            "settlementDate": "2026-03-11",
            "settlementPeriod": 1,
        }]}
        results = ElexonBMRSPoller.parse_demand_response(data)
        assert len(results) == 1
        assert results[0].initial_demand_outturn_mw is None
        assert results[0].initial_transmission_system_demand_outturn_mw is None
