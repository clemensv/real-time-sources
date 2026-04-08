"""Unit tests for the LAQN London bridge."""

from datetime import date

import pytest

from laqn_london.laqn_london import (
    LAQNLondonAPI,
    _coerce_list,
    _format_api_date,
    _parse_float_or_none,
)


@pytest.mark.unit
class TestLAQNLondonAPIInitialization:
    """API initialization and basic configuration."""

    def test_init_uses_http_base_url(self):
        api = LAQNLondonAPI()
        assert api.base_url == "http://api.erg.ic.ac.uk/AirQuality/"

    def test_init_creates_session(self):
        api = LAQNLondonAPI()
        assert api.session is not None
        assert hasattr(api.session, "get")


@pytest.mark.unit
class TestConnectionStringParsing:
    """Connection string parsing mirrors the repo standard."""

    def test_parse_event_hubs_connection_string(self):
        api = LAQNLondonAPI()
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=laqn-london"
        )
        result = api.parse_connection_string(connection_string)

        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "laqn-london"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == connection_string
        assert result["security.protocol"] == "SASL_SSL"
        assert result["sasl.mechanism"] == "PLAIN"

    def test_parse_bootstrap_server_connection_string(self):
        api = LAQNLondonAPI()
        result = api.parse_connection_string("BootstrapServer=broker:9092;EntityPath=test-topic")

        assert result["bootstrap.servers"] == "broker:9092"
        assert result["kafka_topic"] == "test-topic"
        assert "sasl.username" not in result

    def test_invalid_connection_string_raises_value_error(self):
        api = LAQNLondonAPI()
        with pytest.raises(ValueError, match="Invalid connection string format"):
            api.parse_connection_string("EndpointWithoutEquals;EntityPathAlsoInvalid")


@pytest.mark.unit
class TestHelpers:
    """Date and value helpers for LAQN payloads."""

    def test_format_api_date(self):
        assert _format_api_date(date(2026, 4, 7)) == "2026-04-07"

    def test_parse_float_or_none(self):
        assert _parse_float_or_none("35.5") == 35.5
        assert _parse_float_or_none("  ") is None
        assert _parse_float_or_none("") is None
        assert _parse_float_or_none(None) is None

    def test_coerce_list(self):
        assert _coerce_list(None) == []
        assert _coerce_list(" ") == []
        assert _coerce_list({"a": 1}) == [{"a": 1}]
        assert _coerce_list([1, 2]) == [1, 2]

    def test_is_active_site(self):
        assert LAQNLondonAPI.is_active_site({"@SiteCode": "BX1"})
        assert LAQNLondonAPI.is_active_site({"@DateClosed": ""})
        assert not LAQNLondonAPI.is_active_site({"@DateClosed": "2018-01-01 00:00:00"})

    def test_normalize_measurement_skips_blank_values(self):
        measurement = LAQNLondonAPI.normalize_measurement(
            "BX1",
            {
                "@SpeciesCode": "NO2",
                "@MeasurementDateGMT": "2026-04-07 00:00:00",
                "@Value": "",
            },
        )
        assert measurement is None

    def test_extract_daily_index_records_skips_whitespace_species(self):
        records = LAQNLondonAPI.extract_daily_index_records(
            {
                "DailyAirQualityIndex": {
                    "LocalAuthority": [
                        {
                            "Site": [
                                {
                                    "@SiteCode": "BX1",
                                    "@BulletinDate": "2026-04-07 00:00:00",
                                    "Species": " ",
                                }
                            ]
                        }
                    ]
                }
            }
        )
        assert records == []
