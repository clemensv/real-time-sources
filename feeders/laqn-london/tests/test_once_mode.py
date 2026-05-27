"""Verify the --once flag causes the bridge to exit after one polling cycle."""

import asyncio
import sys
from unittest.mock import patch

import pytest

from laqn_london.laqn_london import LAQNLondonAPI, main


class _FakeProducer:
    def __init__(self, *_args, **_kwargs):
        self.flushed = 0

    def flush(self):
        self.flushed += 1


@pytest.mark.unit
def test_feed_once_returns_after_single_cycle():
    """feed(once=True) must complete after one cycle and never reach a second poll."""
    api = LAQNLondonAPI()

    call_counts = {"emit_reference_data": 0, "emit_measurements": 0, "emit_daily_index": 0}

    def fake_reference(_site, _species):
        call_counts["emit_reference_data"] += 1
        return ["BX1"]

    def fake_measurements(*_args, **_kwargs):
        call_counts["emit_measurements"] += 1
        return 0

    def fake_daily(*_args, **_kwargs):
        call_counts["emit_daily_index"] += 1
        return 0

    with patch.object(api, "emit_reference_data", side_effect=fake_reference), \
         patch.object(api, "emit_measurements", side_effect=fake_measurements), \
         patch.object(api, "emit_daily_index", side_effect=fake_daily), \
         patch("laqn_london.laqn_london.Producer", _FakeProducer), \
         patch("laqn_london.laqn_london._save_state"):
        asyncio.run(api.feed(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test",
            polling_interval=3600,
            state_file="",
            once=True,
        ))

    assert call_counts["emit_reference_data"] == 1
    assert call_counts["emit_measurements"] == 1
    assert call_counts["emit_daily_index"] == 1


@pytest.mark.unit
def test_once_flag_parses_from_cli():
    """`feed --once` must wire through to api.feed(once=True)."""
    captured = {}

    def fake_feed(self, kafka_config, kafka_topic, polling_interval, state_file, once=False):
        captured["once"] = once
        async def _noop():
            return None
        return _noop()

    argv = [
        "laqn_london", "feed",
        "--kafka-bootstrap-servers", "localhost:9092",
        "--kafka-topic", "test",
        "--once",
    ]
    with patch.object(sys, "argv", argv), \
         patch.object(LAQNLondonAPI, "feed", fake_feed):
        main()

    assert captured.get("once") is True


@pytest.mark.unit
def test_once_flag_defaults_to_env():
    """ONCE_MODE=true env var must set --once default to True."""
    captured = {}

    def fake_feed(self, kafka_config, kafka_topic, polling_interval, state_file, once=False):
        captured["once"] = once
        async def _noop():
            return None
        return _noop()

    argv = [
        "laqn_london", "feed",
        "--kafka-bootstrap-servers", "localhost:9092",
        "--kafka-topic", "test",
    ]
    with patch.dict("os.environ", {"ONCE_MODE": "true"}), \
         patch.object(sys, "argv", argv), \
         patch.object(LAQNLondonAPI, "feed", fake_feed):
        main()

    assert captured.get("once") is True
