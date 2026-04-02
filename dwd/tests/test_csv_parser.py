"""Tests for the DWD CSV parser."""

import pytest
from dwd.parsers.csv_parser import parse_dwd_csv, map_row


SAMPLE_CSV_AIR_TEMP = """\
STATIONS_ID;MESS_DATUM;  QN;PP_10;TT_10;TM5_10;RF_10;TD_10;eor
         44;202604010000;    3;   -999;   1.8;  -1.1; 100.0;   1.8;eor
         44;202604010010;    3;   -999;   2.1;  -0.8; 100.0;   2.1;eor
         44;202604010020;    3;1013.2;   2.5;  -0.5;  98.0;   2.1;eor
"""

SAMPLE_CSV_PRECIP = """\
STATIONS_ID;MESS_DATUM;QN;RWS_10;RWS_IND_10;eor
         73;202604010000;3;  0.0;0;eor
         73;202604010010;3;  0.2;1;eor
"""

SAMPLE_CSV_WIND = """\
STATIONS_ID;MESS_DATUM;QN;FF_10;DD_10;eor
        164;202604010000;3;  3.5; 220;eor
        164;202604010010;3; -999; -999;eor
"""


class TestParseDwdCsv:
    def test_air_temperature_rows(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        assert len(rows) == 3

    def test_station_id_stripped(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        assert rows[0]["STATIONS_ID"] == "44"

    def test_timestamp_iso(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        assert rows[0]["MESS_DATUM"] == "2026-04-01T00:00:00+00:00"

    def test_missing_value_is_none(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        assert rows[0]["PP_10"] is None  # -999

    def test_valid_float(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        assert rows[0]["TT_10"] == pytest.approx(1.8)

    def test_quality_level_int(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        assert rows[0]["QN"] == 3

    def test_precipitation(self):
        rows = parse_dwd_csv(SAMPLE_CSV_PRECIP)
        assert len(rows) == 2
        assert rows[1]["RWS_10"] == pytest.approx(0.2)
        assert rows[1]["RWS_IND_10"] == 1

    def test_wind_missing(self):
        rows = parse_dwd_csv(SAMPLE_CSV_WIND)
        assert rows[1]["FF_10"] is None
        assert rows[1]["DD_10"] is None


class TestMapRow:
    def test_air_temperature_mapping(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        mapped = map_row(rows[2], "air_temperature")
        assert mapped["station_id"] == "44"
        assert mapped["air_temperature_2m"] == pytest.approx(2.5)
        assert mapped["pressure_station_level"] == pytest.approx(1013.2)
        assert mapped["quality_level"] == 3

    def test_precipitation_mapping(self):
        rows = parse_dwd_csv(SAMPLE_CSV_PRECIP)
        mapped = map_row(rows[1], "precipitation")
        assert mapped["station_id"] == "73"
        assert mapped["precipitation_height"] == pytest.approx(0.2)

    def test_wind_mapping(self):
        rows = parse_dwd_csv(SAMPLE_CSV_WIND)
        mapped = map_row(rows[0], "wind")
        assert mapped["wind_speed"] == pytest.approx(3.5)
        assert mapped["wind_direction"] == pytest.approx(220)

    def test_missing_stays_none(self):
        rows = parse_dwd_csv(SAMPLE_CSV_AIR_TEMP)
        mapped = map_row(rows[0], "air_temperature")
        assert mapped["pressure_station_level"] is None
