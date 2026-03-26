"""End-to-end tests for the IMGW Hydro bridge - hits the real API."""

import pytest
from imgw_hydro.imgw_hydro import IMGWHydroAPI


class TestIMGWHydroE2E:
    """End-to-end tests that use the real IMGW API."""

    @pytest.fixture
    def api(self):
        return IMGWHydroAPI()

    def test_get_all_data(self, api):
        """Test that we can fetch all station data."""
        records = api.get_all_data()
        assert isinstance(records, list)
        assert len(records) > 100  # IMGW has hundreds of stations
        record = records[0]
        assert "id_stacji" in record
        assert "stacja" in record
        assert "rzeka" in record

    def test_parse_all_stations(self, api):
        """Test that all records can be parsed into Station objects."""
        records = api.get_all_data()
        stations = [api.parse_station(r) for r in records]
        assert len(stations) == len(records)
        for s in stations:
            assert s.id_stacji
            assert s.stacja

    def test_parse_all_observations(self, api):
        """Test that records can be parsed into observations."""
        records = api.get_all_data()
        observations = [api.parse_observation(r) for r in records]
        valid_obs = [o for o in observations if o is not None]
        assert len(valid_obs) > 50  # Most stations should have water level data

    def test_get_station_data(self, api):
        """Test fetching data for a specific station."""
        records = api.get_all_data()
        station_id = records[0]["id_stacji"]
        result = api.get_station_data(station_id)
        if isinstance(result, list):
            result = result[0]
        assert result["id_stacji"] == station_id

    def test_station_fields_present(self, api):
        """Test that expected fields are present in API responses."""
        records = api.get_all_data()
        for record in records[:10]:
            assert "id_stacji" in record
            assert "stacja" in record
            assert "rzeka" in record
            assert "stan_wody" in record or record.get("stan_wody") is None

    def test_observation_water_level_numeric(self, api):
        """Test that water levels parse to valid numbers."""
        records = api.get_all_data()
        for record in records:
            obs = api.parse_observation(record)
            if obs:
                assert isinstance(obs.water_level, float)
                assert obs.water_level >= -1000  # reasonable bounds

    def test_station_coordinates(self, api):
        """Test that station coordinates are reasonable for Poland."""
        records = api.get_all_data()
        stations_with_coords = [api.parse_station(r) for r in records if r.get("lon") and r.get("lat")]
        assert len(stations_with_coords) > 50
        for s in stations_with_coords:
            assert 14.0 <= s.longitude <= 25.0, f"Longitude {s.longitude} out of Poland range for {s.stacja}"
            assert 49.0 <= s.latitude <= 55.0, f"Latitude {s.latitude} out of Poland range for {s.stacja}"

    def test_unicode_station_names(self, api):
        """Test that Polish unicode characters are handled correctly."""
        records = api.get_all_data()
        stations = [api.parse_station(r) for r in records]
        # At least some stations should have Polish diacritics
        has_polish_chars = any(
            any(c in s.stacja for c in 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ') for s in stations
        )
        assert has_polish_chars, "Expected some stations with Polish diacritical characters"

    def test_multiple_rivers(self, api):
        """Test that data includes multiple rivers."""
        records = api.get_all_data()
        rivers = set(r.get("rzeka", "") for r in records if r.get("rzeka"))
        assert len(rivers) > 20, f"Expected many rivers, got {len(rivers)}"
