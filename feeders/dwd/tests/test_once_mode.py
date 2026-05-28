"""Tests for the single-cycle (--once / ONCE_MODE) execution path."""

from typing import Any, Dict, List
from unittest.mock import MagicMock, patch
import os
import sys

from dwd.dwd import main, run_feed
from dwd.modules.base import BaseModule


class _FakeModule(BaseModule):
    def __init__(self):
        self.poll_calls = 0

    @property
    def name(self) -> str:
        return "fake"

    @property
    def default_enabled(self) -> bool:
        return True

    @property
    def default_poll_interval(self) -> int:
        return 60

    def poll(self, _state: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.poll_calls += 1
        return []


def test_run_feed_once_exits_without_sleep():
    fake_module = _FakeModule()
    fake_kafka = MagicMock()

    with patch("dwd.dwd.Producer", return_value=fake_kafka), \
         patch("dwd.dwd.DEDWDCDCEventProducer", MagicMock()), \
         patch("dwd.dwd.DEDWDWeatherEventProducer", MagicMock()), \
         patch("dwd.dwd.DEDWDRadarEventProducer", MagicMock()), \
         patch("dwd.dwd.DEDWDForecastEventProducer", MagicMock()), \
         patch("dwd.dwd.load_state", return_value={}), \
         patch("dwd.dwd.save_state") as save_state_mock, \
         patch("dwd.dwd.time.sleep", side_effect=AssertionError("sleep should not be called in --once mode")):
        run_feed(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="dwd",
            polling_interval=None,
            state_file="/tmp/dwd-state.json",
            modules=[fake_module],
            once=True,
        )

    assert fake_module.poll_calls == 1
    save_state_mock.assert_called_once()


def test_once_mode_env_var_sets_main_once_flag():
    fake_module = _FakeModule()

    with patch("dwd.dwd.DWDHttpClient", return_value=MagicMock()), \
         patch("dwd.dwd._resolve_modules", return_value=[fake_module]), \
         patch("dwd.dwd.run_feed") as run_feed_mock, \
         patch.dict(os.environ, {"ONCE_MODE": "true"}, clear=False), \
         patch.object(sys, "argv", [
             "dwd",
             "feed",
             "--kafka-bootstrap-servers", "localhost:9092",
             "--kafka-topic", "dwd",
         ]):
        main()

    assert run_feed_mock.call_args.kwargs["once"] is True
