"""Verify --once causes main() to return after a single polling cycle."""

from __future__ import annotations

import os
from unittest.mock import patch

import requests_mock

from uba_airdata import uba_airdata as bridge
from tests.test_uba_airdata_unit import COMPONENTS_PAYLOAD, MEASURES_PAYLOAD, STATIONS_PAYLOAD


def test_once_mode_runs_single_cycle(monkeypatch, tmp_path):
    """With --once, main() must return after one cycle and call time.sleep zero times for inter-cycle pacing."""

    state_file = tmp_path / "state.json"
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    monkeypatch.setenv("KAFKA_TOPIC", "uba-airdata-test")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.setattr(
        "sys.argv",
        [
            "uba_airdata",
            "feed",
            "--state-file",
            str(state_file),
            "--polling-interval",
            "1",
            "--once",
        ],
    )

    class FakeProducer:
        def __init__(self, *args, **kwargs):
            pass

        def produce(self, *args, **kwargs):
            pass

        def flush(self, *args, **kwargs):
            pass

        def poll(self, *args, **kwargs):
            pass

    sleep_calls: list[float] = []

    def fake_sleep(seconds):
        sleep_calls.append(float(seconds))

    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://www.umweltbundesamt.de/api/air_data/v3/stations/json",
            json=STATIONS_PAYLOAD,
        )
        mocker.get(
            "https://www.umweltbundesamt.de/api/air_data/v3/components/json",
            json=COMPONENTS_PAYLOAD,
        )
        mocker.get(
            "https://www.umweltbundesamt.de/api/air_data/v3/measures/json",
            json=MEASURES_PAYLOAD,
        )

        with patch.object(bridge, "Producer", FakeProducer), patch.object(
            bridge.time, "sleep", side_effect=fake_sleep
        ):
            bridge.main()

    assert sleep_calls == [], "Bridge must not sleep between cycles when --once is set"
    assert state_file.exists(), "State file should be written during the single cycle"


def test_once_mode_env_var(monkeypatch, tmp_path):
    """ONCE_MODE=true env var should be equivalent to --once."""

    state_file = tmp_path / "state.json"
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    monkeypatch.setenv("KAFKA_TOPIC", "uba-airdata-test")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setenv("STATE_FILE", str(state_file))
    monkeypatch.setattr("sys.argv", ["uba_airdata", "feed", "--polling-interval", "1"])

    class FakeProducer:
        def __init__(self, *args, **kwargs):
            pass

        def produce(self, *args, **kwargs):
            pass

        def flush(self, *args, **kwargs):
            pass

        def poll(self, *args, **kwargs):
            pass

    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://www.umweltbundesamt.de/api/air_data/v3/stations/json",
            json=STATIONS_PAYLOAD,
        )
        mocker.get(
            "https://www.umweltbundesamt.de/api/air_data/v3/components/json",
            json=COMPONENTS_PAYLOAD,
        )
        mocker.get(
            "https://www.umweltbundesamt.de/api/air_data/v3/measures/json",
            json=MEASURES_PAYLOAD,
        )

        with patch.object(bridge, "Producer", FakeProducer), patch.object(
            bridge.time, "sleep", lambda *_: None
        ):
            bridge.main()
