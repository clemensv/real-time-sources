from __future__ import annotations

import asyncio
from unittest import mock

import pytest

from noaa_swpc_l1_kafka import app as kafka_app


@pytest.mark.unit
def test_parse_kafka_connection_string_event_hubs_and_harness():
    event_hubs = (
        "Endpoint=sb://namespace.servicebus.windows.net/;"
        "SharedAccessKeyName=RootManageSharedAccessKey;"
        "SharedAccessKey=abc123=;"
        "EntityPath=noaa-topic"
    )
    parsed = kafka_app.parse_kafka_connection_string(event_hubs)
    assert parsed["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
    assert parsed["kafka_topic"] == "noaa-topic"
    assert parsed["sasl.username"] == "$ConnectionString"
    assert parsed["sasl.password"] == event_hubs
    assert parsed["security.protocol"] == "SASL_SSL"
    assert parsed["sasl.mechanism"] == "PLAIN"

    harness = kafka_app.parse_kafka_connection_string(
        "BootstrapServer=broker:9092;EntityPath=test-topic"
    )
    assert harness == {"bootstrap.servers": "broker:9092", "kafka_topic": "test-topic"}


@pytest.mark.unit
def test_build_kafka_config_tls_and_plaintext():
    assert kafka_app.build_kafka_config(bootstrap_servers="b:9093") == {
        "bootstrap.servers": "b:9093",
        "security.protocol": "SSL",
    }
    assert kafka_app.build_kafka_config(
        bootstrap_servers="b:9092",
        sasl_username="u",
        sasl_password="p",
        tls_enabled=False,
    ) == {
        "bootstrap.servers": "b:9092",
        "sasl.mechanisms": "PLAIN",
        "security.protocol": "SASL_PLAINTEXT",
        "sasl.username": "u",
        "sasl.password": "p",
    }


@pytest.mark.unit
def test_row_to_data_preserves_fields(sample_row):
    data = kafka_app._row_to_data(sample_row)

    assert data.spacecraft.value == "dscovr"
    assert data.time_tag == sample_row.time_tag
    assert data.propagated_time_tag == sample_row.propagated_time_tag
    assert data.speed == 410.5
    assert data.bz is None
    assert data.vx is None


@pytest.mark.unit
def test_main_parses_connection_string_and_prefers_entity_path(monkeypatch, tmp_path):
    calls = []

    async def fake_feed(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    with mock.patch.object(kafka_app, "SwpcL1API", return_value=mock.Mock()), \
         mock.patch.object(kafka_app, "feed", side_effect=fake_feed):
        kafka_app.main([
            "feed",
            "--connection-string",
            "BootstrapServer=broker:9092;EntityPath=entity-topic",
            "--kafka-topic",
            "cli-topic",
            "--state-file",
            str(tmp_path / "state.json"),
            "--once",
        ])

    args, kwargs = calls[0]
    assert args[1]["bootstrap.servers"] == "broker:9092"
    assert args[1].get("security.protocol") is None
    assert args[2] == "entity-topic"
    assert kwargs["once"] is True


@pytest.mark.unit
def test_feed_once_sends_rows_flushes_and_saves_state(tmp_path, sample_row):
    api = mock.Mock()
    api.fetch_new_rows.return_value = [sample_row]
    raw_producer = mock.MagicMock()
    event_producer = mock.MagicMock()

    state_file = tmp_path / "state.json"
    with mock.patch.object(kafka_app, "Producer", return_value=raw_producer), \
         mock.patch.object(
             kafka_app,
             "GovNoaaSwpcL1KafkaEventProducer",
             return_value=event_producer,
         ):
        asyncio.run(kafka_app.feed(
            api,
            {"bootstrap.servers": "broker:9092"},
            "topic",
            spacecraft="dscovr",
            polling_interval=1,
            state_file=str(state_file),
            once=True,
            backfill_minutes=60,
        ))

    event_producer.send_gov_noaa_swpc_l1_kafka_propagated_solar_wind.assert_called_once()
    call = event_producer.send_gov_noaa_swpc_l1_kafka_propagated_solar_wind.call_args
    assert call.kwargs["_feedurl"] == kafka_app.FEED_URL
    assert call.kwargs["_spacecraft"] == "dscovr"
    assert call.kwargs["_time"] == sample_row.time_tag.isoformat()
    assert call.kwargs["flush_producer"] is False
    assert raw_producer.flush.call_count == 2
    assert kafka_app.load_state(str(state_file))["last_time_tag"] == sample_row.time_tag.isoformat()
