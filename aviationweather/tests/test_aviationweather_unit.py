"""
Unit tests for AviationWeather.gov bridge.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from aviationweather_producer_data import Metar, Sigmet, Station
from aviationweather.aviationweather import (
    AviationWeatherPoller,
    parse_connection_string,
    API_BASE,
    DEFAULT_STATIONS,
)


# ---------------------------------------------------------------------------
# Sample API responses matching live AviationWeather.gov structure
# ---------------------------------------------------------------------------

SAMPLE_METAR_RESPONSE = [
    {
        "icaoId": "KJFK",
        "receiptTime": "2026-04-08T19:54:10.159Z",
        "obsTime": 1775677860,
        "reportTime": "2026-04-08T20:00:00.000Z",
        "temp": 5.6,
        "dewp": -5,
        "wdir": 200,
        "wspd": 11,
        "wgst": None,
        "visib": "10+",
        "altim": 1036.7,
        "slp": 1036.5,
        "qcField": 4,
        "wxString": None,
        "metarType": "METAR",
        "rawOb": "METAR KJFK 081951Z 20011KT 10SM FEW250 06/M05 A3061 RMK AO2 SLP365 T00561050",
        "lat": 40.6392,
        "lon": -73.7639,
        "elev": 3,
        "name": "New York/JF Kennedy Intl, NY, US",
        "cover": "FEW",
        "clouds": [{"cover": "FEW", "base": 25000}],
        "fltCat": "VFR",
    },
    {
        "icaoId": "EGLL",
        "receiptTime": "2026-04-08T19:54:47.750Z",
        "obsTime": 1775677800,
        "reportTime": "2026-04-08T20:00:00.000Z",
        "temp": 20,
        "dewp": 8,
        "wdir": 220,
        "wspd": 6,
        "wgst": None,
        "visib": "6+",
        "altim": 1021,
        "qcField": 19,
        "wxString": None,
        "metarType": "METAR",
        "rawOb": "METAR EGLL 081950Z COR AUTO 22006KT 190V260 9999 NCD 20/08 Q1021 NOSIG",
        "lat": 51.477,
        "lon": -0.461,
        "elev": 26,
        "name": "London/Heathrow Intl, EN, GB",
        "cover": "CLR",
        "clouds": [],
        "fltCat": "VFR",
    },
]

SAMPLE_STATION_RESPONSE = [
    {
        "id": "KJFK",
        "icaoId": "KJFK",
        "iataId": "JFK",
        "faaId": "JFK",
        "wmoId": "74486",
        "site": "New York/JF Kennedy Intl",
        "lat": 40.63916,
        "lon": -73.76394,
        "elev": 3,
        "state": "NY",
        "country": "US",
        "priority": 0,
        "siteType": ["METAR", "TAF"],
    },
    {
        "id": "EGLL",
        "icaoId": "EGLL",
        "iataId": "LHR",
        "faaId": None,
        "wmoId": "03772",
        "site": "London/Heathrow Intl",
        "lat": 51.477,
        "lon": -0.461,
        "elev": 26,
        "state": None,
        "country": "GB",
        "priority": 0,
        "siteType": ["METAR", "TAF"],
    },
]

SAMPLE_AIRSIGMET_RESPONSE = [
    {
        "icaoId": "KKCI",
        "alphaChar": "W",
        "seriesId": "6W",
        "receiptTime": "2026-04-08T19:44:47.168Z",
        "creationTime": "2026-04-08T19:55:00.000Z",
        "validTimeFrom": 1775678100,
        "validTimeTo": 1775685300,
        "airSigmetType": "SIGMET",
        "hazard": "CONVECTIVE",
        "altitudeHi1": 32000,
        "altitudeHi2": 32000,
        "altitudeLow1": None,
        "altitudeLow2": None,
        "movementDir": 180,
        "movementSpd": 40,
        "rawAirSigmet": "WSUS33 KKCI 081955\nSIGW\nCONVECTIVE SIGMET 6W\nVALID UNTIL 2155Z",
        "postProcessFlag": 0,
        "severity": 5,
        "coords": [
            {"lat": 41.887, "lon": -123.704},
            {"lat": 40.005, "lon": -124.23},
        ],
    },
]

SAMPLE_ISIGMET_RESPONSE = [
    {
        "icaoId": "ZHWH",
        "firId": "ZHWH",
        "firName": "ZHWH WUHAN",
        "receiptTime": "2026-04-08T14:43:20.839Z",
        "validTimeFrom": 1775664000,
        "validTimeTo": 1775678400,
        "seriesId": "8",
        "hazard": "TS",
        "qualifier": "EMBD",
        "base": None,
        "top": 40000,
        "geom": "AREA",
        "coords": [
            {"lon": 115.377, "lat": 36.67},
            {"lon": 112.678, "lat": 35.637},
        ],
        "dir": "NE",
        "spd": "32",
        "chng": "NC",
        "rawSigmet": "WSCI45 ZHWH 081442\nZHWH SIGMET 8 VALID 081600/082000 ZHHH-",
    },
]


# ---------------------------------------------------------------------------
# Helper to create a poller without real Kafka
# ---------------------------------------------------------------------------

def make_poller(last_polled_file="test_state.json", station_ids="KJFK,EGLL"):
    """Create an AviationWeatherPoller with mocked Kafka."""
    with patch("aviationweather.aviationweather.AviationWeatherPoller.__init__", return_value=None):
        poller = AviationWeatherPoller.__new__(AviationWeatherPoller)
        poller.kafka_topic = "test-topic"
        poller.last_polled_file = last_polled_file
        poller.station_ids = station_ids
        poller.metar_poll_interval = 60
        poller.sigmet_poll_interval = 120
        mock_kafka_producer = MagicMock()
        poller.producer = MagicMock()
        poller.producer.producer = mock_kafka_producer
        return poller


# ---------------------------------------------------------------------------
# Test: parse_connection_string
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    """Tests for the parse_connection_string helper."""

    def test_event_hubs_connection_string(self):
        conn_str = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(conn_str)
        assert "bootstrap.servers" in result
        assert result["bootstrap.servers"] == "myns.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert "sasl.password" in result
        assert result["security.protocol"] == "SASL_SSL"

    def test_plain_kafka_connection_string(self):
        conn_str = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        result = parse_connection_string(conn_str)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "my-topic"
        assert "sasl.username" not in result

    def test_empty_connection_string(self):
        result = parse_connection_string("")
        assert result == {}

    def test_connection_string_with_spaces(self):
        conn_str = "BootstrapServer= localhost:9092 ;EntityPath= test-topic "
        result = parse_connection_string(conn_str)
        assert result["bootstrap.servers"].strip() == "localhost:9092"
        assert result["kafka_topic"].strip() == "test-topic"


# ---------------------------------------------------------------------------
# Test: epoch_to_iso
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEpochToIso:
    """Tests for epoch timestamp conversion."""

    def test_valid_epoch(self):
        result = AviationWeatherPoller.epoch_to_iso(1775677860)
        assert result is not None
        assert "2026-04-08" in result
        assert "+00:00" in result

    def test_none_epoch(self):
        assert AviationWeatherPoller.epoch_to_iso(None) is None

    def test_zero_epoch(self):
        result = AviationWeatherPoller.epoch_to_iso(0)
        assert result is not None
        assert "1970-01-01" in result

    def test_float_epoch(self):
        result = AviationWeatherPoller.epoch_to_iso(1775677860.5)
        assert result is not None

    def test_string_epoch_fails(self):
        assert AviationWeatherPoller.epoch_to_iso("not a number") is None


# ---------------------------------------------------------------------------
# Test: safe_int and safe_float
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSafeConversions:
    """Tests for safe type conversion helpers."""

    def test_safe_int_valid(self):
        assert AviationWeatherPoller.safe_int(42) == 42

    def test_safe_int_float(self):
        assert AviationWeatherPoller.safe_int(42.9) == 42

    def test_safe_int_none(self):
        assert AviationWeatherPoller.safe_int(None) is None

    def test_safe_int_string(self):
        assert AviationWeatherPoller.safe_int("not int") is None

    def test_safe_float_valid(self):
        assert AviationWeatherPoller.safe_float(3.14) == 3.14

    def test_safe_float_int(self):
        assert AviationWeatherPoller.safe_float(42) == 42.0

    def test_safe_float_none(self):
        assert AviationWeatherPoller.safe_float(None) is None

    def test_safe_float_string(self):
        assert AviationWeatherPoller.safe_float("not float") is None


# ---------------------------------------------------------------------------
# Test: parse_station
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseStation:
    """Tests for station parsing."""

    def test_parse_valid_station(self):
        station = AviationWeatherPoller.parse_station(SAMPLE_STATION_RESPONSE[0])
        assert station is not None
        assert station.icao_id == "KJFK"
        assert station.iata_id == "JFK"
        assert station.faa_id == "JFK"
        assert station.wmo_id == "74486"
        assert station.name == "New York/JF Kennedy Intl"
        assert station.latitude == pytest.approx(40.63916)
        assert station.longitude == pytest.approx(-73.76394)
        assert station.elevation == 3.0
        assert station.state == "NY"
        assert station.country == "US"
        assert station.site_type == "METAR,TAF"

    def test_parse_station_no_faa_id(self):
        station = AviationWeatherPoller.parse_station(SAMPLE_STATION_RESPONSE[1])
        assert station is not None
        assert station.icao_id == "EGLL"
        assert station.faa_id is None
        assert station.state is None

    def test_parse_station_missing_icao(self):
        result = AviationWeatherPoller.parse_station({"site": "test"})
        assert result is None

    def test_parse_station_missing_lat_lon(self):
        result = AviationWeatherPoller.parse_station({"icaoId": "TEST"})
        assert result is None

    def test_parse_station_uses_name_fallback(self):
        raw = {"icaoId": "TEST", "name": "Test Station", "lat": 10.0, "lon": 20.0}
        station = AviationWeatherPoller.parse_station(raw)
        assert station is not None
        assert station.name == "Test Station"

    def test_parse_station_uses_icao_as_name_fallback(self):
        raw = {"icaoId": "TEST", "lat": 10.0, "lon": 20.0}
        station = AviationWeatherPoller.parse_station(raw)
        assert station is not None
        assert station.name == "TEST"

    def test_parse_station_site_type_none(self):
        raw = {"icaoId": "TEST", "site": "Test", "lat": 10.0, "lon": 20.0}
        station = AviationWeatherPoller.parse_station(raw)
        assert station is not None
        assert station.site_type is None


# ---------------------------------------------------------------------------
# Test: parse_metar
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseMetar:
    """Tests for METAR parsing."""

    def test_parse_valid_metar(self):
        metar = AviationWeatherPoller.parse_metar(SAMPLE_METAR_RESPONSE[0])
        assert metar is not None
        assert metar.icao_id == "KJFK"
        assert "2026-04-08" in metar.obs_time
        assert metar.temp == pytest.approx(5.6)
        assert metar.dewp == pytest.approx(-5.0)
        assert metar.wdir == 200
        assert metar.wspd == 11
        assert metar.wgst is None
        assert metar.visib == "10+"
        assert metar.altim == pytest.approx(1036.7)
        assert metar.slp == pytest.approx(1036.5)
        assert metar.flt_cat == "VFR"
        assert metar.metar_type == "METAR"
        assert "KJFK" in metar.raw_ob

    def test_parse_metar_clouds_serialized(self):
        metar = AviationWeatherPoller.parse_metar(SAMPLE_METAR_RESPONSE[0])
        assert metar is not None
        assert metar.clouds is not None
        clouds = json.loads(metar.clouds)
        assert isinstance(clouds, list)
        assert len(clouds) == 1
        assert clouds[0]["cover"] == "FEW"
        assert clouds[0]["base"] == 25000

    def test_parse_metar_empty_clouds(self):
        metar = AviationWeatherPoller.parse_metar(SAMPLE_METAR_RESPONSE[1])
        assert metar is not None
        assert metar.clouds is not None
        clouds = json.loads(metar.clouds)
        assert clouds == []

    def test_parse_metar_missing_icao(self):
        result = AviationWeatherPoller.parse_metar({"rawOb": "test", "obsTime": 12345})
        assert result is None

    def test_parse_metar_missing_raw_ob(self):
        result = AviationWeatherPoller.parse_metar({"icaoId": "TEST", "obsTime": 12345})
        assert result is None

    def test_parse_metar_missing_obs_time(self):
        result = AviationWeatherPoller.parse_metar({"icaoId": "TEST", "rawOb": "test"})
        assert result is None

    def test_parse_metar_invalid_obs_time(self):
        result = AviationWeatherPoller.parse_metar(
            {"icaoId": "TEST", "rawOb": "test", "obsTime": "not a number"}
        )
        assert result is None

    def test_parse_metar_null_optional_fields(self):
        raw = {
            "icaoId": "TEST",
            "obsTime": 1775677860,
            "rawOb": "METAR TEST",
            "temp": None,
            "dewp": None,
            "wdir": None,
            "wspd": None,
            "wgst": None,
            "visib": None,
            "altim": None,
            "slp": None,
            "qcField": None,
            "wxString": None,
            "metarType": None,
            "lat": None,
            "lon": None,
            "elev": None,
            "fltCat": None,
            "clouds": None,
            "name": None,
            "reportTime": None,
        }
        metar = AviationWeatherPoller.parse_metar(raw)
        assert metar is not None
        assert metar.temp is None
        assert metar.clouds is None
        assert metar.visib is None

    def test_parse_metar_report_time_iso(self):
        metar = AviationWeatherPoller.parse_metar(SAMPLE_METAR_RESPONSE[0])
        assert metar is not None
        assert metar.report_time == "2026-04-08T20:00:00.000Z"

    def test_parse_metar_invalid_report_time(self):
        raw = dict(SAMPLE_METAR_RESPONSE[0])
        raw["reportTime"] = "not-a-date"
        metar = AviationWeatherPoller.parse_metar(raw)
        assert metar is not None
        assert metar.report_time is None

    def test_parse_metar_name_field(self):
        metar = AviationWeatherPoller.parse_metar(SAMPLE_METAR_RESPONSE[0])
        assert metar is not None
        assert metar.name == "New York/JF Kennedy Intl, NY, US"


# ---------------------------------------------------------------------------
# Test: parse_us_sigmet
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseUsSigmet:
    """Tests for US SIGMET parsing."""

    def test_parse_valid_us_sigmet(self):
        sigmet = AviationWeatherPoller.parse_us_sigmet(SAMPLE_AIRSIGMET_RESPONSE[0])
        assert sigmet is not None
        assert sigmet.icao_id == "KKCI"
        assert sigmet.series_id == "6W"
        assert sigmet.hazard == "CONVECTIVE"
        assert sigmet.sigmet_type == "SIGMET"
        assert sigmet.altitude_hi == 32000
        assert sigmet.altitude_low is None
        assert sigmet.movement_dir == "180"
        assert sigmet.movement_spd == "40"
        assert sigmet.severity == 5
        assert sigmet.qualifier is None
        assert "2026-04-08" in sigmet.valid_time_from
        assert "2026-04-08" in sigmet.valid_time_to

    def test_parse_us_sigmet_coords_serialized(self):
        sigmet = AviationWeatherPoller.parse_us_sigmet(SAMPLE_AIRSIGMET_RESPONSE[0])
        assert sigmet is not None
        coords = json.loads(sigmet.coords)
        assert isinstance(coords, list)
        assert len(coords) == 2
        assert coords[0]["lat"] == pytest.approx(41.887)

    def test_parse_us_sigmet_missing_icao(self):
        result = AviationWeatherPoller.parse_us_sigmet({"seriesId": "1W"})
        assert result is None

    def test_parse_us_sigmet_missing_series(self):
        result = AviationWeatherPoller.parse_us_sigmet({"icaoId": "KKCI"})
        assert result is None

    def test_parse_us_sigmet_missing_valid_times(self):
        result = AviationWeatherPoller.parse_us_sigmet(
            {"icaoId": "KKCI", "seriesId": "1W"}
        )
        assert result is None


# ---------------------------------------------------------------------------
# Test: parse_intl_sigmet
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseIntlSigmet:
    """Tests for international SIGMET parsing."""

    def test_parse_valid_intl_sigmet(self):
        sigmet = AviationWeatherPoller.parse_intl_sigmet(SAMPLE_ISIGMET_RESPONSE[0])
        assert sigmet is not None
        assert sigmet.icao_id == "ZHWH"
        assert sigmet.series_id == "8"
        assert sigmet.hazard == "TS"
        assert sigmet.qualifier == "EMBD"
        assert sigmet.sigmet_type == "ISIGMET"
        assert sigmet.altitude_hi == 40000
        assert sigmet.altitude_low is None
        assert sigmet.movement_dir == "NE"
        assert sigmet.movement_spd == "32"
        assert sigmet.severity is None

    def test_parse_intl_sigmet_coords(self):
        sigmet = AviationWeatherPoller.parse_intl_sigmet(SAMPLE_ISIGMET_RESPONSE[0])
        assert sigmet is not None
        coords = json.loads(sigmet.coords)
        assert isinstance(coords, list)
        assert len(coords) == 2

    def test_parse_intl_sigmet_raw_text(self):
        sigmet = AviationWeatherPoller.parse_intl_sigmet(SAMPLE_ISIGMET_RESPONSE[0])
        assert sigmet is not None
        assert "ZHWH SIGMET 8" in sigmet.raw_sigmet


# ---------------------------------------------------------------------------
# Test: sigmet_dedup_key
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSigmetDedupKey:
    """Tests for SIGMET deduplication key generation."""

    def test_dedup_key_format(self):
        sigmet = Sigmet(
            icao_id="KKCI",
            series_id="6W",
            valid_time_from="2026-04-08T19:55:00+00:00",
            valid_time_to="2026-04-08T21:55:00+00:00",
            hazard="CONVECTIVE",
            qualifier=None,
            sigmet_type="SIGMET",
            altitude_hi=32000,
            altitude_low=None,
            movement_dir="180",
            movement_spd="40",
            severity=5,
            raw_sigmet="test",
            coords=None,
        )
        key = AviationWeatherPoller.sigmet_dedup_key(sigmet)
        assert key == "KKCI:6W:2026-04-08T19:55:00+00:00:2026-04-08T21:55:00+00:00"

    def test_different_sigmets_different_keys(self):
        sigmet1 = Sigmet(
            icao_id="KKCI", series_id="6W",
            valid_time_from="2026-04-08T19:55:00+00:00",
            valid_time_to="2026-04-08T21:55:00+00:00",
            hazard=None, qualifier=None, sigmet_type=None,
            altitude_hi=None, altitude_low=None,
            movement_dir=None, movement_spd=None,
            severity=None, raw_sigmet=None, coords=None,
        )
        sigmet2 = Sigmet(
            icao_id="KKCI", series_id="7W",
            valid_time_from="2026-04-08T19:55:00+00:00",
            valid_time_to="2026-04-08T21:55:00+00:00",
            hazard=None, qualifier=None, sigmet_type=None,
            altitude_hi=None, altitude_low=None,
            movement_dir=None, movement_spd=None,
            severity=None, raw_sigmet=None, coords=None,
        )
        assert AviationWeatherPoller.sigmet_dedup_key(sigmet1) != AviationWeatherPoller.sigmet_dedup_key(sigmet2)


# ---------------------------------------------------------------------------
# Test: state persistence
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStatePersistence:
    """Tests for load_state / save_state."""

    def test_load_state_missing_file(self):
        poller = make_poller(last_polled_file="nonexistent_file_xyz.json")
        state = poller.load_state()
        assert state == {"metar_timestamps": {}, "sigmet_keys": []}

    def test_save_and_load_state(self, tmp_path):
        state_file = str(tmp_path / "state.json")
        poller = make_poller(last_polled_file=state_file)
        state = {
            "metar_timestamps": {"KJFK": "2026-04-08T19:51:00+00:00"},
            "sigmet_keys": ["KKCI:6W:2026-04-08T19:55:00+00:00:2026-04-08T21:55:00+00:00"],
        }
        poller.save_state(state)
        loaded = poller.load_state()
        assert loaded["metar_timestamps"]["KJFK"] == "2026-04-08T19:51:00+00:00"
        assert len(loaded["sigmet_keys"]) == 1

    def test_load_state_corrupt_file(self, tmp_path):
        state_file = str(tmp_path / "corrupt.json")
        with open(state_file, 'w') as f:
            f.write("not json")
        poller = make_poller(last_polled_file=state_file)
        state = poller.load_state()
        assert state == {"metar_timestamps": {}, "sigmet_keys": []}


# ---------------------------------------------------------------------------
# Test: fetch methods
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFetchMethods:
    """Tests for API fetch methods."""

    @patch("aviationweather.aviationweather.requests.get")
    def test_fetch_metar_json_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_METAR_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = AviationWeatherPoller.fetch_metar_json("KJFK,EGLL")
        assert len(result) == 2
        assert result[0]["icaoId"] == "KJFK"

    @patch("aviationweather.aviationweather.requests.get")
    def test_fetch_metar_json_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        result = AviationWeatherPoller.fetch_metar_json("KJFK")
        assert result == []

    @patch("aviationweather.aviationweather.requests.get")
    def test_fetch_station_json_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_STATION_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = AviationWeatherPoller.fetch_station_json("KJFK")
        assert len(result) == 2

    @patch("aviationweather.aviationweather.requests.get")
    def test_fetch_airsigmet_json_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_AIRSIGMET_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = AviationWeatherPoller.fetch_airsigmet_json()
        assert len(result) == 1

    @patch("aviationweather.aviationweather.requests.get")
    def test_fetch_isigmet_json_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_ISIGMET_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = AviationWeatherPoller.fetch_isigmet_json()
        assert len(result) == 1

    @patch("aviationweather.aviationweather.requests.get")
    def test_fetch_metar_json_non_list_response(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"error": "bad request"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = AviationWeatherPoller.fetch_metar_json("INVALID")
        assert result == []


# ---------------------------------------------------------------------------
# Test: emit methods with mocked Kafka
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEmitMethods:
    """Tests for the emit_* methods with mocked Kafka."""

    @patch.object(AviationWeatherPoller, "fetch_station_json")
    def test_emit_stations(self, mock_fetch):
        mock_fetch.return_value = SAMPLE_STATION_RESPONSE
        poller = make_poller()
        count = poller.emit_stations()
        assert count == 2
        assert poller.producer.send_gov_noaa_aviationweather_station.call_count == 2
        poller.producer.producer.flush.assert_called()

    @patch.object(AviationWeatherPoller, "fetch_metar_json")
    def test_emit_metars_new(self, mock_fetch):
        mock_fetch.return_value = SAMPLE_METAR_RESPONSE
        poller = make_poller()
        count, timestamps = poller.emit_metars({})
        assert count == 2
        assert "KJFK" in timestamps
        assert "EGLL" in timestamps
        assert poller.producer.send_gov_noaa_aviationweather_metar.call_count == 2

    @patch.object(AviationWeatherPoller, "fetch_metar_json")
    def test_emit_metars_dedup(self, mock_fetch):
        mock_fetch.return_value = SAMPLE_METAR_RESPONSE
        poller = make_poller()
        # First call to get timestamps
        _, timestamps = poller.emit_metars({})
        # Reset mock
        poller.producer.send_gov_noaa_aviationweather_metar.reset_mock()
        # Second call with same timestamps
        count, _ = poller.emit_metars(timestamps)
        assert count == 0
        poller.producer.send_gov_noaa_aviationweather_metar.assert_not_called()

    @patch.object(AviationWeatherPoller, "fetch_airsigmet_json")
    @patch.object(AviationWeatherPoller, "fetch_isigmet_json")
    def test_emit_sigmets_new(self, mock_isigmet, mock_airsigmet):
        mock_airsigmet.return_value = SAMPLE_AIRSIGMET_RESPONSE
        mock_isigmet.return_value = SAMPLE_ISIGMET_RESPONSE
        poller = make_poller()
        count, keys = poller.emit_sigmets(set())
        assert count == 2
        assert len(keys) == 2
        assert poller.producer.send_gov_noaa_aviationweather_sigmet.call_count == 2

    @patch.object(AviationWeatherPoller, "fetch_airsigmet_json")
    @patch.object(AviationWeatherPoller, "fetch_isigmet_json")
    def test_emit_sigmets_dedup(self, mock_isigmet, mock_airsigmet):
        mock_airsigmet.return_value = SAMPLE_AIRSIGMET_RESPONSE
        mock_isigmet.return_value = SAMPLE_ISIGMET_RESPONSE
        poller = make_poller()
        _, keys = poller.emit_sigmets(set())
        # Reset mock
        poller.producer.send_gov_noaa_aviationweather_sigmet.reset_mock()
        # Second call with seen keys
        count, _ = poller.emit_sigmets(keys)
        assert count == 0
        poller.producer.send_gov_noaa_aviationweather_sigmet.assert_not_called()

    @patch.object(AviationWeatherPoller, "fetch_station_json")
    def test_emit_stations_empty(self, mock_fetch):
        mock_fetch.return_value = []
        poller = make_poller()
        count = poller.emit_stations()
        assert count == 0
        poller.producer.producer.flush.assert_not_called()


# ---------------------------------------------------------------------------
# Test: poll_and_send
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollAndSend:
    """Tests for the main polling loop."""

    @patch.object(AviationWeatherPoller, "fetch_isigmet_json")
    @patch.object(AviationWeatherPoller, "fetch_airsigmet_json")
    @patch.object(AviationWeatherPoller, "fetch_metar_json")
    @patch.object(AviationWeatherPoller, "fetch_station_json")
    def test_poll_and_send_once(self, mock_stations, mock_metars, mock_airsigmet, mock_isigmet, tmp_path):
        mock_stations.return_value = SAMPLE_STATION_RESPONSE
        mock_metars.return_value = SAMPLE_METAR_RESPONSE
        mock_airsigmet.return_value = SAMPLE_AIRSIGMET_RESPONSE
        mock_isigmet.return_value = SAMPLE_ISIGMET_RESPONSE

        state_file = str(tmp_path / "state.json")
        poller = make_poller(last_polled_file=state_file)
        poller.poll_and_send(once=True)

        # Stations emitted
        assert poller.producer.send_gov_noaa_aviationweather_station.call_count == 2
        # METARs emitted
        assert poller.producer.send_gov_noaa_aviationweather_metar.call_count == 2
        # SIGMETs emitted
        assert poller.producer.send_gov_noaa_aviationweather_sigmet.call_count == 2
        # State saved
        assert os.path.exists(state_file)


# ---------------------------------------------------------------------------
# Test: dataclass serialization
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDataclassSerialization:
    """Tests for generated dataclass serialization."""

    def test_station_to_json(self):
        station = Station(
            icao_id="KJFK", iata_id="JFK", faa_id="JFK", wmo_id="74486",
            name="Test", latitude=40.0, longitude=-73.0, elevation=3.0,
            state="NY", country="US", site_type="METAR,TAF",
        )
        data = json.loads(station.to_json())
        assert data["icao_id"] == "KJFK"
        assert data["latitude"] == 40.0

    def test_metar_to_json(self):
        metar = Metar(
            icao_id="KJFK", obs_time="2026-04-08T19:51:00+00:00",
            report_time=None, temp=5.6, dewp=-5.0, wdir=200, wspd=11,
            wgst=None, visib="10+", altim=1036.7, slp=1036.5, qc_field=4,
            wx_string=None, metar_type="METAR",
            raw_ob="METAR KJFK test", latitude=40.6, longitude=-73.7,
            elevation=3.0, flt_cat="VFR", clouds='[{"cover":"FEW","base":25000}]',
            name="Test",
        )
        data = json.loads(metar.to_json())
        assert data["icao_id"] == "KJFK"
        assert data["temp"] == 5.6

    def test_sigmet_to_json(self):
        sigmet = Sigmet(
            icao_id="KKCI", series_id="6W",
            valid_time_from="2026-04-08T19:55:00+00:00",
            valid_time_to="2026-04-08T21:55:00+00:00",
            hazard="CONVECTIVE", qualifier=None, sigmet_type="SIGMET",
            altitude_hi=32000, altitude_low=None, movement_dir="180",
            movement_spd="40", severity=5, raw_sigmet="test",
            coords='[{"lat":41.88,"lon":-123.70}]',
        )
        data = json.loads(sigmet.to_json())
        assert data["icao_id"] == "KKCI"
        assert data["hazard"] == "CONVECTIVE"
