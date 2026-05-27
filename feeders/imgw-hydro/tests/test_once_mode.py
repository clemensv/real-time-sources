"""Unit test asserting --once causes main() to return after exactly one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import pytest

from imgw_hydro import imgw_hydro as bridge


SAMPLE_RECORDS = [
    {
        "id_stacji": "150180090",
        "stacja": "Test",
        "rzeka": "TestRiver",
        "wojewodztwo": "test",
        "lon": "18.0",
        "lat": "50.0",
        "stan_wody": "100",
        "stan_wody_data_pomiaru": "2026-03-25 12:00:00",
        "temperatura_wody": None,
        "temperatura_wody_data_pomiaru": None,
        "przeplyw": None,
        "przeplyw_data": None,
        "zjawisko_lodowe": None,
        "zjawisko_zarastania": None,
    },
]


def test_once_mode_exits_after_single_cycle(monkeypatch):
    """`feed --once` must return after one polling cycle without sleeping."""
    fake_producer = MagicMock()
    fake_producer_cls = MagicMock(return_value=fake_producer)

    fake_event_producer = MagicMock()
    fake_event_producer.producer = fake_producer

    sleep_calls = []

    def fake_sleep(seconds):
        sleep_calls.append(seconds)
        raise AssertionError("time.sleep must not be called when --once is set")

    monkeypatch.setattr(bridge, "Producer", fake_producer_cls)
    monkeypatch.setattr(bridge, "PLGovIMGWHydroEventProducer", lambda *a, **kw: fake_event_producer)
    monkeypatch.setattr(bridge.time, "sleep", fake_sleep)
    monkeypatch.setattr(bridge.IMGWHydroAPI, "get_all_data", lambda self: list(SAMPLE_RECORDS))

    argv = [
        "imgw-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--topic", "test-imgw-hydro",
        "--state-file", "",
        "--once",
        "feed",
    ]
    with patch.object(sys, "argv", argv):
        bridge.main()

    assert sleep_calls == [], "Expected no sleep calls in --once mode"
    assert fake_event_producer.producer.flush.call_count >= 1


def test_once_mode_via_env_var(monkeypatch):
    """ONCE_MODE=true env var must also short-circuit the polling loop."""
    fake_producer = MagicMock()
    fake_event_producer = MagicMock()
    fake_event_producer.producer = fake_producer

    monkeypatch.setattr(bridge, "Producer", MagicMock(return_value=fake_producer))
    monkeypatch.setattr(bridge, "PLGovIMGWHydroEventProducer", lambda *a, **kw: fake_event_producer)
    monkeypatch.setattr(bridge.time, "sleep", lambda s: (_ for _ in ()).throw(AssertionError("sleep called")))
    monkeypatch.setattr(bridge.IMGWHydroAPI, "get_all_data", lambda self: list(SAMPLE_RECORDS))

    monkeypatch.setenv("ONCE_MODE", "true")

    argv = [
        "imgw-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--topic", "test-imgw-hydro",
        "--state-file", "",
        "feed",
    ]
    with patch.object(sys, "argv", argv):
        bridge.main()
