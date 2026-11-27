"""Verify the ``--once`` flag exits the polling loop after one cycle.

This guards the contract relied on by the Fabric notebook hosting option,
which runs ``kmi-belgium feed --once`` on a schedule and expects the
process to exit after a single polling cycle.
"""

from __future__ import annotations

import importlib
import json
import sys
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import requests

# Re-use the stubs configured in test_kmi_belgium so the bridge module imports.
from . import test_kmi_belgium  # noqa: F401

from kmi_belgium import kmi_belgium as bridge


def test_feed_once_exits_after_single_cycle():
    call_count = {"feed": 0, "sleep": 0}

    def fake_feed(api, producer, previous_readings):
        call_count["feed"] += 1
        return 0

    def fake_sleep(_seconds):
        call_count["sleep"] += 1
        raise AssertionError("time.sleep must not be called when --once is set")

    argv = [
        "kmi-belgium",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=kmi-belgium",
        "--state-file", "/tmp/kmi-belgium-test-state.json",
        "feed", "--once",
    ]

    with patch.object(bridge, "Producer", lambda *a, **kw: object()), \
         patch.object(bridge, "BEGovKMIWeatherEventProducer", lambda *a, **kw: object()), \
         patch.object(bridge, "KMIBelgiumAPI", lambda *a, **kw: object()), \
         patch.object(bridge, "send_stations", lambda api, producer: None), \
         patch.object(bridge, "feed_observations", fake_feed), \
         patch.object(bridge, "_load_state", lambda path: {}), \
         patch.object(bridge, "_save_state", lambda path, state: None), \
         patch.object(bridge.time, "sleep", fake_sleep), \
         patch.object(sys, "argv", argv):
        bridge.main()

    assert call_count["feed"] == 1, f"expected exactly one feed cycle, got {call_count['feed']}"
    assert call_count["sleep"] == 0, "time.sleep must not run in --once mode"


@pytest.mark.parametrize("transport", ["mqtt", "amqp"])
@pytest.mark.parametrize("selection", ["environment", "cli"])
def test_companion_mock_emits_reference_then_observation_without_http_or_state(monkeypatch, tmp_path, transport, selection):
    state_file = tmp_path / "live-state.json"
    state_file.write_text('{"preserved": true}', encoding="utf-8")
    emitted = []
    app, producer = _install_companion_producer(monkeypatch, transport, emitted)

    def forbid_http(*args, **kwargs):
        raise AssertionError("Mock mode must not call the upstream")

    async def forbid_sleep(*args):
        raise AssertionError("Mock mode must finish after one sample cycle")

    def forbid_state(*args):
        raise AssertionError("Mock mode must not access live state")

    monkeypatch.setattr(requests.sessions.Session, "request", forbid_http)
    monkeypatch.setattr(app.asyncio, "sleep", forbid_sleep)
    monkeypatch.setattr(app, "_load_state", forbid_state)
    monkeypatch.setattr(app, "_save_state", forbid_state)
    monkeypatch.setenv("ONCE_MODE", "false")
    monkeypatch.setenv("KMI_BELGIUM_MOCK", "true" if selection == "environment" else "false")
    argv = [f"kmi-belgium-{transport}", "feed", "--state-file", str(state_file)]
    if selection == "cli":
        argv.append("--mock")
    monkeypatch.setattr(sys, "argv", argv)
    app.main()

    assert [family for family, _ in emitted] == ["station", "observation"]
    assert emitted[0][1]["data"].station_code == emitted[1][1]["data"].station_code
    assert emitted[1][1]["data"].observation_time.tzinfo is not None
    assert isinstance(emitted[0][1]["data"].latitude, float)
    assert isinstance(emitted[0][1]["data"].longitude, float)
    observation = emitted[1][1]["data"]
    assert observation.observation_time == datetime(2024, 5, 1, 10, 20, tzinfo=timezone.utc)
    assert isinstance(observation.temp_dry_shelter_avg, float)
    assert observation.precip_quantity == 0.0
    assert emitted[1][1]["_time"] == observation.observation_time.isoformat()
    identity_argument = "station_code" if transport == "mqtt" else "_station_code"
    assert [kwargs[identity_argument] for _, kwargs in emitted] == [observation.station_code] * 2
    assert state_file.read_text(encoding="utf-8") == '{"preserved": true}'
    if transport == "mqtt":
        producer.connect.assert_awaited_once()
        producer.disconnect.assert_awaited_once()
    else:
        producer.close.assert_called_once()


def _install_companion_producer(monkeypatch, transport, emitted):
    app = importlib.import_module(f"kmi_belgium_{transport}.app")
    producer = MagicMock()
    monkeypatch.setenv("MQTT_AUTH_MODE", "password")
    if transport == "mqtt":
        producer.connect = AsyncMock()
        producer.disconnect = AsyncMock()
        producer.publish_be_gov_kmi_weather_mqtt_station = AsyncMock(side_effect=lambda **kw: emitted.append(("station", kw)))
        producer.publish_be_gov_kmi_weather_mqtt_weather_observation = AsyncMock(side_effect=lambda **kw: emitted.append(("observation", kw)))
        monkeypatch.setattr(app, "BEGovKMIWeatherMqttMqttClient", lambda **kw: producer)
    else:
        producer.send_station.side_effect = lambda **kw: emitted.append(("station", kw))
        producer.send_weather_observation.side_effect = lambda **kw: emitted.append(("observation", kw))
        monkeypatch.setattr(app, "_build_amqp_producer", lambda args: producer)
    return app, producer


def _install_live_api(monkeypatch, app):
    api = MagicMock()
    api.get_latest_observations.return_value = [test_kmi_belgium.SAMPLE_FEATURE]
    api.get_observations.return_value = [test_kmi_belgium.SAMPLE_FEATURE]
    api.parse_observation.side_effect = app.KMIBelgiumAPI.parse_observation
    factory = MagicMock(return_value=api)
    monkeypatch.setattr(app, "KMIBelgiumAPI", factory)
    return factory, api


@pytest.mark.parametrize("transport", ["mqtt", "amqp"])
@pytest.mark.parametrize("mock_value", [None, "false"])
def test_companion_defaults_to_live_acquisition_and_preserves_resume_state(monkeypatch, tmp_path, transport, mock_value):
    emitted = []
    app, producer = _install_companion_producer(monkeypatch, transport, emitted)
    factory, api = _install_live_api(monkeypatch, app)
    state_file = tmp_path / "live-state.json"
    cursor = "2024-05-01T10:10:00Z"
    state_file.write_text(json.dumps({"preserved": True, "__last_timestamp__": cursor}), encoding="utf-8")
    if mock_value is None:
        monkeypatch.delenv("KMI_BELGIUM_MOCK", raising=False)
    else:
        monkeypatch.setenv("KMI_BELGIUM_MOCK", mock_value)

    def forbid_mock(**kwargs):
        raise AssertionError("Live mode must not select synthetic acquisition")

    async def forbid_sleep(*args):
        raise AssertionError("--once must finish after one live cycle")

    monkeypatch.setattr(app, "MockKMIBelgiumAPI", forbid_mock)
    monkeypatch.setattr(app.asyncio, "sleep", forbid_sleep)
    monkeypatch.setattr(sys, "argv", [f"kmi-belgium-{transport}", "feed", "--once", "--state-file", str(state_file)])
    app.main()

    factory.assert_called_once()
    api.get_latest_observations.assert_called_once_with()
    api.get_observations.assert_called_once_with(last_timestamp=cursor)
    assert [family for family, _ in emitted] == ["station", "observation"]
    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["preserved"] is True
    assert state["__last_timestamp__"] == "2024-05-01T10:20:00Z"
    assert state["6418:2024-05-01T10:20:00Z"] == "2024-05-01T10:20:00Z"
    if transport == "mqtt":
        producer.connect.assert_awaited_once()
        producer.disconnect.assert_awaited_once()
    else:
        producer.close.assert_called_once()


@pytest.mark.parametrize("transport", ["mqtt", "amqp"])
@pytest.mark.parametrize("mock_mode", [False, True])
@pytest.mark.parametrize("family", ["station", "observation"])
def test_companion_publish_failure_propagates_and_closes_without_saving_state(monkeypatch, tmp_path, transport, mock_mode, family):
    emitted = []
    app, producer = _install_companion_producer(monkeypatch, transport, emitted)
    if not mock_mode:
        _install_live_api(monkeypatch, app)
    state_file = tmp_path / "live-state.json"
    state_file.write_text('{"preserved": true}', encoding="utf-8")
    method = (
        f"publish_be_gov_kmi_weather_mqtt_{'weather_observation' if family == 'observation' else family}"
        if transport == "mqtt" else
        f"send_{'weather_observation' if family == 'observation' else family}"
    )
    getattr(producer, method).side_effect = RuntimeError("publish failed")
    monkeypatch.setenv("KMI_BELGIUM_MOCK", "true" if mock_mode else "false")
    monkeypatch.setattr(sys, "argv", [f"kmi-belgium-{transport}", "feed", "--once", "--state-file", str(state_file)])

    with pytest.raises(RuntimeError, match="publish failed"):
        app.main()

    assert [name for name, _ in emitted] == ([] if family == "station" else ["station"])
    assert state_file.read_text(encoding="utf-8") == '{"preserved": true}'
    if transport == "mqtt":
        producer.connect.assert_awaited_once()
        producer.disconnect.assert_awaited_once()
    else:
        producer.close.assert_called_once()
