"""Tests for --once / ONCE_MODE single-cycle execution."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from bfs_odl import bfs_odl as bridge


SAMPLE_STATION_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [9.38, 54.78]},
    "properties": {
        "id": "DEZ0001",
        "kenn": "010010001",
        "plz": "24941",
        "name": "Flensburg",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "kid": 6,
        "height_above_sea": 39,
    },
}

SAMPLE_MEASUREMENT_FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [10.24, 52.74]},
    "properties": {
        "id": "DEZ0305",
        "kenn": "033510091",
        "plz": "29348",
        "name": "Eschede",
        "site_status": 1,
        "site_status_text": "in Betrieb",
        "kid": 5,
        "height_above_sea": 63,
        "start_measure": "2026-04-07T12:00:00Z",
        "end_measure": "2026-04-07T13:00:00Z",
        "value": 0.079,
        "value_cosmic": 0.043,
        "value_terrestrial": 0.036,
        "unit": "µSv/h",
        "validated": 1,
        "nuclide": "Gamma-ODL-Brutto",
        "duration": "1h",
    },
}


@pytest.fixture
def _mock_kafka_and_api(monkeypatch):
    """Patch out Kafka producer + BfsOdlAPI so feed() runs without network."""
    fake_producer = MagicMock()
    monkeypatch.setattr(bridge, "Producer", MagicMock(return_value=fake_producer))

    fake_event_producer = MagicMock()
    monkeypatch.setattr(
        bridge, "DeBfsOdlEventProducer", MagicMock(return_value=fake_event_producer)
    )

    fake_api = MagicMock()
    fake_api.fetch_stations.return_value = [SAMPLE_STATION_FEATURE]
    fake_api.parse_station.side_effect = lambda f: bridge.BfsOdlAPI.parse_station(f)
    fake_api.fetch_latest_measurements.return_value = [SAMPLE_MEASUREMENT_FEATURE]
    fake_api.parse_measurement.side_effect = lambda f: bridge.BfsOdlAPI.parse_measurement(f)
    monkeypatch.setattr(bridge, "BfsOdlAPI", MagicMock(return_value=fake_api))

    return fake_api, fake_producer


def _no_sleep(*_args, **_kwargs):
    raise AssertionError("time.sleep must not be called in --once mode")


def test_once_flag_exits_after_one_cycle(monkeypatch, tmp_path, _mock_kafka_and_api):
    """`--once` causes feed() to return after exactly one polling cycle."""
    fake_api, _ = _mock_kafka_and_api
    monkeypatch.setattr(bridge.time, "sleep", _no_sleep)

    state_file = str(tmp_path / "state.json")
    argv = [
        "bfs-odl",
        "feed",
        "--connection-string",
        "BootstrapServer=localhost:9092;EntityPath=test-bfs-odl",
        "--polling-interval",
        "1",
        "--state-file",
        state_file,
        "--once",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    # Should return cleanly, not block in the polling loop.
    bridge.main()

    assert fake_api.fetch_stations.call_count == 1
    assert fake_api.fetch_latest_measurements.call_count == 1


def test_once_mode_env_var_exits_after_one_cycle(monkeypatch, tmp_path, _mock_kafka_and_api):
    """`ONCE_MODE=true` env var alone (no --once flag) also triggers single-cycle exit."""
    fake_api, _ = _mock_kafka_and_api
    monkeypatch.setattr(bridge.time, "sleep", _no_sleep)

    state_file = str(tmp_path / "state.json")
    argv = [
        "bfs-odl",
        "feed",
        "--connection-string",
        "BootstrapServer=localhost:9092;EntityPath=test-bfs-odl",
        "--polling-interval",
        "1",
        "--state-file",
        state_file,
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.setenv("ONCE_MODE", "true")

    bridge.main()

    assert fake_api.fetch_latest_measurements.call_count == 1
