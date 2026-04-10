"""Unit tests for the FMI Finland air quality bridge."""

from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import requests

from fmi_finland.fmi_finland import (
    FMIAirQualityAPI,
    PARAM_MAP,
    _measurement_arg,
    _observation_window,
    create_retrying_session,
    get_station_registry_with_fallback,
    _resolve_fmisid,
    parse_connection_string,
    parse_observations_xml,
    parse_station_metadata,
)

pytestmark = pytest.mark.unit

STATIONS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<wfs:FeatureCollection
  xmlns:wfs="http://www.opengis.net/wfs/2.0"
  xmlns:gml="http://www.opengis.net/gml/3.2"
  xmlns:ef="http://inspire.ec.europa.eu/schemas/ef/4.0"
  xmlns:ins_base="http://inspire.ec.europa.eu/schemas/base/3.3">
  <wfs:member>
    <ef:EnvironmentalMonitoringFacility gml:id="station-1">
      <gml:identifier codeSpace="http://xml.fmi.fi/namespace/stationcode/fmisid">100662</gml:identifier>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/locationcode/name">Helsinki Kallio 2</gml:name>
      <gml:name codeSpace="http://xml.fmi.fi/namespace/location/region">Helsinki</gml:name>
      <ef:name>Helsinki Kallio 2</ef:name>
      <ef:representativePoint>
        <gml:Point gml:id="point-1">
          <gml:pos>60.187390 24.950600</gml:pos>
        </gml:Point>
      </ef:representativePoint>
    </ef:EnvironmentalMonitoringFacility>
  </wfs:member>
</wfs:FeatureCollection>
"""

OBSERVATIONS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<wfs:FeatureCollection
  xmlns:wfs="http://www.opengis.net/wfs/2.0"
  xmlns:gml="http://www.opengis.net/gml/3.2"
  xmlns:BsWfs="http://xml.fmi.fi/schema/wfs/2.0">
  <wfs:member>
    <BsWfs:BsWfsElement gml:id="BsWfsElement.1.1.1">
      <BsWfs:Location><gml:Point gml:id="p1"><gml:pos>60.18739 24.95060</gml:pos></gml:Point></BsWfs:Location>
      <BsWfs:Time>2024-01-15T13:00:00Z</BsWfs:Time>
      <BsWfs:ParameterName>PM10_PT1H_avg</BsWfs:ParameterName>
      <BsWfs:ParameterValue>12.5</BsWfs:ParameterValue>
    </BsWfs:BsWfsElement>
  </wfs:member>
  <wfs:member>
    <BsWfs:BsWfsElement gml:id="BsWfsElement.1.1.2">
      <BsWfs:Location><gml:Point gml:id="p2"><gml:pos>60.18739 24.95060</gml:pos></gml:Point></BsWfs:Location>
      <BsWfs:Time>2024-01-15T13:00:00Z</BsWfs:Time>
      <BsWfs:ParameterName>AQINDEX_PT1H_avg</BsWfs:ParameterName>
      <BsWfs:ParameterValue>1.0</BsWfs:ParameterValue>
    </BsWfs:BsWfsElement>
  </wfs:member>
  <wfs:member>
    <BsWfs:BsWfsElement gml:id="BsWfsElement.1.1.3">
      <BsWfs:Location><gml:Point gml:id="p3"><gml:pos>60.18739 24.95060</gml:pos></gml:Point></BsWfs:Location>
      <BsWfs:Time>2024-01-15T13:00:00Z</BsWfs:Time>
      <BsWfs:ParameterName>O3_PT1H_avg</BsWfs:ParameterName>
      <BsWfs:ParameterValue>NaN</BsWfs:ParameterValue>
    </BsWfs:BsWfsElement>
  </wfs:member>
  <wfs:member>
    <BsWfs:BsWfsElement gml:id="BsWfsElement.100662.PM25_PT1H_avg.4">
      <BsWfs:Location><gml:Point gml:id="p4"><gml:pos>60.18739 24.95060</gml:pos></gml:Point></BsWfs:Location>
      <BsWfs:Time>2024-01-15T13:00:00Z</BsWfs:Time>
      <BsWfs:ParameterName>PM25_PT1H_avg</BsWfs:ParameterName>
      <BsWfs:ParameterValue>6.3</BsWfs:ParameterValue>
    </BsWfs:BsWfsElement>
  </wfs:member>
</wfs:FeatureCollection>
"""


class TestConnectionStringParsing:
    def test_event_hubs_connection_string(self):
        config = parse_connection_string(
            "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=name;SharedAccessKey=secret;EntityPath=topic"
        )
        assert config["bootstrap.servers"] == "namespace.servicebus.windows.net:9093"
        assert config["sasl.username"] == "$ConnectionString"
        assert config["sasl.password"].startswith("Endpoint=sb://")
        assert config["_entity_path"] == "topic"

    def test_plain_kafka_connection_string(self):
        config = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=fmi-finland-airquality")
        assert config["bootstrap.servers"] == "localhost:9092"
        assert config["_entity_path"] == "fmi-finland-airquality"


class TestHttpResilience:
    def test_create_retrying_session(self):
        session = create_retrying_session()
        https_adapter = session.get_adapter("https://opendata.fmi.fi/wfs")

        assert session.headers["User-Agent"] == "GitHub-Copilot-CLI/1.0"
        assert https_adapter.max_retries.total == 3
        assert https_adapter.max_retries.backoff_factor == 1

    def test_get_station_registry_with_fallback_uses_cached_registry(self):
        api = FMIAirQualityAPI()
        api.cached_registry = parse_station_metadata(STATIONS_XML)
        api.get_station_registry = Mock(side_effect=requests.RequestException("timeout"))

        registry = get_station_registry_with_fallback(api)

        assert registry.by_id["100662"].station_name == "Helsinki Kallio 2"


class TestParsingHelpers:
    def test_station_metadata_parsing(self):
        registry = parse_station_metadata(STATIONS_XML)
        station = registry.by_id["100662"]
        assert station.station_name == "Helsinki Kallio 2"
        assert station.municipality == "Helsinki"
        assert station.latitude == 60.18739
        assert station.longitude == 24.9506

    def test_resolve_fmisid_from_numeric_gml_id(self):
        registry = parse_station_metadata(STATIONS_XML)
        resolved = _resolve_fmisid("BsWfsElement.100662.PM10_PT1H_avg.1", None, None, registry)
        assert resolved == "100662"

    def test_resolve_fmisid_from_coordinates_when_gml_id_is_index_only(self):
        registry = parse_station_metadata(STATIONS_XML)
        resolved = _resolve_fmisid("BsWfsElement.1.1.1", 60.18739, 24.9506, registry)
        assert resolved == "100662"

    def test_observation_aggregation_and_nan_handling(self):
        registry = parse_station_metadata(STATIONS_XML)
        stations, observations = parse_observations_xml(OBSERVATIONS_XML, registry)
        assert stations["100662"].station_name == "Helsinki Kallio 2"
        assert len(observations) == 1
        observation = observations[0]
        assert observation["fmisid"] == "100662"
        assert observation["station_name"] == "Helsinki Kallio 2"
        assert observation["observation_time"] == "2024-01-15T13:00:00Z"
        assert observation["aqindex"] == 1.0
        assert observation["pm10_ug_m3"] == 12.5
        assert observation["pm2_5_ug_m3"] == 6.3
        assert observation["o3_ug_m3"] is None

    def test_measurement_arg_preserves_zero(self):
        assert _measurement_arg(0.0) == "0"
        assert _measurement_arg(1.5) == "1.5"
        assert _measurement_arg(None) is None

    def test_observation_window_alignment(self):
        start_time, end_time = _observation_window(datetime(2026, 4, 8, 11, 12, tzinfo=timezone.utc))
        assert start_time == "2026-04-08T09:00:00Z"
        assert end_time == "2026-04-08T10:00:00Z"

    def test_parameter_map_contains_expected_metrics(self):
        assert PARAM_MAP["AQINDEX_PT1H_avg"] == "aqindex"
        assert PARAM_MAP["PM10_PT1H_avg"] == "pm10_ug_m3"
        assert PARAM_MAP["CO_PT1H_avg"] == "co_mg_m3"
