"""Verify the --once flag causes main() to exit after one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import bafu_hydro.bafu_hydro as bridge


SAMPLE_LOCATIONS = {
    "payload": {
        "2018": {
            "details": {
                "id": 2018,
                "name": "Rhein - Basel",
                "water-body-name": "Rhein",
                "water-body-type": "river",
                "lat": 47.5596,
                "lon": 7.5886,
            }
        }
    }
}

SAMPLE_LATEST = {
    "payload": [
        {"loc": 2018, "par": bridge.PAR_HEIGHT, "val": 2.56, "timestamp": 1700000000},
    ]
}


def _fake_get(url, *args, **kwargs):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    if "locations" in url:
        resp.json.return_value = SAMPLE_LOCATIONS
    else:
        resp.json.return_value = SAMPLE_LATEST
    return resp


def test_once_flag_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "bafu-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--topic", "bafu-hydro",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "feed",
        "--once",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    with patch.object(bridge, "Producer") as ProducerCls, \
         patch.object(bridge.requests, "get", side_effect=_fake_get), \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProducerCls.return_value = MagicMock()
        bridge.main()

    sleep_mock.assert_not_called()


def test_once_via_env_var_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "bafu-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--topic", "bafu-hydro",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "feed",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    with patch.object(bridge, "Producer") as ProducerCls, \
         patch.object(bridge.requests, "get", side_effect=_fake_get), \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProducerCls.return_value = MagicMock()
        bridge.main()

    sleep_mock.assert_not_called()
