"""Integration tests for CDEC Reservoirs bridge with mocked API."""

import pytest
import requests_mock
import json
import asyncio
from unittest.mock import MagicMock, patch
from cdec_reservoirs.cdec_reservoirs import (
    CdecReservoirsAPI,
    BASE_URL,
    parse_cdec_timestamp,
    normalize_value,
)


MOCK_READINGS = [
    {
        "stationId": "SHA",
        "durCode": "H",
        "SENSOR_NUM": 15,
        "sensorType": "STORAGE",
        "date": "2026-4-1 0:00",
        "obsDate": "2026-4-1 0:00",
        "value": 4090763,
        "dataFlag": " ",
        "units": "AF"
    },
    {
        "stationId": "SHA",
        "durCode": "H",
        "SENSOR_NUM": 6,
        "sensorType": "RES ELE",
        "date": "2026-4-1 0:00",
        "obsDate": "2026-4-1 0:00",
        "value": 1052.15,
        "dataFlag": " ",
        "units": "FEET"
    },
    {
        "stationId": "ORO",
        "durCode": "H",
        "SENSOR_NUM": 15,
        "sensorType": "STORAGE",
        "date": "2026-4-1 0:00",
        "obsDate": "2026-4-1 0:00",
        "value": 3200000,
        "dataFlag": " ",
        "units": "AF"
    },
    {
        "stationId": "FOL",
        "durCode": "H",
        "SENSOR_NUM": 76,
        "sensorType": "INFLOW",
        "date": "2026-4-1 1:00",
        "obsDate": "2026-4-1 1:00",
        "value": 5200,
        "dataFlag": " ",
        "units": "CFS"
    },
    {
        "stationId": "SHA",
        "durCode": "H",
        "SENSOR_NUM": 23,
        "sensorType": "OUTFLOW",
        "date": "2026-4-1 0:00",
        "obsDate": "2026-4-1 0:00",
        "value": -9999,
        "dataFlag": " ",
        "units": "CFS"
    },
    {
        "stationId": "NML",
        "durCode": "H",
        "SENSOR_NUM": 15,
        "sensorType": "STORAGE",
        "date": "2026-4-1 0:00",
        "obsDate": "2026-4-1 0:00",
        "value": None,
        "dataFlag": " ",
        "units": "AF"
    },
]


@pytest.mark.integration
class TestFetchReadings:
    """Test fetching readings from CDEC with mocked HTTP."""

    def test_fetch_readings_success(self):
        api = CdecReservoirsAPI(stations="SHA,ORO,FOL")
        with requests_mock.Mocker() as m:
            m.get(BASE_URL, json=MOCK_READINGS)
            readings = api.fetch_readings("2026-04-01", "2026-04-02")
            assert len(readings) == 6
            assert readings[0]['stationId'] == 'SHA'
            assert readings[0]['SENSOR_NUM'] == 15

    def test_fetch_readings_empty_list(self):
        api = CdecReservoirsAPI(stations="XYZ")
        with requests_mock.Mocker() as m:
            m.get(BASE_URL, json=[])
            readings = api.fetch_readings("2026-04-01", "2026-04-02")
            assert readings == []

    def test_fetch_readings_http_error(self):
        import requests
        api = CdecReservoirsAPI()
        with requests_mock.Mocker() as m:
            m.get(BASE_URL, status_code=500, text="Server Error")
            with pytest.raises(requests.exceptions.HTTPError):
                api.fetch_readings("2026-04-01", "2026-04-02")

    def test_fetch_readings_timeout(self):
        import requests
        api = CdecReservoirsAPI()
        with requests_mock.Mocker() as m:
            m.get(BASE_URL, exc=requests.exceptions.ConnectTimeout)
            with pytest.raises(requests.exceptions.ConnectTimeout):
                api.fetch_readings("2026-04-01", "2026-04-02")

    def test_fetch_readings_unexpected_response(self):
        api = CdecReservoirsAPI()
        with requests_mock.Mocker() as m:
            m.get(BASE_URL, json={"error": "bad request"})
            readings = api.fetch_readings("2026-04-01", "2026-04-02")
            assert readings == []


@pytest.mark.integration
class TestReadingParsing:
    """Test parsing and normalization of CDEC readings."""

    def test_storage_reading_parsed_correctly(self):
        raw = MOCK_READINGS[0]
        assert raw['stationId'] == 'SHA'
        assert raw['SENSOR_NUM'] == 15
        ts = parse_cdec_timestamp(raw['date'])
        assert ts == "2026-04-01T00:00:00-08:00"
        assert normalize_value(raw['value']) == 4090763.0

    def test_elevation_reading_parsed_correctly(self):
        raw = MOCK_READINGS[1]
        assert raw['sensorType'] == 'RES ELE'
        assert normalize_value(raw['value']) == 1052.15

    def test_inflow_reading_parsed_correctly(self):
        raw = MOCK_READINGS[3]
        assert raw['stationId'] == 'FOL'
        assert raw['SENSOR_NUM'] == 76
        assert normalize_value(raw['value']) == 5200.0

    def test_sentinel_value_normalized_to_none(self):
        raw = MOCK_READINGS[4]
        assert raw['value'] == -9999
        assert normalize_value(raw['value']) is None

    def test_null_value_normalized_to_none(self):
        raw = MOCK_READINGS[5]
        assert raw['value'] is None
        assert normalize_value(raw['value']) is None


@pytest.mark.integration
class TestDataClassCreation:
    """Test creating ReservoirReading data class instances."""

    def test_create_reservoir_reading(self):
        from cdec_reservoirs_producer_data.gov.ca.water.cdec.reservoirreading import ReservoirReading
        reading = ReservoirReading(
            station_id="SHA",
            sensor_num=15,
            sensor_type="STORAGE",
            value=4090763.0,
            units="AF",
            date="2026-04-01T00:00:00-08:00",
            dur_code="H",
            data_flag=" ",
        )
        assert reading.station_id == "SHA"
        assert reading.sensor_num == 15
        assert reading.value == 4090763.0
        assert reading.units == "AF"

    def test_create_reservoir_reading_with_null_value(self):
        from cdec_reservoirs_producer_data.gov.ca.water.cdec.reservoirreading import ReservoirReading
        reading = ReservoirReading(
            station_id="SHA",
            sensor_num=23,
            sensor_type="OUTFLOW",
            value=None,
            units="CFS",
            date="2026-04-01T00:00:00-08:00",
            dur_code="H",
            data_flag=" ",
        )
        assert reading.value is None

    def test_reservoir_reading_to_dict(self):
        from cdec_reservoirs_producer_data.gov.ca.water.cdec.reservoirreading import ReservoirReading
        reading = ReservoirReading(
            station_id="ORO",
            sensor_num=6,
            sensor_type="RES ELE",
            value=900.5,
            units="FEET",
            date="2026-04-01T00:00:00-08:00",
            dur_code="H",
            data_flag=" ",
        )
        d = reading.to_serializer_dict()
        assert d['station_id'] == "ORO"
        assert d['sensor_num'] == 6
        assert d['value'] == 900.5

    def test_reservoir_reading_json_roundtrip(self):
        from cdec_reservoirs_producer_data.gov.ca.water.cdec.reservoirreading import ReservoirReading
        reading = ReservoirReading(
            station_id="FOL",
            sensor_num=76,
            sensor_type="INFLOW",
            value=5200.0,
            units="CFS",
            date="2026-04-01T01:00:00-08:00",
            dur_code="H",
            data_flag=" ",
        )
        json_str = reading.to_json()
        restored = ReservoirReading.from_json(json_str)
        assert restored.station_id == "FOL"
        assert restored.sensor_num == 76
        assert restored.value == 5200.0


@pytest.mark.integration
class TestDedupLogic:
    """Test deduplication logic."""

    def test_dedup_key_format(self):
        """Dedup key should be station_id/sensor_num/date."""
        raw = MOCK_READINGS[0]
        key = f"{raw['stationId']}/{raw['SENSOR_NUM']}/{raw['date']}"
        assert key == "SHA/15/2026-4-1 0:00"

    def test_duplicate_readings_filtered(self):
        """Same station+sensor+date should be deduped."""
        seen = set()
        readings = [
            {"stationId": "SHA", "SENSOR_NUM": 15, "date": "2026-4-1 0:00", "value": 100,
             "sensorType": "STORAGE", "units": "AF", "durCode": "H", "dataFlag": " "},
            {"stationId": "SHA", "SENSOR_NUM": 15, "date": "2026-4-1 0:00", "value": 101,
             "sensorType": "STORAGE", "units": "AF", "durCode": "H", "dataFlag": " "},
        ]
        emitted = []
        for raw in readings:
            key = f"{raw['stationId']}/{raw['SENSOR_NUM']}/{raw['date']}"
            if key not in seen:
                emitted.append(raw)
                seen.add(key)
        assert len(emitted) == 1
        assert emitted[0]['value'] == 100

    def test_different_sensors_not_deduped(self):
        """Same station, different sensors should NOT be deduped."""
        seen = set()
        readings = [
            {"stationId": "SHA", "SENSOR_NUM": 15, "date": "2026-4-1 0:00"},
            {"stationId": "SHA", "SENSOR_NUM": 6, "date": "2026-4-1 0:00"},
        ]
        emitted = []
        for raw in readings:
            key = f"{raw['stationId']}/{raw['SENSOR_NUM']}/{raw['date']}"
            if key not in seen:
                emitted.append(raw)
                seen.add(key)
        assert len(emitted) == 2

    def test_different_timestamps_not_deduped(self):
        """Same station+sensor, different timestamps should NOT be deduped."""
        seen = set()
        readings = [
            {"stationId": "SHA", "SENSOR_NUM": 15, "date": "2026-4-1 0:00"},
            {"stationId": "SHA", "SENSOR_NUM": 15, "date": "2026-4-1 1:00"},
        ]
        emitted = []
        for raw in readings:
            key = f"{raw['stationId']}/{raw['SENSOR_NUM']}/{raw['date']}"
            if key not in seen:
                emitted.append(raw)
                seen.add(key)
        assert len(emitted) == 2


@pytest.mark.integration
class TestMultiStationQuery:
    """Test multi-station query efficiency."""

    def test_comma_separated_stations_in_url(self):
        api = CdecReservoirsAPI(stations="SHA,ORO,FOL")
        url = api.build_url("2026-04-01", "2026-04-02")
        assert "Stations=SHA,ORO,FOL" in url

    def test_single_station_url(self):
        api = CdecReservoirsAPI(stations="SHA")
        url = api.build_url("2026-04-01", "2026-04-02")
        assert "Stations=SHA" in url

    def test_all_default_stations_in_url(self):
        api = CdecReservoirsAPI()
        url = api.build_url("2026-04-01", "2026-04-02")
        for station in ["SHA", "ORO", "FOL", "NML", "DNP", "HTC", "SON", "MIL", "PNF"]:
            assert station in url
