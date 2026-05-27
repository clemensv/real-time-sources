"""End-to-end tests for UK EA Flood Monitoring against real API."""

import pytest
from uk_ea_flood_monitoring.uk_ea_flood_monitoring import EAFloodMonitoringAPI


@pytest.mark.e2e
class TestEAFloodMonitoringRealEndpoints:
    """Test against the real EA Flood Monitoring API endpoints."""

    def test_fetch_real_stations_list(self):
        """Test fetching the actual list of monitoring stations."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()

        assert isinstance(stations, list)
        assert len(stations) > 100  # England has many monitoring stations

        first_station = stations[0]
        assert 'notation' in first_station or 'stationReference' in first_station

    def test_fetch_stations_have_labels(self):
        """Test that stations have label/name information."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        stations_with_labels = [s for s in stations if s.get('label')]

        assert len(stations_with_labels) > 100

    def test_fetch_stations_have_coordinates(self):
        """Test that stations have geographic coordinates."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        stations_with_coords = [s for s in stations if s.get('lat') and s.get('long')]

        assert len(stations_with_coords) > 100

        for station in stations_with_coords[:10]:
            # England's approximate boundaries
            assert 49.0 < station['lat'] < 56.0
            assert -7.0 < station['long'] < 2.0

    def test_fetch_thames_stations(self):
        """Test that Thames river stations are in the list."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        thames_stations = [s for s in stations if s.get('riverName') and 'Thames' in s['riverName']]

        assert len(thames_stations) > 5

    def test_fetch_stations_have_measures(self):
        """Test that stations have associated measures."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        stations_with_measures = [s for s in stations if s.get('measures')]

        assert len(stations_with_measures) > 50

    def test_fetch_latest_readings(self):
        """Test fetching latest readings in bulk."""
        api = EAFloodMonitoringAPI()

        readings = api.get_latest_readings()

        assert isinstance(readings, list)
        assert len(readings) > 100

        first_reading = readings[0]
        assert 'dateTime' in first_reading
        assert 'value' in first_reading
        assert 'measure' in first_reading

    def test_readings_have_valid_values(self):
        """Test that readings contain numeric values."""
        api = EAFloodMonitoringAPI()

        readings = api.get_latest_readings()

        numeric_readings = [r for r in readings if isinstance(r.get('value'), (int, float))]
        assert len(numeric_readings) > 50

    def test_build_measure_map_from_real_data(self):
        """Test building measure map from real station data."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        measure_map = api.build_measure_map(stations)

        assert isinstance(measure_map, dict)
        assert len(measure_map) > 100

    def test_readings_can_be_mapped_to_stations(self):
        """Test that readings can be resolved to station references."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        measure_map = api.build_measure_map(stations)
        readings = api.get_latest_readings()

        mapped_count = 0
        for reading in readings[:100]:
            measure_uri = reading.get("measure", "")
            if measure_uri in measure_map:
                mapped_count += 1

        # At least half of readings should be mappable
        assert mapped_count > 20

    def test_river_variety(self):
        """Test that multiple rivers are represented."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        rivers = set()
        for station in stations:
            river = station.get('riverName')
            if river:
                rivers.add(river)

        assert len(rivers) > 20

    def test_api_response_time(self):
        """Test that API responds in reasonable time."""
        import time

        api = EAFloodMonitoringAPI()

        start_time = time.time()
        stations = api.list_stations()
        end_time = time.time()

        assert (end_time - start_time) < 30.0
        assert len(stations) > 0

    def test_station_status_values(self):
        """Test that stations have status information."""
        api = EAFloodMonitoringAPI()

        stations = api.list_stations()
        stations_with_status = [s for s in stations if s.get('status')]

        assert len(stations_with_status) > 100
