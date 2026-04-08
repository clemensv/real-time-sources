"""Unit tests for BOM Australia Weather Observation Bridge."""

import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from bom_australia_producer_data import WarningBulletin

from bom_australia.bom_australia import (
    BOMAustraliaAPI,
    parse_connection_string,
    send_stations,
    feed_observations,
    feed_warnings,
    _parse_station_list,
    _load_state,
    _save_state,
    FALLBACK_STATIONS,
    STATE_TO_PRODUCT,
)


SAMPLE_OBS_RESPONSE = {
    "observations": {
        "header": [
            {
                "refresh_message": "Issued at 4:51 pm EST Tuesday 7 April 2026",
                "ID": "IDN60901",
                "main_ID": "IDN60900",
                "name": "Sydney Airport",
                "state_time_zone": "NSW",
                "time_zone": "EST",
                "product_name": "Capital City Observations",
                "state": "New South Wales",
            }
        ],
        "data": [
            {
                "sort_order": 0,
                "wmo": 94767,
                "name": "Sydney Airport",
                "history_product": "IDN60901",
                "local_date_time": "07/04:30pm",
                "local_date_time_full": "20260407163000",
                "aifstime_utc": "20260407063000",
                "lat": -33.9,
                "lon": 151.2,
                "apparent_t": 26.2,
                "cloud": "Partly cloudy",
                "cloud_base_m": 3600,
                "cloud_oktas": 5,
                "cloud_type_id": None,
                "cloud_type": "-",
                "delta_t": 6.8,
                "gust_kmh": 19,
                "gust_kt": 10,
                "air_temp": 27.0,
                "dewpt": 16.0,
                "press": 1008.8,
                "press_qnh": 1008.8,
                "press_msl": 1008.8,
                "press_tend": "-",
                "rain_trace": "0.0",
                "rel_hum": 51,
                "sea_state": "-",
                "swell_dir_worded": "-",
                "swell_height": None,
                "swell_period": None,
                "vis_km": "10",
                "weather": "-",
                "wind_dir": "NNE",
                "wind_spd_kmh": 15,
                "wind_spd_kt": 8,
            },
            {
                "sort_order": 1,
                "wmo": 94767,
                "name": "Sydney Airport",
                "history_product": "IDN60901",
                "local_date_time": "07/04:00pm",
                "local_date_time_full": "20260407160000",
                "aifstime_utc": "20260407060000",
                "lat": -33.9,
                "lon": 151.2,
                "apparent_t": 25.5,
                "cloud": "Clear",
                "cloud_base_m": None,
                "cloud_oktas": 1,
                "cloud_type_id": None,
                "cloud_type": "-",
                "delta_t": 6.5,
                "gust_kmh": 17,
                "gust_kt": 9,
                "air_temp": 26.5,
                "dewpt": 15.5,
                "press": 1009.0,
                "press_qnh": 1009.0,
                "press_msl": 1009.0,
                "press_tend": "-",
                "rain_trace": "0.0",
                "rel_hum": 52,
                "sea_state": "-",
                "swell_dir_worded": "-",
                "swell_height": None,
                "swell_period": None,
                "vis_km": "10",
                "weather": "-",
                "wind_dir": "NNE",
                "wind_spd_kmh": 13,
                "wind_spd_kt": 7,
            },
        ],
    }
}

SAMPLE_WARNING_FEED = """<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>Weather Warnings for New South Wales / Australian Capital Territory. Issued by the Australian Bureau of Meteorology</title>
        <link>https://www.bom.gov.au/fwo/IDZ00054.warnings_nsw.xml</link>
        <description>Current weather warnings for New South Wales / Australian Capital Territory.</description>
        <item>
            <title>08/16:29 EST Severe Weather Warning for parts of Snowy Mountains Forecast District.</title>
            <link>https://www.bom.gov.au/products/IDN21037.shtml</link>
            <pubDate>Wed, 08 Apr 2026 06:29:40 GMT</pubDate>
            <guid isPermaLink="false">https://www.bom.gov.au/products/IDN21037.shtml</guid>
        </item>
    </channel>
</rss>
"""


class TestParseStation:
    def test_parse_station_from_observation(self):
        station = BOMAustraliaAPI.parse_station("IDN60901", SAMPLE_OBS_RESPONSE)
        assert station is not None
        assert station.station_wmo == 94767
        assert station.name == "Sydney Airport"
        assert station.product_id == "IDN60901"
        assert station.state == "New South Wales"
        assert station.time_zone == "EST"
        assert station.latitude == -33.9
        assert station.longitude == 151.2

    def test_parse_station_empty_data(self):
        empty = {"observations": {"header": [], "data": []}}
        assert BOMAustraliaAPI.parse_station("IDN60901", empty) is None

    def test_parse_station_no_wmo(self):
        bad = {"observations": {"header": [{"name": "X", "state": "NSW"}], "data": [{"name": "X"}]}}
        assert BOMAustraliaAPI.parse_station("IDN60901", bad) is None


class TestParseObservation:
    def test_parse_observation_success(self):
        obs = BOMAustraliaAPI.parse_observation(SAMPLE_OBS_RESPONSE["observations"]["data"][0])
        assert obs is not None
        assert obs.station_wmo == 94767
        assert obs.air_temp == 27.0
        assert obs.apparent_temp == 26.2
        assert obs.dewpt == 16.0
        assert obs.rel_hum == 51
        assert obs.wind_dir == "NNE"
        assert obs.wind_spd_kmh == 15
        assert obs.gust_kmh == 19
        assert obs.press_msl == 1008.8
        assert obs.cloud == "Partly cloudy"
        assert obs.cloud_oktas == 5
        assert obs.cloud_base_m == 3600
        assert obs.rain_trace == "0.0"
        assert obs.vis_km == "10"
        assert obs.latitude == -33.9
        assert obs.longitude == 151.2
        assert "2026-04-07T06:30:00" in obs.observation_time_utc

    def test_parse_observation_null_fields(self):
        obs = BOMAustraliaAPI.parse_observation(SAMPLE_OBS_RESPONSE["observations"]["data"][0])
        assert obs is not None
        assert obs.swell_height is None
        assert obs.swell_period is None
        assert obs.sea_state is None  # "-" maps to None

    def test_parse_observation_no_wmo(self):
        assert BOMAustraliaAPI.parse_observation({"aifstime_utc": "20260407063000"}) is None

    def test_parse_observation_no_time(self):
        assert BOMAustraliaAPI.parse_observation({"wmo": 94767}) is None

    def test_parse_observation_dash_values(self):
        rec = dict(SAMPLE_OBS_RESPONSE["observations"]["data"][0])
        rec["press_tend"] = "-"
        rec["cloud_type"] = "-"
        rec["weather"] = "-"
        obs = BOMAustraliaAPI.parse_observation(rec)
        assert obs is not None
        assert obs.press_tend is None
        assert obs.cloud_type is None
        assert obs.weather is None


class TestParseWarningFeed:
    def test_parse_warning_feed_success(self):
        bulletins = BOMAustraliaAPI.parse_warning_feed(
            "https://www.bom.gov.au/fwo/IDZ00054.warnings_nsw.xml",
            SAMPLE_WARNING_FEED,
        )

        assert len(bulletins) == 1
        bulletin = bulletins[0]
        assert bulletin.warning_id == "IDN21037"
        assert bulletin.warning_url == "https://www.bom.gov.au/products/IDN21037.shtml"
        assert bulletin.feed_url == "https://www.bom.gov.au/fwo/IDZ00054.warnings_nsw.xml"
        assert bulletin.feed_title.startswith("Weather Warnings for New South Wales")
        assert bulletin.title == "08/16:29 EST Severe Weather Warning for parts of Snowy Mountains Forecast District."
        assert bulletin.published_at == "2026-04-08T06:29:40+00:00"
        assert bulletin.issued_local_time_text == "08/16:29 EST"
        assert bulletin.warning_type == "Severe Weather Warning"
        assert bulletin.affected_area_text == "parts of Snowy Mountains Forecast District."

    def test_parse_warning_feed_invalid_xml(self):
        assert BOMAustraliaAPI.parse_warning_feed("https://www.bom.gov.au/fwo/test.xml", "<rss") == []


class TestConnectionString:
    def test_parse_plain_bootstrap(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        config = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert config["_entity_path"] == "my-topic"

    def test_parse_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=topic"
        config = parse_connection_string(cs)
        assert "bootstrap.servers" in config
        assert config["sasl.mechanism"] == "PLAIN"
        assert config["security.protocol"] == "SASL_SSL"

    def test_parse_empty_parts(self):
        config = parse_connection_string("")
        assert config == {}


class TestStationList:
    def test_parse_station_csv(self):
        stations = _parse_station_list("IDN60901:94767, IDV60901:94866")
        assert len(stations) == 2
        assert stations[0] == ("IDN60901", 94767)
        assert stations[1] == ("IDV60901", 94866)

    def test_parse_empty(self):
        assert _parse_station_list("") == []

    def test_default_stations_non_empty(self):
        assert len(FALLBACK_STATIONS) >= 7

    def test_fallback_stations_have_correct_canberra_product(self):
        canberra = [s for s in FALLBACK_STATIONS if s[1] == 94926]
        assert len(canberra) == 1
        assert canberra[0][0] == "IDC60901"


class TestStationDiscovery:
    SAMPLE_STATIONS_TXT = (
        "Bureau of Meteorology product IDCJMC0014.                                       Produced: 07 Apr 2026\r\n"
        "\r\n"
        "   Site  Dist  Site name                                 Start     End      Lat       Lon Source         STA Height (m)   Bar_ht    WMO\r\n"
        "------- ----- ---------------------------------------- ------- ------- -------- --------- -------------- --- ---------- -------- ------\r\n"
        " 066037 66    SYDNEY AIRPORT AMO                          1929      .. -33.9461  151.1731 GPS            NSW        6.0      6.4  94767\r\n"
        " 086282 08    MELBOURNE AIRPORT                           1970      .. -37.6655  144.8321 GPS            VIC      113.4    113.4  94866\r\n"
        " 001006 01    WYNDHAM AERO                                1951      .. -15.5100  128.1503 GPS            WA         3.8      4.2  95214\r\n"
        " 001000 01    KARUNJIE                                    1940    1983 -16.2919  127.1956 .....          WA       320.0       ..     ..\r\n"
        " 005097 05    LEARMONTH SOLAR OBSERVATORY                 2013      .. -22.2183  114.1031 GPS            NSW         ..       ..     ..\r\n"
    )

    def test_discover_all_active(self):
        api = BOMAustraliaAPI()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = self.SAMPLE_STATIONS_TXT
        mock_resp.raise_for_status = MagicMock()
        with patch.object(api.session, "get", return_value=mock_resp):
            stations = api.discover_stations()
        # 3 active with WMO (Sydney, Melbourne, Wyndham); old closed and no-WMO excluded
        assert len(stations) == 3
        wmos = [s[1] for s in stations]
        assert 94767 in wmos
        assert 94866 in wmos
        assert 95214 in wmos

    def test_discover_with_state_filter(self):
        api = BOMAustraliaAPI()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = self.SAMPLE_STATIONS_TXT
        mock_resp.raise_for_status = MagicMock()
        with patch.object(api.session, "get", return_value=mock_resp):
            stations = api.discover_stations(state_filter="NSW")
        assert len(stations) == 1
        assert stations[0] == ("IDN60901", 94767)

    def test_discover_fallback_on_error(self):
        api = BOMAustraliaAPI()
        with patch.object(api.session, "get", side_effect=Exception("network error")):
            stations = api.discover_stations()
        assert stations == FALLBACK_STATIONS

    def test_state_to_product_covers_all(self):
        assert "NSW" in STATE_TO_PRODUCT
        assert "VIC" in STATE_TO_PRODUCT
        assert "QLD" in STATE_TO_PRODUCT
        assert "WA" in STATE_TO_PRODUCT
        assert "SA" in STATE_TO_PRODUCT
        assert "TAS" in STATE_TO_PRODUCT
        assert "NT" in STATE_TO_PRODUCT


class TestSendStations:
    def test_send_stations_emits_reference_data(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        station_list = [("IDN60901", 94767)]

        with patch.object(api, "get_station_observations", return_value=SAMPLE_OBS_RESPONSE):
            count = send_stations(api, mock_producer, station_list)

        assert count == 1
        mock_producer.send_au_gov_bom_weather_station.assert_called_once()
        mock_producer.producer.flush.assert_called_once()

    def test_send_stations_handles_error(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        with patch.object(api, "get_station_observations", side_effect=Exception("timeout")):
            count = send_stations(api, mock_producer, [("IDN60901", 94767)])

        assert count == 0


class TestFeedObservations:
    def test_feed_observations_emits_new(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_station_observations", return_value=SAMPLE_OBS_RESPONSE):
            count = feed_observations(api, mock_producer, [("IDN60901", 94767)], previous)

        assert count == 1
        assert len(previous) == 1

    def test_feed_observations_deduplicates(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {"94767:2026-04-07T06:30:00+00:00": "2026-04-07T06:30:00+00:00"}

        with patch.object(api, "get_station_observations", return_value=SAMPLE_OBS_RESPONSE):
            count = feed_observations(api, mock_producer, [("IDN60901", 94767)], previous)

        assert count == 0

    def test_feed_observations_handles_error(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        with patch.object(api, "get_station_observations", side_effect=Exception("timeout")):
            count = feed_observations(api, mock_producer, [("IDN60901", 94767)], {})

        assert count == 0


class TestFeedWarnings:
    def test_feed_warnings_emits_new(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {}

        with patch.object(api, "get_warning_feed", return_value=SAMPLE_WARNING_FEED):
            count = feed_warnings(
                api,
                mock_producer,
                ["https://www.bom.gov.au/fwo/IDZ00054.warnings_nsw.xml"],
                previous,
            )

        assert count == 1
        mock_producer.send_au_gov_bom_warning_warning_bulletin.assert_called_once()
        assert previous["IDN21037"] == "2026-04-08T06:29:40+00:00"

    def test_feed_warnings_deduplicates(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()
        previous = {"IDN21037": "2026-04-08T06:29:40+00:00"}

        with patch.object(api, "get_warning_feed", return_value=SAMPLE_WARNING_FEED):
            count = feed_warnings(
                api,
                mock_producer,
                ["https://www.bom.gov.au/fwo/IDZ00054.warnings_nsw.xml"],
                previous,
            )

        assert count == 0
        mock_producer.send_au_gov_bom_warning_warning_bulletin.assert_not_called()

    def test_feed_warnings_handles_error(self):
        api = BOMAustraliaAPI()
        mock_producer = MagicMock()
        mock_producer.producer = MagicMock()

        with patch.object(api, "get_warning_feed", side_effect=Exception("timeout")):
            count = feed_warnings(
                api,
                mock_producer,
                ["https://www.bom.gov.au/fwo/IDZ00054.warnings_nsw.xml"],
                {},
            )

        assert count == 0


class TestState:
    def test_load_state_missing_file(self, tmp_path):
        assert _load_state(str(tmp_path / "nonexistent.json")) == {"observations": {}, "warnings": {}}

    def test_load_state_legacy_flat_dict(self, tmp_path):
        path = str(tmp_path / "state.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"94767:2026-04-07T06:30:00+00:00": "2026-04-07T06:30:00+00:00"}, f)

        loaded = _load_state(path)
        assert loaded["observations"]["94767:2026-04-07T06:30:00+00:00"] == "2026-04-07T06:30:00+00:00"
        assert loaded["warnings"] == {}

    def test_save_and_load_state(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"observations": {"key1": "val1"}, "warnings": {"warn1": "val2"}}
        _save_state(path, data)
        loaded = _load_state(path)
        assert loaded == data

    def test_save_state_truncates(self, tmp_path):
        path = str(tmp_path / "state.json")
        data = {"observations": {str(i): str(i) for i in range(110000)}, "warnings": {}}
        _save_state(path, data)
        loaded = _load_state(path)
        assert len(loaded["observations"]) <= 50000
        assert loaded["warnings"] == {}
