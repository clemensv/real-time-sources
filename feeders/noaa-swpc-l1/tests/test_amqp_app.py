from __future__ import annotations

from unittest import mock

import pytest
from proton import Message, symbol

from noaa_swpc_l1_amqp import app as amqp_app


class FakeSender:
    def __init__(self):
        self.sent = []

    def send(self, message, *args, **kwargs):
        self.sent.append((message, args, kwargs))
        return "sent"


class FakeProducer:
    def __init__(self):
        self.sent = []
        self.closed = False

    def send_propagated_solar_wind(self, **kwargs):
        self.sent.append(kwargs)

    def close(self):
        self.closed = True


@pytest.mark.unit
def test_parse_broker_url_extracts_address_auth_and_tls():
    assert amqp_app._parse_broker_url("amqps://user:pass@example.test:5679/my-address") == (
        "example.test",
        5679,
        True,
        "user",
        "pass",
        "my-address",
    )
    assert amqp_app._parse_broker_url("broker.test") == (
        "broker.test",
        5672,
        False,
        None,
        None,
        None,
    )


@pytest.mark.unit
def test_row_to_data_preserves_fields(sample_row):
    data = amqp_app._row_to_data(sample_row)

    assert data.spacecraft.value == "dscovr"
    assert data.time_tag == sample_row.time_tag
    assert data.propagated_time_tag == sample_row.propagated_time_tag
    assert data.bt == sample_row.bt
    assert data.vx is None


@pytest.mark.unit
def test_install_partition_key_wrapper_stamps_sender_message_subject():
    fake_sender = FakeSender()
    producer = type("Producer", (), {"_sender": fake_sender})()
    message = Message(subject="dscovr")

    amqp_app._install_partition_key_wrapper(producer)
    result = producer._sender.send(message)

    assert result == "sent"
    assert fake_sender.sent[0][0] is message
    assert message.annotations[symbol("x-opt-partition-key")] == "dscovr"


@pytest.mark.unit
def test_install_partition_key_wrapper_stamps_reactor_message_subject():
    calls = []

    class ReactorProducer:
        def _send_via_reactor(self, message, timeout=30.0):
            calls.append((message, timeout))
            return "reactor-sent"

    producer = ReactorProducer()
    message = Message(subject="dscovr")

    amqp_app._install_partition_key_wrapper(producer)
    result = producer._send_via_reactor(message, timeout=5.0)

    assert result == "reactor-sent"
    assert calls == [(message, 5.0)]
    assert message.annotations[amqp_app.PARTITION_KEY_ANNOTATION] == "dscovr"


@pytest.mark.unit
def test_partition_key_stamp_uses_utf8_string_value():
    message = Message(subject="dscovr")

    amqp_app._stamp_partition_key(message)

    key = symbol("x-opt-partition-key")
    assert message.annotations[key] == "dscovr"
    assert isinstance(message.annotations[key], str)


@pytest.mark.unit
def test_main_parses_broker_url_builds_wraps_and_feeds(tmp_path):
    fake_api = mock.Mock()
    fake_producer = FakeProducer()

    with mock.patch.object(amqp_app, "SwpcL1API", return_value=fake_api), \
         mock.patch.object(amqp_app, "_build_producer", return_value=fake_producer) as build, \
         mock.patch.object(amqp_app, "_install_partition_key_wrapper") as install, \
         mock.patch.object(amqp_app, "feed") as feed:
        amqp_app.main([
            "feed",
            "--broker-url",
            "amqps://user:pass@broker.test:5679/from-url",
            "--address",
            "from-cli",
            "--state-file",
            str(tmp_path / "state.json"),
            "--once",
        ])

    build.assert_called_once()
    assert build.call_args.kwargs["host"] == "broker.test"
    assert build.call_args.kwargs["port"] == 5679
    assert build.call_args.kwargs["address"] == "from-url"
    assert build.call_args.kwargs["use_tls"] is True
    assert build.call_args.kwargs["username"] == "user"
    assert build.call_args.kwargs["password"] == "pass"
    install.assert_called_once_with(fake_producer)
    feed.assert_called_once()
    assert feed.call_args.args == (fake_api, fake_producer)
    assert feed.call_args.kwargs["once"] is True


@pytest.mark.unit
def test_feed_once_sends_row_saves_state_and_closes(tmp_path, sample_row):
    api = mock.Mock()
    api.fetch_new_rows.return_value = [sample_row]
    producer = FakeProducer()
    state_file = tmp_path / "state.json"

    amqp_app.feed(
        api,
        producer,
        spacecraft="dscovr",
        polling_interval=1,
        state_file=str(state_file),
        once=True,
        backfill_minutes=60,
    )

    assert producer.closed is True
    assert len(producer.sent) == 1
    sent = producer.sent[0]
    assert sent["_feedurl"] == amqp_app.FEED_URL
    assert sent["_spacecraft"] == "dscovr"
    assert sent["_time_tag"] == sample_row.time_tag.isoformat()
    assert sent["data"].speed == sample_row.speed
    assert amqp_app.load_state(str(state_file))["last_time_tag"] == sample_row.time_tag.isoformat()
