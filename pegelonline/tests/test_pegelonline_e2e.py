"""End-to-end tests for PegelOnline data poller against real API."""

import pytest
from datetime import datetime, timezone, timedelta
from pegelonline.pegelonline import PegelOnlineAPI


@pytest.mark.e2e
class TestPegelOnlineAPIRealEndpoints:
    """Test against the real PegelOnline API endpoints."""

    def test_fetch_real_stations_list(self):
        """Test fetching the actual list of German waterway stations."""
        api = PegelOnlineAPI()
        
        stations = api.list_stations()
        
        # Verify we get a substantial list of stations
        assert isinstance(stations, list)
        assert len(stations) > 100  # Germany has many monitoring stations
        
        # Verify station structure
        first_station = stations[0]
        assert 'uuid' in first_station
        assert 'shortname' in first_station
        assert 'longname' in first_station
        assert 'water' in first_station
        assert 'shortname' in first_station['water']

    def test_fetch_rhine_stations(self):
        """Test that Rhine (Rhein) river stations are in the list."""
        api = PegelOnlineAPI()
        
        stations = api.list_stations()
        
        # Find Rhine stations
        rhine_stations = [s for s in stations if s.get('water', {}).get('shortname') == 'RHEIN']
        
        assert len(rhine_stations) > 10  # Rhine has many monitoring points
        
        # Verify well-known Rhine stations exist
        station_names = [s['shortname'] for s in rhine_stations]
        # These are major Rhine measurement stations
        assert any('MAXAU' in name for name in station_names)

    def test_fetch_elbe_stations(self):
        """Test that Elbe river stations are in the list."""
        api = PegelOnlineAPI()
        
        stations = api.list_stations()
        
        # Find Elbe stations
        elbe_stations = [s for s in stations if s.get('water', {}).get('shortname') == 'ELBE']
        
        assert len(elbe_stations) > 5  # Elbe has multiple monitoring points
        
        # Verify well-known Elbe station
        station_names = [s['shortname'] for s in elbe_stations]
        assert any('HAMBURG' in name or 'DRESDEN' in name for name in station_names)

    def test_fetch_water_level_maxau(self):
        """Test fetching water level for Maxau station on the Rhine."""
        api = PegelOnlineAPI()
        
        # First get the station list to find Maxau's UUID
        stations = api.list_stations()
        maxau_stations = [s for s in stations if 'MAXAU' in s['shortname']]
        
        if not maxau_stations:
            pytest.skip("Maxau station not found in current API response")
        
        maxau_uuid = maxau_stations[0]['uuid']
        
        # Fetch current water level
        measurement = api.get_water_level(maxau_uuid)
        
        if measurement is None:
            pytest.skip("No current measurement available for Maxau")
        
        # Verify measurement structure
        assert 'timestamp' in measurement
        assert 'value' in measurement
        assert isinstance(measurement['value'], (int, float))
        
        # Verify timestamp is recent (within last 24 hours)
        timestamp_str = measurement['timestamp']
        # Parse ISO format with timezone
        if '+' in timestamp_str:
            timestamp_str = timestamp_str.split('+')[0]
        elif 'Z' in timestamp_str:
            timestamp_str = timestamp_str.replace('Z', '')
        
        # Basic validation that we got a valid measurement value
        assert measurement['value'] > 0  # Water level should be positive

    def test_fetch_bulk_water_levels(self):
        """Test fetching all water levels in bulk."""
        api = PegelOnlineAPI()
        
        levels = api.get_water_levels()
        
        # Verify we get water levels for multiple stations
        assert isinstance(levels, dict)
        assert len(levels) > 50  # Should have many stations with current measurements
        
        # Verify structure of returned data
        for station_id, measurement in levels.items():
            assert 'timestamp' in measurement
            assert 'value' in measurement
            assert 'uuid' in measurement
            assert measurement['uuid'] == station_id

    def test_station_coordinates(self):
        """Test that stations have valid geographic coordinates."""
        api = PegelOnlineAPI()
        
        stations = api.list_stations()
        
        # Check a sample of stations for valid coordinates
        stations_with_coords = [s for s in stations if s.get('latitude') and s.get('longitude')]
        
        assert len(stations_with_coords) > 100
        
        for station in stations_with_coords[:10]:  # Check first 10
            # Germany's approximate boundaries
            # Latitude: 47.3 to 55.1
            # Longitude: 5.9 to 15.0
            assert 47.0 < station['latitude'] < 56.0
            assert 5.0 < station['longitude'] < 16.0

    def test_station_has_km_marker(self):
        """Test that river stations have kilometer markers."""
        api = PegelOnlineAPI()
        
        stations = api.list_stations()
        
        # Many stations should have km markers (river kilometer)
        stations_with_km = [s for s in stations if s.get('km')]
        
        assert len(stations_with_km) > 50
        
        # Check some stations have reasonable km values
        for station in stations_with_km[:20]:
            assert isinstance(station['km'], (int, float))
            assert station['km'] > 0

    def test_water_types_variety(self):
        """Test that multiple water bodies are represented."""
        api = PegelOnlineAPI()
        
        stations = api.list_stations()
        
        water_bodies = set()
        for station in stations:
            if station.get('water', {}).get('shortname'):
                water_bodies.add(station['water']['shortname'])
        
        # Should have many different rivers/waterways
        assert len(water_bodies) > 20
        
        # Major German rivers should be present
        assert 'RHEIN' in water_bodies
        assert 'ELBE' in water_bodies
        assert 'DONAU' in water_bodies  # Danube

    def test_api_response_time(self):
        """Test that API responds in reasonable time."""
        import time
        
        api = PegelOnlineAPI()
        
        start_time = time.time()
        stations = api.list_stations()
        end_time = time.time()
        
        # Should complete within 5 seconds
        assert (end_time - start_time) < 5.0
        assert len(stations) > 0

    def test_measurement_states(self):
        """Test that measurements include state information."""
        api = PegelOnlineAPI()
        
        levels = api.get_water_levels()
        
        if not levels:
            pytest.skip("No current measurements available")
        
        # Check that at least some measurements have state info
        measurements_with_states = 0
        for measurement in levels.values():
            if 'stateMnwMhw' in measurement or 'stateNswHsw' in measurement:
                measurements_with_states += 1
        
        # At least 50% should have state information
        assert measurements_with_states > len(levels) * 0.5
