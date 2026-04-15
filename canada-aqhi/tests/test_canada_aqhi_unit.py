"""Unit tests for the Canada AQHI bridge."""

from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import requests

from canada_aqhi.canada_aqhi import (
    COMMUNITY_GEOJSON_URL,
    STATION_GEOJSON_URL,
    CanadaAQHIBridge,
    aqhi_category,
    canonicalize_feed_url,
    create_retrying_session,
    forecast_date_for_period,
    normalize_provinces,
    parse_connection_string,
    province_candidates_for_feed,
)


OBSERVATION_XML = """<?xml version='1.0' encoding='utf-8'?>
<conditionAirQuality productHeader="AQ_OBS">
  <region nameEn="Burin" nameFr="Burin">AADCE</region>
  <dateStamp name="aqObserved" zoneEn="NDT" zoneFr="HAT">
    <year>2026</year>
    <month nameEn="April" nameFr="avril">4</month>
    <day nameEn="Wednesday" nameFr="mercredi">8</day>
    <hour clock="12h" ampm="AM">8</hour>
    <minute>30</minute>
    <second/>
    <UTCStamp>20260408110000</UTCStamp>
    <textSummary lang="EN">8:30 AM NDT Wednesday 8 April 2026</textSummary>
  </dateStamp>
  <airQualityHealthIndex>1.9</airQualityHealthIndex>
  <specialNotes/>
</conditionAirQuality>
"""

FORECAST_XML = """<?xml version="1.0" encoding="ISO-8859-1"?>
<forecastAirQuality productHeader="AQ_FCST" status="issued">
  <region nameEn="Burin" nameFr="Burin">AADCE</region>
  <dateStamp name="aqForecastIssued" zoneEn="NDT" zoneFr="HAT">
    <year>2026</year>
    <month nameEn="April" nameFr="avril">4</month>
    <day nameEn="Wednesday" nameFr="mercredi">8</day>
    <hour clock="12h" ampm="AM">6</hour>
    <minute>0</minute>
    <second/>
    <UTCStamp>20260408083000</UTCStamp>
  </dateStamp>
  <forecastGroup>
    <forecast periodID="1">
      <period forecastName="Today" lang="EN">Wednesday</period>
      <airQualityHealthIndex>2</airQualityHealthIndex>
    </forecast>
    <forecast periodID="2">
      <period forecastName="Tonight" lang="EN">Wednesday night</period>
      <airQualityHealthIndex>2</airQualityHealthIndex>
    </forecast>
    <forecast periodID="3">
      <period forecastName="Tomorrow" lang="EN">Thursday</period>
      <airQualityHealthIndex>3</airQualityHealthIndex>
    </forecast>
    <forecast periodID="4">
      <period forecastName="Tomorrow Night" lang="EN">Thursday night</period>
      <airQualityHealthIndex>4</airQualityHealthIndex>
    </forecast>
  </forecastGroup>
</forecastAirQuality>
"""


@pytest.mark.unit
class TestConnectionStringParsing:
    def test_parse_event_hubs_connection_string(self):
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = parse_connection_string(connection_string)

        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myeventhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == connection_string

    def test_parse_plain_bootstrap_server_connection_string(self):
        result = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=topic1")

        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "topic1"
        assert "sasl.username" not in result

    def test_invalid_connection_string_raises(self):
        with pytest.raises(ValueError, match="Invalid connection string format"):
            parse_connection_string("EndpointWithoutEquals")

    def test_create_retrying_session(self):
        session = create_retrying_session()
        https_adapter = session.get_adapter("https://dd.weather.gc.ca")

        assert session.headers["User-Agent"] == "GitHub-Copilot-CLI/1.0"
        assert https_adapter.max_retries.total == 3
        assert https_adapter.max_retries.backoff_factor == 1


@pytest.mark.unit
class TestAQHICategoryMapping:
    def test_category_low(self):
        assert aqhi_category(2.7) == "Low"

    def test_category_moderate(self):
        assert aqhi_category(5) == "Moderate"

    def test_category_high(self):
        assert aqhi_category(8) == "High"

    def test_category_very_high(self):
        assert aqhi_category(10.5) == "Very High"

    def test_category_unknown(self):
        assert aqhi_category(None) == "Unknown"


@pytest.mark.unit
class TestProvinceHandling:
    def test_normalize_provinces(self):
        assert normalize_provinces("nl,ns,ON") == ["NL", "NS", "ON"]

    def test_invalid_province_raises(self):
        with pytest.raises(ValueError, match="Unsupported provinces"):
            normalize_provinces("ON,XX")

    def test_province_candidates_for_feed(self):
        assert province_candidates_for_feed(
            "http://dd.weather.gc.ca/air_quality/aqhi/ont/observation/realtime/xml/AQ_OBS_FAFFD_CURRENT.xml"
        ) == {"ON"}
        assert province_candidates_for_feed(
            "http://dd.weather.gc.ca/air_quality/aqhi/atl/forecast/realtime/xml/AQ_FCST_AADCE_CURRENT.xml"
        ) == {"NB", "NL", "NS", "PE"}

    def test_canonicalize_feed_url(self):
        assert canonicalize_feed_url(
            "http://dd.weather.gc.ca/air_quality/aqhi/ont/observation/realtime/xml/AQ_OBS_FAFFD_CURRENT.xml"
        ) == "https://dd.weather.gc.ca/today/air_quality/aqhi/ont/observation/realtime/xml/AQ_OBS_FAFFD_CURRENT.xml"


@pytest.mark.unit
class TestDateHandling:
    def test_forecast_date_for_period(self):
        publication = datetime(2026, 4, 8, 8, 30, tzinfo=timezone.utc)

        assert forecast_date_for_period(publication, 1) == "20260408"
        assert forecast_date_for_period(publication, 2) == "20260408"
        assert forecast_date_for_period(publication, 3) == "20260409"
        assert forecast_date_for_period(publication, 4) == "20260409"


@pytest.mark.unit
class TestXMLParsing:
    def test_parse_observation_xml(self):
        parsed = CanadaAQHIBridge.parse_observation_xml(OBSERVATION_XML)

        assert parsed["community_name"] == "Burin"
        assert parsed["observation_datetime"] == "2026-04-08T11:00:00Z"
        assert parsed["aqhi"] == pytest.approx(1.9)
        assert parsed["aqhi_category"] == "Low"

    def test_parse_forecast_xml(self):
        parsed = CanadaAQHIBridge.parse_forecast_xml(FORECAST_XML)

        assert parsed["community_name"] == "Burin"
        assert parsed["publication_datetime"] == "2026-04-08T08:30:00Z"
        assert len(parsed["periods"]) == 4
        assert parsed["periods"][0]["forecast_period"] == 1
        assert parsed["periods"][0]["forecast_period_label"] == "Today"
        assert parsed["periods"][3]["forecast_date"] == "20260409"
        assert parsed["periods"][3]["aqhi_category"] == "Moderate"

    def test_parse_forecast_xml_skips_unsupported_periods(self):
        xml_text = FORECAST_XML.replace(
            "</forecastGroup>",
            '<forecast periodID="5"><period forecastName="Later" lang="EN">Friday</period><airQualityHealthIndex>4</airQualityHealthIndex></forecast></forecastGroup>',
        )

        parsed = CanadaAQHIBridge.parse_forecast_xml(xml_text)

        assert [period["forecast_period"] for period in parsed["periods"]] == [1, 2, 3, 4]


@pytest.mark.unit
class TestCatalogMerging:
    def test_merge_catalogs(self):
        communities = {
            "features": [
                {
                    "properties": {
                        "Latitude": "47.082841",
                        "Longitude": "-55.175272",
                        "cgndb_key": "AADCE",
                        "region_name_en": "Burin",
                    }
                }
            ]
        }
        stations = {
            "features": [
                {
                    "properties": {
                        "cgndb": "AADCE",
                        "name": {"en": "Burin", "fr": "Burin"},
                        "path_to_current_observation": "https://example.test/obs.xml",
                        "path_to_current_forecast": "https://example.test/fcst.xml",
                    }
                }
            ]
        }

        merged = CanadaAQHIBridge.merge_community_catalogs(communities, stations)

        assert merged["AADCE"]["community_name"] == "Burin"
        assert merged["AADCE"]["latitude"] == pytest.approx(47.082841)
        assert merged["AADCE"]["observation_url"] == "https://example.test/obs.xml"

    def test_load_reference_catalogs_skips_irrelevant_regions_before_geolocation(self, monkeypatch):
        communities = {
            "features": [
                {
                    "properties": {
                        "Latitude": "44.0000",
                        "Longitude": "-79.0000",
                        "cgndb_key": "FAFFD",
                        "region_name_en": "Barrie",
                    }
                },
                {
                    "properties": {
                        "Latitude": "47.082841",
                        "Longitude": "-55.175272",
                        "cgndb_key": "AADCE",
                        "region_name_en": "Burin",
                    }
                },
            ]
        }
        stations = {
            "features": [
                {
                    "properties": {
                        "cgndb": "FAFFD",
                        "name": {"en": "Barrie", "fr": "Barrie"},
                        "path_to_current_observation": "http://dd.weather.gc.ca/air_quality/aqhi/ont/observation/realtime/xml/AQ_OBS_FAFFD_CURRENT.xml",
                        "path_to_current_forecast": "http://dd.weather.gc.ca/air_quality/aqhi/ont/forecast/realtime/xml/AQ_FCST_FAFFD_CURRENT.xml",
                    }
                },
                {
                    "properties": {
                        "cgndb": "AADCE",
                        "name": {"en": "Burin", "fr": "Burin"},
                        "path_to_current_observation": "http://dd.weather.gc.ca/air_quality/aqhi/atl/observation/realtime/xml/AQ_OBS_AADCE_CURRENT.xml",
                        "path_to_current_forecast": "http://dd.weather.gc.ca/air_quality/aqhi/atl/forecast/realtime/xml/AQ_FCST_AADCE_CURRENT.xml",
                    }
                },
            ]
        }
        bridge = CanadaAQHIBridge()

        def fake_fetch_json(url, **kwargs):
            if url == COMMUNITY_GEOJSON_URL:
                return communities
            if url == STATION_GEOJSON_URL:
                return stations
            raise AssertionError(f"unexpected url {url}")

        geolocation_calls: list[str] = []

        def fake_resolve_province_code(cgndb_code: str, latitude: float, longitude: float):
            geolocation_calls.append(cgndb_code)
            return "NB"

        monkeypatch.setattr(bridge, "fetch_json", fake_fetch_json)
        monkeypatch.setattr(bridge, "resolve_province_code", fake_resolve_province_code)

        filtered = bridge.load_reference_catalogs({"ON"})

        assert list(filtered) == ["FAFFD"]
        assert filtered["FAFFD"]["province"] == "ON"
        assert geolocation_calls == []

    def test_poll_once_uses_cached_communities_when_refresh_fails(self):
        bridge = CanadaAQHIBridge()
        bridge.communities = {
            "AADCE": {
                "province": "NL",
                "community_name": "Burin",
                "cgndb_code": "AADCE",
                "observation_url": "https://example.test/obs.xml",
                "forecast_url": "https://example.test/fcst.xml",
            }
        }
        bridge.last_reference_refresh = None
        bridge.load_reference_catalogs = Mock(side_effect=requests.RequestException("timeout"))
        bridge.emit_observations = Mock(return_value=1)
        bridge.emit_forecasts = Mock(return_value=2)
        bridge.save_state = Mock()
        producer = Mock()

        counts = bridge.poll_once(producer, {"NL"})

        assert counts == {"communities": 0, "observations": 1, "forecasts": 2}
        bridge.emit_observations.assert_called_once()
        bridge.emit_forecasts.assert_called_once()

    def test_limit_communities_returns_stable_sorted_prefix(self):
        communities = {
            "AADCE": {"province": "NL", "community_name": "Burin"},
            "FAFFD": {"province": "ON", "community_name": "Barrie"},
            "FALIF": {"province": "ON", "community_name": "Belleville"},
        }

        limited = CanadaAQHIBridge.limit_communities(communities, max_communities=2)

        assert list(limited) == ["AADCE", "FAFFD"]

    def test_poll_once_limits_reference_and_telemetry_to_max_communities(self):
        bridge = CanadaAQHIBridge()
        bridge.load_reference_catalogs = Mock(
            return_value={
                "FALIF": {
                    "province": "ON",
                    "community_name": "Belleville",
                    "cgndb_code": "FALIF",
                    "observation_url": "https://example.test/belleville-observation.xml",
                    "forecast_url": "https://example.test/belleville-forecast.xml",
                },
                "AADCE": {
                    "province": "NL",
                    "community_name": "Burin",
                    "cgndb_code": "AADCE",
                    "observation_url": "https://example.test/burin-observation.xml",
                    "forecast_url": "https://example.test/burin-forecast.xml",
                },
                "FAFFD": {
                    "province": "ON",
                    "community_name": "Barrie",
                    "cgndb_code": "FAFFD",
                    "observation_url": "https://example.test/barrie-observation.xml",
                    "forecast_url": "https://example.test/barrie-forecast.xml",
                },
            }
        )
        bridge.emit_reference_data = Mock(return_value=2)
        bridge.emit_observations = Mock(return_value=2)
        bridge.emit_forecasts = Mock(return_value=8)
        bridge.save_state = Mock()
        producer = Mock()

        counts = bridge.poll_once(producer, {"NL", "ON"}, max_communities=2)

        assert counts == {"communities": 2, "observations": 2, "forecasts": 8}
        limited = bridge.emit_reference_data.call_args.args[1]
        assert list(limited) == ["AADCE", "FAFFD"]
        observed = bridge.emit_observations.call_args.args[1]
        assert [entry["community_name"] for entry in observed] == ["Burin", "Barrie"]
        forecasted = bridge.emit_forecasts.call_args.args[1]
        assert [entry["community_name"] for entry in forecasted] == ["Burin", "Barrie"]
