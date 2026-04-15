"""Unit tests for the Canada ECCC Water Office bridge."""

import datetime
import pytest
from unittest.mock import MagicMock, patch

from canada_eccc_wateroffice.canada_eccc_wateroffice import (
    ECCCWaterOfficeAPI,
    parse_connection_string,
    send_stations,
    feed,
    OBSERVATION_WINDOW_SECONDS,
)
from canada_eccc_wateroffice_producer_data import Station, Observation
from canada_eccc_wateroffice_producer_kafka_producer.producer import CAGovECCCHydroEventProducer


SAMPLE_STATION_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-114.56986, 50.94851]},
    "properties": {
        "STATION_NUMBER": "05BJ004",
        "STATION_NAME": "ELBOW RIVER AT BRAGG CREEK",
        "PROV_TERR_STATE_LOC": "AB",
        "STATUS_EN": "Active",
        "CONTRIBUTOR_EN": "Water Survey of Canada",
        "DRAINAGE_AREA_GROSS": 790.0,
        "DRAINAGE_AREA_EFFECT": 790.0,
        "RHBN": 0,
        "REAL_TIME": 1,
    },
}

SAMPLE_STATION_FEATURE_NULL_GEOMETRY = {
    "type": "Feature",
    "geometry": None,
    "properties": {
        "STATION_NUMBER": "05BJ005",
        "STATION_NAME": "TEST RIVER AT TEST CREEK",
        "PROV_TERR_STATE_LOC": "AB",
        "STATUS_EN": None,
        "CONTRIBUTOR_EN": None,
        "DRAINAGE_AREA_GROSS": None,
        "DRAINAGE_AREA_EFFECT": None,
        "RHBN": None,
        "REAL_TIME": None,
    },
}

SAMPLE_OBSERVATION_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-114.56986, 50.94851]},
    "properties": {
        "IDENTIFIER": "05BJ004.2026-03-07T07:00:00Z",
        "STATION_NUMBER": "05BJ004",
        "STATION_NAME": "ELBOW RIVER AT BRAGG CREEK",
        "PROV_TERR_STATE_LOC": "AB",
        "DATETIME": "2026-03-07T07:00:00Z",
        "LEVEL": 0.669,
        "DISCHARGE": None,
    },
}

SAMPLE_OBSERVATION_FEATURE_WITH_DISCHARGE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-114.56986, 50.94851]},
    "properties": {
        "IDENTIFIER": "05BJ004.2026-03-07T08:00:00Z",
        "STATION_NUMBER": "05BJ004",
        "STATION_NAME": "ELBOW RIVER AT BRAGG CREEK",
        "PROV_TERR_STATE_LOC": "AB",
        "DATETIME": "2026-03-07T08:00:00Z",
        "LEVEL": 0.71,
        "DISCHARGE": 12.5,
    },
}

SAMPLE_OBSERVATION_FEATURE_MISSING_FIELDS = {
    "type": "Feature",
    "geometry": None,
    "properties": {
        "IDENTIFIER": None,
        "STATION_NUMBER": None,
        "STATION_NAME": None,
        "PROV_TERR_STATE_LOC": None,
        "DATETIME": None,
        "LEVEL": None,
        "DISCHARGE": None,
    },
}


@pytest.mark.unit
class TestECCCWaterOfficeAPI:
    """Tests for ECCCWaterOfficeAPI parsing methods."""

    def test_parse_station_basic(self):
        station = ECCCWaterOfficeAPI.parse_station(SAMPLE_STATION_FEATURE)
        assert station.station_number == "05BJ004"
        assert station.station_name == "ELBOW RIVER AT BRAGG CREEK"
        assert station.prov_terr_state_loc == "AB"
        assert station.status_en == "Active"
        assert station.contributor_en == "Water Survey of Canada"
        assert station.drainage_area_gross == 790.0
        assert station.drainage_area_effect == 790.0
        assert station.real_time is True
        # RHBN=0 becomes None via generated __post_init__ (falsy int → None)
        assert station.rhbn is None
        assert abs(station.longitude - (-114.56986)) < 1e-5
        assert abs(station.latitude - 50.94851) < 1e-5

    def test_parse_station_null_geometry(self):
        station = ECCCWaterOfficeAPI.parse_station(SAMPLE_STATION_FEATURE_NULL_GEOMETRY)
        assert station.station_number == "05BJ005"
        assert station.latitude is None
        assert station.longitude is None
        assert station.drainage_area_gross is None
        assert station.drainage_area_effect is None
        assert station.rhbn is None
        assert station.real_time is None
        assert station.status_en is None

    def test_parse_observation_basic(self):
        obs = ECCCWaterOfficeAPI.parse_observation(SAMPLE_OBSERVATION_FEATURE)
        assert obs is not None
        assert obs.station_number == "05BJ004"
        assert obs.identifier == "05BJ004.2026-03-07T07:00:00Z"
        assert obs.station_name == "ELBOW RIVER AT BRAGG CREEK"
        assert obs.prov_terr_state_loc == "AB"
        assert obs.level == 0.669
        assert obs.discharge is None
        assert obs.latitude is not None
        assert obs.longitude is not None

    def test_parse_observation_with_discharge(self):
        obs = ECCCWaterOfficeAPI.parse_observation(SAMPLE_OBSERVATION_FEATURE_WITH_DISCHARGE)
        assert obs is not None
        assert obs.level == 0.71
        assert obs.discharge == 12.5

    def test_parse_observation_missing_required_fields(self):
        obs = ECCCWaterOfficeAPI.parse_observation(SAMPLE_OBSERVATION_FEATURE_MISSING_FIELDS)
        assert obs is None

    def test_parse_observation_datetime_parsed(self):
        obs = ECCCWaterOfficeAPI.parse_observation(SAMPLE_OBSERVATION_FEATURE)
        assert obs is not None
        assert isinstance(obs.observation_datetime, datetime.datetime)
        assert obs.observation_datetime.year == 2026
        assert obs.observation_datetime.month == 3
        assert obs.observation_datetime.day == 7

    def test_parse_observation_bad_datetime(self):
        feature = {
            "type": "Feature",
            "geometry": None,
            "properties": {
                "IDENTIFIER": "05BJ004.bad",
                "STATION_NUMBER": "05BJ004",
                "STATION_NAME": "TEST",
                "PROV_TERR_STATE_LOC": "AB",
                "DATETIME": "not-a-date",
                "LEVEL": 1.0,
                "DISCHARGE": None,
            },
        }
        obs = ECCCWaterOfficeAPI.parse_observation(feature)
        assert obs is None


@pytest.mark.unit
class TestConnectionStringParsing:
    """Tests for parse_connection_string."""

    def test_bootstrap_server(self):
        conn_str = "BootstrapServer=localhost:9092"
        config = parse_connection_string(conn_str)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert "sasl.username" not in config

    def test_event_hubs_connection_string(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=mykey;SharedAccessKey=secretval"
        config = parse_connection_string(conn_str)
        assert config["bootstrap.servers"] == "test.servicebus.windows.net:9093"
        assert config["sasl.username"] == "$ConnectionString"
        assert config["sasl.password"] == conn_str
        assert config["security.protocol"] == "SASL_SSL"
        assert config["sasl.mechanism"] == "PLAIN"

    def test_entity_path_extracted(self):
        conn_str = "BootstrapServer=broker:9092;EntityPath=my-topic"
        config = parse_connection_string(conn_str)
        assert config["_entity_path"] == "my-topic"

    def test_empty_string(self):
        config = parse_connection_string("")
        assert "bootstrap.servers" not in config


@pytest.mark.unit
class TestFlushFailure:
    """Dedupe state must not advance when Kafka flush returns non-zero remainder."""

    def test_flush_failure_does_not_advance_seen_ids(self):
        mock_inner_producer = MagicMock()
        mock_inner_producer.flush.return_value = 1  # non-zero = not all delivered

        mock_event_producer = MagicMock(spec=CAGovECCCHydroEventProducer)
        mock_event_producer.producer = mock_inner_producer

        api = ECCCWaterOfficeAPI()
        seen_ids: set = set()

        with patch.object(api, "get_observations", return_value=[SAMPLE_OBSERVATION_FEATURE]):
            count = feed(api, mock_event_producer, seen_ids, {})

        assert count == 0
        assert len(seen_ids) == 0, "seen_ids must not advance when flush fails"

    def test_flush_success_advances_seen_ids(self):
        mock_inner_producer = MagicMock()
        mock_inner_producer.flush.return_value = 0  # zero = all delivered

        mock_event_producer = MagicMock(spec=CAGovECCCHydroEventProducer)
        mock_event_producer.producer = mock_inner_producer

        api = ECCCWaterOfficeAPI()
        seen_ids: set = set()

        with patch.object(api, "get_observations", return_value=[SAMPLE_OBSERVATION_FEATURE]):
            count = feed(api, mock_event_producer, seen_ids, {})

        assert count == 1
        assert "05BJ004.2026-03-07T07:00:00Z" in seen_ids

    def test_already_seen_observations_are_skipped(self):
        mock_inner_producer = MagicMock()
        mock_inner_producer.flush.return_value = 0

        mock_event_producer = MagicMock(spec=CAGovECCCHydroEventProducer)
        mock_event_producer.producer = mock_inner_producer

        api = ECCCWaterOfficeAPI()
        seen_ids = {"05BJ004.2026-03-07T07:00:00Z"}

        with patch.object(api, "get_observations", return_value=[SAMPLE_OBSERVATION_FEATURE]):
            count = feed(api, mock_event_producer, seen_ids, {})

        assert count == 0
        mock_event_producer.send_ca_gov_eccc_hydro_observation.assert_not_called()


@pytest.mark.unit
class TestStationRefreshCache:
    """Station catalog must be preserved when a refresh attempt fails."""

    def test_failed_refresh_retains_old_cache(self):
        """When send_stations raises, the caller's cached catalog should be unchanged."""
        original_stations = {
            "05BJ004": ECCCWaterOfficeAPI.parse_station(SAMPLE_STATION_FEATURE)
        }
        stations = dict(original_stations)

        mock_inner_producer = MagicMock()
        mock_inner_producer.flush.return_value = 0

        mock_event_producer = MagicMock(spec=CAGovECCCHydroEventProducer)
        mock_event_producer.producer = mock_inner_producer

        api = ECCCWaterOfficeAPI()

        with patch.object(api, "get_all_stations", side_effect=Exception("upstream timeout")):
            try:
                new_stations = send_stations(api, mock_event_producer)
                stations = new_stations
            except Exception:
                pass  # caller catches and keeps the old cache

        assert "05BJ004" in stations
        assert stations["05BJ004"].station_name == "ELBOW RIVER AT BRAGG CREEK"

    def test_successful_refresh_replaces_cache(self):
        """When send_stations succeeds, the new catalog replaces the old one."""
        mock_inner_producer = MagicMock()
        mock_inner_producer.flush.return_value = 0

        mock_event_producer = MagicMock(spec=CAGovECCCHydroEventProducer)
        mock_event_producer.producer = mock_inner_producer

        api = ECCCWaterOfficeAPI()

        with patch.object(api, "get_all_stations", return_value=[SAMPLE_STATION_FEATURE]):
            new_stations = send_stations(api, mock_event_producer)

        assert "05BJ004" in new_stations
        assert new_stations["05BJ004"].station_name == "ELBOW RIVER AT BRAGG CREEK"
