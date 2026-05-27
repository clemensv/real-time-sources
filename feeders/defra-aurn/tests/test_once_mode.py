"""Tests for the --once flag added for Fabric notebook hosting."""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest

from defra_aurn.defra_aurn import build_parser, run_feed


@pytest.mark.unit
def test_once_flag_parses_true():
    parser = build_parser()
    args = parser.parse_args(["feed", "--once"])
    assert args.once is True


@pytest.mark.unit
def test_once_flag_default_false(monkeypatch):
    monkeypatch.delenv("ONCE_MODE", raising=False)
    parser = build_parser()
    args = parser.parse_args(["feed"])
    assert args.once is False


@pytest.mark.unit
def test_once_mode_env_var_enables_once(monkeypatch):
    monkeypatch.setenv("ONCE_MODE", "true")
    parser = build_parser()
    args = parser.parse_args(["feed"])
    assert args.once is True


@pytest.mark.unit
def test_run_feed_once_returns_after_single_cycle(monkeypatch):
    """`run_feed` with args.once=True must exit after one polling cycle."""

    fake_catalog = {"ts-1": object()}

    class FakeAPI:
        def __init__(self, *_, **__):
            self.emit_observations_calls = 0

        def emit_observations(self, *_args, **_kwargs):
            self.emit_observations_calls += 1
            return 0

    monkeypatch.setattr("defra_aurn.defra_aurn.DefraAURNAPI", FakeAPI)
    monkeypatch.setattr(
        "defra_aurn.defra_aurn.refresh_reference_data",
        lambda *_a, **_kw: (fake_catalog, True),
    )
    monkeypatch.setattr(
        "defra_aurn.defra_aurn.UkGovDefraAurnStationsEventProducer",
        lambda *_a, **_kw: object(),
    )
    monkeypatch.setattr(
        "defra_aurn.defra_aurn.UkGovDefraAurnTimeseriesEventProducer",
        lambda *_a, **_kw: object(),
    )

    flushed = {"count": 0}

    class FakeProducer:
        def __init__(self, *_a, **_kw):
            pass

        def flush(self):
            flushed["count"] += 1

    monkeypatch.setattr("defra_aurn.defra_aurn.Producer", FakeProducer)
    monkeypatch.setattr("defra_aurn.defra_aurn._load_state", lambda *_: {})
    monkeypatch.setattr("defra_aurn.defra_aurn._save_state", lambda *_: None)

    def _fail_sleep(_seconds):  # pragma: no cover - guard against retry loops
        raise AssertionError("time.sleep must not be called when --once is set")

    monkeypatch.setattr("defra_aurn.defra_aurn.time.sleep", _fail_sleep)

    parser = build_parser()
    args = parser.parse_args(
        [
            "feed",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=defra-aurn",
            "--kafka-enable-tls",
            "false",
            "--once",
        ]
    )

    run_feed(args)

    assert flushed["count"] == 1
