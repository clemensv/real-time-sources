"""Unit tests for the IRCELINE Belgium bridge."""

from __future__ import annotations

from argparse import Namespace
from unittest.mock import MagicMock

import pytest

from irceline_belgium.irceline_belgium import IrcelineBelgiumAPI


class FakeResponse:
    """Simple fake requests response."""

    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload

    def raise_for_status(self):
        return None


@pytest.mark.unit
def test_api_initialization():
    api = IrcelineBelgiumAPI()

    assert api.base_url == "https://geo.irceline.be/sos/api/v1"
    assert api.timeout == 30
    assert api.page_limit == 500
    assert api.reference_refresh_interval == 86400
    assert api.session is not None


@pytest.mark.unit
def test_parse_connection_string_event_hubs():
    config, topic = IrcelineBelgiumAPI.parse_connection_string(
        "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;"
        "SharedAccessKey=secret;EntityPath=irceline-belgium"
    )

    assert config["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
    assert config["security.protocol"] == "SASL_SSL"
    assert config["sasl.mechanisms"] == "PLAIN"
    assert config["sasl.username"] == "$ConnectionString"
    assert "EntityPath=irceline-belgium" in config["sasl.password"]
    assert topic == "irceline-belgium"


@pytest.mark.unit
def test_parse_connection_string_bootstrap_server():
    config, topic = IrcelineBelgiumAPI.parse_connection_string(
        "BootstrapServer=localhost:9092;EntityPath=irceline-belgium"
    )

    assert config == {"bootstrap.servers": "localhost:9092"}
    assert topic == "irceline-belgium"


@pytest.mark.unit
def test_timestamp_conversion_ms_to_iso8601():
    assert IrcelineBelgiumAPI.timestamp_ms_to_iso8601(1743980400000) == "2025-04-06T23:00:00Z"
    assert IrcelineBelgiumAPI.timestamp_ms_to_iso8601(1743980400123) == "2025-04-06T23:00:00.123Z"


@pytest.mark.unit
def test_pagination_logic_for_timeseries():
    session = MagicMock()
    session.get.side_effect = [
        FakeResponse([{"id": str(index)} for index in range(500)]),
        FakeResponse([{"id": "500"}]),
    ]
    api = IrcelineBelgiumAPI(session=session)

    result = api.list_timeseries()

    assert len(result) == 501
    assert session.get.call_count == 2
    first_call = session.get.call_args_list[0]
    second_call = session.get.call_args_list[1]
    assert first_call.kwargs["params"] == {"limit": 500, "offset": 0, "expanded": "true"}
    assert second_call.kwargs["params"] == {"limit": 500, "offset": 500, "expanded": "true"}


@pytest.mark.unit
def test_observation_deduplication_updates_state():
    state = {"6152": 2000}
    values = [
        {"timestamp": 1000, "value": 1.0},
        {"timestamp": 2000, "value": 2.0},
        {"timestamp": 3000, "value": 3.0},
    ]

    new_values = IrcelineBelgiumAPI.filter_new_observations("6152", values, state)

    assert new_values == [{"timestamp": 3000, "value": 3.0}]
    assert state["6152"] == 3000


@pytest.mark.unit
def test_status_interval_parsing():
    parsed = IrcelineBelgiumAPI.parse_status_intervals(
        [
            {"lower": "50.0", "upper": "60.0", "name": "51 - 60 PM10", "color": "#FFBB00"},
            {"lower": "60.0", "upper": "70.0", "name": "61 - 70 PM10", "color": "#FF6600"},
        ]
    )

    assert len(parsed) == 2
    assert parsed[0].lower == "50.0"
    assert parsed[0].upper == "60.0"
    assert parsed[0].name == "51 - 60 PM10"
    assert parsed[0].color == "#FFBB00"


@pytest.mark.unit
def test_build_kafka_config_with_plaintext_bootstrap():
    args = Namespace(
        connection_string=None,
        kafka_bootstrap_servers="localhost:9092",
        kafka_topic="irceline-belgium",
        sasl_username=None,
        sasl_password=None,
        kafka_enable_tls="false",
    )

    config, topic = IrcelineBelgiumAPI.build_kafka_config(args)

    assert config["bootstrap.servers"] == "localhost:9092"
    assert config["security.protocol"] == "PLAINTEXT"
    assert topic == "irceline-belgium"
