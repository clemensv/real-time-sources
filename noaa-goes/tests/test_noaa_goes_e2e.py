"""
End-to-end tests for NOAA SWPC Space Weather poller.
Tests against the actual SWPC API endpoints.

Run with: pytest tests/test_noaa_goes_e2e.py -v -m e2e
Skip in CI: pytest tests/ -v -m "not e2e"
"""

import pytest
import requests


SWPC_ALERTS_URL = "https://services.swpc.noaa.gov/products/alerts.json"
SWPC_K_INDEX_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
SWPC_SOLAR_WIND_SPEED_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json"
SWPC_SOLAR_WIND_MAG_FIELD_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json"


@pytest.mark.e2e
@pytest.mark.slow
class TestSWPCE2E:
    """End-to-end tests against the actual SWPC API"""

    def test_fetch_alerts(self):
        """Test fetching alerts from the real SWPC API"""
        response = requests.get(SWPC_ALERTS_URL, timeout=30)
        assert response.status_code == 200, f"SWPC alerts API returned status {response.status_code}"

        data = response.json()
        assert isinstance(data, list), "Response is not a list"

    def test_alerts_response_structure(self):
        """Test that alert entries have the expected structure"""
        response = requests.get(SWPC_ALERTS_URL, timeout=30)
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        if len(data) == 0:
            pytest.skip("No alerts available at this time")

        alert = data[0]
        assert "product_id" in alert, "Alert missing 'product_id' field"
        assert "issue_datetime" in alert, "Alert missing 'issue_datetime' field"
        assert "message" in alert, "Alert missing 'message' field"

    def test_fetch_k_index(self):
        """Test fetching K-index data from the real SWPC API"""
        response = requests.get(SWPC_K_INDEX_URL, timeout=30)
        assert response.status_code == 200, f"SWPC K-index API returned status {response.status_code}"

        data = response.json()
        assert isinstance(data, list), "Response is not a list"
        assert len(data) > 1, "Response should have header + data rows"

    def test_k_index_response_structure(self):
        """Test that K-index data has the expected array structure"""
        response = requests.get(SWPC_K_INDEX_URL, timeout=30)
        assert response.status_code == 200

        data = response.json()
        # First row is the header
        header = data[0]
        assert isinstance(header, list), "Header row is not a list"

        if len(data) < 2:
            pytest.skip("No K-index data rows available")

        row = data[1]
        assert isinstance(row, list), "Data row is not a list"
        assert len(row) >= 4, f"Data row has {len(row)} elements, expected at least 4"

    def test_fetch_solar_wind_speed(self):
        """Test fetching solar wind speed from the real SWPC API"""
        response = requests.get(SWPC_SOLAR_WIND_SPEED_URL, timeout=30)
        assert response.status_code == 200, f"SWPC solar wind speed API returned status {response.status_code}"

        data = response.json()
        assert isinstance(data, dict), "Response is not a dict"
        assert "WindSpeed" in data, "Response missing 'WindSpeed' field"
        assert "TimeStamp" in data, "Response missing 'TimeStamp' field"

    def test_fetch_solar_wind_mag_field(self):
        """Test fetching solar wind magnetic field from the real SWPC API"""
        response = requests.get(SWPC_SOLAR_WIND_MAG_FIELD_URL, timeout=30)
        assert response.status_code == 200, f"SWPC solar wind mag field API returned status {response.status_code}"

        data = response.json()
        assert isinstance(data, dict), "Response is not a dict"
        assert "Bt" in data, "Response missing 'Bt' field"
        assert "Bz" in data, "Response missing 'Bz' field"
        assert "TimeStamp" in data, "Response missing 'TimeStamp' field"

    def test_solar_wind_speed_values_numeric(self):
        """Test that solar wind speed values can be converted to float"""
        response = requests.get(SWPC_SOLAR_WIND_SPEED_URL, timeout=30)
        assert response.status_code == 200

        data = response.json()
        wind_speed = data.get("WindSpeed")
        if wind_speed is not None and wind_speed != "":
            float_val = float(wind_speed)
            assert float_val >= 0, f"WindSpeed should be non-negative, got {float_val}"

    def test_solar_wind_mag_field_values_numeric(self):
        """Test that magnetic field values can be converted to float"""
        response = requests.get(SWPC_SOLAR_WIND_MAG_FIELD_URL, timeout=30)
        assert response.status_code == 200

        data = response.json()
        bt = data.get("Bt")
        bz = data.get("Bz")
        if bt is not None and bt != "":
            float(bt)  # should not raise
        if bz is not None and bz != "":
            float(bz)  # should not raise
