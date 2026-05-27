"""Unit tests for the Luchtmeetnet Netherlands bridge."""

import json
from pathlib import Path

import pytest

from luchtmeetnet_nl.luchtmeetnet_nl import (
    LuchtmeetnetAPI,
    _build_kafka_config,
    _load_state,
    _save_state,
)


@pytest.mark.unit
class TestLuchtmeetnetInitialization:
    def test_init_creates_session(self):
        api = LuchtmeetnetAPI()
        assert api.base_url == "https://api.luchtmeetnet.nl/open_api"
        assert api.session is not None
        assert hasattr(api.session, "get")


@pytest.mark.unit
class TestConnectionStringParsing:
    def test_parse_event_hubs_connection_string(self):
        api = LuchtmeetnetAPI()
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )

        result = api.parse_connection_string(connection_string)

        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myeventhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == connection_string
        assert result["security.protocol"] == "SASL_SSL"

    def test_parse_plain_bootstrap_connection_string(self):
        api = LuchtmeetnetAPI()

        result = api.parse_connection_string("BootstrapServer=localhost:9092;EntityPath=luchtmeetnet-nl")

        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "luchtmeetnet-nl"
        assert "sasl.username" not in result

    def test_invalid_connection_string_raises(self):
        api = LuchtmeetnetAPI()
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string("BrokenConnectionString")


@pytest.mark.unit
class TestStateHandling:
    def test_load_missing_state_returns_empty_dict(self, tmp_path: Path):
        assert _load_state(str(tmp_path / "missing.json")) == {}

    def test_save_and_load_state_roundtrip(self, tmp_path: Path):
        state_file = tmp_path / "state.json"
        state = {"measurement:NL01491:NO2": "2026-04-08T10:00:00+00:00"}

        _save_state(str(state_file), state)

        assert json.loads(state_file.read_text(encoding="utf-8")) == state
        assert _load_state(str(state_file)) == state


@pytest.mark.unit
class TestKafkaConfig:
    def test_build_kafka_config_with_tls_only(self):
        config = _build_kafka_config("localhost:9093", None, None, True)
        assert config == {
            "bootstrap.servers": "localhost:9093",
            "security.protocol": "SSL",
        }

    def test_build_kafka_config_with_sasl_plaintext(self):
        config = _build_kafka_config("localhost:9092", "$ConnectionString", "secret", False)
        assert config["security.protocol"] == "SASL_PLAINTEXT"
        assert config["sasl.mechanisms"] == "PLAIN"
