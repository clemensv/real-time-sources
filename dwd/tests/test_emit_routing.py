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

    def send_de_dwd_cdc_extreme_wind10_min(self, **_kw):
        self.calls.append("extreme_wind_10min")

    def send_de_dwd_cdc_extreme_temperature10_min(self, **_kw):
        self.calls.append("extreme_temperature_10min")


class FakeWeatherProducer:
    def __init__(self, *_args, **_kwargs):
        self.calls: List[str] = []

    def send_de_dwd_weather_alert(self, **_kw):
        self.calls.append("weather_alert")


class FakeRadarProducer:
    def __init__(self, *_args, **_kwargs):
        self.calls: List[str] = []

    def send_de_dwd_radar_radar_product_catalog(self, **_kw):
        self.calls.append("radar_product_catalog")

    def send_de_dwd_radar_radar_file_product(self, **_kw):
        self.calls.append("radar_file_product")


class FakeForecastProducer:
    def __init__(self, *_args, **_kwargs):
        self.calls: List[str] = []

    def send_de_dwd_forecast_forecast_model_catalog(self, **_kw):
        self.calls.append("forecast_model_catalog")

    def send_de_dwd_forecast_icon_d2_forecast_file(self, **_kw):
        self.calls.append("icon_d2_forecast_file")


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

_EXTREME_WIND_EVENT = {
    "type": "extreme_wind_10min",
    "data": {
        "station_id": "44",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "quality_level": 10,
        "wind_speed_maximum": 12.0,
        "wind_speed_minimum": 1.5,
        "wind_direction_at_maximum": 210.0,
    },
}

_EXTREME_TEMPERATURE_EVENT = {
    "type": "extreme_temperature_10min",
    "data": {
        "station_id": "44",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "quality_level": 10,
        "air_temperature_maximum_2m": 8.5,
        "air_temperature_minimum_5cm": -1.5,
    },
}

_RADAR_PRODUCT_CATALOG_EVENT = {
    "type": "radar_product_catalog",
    "data": {
        "file_path": "weather/radar/composite/ry",
        "product": "ry",
        "directory_path": "weather/radar/composite/ry",
        "description": "DWD radar product directory ry",
    },
}

_RADAR_FILE_EVENT = {
    "type": "radar_file_product",
    "data": {
        "file_path": "weather/radar/composite/ry/raa01-ry_10000-latest-dwd---bin",
        "product": "ry",
        "file_name": "raa01-ry_10000-latest-dwd---bin",
        "modified": "2026-01-01T00:00:00+00:00",
        "size_bytes": 1024,
        "download_url": "https://opendata.dwd.de/weather/radar/composite/ry/raa01-ry_10000-latest-dwd---bin",
    },
}

_FORECAST_MODEL_CATALOG_EVENT = {
    "type": "forecast_model_catalog",
    "data": {
        "file_path": "weather/nwp/icon-d2/grib",
        "model": "icon-d2",
        "base_path": "weather/nwp/icon-d2/grib",
        "description": "DWD ICON-D2 NWP model forecast feed from Open Data directories.",
    },
}

_ICON_D2_FILE_EVENT = {
    "type": "icon_d2_forecast_file",
    "data": {
        "file_path": "weather/nwp/icon-d2/grib/icon-d2_germany_regular-lat-lon_single-level_2026010100_000_T_2M.grib2.bz2",
        "model": "icon-d2",
        "file_name": "icon-d2_germany_regular-lat-lon_single-level_2026010100_000_T_2M.grib2.bz2",
        "run": "2026010100",
        "forecast_hour": 0,
        "parameter": "regular-lat-lon",
        "level_type": "single-level",
        "level": "2026010100",
        "modified": "2026-01-01T00:00:00+00:00",
        "size_bytes": 2048,
        "download_url": "https://opendata.dwd.de/weather/nwp/icon-d2/grib/icon-d2_germany_regular-lat-lon_single-level_2026010100_000_T_2M.grib2.bz2",
    },
}


# ---------------------------------------------------------------------------
# Tests: _emit_event dispatch routing
# ---------------------------------------------------------------------------

class TestEmitEventRouting:
    """_emit_event routes each event type to the correct generated producer class."""

    def _make(self):
        return FakeCDCProducer(), FakeWeatherProducer(), FakeRadarProducer(), FakeForecastProducer()

    def test_station_metadata_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _STATION_EVENT)
        assert cdc.calls == ["station_metadata"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_weather_alert_routed_to_weather(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _ALERT_EVENT)
        assert cdc.calls == []
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == ["weather_alert"]

    def test_both_families_in_one_logical_sequence(self):
        """Both producer classes are exercised when both event families are present."""
        cdc, wx, radar, forecast = self._make()
        for ev in [_STATION_EVENT, _ALERT_EVENT]:
            _emit_event(cdc, wx, radar, forecast, ev)
        assert "station_metadata" in cdc.calls
        assert "weather_alert" in wx.calls

    def test_air_temperature_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _AIR_TEMP_EVENT)
        assert cdc.calls == ["air_temperature_10min"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_precipitation_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _PRECIP_EVENT)
        assert cdc.calls == ["precipitation_10min"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_wind_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _WIND_EVENT)
        assert cdc.calls == ["wind_10min"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_solar_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _SOLAR_EVENT)
        assert cdc.calls == ["solar_10min"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_hourly_observation_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _HOURLY_EVENT)
        assert cdc.calls == ["hourly_observation"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_extreme_wind_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _EXTREME_WIND_EVENT)
        assert cdc.calls == ["extreme_wind_10min"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_extreme_temperature_routed_to_cdc(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _EXTREME_TEMPERATURE_EVENT)
        assert cdc.calls == ["extreme_temperature_10min"]
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_unknown_type_routed_to_neither(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, {"type": "unknown_type", "data": {}})
        assert cdc.calls == []
        assert radar.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_radar_types_routed_to_radar_producer(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _RADAR_PRODUCT_CATALOG_EVENT)
        _emit_event(cdc, wx, radar, forecast, _RADAR_FILE_EVENT)
        assert radar.calls == ["radar_product_catalog", "radar_file_product"]
        assert cdc.calls == []
        assert forecast.calls == []
        assert wx.calls == []

    def test_forecast_types_routed_to_forecast_producer(self):
        cdc, wx, radar, forecast = self._make()
        _emit_event(cdc, wx, radar, forecast, _FORECAST_MODEL_CATALOG_EVENT)
        _emit_event(cdc, wx, radar, forecast, _ICON_D2_FILE_EVENT)
        assert forecast.calls == ["forecast_model_catalog", "icon_d2_forecast_file"]
        assert cdc.calls == []
        assert radar.calls == []
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

        class FakeRadar:
            def __init__(self, *_a, **_kw):
                pass

            def send_de_dwd_radar_radar_product_catalog(self, **_kw):
                sent.append("radar:radar_product_catalog")

        class FakeForecast:
            def __init__(self, *_a, **_kw):
                pass

            def send_de_dwd_forecast_forecast_model_catalog(self, **_kw):
                sent.append("forecast:forecast_model_catalog")

        fake_kafka = MagicMock()
        modules = [
            _FakeModule("station_metadata", [_STATION_EVENT]),
            _FakeModule("weather_alerts", [_ALERT_EVENT]),
            _FakeModule("radar_products", [_RADAR_PRODUCT_CATALOG_EVENT]),
            _FakeModule("icon_d2_forecast", [_FORECAST_MODEL_CATALOG_EVENT]),
        ]

        with patch("dwd.dwd.Producer", return_value=fake_kafka), \
             patch("dwd.dwd.DEDWDCDCEventProducer", FakeCDC), \
             patch("dwd.dwd.DEDWDWeatherEventProducer", FakeWeather), \
             patch("dwd.dwd.DEDWDRadarEventProducer", FakeRadar), \
             patch("dwd.dwd.DEDWDForecastEventProducer", FakeForecast), \
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
        assert "radar:radar_product_catalog" in sent, "Radar producer was not called"
        assert "forecast:forecast_model_catalog" in sent, "Forecast producer was not called"
