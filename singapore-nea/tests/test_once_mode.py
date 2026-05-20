"""Tests for --once / ONCE_MODE single-cycle execution."""

import os
import sys
from unittest.mock import patch, MagicMock

import pytest

from singapore_nea import singapore_nea as bridge


@pytest.fixture
def fake_kafka(monkeypatch):
    fake = MagicMock()
    monkeypatch.setattr(bridge, "Producer", lambda *a, **kw: fake)
    return fake


def _run_main_with_argv(argv, monkeypatch, tmp_path):
    state_file = tmp_path / "state.json"
    # --state-file is a top-level parser arg; insert before the subcommand
    if "feed" in argv:
        idx = argv.index("feed")
        argv = argv[:idx] + ["--state-file", str(state_file)] + argv[idx:]
    else:
        argv = argv + ["--state-file", str(state_file)]
    monkeypatch.setattr(sys, "argv", argv)

    monkeypatch.setattr(bridge, "send_stations", lambda *a, **kw: 0)
    monkeypatch.setattr(bridge, "fetch_and_send_regions", lambda *a, **kw: 0)
    monkeypatch.setattr(bridge, "feed_observations", lambda *a, **kw: 0)
    monkeypatch.setattr(bridge, "fetch_and_send_psi", lambda *a, **kw: 0)
    monkeypatch.setattr(bridge, "fetch_and_send_pm25", lambda *a, **kw: 0)

    def _no_sleep(_seconds):
        raise AssertionError("--once mode should not sleep between cycles")

    monkeypatch.setattr(bridge.time, "sleep", _no_sleep)

    bridge.main()


def test_once_flag_exits_after_single_cycle(monkeypatch, tmp_path, fake_kafka):
    argv = [
        "singapore-nea",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--topic", "test-topic",
        "--airquality-topic", "test-airquality",
        "--once",
        "feed",
    ]
    _run_main_with_argv(argv, monkeypatch, tmp_path)


def test_once_mode_env_var(monkeypatch, tmp_path, fake_kafka):
    monkeypatch.setenv("ONCE_MODE", "true")
    argv = [
        "singapore-nea",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--topic", "test-topic",
        "--airquality-topic", "test-airquality",
        "feed",
    ]
    _run_main_with_argv(argv, monkeypatch, tmp_path)


def test_once_without_airquality(monkeypatch, tmp_path, fake_kafka):
    argv = [
        "singapore-nea",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--topic", "test-topic",
        "--airquality-topic", "",
        "--once",
        "feed",
    ]
    _run_main_with_argv(argv, monkeypatch, tmp_path)
