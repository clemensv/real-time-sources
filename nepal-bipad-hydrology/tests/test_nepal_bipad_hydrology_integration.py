"""Integration tests for Nepal BIPAD Hydrology bridge with mocked API."""

import pytest
import requests_mock
import json
from unittest.mock import MagicMock, patch
from nepal_bipad_hydrology.nepal_bipad_hydrology import NepalBipadHydrologyAPI


SAMPLE_STATIONS_PAGE_1 = [
    {
        "id": 3,
        "affectedDemography": {"maleCount": 260058, "femaleCount": 290094, "householdCount": 123181},
        "title": "Babai at Chepang",
        "basin": "Babai",
        "point": {"type": "Point", "coordinates": [81.7135456, 28.3565601]},
        "waterLevel": 1.944,
        "dangerLevel": 6.8,
        "warningLevel": 5.5,
        "waterLevelOn": "2024-01-15T12:00:00+05:45",
        "status": "BELOW WARNING LEVEL",
        "elevation": 308,
        "steady": "STEADY",
        "description": "Old Station",
        "stationSeriesId": 649,
        "dataSource": "hydrology.gov.np",
        "ward": 4870,
        "municipality": 58002,
        "district": 65,
        "province": 5,
    },
    {
        "id": 201,
        "title": "Pasaha Khola at Maheshpur",
        "basin": "Basin From Siwalik Zone",
        "point": {"type": "Point", "coordinates": [85.043521, 27.025129]},
        "waterLevel": 89.911,
        "dangerLevel": 92.0,
        "warningLevel": 91.5,
        "waterLevelOn": "2024-11-18T21:10:00+05:45",
        "status": "BELOW WARNING LEVEL",
        "elevation": 89,
        "steady": "STEADY",
        "description": "Pasaha Khola at Maheshpur",
        "stationSeriesId": 26117,
        "dataSource": "hydrology.gov.np",
        "ward": 6715,
        "municipality": 33006,
        "district": 33,
        "province": 2,
    },
]


def _api_response(results, offset=0, limit=100):
    """Build a Django REST Framework-style paginated response."""
    next_url = None
    if len(results) == limit:
        next_url = f"https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit={limit}&offset={offset + limit}"
    return {
        "count": 9223372036854775807,
        "next": next_url,
        "previous": None,
        "results": results,
    }


@pytest.mark.integration
class TestFetchAllStations:
    """Test station fetching with pagination."""

    def test_fetch_single_page(self):
        api = NepalBipadHydrologyAPI()
        with requests_mock.Mocker() as m:
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=100&offset=0",
                json=_api_response(SAMPLE_STATIONS_PAGE_1),
            )
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=100&offset=100",
                json=_api_response([]),
            )
            stations = api.fetch_all_stations()
            assert len(stations) == 2
            assert stations[0]["id"] == 3
            assert stations[1]["id"] == 201

    def test_fetch_multiple_pages(self):
        api = NepalBipadHydrologyAPI(page_size=1)
        page1 = [SAMPLE_STATIONS_PAGE_1[0]]
        page2 = [SAMPLE_STATIONS_PAGE_1[1]]
        with requests_mock.Mocker() as m:
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=1&offset=0",
                json=_api_response(page1, offset=0, limit=1),
            )
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=1&offset=1",
                json=_api_response(page2, offset=1, limit=1),
            )
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=1&offset=2",
                json=_api_response([]),
            )
            stations = api.fetch_all_stations()
            assert len(stations) == 2

    def test_fetch_empty_result(self):
        api = NepalBipadHydrologyAPI()
        with requests_mock.Mocker() as m:
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=100&offset=0",
                json=_api_response([]),
            )
            stations = api.fetch_all_stations()
            assert len(stations) == 0

    def test_fetch_handles_http_error(self):
        import requests
        api = NepalBipadHydrologyAPI()
        with requests_mock.Mocker() as m:
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=100&offset=0",
                status_code=500,
                text="Internal Server Error",
            )
            with pytest.raises(requests.exceptions.HTTPError):
                api.fetch_all_stations()

    def test_fetch_handles_timeout(self):
        import requests
        api = NepalBipadHydrologyAPI()
        with requests_mock.Mocker() as m:
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=100&offset=0",
                exc=requests.exceptions.ConnectTimeout,
            )
            with pytest.raises(requests.exceptions.ConnectTimeout):
                api.fetch_all_stations()

    def test_pagination_stops_on_empty_results_not_count(self):
        """Verify we don't trust the count field (max long)."""
        api = NepalBipadHydrologyAPI(page_size=2)
        with requests_mock.Mocker() as m:
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=2&offset=0",
                json={
                    "count": 9223372036854775807,
                    "next": "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=2&offset=2",
                    "previous": None,
                    "results": SAMPLE_STATIONS_PAGE_1,
                },
            )
            m.get(
                "https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=2&offset=2",
                json={
                    "count": 9223372036854775807,
                    "next": None,
                    "previous": None,
                    "results": [],
                },
            )
            stations = api.fetch_all_stations()
            assert len(stations) == 2


@pytest.mark.integration
class TestNepalTimezoneHandling:
    """Test Nepal timezone (+05:45) in water level timestamps."""

    def test_water_level_on_preserves_nepal_timezone(self):
        raw = {
            "id": 3,
            "title": "T",
            "basin": "B",
            "waterLevel": 1.0,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
            "waterLevelOn": "2024-01-15T03:50:00+05:45",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert "+05:45" in parsed["water_level_on"]

    def test_water_level_on_empty_string(self):
        raw = {
            "id": 3,
            "title": "T",
            "basin": "B",
            "waterLevel": 1.0,
            "status": "BELOW WARNING LEVEL",
            "steady": "STEADY",
        }
        parsed = NepalBipadHydrologyAPI.parse_reading(raw)
        assert parsed["water_level_on"] == ""
