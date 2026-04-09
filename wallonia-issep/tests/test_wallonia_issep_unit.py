"""Unit tests for the Wallonia ISSeP air quality bridge."""

from __future__ import annotations

import json
from argparse import Namespace
from unittest.mock import MagicMock

import pytest

from wallonia_issep.wallonia_issep import (
    WalloniaISsePAPI,
    _load_state,
    _save_state,
    _parse_bool,
    _safe_int,
    _safe_float,
)


# ---------------------------------------------------------------------------
# Sample API records
# ---------------------------------------------------------------------------

SAMPLE_RECORD = {
    "id_configuration": 10412,
    "moment": "2026-04-08T20:21:04+02:00",
    "co": 16,
    "no": 7,
    "no2": -1,
    "o3no2": -2,
    "ppbno": 2.711,
    "ppbno_statut": 100,
    "ppbno2": 0.985,
    "ppbno2_statut": 0,
    "ppbo3": 9.941,
    "ppbo3_statut": 0,
    "ugpcmno": 3.38,
    "ugpcmno_statut": 100,
    "ugpcmno2": 1.888,
    "ugpcmno2_statut": 0,
    "ugpcmo3": 19.965,
    "ugpcmo3_statut": 100,
    "bme_t": 21.3,
    "bme_t_statut": 100,
    "bme_pres": 101405,
    "bme_pres_statut": 100,
    "bme_rh": 38.97,
    "bme_rh_statut": 100,
    "pm1": 3.62,
    "pm1_statut": 100,
    "pm25": 1.957,
    "pm25_statut": 100,
    "pm4": 3.83,
    "pm4_statut": 100,
    "pm10": 5.148,
    "pm10_statut": 100,
    "vbat": 4.12,
    "vbat_statut": 100,
    "mwh_bat": -1.95,
    "mwh_pv": 1.56,
    "co_rf": 0.0,
    "no_rf": 0.0,
    "no2_rf": 0.0,
    "o3no2_rf": 0.0,
    "o3_rf": 0.0,
    "pm10_rf": 0.0,
}

SAMPLE_RECORD_NEGATIVE = {
    "id_configuration": 10296,
    "moment": "2026-04-08T20:16:42+02:00",
    "co": 201,
    "no": 48,
    "no2": -37,
    "o3no2": -84,
    "ppbno": 1.227,
    "ppbno_statut": 100,
    "ppbno2": 7.507,
    "ppbno2_statut": 100,
    "ppbo3": 26.464,
    "ppbo3_statut": 100,
    "ugpcmno": 1.53,
    "ugpcmno_statut": 100,
    "ugpcmno2": 14.383,
    "ugpcmno2_statut": 100,
    "ugpcmo3": 53.559,
    "ugpcmo3_statut": 100,
    "bme_t": 21.37,
    "bme_t_statut": 100,
    "bme_pres": 100546,
    "bme_pres_statut": 100,
    "bme_rh": 0.0,
    "bme_rh_statut": 0,
    "pm1": 4.69,
    "pm1_statut": 100,
    "pm25": 5.21,
    "pm25_statut": 100,
    "pm4": 5.42,
    "pm4_statut": 100,
    "pm10": 5.52,
    "pm10_statut": 100,
    "vbat": 4.11,
    "vbat_statut": 100,
    "mwh_bat": -1.74,
    "mwh_pv": 5.47,
    "co_rf": 0.0,
    "no_rf": 0.39666666666666667,
    "no2_rf": 13.087666666666669,
    "o3no2_rf": 88.32800000000002,
    "o3_rf": 75.24033333333335,
    "pm10_rf": 17.13766666666666,
    "vbat_statut": 100,
}


class FakeResponse:
    """Simple fake requests response."""

    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload

    def raise_for_status(self):
        return None


# ---------------------------------------------------------------------------
# API initialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_api_initialization():
    api = WalloniaISsePAPI()
    assert api.base_url == WalloniaISsePAPI.BASE_URL
    assert api.timeout == 30
    assert api.page_limit == 100
    assert api.reference_refresh_interval == 86400
    assert api.session is not None


@pytest.mark.unit
def test_api_custom_initialization():
    api = WalloniaISsePAPI(base_url="https://example.com/api/", timeout=60, page_limit=50)
    assert api.base_url == "https://example.com/api"
    assert api.timeout == 60
    assert api.page_limit == 50


# ---------------------------------------------------------------------------
# Connection string parsing
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_parse_connection_string_event_hubs():
    config, topic = WalloniaISsePAPI.parse_connection_string(
        "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;"
        "SharedAccessKey=secret;EntityPath=wallonia-issep"
    )
    assert config["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
    assert config["security.protocol"] == "SASL_SSL"
    assert config["sasl.mechanisms"] == "PLAIN"
    assert config["sasl.username"] == "$ConnectionString"
    assert "EntityPath=wallonia-issep" in config["sasl.password"]
    assert topic == "wallonia-issep"


@pytest.mark.unit
def test_parse_connection_string_bootstrap_server():
    config, topic = WalloniaISsePAPI.parse_connection_string(
        "BootstrapServer=localhost:9092;EntityPath=wallonia-issep"
    )
    assert config == {"bootstrap.servers": "localhost:9092"}
    assert topic == "wallonia-issep"


@pytest.mark.unit
def test_parse_connection_string_empty():
    config, topic = WalloniaISsePAPI.parse_connection_string("")
    assert config == {}
    assert topic is None


@pytest.mark.unit
def test_parse_connection_string_unsupported():
    with pytest.raises(ValueError, match="Unsupported"):
        WalloniaISsePAPI.parse_connection_string("SomeKey=SomeValue")


@pytest.mark.unit
def test_parse_connection_string_invalid_format():
    with pytest.raises(ValueError, match="Invalid"):
        WalloniaISsePAPI.parse_connection_string("no-equals-sign")


@pytest.mark.unit
def test_parse_connection_string_event_hubs_no_entity_path():
    config, topic = WalloniaISsePAPI.parse_connection_string(
        "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=secret"
    )
    assert config["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
    assert topic is None


# ---------------------------------------------------------------------------
# Observation parsing
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_normalize_observation_full_record():
    api = WalloniaISsePAPI()
    obs = api.normalize_observation(SAMPLE_RECORD)
    assert obs.configuration_id == "10412"
    assert obs.moment == "2026-04-08T20:21:04+02:00"
    assert obs.co == 16
    assert obs.no == 7
    assert obs.no2 == -1
    assert obs.o3no2 == -2
    assert obs.ppbno == 2.711
    assert obs.ppbno_statut == 100
    assert obs.ppbno2 == 0.985
    assert obs.ppbno2_statut == 0
    assert obs.ppbo3 == 9.941
    assert obs.ppbo3_statut == 0
    assert obs.bme_t == 21.3
    assert obs.bme_pres == 101405
    assert obs.bme_rh == 38.97
    assert obs.pm1 == 3.62
    assert obs.pm25 == 1.957
    assert obs.pm4 == 3.83
    assert obs.pm10 == 5.148
    assert obs.vbat == 4.12
    assert obs.mwh_bat == -1.95
    assert obs.mwh_pv == 1.56
    assert obs.co_rf == 0.0
    assert obs.pm10_rf == 0.0


@pytest.mark.unit
def test_normalize_observation_negative_values():
    """Negative raw values (e.g. no2=-37) are valid sensor readings."""
    api = WalloniaISsePAPI()
    obs = api.normalize_observation(SAMPLE_RECORD_NEGATIVE)
    assert obs.configuration_id == "10296"
    assert obs.no2 == -37
    assert obs.o3no2 == -84
    assert obs.mwh_bat == -1.74


@pytest.mark.unit
def test_normalize_observation_null_fields():
    """Missing fields should result in None."""
    api = WalloniaISsePAPI()
    minimal_record = {
        "id_configuration": 99999,
        "moment": "2026-04-08T10:00:00+02:00",
    }
    obs = api.normalize_observation(minimal_record)
    assert obs.configuration_id == "99999"
    assert obs.moment == "2026-04-08T10:00:00+02:00"
    assert obs.co is None
    assert obs.no is None
    assert obs.no2 is None
    assert obs.o3no2 is None
    assert obs.ppbno is None
    assert obs.ppbno_statut is None
    assert obs.bme_t is None
    assert obs.bme_pres is None
    assert obs.pm1 is None
    assert obs.pm25 is None
    assert obs.pm10 is None
    assert obs.vbat is None
    assert obs.mwh_bat is None
    assert obs.co_rf is None
    assert obs.o3_rf is None
    assert obs.pm10_rf is None


@pytest.mark.unit
def test_normalize_observation_config_id_as_string():
    """The configuration_id should always be a string."""
    api = WalloniaISsePAPI()
    obs = api.normalize_observation(SAMPLE_RECORD)
    assert isinstance(obs.configuration_id, str)
    assert obs.configuration_id == "10412"


@pytest.mark.unit
def test_normalize_observation_zero_humidity():
    """Zero humidity is valid, not None."""
    api = WalloniaISsePAPI()
    obs = api.normalize_observation(SAMPLE_RECORD_NEGATIVE)
    assert obs.bme_rh == 0.0
    assert obs.bme_rh_statut == 0


# ---------------------------------------------------------------------------
# Serialization roundtrips
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_observation_serialization_roundtrip():
    api = WalloniaISsePAPI()
    obs = api.normalize_observation(SAMPLE_RECORD)
    serialized = obs.to_serializer_dict()
    assert serialized["configuration_id"] == "10412"
    assert serialized["moment"] == "2026-04-08T20:21:04+02:00"
    assert serialized["no2"] == -1
    assert serialized["pm25"] == 1.957
    from wallonia_issep_producer_data import Observation
    restored = Observation.from_serializer_dict(serialized)
    assert restored.configuration_id == obs.configuration_id
    assert restored.moment == obs.moment
    assert restored.co == obs.co
    assert restored.no2 == obs.no2


@pytest.mark.unit
def test_observation_json_roundtrip():
    api = WalloniaISsePAPI()
    obs = api.normalize_observation(SAMPLE_RECORD)
    json_str = obs.to_json()  # type: ignore[attr-defined]
    from wallonia_issep_producer_data import Observation
    restored = Observation.from_json(json_str)  # type: ignore[attr-defined]
    assert restored.configuration_id == "10412"
    assert restored.no2 == -1
    assert restored.ppbno == 2.711


@pytest.mark.unit
def test_sensor_configuration_serialization():
    from wallonia_issep_producer_data import SensorConfiguration
    config = SensorConfiguration(configuration_id="10412")
    serialized = config.to_serializer_dict()
    assert serialized == {"configuration_id": "10412"}
    restored = SensorConfiguration.from_serializer_dict(serialized)
    assert restored.configuration_id == "10412"


@pytest.mark.unit
def test_sensor_configuration_json_roundtrip():
    from wallonia_issep_producer_data import SensorConfiguration
    config = SensorConfiguration(configuration_id="10296")
    json_str = config.to_json()  # type: ignore[attr-defined]
    restored = SensorConfiguration.from_json(json_str)  # type: ignore[attr-defined]
    assert restored.configuration_id == "10296"


@pytest.mark.unit
def test_observation_byte_array_roundtrip():
    api = WalloniaISsePAPI()
    obs = api.normalize_observation(SAMPLE_RECORD)
    byte_arr = obs.to_byte_array("application/json")
    from wallonia_issep_producer_data import Observation
    restored = Observation.from_data(byte_arr, "application/json")
    assert restored is not None
    assert restored.configuration_id == "10412"
    assert restored.no2 == -1


@pytest.mark.unit
def test_observation_null_fields_in_json():
    """Null fields should serialize and deserialize as None."""
    api = WalloniaISsePAPI()
    minimal = {"id_configuration": 1, "moment": "2026-01-01T00:00:00+00:00"}
    obs = api.normalize_observation(minimal)
    json_str = obs.to_json()  # type: ignore[attr-defined]
    parsed = json.loads(json_str)
    assert parsed["co"] is None
    assert parsed["pm10"] is None
    assert parsed["vbat"] is None


# ---------------------------------------------------------------------------
# Sensor configuration extraction
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_extract_configurations():
    records = [
        {"id_configuration": 10412, "moment": "2026-04-08T20:21:04+02:00"},
        {"id_configuration": 10296, "moment": "2026-04-08T20:16:42+02:00"},
        {"id_configuration": 10412, "moment": "2026-04-08T20:31:04+02:00"},  # duplicate
    ]
    configs = WalloniaISsePAPI.extract_configurations(records)
    assert len(configs) == 2
    ids = {c.configuration_id for c in configs}
    assert ids == {"10412", "10296"}


@pytest.mark.unit
def test_extract_configurations_empty():
    configs = WalloniaISsePAPI.extract_configurations([])
    assert configs == []


@pytest.mark.unit
def test_extract_configurations_preserves_order():
    records = [
        {"id_configuration": 30000, "moment": "2026-01-01T00:00:00+00:00"},
        {"id_configuration": 10000, "moment": "2026-01-01T00:00:00+00:00"},
        {"id_configuration": 20000, "moment": "2026-01-01T00:00:00+00:00"},
    ]
    configs = WalloniaISsePAPI.extract_configurations(records)
    assert [c.configuration_id for c in configs] == ["30000", "10000", "20000"]


# ---------------------------------------------------------------------------
# Deduplication logic
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_filter_new_records_all_new():
    state: Dict = {}
    records = [
        {"id_configuration": 10412, "moment": "2026-04-08T20:21:04+02:00"},
        {"id_configuration": 10296, "moment": "2026-04-08T20:16:42+02:00"},
    ]
    new = WalloniaISsePAPI.filter_new_records(records, state)
    assert len(new) == 2
    assert state["10412"] == "2026-04-08T20:21:04+02:00"
    assert state["10296"] == "2026-04-08T20:16:42+02:00"


@pytest.mark.unit
def test_filter_new_records_dedup_older():
    state = {"10412": "2026-04-08T20:21:04+02:00"}
    records = [
        {"id_configuration": 10412, "moment": "2026-04-08T20:21:04+02:00"},  # same
        {"id_configuration": 10412, "moment": "2026-04-08T20:10:00+02:00"},  # older
        {"id_configuration": 10412, "moment": "2026-04-08T20:31:04+02:00"},  # newer
    ]
    new = WalloniaISsePAPI.filter_new_records(records, state)
    assert len(new) == 1
    assert new[0]["moment"] == "2026-04-08T20:31:04+02:00"
    assert state["10412"] == "2026-04-08T20:31:04+02:00"


@pytest.mark.unit
def test_filter_new_records_empty_state():
    state: Dict = {}
    records = [
        {"id_configuration": 10412, "moment": "2026-04-08T20:21:04+02:00"},
    ]
    new = WalloniaISsePAPI.filter_new_records(records, state)
    assert len(new) == 1


@pytest.mark.unit
def test_filter_new_records_skips_missing_config():
    state: Dict = {}
    records = [
        {"moment": "2026-04-08T20:21:04+02:00"},  # missing id_configuration
    ]
    new = WalloniaISsePAPI.filter_new_records(records, state)
    assert len(new) == 0


@pytest.mark.unit
def test_filter_new_records_skips_missing_moment():
    state: Dict = {}
    records = [
        {"id_configuration": 10412},  # missing moment
    ]
    new = WalloniaISsePAPI.filter_new_records(records, state)
    assert len(new) == 0


@pytest.mark.unit
def test_filter_new_records_state_not_advanced_for_older():
    state = {"10412": "2026-04-08T22:00:00+02:00"}
    records = [
        {"id_configuration": 10412, "moment": "2026-04-08T20:00:00+02:00"},
    ]
    new = WalloniaISsePAPI.filter_new_records(records, state)
    assert len(new) == 0
    assert state["10412"] == "2026-04-08T22:00:00+02:00"


@pytest.mark.unit
def test_filter_new_records_multiple_configs():
    state: Dict = {}
    records = [
        {"id_configuration": 10412, "moment": "2026-04-08T20:00:00+02:00"},
        {"id_configuration": 10296, "moment": "2026-04-08T20:05:00+02:00"},
        {"id_configuration": 10412, "moment": "2026-04-08T20:10:00+02:00"},
    ]
    new = WalloniaISsePAPI.filter_new_records(records, state)
    assert len(new) == 3
    assert state["10412"] == "2026-04-08T20:10:00+02:00"
    assert state["10296"] == "2026-04-08T20:05:00+02:00"


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_pagination_single_page():
    session = MagicMock()
    session.get.return_value = FakeResponse({
        "total_count": 3,
        "results": [
            {"id_configuration": 1, "moment": "2026-01-01T00:00:00+00:00"},
            {"id_configuration": 2, "moment": "2026-01-01T00:00:00+00:00"},
            {"id_configuration": 3, "moment": "2026-01-01T00:00:00+00:00"},
        ],
    })
    api = WalloniaISsePAPI(session=session, page_limit=100)
    records = api.fetch_all_records()
    assert len(records) == 3
    assert session.get.call_count == 1


@pytest.mark.unit
def test_pagination_multiple_pages():
    session = MagicMock()
    session.get.side_effect = [
        FakeResponse({
            "total_count": 5,
            "results": [{"id_configuration": i, "moment": "2026-01-01T00:00:00+00:00"} for i in range(3)],
        }),
        FakeResponse({
            "total_count": 5,
            "results": [{"id_configuration": i, "moment": "2026-01-01T00:00:00+00:00"} for i in range(3, 5)],
        }),
    ]
    api = WalloniaISsePAPI(session=session, page_limit=3)
    records = api.fetch_all_records()
    assert len(records) == 5
    assert session.get.call_count == 2
    first_call = session.get.call_args_list[0]
    assert first_call.kwargs["params"]["offset"] == 0
    second_call = session.get.call_args_list[1]
    assert second_call.kwargs["params"]["offset"] == 3


@pytest.mark.unit
def test_pagination_empty_results():
    session = MagicMock()
    session.get.return_value = FakeResponse({"total_count": 0, "results": []})
    api = WalloniaISsePAPI(session=session)
    records = api.fetch_all_records()
    assert records == []


# ---------------------------------------------------------------------------
# Kafka config building
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_build_kafka_config_plaintext():
    args = Namespace(
        connection_string=None,
        kafka_bootstrap_servers="localhost:9092",
        kafka_topic="wallonia-issep",
        sasl_username=None,
        sasl_password=None,
        kafka_enable_tls="false",
    )
    config, topic = WalloniaISsePAPI.build_kafka_config(args)
    assert config["bootstrap.servers"] == "localhost:9092"
    assert config["security.protocol"] == "PLAINTEXT"
    assert topic == "wallonia-issep"


@pytest.mark.unit
def test_build_kafka_config_connection_string():
    args = Namespace(
        connection_string="BootstrapServer=broker:9092;EntityPath=my-topic",
        kafka_bootstrap_servers=None,
        kafka_topic=None,
        sasl_username=None,
        sasl_password=None,
        kafka_enable_tls="true",
    )
    config, topic = WalloniaISsePAPI.build_kafka_config(args)
    assert config["bootstrap.servers"] == "broker:9092"
    assert topic == "my-topic"


@pytest.mark.unit
def test_build_kafka_config_sasl():
    args = Namespace(
        connection_string=None,
        kafka_bootstrap_servers="broker:9092",
        kafka_topic="wallonia-issep",
        sasl_username="user",
        sasl_password="pass",
        kafka_enable_tls="true",
    )
    config, topic = WalloniaISsePAPI.build_kafka_config(args)
    assert config["sasl.username"] == "user"
    assert config["sasl.password"] == "pass"
    assert config["security.protocol"] == "SASL_SSL"


@pytest.mark.unit
def test_build_kafka_config_no_bootstrap_raises():
    args = Namespace(
        connection_string=None,
        kafka_bootstrap_servers=None,
        kafka_topic=None,
        sasl_username=None,
        sasl_password=None,
        kafka_enable_tls="true",
    )
    with pytest.raises(ValueError, match="bootstrap servers"):
        WalloniaISsePAPI.build_kafka_config(args)


@pytest.mark.unit
def test_build_kafka_config_default_topic():
    args = Namespace(
        connection_string=None,
        kafka_bootstrap_servers="broker:9092",
        kafka_topic=None,
        sasl_username=None,
        sasl_password=None,
        kafka_enable_tls="false",
    )
    _, topic = WalloniaISsePAPI.build_kafka_config(args)
    assert topic == "wallonia-issep"


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_load_state_missing_file():
    state = _load_state("/nonexistent/path/state.json")
    assert state == {}


@pytest.mark.unit
def test_load_state_empty_path():
    state = _load_state("")
    assert state == {}


@pytest.mark.unit
def test_save_and_load_state(tmp_path):
    state_file = str(tmp_path / "state.json")
    original = {"10412": "2026-04-08T20:21:04+02:00", "10296": "2026-04-08T20:16:42+02:00"}
    _save_state(state_file, original)
    loaded = _load_state(state_file)
    assert loaded == original


@pytest.mark.unit
def test_save_state_empty_path():
    # Should not raise
    _save_state("", {"key": "value"})


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_parse_bool_true():
    assert _parse_bool(True) is True
    assert _parse_bool("true") is True
    assert _parse_bool("True") is True
    assert _parse_bool("1") is True
    assert _parse_bool("yes") is True


@pytest.mark.unit
def test_parse_bool_false():
    assert _parse_bool(False) is False
    assert _parse_bool("false") is False
    assert _parse_bool("0") is False
    assert _parse_bool("no") is False
    assert _parse_bool("off") is False
    assert _parse_bool("") is False


@pytest.mark.unit
def test_safe_int():
    assert _safe_int(42) == 42
    assert _safe_int("42") == 42
    assert _safe_int(None) is None
    assert _safe_int("abc") is None
    assert _safe_int(-37) == -37
    assert _safe_int(0) == 0


@pytest.mark.unit
def test_safe_float():
    assert _safe_float(3.14) == 3.14
    assert _safe_float("3.14") == 3.14
    assert _safe_float(None) is None
    assert _safe_float("abc") is None
    assert _safe_float(-1.95) == -1.95
    assert _safe_float(0) == 0.0


@pytest.mark.unit
def test_safe_int_from_float():
    assert _safe_int(42.0) == 42
    assert _safe_int(42.7) == 42


@pytest.mark.unit
def test_safe_float_from_int():
    assert _safe_float(42) == 42.0


# ---------------------------------------------------------------------------
# Integration-level: emit_reference_data
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_emit_reference_data_calls_producer():
    api = WalloniaISsePAPI()
    mock_producer = MagicMock()
    mock_producer.producer = MagicMock()
    records = [
        {"id_configuration": 10412, "moment": "2026-04-08T20:21:04+02:00"},
        {"id_configuration": 10296, "moment": "2026-04-08T20:16:42+02:00"},
    ]
    configs = api.emit_reference_data(mock_producer, records)
    assert len(configs) == 2
    assert mock_producer.send_be_issep_airquality_sensor_configuration.call_count == 2
    mock_producer.producer.flush.assert_called_once()


@pytest.mark.unit
def test_emit_reference_data_passes_correct_args():
    api = WalloniaISsePAPI()
    mock_producer = MagicMock()
    mock_producer.producer = MagicMock()
    records = [{"id_configuration": 10412, "moment": "2026-04-08T20:21:04+02:00"}]
    api.emit_reference_data(mock_producer, records)
    call_kwargs = mock_producer.send_be_issep_airquality_sensor_configuration.call_args.kwargs
    assert call_kwargs["_configuration_id"] == "10412"
    assert call_kwargs["flush_producer"] is False


# ---------------------------------------------------------------------------
# Integration-level: poll_observations
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_poll_observations_emits_new():
    session = MagicMock()
    session.get.return_value = FakeResponse({
        "total_count": 1,
        "results": [SAMPLE_RECORD],
    })
    api = WalloniaISsePAPI(session=session)
    mock_producer = MagicMock()
    mock_producer.producer = MagicMock()
    state: Dict = {}

    count, all_records = api.poll_observations(producer=mock_producer, state=state)
    assert count == 1
    assert len(all_records) == 1
    assert mock_producer.send_be_issep_airquality_observation.call_count == 1
    call_kwargs = mock_producer.send_be_issep_airquality_observation.call_args.kwargs
    assert call_kwargs["_configuration_id"] == "10412"
    assert call_kwargs["flush_producer"] is False


@pytest.mark.unit
def test_poll_observations_dedup():
    session = MagicMock()
    session.get.return_value = FakeResponse({
        "total_count": 1,
        "results": [SAMPLE_RECORD],
    })
    api = WalloniaISsePAPI(session=session)
    mock_producer = MagicMock()
    mock_producer.producer = MagicMock()
    state = {"10412": "2026-04-08T20:21:04+02:00"}

    count, _ = api.poll_observations(producer=mock_producer, state=state)
    assert count == 0
    mock_producer.send_be_issep_airquality_observation.assert_not_called()


# Type alias for Dict used in tests
from typing import Dict
