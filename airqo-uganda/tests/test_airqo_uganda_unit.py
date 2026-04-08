"""
Unit tests for the AirQo Uganda air quality bridge.
Tests core functionality without external dependencies.
"""

import json
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

from airqo_uganda_producer_data import Measurement, Site
from airqo_uganda.airqo_uganda import (
    AirQoUgandaAPI,
    parse_connection_string,
    _safe_float,
    _safe_str,
)


SAMPLE_GRIDS_SUMMARY_RESPONSE = {
    "success": True,
    "message": "Successfully retrieved grids",
    "meta": {"total": 1, "limit": 30, "skip": 0, "page": 1, "totalPages": 1},
    "grids": [
        {
            "_id": "grid_001",
            "name": "kampala",
            "long_name": "Kampala",
            "network": "airqo",
            "sites": [
                {
                    "_id": "60d058c8048305120d200001",
                    "name": "Makerere University",
                    "generated_name": "site_001",
                    "formatted_name": "University Rd, Kampala, Uganda",
                    "approximate_latitude": 0.3476,
                    "approximate_longitude": 32.5825,
                    "country": "Uganda",
                    "region": "Central Region",
                    "city": "Kampala",
                    "isOnline": True,
                    "lastRawData": "2026-04-06T18:00:00.000Z",
                },
                {
                    "_id": "60d058c8048305120d200002",
                    "name": "Nakasero II",
                    "generated_name": "site_002",
                    "formatted_name": "31 Buganda Rd, Kampala, Uganda",
                    "approximate_latitude": 0.32005,
                    "approximate_longitude": 32.5718,
                    "country": "Uganda",
                    "region": "Central Region",
                    "city": "Kampala",
                    "isOnline": False,
                },
            ],
            "numberOfSites": 2,
        }
    ],
}


SAMPLE_MEASUREMENTS_RESPONSE = {
    "success": True,
    "message": "successfully returned the measurements",
    "measurements": [
        {
            "device": "aq_01",
            "device_id": "5f2036bc70223655545a0001",
            "site_id": "60d058c8048305120d200001",
            "time": "2026-04-06T18:00:00.000Z",
            "pm2_5": {"value": 45.2, "calibratedValue": 38.1},
            "pm10": {"value": 67.8, "calibratedValue": 55.0},
            "temperature": {"value": 24.5},
            "humidity": {"value": 72.0},
            "location": {"latitude": 0.3476, "longitude": 32.5825},
            "frequency": "hourly",
        },
        {
            "device": "aq_02",
            "device_id": "5f2036bc70223655545a0002",
            "site_id": "60d058c8048305120d200002",
            "time": "2026-04-06T18:00:00.000Z",
            "pm2_5": {"value": 20.99},
            "pm10": {"value": 24.60},
            "temperature": {"value": 28.3},
            "humidity": {"value": 65.0},
            "location": {"latitude": 0.32005, "longitude": 32.5718},
            "frequency": "hourly",
        },
    ],
}


SAMPLE_MEASUREMENT_MISSING_FIELDS = {
    "device": "aq_03",
    "device_id": None,
    "site_id": "60d058c8048305120d200003",
    "time": "2026-04-06T19:00:00.000Z",
    "pm2_5": None,
    "pm10": {},
    "temperature": {},
    "humidity": None,
    "location": None,
    "frequency": None,
}


@pytest.mark.unit
class TestSafeFloat:
    """Unit tests for the _safe_float helper."""

    def test_valid_float(self):
        assert _safe_float(10.5) == 10.5

    def test_valid_int(self):
        assert _safe_float(42) == 42.0

    def test_valid_string(self):
        assert _safe_float("10.5") == 10.5

    def test_none(self):
        assert _safe_float(None) is None

    def test_empty_string(self):
        assert _safe_float("") is None

    def test_null_string(self):
        assert _safe_float("null") is None

    def test_nan_string(self):
        assert _safe_float("nan") is None

    def test_invalid_string(self):
        assert _safe_float("not a number") is None

    def test_zero(self):
        assert _safe_float(0) == 0.0

    def test_negative(self):
        assert _safe_float(-3.14) == -3.14


@pytest.mark.unit
class TestSafeStr:
    """Unit tests for the _safe_str helper."""

    def test_valid_string(self):
        assert _safe_str("hello") == "hello"

    def test_none(self):
        assert _safe_str(None) is None

    def test_empty_string(self):
        assert _safe_str("") is None

    def test_whitespace_only(self):
        assert _safe_str("   ") is None

    def test_strips_whitespace(self):
        assert _safe_str("  hello  ") == "hello"


@pytest.mark.unit
class TestParseConnectionString:
    """Unit tests for parse_connection_string."""

    def test_event_hubs_connection_string(self):
        conn = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootPolicy;"
            "SharedAccessKey=abc123=;"
            "EntityPath=my-topic"
        )
        result = parse_connection_string(conn)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "my-topic"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["security.protocol"] == "SASL_SSL"

    def test_bootstrap_server_connection_string(self):
        conn = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(conn)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "test-topic"
        assert "sasl.username" not in result

    def test_empty_connection_string_returns_empty_dict(self):
        result = parse_connection_string("")
        assert "bootstrap.servers" not in result


@pytest.mark.unit
class TestBuildSitePayload:
    """Unit tests for AirQoUgandaAPI.build_site_payload."""

    def test_full_site(self):
        api = AirQoUgandaAPI()
        raw = SAMPLE_GRIDS_SUMMARY_RESPONSE["grids"][0]["sites"][0]
        payload = api.build_site_payload(raw)
        assert payload["site_id"] == "60d058c8048305120d200001"
        assert payload["name"] == "Makerere University"
        assert payload["formatted_name"] == "University Rd, Kampala, Uganda"
        assert payload["latitude"] == 0.3476
        assert payload["longitude"] == 32.5825
        assert payload["country"] == "Uganda"
        assert payload["region"] == "Central Region"
        assert payload["city"] == "Kampala"
        assert payload["is_online"] is True

    def test_offline_site(self):
        api = AirQoUgandaAPI()
        raw = SAMPLE_GRIDS_SUMMARY_RESPONSE["grids"][0]["sites"][1]
        payload = api.build_site_payload(raw)
        assert payload["is_online"] is False

    def test_site_creates_dataclass(self):
        api = AirQoUgandaAPI()
        raw = SAMPLE_GRIDS_SUMMARY_RESPONSE["grids"][0]["sites"][0]
        payload = api.build_site_payload(raw)
        site = Site(**payload)
        assert site.site_id == "60d058c8048305120d200001"
        assert site.name == "Makerere University"
        assert site.latitude == 0.3476


@pytest.mark.unit
class TestBuildMeasurementPayload:
    """Unit tests for AirQoUgandaAPI.build_measurement_payload."""

    def test_full_measurement(self):
        api = AirQoUgandaAPI()
        raw = SAMPLE_MEASUREMENTS_RESPONSE["measurements"][0]
        payload = api.build_measurement_payload(raw)
        assert payload["site_id"] == "60d058c8048305120d200001"
        assert payload["device"] == "aq_01"
        assert payload["device_id"] == "5f2036bc70223655545a0001"
        assert payload["timestamp"] == "2026-04-06T18:00:00.000Z"
        assert payload["pm2_5_raw"] == 45.2
        assert payload["pm2_5_calibrated"] == 38.1
        assert payload["pm10_raw"] == 67.8
        assert payload["pm10_calibrated"] == 55.0
        assert payload["temperature"] == 24.5
        assert payload["humidity"] == 72.0
        assert payload["latitude"] == 0.3476
        assert payload["longitude"] == 32.5825
        assert payload["frequency"] == "hourly"

    def test_measurement_with_missing_calibration(self):
        api = AirQoUgandaAPI()
        raw = SAMPLE_MEASUREMENTS_RESPONSE["measurements"][1]
        payload = api.build_measurement_payload(raw)
        assert payload["pm2_5_raw"] == 20.99
        assert payload["pm2_5_calibrated"] is None
        assert payload["pm10_raw"] == 24.60
        assert payload["pm10_calibrated"] is None

    def test_measurement_with_null_fields(self):
        api = AirQoUgandaAPI()
        payload = api.build_measurement_payload(SAMPLE_MEASUREMENT_MISSING_FIELDS)
        assert payload["device"] == "aq_03"
        assert payload["device_id"] is None
        assert payload["pm2_5_raw"] is None
        assert payload["pm2_5_calibrated"] is None
        assert payload["pm10_raw"] is None
        assert payload["pm10_calibrated"] is None
        assert payload["temperature"] is None
        assert payload["humidity"] is None
        assert payload["latitude"] is None
        assert payload["longitude"] is None
        assert payload["frequency"] is None

    def test_measurement_creates_dataclass(self):
        api = AirQoUgandaAPI()
        raw = SAMPLE_MEASUREMENTS_RESPONSE["measurements"][0]
        payload = api.build_measurement_payload(raw)
        measurement = Measurement(**payload)
        assert measurement.site_id == "60d058c8048305120d200001"
        assert measurement.pm2_5_raw == 45.2
        assert measurement.pm2_5_calibrated == 38.1


@pytest.mark.unit
class TestDeduplication:
    """Unit tests for measurement deduplication."""

    def test_new_measurement_should_emit(self):
        api = AirQoUgandaAPI()
        assert api.should_emit_measurement("aq_01", "2026-04-06T18:00:00Z") is True

    def test_duplicate_measurement_should_not_emit(self):
        api = AirQoUgandaAPI()
        api.remember_measurement("aq_01", "2026-04-06T18:00:00Z")
        assert api.should_emit_measurement("aq_01", "2026-04-06T18:00:00Z") is False

    def test_new_timestamp_should_emit(self):
        api = AirQoUgandaAPI()
        api.remember_measurement("aq_01", "2026-04-06T18:00:00Z")
        assert api.should_emit_measurement("aq_01", "2026-04-06T19:00:00Z") is True


@pytest.mark.unit
class TestFetchSites:
    """Unit tests for AirQoUgandaAPI.fetch_sites."""

    def test_fetch_sites_parses_grids(self):
        import requests_mock

        api = AirQoUgandaAPI()
        with requests_mock.Mocker() as m:
            m.get(
                "https://api.airqo.net/api/v2/devices/grids/summary",
                json=SAMPLE_GRIDS_SUMMARY_RESPONSE,
            )
            sites = api.fetch_sites()
        assert len(sites) == 2
        assert sites[0]["_id"] == "60d058c8048305120d200001"
        assert sites[1]["_id"] == "60d058c8048305120d200002"

    def test_fetch_sites_deduplicates(self):
        import requests_mock

        duped_response = {
            "success": True,
            "meta": {"total": 1, "limit": 30, "skip": 0, "page": 1, "totalPages": 1},
            "grids": [
                {
                    "_id": "grid_1",
                    "sites": [{"_id": "site_1", "name": "A"}],
                },
                {
                    "_id": "grid_2",
                    "sites": [{"_id": "site_1", "name": "A"}],
                },
            ],
        }
        api = AirQoUgandaAPI()
        with requests_mock.Mocker() as m:
            m.get(
                "https://api.airqo.net/api/v2/devices/grids/summary",
                json=duped_response,
            )
            sites = api.fetch_sites()
        assert len(sites) == 1


@pytest.mark.unit
class TestFetchMeasurements:
    """Unit tests for AirQoUgandaAPI.fetch_measurements."""

    def test_fetch_measurements_with_key(self):
        import requests_mock

        api = AirQoUgandaAPI(api_key="test-key")
        with requests_mock.Mocker() as m:
            m.get(
                "https://api.airqo.net/api/v2/devices/measurements",
                json=SAMPLE_MEASUREMENTS_RESPONSE,
            )
            measurements = api.fetch_measurements()
        assert len(measurements) == 2

    def test_fetch_measurements_without_key(self):
        api = AirQoUgandaAPI(api_key="")
        measurements = api.fetch_measurements()
        assert len(measurements) == 0

    def test_fetch_measurements_api_failure(self):
        import requests_mock

        api = AirQoUgandaAPI(api_key="test-key")
        with requests_mock.Mocker() as m:
            m.get(
                "https://api.airqo.net/api/v2/devices/measurements",
                json={"success": False, "message": "API Error"},
            )
            measurements = api.fetch_measurements()
        assert len(measurements) == 0


@pytest.mark.unit
class TestTimestampParsing:
    """Unit tests for timestamp handling in measurement payloads."""

    def test_iso_timestamp(self):
        api = AirQoUgandaAPI()
        raw = {"time": "2026-04-06T18:00:00.000Z", "device": "x", "site_id": "s"}
        payload = api.build_measurement_payload(raw)
        assert payload["timestamp"] == "2026-04-06T18:00:00.000Z"

    def test_fallback_to_timestamp_field(self):
        api = AirQoUgandaAPI()
        raw = {"timestamp": "2026-04-06T19:00:00Z", "device": "x", "site_id": "s"}
        payload = api.build_measurement_payload(raw)
        assert payload["timestamp"] == "2026-04-06T19:00:00Z"

    def test_missing_timestamp(self):
        api = AirQoUgandaAPI()
        raw = {"device": "x", "site_id": "s"}
        payload = api.build_measurement_payload(raw)
        assert payload["timestamp"] == ""
