from datetime import datetime, timezone

from dwd.modules.icon_d2_forecast import IconD2ForecastModule
from dwd.modules.radar_products import RadarProductsModule
from dwd.util.http_client import DirEntry


class _FakeHttpClient:
    def __init__(self, listings):
        self.base_url = "https://opendata.dwd.de"
        self._listings = listings

    def list_directory(self, path):
        return self._listings.get(path, [])


def _entry(name: str, size: str = "1K"):
    return DirEntry(name=name, modified=datetime(2026, 1, 1, tzinfo=timezone.utc), size_str=size)


def test_radar_module_emits_catalog_and_file_events():
    client = _FakeHttpClient({
        "weather/radar/composite/": [_entry("ry/")],
        "weather/radar/composite/ry/": [_entry("radar.bin", "2K")],
    })
    module = RadarProductsModule(client)
    state = {}

    events = module.poll(state)
    types = {e["type"] for e in events}

    assert "radar_product_catalog" in types
    assert "radar_file_product" in types


def test_icon_d2_module_emits_catalog_and_file_events():
    client = _FakeHttpClient({
        "weather/nwp/icon-d2/grib/": [_entry("icon-d2_germany_regular-lat-lon_single-level_2026010100_000_T_2M.grib2.bz2", "3K")],
    })
    module = IconD2ForecastModule(client)
    state = {}

    events = module.poll(state)
    types = {e["type"] for e in events}

    assert "forecast_model_catalog" in types
    assert "icon_d2_forecast_file" in types
