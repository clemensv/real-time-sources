"""Verify the --once flag drives a single polling cycle and exits."""

from __future__ import annotations

import os
import sys
from unittest.mock import MagicMock, patch

import pytest


def _force_offline_kafka(monkeypatch):
    monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=localhost:9092;EntityPath=nws-forecasts")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")


def test_once_flag_exits_after_single_cycle(monkeypatch):
    _force_offline_kafka(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["nws-forecasts", "--once"])

    from nws_forecasts.nws_forecasts import NWSForecastPoller, main

    with patch.object(NWSForecastPoller, "run", autospec=True) as run, \
            patch("nws_forecasts.nws_forecasts.Producer") as producer_cls, \
            patch("nws_forecasts.nws_forecasts.MicrosoftOpenDataUSNOAANWSForecastsEventProducer") as ev_producer_cls, \
            patch("nws_forecasts.nws_forecasts.time.sleep", side_effect=AssertionError("sleep called in --once mode")):
        producer_cls.return_value = MagicMock()
        ev_producer_cls.return_value = MagicMock()
        # main() must return cleanly without ever sleeping.
        main()

    run.assert_called_once()
    assert run.call_args.kwargs == {"once": True}


def test_once_flag_via_env_var(monkeypatch):
    _force_offline_kafka(monkeypatch)
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr(sys, "argv", ["nws-forecasts"])

    from nws_forecasts.nws_forecasts import NWSForecastPoller, main

    with patch.object(NWSForecastPoller, "run", autospec=True) as run, \
            patch("nws_forecasts.nws_forecasts.Producer") as producer_cls, \
            patch("nws_forecasts.nws_forecasts.MicrosoftOpenDataUSNOAANWSForecastsEventProducer") as ev_producer_cls, \
            patch("nws_forecasts.nws_forecasts.time.sleep", side_effect=AssertionError("sleep called in --once mode")):
        producer_cls.return_value = MagicMock()
        ev_producer_cls.return_value = MagicMock()
        main()

    run.assert_called_once()
    assert run.call_args.kwargs == {"once": True}
