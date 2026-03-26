"""
End-to-end tests for NOAA NDBC Buoy Observations poller.
Tests against the actual NDBC API endpoints.

Run with: pytest tests/test_noaa_ndbc_e2e.py -v -m e2e
Skip in CI: pytest tests/ -v -m "not e2e"
"""

import pytest
import requests


NDBC_LATEST_OBS_URL = "https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt"
NDBC_STATION_TABLE_URL = "https://www.ndbc.noaa.gov/data/stations/station_table.txt"


@pytest.mark.e2e
@pytest.mark.slow
class TestNDBCE2E:
    """End-to-end tests against the actual NDBC API"""

    def test_fetch_latest_observations(self):
        """Test fetching latest observations from the real NDBC endpoint"""
        response = requests.get(NDBC_LATEST_OBS_URL, timeout=60)
        assert response.status_code == 200, f"NDBC API returned status {response.status_code}"
        assert len(response.text) > 0, "Response body is empty"

    def test_response_is_text(self):
        """Test that the response is text format"""
        response = requests.get(NDBC_LATEST_OBS_URL, timeout=60)
        assert response.status_code == 200
        # The response should be plain text
        content_type = response.headers.get('Content-Type', '')
        assert 'text' in content_type.lower() or len(response.text) > 100

    def test_response_has_header_lines(self):
        """Test that the response starts with header lines"""
        response = requests.get(NDBC_LATEST_OBS_URL, timeout=60)
        assert response.status_code == 200

        lines = response.text.strip().split('\n')
        assert len(lines) >= 3, "Expected at least 3 lines (2 headers + 1 data)"

        # First header line should start with #STN or similar
        assert lines[0].startswith('#'), f"First line doesn't start with #: {lines[0][:50]}"

    def test_at_least_some_stations(self):
        """Test that at least some stations are returned"""
        response = requests.get(NDBC_LATEST_OBS_URL, timeout=60)
        assert response.status_code == 200

        lines = response.text.strip().split('\n')
        data_lines = [l for l in lines[2:] if l.strip()]
        assert len(data_lines) > 10, f"Expected more than 10 stations, got {len(data_lines)}"

    def test_parse_real_response(self):
        """Test parsing the actual NDBC response"""
        response = requests.get(NDBC_LATEST_OBS_URL, timeout=60)
        assert response.status_code == 200

        # Import and test with the real parser
        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller
        observations = NDBCBuoyPoller.parse_observations(None, response.text)

        assert len(observations) > 10, f"Expected more than 10 observations, got {len(observations)}"

        # Verify first observation has required fields
        obs = observations[0]
        assert obs.station_id is not None and obs.station_id != ""
        assert obs.latitude != 0.0 or obs.longitude != 0.0
        assert obs.timestamp is not None and obs.timestamp != ""

    def test_station_ids_are_strings(self):
        """Test that station IDs are non-empty strings"""
        response = requests.get(NDBC_LATEST_OBS_URL, timeout=60)
        assert response.status_code == 200

        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller
        observations = NDBCBuoyPoller.parse_observations(None, response.text)

        for obs in observations[:20]:
            assert isinstance(obs.station_id, str)
            assert len(obs.station_id) > 0

    def test_coordinates_in_valid_range(self):
        """Test that coordinates are in valid lat/lon ranges"""
        response = requests.get(NDBC_LATEST_OBS_URL, timeout=60)
        assert response.status_code == 200

        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller
        observations = NDBCBuoyPoller.parse_observations(None, response.text)

        for obs in observations[:50]:
            assert -90 <= obs.latitude <= 90, f"Invalid latitude {obs.latitude} for station {obs.station_id}"
            assert -180 <= obs.longitude <= 180, f"Invalid longitude {obs.longitude} for station {obs.station_id}"

    def test_fetch_stations_from_real_api(self):
        """Test fetching the real station table and parsing it"""
        response = requests.get(NDBC_STATION_TABLE_URL, timeout=60)
        assert response.status_code == 200, f"NDBC station table API returned status {response.status_code}"

        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller
        poller_cls = NDBCBuoyPoller

        # Parse the raw text ourselves to verify structure
        lines = response.text.strip().split('\n')
        data_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        assert len(data_lines) > 100, f"Expected more than 100 stations, got {len(data_lines)}"

        # Use a mock poller just to call the static parse method
        for line in data_lines[:5]:
            fields = [f.strip() for f in line.split('|')]
            assert len(fields) >= 6, f"Expected at least 6 pipe-delimited fields, got {len(fields)}: {line[:80]}"
            assert len(fields[0]) > 0, "Station ID should not be empty"

    def test_parse_station_location_from_real_data(self):
        """Test parsing lat/lon from real station table LOCATION fields"""
        response = requests.get(NDBC_STATION_TABLE_URL, timeout=60)
        assert response.status_code == 200

        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller

        lines = response.text.strip().split('\n')
        data_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]

        parsed_count = 0
        for line in data_lines[:50]:
            fields = [f.strip() for f in line.split('|')]
            if len(fields) > 6 and fields[6].strip():
                lat, lon = NDBCBuoyPoller.parse_station_location(fields[6])
                if lat is not None and lon is not None:
                    assert -90 <= lat <= 90, f"Invalid latitude {lat}"
                    assert -180 <= lon <= 180, f"Invalid longitude {lon}"
                    parsed_count += 1

        assert parsed_count > 10, f"Expected to parse lat/lon for at least 10 stations, got {parsed_count}"
