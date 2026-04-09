"""Unit tests for GeoSphere Austria TAWES bridge."""

import json
import pytest

from geosphere_austria.geosphere_austria import (
    PARAM_MAP,
    fetch_station_metadata,
    observation_fingerprint,
    parse_connection_string,
    parse_observation,
    parse_station,
    send_observation_events,
    send_station_events,
    load_state,
    save_state,
)
from geosphere_austria_producer_data import WeatherObservation, WeatherStation

pytestmark = pytest.mark.unit

# ---------------------------------------------------------------------------
# Sample data fixtures
# ---------------------------------------------------------------------------

SAMPLE_STATION_RAW = {
    "type": "INDIVIDUAL",
    "id": "11035",
    "name": "WIEN HOHE WARTE",
    "state": "Wien",
    "lat": 48.2486,
    "lon": 16.3564,
    "altitude": 198.0,
    "valid_from": "1990-01-01T00:00:00",
    "valid_to": "2027-01-01T00:00:00",
    "has_sunshine": True,
    "has_global_radiation": True,
    "is_active": True,
}

SAMPLE_STATION_NO_STATE = {
    "type": "INDIVIDUAL",
    "id": "99999",
    "name": "TEST STATION",
    "lat": 47.0,
    "lon": 15.0,
    "altitude": 500.0,
    "is_active": True,
}

SAMPLE_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [16.3564, 48.2486]},
    "properties": {
        "parameters": {
            "TL": {"name": "Lufttemperatur", "unit": "°C", "data": [3.9]},
            "RF": {"name": "Relative Feuchte", "unit": "%", "data": [64.0]},
            "RR": {"name": "Niederschlag", "unit": "mm", "data": [0.0]},
            "DD": {"name": "Windrichtung", "unit": "°", "data": [296.0]},
            "FF": {"name": "Windgeschwindigkeit", "unit": "m/s", "data": [3.2]},
            "P": {"name": "Luftdruck", "unit": "hPa", "data": [999.7]},
            "SO": {"name": "Sonnenscheindauer", "unit": "sec", "data": [0.0]},
            "GLOW": {"name": "Globalstrahlung", "unit": "W/m²", "data": [0.0]},
        },
        "station": "11035",
    },
}

SAMPLE_FEATURE_NULL = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [11.7, 47.5]},
    "properties": {
        "parameters": {
            "TL": {"name": "Lufttemperatur", "unit": "°C", "data": [None]},
            "RF": {"name": "Relative Feuchte", "unit": "%", "data": [None]},
            "RR": {"name": "Niederschlag", "unit": "mm", "data": [0.0]},
            "DD": {"name": "Windrichtung", "unit": "°", "data": [None]},
            "FF": {"name": "Windgeschwindigkeit", "unit": "m/s", "data": [None]},
            "P": {"name": "Luftdruck", "unit": "hPa", "data": [None]},
        },
        "station": "11266",
    },
}

SAMPLE_GEOJSON_RESPONSE = {
    "media_type": "application/json",
    "type": "FeatureCollection",
    "version": "v1",
    "timestamps": ["2024-01-15T13:00+00:00"],
    "features": [SAMPLE_FEATURE],
}

SAMPLE_METADATA_RESPONSE = {
    "title": "TAWES",
    "parameters": [],
    "stations": [
        SAMPLE_STATION_RAW,
        {
            "type": "INDIVIDUAL",
            "id": "99998",
            "name": "INACTIVE STATION",
            "state": "Tirol",
            "lat": 47.0,
            "lon": 11.0,
            "altitude": 600.0,
            "is_active": False,
        },
        SAMPLE_STATION_NO_STATE,
    ],
}


# ---------------------------------------------------------------------------
# Connection string parsing
# ---------------------------------------------------------------------------


class TestParseConnectionString:
    """Tests for parse_connection_string."""

    def test_bootstrap_server_format(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        config, topic = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert topic == "my-topic"

    def test_bootstrap_server_no_tls(self, monkeypatch):
        monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
        cs = "BootstrapServer=broker:9092;EntityPath=test-topic"
        config, topic = parse_connection_string(cs)
        assert config["security.protocol"] == "PLAINTEXT"
        assert topic == "test-topic"

    def test_bootstrap_server_tls_default(self, monkeypatch):
        monkeypatch.delenv("KAFKA_ENABLE_TLS", raising=False)
        cs = "BootstrapServer=broker:9092;EntityPath=test-topic"
        config, _ = parse_connection_string(cs)
        assert "security.protocol" not in config

    def test_event_hubs_format(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=key;SharedAccessKey=secret;EntityPath=eh-topic"
        config, topic = parse_connection_string(cs)
        assert "ns.servicebus.windows.net:9093" in config["bootstrap.servers"]
        assert config["security.protocol"] == "SASL_SSL"
        assert config["sasl.mechanisms"] == "PLAIN"
        assert topic == "eh-topic"

    def test_invalid_connection_string(self):
        with pytest.raises(ValueError):
            parse_connection_string("not-a-valid-string")

    def test_bootstrap_server_no_entity_path(self):
        cs = "BootstrapServer=localhost:9092"
        config, topic = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert topic is None


# ---------------------------------------------------------------------------
# Station metadata parsing
# ---------------------------------------------------------------------------


class TestParseStation:
    """Tests for parse_station."""

    def test_basic_station(self):
        station = parse_station(SAMPLE_STATION_RAW)
        assert station.station_id == "11035"
        assert station.station_name == "WIEN HOHE WARTE"
        assert station.latitude == 48.2486
        assert station.longitude == 16.3564
        assert station.altitude == 198.0
        assert station.state == "Wien"

    def test_station_without_state(self):
        station = parse_station(SAMPLE_STATION_NO_STATE)
        assert station.station_id == "99999"
        assert station.state is None

    def test_station_id_is_string(self):
        raw = {**SAMPLE_STATION_RAW, "id": 12345}
        station = parse_station(raw)
        assert station.station_id == "12345"
        assert isinstance(station.station_id, str)

    def test_station_empty_state_becomes_none(self):
        raw = {**SAMPLE_STATION_RAW, "state": ""}
        station = parse_station(raw)
        assert station.state is None

    def test_station_altitude_default(self):
        raw = dict(SAMPLE_STATION_RAW)
        del raw["altitude"]
        station = parse_station(raw)
        assert station.altitude == 0.0


# ---------------------------------------------------------------------------
# Observation parsing
# ---------------------------------------------------------------------------


class TestParseObservation:
    """Tests for parse_observation."""

    def test_full_observation(self):
        obs = parse_observation(SAMPLE_FEATURE, "2024-01-15T13:00+00:00")
        assert obs is not None
        assert obs.station_id == "11035"
        assert obs.observation_time == "2024-01-15T13:00+00:00"
        assert obs.temperature == 3.9
        assert obs.humidity == 64.0
        assert obs.precipitation == 0.0
        assert obs.wind_direction == 296.0
        assert obs.wind_speed == 3.2
        assert obs.pressure == 999.7
        assert obs.sunshine_duration == 0.0
        assert obs.global_radiation == 0.0

    def test_null_values(self):
        obs = parse_observation(SAMPLE_FEATURE_NULL, "2024-01-15T13:00+00:00")
        assert obs is not None
        assert obs.station_id == "11266"
        assert obs.temperature is None
        assert obs.humidity is None
        assert obs.precipitation == 0.0
        assert obs.wind_direction is None
        assert obs.wind_speed is None
        assert obs.pressure is None
        assert obs.sunshine_duration is None
        assert obs.global_radiation is None

    def test_missing_station_returns_none(self):
        feature = {"type": "Feature", "geometry": {}, "properties": {"parameters": {}}}
        obs = parse_observation(feature, "2024-01-15T13:00+00:00")
        assert obs is None

    def test_missing_parameter_returns_none_value(self):
        feature = {
            "type": "Feature",
            "geometry": {},
            "properties": {
                "parameters": {
                    "TL": {"name": "Temp", "unit": "°C", "data": [5.0]},
                },
                "station": "12345",
            },
        }
        obs = parse_observation(feature, "2024-01-15T13:00+00:00")
        assert obs.temperature == 5.0
        assert obs.humidity is None
        assert obs.precipitation is None

    def test_empty_data_array(self):
        feature = {
            "type": "Feature",
            "geometry": {},
            "properties": {
                "parameters": {
                    "TL": {"name": "Temp", "unit": "°C", "data": []},
                },
                "station": "12345",
            },
        }
        obs = parse_observation(feature, "2024-01-15T13:00+00:00")
        assert obs.temperature is None

    def test_zero_values_preserved(self):
        """Ensure zero values are not treated as None."""
        feature = {
            "type": "Feature",
            "geometry": {},
            "properties": {
                "parameters": {
                    "TL": {"name": "Temp", "unit": "°C", "data": [0.0]},
                    "RR": {"name": "Niederschlag", "unit": "mm", "data": [0.0]},
                    "SO": {"name": "Sonnenschein", "unit": "sec", "data": [0.0]},
                },
                "station": "12345",
            },
        }
        obs = parse_observation(feature, "2024-01-15T13:00+00:00")
        assert obs.temperature == 0.0
        assert obs.precipitation == 0.0
        assert obs.sunshine_duration == 0.0


# ---------------------------------------------------------------------------
# PARAM_MAP coverage
# ---------------------------------------------------------------------------


class TestParamMap:
    """Verify PARAM_MAP completeness."""

    def test_all_params_present(self):
        expected = {"TL", "RF", "RR", "DD", "FF", "P", "SO", "GLOW"}
        assert set(PARAM_MAP.keys()) == expected

    def test_all_fields_mapped(self):
        expected_fields = {
            "temperature", "humidity", "precipitation", "wind_direction",
            "wind_speed", "pressure", "sunshine_duration", "global_radiation",
        }
        assert set(PARAM_MAP.values()) == expected_fields


# ---------------------------------------------------------------------------
# Observation fingerprint
# ---------------------------------------------------------------------------


class TestObservationFingerprint:
    """Tests for observation_fingerprint dedup logic."""

    def test_same_data_same_fingerprint(self):
        obs1 = WeatherObservation(
            station_id="11035", observation_time="2024-01-15T13:00+00:00",
            temperature=3.9, humidity=64.0, precipitation=0.0,
            wind_direction=296.0, wind_speed=3.2, pressure=999.7,
            sunshine_duration=0.0, global_radiation=0.0,
        )
        obs2 = WeatherObservation(
            station_id="11035", observation_time="2024-01-15T13:00+00:00",
            temperature=3.9, humidity=64.0, precipitation=0.0,
            wind_direction=296.0, wind_speed=3.2, pressure=999.7,
            sunshine_duration=0.0, global_radiation=0.0,
        )
        assert observation_fingerprint(obs1) == observation_fingerprint(obs2)

    def test_different_data_different_fingerprint(self):
        obs1 = WeatherObservation(
            station_id="11035", observation_time="2024-01-15T13:00+00:00",
            temperature=3.9, humidity=64.0, precipitation=0.0,
            wind_direction=296.0, wind_speed=3.2, pressure=999.7,
            sunshine_duration=0.0, global_radiation=0.0,
        )
        obs2 = WeatherObservation(
            station_id="11035", observation_time="2024-01-15T13:10+00:00",
            temperature=4.1, humidity=63.0, precipitation=0.0,
            wind_direction=290.0, wind_speed=3.0, pressure=999.5,
            sunshine_duration=0.0, global_radiation=0.0,
        )
        assert observation_fingerprint(obs1) != observation_fingerprint(obs2)

    def test_null_fields_in_fingerprint(self):
        obs = WeatherObservation(
            station_id="11035", observation_time="2024-01-15T13:00+00:00",
            temperature=None, humidity=None, precipitation=None,
            wind_direction=None, wind_speed=None, pressure=None,
            sunshine_duration=None, global_radiation=None,
        )
        fp = observation_fingerprint(obs)
        assert isinstance(fp, str) and len(fp) == 32


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------


class TestStatePersistence:
    """Tests for load_state and save_state."""

    def test_load_missing_file(self, tmp_path):
        result = load_state(str(tmp_path / "nonexistent.json"))
        assert result == {}

    def test_save_and_load(self, tmp_path):
        path = str(tmp_path / "state.json")
        state = {"fingerprints": {"11035": "abc123"}}
        save_state(path, state)
        loaded = load_state(path)
        assert loaded == state

    def test_load_corrupt_file(self, tmp_path):
        path = str(tmp_path / "bad.json")
        with open(path, "w") as f:
            f.write("not json{{{")
        result = load_state(path)
        assert result == {}


# ---------------------------------------------------------------------------
# WeatherStation data class
# ---------------------------------------------------------------------------


class TestWeatherStationDataClass:
    """Tests for generated WeatherStation data class."""

    def test_to_json_roundtrip(self):
        station = WeatherStation(
            station_id="11035", station_name="WIEN HOHE WARTE",
            latitude=48.2486, longitude=16.3564, altitude=198.0, state="Wien",
        )
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == "11035"
        assert data["state"] == "Wien"

    def test_null_state_serialization(self):
        station = WeatherStation(
            station_id="99999", station_name="TEST",
            latitude=47.0, longitude=15.0, altitude=500.0, state=None,
        )
        json_str = station.to_json()
        data = json.loads(json_str)
        assert data["state"] is None


# ---------------------------------------------------------------------------
# WeatherObservation data class
# ---------------------------------------------------------------------------


class TestWeatherObservationDataClass:
    """Tests for generated WeatherObservation data class."""

    def test_to_json_roundtrip(self):
        obs = WeatherObservation(
            station_id="11035", observation_time="2024-01-15T13:00+00:00",
            temperature=3.9, humidity=64.0, precipitation=0.0,
            wind_direction=296.0, wind_speed=3.2, pressure=999.7,
            sunshine_duration=0.0, global_radiation=0.0,
        )
        json_str = obs.to_json()
        data = json.loads(json_str)
        assert data["station_id"] == "11035"
        assert data["temperature"] == 3.9

    def test_null_fields_serialization(self):
        obs = WeatherObservation(
            station_id="11035", observation_time="2024-01-15T13:00+00:00",
            temperature=None, humidity=None, precipitation=None,
            wind_direction=None, wind_speed=None, pressure=None,
            sunshine_duration=None, global_radiation=None,
        )
        json_str = obs.to_json()
        data = json.loads(json_str)
        assert data["temperature"] is None
        assert data["global_radiation"] is None


# ---------------------------------------------------------------------------
# Producer emission (mocked)
# ---------------------------------------------------------------------------


class FakeProducer:
    """Minimal fake confluent_kafka.Producer for testing."""

    def __init__(self):
        self.messages = []

    def produce(self, topic, key=None, value=None, headers=None):
        self.messages.append({"topic": topic, "key": key, "value": value, "headers": headers})

    def flush(self):
        pass


class TestSendStationEvents:
    """Tests for send_station_events."""

    def test_emits_all_stations(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        stations = [
            WeatherStation(station_id="11035", station_name="WIEN", latitude=48.0, longitude=16.0, altitude=200.0, state="Wien"),
            WeatherStation(station_id="11266", station_name="ACHENKIRCH", latitude=47.5, longitude=11.7, altitude=931.0, state="Tirol"),
        ]
        count = send_station_events(producer, stations)
        assert count == 2
        assert len(fake.messages) == 2

    def test_empty_stations(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        count = send_station_events(producer, [])
        assert count == 0

    def test_station_key_format(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        stations = [
            WeatherStation(station_id="11035", station_name="WIEN", latitude=48.0, longitude=16.0, altitude=200.0, state="Wien"),
        ]
        send_station_events(producer, stations)
        msg = fake.messages[0]
        assert msg["key"] == "11035"

    def test_station_cloudevent_type(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        stations = [
            WeatherStation(station_id="11035", station_name="WIEN", latitude=48.0, longitude=16.0, altitude=200.0, state="Wien"),
        ]
        send_station_events(producer, stations)
        value = json.loads(fake.messages[0]["value"])
        assert value["type"] == "at.geosphere.tawes.WeatherStation"
        assert value["subject"] == "11035"


class TestSendObservationEvents:
    """Tests for send_observation_events with dedup."""

    def _make_obs(self, station_id="11035", temp=3.9):
        return WeatherObservation(
            station_id=station_id, observation_time="2024-01-15T13:00+00:00",
            temperature=temp, humidity=64.0, precipitation=0.0,
            wind_direction=296.0, wind_speed=3.2, pressure=999.7,
            sunshine_duration=0.0, global_radiation=0.0,
        )

    def test_emits_new_observations(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        state = {}
        count = send_observation_events(producer, [self._make_obs()], state)
        assert count == 1
        assert len(fake.messages) == 1

    def test_dedup_skips_identical(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        state = {}
        send_observation_events(producer, [self._make_obs()], state)
        fake.messages.clear()
        count = send_observation_events(producer, [self._make_obs()], state)
        assert count == 0
        assert len(fake.messages) == 0

    def test_dedup_emits_changed(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        state = {}
        send_observation_events(producer, [self._make_obs(temp=3.9)], state)
        fake.messages.clear()
        count = send_observation_events(producer, [self._make_obs(temp=4.1)], state)
        assert count == 1

    def test_observation_key_format(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        state = {}
        send_observation_events(producer, [self._make_obs()], state)
        msg = fake.messages[0]
        assert msg["key"] == "11035"

    def test_observation_cloudevent_type(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        state = {}
        send_observation_events(producer, [self._make_obs()], state)
        value = json.loads(fake.messages[0]["value"])
        assert value["type"] == "at.geosphere.tawes.WeatherObservation"
        assert value["subject"] == "11035"

    def test_multiple_stations(self):
        fake = FakeProducer()
        producer = AtGeosphereTawesEventProducer(fake, "test-topic")
        state = {}
        obs = [self._make_obs("11035", 3.9), self._make_obs("11266", 0.2)]
        count = send_observation_events(producer, obs, state)
        assert count == 2


# Import for type access
from geosphere_austria_producer_kafka_producer.producer import AtGeosphereTawesEventProducer


# ---------------------------------------------------------------------------
# Fetch station metadata filtering
# ---------------------------------------------------------------------------


class TestFetchStationMetadata:
    """Tests for fetch_station_metadata (mocked HTTP)."""

    def test_filters_inactive_stations(self, requests_mock):
        requests_mock.get(
            "https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min/metadata",
            json=SAMPLE_METADATA_RESPONSE,
        )
        import requests as req
        session = req.Session()
        stations = fetch_station_metadata(session)
        assert len(stations) == 2
        ids = {s["id"] for s in stations}
        assert "11035" in ids
        assert "99999" in ids
        assert "99998" not in ids
