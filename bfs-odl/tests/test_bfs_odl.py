"""Unit tests for BfS ODL bridge."""

import json
import pytest
from unittest.mock import MagicMock, patch
from bfs_odl.bfs_odl import BfsOdlAPI, _load_state, _save_state, _parse_connection_string


SAMPLE_STATION_FEATURE = {
    "type": "Feature",
    "id": "odlinfo_sitelist.fid1",
    "geometry": {
        "type": "Point",
        "coordinates": [9.38, 54.78]
    },
    "properties": {
        "id": "DEZ0001",
        "kenn": "010010001",
        "plz": "24941",
        "name": "Flensburg",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "kid": 6,
        "height_above_sea": 39,
        "start_measure": "2026-04-07T13:00:00Z",
        "end_measure": "2026-04-07T14:00:00Z",
        "value": 0.082,
        "value_cosmic": None,
        "value_terrestrial": None,
        "unit": "µSv/h",
        "validated": 1,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "10min"
    }
}

SAMPLE_MEASUREMENT_FEATURE = {
    "type": "Feature",
    "id": "odlinfo_odl_1h_latest.fid2",
    "geometry": {
        "type": "Point",
        "coordinates": [10.24, 52.74]
    },
    "properties": {
        "id": "DEZ0305",
        "kenn": "033510091",
        "plz": "29348",
        "name": "Eschede",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "kid": 5,
        "height_above_sea": 63,
        "start_measure": "2026-04-07T12:00:00Z",
        "end_measure": "2026-04-07T13:00:00Z",
        "value": 0.079,
        "value_cosmic": 0.043,
        "value_terrestrial": 0.036,
        "unit": "µSv/h",
        "validated": 1,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h"
    }
}

SAMPLE_MEASUREMENT_NULL_COSMIC = {
    "type": "Feature",
    "id": "odlinfo_odl_1h_latest.fid3",
    "geometry": {
        "type": "Point",
        "coordinates": [8.0, 50.0]
    },
    "properties": {
        "id": "DEZ9999",
        "kenn": "099990001",
        "plz": "60000",
        "name": "TestStation",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "kid": 1,
        "height_above_sea": 100,
        "start_measure": "2026-04-07T12:00:00Z",
        "end_measure": "2026-04-07T13:00:00Z",
        "value": 0.1,
        "value_cosmic": None,
        "value_terrestrial": None,
        "unit": "µSv/h",
        "validated": 0,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h"
    }
}


class TestParseStation:
    def test_basic_fields(self):
        station = BfsOdlAPI.parse_station(SAMPLE_STATION_FEATURE)
        assert station.station_id == "010010001"
        assert station.station_code == "DEZ0001"
        assert station.name == "Flensburg"
        assert station.postal_code == "24941"
        assert station.site_status == 1
        assert station.site_status_text == "in Betrieb"
        assert station.kid == 6

    def test_coordinates(self):
        station = BfsOdlAPI.parse_station(SAMPLE_STATION_FEATURE)
        assert station.longitude == 9.38
        assert station.latitude == 54.78

    def test_height(self):
        station = BfsOdlAPI.parse_station(SAMPLE_STATION_FEATURE)
        assert station.height_above_sea == 39

    def test_null_height(self):
        feature = json.loads(json.dumps(SAMPLE_STATION_FEATURE))
        feature["properties"]["height_above_sea"] = None
        station = BfsOdlAPI.parse_station(feature)
        assert station.height_above_sea is None

    def test_missing_geometry(self):
        feature = json.loads(json.dumps(SAMPLE_STATION_FEATURE))
        feature["geometry"] = None
        station = BfsOdlAPI.parse_station(feature)
        assert station.longitude == 0.0
        assert station.latitude == 0.0


class TestParseMeasurement:
    def test_basic_fields(self):
        m = BfsOdlAPI.parse_measurement(SAMPLE_MEASUREMENT_FEATURE)
        assert m.station_id == "033510091"
        assert m.start_measure == "2026-04-07T12:00:00Z"
        assert m.end_measure == "2026-04-07T13:00:00Z"
        assert m.value == 0.079
        assert m.nuclide == "Gamma-ODL-Brutto"
        assert m.validated == 1

    def test_cosmic_terrestrial(self):
        m = BfsOdlAPI.parse_measurement(SAMPLE_MEASUREMENT_FEATURE)
        assert m.value_cosmic == 0.043
        assert m.value_terrestrial == 0.036

    def test_null_cosmic_terrestrial(self):
        m = BfsOdlAPI.parse_measurement(SAMPLE_MEASUREMENT_NULL_COSMIC)
        assert m.value_cosmic is None
        assert m.value_terrestrial is None
        assert m.validated == 0


class TestFetchStations:
    @patch("bfs_odl.bfs_odl.requests.Session")
    def test_fetch_stations(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": [SAMPLE_STATION_FEATURE],
            "totalFeatures": 1,
        }
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response

        api = BfsOdlAPI()
        stations = api.fetch_stations()
        assert len(stations) == 1
        assert stations[0]["properties"]["kenn"] == "010010001"

    @patch("bfs_odl.bfs_odl.requests.Session")
    def test_fetch_latest_measurements(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": [SAMPLE_MEASUREMENT_FEATURE],
            "totalFeatures": 1,
        }
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response

        api = BfsOdlAPI()
        measurements = api.fetch_latest_measurements()
        assert len(measurements) == 1
        assert measurements[0]["properties"]["kenn"] == "033510091"


class TestState:
    def test_load_missing_file(self, tmp_path):
        result = _load_state(str(tmp_path / "missing.json"))
        assert result == {}

    def test_save_and_load(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"033510091": "2026-04-07T13:00:00Z"}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_empty_path(self):
        _save_state("", {"key": "value"})
        result = _load_state("")
        assert result == {}


class TestConnectionStringParsing:
    def test_plain_kafka(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=bfs-odl"
        kafka_config, topic = _parse_connection_string(conn)
        assert kafka_config["bootstrap.servers"] == "localhost:9092"
        assert topic == "bfs-odl"

    def test_event_hubs(self):
        conn = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123;EntityPath=bfs-odl"
        kafka_config, topic = _parse_connection_string(conn)
        assert "myhub.servicebus.windows.net" in kafka_config["bootstrap.servers"]
        assert topic == "bfs-odl"
        assert kafka_config["security.protocol"] == "SASL_SSL"


from bfs_odl_producer_kafka_producer.producer import DeBfsOdlEventProducer
