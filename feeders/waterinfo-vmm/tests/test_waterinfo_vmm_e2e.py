"""End-to-end tests for Waterinfo VMM bridge against the real KIWIS API."""

import time
import pytest
import requests


KIWIS_BASE_URL = "https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS"
DEFAULT_PARAMS = {
    "service": "kisters",
    "type": "QueryServices",
    "format": "json",
    "datasource": "1",
    "timezone": "UTC",
}


class TestWaterinfoRealEndpoints:
    """Tests against the real Waterinfo KIWIS API."""

    def test_fetch_real_station_list(self):
        """Verify station list endpoint returns data."""
        params = {**DEFAULT_PARAMS, "request": "getStationList",
                  "returnfields": "station_no,station_name,station_latitude,station_longitude,station_id,river_name"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 100  # header + stations

    def test_station_has_required_fields(self):
        """Verify station records have required fields."""
        params = {**DEFAULT_PARAMS, "request": "getStationList",
                  "returnfields": "station_no,station_name,station_latitude,station_longitude,station_id,river_name"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        data = r.json()
        headers = data[0]
        assert "station_no" in headers
        assert "station_name" in headers
        assert "station_latitude" in headers
        assert "station_longitude" in headers

    def test_station_coordinates_valid(self):
        """Verify station coordinates are in Belgium's range."""
        params = {**DEFAULT_PARAMS, "request": "getStationList",
                  "returnfields": "station_no,station_name,station_latitude,station_longitude"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        data = r.json()
        headers = data[0]
        lat_idx = headers.index("station_latitude")
        lon_idx = headers.index("station_longitude")
        # Check first 10 stations
        for row in data[1:11]:
            lat = float(row[lat_idx])
            lon = float(row[lon_idx])
            assert 49.0 < lat < 52.0, f"Latitude {lat} outside Belgium range"
            assert 2.0 < lon < 7.0, f"Longitude {lon} outside Belgium range"

    def test_fetch_water_level_value_layer(self):
        """Verify getTimeseriesValueLayer returns water level data."""
        params = {**DEFAULT_PARAMS, "request": "getTimeseriesValueLayer",
                  "timeseriesgroup_id": "192780",
                  "metadata": "true",
                  "md_returnfields": "ts_id,station_no,station_name,stationparameter_name,ts_unitname"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 100

    def test_value_layer_entry_structure(self):
        """Verify each entry in the value layer has expected fields."""
        params = {**DEFAULT_PARAMS, "request": "getTimeseriesValueLayer",
                  "timeseriesgroup_id": "192780",
                  "metadata": "true",
                  "md_returnfields": "ts_id,station_no,station_name,stationparameter_name,ts_unitname"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        data = r.json()
        entry = data[0]
        assert "ts_id" in entry
        assert "station_no" in entry
        assert "station_name" in entry
        assert "ts_value" in entry
        assert "timestamp" in entry

    def test_value_layer_has_unit_and_parameter(self):
        """Verify value layer entries include unit and parameter info."""
        params = {**DEFAULT_PARAMS, "request": "getTimeseriesValueLayer",
                  "timeseriesgroup_id": "192780",
                  "metadata": "true",
                  "md_returnfields": "ts_id,station_no,station_name,stationparameter_name,ts_unitname"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        data = r.json()
        entry = data[0]
        assert entry.get("stationparameter_name") == "H"
        assert "meter" in entry.get("ts_unitname", "").lower()

    def test_fetch_timeseries_values(self):
        """Verify getTimeseriesValues returns valid time series data."""
        params = {**DEFAULT_PARAMS, "request": "getTimeseriesValueLayer",
                  "timeseriesgroup_id": "192780",
                  "metadata": "true",
                  "md_returnfields": "ts_id"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        layer = r.json()
        # Pick a station that has a recent value
        ts_id = None
        for entry in layer:
            if entry.get("ts_value") is not None:
                ts_id = str(entry["ts_id"])
                break
        assert ts_id is not None, "No active station found"
        # Fetch its time series
        params2 = {**DEFAULT_PARAMS, "request": "getTimeseriesValues",
                   "ts_id": ts_id, "period": "PT1H"}
        r2 = requests.get(KIWIS_BASE_URL, params=params2, timeout=30)
        assert r2.status_code == 200
        data = r2.json()
        assert len(data) > 0
        assert "data" in data[0]

    def test_api_response_time(self):
        """Verify the API responds within a reasonable time."""
        params = {**DEFAULT_PARAMS, "request": "getTimeseriesValueLayer",
                  "timeseriesgroup_id": "192780",
                  "metadata": "true",
                  "md_returnfields": "ts_id,station_no"}
        start = time.time()
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        elapsed = time.time() - start
        assert r.status_code == 200
        assert elapsed < 15, f"API took {elapsed:.1f}s, expected < 15s"

    def test_group_list_contains_water_level(self):
        """Verify the group list includes the water level 15-min group."""
        params = {**DEFAULT_PARAMS, "request": "getGroupList",
                  "group_type": "timeseries", "group_name": "*Download*Waterstand*15m*"}
        r = requests.get(KIWIS_BASE_URL, params=params, timeout=30)
        assert r.status_code == 200
        data = r.json()
        # Should find the 192780 group
        found = False
        for row in data[1:]:
            if row[0] == "192780":
                found = True
                break
        assert found, "Water level 15-min group 192780 not found"
