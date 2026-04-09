"""
Unit tests for USGS NWIS Water Quality bridge.
Tests that don't require external dependencies or API calls.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

from usgs_nwis_wq.usgs_nwis_wq import (
    USGSWaterQualityPoller,
    WQ_PARAMETER_CODES,
    ALL_WQ_PARAM_CODES,
    STATE_CODES,
    parse_connection_string,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

SAMPLE_WATERML_RESPONSE = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://waterservices.usgs.gov/nwis/iv/",
            "criteria": {},
            "note": []
        },
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA",
                    "siteCode": [
                        {"value": "01646500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {"zoneOffset": "-05:00", "zoneAbbreviation": "EST"},
                        "daylightSavingsTimeZone": {"zoneOffset": "-04:00", "zoneAbbreviation": "EDT"},
                        "siteUsesDaylightSavingsTime": True
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 38.94977778,
                            "longitude": -77.12763889
                        },
                        "localSiteXY": []
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "020700081005", "name": "hucCd"},
                        {"value": "24", "name": "stateCd"},
                        {"value": "24031", "name": "countyCd"}
                    ]
                },
                "variable": {
                    "variableCode": [
                        {"value": "00300", "network": "NWIS", "vocabulary": "NWIS:UnitValues",
                         "variableID": 45807042, "default": True}
                    ],
                    "variableName": "Dissolved oxygen, water, unfiltered, mg/L",
                    "variableDescription": "Dissolved oxygen, water, unfiltered, milligrams per liter",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "mg/l"},
                    "options": {"option": [{"name": "Statistic", "optionCode": "00000"}]},
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807042"
                },
                "values": [
                    {
                        "value": [
                            {"value": "10.5", "qualifiers": ["P"],
                             "dateTime": "2024-11-15T11:45:00.000-05:00"},
                            {"value": "10.6", "qualifiers": ["P"],
                             "dateTime": "2024-11-15T12:00:00.000-05:00"},
                            {"value": "10.4", "qualifiers": ["A"],
                             "dateTime": "2024-11-15T12:15:00.000-05:00"}
                        ],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "sonde", "methodID": 12345}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": []
                    }
                ],
                "name": "USGS:01646500:00300:00000"
            },
            {
                "sourceInfo": {
                    "siteName": "POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA",
                    "siteCode": [
                        {"value": "01646500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {"zoneOffset": "-05:00", "zoneAbbreviation": "EST"},
                        "daylightSavingsTimeZone": {"zoneOffset": "-04:00", "zoneAbbreviation": "EDT"},
                        "siteUsesDaylightSavingsTime": True
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 38.94977778,
                            "longitude": -77.12763889
                        },
                        "localSiteXY": []
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "020700081005", "name": "hucCd"},
                        {"value": "24", "name": "stateCd"},
                        {"value": "24031", "name": "countyCd"}
                    ]
                },
                "variable": {
                    "variableCode": [
                        {"value": "00010", "network": "NWIS", "vocabulary": "NWIS:UnitValues",
                         "variableID": 45807099, "default": True}
                    ],
                    "variableName": "Temperature, water, &#176;C",
                    "variableDescription": "Temperature, water, degrees Celsius",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "deg C"},
                    "options": {"option": [{"name": "Statistic", "optionCode": "00000"}]},
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807099"
                },
                "values": [
                    {
                        "value": [
                            {"value": "16.6", "qualifiers": ["P"],
                             "dateTime": "2024-11-15T11:45:00.000-05:00"},
                            {"value": "-999999.0", "qualifiers": ["P"],
                             "dateTime": "2024-11-15T12:00:00.000-05:00"}
                        ],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "sonde", "methodID": 12346}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": []
                    }
                ],
                "name": "USGS:01646500:00010:00000"
            }
        ]
    }
}


# ---------------------------------------------------------------------------
# Tests: Initialization
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestPollerInitialization:
    """Test USGSWaterQualityPoller initialization."""

    def test_init_without_kafka(self):
        poller = USGSWaterQualityPoller()
        assert poller.site_producer is None
        assert poller.readings_producer is None
        assert poller.states == STATE_CODES

    def test_init_with_custom_states(self):
        poller = USGSWaterQualityPoller(states=['MD', 'VA'])
        assert poller.states == ['MD', 'VA']

    def test_init_with_sites(self):
        poller = USGSWaterQualityPoller(sites=['01646500', '01578310'])
        assert poller.sites == ['01646500', '01578310']

    def test_init_with_custom_parameter_codes(self):
        poller = USGSWaterQualityPoller(parameter_codes='00300,00010')
        assert poller.parameter_codes == '00300,00010'

    def test_init_default_parameter_codes(self):
        poller = USGSWaterQualityPoller()
        assert poller.parameter_codes == ALL_WQ_PARAM_CODES

    @patch('usgs_nwis_wq.usgs_nwis_wq.USGSWaterQualitySitesEventProducer')
    @patch('usgs_nwis_wq.usgs_nwis_wq.USGSWaterQualityReadingsEventProducer')
    @patch('usgs_nwis_wq.usgs_nwis_wq.Producer')
    def test_init_with_kafka_config(self, mock_producer_cls, mock_readings_prod, mock_site_prod):
        config = {'bootstrap.servers': 'localhost:9092'}
        poller = USGSWaterQualityPoller(kafka_config=config, kafka_topic='test-topic')
        mock_producer_cls.assert_called_once_with(config)
        assert poller.kafka_topic == 'test-topic'


# ---------------------------------------------------------------------------
# Tests: Parameter codes
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParameterCodes:
    """Test water quality parameter code configuration."""

    def test_wq_parameter_codes_dict(self):
        assert isinstance(WQ_PARAMETER_CODES, dict)
        assert '00010' in WQ_PARAMETER_CODES
        assert '00300' in WQ_PARAMETER_CODES
        assert '00400' in WQ_PARAMETER_CODES
        assert '00095' in WQ_PARAMETER_CODES
        assert '63680' in WQ_PARAMETER_CODES
        assert '99133' in WQ_PARAMETER_CODES

    def test_all_codes_are_5_digits(self):
        for code in WQ_PARAMETER_CODES:
            assert len(code) == 5, f"Parameter code {code} is not 5 digits"
            assert code.isdigit(), f"Parameter code {code} is not numeric"

    def test_all_wq_param_codes_string(self):
        assert isinstance(ALL_WQ_PARAM_CODES, str)
        codes = ALL_WQ_PARAM_CODES.split(',')
        assert len(codes) == len(WQ_PARAMETER_CODES)

    def test_parameter_names_are_strings(self):
        for code, name in WQ_PARAMETER_CODES.items():
            assert isinstance(name, str)
            assert len(name) > 0


# ---------------------------------------------------------------------------
# Tests: State codes
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStateCodes:
    """Test state code list."""

    def test_state_codes_list(self):
        assert isinstance(STATE_CODES, list)
        assert len(STATE_CODES) > 50

    def test_common_states(self):
        for state in ['CA', 'NY', 'TX', 'FL', 'MD', 'VA']:
            assert state in STATE_CODES

    def test_territories(self):
        assert 'PR' in STATE_CODES
        assert 'GU' in STATE_CODES
        assert 'VI' in STATE_CODES

    def test_codes_uppercase_2char(self):
        for code in STATE_CODES:
            assert code.isupper()
            assert len(code) == 2


# ---------------------------------------------------------------------------
# Tests: URL building
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestURLBuilding:
    """Test API URL construction."""

    def test_url_by_state(self):
        url = USGSWaterQualityPoller.build_api_url(state_cd='MD')
        assert 'stateCd=MD' in url
        assert 'format=json' in url
        assert 'parameterCd=' in url

    def test_url_by_sites(self):
        url = USGSWaterQualityPoller.build_api_url(sites=['01646500', '01578310'])
        assert 'sites=01646500,01578310' in url
        assert 'stateCd' not in url

    def test_url_custom_period(self):
        url = USGSWaterQualityPoller.build_api_url(state_cd='VA', period='PT4H')
        assert 'period=PT4H' in url

    def test_url_custom_params(self):
        url = USGSWaterQualityPoller.build_api_url(state_cd='CA', parameter_codes='00300,00010')
        assert 'parameterCd=00300,00010' in url

    def test_url_uses_https(self):
        url = USGSWaterQualityPoller.build_api_url(state_cd='NY')
        assert url.startswith('https://')

    def test_base_url(self):
        assert USGSWaterQualityPoller.BASE_URL == "https://waterservices.usgs.gov/nwis/iv/"


# ---------------------------------------------------------------------------
# Tests: WaterML parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestWaterMLParsing:
    """Test WaterML 2.0 JSON response parsing."""

    def test_parse_sites(self):
        sites, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        assert len(sites) == 1
        site = sites[0]
        assert site.site_number == '01646500'
        assert site.site_name == 'POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA'
        assert site.agency_code == 'USGS'

    def test_parse_site_location(self):
        sites, _ = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        site = sites[0]
        assert abs(site.latitude - 38.94977778) < 0.0001
        assert abs(site.longitude - (-77.12763889)) < 0.0001

    def test_parse_site_properties(self):
        sites, _ = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        site = sites[0]
        assert site.site_type == 'ST'
        assert site.state_code == '24'
        assert site.county_code == '24031'
        assert site.huc_code == '020700081005'

    def test_parse_site_dedup(self):
        """Same site appearing in multiple timeSeries should only produce one MonitoringSite."""
        sites, _ = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        assert len(sites) == 1

    def test_parse_readings_count(self):
        _, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        # 3 DO readings + 2 temp readings = 5
        assert len(readings) == 5

    def test_parse_reading_do(self):
        _, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        do_readings = [r for r in readings if r.parameter_code == '00300']
        assert len(do_readings) == 3
        assert do_readings[0].value == 10.5
        assert do_readings[0].unit == 'mg/l'
        assert do_readings[0].qualifier == 'P'

    def test_parse_reading_temperature(self):
        _, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        temp_readings = [r for r in readings if r.parameter_code == '00010']
        assert len(temp_readings) == 2
        assert temp_readings[0].value == 16.6
        assert temp_readings[0].unit == 'deg C'

    def test_parse_no_data_value_becomes_null(self):
        """noDataValue sentinel (-999999.0) should be parsed as None."""
        _, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        temp_readings = [r for r in readings if r.parameter_code == '00010']
        # Second temp reading has -999999.0
        assert temp_readings[1].value is None

    def test_parse_datetime_utc_conversion(self):
        _, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        # First DO reading: 2024-11-15T11:45:00-05:00 → 2024-11-15T16:45:00+00:00
        dt = datetime.fromisoformat(readings[0].date_time)
        assert dt.tzinfo is not None
        assert dt.hour == 16
        assert dt.minute == 45

    def test_parse_html_entities(self):
        """Variable names with HTML entities (&#176;) should be unescaped."""
        _, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        temp_readings = [r for r in readings if r.parameter_code == '00010']
        assert '°' in temp_readings[0].parameter_name or 'degrees' in temp_readings[0].parameter_name.lower()

    def test_parse_reading_site_name(self):
        _, readings = USGSWaterQualityPoller.parse_waterml_response(SAMPLE_WATERML_RESPONSE)
        for r in readings:
            assert r.site_name == 'POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA'

    def test_parse_empty_response(self):
        empty = {"value": {"timeSeries": []}}
        sites, readings = USGSWaterQualityPoller.parse_waterml_response(empty)
        assert len(sites) == 0
        assert len(readings) == 0

    def test_parse_missing_timeseries_key(self):
        no_ts = {"value": {}}
        sites, readings = USGSWaterQualityPoller.parse_waterml_response(no_ts)
        assert len(sites) == 0
        assert len(readings) == 0

    def test_parse_empty_values(self):
        """TimeSeries entry with empty values array should produce no readings."""
        data = {
            "value": {
                "timeSeries": [{
                    "sourceInfo": {
                        "siteName": "Test Site",
                        "siteCode": [{"value": "12345678", "agencyCode": "USGS"}],
                        "geoLocation": {"geogLocation": {"latitude": 40.0, "longitude": -75.0}},
                        "siteProperty": [],
                        "timeZoneInfo": {
                            "defaultTimeZone": {"zoneOffset": "-05:00"},
                            "siteUsesDaylightSavingsTime": False
                        }
                    },
                    "variable": {
                        "variableCode": [{"value": "00300"}],
                        "variableName": "DO",
                        "variableDescription": "Dissolved oxygen",
                        "unit": {"unitCode": "mg/l"},
                        "noDataValue": -999999.0
                    },
                    "values": [{"value": [], "qualifier": [], "method": []}]
                }]
            }
        }
        sites, readings = USGSWaterQualityPoller.parse_waterml_response(data)
        assert len(sites) == 1
        assert len(readings) == 0


# ---------------------------------------------------------------------------
# Tests: Deduplication
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDeduplication:
    """Test dedup logic."""

    def test_is_duplicate_returns_false_for_new(self):
        poller = USGSWaterQualityPoller()
        assert not poller.is_duplicate({}, '01646500', '00300', '2024-11-15T16:45:00+00:00')

    def test_is_duplicate_returns_true_for_old(self):
        poller = USGSWaterQualityPoller()
        last = {'01646500/00300': '2024-11-15T17:00:00+00:00'}
        assert poller.is_duplicate(last, '01646500', '00300', '2024-11-15T16:45:00+00:00')

    def test_is_duplicate_exact_match(self):
        poller = USGSWaterQualityPoller()
        last = {'01646500/00300': '2024-11-15T16:45:00+00:00'}
        assert poller.is_duplicate(last, '01646500', '00300', '2024-11-15T16:45:00+00:00')

    def test_update_last_polled(self):
        poller = USGSWaterQualityPoller()
        last = {}
        poller.update_last_polled(last, '01646500', '00300', '2024-11-15T16:45:00+00:00')
        assert last['01646500/00300'] == '2024-11-15T16:45:00+00:00'

    def test_update_last_polled_newer(self):
        poller = USGSWaterQualityPoller()
        last = {'01646500/00300': '2024-11-15T16:00:00+00:00'}
        poller.update_last_polled(last, '01646500', '00300', '2024-11-15T16:45:00+00:00')
        assert last['01646500/00300'] == '2024-11-15T16:45:00+00:00'

    def test_update_last_polled_older_no_change(self):
        poller = USGSWaterQualityPoller()
        last = {'01646500/00300': '2024-11-15T17:00:00+00:00'}
        poller.update_last_polled(last, '01646500', '00300', '2024-11-15T16:45:00+00:00')
        assert last['01646500/00300'] == '2024-11-15T17:00:00+00:00'


# ---------------------------------------------------------------------------
# Tests: State persistence
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStatePersistence:
    """Test last-polled-times file handling."""

    def test_load_nonexistent_file(self):
        poller = USGSWaterQualityPoller(last_polled_file='nonexistent_path_abc.json')
        result = poller.load_last_polled_times()
        assert result == {}

    def test_load_no_file_configured(self):
        poller = USGSWaterQualityPoller(last_polled_file=None)
        result = poller.load_last_polled_times()
        assert result == {}

    def test_save_no_file_configured(self):
        """save should be a no-op when no file is configured."""
        poller = USGSWaterQualityPoller(last_polled_file=None)
        poller.save_last_polled_times({'test': 'value'})  # should not raise


# ---------------------------------------------------------------------------
# Tests: Connection string parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestConnectionStringParsing:
    """Test Kafka connection string parsing."""

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=my-topic"
        config, topic = parse_connection_string(cs)
        assert 'myns.servicebus.windows.net:9093' in config['bootstrap.servers']
        assert topic == 'my-topic'
        assert config['security.protocol'] == 'SASL_SSL'

    def test_simple_bootstrap_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        config, topic = parse_connection_string(cs)
        assert config['bootstrap.servers'] == 'localhost:9092'
        assert topic == 'test-topic'

    @patch.dict('os.environ', {'KAFKA_ENABLE_TLS': 'false'})
    def test_bootstrap_no_tls(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        config, topic = parse_connection_string(cs)
        assert config['security.protocol'] == 'PLAINTEXT'


# ---------------------------------------------------------------------------
# Tests: Multi-site and edge cases in parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParsingEdgeCases:
    """Test edge cases in WaterML parsing."""

    def test_parse_non_numeric_value(self):
        """Non-numeric values should result in value=None."""
        data = {
            "value": {
                "timeSeries": [{
                    "sourceInfo": {
                        "siteName": "Test",
                        "siteCode": [{"value": "99999999", "agencyCode": "USGS"}],
                        "geoLocation": {"geogLocation": {"latitude": 40.0, "longitude": -75.0}},
                        "siteProperty": [],
                        "timeZoneInfo": {
                            "defaultTimeZone": {"zoneOffset": "-05:00"},
                            "siteUsesDaylightSavingsTime": False
                        }
                    },
                    "variable": {
                        "variableCode": [{"value": "00400"}],
                        "variableName": "pH",
                        "variableDescription": "pH, water",
                        "unit": {"unitCode": "std units"},
                        "noDataValue": -999999.0
                    },
                    "values": [{
                        "value": [
                            {"value": "Eqp", "qualifiers": ["P"],
                             "dateTime": "2024-11-15T12:00:00.000-05:00"}
                        ]
                    }]
                }]
            }
        }
        _, readings = USGSWaterQualityPoller.parse_waterml_response(data)
        assert len(readings) == 1
        assert readings[0].value is None
        assert readings[0].parameter_code == '00400'

    def test_parse_multiple_sites(self):
        """Response with multiple distinct sites should produce separate MonitoringSites."""
        data = {
            "value": {
                "timeSeries": [
                    {
                        "sourceInfo": {
                            "siteName": "Site A",
                            "siteCode": [{"value": "11111111", "agencyCode": "USGS"}],
                            "geoLocation": {"geogLocation": {"latitude": 40.0, "longitude": -75.0}},
                            "siteProperty": [],
                            "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "-05:00"}, "siteUsesDaylightSavingsTime": False}
                        },
                        "variable": {
                            "variableCode": [{"value": "00300"}],
                            "variableName": "DO", "variableDescription": "DO",
                            "unit": {"unitCode": "mg/l"}, "noDataValue": -999999.0
                        },
                        "values": [{"value": [{"value": "8.0", "qualifiers": ["P"], "dateTime": "2024-11-15T12:00:00.000-05:00"}]}]
                    },
                    {
                        "sourceInfo": {
                            "siteName": "Site B",
                            "siteCode": [{"value": "22222222", "agencyCode": "USGS"}],
                            "geoLocation": {"geogLocation": {"latitude": 41.0, "longitude": -76.0}},
                            "siteProperty": [],
                            "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "-05:00"}, "siteUsesDaylightSavingsTime": False}
                        },
                        "variable": {
                            "variableCode": [{"value": "00010"}],
                            "variableName": "Temp", "variableDescription": "Temperature",
                            "unit": {"unitCode": "deg C"}, "noDataValue": -999999.0
                        },
                        "values": [{"value": [{"value": "15.0", "qualifiers": ["A"], "dateTime": "2024-11-15T12:00:00.000-05:00"}]}]
                    }
                ]
            }
        }
        sites, readings = USGSWaterQualityPoller.parse_waterml_response(data)
        assert len(sites) == 2
        assert {s.site_number for s in sites} == {'11111111', '22222222'}
        assert len(readings) == 2

    def test_parse_missing_qualifier(self):
        """Readings without qualifiers should have qualifier=None."""
        data = {
            "value": {
                "timeSeries": [{
                    "sourceInfo": {
                        "siteName": "Test",
                        "siteCode": [{"value": "33333333", "agencyCode": "USGS"}],
                        "geoLocation": {"geogLocation": {"latitude": 40.0, "longitude": -75.0}},
                        "siteProperty": [],
                        "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "+00:00"}, "siteUsesDaylightSavingsTime": False}
                    },
                    "variable": {
                        "variableCode": [{"value": "00095"}],
                        "variableName": "SC", "variableDescription": "Specific Conductance",
                        "unit": {"unitCode": "uS/cm"}, "noDataValue": -999999.0
                    },
                    "values": [{
                        "value": [{"value": "500", "qualifiers": [], "dateTime": "2024-11-15T12:00:00.000+00:00"}]
                    }]
                }]
            }
        }
        _, readings = USGSWaterQualityPoller.parse_waterml_response(data)
        assert len(readings) == 1
        assert readings[0].qualifier is None
        assert readings[0].value == 500.0

    def test_parse_null_value_entry(self):
        """value key is None (rare but possible)."""
        data = {
            "value": {
                "timeSeries": [{
                    "sourceInfo": {
                        "siteName": "Test",
                        "siteCode": [{"value": "44444444", "agencyCode": "USGS"}],
                        "geoLocation": {"geogLocation": {"latitude": 40.0, "longitude": -75.0}},
                        "siteProperty": [],
                        "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "+00:00"}, "siteUsesDaylightSavingsTime": False}
                    },
                    "variable": {
                        "variableCode": [{"value": "63680"}],
                        "variableName": "Turbidity",
                        "variableDescription": "Turbidity FNU",
                        "unit": {"unitCode": "FNU"},
                        "noDataValue": -999999.0
                    },
                    "values": [{
                        "value": [{"value": None, "qualifiers": ["P"], "dateTime": "2024-11-15T12:00:00.000+00:00"}]
                    }]
                }]
            }
        }
        _, readings = USGSWaterQualityPoller.parse_waterml_response(data)
        assert len(readings) == 1
        assert readings[0].value is None

    def test_parse_missing_datetime_skips_reading(self):
        """Entries without dateTime should be skipped."""
        data = {
            "value": {
                "timeSeries": [{
                    "sourceInfo": {
                        "siteName": "Test",
                        "siteCode": [{"value": "55555555", "agencyCode": "USGS"}],
                        "geoLocation": {"geogLocation": {"latitude": 40.0, "longitude": -75.0}},
                        "siteProperty": [],
                        "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "+00:00"}, "siteUsesDaylightSavingsTime": False}
                    },
                    "variable": {
                        "variableCode": [{"value": "00300"}],
                        "variableName": "DO", "variableDescription": "DO",
                        "unit": {"unitCode": "mg/l"}, "noDataValue": -999999.0
                    },
                    "values": [{
                        "value": [{"value": "9.0", "qualifiers": ["P"], "dateTime": ""}]
                    }]
                }]
            }
        }
        _, readings = USGSWaterQualityPoller.parse_waterml_response(data)
        assert len(readings) == 0

    def test_parse_no_geo_location(self):
        """Sites without geoLocation should have None lat/lon."""
        data = {
            "value": {
                "timeSeries": [{
                    "sourceInfo": {
                        "siteName": "No Geo",
                        "siteCode": [{"value": "66666666", "agencyCode": "USGS"}],
                        "geoLocation": {"geogLocation": {}, "localSiteXY": []},
                        "siteProperty": [],
                        "timeZoneInfo": {"defaultTimeZone": {"zoneOffset": "+00:00"}, "siteUsesDaylightSavingsTime": False}
                    },
                    "variable": {
                        "variableCode": [{"value": "00300"}],
                        "variableName": "DO", "variableDescription": "DO",
                        "unit": {"unitCode": "mg/l"}, "noDataValue": -999999.0
                    },
                    "values": [{"value": []}]
                }]
            }
        }
        sites, _ = USGSWaterQualityPoller.parse_waterml_response(data)
        assert len(sites) == 1
        assert sites[0].latitude is None
        assert sites[0].longitude is None
