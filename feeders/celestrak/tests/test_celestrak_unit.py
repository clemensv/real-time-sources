"""Unit tests for the transport-agnostic CelesTrak core.

These tests exercise only the pure logic in :mod:`celestrak_core` -- the
usage-policy state on the HTTP client, connection-string parsing, the
configuration model and state I/O -- with no Kafka, MQTT or AMQP producers in
scope.
"""

import os
import tempfile

import pytest

from celestrak_core import (
    GP_URL,
    SATCAT_URL,
    SUPGP_URL,
    CelesTrakAPI,
    FeedConfig,
    build_kafka_config,
    load_state,
    parse_kafka_connection_string,
    save_state,
)


@pytest.mark.unit
class TestCelesTrakAPIInitialization:
    def test_init_not_halted(self):
        api = CelesTrakAPI()
        assert api.halted is False

    def test_reset_halt_clears_flag(self):
        api = CelesTrakAPI()
        api.halted = True
        api.reset_halt()
        assert api.halted is False

    def test_endpoint_urls_are_https_celestrak(self):
        for url in (GP_URL, SATCAT_URL, SUPGP_URL):
            assert url.startswith("https://celestrak.org/")


@pytest.mark.unit
class TestConnectionStringParsing:
    def test_parse_event_hubs_connection_string(self):
        cs = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = parse_kafka_connection_string(cs)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myeventhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert cs.strip() in result["sasl.password"]
        assert result["security.protocol"] == "SASL_SSL"
        assert result["sasl.mechanism"] == "PLAIN"

    def test_parse_bootstrap_server_shape(self):
        cs = "BootstrapServer=broker:9092;EntityPath=mytopic"
        result = parse_kafka_connection_string(cs)
        assert result["bootstrap.servers"] == "broker:9092"
        assert result["kafka_topic"] == "mytopic"
        assert "security.protocol" not in result

    def test_parse_connection_string_without_sasl(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = parse_kafka_connection_string(cs)
        assert "sasl.username" not in result
        assert "security.protocol" not in result


@pytest.mark.unit
class TestBuildKafkaConfig:
    def test_with_credentials_uses_sasl_ssl(self):
        cfg = build_kafka_config(
            bootstrap_servers="broker:9093",
            sasl_username="user",
            sasl_password="secret",
        )
        assert cfg["security.protocol"] == "SASL_SSL"
        assert cfg["sasl.mechanisms"] == "PLAIN"
        assert cfg["sasl.username"] == "user"

    def test_with_credentials_tls_off_uses_sasl_plaintext(self):
        cfg = build_kafka_config(
            bootstrap_servers="broker:9092",
            sasl_username="user",
            sasl_password="secret",
            tls_enabled=False,
        )
        assert cfg["security.protocol"] == "SASL_PLAINTEXT"

    def test_without_credentials_tls_on_uses_ssl(self):
        cfg = build_kafka_config(bootstrap_servers="broker:9093")
        assert cfg["security.protocol"] == "SSL"
        assert "sasl.username" not in cfg


@pytest.mark.unit
class TestFeedConfigFromEnv:
    def test_defaults(self, monkeypatch):
        for var in ("CELESTRAK_GROUPS", "SUPGP_SOURCES", "POLLING_INTERVAL",
                    "REFERENCE_REFRESH_INTERVAL", "STATE_FILE", "ONCE_MODE"):
            monkeypatch.delenv(var, raising=False)
        cfg = FeedConfig.from_env()
        assert cfg.groups == ["stations"]
        assert cfg.supgp_sources == []
        assert cfg.polling_interval == 3600
        assert cfg.reference_refresh_interval == 86400
        assert cfg.once is False

    def test_env_overrides(self, monkeypatch):
        monkeypatch.setenv("CELESTRAK_GROUPS", "stations, active , weather")
        monkeypatch.setenv("SUPGP_SOURCES", "SpaceX-E,GLONASS")
        monkeypatch.setenv("POLLING_INTERVAL", "1800")
        monkeypatch.setenv("ONCE_MODE", "true")
        cfg = FeedConfig.from_env()
        assert cfg.groups == ["stations", "active", "weather"]
        assert cfg.supgp_sources == ["SpaceX-E", "GLONASS"]
        assert cfg.polling_interval == 1800
        assert cfg.once is True

    def test_explicit_kwargs_win_over_env(self, monkeypatch):
        monkeypatch.setenv("CELESTRAK_GROUPS", "weather")
        cfg = FeedConfig.from_env(groups=["gps-ops"], once=True)
        assert cfg.groups == ["gps-ops"]
        assert cfg.once is True


@pytest.mark.unit
class TestStateIO:
    def test_roundtrip_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "state.json")
            payload = {"gp": {"25544": "2026-07-16T12:00:00"}, "supgp": {}}
            save_state(path, payload)
            assert load_state(path) == payload

    def test_load_state_missing_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            assert load_state(os.path.join(tmp, "nope.json")) == {}
