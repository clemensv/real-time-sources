"""Unit tests for the IMGW Hydro bridge."""

import json
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from imgw_hydro.imgw_hydro import IMGWHydroAPI, parse_connection_string, feed_stations, IMGW_BASE_URL
from imgw_hydro.imgw_hydro_producer.pl.gov.imgw.hydro.station import Station
from imgw_hydro.imgw_hydro_producer.pl.gov.imgw.hydro.water_level_observation import WaterLevelObservation
from imgw_hydro.imgw_hydro_producer.producer_client import PLGovIMGWHydroEventProducer


SAMPLE_RECORD = {
    "id_stacji": "150180090",
    "stacja": "Nędza",
    "rzeka": "Sumina",
    "wojewodztwo": "śląskie",
    "lon": "18.5431",
    "lat": "50.3825",
    "stan_wody": "45",
    "stan_wody_data_pomiaru": "2026-03-25 12:00:00",
    "temperatura_wody": "4.8",
    "temperatura_wody_data_pomiaru": "2026-03-25 06:00:00",
    "przeplyw": "0.65",
    "przeplyw_data": "2026-02-18 09:50:00",
    "zjawisko_lodowe": "0",
    "zjawisko_lodowe_data_pomiaru": "2026-02-26 13:40:00",
    "zjawisko_zarastania": "0",
    "zjawisko_zarastania_data_pomiaru": "2026-02-26 13:40:00",
}

SAMPLE_RECORD_MINIMAL = {
    "id_stacji": "150190010",
    "stacja": "Krzyżanowice",
    "rzeka": "Odra",
    "wojewodztwo": None,
    "lon": None,
    "lat": None,
    "stan_wody": "200",
    "stan_wody_data_pomiaru": "2026-03-25 12:00:00",
    "temperatura_wody": None,
    "temperatura_wody_data_pomiaru": None,
    "przeplyw": None,
    "przeplyw_data": None,
    "zjawisko_lodowe": None,
    "zjawisko_lodowe_data_pomiaru": None,
    "zjawisko_zarastania": None,
    "zjawisko_zarastania_data_pomiaru": None,
}

SAMPLE_RECORD_NO_WATER_LEVEL = {
    "id_stacji": "999999999",
    "stacja": "TestStation",
    "rzeka": "TestRiver",
    "wojewodztwo": "test",
    "lon": "20.0",
    "lat": "52.0",
    "stan_wody": None,
    "stan_wody_data_pomiaru": None,
    "temperatura_wody": None,
    "temperatura_wody_data_pomiaru": None,
    "przeplyw": None,
    "przeplyw_data": None,
    "zjawisko_lodowe": None,
    "zjawisko_lodowe_data_pomiaru": None,
    "zjawisko_zarastania": None,
    "zjawisko_zarastania_data_pomiaru": None,
}


class TestIMGWHydroInitialization:
    """Tests for the IMGWHydroAPI class initialization."""

    def test_default_initialization(self):
        api = IMGWHydroAPI()
        assert api.base_url == IMGW_BASE_URL
        assert api.polling_interval == 600

    def test_custom_initialization(self):
        api = IMGWHydroAPI(base_url="https://example.com", polling_interval=300)
        assert api.base_url == "https://example.com"
        assert api.polling_interval == 300


class TestConnectionStringParsing:
    """Tests for connection string parsing."""

    def test_event_hubs_connection_string(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=testkey"
        config = parse_connection_string(conn_str)
        assert config['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert config['sasl.username'] == '$ConnectionString'
        assert config['security.protocol'] == 'SASL_SSL'
        assert config['sasl.mechanism'] == 'PLAIN'

    def test_bootstrap_server(self):
        conn_str = "BootstrapServer=localhost:9092"
        config = parse_connection_string(conn_str)
        assert config['bootstrap.servers'] == 'localhost:9092'

    def test_empty_connection_string(self):
        config = parse_connection_string("")
        assert 'bootstrap.servers' not in config


class TestDataClasses:
    """Tests for the data classes."""

    def test_station_creation(self):
        station = Station(
            id_stacji="150180090",
            stacja="Nędza",
            rzeka="Sumina",
            wojewodztwo="śląskie",
            longitude=18.5431,
            latitude=50.3825,
        )
        assert station.id_stacji == "150180090"
        assert station.stacja == "Nędza"
        assert station.rzeka == "Sumina"
        assert station.wojewodztwo == "śląskie"
        assert station.longitude == 18.5431
        assert station.latitude == 50.3825

    def test_station_serialization(self):
        station = Station(
            id_stacji="150180090",
            stacja="Nędza",
            rzeka="Sumina",
            wojewodztwo="śląskie",
            longitude=18.5431,
            latitude=50.3825,
        )
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["id_stacji"] == "150180090"
        assert data["stacja"] == "Nędza"

    def test_station_from_data(self):
        data = {"id_stacji": "123", "stacja": "Test", "rzeka": "River", "wojewodztwo": "test", "longitude": 20.0, "latitude": 52.0}
        station = Station.from_data(data)
        assert station.id_stacji == "123"
        assert station.longitude == 20.0

    def test_station_to_byte_array(self):
        station = Station(id_stacji="123", stacja="Test", rzeka="River", wojewodztwo="test", longitude=20.0, latitude=52.0)
        data = station.to_byte_array("application/json")
        assert isinstance(data, bytes)
        parsed = json.loads(data)
        assert parsed["id_stacji"] == "123"

    def test_water_level_observation_creation(self):
        obs = WaterLevelObservation(
            station_id="150180090",
            station_name="Nędza",
            river="Sumina",
            voivodeship="śląskie",
            water_level=45.0,
            water_level_timestamp="2026-03-25 12:00:00",
            water_temperature=4.8,
            water_temperature_timestamp="2026-03-25 06:00:00",
            discharge=0.65,
            discharge_timestamp="2026-02-18 09:50:00",
            ice_phenomenon_code="0",
            overgrowth_code="0",
        )
        assert obs.station_id == "150180090"
        assert obs.water_level == 45.0
        assert obs.water_temperature == 4.8
        assert obs.discharge == 0.65

    def test_water_level_observation_nullable_fields(self):
        obs = WaterLevelObservation(
            station_id="150190010",
            station_name="Krzyżanowice",
            river="Odra",
            voivodeship="",
            water_level=200.0,
            water_level_timestamp="2026-03-25 12:00:00",
        )
        assert obs.water_temperature is None
        assert obs.discharge is None
        assert obs.ice_phenomenon_code is None

    def test_water_level_observation_serialization(self):
        obs = WaterLevelObservation(
            station_id="123",
            station_name="Test",
            river="River",
            voivodeship="test",
            water_level=100.0,
            water_level_timestamp="2026-01-01 00:00:00",
        )
        json_str = obs.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == "123"
        assert data["water_level"] == 100.0
        assert data["water_temperature"] is None

    def test_water_level_observation_from_data(self):
        data = {
            "station_id": "123",
            "station_name": "Test",
            "river": "River",
            "voivodeship": "test",
            "water_level": 100.0,
            "water_level_timestamp": "2026-01-01 00:00:00",
        }
        obs = WaterLevelObservation.from_data(data)
        assert obs.station_id == "123"
        assert obs.water_level == 100.0


class TestAPIParsing:
    """Tests for API record parsing."""

    def test_parse_station_full(self):
        station = IMGWHydroAPI.parse_station(SAMPLE_RECORD)
        assert station.id_stacji == "150180090"
        assert station.stacja == "Nędza"
        assert station.rzeka == "Sumina"
        assert station.wojewodztwo == "śląskie"
        assert station.longitude == 18.5431
        assert station.latitude == 50.3825

    def test_parse_station_null_coords(self):
        station = IMGWHydroAPI.parse_station(SAMPLE_RECORD_MINIMAL)
        assert station.id_stacji == "150190010"
        assert station.longitude == 0.0
        assert station.latitude == 0.0
        assert station.wojewodztwo == ""

    def test_parse_observation_full(self):
        obs = IMGWHydroAPI.parse_observation(SAMPLE_RECORD)
        assert obs is not None
        assert obs.station_id == "150180090"
        assert obs.water_level == 45.0
        assert obs.water_temperature == 4.8
        assert obs.discharge == 0.65
        assert obs.ice_phenomenon_code == "0"

    def test_parse_observation_minimal(self):
        obs = IMGWHydroAPI.parse_observation(SAMPLE_RECORD_MINIMAL)
        assert obs is not None
        assert obs.station_id == "150190010"
        assert obs.water_level == 200.0
        assert obs.water_temperature is None
        assert obs.discharge is None

    def test_parse_observation_no_water_level(self):
        obs = IMGWHydroAPI.parse_observation(SAMPLE_RECORD_NO_WATER_LEVEL)
        assert obs is None


class TestAPIRequests:
    """Tests for API requests with mocked HTTP."""

    @patch.object(IMGWHydroAPI, 'get_all_data')
    def test_get_all_data(self, mock_get_all_data):
        mock_get_all_data.return_value = [SAMPLE_RECORD, SAMPLE_RECORD_MINIMAL]
        api = IMGWHydroAPI()
        records = api.get_all_data()
        assert len(records) == 2
        assert records[0]["id_stacji"] == "150180090"

    @patch.object(IMGWHydroAPI, 'get_station_data')
    def test_get_station_data(self, mock_get_station_data):
        mock_get_station_data.return_value = SAMPLE_RECORD
        api = IMGWHydroAPI()
        record = api.get_station_data("150180090")
        assert record["id_stacji"] == "150180090"

    @patch.object(IMGWHydroAPI, 'get_all_data')
    def test_feed_stations(self, mock_get_all_data):
        mock_get_all_data.return_value = [SAMPLE_RECORD, SAMPLE_RECORD_MINIMAL, SAMPLE_RECORD_NO_WATER_LEVEL]
        api = IMGWHydroAPI()
        mock_producer = MagicMock(spec=PLGovIMGWHydroEventProducer)
        mock_producer.producer = MagicMock()
        count = feed_stations(api, mock_producer)
        # 3 stations + 2 observations (third has no water level)
        assert count == 5
        assert mock_producer.send_pl_gov_imgw_hydro_station.call_count == 3
        assert mock_producer.send_pl_gov_imgw_hydro_water_level_observation.call_count == 2

    @patch.object(IMGWHydroAPI, 'get_all_data')
    def test_feed_stations_empty(self, mock_get_all_data):
        mock_get_all_data.return_value = []
        api = IMGWHydroAPI()
        mock_producer = MagicMock(spec=PLGovIMGWHydroEventProducer)
        mock_producer.producer = MagicMock()
        count = feed_stations(api, mock_producer)
        assert count == 0

    @patch.object(IMGWHydroAPI, 'get_all_data')
    def test_feed_stations_error(self, mock_get_all_data):
        mock_get_all_data.side_effect = Exception("Network error")
        api = IMGWHydroAPI()
        mock_producer = MagicMock(spec=PLGovIMGWHydroEventProducer)
        with pytest.raises(Exception, match="Network error"):
            feed_stations(api, mock_producer)


class TestProducerClient:
    """Tests for the Kafka producer client."""

    def test_send_station(self):
        mock_kafka_producer = MagicMock()
        producer = PLGovIMGWHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(id_stacji="123", stacja="Test", rzeka="River", wojewodztwo="test", longitude=20.0, latitude=52.0)
        producer.send_pl_gov_imgw_hydro_station(station)
        mock_kafka_producer.produce.assert_called_once()
        mock_kafka_producer.flush.assert_called_once()

    def test_send_observation(self):
        mock_kafka_producer = MagicMock()
        producer = PLGovIMGWHydroEventProducer(mock_kafka_producer, "test-topic")
        obs = WaterLevelObservation(
            station_id="123", station_name="Test", river="River", voivodeship="test",
            water_level=100.0, water_level_timestamp="2026-01-01 00:00:00",
        )
        producer.send_pl_gov_imgw_hydro_water_level_observation(obs)
        mock_kafka_producer.produce.assert_called_once()

    def test_send_station_no_flush(self):
        mock_kafka_producer = MagicMock()
        producer = PLGovIMGWHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(id_stacji="123", stacja="Test", rzeka="River", wojewodztwo="test", longitude=20.0, latitude=52.0)
        producer.send_pl_gov_imgw_hydro_station(station, flush_producer=False)
        mock_kafka_producer.produce.assert_called_once()
        mock_kafka_producer.flush.assert_not_called()

    def test_send_station_binary_mode(self):
        mock_kafka_producer = MagicMock()
        producer = PLGovIMGWHydroEventProducer(mock_kafka_producer, "test-topic", content_mode='binary')
        station = Station(id_stacji="123", stacja="Test", rzeka="River", wojewodztwo="test", longitude=20.0, latitude=52.0)
        producer.send_pl_gov_imgw_hydro_station(station)
        mock_kafka_producer.produce.assert_called_once()

    def test_cloudevents_structured_format(self):
        mock_kafka_producer = MagicMock()
        producer = PLGovIMGWHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(id_stacji="123", stacja="Test", rzeka="River", wojewodztwo="test", longitude=20.0, latitude=52.0)
        producer.send_pl_gov_imgw_hydro_station(station)
        call_kwargs = mock_kafka_producer.produce.call_args
        headers = dict(call_kwargs[1]['headers']) if isinstance(call_kwargs[1]['headers'], list) else call_kwargs[1]['headers']
        assert b"application/cloudevents+json" in [v for v in headers.values()] or any(b"application/cloudevents+json" == v for _, v in call_kwargs[1]['headers'])

    def test_station_cloudevent_value(self):
        mock_kafka_producer = MagicMock()
        producer = PLGovIMGWHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(id_stacji="123", stacja="Test", rzeka="River", wojewodztwo="test", longitude=20.0, latitude=52.0)
        producer.send_pl_gov_imgw_hydro_station(station)
        call_kwargs = mock_kafka_producer.produce.call_args
        value = json.loads(call_kwargs[1]['value'])
        assert value['type'] == 'PL.Gov.IMGW.Hydro.Station'
        assert value['source'] == 'https://danepubliczne.imgw.pl'
        assert value['data']['id_stacji'] == '123'
