"""
Test that --once causes poll_and_send() to return after exactly one cycle.
"""

import os
from unittest.mock import patch, MagicMock

from aviationweather.aviationweather import AviationWeatherPoller


def _make_poller(tmp_path):
    state_file = tmp_path / "state.json"
    with patch("confluent_kafka.Producer") as mock_kp, \
         patch("aviationweather.aviationweather.GovNoaaAviationweatherEventProducer") as mock_evt:
        mock_evt.return_value = MagicMock(producer=MagicMock())
        poller = AviationWeatherPoller(
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="test-topic",
            last_polled_file=str(state_file),
            station_ids="KJFK",
            metar_poll_interval=900,
            sigmet_poll_interval=900,
        )
    return poller


def test_poll_and_send_once_exits_after_single_cycle(tmp_path):
    poller = _make_poller(tmp_path)

    with patch.object(poller, "emit_stations", return_value=1) as m_st, \
         patch.object(poller, "emit_metars", return_value=(0, {})) as m_metar, \
         patch.object(poller, "emit_sigmets", return_value=(0, set())) as m_sigmet, \
         patch("aviationweather.aviationweather.time.sleep") as m_sleep:
        poller.poll_and_send(once=True)

    assert m_metar.call_count == 1, "METAR poll must run exactly once"
    assert m_sigmet.call_count == 1, "SIGMET poll must run exactly once"
    assert m_sleep.call_count == 0, "Must not sleep when --once is set"
    assert m_st.call_count >= 1, "Station reference data must be emitted at startup"


def test_main_parses_once_flag(monkeypatch, tmp_path):
    monkeypatch.setenv("CONNECTION_STRING",
                       "BootstrapServer=localhost:9092;EntityPath=test-topic")
    monkeypatch.setenv("AVIATIONWEATHER_LAST_POLLED_FILE", str(tmp_path / "s.json"))
    monkeypatch.setattr("sys.argv", ["aviationweather", "--once"])

    captured = {}

    def fake_init(self, **kwargs):
        captured["init"] = kwargs

    def fake_poll(self, once=False):
        captured["once"] = once

    with patch.object(AviationWeatherPoller, "__init__", fake_init), \
         patch.object(AviationWeatherPoller, "poll_and_send", fake_poll):
        from aviationweather.aviationweather import main
        main()

    assert captured.get("once") is True


def test_main_once_via_env(monkeypatch, tmp_path):
    monkeypatch.setenv("CONNECTION_STRING",
                       "BootstrapServer=localhost:9092;EntityPath=test-topic")
    monkeypatch.setenv("AVIATIONWEATHER_LAST_POLLED_FILE", str(tmp_path / "s.json"))
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr("sys.argv", ["aviationweather"])

    captured = {}

    def fake_init(self, **kwargs):
        pass

    def fake_poll(self, once=False):
        captured["once"] = once

    with patch.object(AviationWeatherPoller, "__init__", fake_init), \
         patch.object(AviationWeatherPoller, "poll_and_send", fake_poll):
        from aviationweather.aviationweather import main
        main()

    assert captured.get("once") is True
