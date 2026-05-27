"""Unit tests for the transport-agnostic pegelonline core.

These tests exercise only the pure logic in :mod:`pegelonline_core` — the HTTP
client surface, connection-string parsing, and state I/O — with no Kafka or
MQTT producers in scope.
"""

import json
import os
import tempfile

import pytest

from pegelonline_core import (
    FEED_URL_ROOT,
    PegelOnlineAPI,
    load_state,
    save_state,
    parse_kafka_connection_string,
)


@pytest.mark.unit
class TestPegelOnlineAPIInitialization:
    def test_init_creates_empty_skip_urls(self):
        api = PegelOnlineAPI()
        assert api.skip_urls == []

    def test_init_creates_empty_etags(self):
        api = PegelOnlineAPI()
        assert api.etags == {}

    def test_feed_url_root_is_https_v2(self):
        assert FEED_URL_ROOT.startswith("https://")
        assert "/rest-api/v2" in FEED_URL_ROOT


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

    def test_parse_connection_string_without_sasl(self):
        cs = "Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic"
        result = parse_kafka_connection_string(cs)
        assert "sasl.username" not in result
        assert "security.protocol" not in result

    def test_parse_connection_string_strips_whitespace(self):
        cs = "  Endpoint=sb://test.servicebus.windows.net/;EntityPath=topic  "
        result = parse_kafka_connection_string(cs)
        assert result["bootstrap.servers"] == "test.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "topic"

    def test_parse_bootstrap_server_shape(self):
        cs = "BootstrapServer=broker:9092;EntityPath=mytopic"
        result = parse_kafka_connection_string(cs)
        assert result["bootstrap.servers"] == "broker:9092"
        assert result["kafka_topic"] == "mytopic"
        assert "security.protocol" not in result


@pytest.mark.unit
class TestStateIO:
    def test_roundtrip_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "state.json")
            payload = {"s1": {"timestamp": "2024-01-15T12:00:00+01:00", "value": 1}}
            save_state(path, payload)
            assert load_state(path) == payload

    def test_load_state_missing_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            assert load_state(os.path.join(tmp, "nope.json")) == {}
