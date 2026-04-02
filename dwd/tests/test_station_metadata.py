"""Tests for station metadata module parsing."""

from dwd.modules.station_metadata import _parse_station_list


SAMPLE_STATION_LIST = """\
Stations_id von_datum bis_datum Stationshoehe geoBreite geoLaenge Stationsname                              Bundesland Abgabe
----------- --------- --------- ------------- --------- --------- ----------------------------------------- ---------- ------
00044 20070209 20260401             44     52.9336    8.2370 Großenkneten                              Niedersachsen      Frei
00073 20070401 20260401            162     48.8049   13.3564 Aulzhausen                                Bayern             Frei
00078 20041101 20240101            645     47.8413   12.0031 Traunstein                                Bayern             Frei
"""


class TestStationListParser:
    def test_parses_stations(self):
        stations = _parse_station_list(SAMPLE_STATION_LIST)
        assert len(stations) == 3

    def test_station_id(self):
        stations = _parse_station_list(SAMPLE_STATION_LIST)
        assert stations[0]["station_id"] == "44"

    def test_coordinates(self):
        stations = _parse_station_list(SAMPLE_STATION_LIST)
        assert abs(stations[0]["latitude"] - 52.9336) < 0.001
        assert abs(stations[0]["longitude"] - 8.2370) < 0.001

    def test_elevation(self):
        stations = _parse_station_list(SAMPLE_STATION_LIST)
        assert stations[0]["elevation"] == 44.0

    def test_state(self):
        stations = _parse_station_list(SAMPLE_STATION_LIST)
        assert stations[0]["state"] == "Niedersachsen"
        assert stations[1]["state"] == "Bayern"

    def test_station_name(self):
        stations = _parse_station_list(SAMPLE_STATION_LIST)
        assert stations[0]["station_name"] == "Großenkneten"
