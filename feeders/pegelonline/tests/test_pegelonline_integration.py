"""Integration tests for the pegelonline core HTTP client.

The upstream API is mocked via ``requests_mock``; no Kafka or MQTT is involved
here. Transport-specific producer interactions live in
``test_pegelonline_kafka_app.py`` and ``test_pegelonline_mqtt_app.py``.
"""

import pytest
import requests
import requests_mock

from pegelonline_core import PegelOnlineAPI


@pytest.mark.integration
class TestAPIStationListing:
    def test_list_stations_success(self):
        api = PegelOnlineAPI()
        mock_stations = [
            {"uuid": "u1", "shortname": "MAXAU", "water": {"shortname": "RHEIN"}},
            {"uuid": "u2", "shortname": "HAMBURG", "water": {"shortname": "ELBE"}},
        ]
        with requests_mock.Mocker() as m:
            m.get("https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json",
                  json=mock_stations)
            stations = api.list_stations()
        assert [s["shortname"] for s in stations] == ["MAXAU", "HAMBURG"]

    def test_list_stations_http_error(self):
        api = PegelOnlineAPI()
        with requests_mock.Mocker() as m:
            m.get("https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json",
                  status_code=500)
            with pytest.raises(requests.exceptions.HTTPError):
                api.list_stations()


@pytest.mark.integration
class TestWaterLevelRetrieval:
    BASE = "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations"

    def test_get_water_level_success(self):
        api = PegelOnlineAPI()
        station = "u1"
        with requests_mock.Mocker() as m:
            m.get(f"{self.BASE}/{station}/W/currentmeasurement.json",
                  json={"timestamp": "2024-01-15T12:00:00+01:00", "value": 450,
                        "stateMnwMhw": "normal", "stateNswHsw": "unknown"})
            measurement = api.get_water_level(station)
        assert measurement["value"] == 450

    def test_get_water_level_304_returns_none(self):
        api = PegelOnlineAPI()
        station = "u1"
        url = f"{self.BASE}/{station}/W/currentmeasurement.json"
        api.etags[url] = '"abc"'
        with requests_mock.Mocker() as m:
            m.get(url, status_code=304)
            assert api.get_water_level(station) is None

    def test_get_water_level_stores_etag(self):
        api = PegelOnlineAPI()
        station = "u1"
        url = f"{self.BASE}/{station}/W/currentmeasurement.json"
        with requests_mock.Mocker() as m:
            m.get(url, json={"value": 1, "timestamp": "t", "stateMnwMhw": "n", "stateNswHsw": "u"},
                  headers={"ETag": '"new"'})
            api.get_water_level(station)
        assert api.etags[url] == '"new"'

    def test_get_water_level_500_sidelines_url(self):
        api = PegelOnlineAPI()
        station = "err"
        url = f"{self.BASE}/{station}/W/currentmeasurement.json"
        with requests_mock.Mocker() as m:
            m.get(url, status_code=500)
            assert api.get_water_level(station) is None
        assert url in api.skip_urls

    def test_get_water_level_skipped_url_returns_none_without_request(self):
        api = PegelOnlineAPI()
        url = f"{self.BASE}/skipped/W/currentmeasurement.json"
        api.skip_urls.append(url)
        with requests_mock.Mocker() as m:
            m.get(url, json={"value": 100})
            assert api.get_water_level("skipped") is None
            assert not m.called


@pytest.mark.integration
class TestBulkWaterLevels:
    URL = ("https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json"
           "?includeTimeseries=true&includeCurrentMeasurement=true")

    def test_get_water_levels_success(self):
        api = PegelOnlineAPI()
        mock_stations = [
            {"uuid": "s1", "timeseries": [{"shortname": "W", "currentMeasurement": {
                "timestamp": "t1", "value": 450, "stateMnwMhw": "n", "stateNswHsw": "u"}}]},
            {"uuid": "s2", "timeseries": [{"shortname": "W", "currentMeasurement": {
                "timestamp": "t2", "value": 380, "stateMnwMhw": "n", "stateNswHsw": "u"}}]},
        ]
        with requests_mock.Mocker() as m:
            m.get(self.URL, json=mock_stations)
            levels = api.get_water_levels()
        assert set(levels) == {"s1", "s2"}
        assert levels["s1"]["value"] == 450
        assert levels["s1"]["uuid"] == "s1"

    def test_get_water_levels_filters_non_w(self):
        api = PegelOnlineAPI()
        mock_stations = [{
            "uuid": "s1",
            "timeseries": [
                {"shortname": "Q", "currentMeasurement": {"value": 1}},
                {"shortname": "W", "currentMeasurement": {
                    "timestamp": "t", "value": 7, "stateMnwMhw": "n", "stateNswHsw": "u"}},
            ],
        }]
        with requests_mock.Mocker() as m:
            m.get(self.URL, json=mock_stations)
            levels = api.get_water_levels()
        assert levels["s1"]["value"] == 7

    def test_get_water_levels_http_error_returns_empty(self):
        api = PegelOnlineAPI()
        with requests_mock.Mocker() as m:
            m.get(self.URL, status_code=503)
            assert api.get_water_levels() == {}
