"""Unit tests for the SMHI Hydro bridge - no network access required."""

import json
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from smhi_hydro.smhi_hydro import SMHIHydroAPI, parse_connection_string, feed_stations
from smhi_hydro_producer_data import Station
from smhi_hydro_producer_data import DischargeObservation
from smhi_hydro_producer_kafka_producer.producer import SEGovSMHIHydroEventProducer


SAMPLE_STATION_DATA = {
    "key": "1583",
    "name": "VÄSTERSEL",
    "owner": "SMHI",
    "measuringStations": "CORE",
    "region": 36,
    "catchmentName": "MOÄLVEN",
    "catchmentNumber": 36000,
    "catchmentSize": 1465.2,
    "from": 420898500000,
    "to": 1774455300000,
    "latitude": 63.4332,
    "longitude": 18.3034,
    "value": [
        {"date": 1774451700000, "value": 16.0, "quality": "O"},
        {"date": 1774452600000, "value": 16.0, "quality": "O"},
        {"date": 1774453500000, "value": 16.0, "quality": "O"},
        {"date": 1774454400000, "value": 16.0, "quality": "O"},
    ]
}

SAMPLE_STATION_DATA_2 = {
    "key": "2305",
    "name": "HULUBÄCKEN",
    "owner": "SMHI",
    "measuringStations": "CORE",
    "region": 101,
    "catchmentName": "NISSAN",
    "catchmentNumber": 101000,
    "catchmentSize": 3.8,
    "from": 354705300000,
    "to": 1774454400000,
    "latitude": 57.7219,
    "longitude": 13.7301,
    "value": [
        {"date": 1774451700000, "value": 0.069, "quality": "O"},
        {"date": 1774452600000, "value": 0.071, "quality": "O"},
        {"date": 1774453500000, "value": 0.072, "quality": "O"},
    ]
}

SAMPLE_STATION_EMPTY_VALUES = {
    "key": "2429",
    "name": "FINSTA",
    "owner": "SMHI",
    "measuringStations": "CORE",
    "region": 59,
    "catchmentName": "NORRTÄLJEÅN",
    "catchmentNumber": 59000,
    "catchmentSize": 156.3,
    "from": 668790000000,
    "to": 1774455300000,
    "latitude": 59.7354,
    "longitude": 18.4883,
    "value": []
}

SAMPLE_BULK_RESPONSE = {
    "updated": 1774454400000,
    "parameter": {"key": "2", "name": "Vattenföring (15 min)", "unit": "m³/s"},
    "period": {"key": "latest-hour", "from": 1774450801000, "to": 1774454400000,
               "summary": "Data från senaste timmen"},
    "link": [],
    "station": [SAMPLE_STATION_DATA, SAMPLE_STATION_DATA_2, SAMPLE_STATION_EMPTY_VALUES]
}


class TestParseStation:
    """Tests for station parsing."""

    def test_parse_station_basic(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        assert station.station_id == "1583"
        assert station.name == "VÄSTERSEL"
        assert station.owner == "SMHI"
        assert station.measuring_stations == "CORE"
        assert station.region == 36
        assert station.catchment_name == "MOÄLVEN"
        assert station.catchment_number == 36000
        assert station.catchment_size == 1465.2
        assert station.latitude == 63.4332
        assert station.longitude == 18.3034

    def test_parse_station_second(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA_2)
        assert station.station_id == "2305"
        assert station.name == "HULUBÄCKEN"
        assert station.catchment_name == "NISSAN"
        assert station.catchment_size == 3.8

    def test_parse_station_empty_values(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_EMPTY_VALUES)
        assert station.station_id == "2429"
        assert station.name == "FINSTA"

    def test_parse_station_all_fields_types(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        assert isinstance(station.station_id, str)
        assert isinstance(station.name, str)
        assert isinstance(station.owner, str)
        assert isinstance(station.measuring_stations, str)
        assert isinstance(station.region, int)
        assert isinstance(station.catchment_name, str)
        assert isinstance(station.catchment_number, int)
        assert isinstance(station.catchment_size, float)
        assert isinstance(station.latitude, float)
        assert isinstance(station.longitude, float)


class TestParseObservation:
    """Tests for observation parsing."""

    def test_parse_latest_observation(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        assert obs is not None
        assert obs.station_id == "1583"
        assert obs.station_name == "VÄSTERSEL"
        assert obs.catchment_name == "MOÄLVEN"
        assert obs.discharge == 16.0
        assert obs.quality == "O"
        assert "2026" in obs.timestamp

    def test_parse_latest_observation_small_value(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA_2)
        assert obs is not None
        assert obs.discharge == 0.072
        assert obs.station_id == "2305"

    def test_parse_observation_empty_values(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_EMPTY_VALUES)
        assert obs is None

    def test_parse_observation_no_value_key(self):
        data = {**SAMPLE_STATION_DATA, "value": [{"date": 1774451700000, "value": None, "quality": "O"}]}
        obs = SMHIHydroAPI.parse_latest_observation(data)
        assert obs is None

    def test_parse_observation_timestamp_is_iso(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        assert obs is not None
        assert "T" in obs.timestamp
        assert obs.timestamp.endswith("+00:00")

    def test_parse_observation_uses_latest_value(self):
        """The last entry in the value array should be used."""
        data = {
            **SAMPLE_STATION_DATA,
            "value": [
                {"date": 1774451700000, "value": 10.0, "quality": "O"},
                {"date": 1774452600000, "value": 20.0, "quality": "O"},
                {"date": 1774453500000, "value": 30.0, "quality": "O"},
            ]
        }
        obs = SMHIHydroAPI.parse_latest_observation(data)
        assert obs is not None
        assert obs.discharge == 30.0

    def test_parse_observation_field_types(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        assert obs is not None
        assert isinstance(obs.station_id, str)
        assert isinstance(obs.station_name, str)
        assert isinstance(obs.catchment_name, str)
        assert isinstance(obs.timestamp, str)
        assert isinstance(obs.discharge, float)
        assert isinstance(obs.quality, str)


class TestStationDataclass:
    """Tests for the Station dataclass."""

    def test_station_to_json(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == "1583"
        assert data["name"] == "VÄSTERSEL"
        assert data["latitude"] == 63.4332

    def test_station_to_dict(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        d = station.to_dict()
        assert d["station_id"] == "1583"
        assert d["catchment_name"] == "MOÄLVEN"

    def test_station_from_data_json(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        json_str = station.to_json()
        station2 = Station.from_data(json_str, "application/json")
        assert station2.station_id == station.station_id
        assert station2.name == station.name

    def test_station_from_data_bytes(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        byte_data = station.to_byte_array("application/json")
        station2 = Station.from_data(byte_data, "application/json")
        assert station2.station_id == station.station_id

    def test_station_from_data_dict(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        d = station.to_dict()
        station2 = Station.from_data(d, "application/json")
        assert station2.station_id == station.station_id

    def test_station_unsupported_content_type(self):
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        with pytest.raises(NotImplementedError):
            station.to_byte_array("application/xml")

    def test_station_from_data_unsupported(self):
        with pytest.raises(NotImplementedError):
            Station.from_data("<xml/>", "application/xml")


class TestDischargeObservationDataclass:
    """Tests for the DischargeObservation dataclass."""

    def test_observation_to_json(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        json_str = obs.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == "1583"
        assert data["discharge"] == 16.0

    def test_observation_to_dict(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        d = obs.to_dict()
        assert d["station_name"] == "VÄSTERSEL"
        assert d["quality"] == "O"

    def test_observation_from_data_json(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        json_str = obs.to_json()
        obs2 = DischargeObservation.from_data(json_str, "application/json")
        assert obs2.station_id == obs.station_id
        assert obs2.discharge == obs.discharge

    def test_observation_from_data_bytes(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        byte_data = obs.to_byte_array("application/json")
        obs2 = DischargeObservation.from_data(byte_data, "application/json")
        assert obs2.station_id == obs.station_id

    def test_observation_unsupported_content_type(self):
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        with pytest.raises(NotImplementedError):
            obs.to_byte_array("application/xml")


class TestParseConnectionString:
    """Tests for connection string parsing."""

    def test_parse_event_hubs_connection_string(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123="
        config = parse_connection_string(cs)
        assert config['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert config['sasl.username'] == '$ConnectionString'
        assert config['sasl.password'] == cs
        assert config['security.protocol'] == 'SASL_SSL'
        assert config['sasl.mechanism'] == 'PLAIN'

    def test_parse_kafka_connection_string(self):
        cs = "BootstrapServer=localhost:9092"
        config = parse_connection_string(cs)
        assert config['bootstrap.servers'] == 'localhost:9092'
        assert 'sasl.username' not in config

    def test_parse_empty_connection_string(self):
        config = parse_connection_string("")
        assert config == {}


class TestFeedStations:
    """Tests for the feed_stations function."""

    def test_feed_stations_with_mock(self):
        api = SMHIHydroAPI()
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic')

        with patch.object(api, 'get_bulk_discharge_data', return_value=SAMPLE_BULK_RESPONSE):
            count = feed_stations(api, event_producer)

        # 3 stations + 2 observations (FINSTA has empty values)
        assert count == 5

    def test_feed_stations_sends_stations(self):
        api = SMHIHydroAPI()
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic')

        with patch.object(api, 'get_bulk_discharge_data', return_value=SAMPLE_BULK_RESPONSE):
            feed_stations(api, event_producer)

        assert mock_producer.produce.call_count == 5

    def test_feed_stations_empty_response(self):
        api = SMHIHydroAPI()
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic')

        with patch.object(api, 'get_bulk_discharge_data', return_value={"station": []}):
            count = feed_stations(api, event_producer)

        assert count == 0

    def test_feed_stations_flushes(self):
        api = SMHIHydroAPI()
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic')

        with patch.object(api, 'get_bulk_discharge_data', return_value=SAMPLE_BULK_RESPONSE):
            feed_stations(api, event_producer)

        mock_producer.flush.assert_called()


class TestSMHIHydroAPI:
    """Tests for the SMHIHydroAPI class."""

    def test_default_urls(self):
        api = SMHIHydroAPI()
        assert "opendata-download-hydroobs.smhi.se" in api.bulk_discharge_url
        assert "parameter/2" in api.bulk_discharge_url
        assert "latest-hour" in api.bulk_discharge_url

    def test_custom_base_url(self):
        api = SMHIHydroAPI(base_url="https://test.example.com/api")
        assert api.bulk_discharge_url.startswith("https://test.example.com/api")

    def test_polling_interval(self):
        api = SMHIHydroAPI(polling_interval=300)
        assert api.polling_interval == 300

    def test_get_bulk_discharge_data_mock(self):
        api = SMHIHydroAPI()
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_BULK_RESPONSE
        mock_response.raise_for_status = MagicMock()
        with patch.object(api.session, 'get', return_value=mock_response):
            data = api.get_bulk_discharge_data()
        assert data == SAMPLE_BULK_RESPONSE
        assert len(data["station"]) == 3


class TestProducerClient:
    """Tests for the SEGovSMHIHydroEventProducer."""

    def test_send_station_structured(self):
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic', 'structured')
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        event_producer.send_se_gov_smhi_hydro_station(station.station_id, station)
        mock_producer.produce.assert_called_once()
        call_args = mock_producer.produce.call_args
        # produce is called with positional topic arg or keyword args
        topic_arg = call_args.args[0] if call_args.args else call_args.kwargs.get('topic')
        assert topic_arg == 'test-topic'
        value_arg = call_args.kwargs.get('value')
        value = json.loads(value_arg)
        assert value['type'] == 'SE.Gov.SMHI.Hydro.Station'
        assert value['source'] == 'https://opendata-download-hydroobs.smhi.se'

    def test_send_observation_structured(self):
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic', 'structured')
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        event_producer.send_se_gov_smhi_hydro_discharge_observation(obs.station_id, obs)
        mock_producer.produce.assert_called_once()
        call_args = mock_producer.produce.call_args
        value_arg = call_args.kwargs.get('value')
        value = json.loads(value_arg)
        assert value['type'] == 'SE.Gov.SMHI.Hydro.DischargeObservation'
        assert value['data']['discharge'] == 16.0

    def test_send_station_no_flush(self):
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic')
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        event_producer.send_se_gov_smhi_hydro_station(station.station_id, station, flush_producer=False)
        mock_producer.flush.assert_not_called()

    def test_send_station_with_key_mapper(self):
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic')
        station = SMHIHydroAPI.parse_station(SAMPLE_STATION_DATA)
        event_producer.send_se_gov_smhi_hydro_station(
            station.station_id,
            station,
            key_mapper=lambda ce, s: f"custom:{s.station_id}"
        )
        call_args = mock_producer.produce.call_args
        assert call_args.kwargs['key'] == "custom:1583"

    def test_send_observation_binary_mode(self):
        mock_producer = MagicMock()
        mock_producer.flush = MagicMock()
        event_producer = SEGovSMHIHydroEventProducer(mock_producer, 'test-topic', 'binary')
        obs = SMHIHydroAPI.parse_latest_observation(SAMPLE_STATION_DATA)
        event_producer.send_se_gov_smhi_hydro_discharge_observation(obs.station_id, obs)
        mock_producer.produce.assert_called_once()


class TestUnicodeHandling:
    """Tests for handling Swedish unicode characters."""

    def test_station_name_with_swedish_chars(self):
        data = {**SAMPLE_STATION_DATA, "name": "ÅKESTA KVARN", "catchmentName": "GÖTA ÄLV"}
        station = SMHIHydroAPI.parse_station(data)
        assert station.name == "ÅKESTA KVARN"
        assert station.catchment_name == "GÖTA ÄLV"

    def test_station_json_roundtrip_unicode(self):
        data = {**SAMPLE_STATION_DATA, "name": "ÖVRE ABISKOJOKK", "catchmentName": "TORNEÄLVEN"}
        station = SMHIHydroAPI.parse_station(data)
        json_str = station.to_json()
        station2 = Station.from_data(json_str, "application/json")
        assert station2.name == "ÖVRE ABISKOJOKK"
        assert station2.catchment_name == "TORNEÄLVEN"

    def test_observation_with_unicode_names(self):
        data = {**SAMPLE_STATION_DATA, "name": "TÄRENDÖ", "catchmentName": "KALIXÄLVEN"}
        obs = SMHIHydroAPI.parse_latest_observation(data)
        assert obs is not None
        assert obs.station_name == "TÄRENDÖ"
        assert obs.catchment_name == "KALIXÄLVEN"
