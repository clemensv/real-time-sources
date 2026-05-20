"""Verify the --once flag causes main() to exit after one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import requests_mock

import nepal_bipad_hydrology.nepal_bipad_hydrology as bridge


SAMPLE_STATIONS_PAGE = {
    "results": [
        {
            "id": 1,
            "title": "Karnali at Chisapani",
            "basin": "Karnali",
            "point": {"coordinates": [81.27, 28.64]},
            "elevation": 191.0,
            "dangerLevel": 10.8,
            "warningLevel": 10.0,
            "description": "Test station",
            "dataSource": "DHM",
            "province": 6,
            "district": 34,
            "municipality": 76,
            "ward": 1,
            "waterLevel": 5.2,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2024-01-01T00:00:00Z",
        },
    ]
}
EMPTY_PAGE = {"results": []}


def _register_pages(m):
    base = "https://bipadportal.gov.np/api/v1/river-stations/"
    # First page returns one station, second page is empty (terminates pagination).
    m.get(base, [
        {"json": SAMPLE_STATIONS_PAGE, "status_code": 200},
        {"json": EMPTY_PAGE, "status_code": 200},
        {"json": SAMPLE_STATIONS_PAGE, "status_code": 200},
        {"json": EMPTY_PAGE, "status_code": 200},
    ])


def test_once_flag_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "nepal-bipad-hydrology", "feed",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "--once",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    with requests_mock.Mocker() as m, \
         patch.object(bridge, "Producer") as ProducerCls, \
         patch.object(bridge.time, "sleep", sleep_mock):
        _register_pages(m)
        ProducerCls.return_value = MagicMock()
        bridge.main()

    sleep_mock.assert_not_called()


def test_once_via_env_var_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "nepal-bipad-hydrology", "feed",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--state-file", str(state_file),
        "--polling-interval", "1",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    with requests_mock.Mocker() as m, \
         patch.object(bridge, "Producer") as ProducerCls, \
         patch.object(bridge.time, "sleep", sleep_mock):
        _register_pages(m)
        ProducerCls.return_value = MagicMock()
        bridge.main()

    sleep_mock.assert_not_called()
