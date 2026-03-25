"""
End-to-end tests for NOAA NDBC Buoy Observations poller.
Tests against the actual NDBC API endpoints.

Run with: pytest tests/test_noaa_ndbc_e2e.py -v -m e2e
Skip in CI: pytest tests/ -v -m "not e2e"
"""

import pytest
import requests


NDBC_LATEST_OBS_URL = "https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt"


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
