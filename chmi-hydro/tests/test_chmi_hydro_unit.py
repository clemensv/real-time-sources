"""Unit tests for the ČHMÚ Hydro bridge."""

import json
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from chmi_hydro.chmi_hydro import CHMIHydroAPI, parse_connection_string, feed_stations, CHMI_BASE_URL
from chmi_hydro.chmi_hydro_producer.cz.gov.chmi.hydro.station import Station
from chmi_hydro.chmi_hydro_producer.cz.gov.chmi.hydro.water_level_observation import WaterLevelObservation
from chmi_hydro.chmi_hydro_producer.producer_client import CZGovCHMIHydroEventProducer


# Meta1.json header: objID,DBC,STATION_NAME,STREAM_NAME,GEOGR1,GEOGR2,
# SPA_TYP,SPAH_DS,SPAH_UNIT,DRYH,SPA1H,SPA2H,SPA3H,SPA4H,
# SPAQ_DS,SPAQ_UNIT,DRYQ,SPA1Q,SPA2Q,SPA3Q,SPA4Q,ISFORECAST
SAMPLE_META_RECORD = [
    "0-203-1-001000", "001000", "Špindlerův Mlýn", "Labe",
    50.7231692, 15.5980379,
    "H", "vodní stav", "CM", 88,
    165, 200, 220, 297,
    "průtok", "M3_S", 0.419,
    19.3, 39.4, 54.5, 137,
    0
]

SAMPLE_META_RECORD_FORECAST = [
    "0-203-1-042000", "042000", "Němčice", "Labe",
    50.0946613, 15.8067603,
    "H", "vodní stav", "CM", 54,
    350, 400, 450, 659,
    "průtok", "M3_S", 10.1,
    200, 249, 307, 725,
    1
]

SAMPLE_META_RECORD_NULL_FLOODS = [
    "0-203-1-003000", "003000", "Prosečné", "Malé Labe",
    50.552152, 15.694443,
    "H", "vodní stav", "CM", 44,
    None, None, None, 214,
    "průtok", "M3_S", 0.288,
    None, None, None, 70.5,
    0
]

SAMPLE_STATION_DATA = {
    "objList": [{
        "objID": "0-203-1-001000",
        "tsList": [
            {
                "tsConID": "H",
                "unit": "CM",
                "tsData": [
                    {"dt": "2026-03-25T00:00:00Z", "value": 96},
                    {"dt": "2026-03-25T00:10:00Z", "value": 96},
                    {"dt": "2026-03-25T00:20:00Z", "value": 95},
                ]
            },
            {
                "tsConID": "Q",
                "unit": "M3_S",
                "tsData": [
                    {"dt": "2026-03-25T00:00:00Z", "value": 1.08244},
                    {"dt": "2026-03-25T00:10:00Z", "value": 1.08244},
                    {"dt": "2026-03-25T00:20:00Z", "value": 1.05},
                ]
            }
        ]
    }]
}

SAMPLE_STATION_DATA_WITH_TEMP = {
    "objList": [{
        "objID": "0-203-1-042000",
        "tsList": [
            {
                "tsConID": "H",
                "unit": "CM",
                "tsData": [
                    {"dt": "2026-03-25T12:00:00Z", "value": 150},
                ]
            },
            {
                "tsConID": "Q",
                "unit": "M3_S",
                "tsData": [
                    {"dt": "2026-03-25T12:00:00Z", "value": 5.23},
                ]
            },
            {
                "tsConID": "TH",
                "unit": "0C",
                "tsData": [
                    {"dt": "2026-03-25T12:00:00Z", "value": 7.5},
                ]
            }
        ]
    }]
}

SAMPLE_STATION_DATA_EMPTY = {
    "objList": [{
        "objID": "0-203-1-999999",
        "tsList": []
    }]
}

SAMPLE_STATION_DATA_NULL_VALUES = {
    "objList": [{
        "objID": "0-203-1-999998",
        "tsList": [
            {
                "tsConID": "H",
                "unit": "CM",
                "tsData": [
                    {"dt": "2026-03-25T00:00:00Z", "value": None},
                ]
            }
        ]
    }]
}

SAMPLE_METADATA_RESPONSE = {
    "zaznamID": "test",
    "datovyZdrojID": "hydrologie",
    "datovyTokID": "Open.Data.Metadata",
    "datumVytvoreni": "2026-03-25T14:00:03Z",
    "verzeDat": "1.0",
    "data": {
        "type": "DataCollection",
        "data": {
            "header": "objID,DBC,STATION_NAME,STREAM_NAME,GEOGR1,GEOGR2,SPA_TYP,SPAH_DS,SPAH_UNIT,DRYH,SPA1H,SPA2H,SPA3H,SPA4H,SPAQ_DS,SPAQ_UNIT,DRYQ,SPA1Q,SPA2Q,SPA3Q,SPA4Q,ISFORECAST",
            "values": [SAMPLE_META_RECORD, SAMPLE_META_RECORD_FORECAST, SAMPLE_META_RECORD_NULL_FLOODS]
        }
    }
}


class TestCHMIHydroInitialization:
    """Tests for the CHMIHydroAPI class initialization."""

    def test_default_initialization(self):
        api = CHMIHydroAPI()
        assert api.base_url == CHMI_BASE_URL
        assert api.polling_interval == 600

    def test_custom_initialization(self):
        api = CHMIHydroAPI(base_url="https://example.com", polling_interval=300)
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
            station_id="0-203-1-001000",
            dbc="001000",
            station_name="Špindlerův Mlýn",
            stream_name="Labe",
            latitude=50.7231692,
            longitude=15.5980379,
            flood_level_1=165.0,
            flood_level_2=200.0,
            flood_level_3=220.0,
            flood_level_4=297.0,
            has_forecast=False,
        )
        assert station.station_id == "0-203-1-001000"
        assert station.station_name == "Špindlerův Mlýn"
        assert station.stream_name == "Labe"
        assert station.latitude == 50.7231692
        assert station.longitude == 15.5980379
        assert station.flood_level_1 == 165.0
        assert station.has_forecast is False

    def test_station_serialization(self):
        station = Station(
            station_id="0-203-1-001000",
            dbc="001000",
            station_name="Špindlerův Mlýn",
            stream_name="Labe",
            latitude=50.7231692,
            longitude=15.5980379,
        )
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == "0-203-1-001000"
        assert data["station_name"] == "Špindlerův Mlýn"

    def test_station_from_data(self):
        data = {"station_id": "123", "dbc": "123", "station_name": "Test",
                "stream_name": "River", "latitude": 50.0, "longitude": 15.0}
        station = Station.from_data(data)
        assert station.station_id == "123"
        assert station.latitude == 50.0

    def test_station_to_byte_array(self):
        station = Station(station_id="123", dbc="123", station_name="Test",
                         stream_name="River", latitude=50.0, longitude=15.0)
        data = station.to_byte_array("application/json")
        assert isinstance(data, bytes)
        parsed = json.loads(data)
        assert parsed["station_id"] == "123"

    def test_station_nullable_flood_levels(self):
        station = Station(
            station_id="123", dbc="123", station_name="Test",
            stream_name="River", latitude=50.0, longitude=15.0,
        )
        assert station.flood_level_1 is None
        assert station.flood_level_2 is None
        assert station.flood_level_3 is None
        assert station.flood_level_4 is None

    def test_water_level_observation_creation(self):
        obs = WaterLevelObservation(
            station_id="0-203-1-001000",
            station_name="Špindlerův Mlýn",
            stream_name="Labe",
            water_level=95.0,
            water_level_timestamp="2026-03-25T00:20:00Z",
            discharge=1.05,
            discharge_timestamp="2026-03-25T00:20:00Z",
            water_temperature=7.5,
            water_temperature_timestamp="2026-03-25T12:00:00Z",
        )
        assert obs.station_id == "0-203-1-001000"
        assert obs.water_level == 95.0
        assert obs.discharge == 1.05
        assert obs.water_temperature == 7.5

    def test_water_level_observation_nullable_fields(self):
        obs = WaterLevelObservation(
            station_id="123",
            station_name="Test",
            stream_name="River",
        )
        assert obs.water_level is None
        assert obs.discharge is None
        assert obs.water_temperature is None

    def test_water_level_observation_serialization(self):
        obs = WaterLevelObservation(
            station_id="123",
            station_name="Test",
            stream_name="River",
            water_level=100.0,
            water_level_timestamp="2026-01-01T00:00:00Z",
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
            "stream_name": "River",
            "water_level": 100.0,
            "water_level_timestamp": "2026-01-01T00:00:00Z",
        }
        obs = WaterLevelObservation.from_data(data)
        assert obs.station_id == "123"
        assert obs.water_level == 100.0


class TestAPIParsing:
    """Tests for API record parsing."""

    def test_parse_station_full(self):
        station = CHMIHydroAPI.parse_station(SAMPLE_META_RECORD)
        assert station.station_id == "0-203-1-001000"
        assert station.dbc == "001000"
        assert station.station_name == "Špindlerův Mlýn"
        assert station.stream_name == "Labe"
        assert station.latitude == 50.7231692
        assert station.longitude == 15.5980379
        assert station.flood_level_1 == 165.0
        assert station.flood_level_2 == 200.0
        assert station.flood_level_3 == 220.0
        assert station.flood_level_4 == 297.0
        assert station.has_forecast is False

    def test_parse_station_with_forecast(self):
        station = CHMIHydroAPI.parse_station(SAMPLE_META_RECORD_FORECAST)
        assert station.station_id == "0-203-1-042000"
        assert station.station_name == "Němčice"
        assert station.has_forecast is True

    def test_parse_station_null_floods(self):
        station = CHMIHydroAPI.parse_station(SAMPLE_META_RECORD_NULL_FLOODS)
        assert station.station_id == "0-203-1-003000"
        assert station.flood_level_1 is None
        assert station.flood_level_2 is None
        assert station.flood_level_3 is None
        assert station.flood_level_4 == 214.0

    def test_parse_observation_full(self):
        obs = CHMIHydroAPI.parse_observation(
            "0-203-1-001000", "Špindlerův Mlýn", "Labe", SAMPLE_STATION_DATA)
        assert obs is not None
        assert obs.station_id == "0-203-1-001000"
        assert obs.water_level == 95.0
        assert obs.water_level_timestamp == "2026-03-25T00:20:00Z"
        assert obs.discharge == 1.05
        assert obs.discharge_timestamp == "2026-03-25T00:20:00Z"

    def test_parse_observation_with_temperature(self):
        obs = CHMIHydroAPI.parse_observation(
            "0-203-1-042000", "Němčice", "Labe", SAMPLE_STATION_DATA_WITH_TEMP)
        assert obs is not None
        assert obs.water_level == 150.0
        assert obs.discharge == 5.23
        assert obs.water_temperature == 7.5

    def test_parse_observation_empty_ts_list(self):
        obs = CHMIHydroAPI.parse_observation(
            "0-203-1-999999", "Test", "River", SAMPLE_STATION_DATA_EMPTY)
        assert obs is None

    def test_parse_observation_null_values(self):
        obs = CHMIHydroAPI.parse_observation(
            "0-203-1-999998", "Test", "River", SAMPLE_STATION_DATA_NULL_VALUES)
        assert obs is None

    def test_parse_observation_empty_obj_list(self):
        obs = CHMIHydroAPI.parse_observation(
            "test", "Test", "River", {"objList": []})
        assert obs is None


class TestAPIRequests:
    """Tests for API requests with mocked HTTP."""

    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_metadata')
    def test_get_metadata(self, mock_get_metadata):
        mock_get_metadata.return_value = [SAMPLE_META_RECORD, SAMPLE_META_RECORD_FORECAST]
        api = CHMIHydroAPI()
        records = api.get_metadata()
        assert len(records) == 2

    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_station_data')
    def test_get_station_data(self, mock_get_station_data):
        mock_get_station_data.return_value = SAMPLE_STATION_DATA
        api = CHMIHydroAPI()
        data = api.get_station_data("0-203-1-001000")
        assert data is not None
        assert data["objList"][0]["objID"] == "0-203-1-001000"

    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_all_station_data')
    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_metadata')
    def test_feed_stations(self, mock_get_metadata, mock_get_all_data):
        mock_get_metadata.return_value = [SAMPLE_META_RECORD, SAMPLE_META_RECORD_FORECAST]
        mock_get_all_data.return_value = {
            "0-203-1-001000": SAMPLE_STATION_DATA,
            "0-203-1-042000": SAMPLE_STATION_DATA_WITH_TEMP,
        }
        api = CHMIHydroAPI()
        mock_producer = MagicMock(spec=CZGovCHMIHydroEventProducer)
        mock_producer.producer = MagicMock()
        count = feed_stations(api, mock_producer)
        # 2 stations + 2 observations
        assert count == 4
        assert mock_producer.send_cz_gov_chmi_hydro_station.call_count == 2
        assert mock_producer.send_cz_gov_chmi_hydro_water_level_observation.call_count == 2

    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_all_station_data')
    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_metadata')
    def test_feed_stations_no_data(self, mock_get_metadata, mock_get_all_data):
        mock_get_metadata.return_value = [SAMPLE_META_RECORD]
        mock_get_all_data.return_value = {}
        api = CHMIHydroAPI()
        mock_producer = MagicMock(spec=CZGovCHMIHydroEventProducer)
        mock_producer.producer = MagicMock()
        count = feed_stations(api, mock_producer)
        # 1 station, 0 observations (no data returned)
        assert count == 1
        assert mock_producer.send_cz_gov_chmi_hydro_station.call_count == 1
        assert mock_producer.send_cz_gov_chmi_hydro_water_level_observation.call_count == 0

    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_all_station_data')
    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_metadata')
    def test_feed_stations_empty(self, mock_get_metadata, mock_get_all_data):
        mock_get_metadata.return_value = []
        mock_get_all_data.return_value = {}
        api = CHMIHydroAPI()
        mock_producer = MagicMock(spec=CZGovCHMIHydroEventProducer)
        mock_producer.producer = MagicMock()
        count = feed_stations(api, mock_producer)
        assert count == 0

    @patch('chmi_hydro.chmi_hydro.CHMIHydroAPI.get_metadata')
    def test_feed_stations_error(self, mock_get_metadata):
        mock_get_metadata.side_effect = Exception("Network error")
        api = CHMIHydroAPI()
        mock_producer = MagicMock(spec=CZGovCHMIHydroEventProducer)
        with pytest.raises(Exception, match="Network error"):
            feed_stations(api, mock_producer)


class TestProducerClient:
    """Tests for the Kafka producer client."""

    def test_send_station(self):
        mock_kafka_producer = MagicMock()
        producer = CZGovCHMIHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(station_id="123", dbc="123", station_name="Test",
                         stream_name="River", latitude=50.0, longitude=15.0)
        producer.send_cz_gov_chmi_hydro_station(station)
        mock_kafka_producer.produce.assert_called_once()
        mock_kafka_producer.flush.assert_called_once()

    def test_send_observation(self):
        mock_kafka_producer = MagicMock()
        producer = CZGovCHMIHydroEventProducer(mock_kafka_producer, "test-topic")
        obs = WaterLevelObservation(
            station_id="123", station_name="Test", stream_name="River",
            water_level=100.0, water_level_timestamp="2026-01-01T00:00:00Z",
        )
        producer.send_cz_gov_chmi_hydro_water_level_observation(obs)
        mock_kafka_producer.produce.assert_called_once()

    def test_send_station_no_flush(self):
        mock_kafka_producer = MagicMock()
        producer = CZGovCHMIHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(station_id="123", dbc="123", station_name="Test",
                         stream_name="River", latitude=50.0, longitude=15.0)
        producer.send_cz_gov_chmi_hydro_station(station, flush_producer=False)
        mock_kafka_producer.produce.assert_called_once()
        mock_kafka_producer.flush.assert_not_called()

    def test_send_station_binary_mode(self):
        mock_kafka_producer = MagicMock()
        producer = CZGovCHMIHydroEventProducer(mock_kafka_producer, "test-topic", content_mode='binary')
        station = Station(station_id="123", dbc="123", station_name="Test",
                         stream_name="River", latitude=50.0, longitude=15.0)
        producer.send_cz_gov_chmi_hydro_station(station)
        mock_kafka_producer.produce.assert_called_once()

    def test_cloudevents_structured_format(self):
        mock_kafka_producer = MagicMock()
        producer = CZGovCHMIHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(station_id="123", dbc="123", station_name="Test",
                         stream_name="River", latitude=50.0, longitude=15.0)
        producer.send_cz_gov_chmi_hydro_station(station)
        call_kwargs = mock_kafka_producer.produce.call_args
        headers = dict(call_kwargs[1]['headers']) if isinstance(call_kwargs[1]['headers'], list) else call_kwargs[1]['headers']
        assert b"application/cloudevents+json" in [v for v in headers.values()] or any(b"application/cloudevents+json" == v for _, v in call_kwargs[1]['headers'])

    def test_station_cloudevent_value(self):
        mock_kafka_producer = MagicMock()
        producer = CZGovCHMIHydroEventProducer(mock_kafka_producer, "test-topic")
        station = Station(station_id="123", dbc="123", station_name="Test",
                         stream_name="River", latitude=50.0, longitude=15.0)
        producer.send_cz_gov_chmi_hydro_station(station)
        call_kwargs = mock_kafka_producer.produce.call_args
        value = json.loads(call_kwargs[1]['value'])
        assert value['type'] == 'CZ.Gov.CHMI.Hydro.Station'
        assert value['source'] == 'https://opendata.chmi.cz'
        assert value['data']['station_id'] == '123'
