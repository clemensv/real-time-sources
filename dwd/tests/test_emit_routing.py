"""Tests that _emit_event and run_feed route events to the correct generated producer class.

DEDWDCDCEventProducer handles all climate data centre (CDC) families; DEDWDWeatherEventProducer
handles weather alerts.  This module verifies the dispatch layer routes both families and that
a single run_feed cycle instantiates and exercises both generated producer classes.
"""

import os
import tempfile
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from dwd.dwd import _emit_event, run_feed
from dwd.modules.base import BaseModule


# ---------------------------------------------------------------------------
# Minimal fake producer stubs — record which send method was called
# ---------------------------------------------------------------------------

class FakeCDCProducer:
    def __init__(self, *_args, **_kwargs):
        self.calls: List[str] = []

    def send_de_dwd_cdc_station_metadata(self, **_kw):
        self.calls.append("station_metadata")

    def send_de_dwd_cdc_air_temperature10_min(self, **_kw):
        self.calls.append("air_temperature_10min")

    def send_de_dwd_cdc_precipitation10_min(self, **_kw):
        self.calls.append("precipitation_10min")

    def send_de_dwd_cdc_wind10_min(self, **_kw):
        self.calls.append("wind_10min")

    def send_de_dwd_cdc_solar10_min(self, **_kw):
        self.calls.append("solar_10min")

    def send_de_dwd_cdc_hourly_observation(self, **_kw):
        self.calls.append("hourly_observation")


class FakeWeatherProducer:
    def __init__(self, *_args, **_kwargs):
        self.calls: List[str] = []

    def send_de_dwd_weather_alert(self, **_kw):
        self.calls.append("weather_alert")


# ---------------------------------------------------------------------------
# Fake BaseModule for run_feed wiring tests
# ---------------------------------------------------------------------------

class _FakeModule(BaseModule):
    def __init__(self, name_: str, events: List[Dict[str, Any]], *, enabled: bool = True):
        self._name = name_
        self._events = events
        self._enabled = enabled

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_enabled(self) -> bool:
        return self._enabled

    @property
    def default_poll_interval(self) -> int:
        return 3600

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self._events


# ---------------------------------------------------------------------------
# Representative event payloads (fields must match the generated data classes)
# ---------------------------------------------------------------------------

_STATION_EVENT = {
    "type": "station_metadata",
    "data": {
        "station_id": "44",
        "station_name": "Großenkneten",
        "latitude": 52.9336,
        "longitude": 8.2370,
        "elevation": 44.0,
        "state": "Niedersachsen",
        "from_date": "2007-02-09",
        "to_date": "2026-04-01",
    },
}

_ALERT_EVENT = {
    "type": "weather_alert",
    "data": {
        "identifier": "2.49.0.0.276.0.DWD.PVW.1234567890.1",
        "sender": "opendata@dwd.de",
        "sent": "2026-03-30T09:06:00+00:00",
        "status": "Actual",
        "msg_type": "Alert",
        "severity": "Moderate",
        "urgency": "Immediate",
        "certainty": "Likely",
        "event": "FROST",
        "headline": "Amtliche WARNUNG vor FROST",
        "description": "Es tritt mäßiger Frost auf.",
        "effective": "2026-03-30T18:00:00+01:00",
        "onset": "2026-03-30T20:00:00+01:00",
        "expires": "2026-03-31T10:00:00+01:00",
        "area_desc": "Kreis Ahrweiler",
        "geocodes": '{"WARNCELLID": "807131000"}',
    },
}

_AIR_TEMP_EVENT = {
    "type": "air_temperature_10min",
    "data": {
        "station_id": "44",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "quality_level": 10,
        "pressure_station_level": 1013.0,
        "air_temperature_2m": 5.0,
        "air_temperature_5cm": 4.5,
        "relative_humidity": 80.0,
        "dew_point_temperature": 2.0,
    },
}

_PRECIP_EVENT = {
    "type": "precipitation_10min",
    "data": {
        "station_id": "44",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "quality_level": 10,
        "precipitation_height": 0.0,
        "precipitation_indicator": 0,
    },
}

_WIND_EVENT = {
    "type": "wind_10min",
    "data": {
        "station_id": "44",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "quality_level": 10,
        "wind_speed": 3.0,
        "wind_direction": 180.0,
    },
}

_SOLAR_EVENT = {
    "type": "solar_10min",
    "data": {
        "station_id": "44",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "quality_level": 10,
        "global_radiation": 0.0,
        "sunshine_duration": 0.0,
        "diffuse_radiation": 0.0,
        "longwave_radiation": 0.0,
    },
}

_HOURLY_EVENT = {
    "type": "hourly_observation",
    "data": {
        "station_id": "44",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "quality_level": 10,
        "parameter": "air_temperature",
        "value": 5.0,
        "unit": "°C",
    },
}


# ---------------------------------------------------------------------------
# Tests: _emit_event dispatch routing
# ---------------------------------------------------------------------------

class TestEmitEventRouting:
    """_emit_event routes each event type to the correct generated producer class."""

    def _make(self):
        return FakeCDCProducer(), FakeWeatherProducer()

    def test_station_metadata_routed_to_cdc(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, _STATION_EVENT)
        assert cdc.calls == ["station_metadata"]
        assert wx.calls == []

    def test_weather_alert_routed_to_weather(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, _ALERT_EVENT)
        assert cdc.calls == []
        assert wx.calls == ["weather_alert"]

    def test_both_families_in_one_logical_sequence(self):
        """Both producer classes are exercised when both event families are present."""
        cdc, wx = self._make()
        for ev in [_STATION_EVENT, _ALERT_EVENT]:
            _emit_event(cdc, wx, ev)
        assert "station_metadata" in cdc.calls
        assert "weather_alert" in wx.calls

    def test_air_temperature_routed_to_cdc(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, _AIR_TEMP_EVENT)
        assert cdc.calls == ["air_temperature_10min"]
        assert wx.calls == []

    def test_precipitation_routed_to_cdc(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, _PRECIP_EVENT)
        assert cdc.calls == ["precipitation_10min"]
        assert wx.calls == []

    def test_wind_routed_to_cdc(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, _WIND_EVENT)
        assert cdc.calls == ["wind_10min"]
        assert wx.calls == []

    def test_solar_routed_to_cdc(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, _SOLAR_EVENT)
        assert cdc.calls == ["solar_10min"]
        assert wx.calls == []

    def test_hourly_observation_routed_to_cdc(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, _HOURLY_EVENT)
        assert cdc.calls == ["hourly_observation"]
        assert wx.calls == []

    def test_unknown_type_routed_to_neither(self):
        cdc, wx = self._make()
        _emit_event(cdc, wx, {"type": "unknown_type", "data": {}})
        assert cdc.calls == []
        assert wx.calls == []


# ---------------------------------------------------------------------------
# Test: run_feed one-cycle wiring — both generated producer classes used
# ---------------------------------------------------------------------------

class TestRunFeedDualProducerWiring:
    """run_feed creates and exercises both DEDWDCDCEventProducer and
    DEDWDWeatherEventProducer in a single polling cycle."""

    def test_one_cycle_exercises_both_producer_classes(self):
        sent = []

        class FakeCDC:
            def __init__(self, *_a, **_kw):
                pass

            def send_de_dwd_cdc_station_metadata(self, **_kw):
                sent.append("cdc:station_metadata")

        class FakeWeather:
            def __init__(self, *_a, **_kw):
                pass

            def send_de_dwd_weather_alert(self, **_kw):
                sent.append("weather:weather_alert")

        fake_kafka = MagicMock()
        modules = [
            _FakeModule("station_metadata", [_STATION_EVENT]),
            _FakeModule("weather_alerts", [_ALERT_EVENT]),
        ]

        with patch("dwd.dwd.Producer", return_value=fake_kafka), \
             patch("dwd.dwd.DEDWDCDCEventProducer", FakeCDC), \
             patch("dwd.dwd.DEDWDWeatherEventProducer", FakeWeather), \
             patch("dwd.dwd.load_state", return_value={}), \
             patch("dwd.dwd.save_state"), \
             patch("dwd.dwd.time.sleep", side_effect=KeyboardInterrupt):
            run_feed(
                kafka_config={"bootstrap.servers": "localhost:9092"},
                kafka_topic="test-topic",
                polling_interval=None,
                state_file="",
                modules=modules,
            )

        assert "cdc:station_metadata" in sent, "CDC producer was not called"
        assert "weather:weather_alert" in sent, "Weather producer was not called"
