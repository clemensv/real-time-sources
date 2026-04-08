"""Integration tests with mocked Luchtmeetnet API responses."""

import pytest
import requests_mock

from luchtmeetnet_nl.luchtmeetnet_nl import LuchtmeetnetAPI


BASE_URL = "https://api.luchtmeetnet.nl/open_api"


@pytest.mark.integration
class TestReferenceFetching:
    def test_fetch_all_stations_paginates_and_merges_details(self):
        api = LuchtmeetnetAPI()

        with requests_mock.Mocker() as mocker:
            mocker.get(
                f"{BASE_URL}/stations",
                [
                    {
                        "json": {
                            "pagination": {"last_page": 2},
                            "data": [{"number": "NL01491", "location": "Overschie-A13"}],
                        }
                    },
                    {
                        "json": {
                            "pagination": {"last_page": 2},
                            "data": [{"number": "NL49557", "location": "Wijk aan Zee-Bosweg"}],
                        }
                    },
                ],
            )
            mocker.get(
                f"{BASE_URL}/stations/NL01491",
                json={
                    "data": {
                        "type": "Traffic",
                        "components": ["NO2", "PM10"],
                        "geometry": {"type": "point", "coordinates": [4.4307, 51.93858]},
                        "municipality": "Rotterdam",
                        "province": None,
                        "organisation": "DCMR (Rijnmond)",
                        "location": "Overschie-A13",
                        "year_start": "",
                    }
                },
            )
            mocker.get(
                f"{BASE_URL}/stations/NL49557",
                json={
                    "data": {
                        "type": "Regional",
                        "components": ["PM25"],
                        "geometry": {"type": "point", "coordinates": [4.599, 52.493]},
                        "municipality": "Beverwijk",
                        "province": "Noord-Holland",
                        "organisation": "RIVM",
                        "location": "Wijk aan Zee-Bosweg",
                        "year_start": "2010",
                    }
                },
            )

            stations = api.fetch_all_stations()

        assert [station.station_number for station in stations] == ["NL01491", "NL49557"]
        assert stations[0].components == ["NO2", "PM10"]
        assert stations[1].province == "Noord-Holland"

    def test_fetch_all_components(self):
        api = LuchtmeetnetAPI()

        with requests_mock.Mocker() as mocker:
            mocker.get(
                f"{BASE_URL}/components",
                json={
                    "data": [
                        {"formula": "NO2", "name": {"NL": "Stikstofdioxide (NO2)", "EN": "Nitrogen dioxide (NO2)"}},
                        {"formula": "PM10", "name": {"NL": "Fijn stof (PM10)", "EN": "Particulate matter (PM10)"}},
                    ]
                },
            )

            components = api.fetch_all_components()

        assert [component.formula for component in components] == ["NO2", "PM10"]
        assert components[0].name_en == "Nitrogen dioxide (NO2)"


@pytest.mark.integration
class TestTelemetryFetching:
    def test_get_measurements_returns_page_one_data(self):
        api = LuchtmeetnetAPI()

        with requests_mock.Mocker() as mocker:
            mocker.get(
                f"{BASE_URL}/measurements",
                json={
                    "pagination": {"last_page": 1, "current_page": 1},
                    "data": [
                        {
                            "station_number": "NL01491",
                            "formula": "NO2",
                            "value": 27.4,
                            "timestamp_measured": "2026-04-08T10:00:00+00:00",
                        }
                    ],
                },
            )

            measurements = api.get_measurements("NL01491", "NO2")

        assert measurements[0]["value"] == 27.4
        assert measurements[0]["formula"] == "NO2"

    def test_get_lki_returns_page_one_data(self):
        api = LuchtmeetnetAPI()

        with requests_mock.Mocker() as mocker:
            mocker.get(
                f"{BASE_URL}/lki",
                json={
                    "pagination": {"last_page": 1, "current_page": 1},
                    "data": [
                        {
                            "station_number": "NL01491",
                            "formula": "LKI",
                            "value": 5,
                            "timestamp_measured": "2026-04-08T10:00:00+00:00",
                        }
                    ],
                },
            )

            rows = api.get_lki("NL01491")

        assert rows[0]["value"] == 5
        assert rows[0]["station_number"] == "NL01491"
