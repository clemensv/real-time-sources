"""Live API tests for the NWS forecasts bridge."""

import pytest
import requests


HEADERS = {
    "User-Agent": "(real-time-sources-test, clemensv@microsoft.com)",
    "Accept": "application/geo+json",
}


@pytest.mark.e2e
@pytest.mark.slow
class TestNWSForecastsE2E:
    def test_fetch_zone_metadata(self):
        response = requests.get("https://api.weather.gov/zones/forecast/WAZ315", headers=HEADERS, timeout=30)
        assert response.status_code == 200
        props = response.json()["properties"]
        assert props["id"] == "WAZ315"
        assert props["name"] == "City of Seattle"

    def test_fetch_land_zone_forecast(self):
        response = requests.get("https://api.weather.gov/zones/forecast/WAZ315/forecast", headers=HEADERS, timeout=30)
        assert response.status_code == 200
        props = response.json()["properties"]
        assert props["zone"].endswith("/WAZ315")
        assert len(props["periods"]) > 0
        assert "detailedForecast" in props["periods"][0]

    def test_fetch_marine_zone_forecast_text(self):
        response = requests.get(
            "https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/pzz135.txt",
            headers={"User-Agent": HEADERS["User-Agent"]},
            timeout=30,
        )
        assert response.status_code == 200
        assert "PZZ135-" in response.text
        assert ".TONIGHT..." in response.text
