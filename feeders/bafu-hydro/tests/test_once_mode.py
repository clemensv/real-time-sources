"""Verify the --once flag causes main() to exit after one polling cycle."""

import json
import sys
import pytest
from unittest.mock import patch, MagicMock, call

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
         patch.object(bridge.requests.Session, "get", side_effect=_fake_get) as get_mock, \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProducerCls.return_value = MagicMock()
        ProducerCls.return_value.flush.return_value = 0
        bridge.main()

    sleep_mock.assert_not_called()
    assert get_mock.call_args_list == [
        call(f"{bridge.EXISTENZ_BASE_URL}/locations", timeout=60),
        call(f"{bridge.EXISTENZ_BASE_URL}/latest", timeout=60),
    ]
    assert ProducerCls.return_value.produce.call_count == 2


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
         patch.object(bridge.requests.Session, "get", side_effect=_fake_get) as get_mock, \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProducerCls.return_value = MagicMock()
        ProducerCls.return_value.flush.return_value = 0
        bridge.main()

    sleep_mock.assert_not_called()
    assert get_mock.call_args_list == [
        call(f"{bridge.EXISTENZ_BASE_URL}/locations", timeout=60),
        call(f"{bridge.EXISTENZ_BASE_URL}/latest", timeout=60),
    ]
    assert ProducerCls.return_value.produce.call_count == 2


@pytest.mark.parametrize("selector", ["flag", "environment"])
def test_mock_mode_uses_normal_producer_without_http_state_or_sleep(tmp_path, monkeypatch, selector):
    state_file = tmp_path / "state.json"
    state_file.write_text('{"retained-live-reading": "unchanged"}', encoding="utf-8")
    original_state = state_file.read_bytes()
    argv = [
        "bafu-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--state-file", str(state_file),
        "feed",
    ]
    monkeypatch.delenv("MOCK_MODE", raising=False)
    monkeypatch.delenv("ONCE_MODE", raising=False)
    if selector == "flag":
        argv.append("--mock")
    else:
        monkeypatch.setenv("MOCK_MODE", "true")
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    kafka_producer = MagicMock()
    kafka_producer.flush.return_value = 0
    forbidden = AssertionError("Mock mode must not touch HTTP, state or sleep")

    with patch.object(bridge, "Producer", return_value=kafka_producer), \
         patch.object(bridge.requests.Session, "request", side_effect=forbidden), \
         patch.object(bridge, "_load_state", side_effect=forbidden), \
         patch.object(bridge, "_save_state", side_effect=forbidden), \
         patch.object(bridge.time, "sleep", side_effect=forbidden):
        bridge.main()

    calls = kafka_producer.produce.call_args_list
    events = [json.loads(item.kwargs["value"]) for item in calls]
    assert [event["type"].split(".")[-1] for event in events] == (
        ["Station"] * 3 + ["WaterLevelObservation"] * 3
    )
    for item, event in zip(calls, events):
        key = item.kwargs["key"]
        if isinstance(key, bytes):
            key = key.decode("utf-8")
        assert key == event["subject"] == event["data"]["station_id"]
        assert key.startswith("mock-station-")
    assert state_file.read_bytes() == original_state


@pytest.mark.parametrize("flush_results,produced_count", [([1], 3), ([0, 1], 6)])
def test_mock_mode_surfaces_failed_flush(monkeypatch, flush_results, produced_count):
    monkeypatch.setattr(sys, "argv", [
        "bafu-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "feed", "--mock",
    ])
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    kafka_producer = MagicMock()
    kafka_producer.flush.side_effect = flush_results
    with patch.object(bridge, "Producer", return_value=kafka_producer), \
         patch.object(bridge.requests.Session, "request", side_effect=AssertionError("Unexpected HTTP")):
        with pytest.raises(RuntimeError, match="Kafka flush failed"):
            bridge.main()
    assert kafka_producer.produce.call_count == produced_count


def test_false_mock_setting_keeps_http_failure_visible(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", [
        "bafu-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--state-file", str(tmp_path / "state.json"),
        "feed", "--once",
    ])
    monkeypatch.setenv("MOCK_MODE", "false")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    forbidden = bridge.requests.HTTPError("403 Forbidden")
    kafka_producer = MagicMock()
    kafka_producer.flush.return_value = 0
    with patch.object(bridge, "Producer", return_value=kafka_producer), \
         patch.object(bridge.requests.Session, "get", side_effect=forbidden) as get_mock:
        with pytest.raises(bridge.requests.HTTPError, match="403 Forbidden"):
            bridge.main()
    assert get_mock.call_args_list == [
        call(f"{bridge.EXISTENZ_BASE_URL}/locations", timeout=60),
    ]
    kafka_producer.produce.assert_not_called()


def test_once_mode_propagates_failed_delivery_without_state_changes(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    state_file.write_text('{"retained-live-reading": "unchanged"}', encoding="utf-8")
    original_state = state_file.read_bytes()
    monkeypatch.setattr(sys, "argv", [
        "bafu-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--state-file", str(state_file),
        "feed", "--once",
    ])
    monkeypatch.delenv("MOCK_MODE", raising=False)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    kafka_producer = MagicMock()
    kafka_producer.flush.side_effect = [0, 1]
    with patch.object(bridge, "Producer", return_value=kafka_producer), \
         patch.object(bridge.requests.Session, "get", side_effect=_fake_get), \
         patch.object(bridge.time, "sleep", side_effect=AssertionError("Unexpected sleep")):
        with pytest.raises(RuntimeError, match="Kafka flush failed"):
            bridge.main()
    assert state_file.read_bytes() == original_state
