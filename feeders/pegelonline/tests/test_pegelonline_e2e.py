"""End-to-end tests for the pegelonline core against the real PegelOnline API."""

import pytest

from pegelonline_core import PegelOnlineAPI


@pytest.mark.e2e
class TestPegelOnlineAPIRealEndpoints:
    def test_fetch_real_stations_list(self):
        api = PegelOnlineAPI()
        stations = api.list_stations()
        assert isinstance(stations, list)
        assert len(stations) > 100
        first = stations[0]
        assert {"uuid", "shortname", "longname", "water"}.issubset(first)
        assert "shortname" in first["water"]

    def test_fetch_rhine_stations(self):
        api = PegelOnlineAPI()
        stations = api.list_stations()
        rhine = [s for s in stations if (s.get("water") or {}).get("shortname") == "RHEIN"]
        assert len(rhine) > 10

    def test_get_water_levels_real(self):
        api = PegelOnlineAPI()
        levels = api.get_water_levels()
        assert isinstance(levels, dict)
        assert len(levels) > 50
        first_id = next(iter(levels))
        measurement = levels[first_id]
        assert "timestamp" in measurement
        assert "value" in measurement
