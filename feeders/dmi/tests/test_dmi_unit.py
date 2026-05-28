"""Unit tests for the DMI feeder normalizers, config, and pagination."""

from __future__ import annotations

import os
from typing import Any, Dict
from unittest import mock

import pytest

from dmi_core.acquisition import (
    DmiLightningAPI,
    DmiMetObsAPI,
    DmiOceanObsAPI,
    _feature_properties,
)
from dmi_core.config import (
    DmiApiKeys,
    FeedConfig,
    build_kafka_config,
    parse_kafka_connection_string,
)

from dmi_kafka.app import (
    _build_lightning_sensor,
    _build_lightning_strike,
    _build_met_observation,
    _build_met_station,
    _build_ocean_observation,
    _build_ocean_station,
    _build_tidewater_prediction,
    _build_tidewater_station,
)
from dmi_amqp.app import _parse_broker_url


# ---------------------------------------------------------------------------
# _feature_properties
# ---------------------------------------------------------------------------


def test_feature_properties_merges_id_and_coords():
    feature: Dict[str, Any] = {
        "id": "06180",
        "properties": {"stationId": "06180", "name": "Roskilde"},
        "geometry": {"type": "Point", "coordinates": [12.32, 55.65]},
    }
    out = _feature_properties(feature)
    assert out["stationId"] == "06180"
    assert out["id"] == "06180"
    assert out["longitude"] == 12.32
    assert out["latitude"] == 55.65


def test_feature_properties_does_not_override_existing_lat_lon():
    feature = {
        "properties": {"latitude": 99.0, "longitude": 88.0},
        "geometry": {"coordinates": [1.0, 2.0]},
    }
    out = _feature_properties(feature)
    assert out["latitude"] == 99.0
    assert out["longitude"] == 88.0


def test_feature_properties_missing_geometry_safe():
    feature = {"properties": {"a": 1}}
    out = _feature_properties(feature)
    assert out == {"a": 1}


# ---------------------------------------------------------------------------
# DmiApiKeys.from_env
# ---------------------------------------------------------------------------


def test_dmi_api_keys_picks_specific_envs(monkeypatch):
    monkeypatch.setenv("DMI_API_KEY", "fallback")
    monkeypatch.setenv("DMI_METOBS_API_KEY", "m")
    monkeypatch.setenv("DMI_OCEANOBS_API_KEY", "o")
    monkeypatch.setenv("DMI_LIGHTNING_API_KEY", "l")
    keys = DmiApiKeys.from_env()
    assert keys.met_obs == "m"
    assert keys.ocean_obs == "o"
    assert keys.lightning == "l"


def test_dmi_api_keys_falls_back(monkeypatch):
    monkeypatch.delenv("DMI_METOBS_API_KEY", raising=False)
    monkeypatch.delenv("DMI_OCEANOBS_API_KEY", raising=False)
    monkeypatch.delenv("DMI_LIGHTNING_API_KEY", raising=False)
    monkeypatch.setenv("DMI_API_KEY", "k")
    keys = DmiApiKeys.from_env()
    assert keys.met_obs == "k"
    assert keys.ocean_obs == "k"
    assert keys.lightning == "k"


# ---------------------------------------------------------------------------
# FeedConfig.from_env
# ---------------------------------------------------------------------------


def test_feed_config_defaults(monkeypatch):
    monkeypatch.delenv("POLLING_INTERVAL", raising=False)
    monkeypatch.delenv("ONCE_MODE", raising=False)
    cfg = FeedConfig.from_env()
    assert cfg.polling_interval == 300
    assert cfg.once is False


def test_feed_config_env_overrides(monkeypatch):
    monkeypatch.setenv("POLLING_INTERVAL", "42")
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setenv("STATE_FILE", "/tmp/x.json")
    cfg = FeedConfig.from_env()
    assert cfg.polling_interval == 42
    assert cfg.state_file == "/tmp/x.json"
    assert cfg.once is True


# ---------------------------------------------------------------------------
# parse_kafka_connection_string
# ---------------------------------------------------------------------------


def test_parse_event_hubs_connection_string():
    cs = (
        "Endpoint=sb://ns.servicebus.windows.net/;"
        "SharedAccessKeyName=root;"
        "SharedAccessKey=abc;"
        "EntityPath=dmi"
    )
    cfg = parse_kafka_connection_string(cs)
    assert cfg["bootstrap.servers"] == "ns.servicebus.windows.net:9093"
    assert cfg["kafka_topic"] == "dmi"
    assert cfg["sasl.username"] == "$ConnectionString"
    assert cfg["sasl.password"] == cs
    assert cfg["security.protocol"] == "SASL_SSL"
    assert cfg["sasl.mechanism"] == "PLAIN"


def test_parse_harness_bootstrap_form():
    cs = "BootstrapServer=localhost:9092;EntityPath=dmi"
    cfg = parse_kafka_connection_string(cs)
    assert cfg["bootstrap.servers"] == "localhost:9092"
    assert cfg["kafka_topic"] == "dmi"
    assert "sasl.username" not in cfg


def test_build_kafka_config_sasl_vs_plain():
    sasl = build_kafka_config(
        bootstrap_servers="b:9093",
        sasl_username="u",
        sasl_password="p",
        tls_enabled=True,
    )
    assert sasl["security.protocol"] == "SASL_SSL"
    plain_tls = build_kafka_config(bootstrap_servers="b:9092", tls_enabled=True)
    assert plain_tls["security.protocol"] == "SSL"
    plain = build_kafka_config(bootstrap_servers="b:9092", tls_enabled=False)
    assert "security.protocol" not in plain


def test_parse_amqp_broker_url_defaults():
    host, port, tls, user, pwd, path = _parse_broker_url("broker.example.com")
    assert host == "broker.example.com"
    assert port == 5672
    assert tls is False
    assert user is None
    assert pwd is None
    assert path is None


def test_parse_amqp_broker_url_with_auth_and_path():
    host, port, tls, user, pwd, path = _parse_broker_url(
        "amqps://alice:secret@broker.example.com:5671/dmi"
    )
    assert host == "broker.example.com"
    assert port == 5671
    assert tls is True
    assert user == "alice"
    assert pwd == "secret"
    assert path == "dmi"


# ---------------------------------------------------------------------------
# Builders (normalizers)
# ---------------------------------------------------------------------------


def test_build_met_station_minimal():
    raw = {
        "stationId": "06180",
        "name": "Roskilde",
        "country": "DNK",
        "type": "Synop",
        "parameterId": ["temp_dry", "wind_speed"],
        "latitude": 55.65,
        "longitude": 12.32,
        "validFrom": "2020-01-01T00:00:00Z",
    }
    s = _build_met_station(raw)
    assert s.station_id == "06180"
    assert s.name == "Roskilde"
    assert s.parameter_id == ["temp_dry", "wind_speed"]
    assert s.latitude == 55.65
    assert s.valid_from == "2020-01-01T00:00:00Z"


def test_build_met_observation():
    raw = {
        "id": "abc",
        "stationId": "06180",
        "parameterId": "temp_dry",
        "observed": "2025-01-01T10:00:00Z",
        "value": 1.5,
    }
    o = _build_met_observation(raw)
    assert o.station_id == "06180"
    assert o.parameter_id == "temp_dry"
    assert o.value == 1.5


def test_build_ocean_station_and_observation():
    s = _build_ocean_station({"stationId": "9999", "name": "Hornbaek", "country": "DNK",
                              "latitude": 56.1, "longitude": 12.5,
                              "parameterId": ["sea_reg"]})
    assert s.station_id == "9999"
    assert s.parameter_id == ["sea_reg"]
    o = _build_ocean_observation({"stationId": "9999", "parameterId": "sea_reg",
                                  "observed": "2025-01-01T00:00:00Z", "value": 12.3})
    assert o.value == 12.3


def test_build_tidewater_station_and_prediction():
    s = _build_tidewater_station({"stationId": "T1", "name": "Esbjerg",
                                  "country": "DNK", "latitude": 55.5, "longitude": 8.4})
    assert s.station_id == "T1"
    p = _build_tidewater_prediction({"stationId": "T1", "predictionType": "harmonic",
                                     "predictionTime": "2025-01-01T01:00:00Z",
                                     "value": 0.85})
    assert p.station_id == "T1"
    assert p.prediction_type == "harmonic"
    assert p.value == 0.85


def test_build_lightning_sensor():
    raw = {"sensorId": "DK_BOR", "name": "Bornholm", "country": "DNK",
           "latitude": 55.1, "longitude": 14.9}
    s = _build_lightning_sensor(raw)
    assert s.sensor_id == "DK_BOR"
    assert s.country == "DNK"


def test_build_lightning_strike_sensors_is_string():
    raw = {
        "id": "S1",
        "observed": "2025-01-01T00:00:00Z",
        "type": 1,
        "amp": -12.4,
        "strokes": 2,
        "sensors": "DK_BOR,DK_CPH,DE_HAM",
        "latitude": 55.0,
        "longitude": 12.0,
    }
    st = _build_lightning_strike(raw)
    assert st.strike_id == "S1"
    assert st.type == 1
    assert st.sensors == "DK_BOR,DK_CPH,DE_HAM"


def test_build_lightning_strike_sensors_from_list():
    """If upstream ever returns sensors as a list, normalize to CSV."""
    raw = {"id": "S2", "observed": "2025-01-01T00:00:00Z",
           "type": 0, "sensors": ["DK_BOR", "DK_CPH"],
           "latitude": 0.0, "longitude": 0.0}
    st = _build_lightning_strike(raw)
    assert st.sensors == "DK_BOR,DK_CPH"


def test_build_lightning_strike_sensors_none():
    raw = {"id": "S3", "observed": "2025-01-01T00:00:00Z",
           "type": 0, "latitude": 0.0, "longitude": 0.0}
    st = _build_lightning_strike(raw)
    assert st.sensors is None


# ---------------------------------------------------------------------------
# API clients require key
# ---------------------------------------------------------------------------


def test_clients_require_api_key():
    for cls in (DmiMetObsAPI, DmiOceanObsAPI, DmiLightningAPI):
        with pytest.raises(ValueError):
            cls(api_key="")


def test_pagination_stops_on_short_page():
    api = DmiMetObsAPI(api_key="k")
    page1 = {"features": [{"id": str(i), "properties": {"i": i}} for i in range(1000)]}
    page2 = {"features": [{"id": "x", "properties": {"i": 1000}}]}
    with mock.patch.object(api, "_get", side_effect=[page1, page2]) as m:
        out = list(api._iter_collection("station"))
    assert len(out) == 1001
    assert m.call_count == 2
    # second page should be requested with offset=1000
    args, kwargs = m.call_args_list[1]
    assert kwargs["params"]["offset"] == 1000


def test_pagination_stops_on_empty_page():
    api = DmiMetObsAPI(api_key="k")
    with mock.patch.object(api, "_get", return_value={"features": []}):
        assert list(api._iter_collection("station")) == []
