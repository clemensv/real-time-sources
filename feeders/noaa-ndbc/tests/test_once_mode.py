"""Tests for --once single-cycle exit, used by the Fabric notebook hosting path."""

import sys
from unittest.mock import MagicMock, patch

import pytest

import noaa_ndbc.noaa_ndbc as bridge  # noqa: F401  (ensure submodule import for patch())


@pytest.fixture
def fake_producer():
    producer = MagicMock()
    producer.producer = MagicMock()
    return producer


def _run_main_with_once(monkeypatch, fake_producer, argv):
    monkeypatch.setattr(sys, "argv", argv)

    with patch(
        "noaa_ndbc.noaa_ndbc.MicrosoftOpenDataUSNOAANDBCEventProducer",
        return_value=fake_producer,
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.fetch_stations", return_value=[]
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_observations", return_value=[]
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.fetch_realtime2_file_index",
        return_value={},
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_solar_radiation_observations",
        return_value=[],
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_oceanographic_observations",
        return_value=[],
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_dart_measurements", return_value=[]
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_continuous_wind_observations",
        return_value=[],
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_supplemental_measurements",
        return_value=[],
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_detailed_wave_summaries",
        return_value=[],
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.poll_hourly_rain_measurements",
        return_value=[],
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.load_state", return_value={}
    ), patch(
        "noaa_ndbc.noaa_ndbc.NDBCBuoyPoller.save_state"
    ), patch(
        "noaa_ndbc.noaa_ndbc.time.sleep"
    ) as sleep_mock:
        from noaa_ndbc.noaa_ndbc import main
        main()
    return sleep_mock


def test_once_flag_exits_after_one_cycle(monkeypatch, fake_producer):
    sleep_mock = _run_main_with_once(
        monkeypatch,
        fake_producer,
        [
            "noaa-ndbc",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=test-topic",
            "--once",
        ],
    )
    # Single-cycle exit must NOT sleep at the end of the loop.
    sleep_mock.assert_not_called()


def test_once_env_var_exits_after_one_cycle(monkeypatch, fake_producer):
    monkeypatch.setenv("ONCE_MODE", "true")
    sleep_mock = _run_main_with_once(
        monkeypatch,
        fake_producer,
        [
            "noaa-ndbc",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=test-topic",
        ],
    )
    sleep_mock.assert_not_called()
