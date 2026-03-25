"""End-to-end tests for the SMHI Hydro bridge - hits the real API."""

import pytest
from smhi_hydro.smhi_hydro import SMHIHydroAPI


class TestSMHIHydroE2E:
    """End-to-end tests that use the real SMHI open data API."""

    @pytest.fixture
    def api(self):
        return SMHIHydroAPI()

    def test_get_bulk_discharge_data(self, api):
        """Test that we can fetch bulk discharge data."""
        data = api.get_bulk_discharge_data()
        assert isinstance(data, dict)
        assert "station" in data
        assert "parameter" in data
        assert len(data["station"]) > 100

    def test_parameter_is_discharge(self, api):
        """Test that the parameter is discharge (Vattenföring)."""
        data = api.get_bulk_discharge_data()
        assert data["parameter"]["key"] == "2"
        assert "m³/s" in data["parameter"]["unit"]

    def test_parse_all_stations(self, api):
        """Test that all station entries can be parsed into Station objects."""
        data = api.get_bulk_discharge_data()
        stations = [api.parse_station(s) for s in data["station"]]
        assert len(stations) == len(data["station"])
        for s in stations:
            assert s.station_id
            assert s.name

    def test_parse_observations(self, api):
        """Test parsing observations from bulk data."""
        data = api.get_bulk_discharge_data()
        observations = []
        for station_data in data["station"]:
            obs = api.parse_latest_observation(station_data)
            if obs:
                observations.append(obs)
        assert len(observations) > 50, f"Expected many observations, got {len(observations)}"

    def test_station_coordinates_sweden(self, api):
        """Test that station coordinates are reasonable for Sweden."""
        data = api.get_bulk_discharge_data()
        stations = [api.parse_station(s) for s in data["station"]]
        for s in stations:
            assert 55.0 <= s.latitude <= 70.0, f"Latitude {s.latitude} out of Sweden range for {s.name}"
            assert 10.0 <= s.longitude <= 25.0, f"Longitude {s.longitude} out of Sweden range for {s.name}"

    def test_multiple_catchments(self, api):
        """Test that data includes multiple catchment areas."""
        data = api.get_bulk_discharge_data()
        catchments = set(s.get("catchmentName", "") for s in data["station"] if s.get("catchmentName"))
        assert len(catchments) > 20, f"Expected many catchments, got {len(catchments)}"

    def test_unicode_station_names(self, api):
        """Test that Swedish unicode characters are handled correctly."""
        data = api.get_bulk_discharge_data()
        stations = [api.parse_station(s) for s in data["station"]]
        has_swedish_chars = any(
            any(c in s.name or c in s.catchment_name for c in 'åäöÅÄÖ') for s in stations
        )
        assert has_swedish_chars, "Expected some stations with Swedish diacritical characters"

    def test_discharge_values_reasonable(self, api):
        """Test that discharge values are within a reasonable range."""
        data = api.get_bulk_discharge_data()
        for station_data in data["station"]:
            obs = api.parse_latest_observation(station_data)
            if obs:
                assert obs.discharge >= 0.0, f"Negative discharge {obs.discharge} for {obs.station_name}"
                assert obs.discharge < 10000.0, f"Unreasonably high discharge {obs.discharge} for {obs.station_name}"

    def test_all_stations_have_owner(self, api):
        """Test that all stations have an owner field."""
        data = api.get_bulk_discharge_data()
        stations = [api.parse_station(s) for s in data["station"]]
        for s in stations:
            assert s.owner, f"Station {s.name} has no owner"

    def test_observation_timestamps_are_recent(self, api):
        """Test that observation timestamps are recent (within last day)."""
        from datetime import datetime, timezone, timedelta
        data = api.get_bulk_discharge_data()
        now = datetime.now(tz=timezone.utc)
        one_day_ago = now - timedelta(days=1)
        for station_data in data["station"]:
            obs = api.parse_latest_observation(station_data)
            if obs:
                ts = datetime.fromisoformat(obs.timestamp)
                assert ts > one_day_ago, f"Observation timestamp {obs.timestamp} is too old for {obs.station_name}"
