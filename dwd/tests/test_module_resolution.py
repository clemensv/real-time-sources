"""Tests for module registry resolution in dwd.dwd."""

from dwd.dwd import _resolve_modules
from dwd.util.http_client import DWDHttpClient


def test_extreme_module_is_available_when_enabled():
    modules = _resolve_modules(
        http_client=DWDHttpClient(base_url="https://example.invalid"),
        enabled_csv="station_obs_10min_extremes",
        disabled_csv=None,
        ten_min_params=None,
        station_filter=None,
    )
    assert len(modules) == 1
    assert modules[0].name == "station_obs_10min_extremes"


def test_extreme_module_is_off_by_default():
    modules = _resolve_modules(
        http_client=DWDHttpClient(base_url="https://example.invalid"),
        enabled_csv=None,
        disabled_csv=None,
        ten_min_params=None,
        station_filter=None,
    )
    names = {m.name for m in modules}
    assert "station_obs_10min_extremes" not in names
