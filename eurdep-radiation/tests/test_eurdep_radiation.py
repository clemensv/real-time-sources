"""Unit and integration tests for the EURDEP radiation bridge."""

import json
import pytest
from unittest.mock import MagicMock, patch, call
from eurdep_radiation.eurdep_radiation import (
    EurdepAPI,
    _load_state,
    _save_state,
    _parse_connection_string,
)


# ---------------------------------------------------------------------------
# Sample feature fixtures
# ---------------------------------------------------------------------------

SAMPLE_FEATURE_AT0001_6H = {
    "type": "Feature",
    "id": "eurdep_latestValue.fid1",
    "geometry": {"type": "Point", "coordinates": [16.39, 48.73]},
    "properties": {
        "id": "AT0001",
        "name": "Laa/ThayaAMS",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "height_above_sea": 183,
        "analyzed_range_in_h": 6,
        "start_measure": "2026-04-08T19:00:00Z",
        "end_measure": "2026-04-08T20:00:00Z",
        "value": 0.08,
        "unit": "µSv/h",
        "validated": 2,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}

SAMPLE_FEATURE_AT0001_12H = {
    "type": "Feature",
    "id": "eurdep_latestValue.fid2",
    "geometry": {"type": "Point", "coordinates": [16.39, 48.73]},
    "properties": {
        "id": "AT0001",
        "name": "Laa/ThayaAMS",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "height_above_sea": 183,
        "analyzed_range_in_h": 12,
        "start_measure": "2026-04-08T19:00:00Z",
        "end_measure": "2026-04-08T20:00:00Z",
        "value": 0.08,
        "unit": "µSv/h",
        "validated": 2,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}

SAMPLE_FEATURE_AT0001_24H = {
    "type": "Feature",
    "id": "eurdep_latestValue.fid3",
    "geometry": {"type": "Point", "coordinates": [16.39, 48.73]},
    "properties": {
        "id": "AT0001",
        "name": "Laa/ThayaAMS",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "height_above_sea": 183,
        "analyzed_range_in_h": 24,
        "start_measure": "2026-04-08T19:00:00Z",
        "end_measure": "2026-04-08T20:00:00Z",
        "value": 0.08,
        "unit": "µSv/h",
        "validated": 2,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}

SAMPLE_FEATURE_DE0123 = {
    "type": "Feature",
    "id": "eurdep_latestValue.fid4",
    "geometry": {"type": "Point", "coordinates": [10.24, 52.74]},
    "properties": {
        "id": "DE0123",
        "name": "Eschede",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "height_above_sea": 63,
        "analyzed_range_in_h": 6,
        "start_measure": "2026-04-08T12:00:00Z",
        "end_measure": "2026-04-08T13:00:00Z",
        "value": 0.079,
        "unit": "µSv/h",
        "validated": 1,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}

SAMPLE_FEATURE_NULL_HEIGHT = {
    "type": "Feature",
    "id": "eurdep_latestValue.fid5",
    "geometry": {"type": "Point", "coordinates": [2.35, 48.86]},
    "properties": {
        "id": "FR0042",
        "name": "Paris-Centre",
        "site_status": 1,
        "site_status_text": "en service",
        "height_above_sea": None,
        "analyzed_range_in_h": 6,
        "start_measure": "2026-04-08T12:00:00Z",
        "end_measure": "2026-04-08T13:00:00Z",
        "value": 0.065,
        "unit": "µSv/h",
        "validated": 0,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}

SAMPLE_FEATURE_NULL_VALUE = {
    "type": "Feature",
    "id": "eurdep_latestValue.fid6",
    "geometry": {"type": "Point", "coordinates": [14.42, 50.08]},
    "properties": {
        "id": "CZ0001",
        "name": "Praha-Centrum",
        "site_status": 1,
        "site_status_text": "v provozu",
        "height_above_sea": 200,
        "analyzed_range_in_h": 6,
        "start_measure": "2026-04-08T12:00:00Z",
        "end_measure": "2026-04-08T13:00:00Z",
        "value": None,
        "unit": "µSv/h",
        "validated": 0,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}

SAMPLE_FEATURE_NO_GEOMETRY = {
    "type": "Feature",
    "id": "eurdep_latestValue.fid7",
    "geometry": None,
    "properties": {
        "id": "PL0001",
        "name": "Warszawa",
        "site_status": 1,
        "site_status_text": "aktywna",
        "height_above_sea": 100,
        "analyzed_range_in_h": 6,
        "start_measure": "2026-04-08T12:00:00Z",
        "end_measure": "2026-04-08T13:00:00Z",
        "value": 0.11,
        "unit": "µSv/h",
        "validated": 1,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}


# ---------------------------------------------------------------------------
# Station parsing tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestExtractStations:
    def test_basic_station_fields(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_AT0001_6H])
        assert "AT0001" in stations
        s = stations["AT0001"]
        assert s.station_id == "AT0001"
        assert s.name == "Laa/ThayaAMS"
        assert s.site_status == 1
        assert s.site_status_text == "in Betrieb"

    def test_country_code_extraction(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_AT0001_6H])
        assert stations["AT0001"].country_code == "AT"

    def test_country_code_germany(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_DE0123])
        assert stations["DE0123"].country_code == "DE"

    def test_country_code_france(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_NULL_HEIGHT])
        assert stations["FR0042"].country_code == "FR"

    def test_coordinates(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_AT0001_6H])
        s = stations["AT0001"]
        assert s.longitude == 16.39
        assert s.latitude == 48.73

    def test_height_above_sea(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_AT0001_6H])
        assert stations["AT0001"].height_above_sea == 183

    def test_null_height(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_NULL_HEIGHT])
        assert stations["FR0042"].height_above_sea is None

    def test_missing_geometry(self):
        stations = EurdepAPI.extract_stations([SAMPLE_FEATURE_NO_GEOMETRY])
        s = stations["PL0001"]
        assert s.longitude == 0.0
        assert s.latitude == 0.0

    def test_deduplication_across_ranges(self):
        """Same station at different analyzed_range_in_h should produce one station."""
        features = [
            SAMPLE_FEATURE_AT0001_6H,
            SAMPLE_FEATURE_AT0001_12H,
            SAMPLE_FEATURE_AT0001_24H,
        ]
        stations = EurdepAPI.extract_stations(features)
        assert len(stations) == 1
        assert "AT0001" in stations

    def test_multiple_stations(self):
        features = [SAMPLE_FEATURE_AT0001_6H, SAMPLE_FEATURE_DE0123]
        stations = EurdepAPI.extract_stations(features)
        assert len(stations) == 2
        assert "AT0001" in stations
        assert "DE0123" in stations

    def test_empty_features_list(self):
        stations = EurdepAPI.extract_stations([])
        assert stations == {}

    def test_feature_missing_id(self):
        feature = json.loads(json.dumps(SAMPLE_FEATURE_AT0001_6H))
        feature["properties"]["id"] = ""
        stations = EurdepAPI.extract_stations([feature])
        assert len(stations) == 0


# ---------------------------------------------------------------------------
# Reading parsing tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestExtractReadings:
    def test_basic_reading_fields(self):
        readings = EurdepAPI.extract_readings([SAMPLE_FEATURE_DE0123])
        assert len(readings) == 1
        r = readings[0]
        assert r.station_id == "DE0123"
        assert r.name == "Eschede"
        assert r.value == 0.079
        assert r.unit == "µSv/h"
        assert r.start_measure == "2026-04-08T12:00:00Z"
        assert r.end_measure == "2026-04-08T13:00:00Z"
        assert r.nuclide == "Gamma-ODL-Brutto"
        assert r.duration == "1h"
        assert r.validated == 1

    def test_prefers_shortest_analyzed_range(self):
        """Should pick the 6h range over 12h and 24h."""
        features = [
            SAMPLE_FEATURE_AT0001_24H,
            SAMPLE_FEATURE_AT0001_12H,
            SAMPLE_FEATURE_AT0001_6H,
        ]
        readings = EurdepAPI.extract_readings(features)
        assert len(readings) == 1
        assert readings[0].station_id == "AT0001"

    def test_dedup_same_station_same_end_measure(self):
        """Three features for the same station+end_measure => one reading."""
        features = [
            SAMPLE_FEATURE_AT0001_6H,
            SAMPLE_FEATURE_AT0001_12H,
            SAMPLE_FEATURE_AT0001_24H,
        ]
        readings = EurdepAPI.extract_readings(features)
        assert len(readings) == 1

    def test_different_stations_produce_separate_readings(self):
        features = [SAMPLE_FEATURE_AT0001_6H, SAMPLE_FEATURE_DE0123]
        readings = EurdepAPI.extract_readings(features)
        assert len(readings) == 2
        ids = {r.station_id for r in readings}
        assert ids == {"AT0001", "DE0123"}

    def test_null_value_reading(self):
        readings = EurdepAPI.extract_readings([SAMPLE_FEATURE_NULL_VALUE])
        assert len(readings) == 1
        assert readings[0].value is None
        assert readings[0].validated == 0

    def test_empty_features_list(self):
        readings = EurdepAPI.extract_readings([])
        assert len(readings) == 0

    def test_feature_missing_end_measure(self):
        feature = json.loads(json.dumps(SAMPLE_FEATURE_AT0001_6H))
        feature["properties"]["end_measure"] = ""
        readings = EurdepAPI.extract_readings([feature])
        assert len(readings) == 0

    def test_feature_missing_station_id(self):
        feature = json.loads(json.dumps(SAMPLE_FEATURE_AT0001_6H))
        feature["properties"]["id"] = ""
        readings = EurdepAPI.extract_readings([feature])
        assert len(readings) == 0


# ---------------------------------------------------------------------------
# WFS fetch tests
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestFetchFeatures:
    @patch("eurdep_radiation.eurdep_radiation.requests.Session")
    def test_single_page_fetch(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": [SAMPLE_FEATURE_AT0001_6H, SAMPLE_FEATURE_DE0123],
        }
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response

        api = EurdepAPI()
        features = api.fetch_all_features()
        assert len(features) == 2
        assert features[0]["properties"]["id"] == "AT0001"
        mock_session.get.assert_called_once()

    @patch("eurdep_radiation.eurdep_radiation.requests.Session")
    def test_pagination(self, mock_session_cls):
        """When the first page returns exactly PAGE_SIZE features, a second page is fetched."""
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        from eurdep_radiation.eurdep_radiation import PAGE_SIZE
        # First page: exactly PAGE_SIZE features
        page1_features = [SAMPLE_FEATURE_AT0001_6H] * PAGE_SIZE
        page1_response = MagicMock()
        page1_response.json.return_value = {"type": "FeatureCollection", "features": page1_features}
        page1_response.raise_for_status = MagicMock()

        # Second page: less than PAGE_SIZE
        page2_features = [SAMPLE_FEATURE_DE0123]
        page2_response = MagicMock()
        page2_response.json.return_value = {"type": "FeatureCollection", "features": page2_features}
        page2_response.raise_for_status = MagicMock()

        mock_session.get.side_effect = [page1_response, page2_response]

        api = EurdepAPI()
        features = api.fetch_all_features()
        assert len(features) == PAGE_SIZE + 1
        assert mock_session.get.call_count == 2

    @patch("eurdep_radiation.eurdep_radiation.requests.Session")
    def test_empty_response(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_response = MagicMock()
        mock_response.json.return_value = {"type": "FeatureCollection", "features": []}
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response

        api = EurdepAPI()
        features = api.fetch_all_features()
        assert features == []


# ---------------------------------------------------------------------------
# State persistence tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestState:
    def test_load_missing_file(self, tmp_path):
        result = _load_state(str(tmp_path / "missing.json"))
        assert result == {}

    def test_save_and_load(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"AT0001|2026-04-08T20:00:00Z": "2026-04-08T20:00:00Z"}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_empty_path(self):
        _save_state("", {"key": "value"})
        result = _load_state("")
        assert result == {}

    def test_load_corrupt_file(self, tmp_path):
        path = str(tmp_path / "corrupt.json")
        with open(path, "w") as f:
            f.write("not valid json{{{")
        result = _load_state(path)
        assert result == {}

    def test_save_overwrites(self, tmp_path):
        path = str(tmp_path / "state.json")
        _save_state(path, {"a": "1"})
        _save_state(path, {"b": "2"})
        loaded = _load_state(path)
        assert loaded == {"b": "2"}


# ---------------------------------------------------------------------------
# Connection string parsing tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestConnectionStringParsing:
    def test_plain_kafka(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=eurdep-radiation"
        kafka_config, topic = _parse_connection_string(conn)
        assert kafka_config["bootstrap.servers"] == "localhost:9092"
        assert topic == "eurdep-radiation"

    def test_event_hubs(self):
        conn = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=abc123;EntityPath=eurdep-radiation"
        kafka_config, topic = _parse_connection_string(conn)
        assert "myhub.servicebus.windows.net" in kafka_config["bootstrap.servers"]
        assert topic == "eurdep-radiation"
        assert kafka_config["security.protocol"] == "SASL_SSL"
        assert kafka_config["sasl.mechanism"] == "PLAIN"

    def test_no_entity_path(self):
        conn = "BootstrapServer=localhost:9092"
        kafka_config, topic = _parse_connection_string(conn)
        assert kafka_config["bootstrap.servers"] == "localhost:9092"
        assert topic is None

    def test_empty_connection_string(self):
        kafka_config, topic = _parse_connection_string("")
        assert topic is None


# ---------------------------------------------------------------------------
# Data class serialization tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDataClassSerialization:
    def test_station_to_json(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.station import Station
        s = Station(
            station_id="AT0001",
            name="Laa/ThayaAMS",
            country_code="AT",
            latitude=48.73,
            longitude=16.39,
            height_above_sea=183.0,
            site_status=1,
            site_status_text="in Betrieb",
        )
        j = json.loads(s.to_json())
        assert j["station_id"] == "AT0001"
        assert j["country_code"] == "AT"
        assert j["latitude"] == 48.73
        assert j["height_above_sea"] == 183.0

    def test_station_null_height_to_json(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.station import Station
        s = Station(
            station_id="FR0042",
            name="Paris-Centre",
            country_code="FR",
            latitude=48.86,
            longitude=2.35,
            height_above_sea=None,
            site_status=1,
            site_status_text="en service",
        )
        j = json.loads(s.to_json())
        assert j["height_above_sea"] is None

    def test_reading_to_json(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading
        r = DoseRateReading(
            station_id="DE0123",
            name="Eschede",
            value=0.079,
            unit="µSv/h",
            start_measure="2026-04-08T12:00:00Z",
            end_measure="2026-04-08T13:00:00Z",
            nuclide="Gamma-ODL-Brutto",
            duration="1h",
            validated=1,
        )
        j = json.loads(r.to_json())
        assert j["station_id"] == "DE0123"
        assert j["value"] == 0.079
        assert j["unit"] == "µSv/h"

    def test_reading_null_value_to_json(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading
        r = DoseRateReading(
            station_id="CZ0001",
            name="Praha-Centrum",
            value=None,
            unit="µSv/h",
            start_measure="2026-04-08T12:00:00Z",
            end_measure="2026-04-08T13:00:00Z",
            nuclide="Gamma-ODL-Brutto",
            duration="1h",
            validated=0,
        )
        j = json.loads(r.to_json())
        assert j["value"] is None

    def test_station_avro_roundtrip(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.station import Station
        s = Station(
            station_id="AT0001",
            name="Laa/ThayaAMS",
            country_code="AT",
            latitude=48.73,
            longitude=16.39,
            height_above_sea=183.0,
            site_status=1,
            site_status_text="in Betrieb",
        )
        data = s.to_byte_array("avro/binary")
        restored = Station.from_data(data, "avro/binary")
        assert restored.station_id == "AT0001"
        assert restored.country_code == "AT"
        assert restored.height_above_sea == 183.0

    def test_reading_avro_roundtrip(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading
        r = DoseRateReading(
            station_id="DE0123",
            name="Eschede",
            value=0.079,
            unit="µSv/h",
            start_measure="2026-04-08T12:00:00Z",
            end_measure="2026-04-08T13:00:00Z",
            nuclide="Gamma-ODL-Brutto",
            duration="1h",
            validated=1,
        )
        data = r.to_byte_array("avro/binary")
        restored = DoseRateReading.from_data(data, "avro/binary")
        assert restored.station_id == "DE0123"
        assert restored.value == 0.079

    def test_station_avro_null_height(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.station import Station
        s = Station(
            station_id="FR0042",
            name="Paris",
            country_code="FR",
            latitude=48.86,
            longitude=2.35,
            height_above_sea=None,
            site_status=1,
            site_status_text="en service",
        )
        data = s.to_byte_array("avro/binary")
        restored = Station.from_data(data, "avro/binary")
        assert restored.height_above_sea is None

    def test_reading_avro_null_value(self):
        from eurdep_radiation_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading
        r = DoseRateReading(
            station_id="CZ0001",
            name="Praha",
            value=None,
            unit="µSv/h",
            start_measure="2026-04-08T12:00:00Z",
            end_measure="2026-04-08T13:00:00Z",
            nuclide="Gamma-ODL-Brutto",
            duration="1h",
            validated=0,
        )
        data = r.to_byte_array("avro/binary")
        restored = DoseRateReading.from_data(data, "avro/binary")
        assert restored.value is None


# ---------------------------------------------------------------------------
# Producer import test
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestProducerImport:
    def test_import_event_producer(self):
        from eurdep_radiation_producer_kafka_producer.producer import EuJrcEurdepEventProducer
        assert hasattr(EuJrcEurdepEventProducer, "send_eu_jrc_eurdep_station")
        assert hasattr(EuJrcEurdepEventProducer, "send_eu_jrc_eurdep_dose_rate_reading")

    def test_data_class_imports(self):
        from eurdep_radiation_producer_data import Station, DoseRateReading
        assert Station is not None
        assert DoseRateReading is not None
