"""End-to-end tests for the ČHMÚ Hydro bridge - hits the real API."""

import pytest
from chmi_hydro.chmi_hydro import CHMIHydroAPI


class TestCHMIHydroE2E:
    """End-to-end tests that use the real ČHMÚ open data API."""

    @pytest.fixture
    def api(self):
        return CHMIHydroAPI()

    def test_get_metadata(self, api):
        """Test that we can fetch station metadata."""
        metadata = api.get_metadata()
        assert isinstance(metadata, list)
        assert len(metadata) > 100  # ČHMÚ has hundreds of stations

    def test_parse_all_stations(self, api):
        """Test that all metadata records can be parsed into Station objects."""
        metadata = api.get_metadata()
        stations = [api.parse_station(r) for r in metadata]
        assert len(stations) == len(metadata)
        for s in stations:
            assert s.station_id
            assert s.station_name

    def test_get_station_data(self, api):
        """Test fetching data for a specific station."""
        metadata = api.get_metadata()
        station_id = metadata[0][0]
        data = api.get_station_data(station_id)
        assert data is not None
        assert "objList" in data
        assert len(data["objList"]) > 0

    def test_parse_observation(self, api):
        """Test parsing observation data from a station."""
        metadata = api.get_metadata()
        station_id = metadata[0][0]
        station_name = metadata[0][2]
        stream_name = metadata[0][3] or ""
        data = api.get_station_data(station_id)
        assert data is not None
        obs = api.parse_observation(station_id, station_name, stream_name, data)
        assert obs is not None
        assert obs.station_id == station_id

    def test_station_coordinates(self, api):
        """Test that station coordinates are reasonable for Czech Republic."""
        metadata = api.get_metadata()
        stations = [api.parse_station(r) for r in metadata if r[4] is not None and r[5] is not None]
        assert len(stations) > 50
        for s in stations:
            if s.latitude != 0.0 and s.longitude != 0.0:
                assert 48.0 <= s.latitude <= 52.0, f"Latitude {s.latitude} out of Czech range for {s.station_name}"
                assert 12.0 <= s.longitude <= 19.0, f"Longitude {s.longitude} out of Czech range for {s.station_name}"

    def test_multiple_streams(self, api):
        """Test that data includes multiple rivers/streams."""
        metadata = api.get_metadata()
        streams = set(r[3] for r in metadata if r[3])
        assert len(streams) > 20, f"Expected many rivers, got {len(streams)}"

    def test_unicode_station_names(self, api):
        """Test that Czech unicode characters are handled correctly."""
        metadata = api.get_metadata()
        stations = [api.parse_station(r) for r in metadata]
        has_czech_chars = any(
            any(c in s.station_name for c in 'áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ') for s in stations
        )
        assert has_czech_chars, "Expected some stations with Czech diacritical characters"

    def test_flood_levels_present(self, api):
        """Test that some stations have flood warning levels."""
        metadata = api.get_metadata()
        stations = [api.parse_station(r) for r in metadata]
        stations_with_floods = [s for s in stations if s.flood_level_1 is not None]
        assert len(stations_with_floods) > 50, "Expected many stations with flood warning levels"

    def test_fetch_multiple_stations(self, api):
        """Test fetching data for multiple stations concurrently."""
        metadata = api.get_metadata()
        station_ids = [r[0] for r in metadata[:5]]
        results = api.get_all_station_data(station_ids)
        assert len(results) > 0
        for sid, data in results.items():
            assert "objList" in data
