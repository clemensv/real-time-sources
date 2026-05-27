"""
Unit tests for USGS Geomagnetism Program bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from usgs_geomag_producer_data import Observatory, MagneticFieldReading
from usgs_geomag.usgs_geomag import USGSGeomagPoller, parse_connection_string


SAMPLE_OBSERVATORIES_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "BOU",
            "properties": {
                "name": "Boulder",
                "agency": "USGS",
                "agency_name": "United States Geological Survey (USGS)",
                "sensor_orientation": "HDZ",
                "sensor_sampling_rate": 100.0,
                "declination_base": 5527
            },
            "geometry": {
                "type": "Point",
                "coordinates": [254.763, 40.137, 1682]
            }
        },
        {
            "type": "Feature",
            "id": "BRW",
            "properties": {
                "name": "Barrow",
                "agency": "USGS",
                "agency_name": "United States Geological Survey (USGS)",
                "sensor_orientation": "HDZ",
                "sensor_sampling_rate": 100.0,
                "declination_base": 10589
            },
            "geometry": {
                "type": "Point",
                "coordinates": [203.378, 71.322, 10]
            }
        },
        {
            "type": "Feature",
            "id": "FRN",
            "properties": {
                "name": "Fresno",
                "agency": "USGS",
                "agency_name": "United States Geological Survey (USGS)",
                "sensor_orientation": "HDZ",
                "sensor_sampling_rate": 100.0,
                "declination_base": 8232
            },
            "geometry": {
                "type": "Point",
                "coordinates": [240.283, 37.091, 331]
            }
        }
    ]
}


SAMPLE_TIMESERIES_RESPONSE = {
    "type": "Timeseries",
    "metadata": {
        "intermagnet": {
            "imo": {
                "iaga_code": "BOU",
                "name": "Boulder",
                "coordinates": [254.763, 40.137, 1682.0]
            },
            "reported_orientation": "HDZF",
            "sensor_orientation": "HDZ",
            "data_type": "variation",
            "sampling_period": 60.0,
            "digital_sampling_rate": 0.01
        },
        "status": 200,
        "generated": "2024-01-01T00:10:00Z",
        "url": None
    },
    "times": [
        "2024-01-01T00:00:00.000Z",
        "2024-01-01T00:01:00.000Z",
        "2024-01-01T00:02:00.000Z",
        "2024-01-01T00:03:00.000Z",
        "2024-01-01T00:04:00.000Z"
    ],
    "values": [
        {
            "id": "H",
            "metadata": {"element": "H", "network": "NT", "station": "BOU", "channel": "H", "location": "R0"},
            "values": [20656.086, 20655.816, 20655.985, 20655.756, 20655.562]
        },
        {
            "id": "D",
            "metadata": {"element": "D", "network": "NT", "station": "BOU", "channel": "D", "location": "R0"},
            "values": [5.173, 5.182, 5.165, 5.169, 5.198]
        },
        {
            "id": "Z",
            "metadata": {"element": "Z", "network": "NT", "station": "BOU", "channel": "Z", "location": "R0"},
            "values": [46726.692, 46726.764, 46726.737, 46726.831, 46726.804]
        },
        {
            "id": "F",
            "metadata": {"element": "F", "network": "NT", "station": "BOU", "channel": "F", "location": "R0"},
            "values": [51107.76, 51107.711, 51107.788, 51107.756, 51107.659]
        }
    ]
}


SAMPLE_TIMESERIES_WITH_NULLS = {
    "type": "Timeseries",
    "metadata": {"status": 200},
    "times": [
        "2024-01-01T00:00:00.000Z",
        "2024-01-01T00:01:00.000Z"
    ],
    "values": [
        {"id": "H", "metadata": {}, "values": [20656.086, None]},
        {"id": "D", "metadata": {}, "values": [None, 5.182]},
        {"id": "Z", "metadata": {}, "values": [46726.692, 46726.764]},
        {"id": "F", "metadata": {}, "values": [51107.76, None]}
    ]
}


SAMPLE_EMPTY_TIMESERIES = {
    "type": "Timeseries",
    "metadata": {"status": 200},
    "times": [],
    "values": []
}


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for the parse_connection_string helper."""

    def test_parse_event_hubs_connection_string(self):
        cs = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'myns.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myhub'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['security.protocol'] == 'SASL_SSL'

    def test_parse_plain_bootstrap_server(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'test-topic'
        assert 'sasl.username' not in result

    def test_parse_invalid_returns_empty(self):
        result = parse_connection_string("")
        assert 'bootstrap.servers' not in result
        assert 'kafka_topic' not in result


@pytest.mark.unit
class TestParseObservatory:
    """Unit tests for observatory parsing."""

    def test_parse_observatory_basic(self):
        feature = SAMPLE_OBSERVATORIES_GEOJSON["features"][0]
        obs = USGSGeomagPoller.parse_observatory(feature)
        assert obs.iaga_code == "BOU"
        assert obs.name == "Boulder"
        assert obs.agency == "USGS"
        assert obs.agency_name == "United States Geological Survey (USGS)"
        assert obs.latitude == 40.137
        assert obs.longitude == 254.763
        assert obs.elevation == 1682
        assert obs.sensor_orientation == "HDZ"
        assert obs.sensor_sampling_rate == 100.0
        assert obs.declination_base == 5527

    def test_parse_observatory_barrow(self):
        feature = SAMPLE_OBSERVATORIES_GEOJSON["features"][1]
        obs = USGSGeomagPoller.parse_observatory(feature)
        assert obs.iaga_code == "BRW"
        assert obs.name == "Barrow"
        assert obs.latitude == 71.322
        assert obs.longitude == 203.378
        assert obs.elevation == 10

    def test_parse_observatory_missing_geometry(self):
        feature = {
            "type": "Feature",
            "id": "TST",
            "properties": {"name": "Test"},
            "geometry": {}
        }
        obs = USGSGeomagPoller.parse_observatory(feature)
        assert obs.iaga_code == "TST"
        assert obs.latitude is None
        assert obs.longitude is None
        assert obs.elevation is None

    def test_parse_observatory_empty_properties(self):
        feature = {
            "type": "Feature",
            "id": "XX",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [0, 0, 0]}
        }
        obs = USGSGeomagPoller.parse_observatory(feature)
        assert obs.iaga_code == "XX"
        assert obs.name == ""
        assert obs.agency is None
        assert obs.sensor_orientation is None


@pytest.mark.unit
class TestParseTimeseries:
    """Unit tests for timeseries parsing."""

    def test_parse_basic_timeseries(self):
        readings = USGSGeomagPoller.parse_timeseries("BOU", SAMPLE_TIMESERIES_RESPONSE)
        assert len(readings) == 5
        r0 = readings[0]
        assert r0.iaga_code == "BOU"
        assert r0.timestamp == datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert r0.h == 20656.086
        assert r0.d == 5.173
        assert r0.z == 46726.692
        assert r0.f == 51107.76

    def test_parse_timeseries_values(self):
        readings = USGSGeomagPoller.parse_timeseries("BOU", SAMPLE_TIMESERIES_RESPONSE)
        r4 = readings[4]
        assert r4.h == 20655.562
        assert r4.d == 5.198
        assert r4.z == 46726.804
        assert r4.f == 51107.659

    def test_parse_timeseries_timestamps(self):
        readings = USGSGeomagPoller.parse_timeseries("BOU", SAMPLE_TIMESERIES_RESPONSE)
        assert readings[1].timestamp == datetime(2024, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
        assert readings[2].timestamp == datetime(2024, 1, 1, 0, 2, 0, tzinfo=timezone.utc)
        assert readings[3].timestamp == datetime(2024, 1, 1, 0, 3, 0, tzinfo=timezone.utc)

    def test_parse_timeseries_with_nulls(self):
        readings = USGSGeomagPoller.parse_timeseries("BOU", SAMPLE_TIMESERIES_WITH_NULLS)
        assert len(readings) == 2
        r0 = readings[0]
        assert r0.h == 20656.086
        assert r0.d is None
        assert r0.z == 46726.692
        assert r0.f == 51107.76

        r1 = readings[1]
        assert r1.h is None
        assert r1.d == 5.182
        assert r1.z == 46726.764
        assert r1.f is None

    def test_parse_empty_timeseries(self):
        readings = USGSGeomagPoller.parse_timeseries("BOU", SAMPLE_EMPTY_TIMESERIES)
        assert len(readings) == 0

    def test_parse_timeseries_missing_element(self):
        """Test when some elements are missing entirely from values."""
        data = {
            "times": ["2024-01-01T00:00:00.000Z"],
            "values": [
                {"id": "H", "metadata": {}, "values": [20000.0]},
            ]
        }
        readings = USGSGeomagPoller.parse_timeseries("CMO", data)
        assert len(readings) == 1
        assert readings[0].h == 20000.0
        assert readings[0].d is None
        assert readings[0].z is None
        assert readings[0].f is None
        assert readings[0].iaga_code == "CMO"

    def test_parse_timeseries_invalid_timestamp(self):
        data = {
            "times": ["not-a-timestamp", "2024-01-01T00:01:00.000Z"],
            "values": [
                {"id": "H", "metadata": {}, "values": [100.0, 200.0]},
            ]
        }
        readings = USGSGeomagPoller.parse_timeseries("BOU", data)
        assert len(readings) == 1
        assert readings[0].h == 200.0


@pytest.mark.unit
class TestObservatoryDataClass:
    """Unit tests for the Observatory data class."""

    def test_create_instance(self):
        obs = Observatory.create_instance()
        assert obs.iaga_code == "BOU"
        assert obs.name == "Boulder"
        assert obs.latitude == 40.137

    def test_to_serializer_dict(self):
        obs = Observatory(
            iaga_code="FRN", name="Fresno", agency="USGS",
            agency_name="United States Geological Survey (USGS)",
            latitude=37.091, longitude=240.283, elevation=331.0,
            sensor_orientation="HDZ", sensor_sampling_rate=100.0,
            declination_base=8232
        )
        d = obs.to_serializer_dict()
        assert d["iaga_code"] == "FRN"
        assert d["name"] == "Fresno"
        assert d["latitude"] == 37.091

    def test_from_serializer_dict(self):
        data = {
            "iaga_code": "HON", "name": "Honolulu",
            "agency": "USGS", "agency_name": None,
            "latitude": 21.316, "longitude": 202.0,
            "elevation": 4.0, "sensor_orientation": "HDZ",
            "sensor_sampling_rate": 100.0, "declination_base": None
        }
        obs = Observatory.from_serializer_dict(data)
        assert obs.iaga_code == "HON"
        assert obs.name == "Honolulu"

    def test_observatory_nullable_fields(self):
        obs = Observatory(
            iaga_code="TST", name="Test",
            agency=None, agency_name=None,
            latitude=None, longitude=None, elevation=None,
            sensor_orientation=None, sensor_sampling_rate=None,
            declination_base=None
        )
        assert obs.agency is None
        assert obs.latitude is None
        assert obs.elevation is None


@pytest.mark.unit
class TestMagneticFieldReadingDataClass:
    """Unit tests for the MagneticFieldReading data class."""

    def test_create_instance(self):
        reading = MagneticFieldReading.create_instance()
        assert reading.iaga_code == "BOU"
        assert reading.h == 20656.086
        assert reading.d == 5.173

    def test_to_serializer_dict(self):
        reading = MagneticFieldReading(
            iaga_code="BOU",
            timestamp=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            h=20656.0, d=5.17, z=46726.7, f=51107.8
        )
        d = reading.to_serializer_dict()
        assert d["iaga_code"] == "BOU"
        assert d["h"] == 20656.0
        assert d["d"] == 5.17

    def test_from_serializer_dict(self):
        data = {
            "iaga_code": "BRW",
            "timestamp": datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
            "h": 10000.0, "d": 10.0, "z": 50000.0, "f": 55000.0
        }
        reading = MagneticFieldReading.from_serializer_dict(data)
        assert reading.iaga_code == "BRW"
        assert reading.h == 10000.0

    def test_nullable_reading_fields(self):
        reading = MagneticFieldReading(
            iaga_code="TST",
            timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
            h=None, d=None, z=None, f=None
        )
        assert reading.h is None
        assert reading.d is None
        assert reading.z is None
        assert reading.f is None


@pytest.mark.unit
class TestUSGSGeomagPoller:
    """Unit tests for the USGSGeomagPoller class."""

    @pytest.fixture
    def mock_kafka_config(self):
        return {
            'bootstrap.servers': 'localhost:9092',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': 'test_user',
            'sasl.password': 'test_password'
        }

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = USGSGeomagPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )
        assert poller.kafka_topic == 'test-topic'
        assert poller.last_polled_file == temp_state_file
        assert poller.observatories == [
            "BOU", "BRW", "BSL", "CMO", "DED", "FRD", "FRN",
            "GUA", "HON", "NEW", "SHU", "SIT", "SJG", "TUC",
        ]
        mock_producer_class.assert_called_once_with(mock_kafka_config)

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init_custom_observatories(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        poller = USGSGeomagPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
            observatories=["BOU", "FRN"]
        )
        assert poller.observatories == ["BOU", "FRN"]

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_empty(self, mock_producer_class, mock_event_producer, mock_kafka_config):
        poller = USGSGeomagPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file='/nonexistent/path/state.json'
        )
        state = poller.load_state()
        assert state == {"last_timestamps": {}, "last_reference_emit": None}

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    def test_load_state_existing(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        state_data = {
            "last_timestamps": {"BOU": "2024-01-01T00:05:00+00:00"},
            "last_reference_emit": "2024-01-01T00:00:00+00:00"
        }
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        poller = USGSGeomagPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )
        state = poller.load_state()
        assert state["last_timestamps"]["BOU"] == "2024-01-01T00:05:00+00:00"
        assert state["last_reference_emit"] == "2024-01-01T00:00:00+00:00"

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    def test_save_state(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        poller = USGSGeomagPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )
        state_data = {
            "last_timestamps": {"BOU": "2024-01-01T00:05:00+00:00"},
            "last_reference_emit": "2024-01-01T00:00:00+00:00"
        }
        poller.save_state(state_data)

        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["last_timestamps"]["BOU"] == "2024-01-01T00:05:00+00:00"

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('usgs_geomag.usgs_geomag.requests.get')
    def test_fetch_observatories(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_OBSERVATORIES_GEOJSON
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        features = USGSGeomagPoller.fetch_observatories()
        assert len(features) == 3
        assert features[0]["id"] == "BOU"
        assert features[1]["id"] == "BRW"

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('usgs_geomag.usgs_geomag.requests.get')
    def test_fetch_observatories_error(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Network error")
        features = USGSGeomagPoller.fetch_observatories()
        assert features == []

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('usgs_geomag.usgs_geomag.requests.get')
    def test_fetch_variation_data(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_TIMESERIES_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        data = USGSGeomagPoller.fetch_variation_data("BOU", "2024-01-01T00:00:00Z", "2024-01-01T00:05:00Z")
        assert data is not None
        assert data["type"] == "Timeseries"

        # Verify the request parameters
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args
        params = call_kwargs[1]["params"]
        assert params["id"] == "BOU"
        assert params["type"] == "variation"
        assert params["elements"] == "H,D,Z,F"
        assert params["sampling_period"] == "60"

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('usgs_geomag.usgs_geomag.requests.get')
    def test_fetch_variation_data_error(self, mock_get, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        mock_get.side_effect = Exception("Timeout")
        data = USGSGeomagPoller.fetch_variation_data("BOU", "2024-01-01T00:00:00Z", "2024-01-01T00:05:00Z")
        assert data is None

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    def test_default_observatories_list(self, mock_producer_class, mock_event_producer, mock_kafka_config, temp_state_file):
        """Verify all expected observatories are in the default list."""
        from usgs_geomag.usgs_geomag import DEFAULT_OBSERVATORIES
        expected = {"BOU", "BRW", "BSL", "CMO", "DED", "FRD", "FRN",
                    "GUA", "HON", "NEW", "SHU", "SIT", "SJG", "TUC"}
        assert set(DEFAULT_OBSERVATORIES) == expected

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('usgs_geomag.usgs_geomag.USGSGeomagPoller.fetch_observatories')
    @patch('usgs_geomag.usgs_geomag.USGSGeomagPoller.fetch_variation_data')
    def test_poll_and_send_once(self, mock_fetch_data, mock_fetch_obs,
                                mock_producer_class, mock_event_producer,
                                mock_kafka_config, temp_state_file):
        """Test poll_and_send with once=True executes one iteration."""
        mock_fetch_obs.return_value = SAMPLE_OBSERVATORIES_GEOJSON["features"]
        mock_fetch_data.return_value = SAMPLE_TIMESERIES_RESPONSE

        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_ep = Mock()
        mock_ep.producer = Mock()
        mock_ep.producer.flush = Mock()
        mock_event_producer.return_value = mock_ep

        poller = USGSGeomagPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
            observatories=["BOU"]
        )
        poller.poll_and_send(once=True)

        # Reference data should be emitted
        mock_ep.send_gov_usgs_geomag_observatory.assert_called()
        # Telemetry should be emitted
        mock_ep.send_gov_usgs_geomag_magnetic_field_reading.assert_called()

    @patch('usgs_geomag.usgs_geomag.GovUsgsGeomagEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('usgs_geomag.usgs_geomag.USGSGeomagPoller.fetch_observatories')
    @patch('usgs_geomag.usgs_geomag.USGSGeomagPoller.fetch_variation_data')
    def test_deduplication(self, mock_fetch_data, mock_fetch_obs,
                           mock_producer_class, mock_event_producer,
                           mock_kafka_config, temp_state_file):
        """Test that readings with already-seen timestamps are skipped."""
        mock_fetch_obs.return_value = SAMPLE_OBSERVATORIES_GEOJSON["features"]
        mock_fetch_data.return_value = SAMPLE_TIMESERIES_RESPONSE

        # Pre-set state with last seen timestamp at 00:03
        state_data = {
            "last_timestamps": {"BOU": "2024-01-01T00:03:00+00:00"},
            "last_reference_emit": "2024-01-01T00:00:00+00:00"
        }
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_ep = Mock()
        mock_ep.producer = Mock()
        mock_ep.producer.flush = Mock()
        mock_event_producer.return_value = mock_ep

        poller = USGSGeomagPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file,
            observatories=["BOU"]
        )
        poller.poll_and_send(once=True)

        # Only the reading at 00:04 should be sent (00:00-00:03 already seen)
        reading_calls = mock_ep.send_gov_usgs_geomag_magnetic_field_reading.call_args_list
        assert len(reading_calls) == 1
        sent_reading = reading_calls[0][0][1]
        assert sent_reading.timestamp == datetime(2024, 1, 1, 0, 4, 0, tzinfo=timezone.utc)

    def test_parse_connection_string_bootstrap(self):
        cs = "BootstrapServer=broker1:9092;EntityPath=my-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'broker1:9092'
        assert result['kafka_topic'] == 'my-topic'

    def test_parse_connection_string_empty(self):
        result = parse_connection_string("")
        assert 'bootstrap.servers' not in result


@pytest.mark.unit
class TestUrlConstruction:
    """Unit tests for URL construction and API parameter formatting."""

    @patch('usgs_geomag.usgs_geomag.requests.get')
    def test_data_url_params(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_TIMESERIES_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        USGSGeomagPoller.fetch_variation_data("HON", "2024-06-01T00:00:00Z", "2024-06-01T01:00:00Z")

        mock_get.assert_called_once()
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["id"] == "HON"
        assert params["format"] == "json"
        assert params["starttime"] == "2024-06-01T00:00:00Z"
        assert params["endtime"] == "2024-06-01T01:00:00Z"

    @patch('usgs_geomag.usgs_geomag.requests.get')
    def test_observatories_url(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_OBSERVATORIES_GEOJSON
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        USGSGeomagPoller.fetch_observatories()
        mock_get.assert_called_once_with(
            "https://geomag.usgs.gov/ws/observatories/", timeout=60)
