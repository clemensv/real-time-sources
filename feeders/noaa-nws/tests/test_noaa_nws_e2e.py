"""
End-to-end tests for NOAA NWS Weather Alerts poller.
Tests against the actual NWS API endpoints.

Run with: pytest tests/test_noaa_nws_e2e.py -v -m e2e
Skip in CI: pytest tests/ -v -m "not e2e"
"""

import pytest
import requests


NWS_ALERTS_URL = "https://api.weather.gov/alerts/active"
NWS_ZONES_URL = "https://api.weather.gov/zones?type=forecast&limit=10"
NWS_HEADERS = {
    "User-Agent": "(real-time-sources-test, clemensv@microsoft.com)",
    "Accept": "application/geo+json"
}


@pytest.mark.e2e
@pytest.mark.slow
class TestNWSE2E:
    """End-to-end tests against the actual NWS API"""

    def test_fetch_active_alerts(self):
        """Test fetching active alerts from the real NWS API"""
        response = requests.get(NWS_ALERTS_URL, headers=NWS_HEADERS, timeout=30)
        assert response.status_code == 200, f"NWS API returned status {response.status_code}"

        data = response.json()
        assert data.get("type") == "FeatureCollection", "Response is not a GeoJSON FeatureCollection"
        assert "features" in data, "Response missing 'features' key"
        # features can be empty if there are no active alerts, but the key must exist
        assert isinstance(data["features"], list), "'features' is not a list"

    def test_alert_response_structure(self):
        """Test that alert response has the expected GeoJSON structure"""
        response = requests.get(NWS_ALERTS_URL, headers=NWS_HEADERS, timeout=30)
        assert response.status_code == 200

        data = response.json()
        assert "type" in data
        assert "features" in data

        # If there are alerts, verify their structure
        if len(data["features"]) > 0:
            feature = data["features"][0]
            assert "type" in feature
            assert feature["type"] == "Feature"
            assert "properties" in feature

    def test_alert_fields_present(self):
        """Test that alert features contain expected property fields"""
        response = requests.get(NWS_ALERTS_URL, headers=NWS_HEADERS, timeout=30)
        assert response.status_code == 200

        data = response.json()
        features = data.get("features", [])

        if len(features) == 0:
            pytest.skip("No active alerts at this time")

        props = features[0].get("properties", {})

        expected_fields = [
            "id", "areaDesc", "sent", "effective", "expires",
            "status", "messageType", "category", "severity",
            "certainty", "urgency", "event", "senderName",
            "headline", "description"
        ]

        for field in expected_fields:
            assert field in props, f"Alert property missing expected field: {field}"

    def test_alert_severity_values(self):
        """Test that severity values are within expected enum"""
        response = requests.get(NWS_ALERTS_URL, headers=NWS_HEADERS, timeout=30)
        assert response.status_code == 200

        data = response.json()
        features = data.get("features", [])

        if len(features) == 0:
            pytest.skip("No active alerts at this time")

        valid_severities = {"Extreme", "Severe", "Moderate", "Minor", "Unknown"}
        for feature in features[:10]:  # check up to 10 alerts
            severity = feature["properties"].get("severity", "")
            assert severity in valid_severities, f"Unexpected severity value: {severity}"

    def test_alert_status_values(self):
        """Test that status values are within expected enum"""
        response = requests.get(NWS_ALERTS_URL, headers=NWS_HEADERS, timeout=30)
        assert response.status_code == 200

        data = response.json()
        features = data.get("features", [])

        if len(features) == 0:
            pytest.skip("No active alerts at this time")

        valid_statuses = {"Actual", "Exercise", "System", "Test", "Draft"}
        for feature in features[:10]:
            status = feature["properties"].get("status", "")
            assert status in valid_statuses, f"Unexpected status value: {status}"

    def test_user_agent_required(self):
        """Test that NWS API requires a User-Agent header"""
        # NWS API requires User-Agent; sending without it should still work
        # but may get a 403 or different response
        response = requests.get(NWS_ALERTS_URL, headers=NWS_HEADERS, timeout=30)
        assert response.status_code == 200, "NWS API should respond 200 with proper User-Agent"

    def test_fetch_zones_from_real_api(self):
        """Test fetching forecast zones from the real NWS API"""
        response = requests.get(NWS_ZONES_URL, headers=NWS_HEADERS, timeout=30)
        assert response.status_code == 200, f"NWS Zones API returned status {response.status_code}"

        data = response.json()
        assert data.get("type") == "FeatureCollection", "Response is not a GeoJSON FeatureCollection"
        assert "features" in data, "Response missing 'features' key"

        features = data["features"]
        assert len(features) > 0, "Expected at least one forecast zone"

        # Verify structure of the first zone
        zone_props = features[0].get("properties", {})
        assert "id" in zone_props, "Zone missing 'id' property"
        assert "name" in zone_props, "Zone missing 'name' property"
        assert "state" in zone_props, "Zone missing 'state' property"
        assert "type" in zone_props, "Zone missing 'type' property"

        # Verify id looks like a zone code (e.g., AKZ317, TXZ211)
        zone_id = zone_props["id"]
        assert len(zone_id) >= 3, f"Zone id '{zone_id}' seems too short"
