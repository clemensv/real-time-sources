"""Unit and integration tests for the NDW Netherlands Road Traffic bridge."""

from __future__ import annotations

import gzip
import json
import os
import textwrap
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from ndw_road_traffic.ndw_road_traffic import (
    parse_traffic_speed_xml,
    parse_travel_time_xml,
    parse_measurement_site_xml,
    parse_drip_xml,
    parse_msi_xml,
    parse_situation_xml,
    _build_kafka_config,
    StateManager,
    NdwPoller,
    DATEX2_V2,
)
from ndw_road_traffic_producer_data import (
    PointMeasurementSite,
    RouteMeasurementSite,
    TrafficObservation,
    TravelTimeObservation,
    DripSign,
    DripDisplayState,
    MsiSign,
    MsiDisplayState,
    Roadwork,
    BridgeOpening,
    TemporaryClosure,
    TemporarySpeedLimit,
    SafetyRelatedMessage,
)


# ---------------------------------------------------------------------------
# Helpers – XML builders
# ---------------------------------------------------------------------------

def _speed_xml(site_id: str = "SITE01", mtime: str = "2024-06-01T12:00:00Z",
               speeds: List[float] = None, flows: List[int] = None) -> bytes:
    if speeds is None:
        speeds = [80.0]
    if flows is None:
        flows = [120]
    flow_mvs = "".join(
        f"""<measuredValue index="{i+1}">
              <measuredValue>
                <basicData xsi:type="TrafficFlow">
                  <vehicleFlow><vehicleFlowRate>{f}</vehicleFlowRate></vehicleFlow>
                </basicData>
              </measuredValue>
            </measuredValue>"""
        for i, f in enumerate(flows)
    )
    speed_mvs = "".join(
        f"""<measuredValue index="{len(flows)+i+1}">
              <measuredValue>
                <basicData xsi:type="TrafficSpeed">
                  <averageVehicleSpeed><speed>{s}</speed></averageVehicleSpeed>
                </basicData>
              </measuredValue>
            </measuredValue>"""
        for i, s in enumerate(speeds)
    )
    return textwrap.dedent(f"""\
        <?xml version="1.0"?>
        <SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP:Body>
        <d2LogicalModel xmlns="{DATEX2_V2}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <payloadPublication xsi:type="MeasuredDataPublication">
          <siteMeasurements>
            <measurementSiteReference id="{site_id}" version="1"/>
            <measurementTimeDefault>{mtime}</measurementTimeDefault>
            {flow_mvs}
            {speed_mvs}
          </siteMeasurements>
        </payloadPublication>
        </d2LogicalModel>
        </SOAP:Body>
        </SOAP:Envelope>
    """).strip().encode("utf-8")


def _traveltime_xml(site_id: str = "TT01", mtime: str = "2024-06-01T12:00:00Z",
                    duration: float = 26.2, ref_duration: float = 21.4,
                    accuracy: float = 100.0, data_quality: float = 41.3,
                    n_input: int = 13, invalid: bool = False) -> bytes:
    dur_val = -1.0 if invalid else duration
    ref_val = -1.0 if invalid else ref_duration
    return textwrap.dedent(f"""\
        <?xml version="1.0"?>
        <d2LogicalModel xmlns="{DATEX2_V2}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <payloadPublication xsi:type="MeasuredDataPublication">
          <siteMeasurements>
            <measurementSiteReference id="{site_id}" version="1"/>
            <measurementTimeDefault>{mtime}</measurementTimeDefault>
            <measuredValue index="1">
              <measuredValue>
                <basicData xsi:type="TravelTimeData">
                  <travelTime accuracy="{accuracy}"
                              numberOfInputValuesUsed="{n_input}"
                              supplierCalculatedDataQuality="{data_quality}">
                    <duration>{dur_val}</duration>
                  </travelTime>
                </basicData>
                <measuredValueExtension>
                  <measuredValueExtended>
                    <basicDataReferenceValue>
                      <travelTimeData>
                        <travelTime>
                          <duration>{ref_val}</duration>
                        </travelTime>
                      </travelTimeData>
                    </basicDataReferenceValue>
                  </measuredValueExtended>
                </measuredValueExtension>
              </measuredValue>
            </measuredValue>
          </siteMeasurements>
        </payloadPublication>
        </d2LogicalModel>
    """).strip().encode("utf-8")


def _measurement_site_xml(point_ids: List[str] = None, route_ids: List[str] = None) -> bytes:
    if point_ids is None:
        point_ids = ["POINT01"]
    if route_ids is None:
        route_ids = ["ROUTE01"]

    records = ""
    for pid in point_ids:
        records += f"""
        <mst:measurementSiteRecord id="{pid}"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:type="mst:PointMeasurementSiteRecord">
          <mst:measurementSiteName>
            <com:value lang="nl">Test Point Site {pid}</com:value>
          </mst:measurementSiteName>
          <mst:measurementSiteLocation>
            <com:pointByCoordinates>
              <com:pointCoordinates>
                <com:latitude>52.3702</com:latitude>
                <com:longitude>4.8952</com:longitude>
              </com:pointCoordinates>
            </com:pointByCoordinates>
          </mst:measurementSiteLocation>
          <mst:measurementSpecificCharacteristics index="1">
            <mst:period>60</mst:period>
          </mst:measurementSpecificCharacteristics>
        </mst:measurementSiteRecord>
        """

    for rid in route_ids:
        records += f"""
        <mst:measurementSiteRecord id="{rid}"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:type="mst:RouteMeasurementSiteRecord">
          <mst:measurementSiteName>
            <com:value lang="nl">Test Route Site {rid}</com:value>
          </mst:measurementSiteName>
          <mst:measurementSiteLocation>
            <com:linear>
              <com:startOfLinear>
                <com:pointByCoordinates>
                  <com:pointCoordinates>
                    <com:latitude>52.1</com:latitude>
                    <com:longitude>4.1</com:longitude>
                  </com:pointCoordinates>
                </com:pointByCoordinates>
              </com:startOfLinear>
              <com:endOfLinear>
                <com:pointByCoordinates>
                  <com:pointCoordinates>
                    <com:latitude>52.2</com:latitude>
                    <com:longitude>4.2</com:longitude>
                  </com:pointCoordinates>
                </com:pointByCoordinates>
              </com:endOfLinear>
            </com:linear>
          </mst:measurementSiteLocation>
          <mst:length>5000</mst:length>
        </mst:measurementSiteRecord>
        """

    return textwrap.dedent(f"""\
        <?xml version="1.0"?>
        <d2LogicalModel
            xmlns:mst="http://datex2.eu/schema/3/measurementSiteTable"
            xmlns:com="http://datex2.eu/schema/3/common"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <payloadPublication xsi:type="mst:MeasurementSiteTablePublication">
            <com:publicationTime>2024-06-01T12:00:00Z</com:publicationTime>
            <mst:measurementSiteTable>
              {records}
            </mst:measurementSiteTable>
          </payloadPublication>
        </d2LogicalModel>
    """).strip().encode("utf-8")


def _drip_xml(controller_id: str = "DRIP01", vms_index: str = "1",
              pub_time: str = "2024-06-01T12:00:00Z") -> bytes:
    return textwrap.dedent(f"""\
        <?xml version="1.0"?>
        <d2LogicalModel
            xmlns:vms="http://datex2.eu/schema/3/vms"
            xmlns:com="http://datex2.eu/schema/3/common"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <payloadPublication xsi:type="vms:VmsDatexPublication">
            <com:publicationTime>{pub_time}</com:publicationTime>
            <vms:vmsUnit>
              <vms:vmsUnitRecord id="{controller_id}">
                <vms:vmsUnitLocation>
                  <com:pointByCoordinates>
                    <com:pointCoordinates>
                      <com:latitude>52.3702</com:latitude>
                      <com:longitude>4.8952</com:longitude>
                    </com:pointCoordinates>
                  </com:pointByCoordinates>
                </vms:vmsUnitLocation>
                <vms:vmsRecord>
                  <vms:vmsIndex>{vms_index}</vms:vmsIndex>
                  <vms:vmsType>presignalling</vms:vmsType>
                  <vms:vmsStatus>
                    <vms:vmsWorking>true</vms:vmsWorking>
                    <vms:displayedText>
                      <vms:vmsText>
                        <vms:vmsTextLine>TEST ROUTE</vms:vmsTextLine>
                        <vms:vmsTextLine>A1-A10</vms:vmsTextLine>
                      </vms:vmsText>
                    </vms:displayedText>
                  </vms:vmsStatus>
                </vms:vmsRecord>
              </vms:vmsUnitRecord>
            </vms:vmsUnit>
          </payloadPublication>
        </d2LogicalModel>
    """).strip().encode("utf-8")


def _msi_xml(sign_id: str = "MSI01", pub_time: str = "2024-06-01T12:00:00Z",
             image_code: str = "70") -> bytes:
    return textwrap.dedent(f"""\
        <?xml version="1.0"?>
        <d2LogicalModel
            xmlns:vms="http://datex2.eu/schema/3/vms"
            xmlns:com="http://datex2.eu/schema/3/common"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <payloadPublication xsi:type="vms:VmsDatexPublication">
            <com:publicationTime>{pub_time}</com:publicationTime>
            <vms:vmsUnit>
              <vms:vmsUnitRecord id="{sign_id}">
                <vms:vmsUnitLocation>
                  <com:pointByCoordinates>
                    <com:pointCoordinates>
                      <com:latitude>52.3702</com:latitude>
                      <com:longitude>4.8952</com:longitude>
                    </com:pointCoordinates>
                  </com:pointByCoordinates>
                </vms:vmsUnitLocation>
                <vms:vmsType>matrixBoardOneByOne</vms:vmsType>
                <vms:vmsRecord>
                  <vms:vmsIndex>1</vms:vmsIndex>
                  <vms:vmsStatus>
                    <vms:displayedText>
                      <vms:vmsText>
                        <vms:vmsTextLine>{image_code}</vms:vmsTextLine>
                      </vms:vmsText>
                    </vms:displayedText>
                  </vms:vmsStatus>
                </vms:vmsRecord>
              </vms:vmsUnitRecord>
            </vms:vmsUnit>
          </payloadPublication>
        </d2LogicalModel>
    """).strip().encode("utf-8")


def _situation_xml(situation_id: str = "SIT01", record_id: str = "REC01",
                   version_time: str = "2024-06-01T12:00:00Z",
                   rec_type: str = "sit:ConstructionWorks",
                   speed_limit: int = None) -> bytes:
    xsi_type_attr = f'xsi:type="{rec_type}"' if rec_type else ""
    speed_elem = f"<sit:maximumSpeedLimit>{speed_limit}</sit:maximumSpeedLimit>" if speed_limit else ""
    return textwrap.dedent(f"""\
        <?xml version="1.0"?>
        <d2LogicalModel
            xmlns:sit="http://datex2.eu/schema/3/situation"
            xmlns:com="http://datex2.eu/schema/3/common"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <payloadPublication xsi:type="sit:SituationPublication">
            <com:publicationTime>2024-06-01T12:00:00Z</com:publicationTime>
            <sit:situation id="{situation_id}">
              <sit:situationRecord id="{record_id}" {xsi_type_attr}>
                <sit:situationRecordVersionTime>{version_time}</sit:situationRecordVersionTime>
                <sit:validityStatus>active</sit:validityStatus>
                <sit:validity>
                  <com:validityTimeSpecification>
                    <com:overallStartTime>2024-06-01T08:00:00Z</com:overallStartTime>
                    <com:overallEndTime>2024-06-01T20:00:00Z</com:overallEndTime>
                  </com:validityTimeSpecification>
                </sit:validity>
                <sit:comment>
                  <com:value lang="nl">Test werkzaamheden A1</com:value>
                </sit:comment>
                {speed_elem}
              </sit:situationRecord>
            </sit:situation>
          </payloadPublication>
        </d2LogicalModel>
    """).strip().encode("utf-8")


# ---------------------------------------------------------------------------
# Tests – parse_traffic_speed_xml
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseTrafficSpeedXml:
    def test_basic_parse(self):
        xml = _speed_xml("SITE01", "2024-06-01T12:00:00Z", speeds=[80.0, 90.0], flows=[120, 130])
        results = parse_traffic_speed_xml(xml)
        assert len(results) == 1
        r = results[0]
        assert r["measurement_site_id"] == "SITE01"
        assert r["measurement_time"] == "2024-06-01T12:00:00Z"
        assert r["average_speed"] == pytest.approx(85.0, abs=0.1)
        assert r["vehicle_flow_rate"] == 250
        assert r["number_of_lanes_with_data"] == 2

    def test_zero_speed_excluded(self):
        xml = _speed_xml("SITE02", speeds=[0.0], flows=[100])
        results = parse_traffic_speed_xml(xml)
        assert results[0]["average_speed"] is None
        assert results[0]["vehicle_flow_rate"] == 100

    def test_multiple_sites(self):
        xml = _speed_xml("S1", flows=[100], speeds=[80.0])
        root_bytes = xml
        results = parse_traffic_speed_xml(root_bytes)
        assert len(results) >= 1

    def test_empty_xml(self):
        xml = f'<root xmlns="{DATEX2_V2}"></root>'.encode()
        results = parse_traffic_speed_xml(xml)
        assert results == []


# ---------------------------------------------------------------------------
# Tests – parse_travel_time_xml
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseTravelTimeXml:
    def test_basic_parse(self):
        xml = _traveltime_xml("TT01", duration=26.2, ref_duration=21.4, accuracy=100.0,
                               data_quality=41.3, n_input=13)
        results = parse_travel_time_xml(xml)
        assert len(results) == 1
        r = results[0]
        assert r["measurement_site_id"] == "TT01"
        assert r["duration"] == pytest.approx(26.2)
        assert r["reference_duration"] == pytest.approx(21.4)
        assert r["accuracy"] == pytest.approx(100.0)
        assert r["data_quality"] == pytest.approx(41.3)
        assert r["number_of_input_values"] == 13

    def test_invalid_duration_becomes_none(self):
        xml = _traveltime_xml("TT02", invalid=True)
        results = parse_travel_time_xml(xml)
        assert results[0]["duration"] is None
        assert results[0]["reference_duration"] is None


# ---------------------------------------------------------------------------
# Tests – parse_measurement_site_xml
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseMeasurementSiteXml:
    def test_point_site_parsed(self):
        xml = _measurement_site_xml(point_ids=["POINT01"], route_ids=[])
        points, routes = parse_measurement_site_xml(xml)
        assert len(points) == 1
        assert len(routes) == 0
        p = points[0]
        assert p["measurement_site_id"] == "POINT01"
        assert p["latitude"] == pytest.approx(52.3702, abs=0.001)
        assert p["longitude"] == pytest.approx(4.8952, abs=0.001)

    def test_route_site_parsed(self):
        xml = _measurement_site_xml(point_ids=[], route_ids=["ROUTE01"])
        points, routes = parse_measurement_site_xml(xml)
        assert len(points) == 0
        assert len(routes) == 1
        r = routes[0]
        assert r["measurement_site_id"] == "ROUTE01"
        assert r["length_metres"] == pytest.approx(5000.0)

    def test_both_types(self):
        xml = _measurement_site_xml(point_ids=["P1", "P2"], route_ids=["R1"])
        points, routes = parse_measurement_site_xml(xml)
        assert len(points) == 2
        assert len(routes) == 1


# ---------------------------------------------------------------------------
# Tests – parse_drip_xml
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseDripXml:
    def test_sign_and_state_parsed(self):
        xml = _drip_xml("DRIP01", "1", "2024-06-01T12:00:00Z")
        signs, states = parse_drip_xml(xml)
        assert len(signs) == 1
        assert len(states) == 1
        s = signs[0]
        assert s["vms_controller_id"] == "DRIP01"
        assert s["vms_index"] == "1"
        assert s["vms_type"] == "presignalling"
        assert s["latitude"] == pytest.approx(52.3702, abs=0.001)

        st = states[0]
        assert st["vms_controller_id"] == "DRIP01"
        assert st["vms_index"] == "1"
        assert st["publication_time"] == "2024-06-01T12:00:00Z"
        assert st["active"] is True
        assert "TEST ROUTE" in (st["vms_text"] or "")

    def test_vms_index_is_string(self):
        xml = _drip_xml("CTRL", "3")
        signs, states = parse_drip_xml(xml)
        assert isinstance(signs[0]["vms_index"], str)
        assert isinstance(states[0]["vms_index"], str)


# ---------------------------------------------------------------------------
# Tests – parse_msi_xml
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseMsiXml:
    def test_speed_limit_image(self):
        xml = _msi_xml("MSI01", image_code="70")
        signs, states = parse_msi_xml(xml)
        assert len(signs) == 1
        assert len(states) == 1
        st = states[0]
        assert st["sign_id"] == "MSI01"
        assert st["image_code"] == "70"
        assert st["state"] == "speed_limit"
        assert st["speed_limit"] == 70

    def test_blank_image(self):
        xml = _msi_xml("MSI02", image_code="blank")
        _, states = parse_msi_xml(xml)
        assert states[0]["state"] == "open"

    def test_sign_reference(self):
        xml = _msi_xml("MSI03")
        signs, _ = parse_msi_xml(xml)
        assert signs[0]["sign_id"] == "MSI03"
        assert signs[0]["sign_type"] == "matrixBoardOneByOne"


# ---------------------------------------------------------------------------
# Tests – parse_situation_xml
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseSituationXml:
    def test_roadwork_parsed(self):
        xml = _situation_xml("SIT01", "REC01", rec_type="sit:ConstructionWorks")
        results = parse_situation_xml(xml, "roadwork")
        assert len(results) == 1
        r = results[0]
        assert r["situation_record_id"] == "REC01"
        assert r["version_time"] == "2024-06-01T12:00:00Z"
        assert r["validity_status"] == "active"

    def test_bridge_opening_parsed(self):
        xml = _situation_xml("SIT02", "REC02", rec_type="sit:BridgeOpening")
        results = parse_situation_xml(xml, "bridge_opening")
        assert len(results) == 1
        assert results[0]["situation_record_id"] == "REC02"

    def test_temporary_closure_parsed(self):
        xml = _situation_xml("SIT03", "REC03", rec_type="sit:RoadClosure")
        results = parse_situation_xml(xml, "temporary_closure")
        assert results[0]["situation_record_id"] == "REC03"

    def test_temporary_speed_limit_parsed(self):
        xml = _situation_xml("SIT04", "REC04", rec_type="sit:SpeedLimit", speed_limit=80)
        results = parse_situation_xml(xml, "temporary_speed_limit")
        r = results[0]
        assert r["situation_record_id"] == "REC04"
        assert r["speed_limit_kmh"] == 80

    def test_safety_related_message_parsed(self):
        xml = _situation_xml("SIT05", "REC05", rec_type="sit:VehicleObstruction")
        results = parse_situation_xml(xml, "safety_related_message")
        r = results[0]
        assert r["situation_record_id"] == "REC05"
        assert r["message_type"] == "VehicleObstruction"

    def test_empty_feed(self):
        xml = b'<?xml version="1.0"?><root/>'
        results = parse_situation_xml(xml, "roadwork")
        assert results == []


# ---------------------------------------------------------------------------
# Tests – _build_kafka_config
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBuildKafkaConfig:
    def test_bootstrap_server_format(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        config, topic = _build_kafka_config(cs, enable_tls=False)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert topic == "my-topic"
        assert config.get("security.protocol") == "PLAINTEXT"

    def test_event_hubs_format(self):
        cs = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=my-eh"
        config, topic = _build_kafka_config(cs, enable_tls=True)
        assert "myns.servicebus.windows.net" in config["bootstrap.servers"]
        assert config.get("security.protocol") == "SASL_SSL"
        assert topic == "my-eh"

    def test_bootstrap_no_tls_default(self):
        cs = "BootstrapServer=kafka:9092;EntityPath=t"
        config, _ = _build_kafka_config(cs, enable_tls=False)
        assert config["security.protocol"] == "PLAINTEXT"


# ---------------------------------------------------------------------------
# Tests – StateManager
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestStateManager:
    def test_is_new_first_time(self, tmp_path):
        sm = StateManager(str(tmp_path / "state.json"))
        assert sm.is_new("speed", "S1", "2024-01-01T00:00:00Z") is True

    def test_is_new_same_value(self, tmp_path):
        sm = StateManager(str(tmp_path / "state.json"))
        sm.is_new("speed", "S1", "2024-01-01T00:00:00Z")
        assert sm.is_new("speed", "S1", "2024-01-01T00:00:00Z") is False

    def test_is_new_updated_value(self, tmp_path):
        sm = StateManager(str(tmp_path / "state.json"))
        sm.is_new("speed", "S1", "2024-01-01T00:00:00Z")
        assert sm.is_new("speed", "S1", "2024-01-02T00:00:00Z") is True

    def test_save_and_reload(self, tmp_path):
        path = str(tmp_path / "state.json")
        sm = StateManager(path)
        sm.is_new("speed", "S1", "T1")
        sm.save()

        sm2 = StateManager(path)
        assert sm2.is_new("speed", "S1", "T1") is False
        assert sm2.is_new("speed", "S1", "T2") is True


# ---------------------------------------------------------------------------
# Tests – flush failure: state must not advance
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFlushFailure:
    def _make_fake_producer(self, flush_result: int = 1):
        """Create a fake producer class that records calls."""
        kafka_mock = MagicMock()
        kafka_mock.flush.return_value = flush_result
        prod = MagicMock()
        prod.producer = kafka_mock
        return prod

    def test_speed_flush_failure_does_not_advance_state(self, tmp_path):
        avg_prod = self._make_fake_producer(flush_result=1)
        drip_prod = self._make_fake_producer(flush_result=0)
        msi_prod = self._make_fake_producer(flush_result=0)
        sit_prod = self._make_fake_producer(flush_result=0)
        sm = StateManager(str(tmp_path / "state.json"))

        xml_bytes = _speed_xml("SITE01", "2024-06-01T12:00:00Z", speeds=[80.0], flows=[100])

        poller = NdwPoller(avg_prod, drip_prod, msi_prod, sit_prod, sm)

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml", return_value=xml_bytes):
            result = poller._poll_speed()

        # Flush returned 1 (non-zero), so no state advance
        assert sm.state.get("speed", {}).get("SITE01") is None
        assert result == 0

    def test_speed_flush_success_advances_state(self, tmp_path):
        avg_prod = self._make_fake_producer(flush_result=0)
        drip_prod = self._make_fake_producer(flush_result=0)
        msi_prod = self._make_fake_producer(flush_result=0)
        sit_prod = self._make_fake_producer(flush_result=0)
        sm = StateManager(str(tmp_path / "state.json"))

        xml_bytes = _speed_xml("SITE01", "2024-06-01T12:00:00Z", speeds=[80.0], flows=[100])
        poller = NdwPoller(avg_prod, drip_prod, msi_prod, sit_prod, sm)

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml", return_value=xml_bytes):
            result = poller._poll_speed()

        assert sm.state["speed"].get("SITE01") == "2024-06-01T12:00:00Z"
        assert result == 1


# ---------------------------------------------------------------------------
# Tests – reference data cache preservation on failure
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestCachePreservation:
    def _make_poller(self, tmp_path):
        kafka_mock = MagicMock()
        kafka_mock.flush.return_value = 0
        prod_mock = MagicMock()
        prod_mock.producer = kafka_mock

        sm = StateManager(str(tmp_path / "state.json"))
        poller = NdwPoller(prod_mock, prod_mock, prod_mock, prod_mock, sm)
        return poller

    def test_measurement_sites_cache_preserved_on_download_failure(self, tmp_path):
        poller = self._make_poller(tmp_path)
        old_cache = [{"measurement_site_id": "OLD_POINT", "name": "Old", "measurement_site_type": None,
                      "period": None, "latitude": 1.0, "longitude": 2.0, "road_name": None,
                      "lane_count": None, "carriageway_type": None}]
        poller._point_sites_cache = old_cache

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml",
                   side_effect=Exception("connection error")):
            poller._refresh_measurement_sites()

        assert poller._point_sites_cache == old_cache

    def test_drip_signs_cache_preserved_on_download_failure(self, tmp_path):
        poller = self._make_poller(tmp_path)
        old_cache = [{"vms_controller_id": "DRIP_OLD", "vms_index": "1", "vms_type": None,
                      "latitude": None, "longitude": None, "road_name": None, "description": None}]
        poller._drip_signs_cache = old_cache

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml",
                   side_effect=Exception("timeout")):
            poller._refresh_drip_signs()

        assert poller._drip_signs_cache == old_cache

    def test_msi_signs_cache_preserved_on_download_failure(self, tmp_path):
        poller = self._make_poller(tmp_path)
        old_cache = [{"sign_id": "MSI_OLD", "sign_type": None, "latitude": None,
                      "longitude": None, "road_name": None, "lane": None, "description": None}]
        poller._msi_signs_cache = old_cache

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml",
                   side_effect=Exception("timeout")):
            poller._refresh_msi_signs()

        assert poller._msi_signs_cache == old_cache


# ---------------------------------------------------------------------------
# Tests – multi-family wiring (one-cycle test)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestMultiFamilyWiring:
    """Verify all four producer classes are exercised in one poll cycle."""

    def _make_producers(self):
        def make_prod():
            kafka_mock = MagicMock()
            kafka_mock.flush.return_value = 0
            prod = MagicMock()
            prod.producer = kafka_mock
            return prod

        return make_prod(), make_prod(), make_prod(), make_prod()

    def test_all_producers_called(self, tmp_path):
        avg_prod, drip_prod, msi_prod, sit_prod = self._make_producers()
        sm = StateManager(str(tmp_path / "state.json"))
        poller = NdwPoller(avg_prod, drip_prod, msi_prod, sit_prod, sm)

        speed_xml = _speed_xml("S1", "2024-06-01T12:00:00Z", speeds=[80.0], flows=[100])
        tt_xml = _traveltime_xml("T1", duration=30.0)
        drip_xml_bytes = _drip_xml("D1", "1", "2024-06-01T12:00:00Z")
        msi_xml_bytes = _msi_xml("M1", image_code="70")

        def fake_download(session, url, **kwargs):
            if "trafficspeed" in url:
                return speed_xml
            elif "traveltime" in url:
                return tt_xml
            elif "drip" in url or "dynamische" in url:
                return drip_xml_bytes
            elif "msi" in url or "Matrix" in url:
                return msi_xml_bytes
            return b'<?xml version="1.0"?><root/>'

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml", side_effect=fake_download):
            poller._poll_speed()
            poller._poll_traveltime()
            poller._poll_drip_states()
            poller._poll_msi_states()

        # AVG producer used for speed and travel time
        assert avg_prod.send_nl_ndw_avg_traffic_observation.called
        assert avg_prod.send_nl_ndw_avg_travel_time_observation.called
        # DRIP producer used for display states
        assert drip_prod.send_nl_ndw_drip_drip_display_state.called
        # MSI producer used for display states
        assert msi_prod.send_nl_ndw_msi_msi_display_state.called

    def test_situation_producers_called(self, tmp_path):
        avg_prod, drip_prod, msi_prod, sit_prod = self._make_producers()
        sm = StateManager(str(tmp_path / "state.json"))
        poller = NdwPoller(avg_prod, drip_prod, msi_prod, sit_prod, sm)

        roadwork_xml = _situation_xml("S1", "R1")
        bridge_xml = _situation_xml("S2", "R2", rec_type="sit:BridgeOpening")
        closure_xml = _situation_xml("S3", "R3", rec_type="sit:RoadClosure")
        speed_xml_s = _situation_xml("S4", "R4", rec_type="sit:SpeedLimit", speed_limit=80)
        safety_xml = _situation_xml("S5", "R5", rec_type="sit:VehicleObstruction")

        feed_map = {
            "planningsfeed_wegwerkzaamheden": roadwork_xml,
            "planningsfeed_brugopeningen": bridge_xml,
            "afsluitingen": closure_xml,
            "maximum_snelheden": speed_xml_s,
            "srti": safety_xml,
        }

        def fake_download(session, url, **kwargs):
            for k, v in feed_map.items():
                if k in url:
                    return v
            return b'<?xml version="1.0"?><root/>'

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml", side_effect=fake_download):
            poller._poll_situations()

        assert sit_prod.send_nl_ndw_situations_roadwork.called
        assert sit_prod.send_nl_ndw_situations_bridge_opening.called
        assert sit_prod.send_nl_ndw_situations_temporary_closure.called
        assert sit_prod.send_nl_ndw_situations_temporary_speed_limit.called
        assert sit_prod.send_nl_ndw_situations_safety_related_message.called

    def test_reference_producers_called(self, tmp_path):
        avg_prod, drip_prod, msi_prod, sit_prod = self._make_producers()
        sm = StateManager(str(tmp_path / "state.json"))
        poller = NdwPoller(avg_prod, drip_prod, msi_prod, sit_prod, sm)

        msite_xml = _measurement_site_xml(point_ids=["P1"], route_ids=["R1"])
        drip_ref_xml = _drip_xml("D1", "1")
        msi_ref_xml = _msi_xml("M1")

        def fake_download(session, url, **kwargs):
            if "measurement_current" in url:
                return msite_xml
            elif "dynamische" in url or "drip" in url.lower():
                return drip_ref_xml
            elif "Matrix" in url or "msi" in url.lower():
                return msi_ref_xml
            return b'<?xml version="1.0"?><root/>'

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml", side_effect=fake_download):
            poller.emit_reference_data()

        assert avg_prod.send_nl_ndw_avg_point_measurement_site.called
        assert avg_prod.send_nl_ndw_avg_route_measurement_site.called
        assert drip_prod.send_nl_ndw_drip_drip_sign.called
        assert msi_prod.send_nl_ndw_msi_msi_sign.called


# ---------------------------------------------------------------------------
# Tests – single-feed failure isolation
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestFeedIsolation:
    def test_speed_failure_does_not_block_traveltime(self, tmp_path):
        kafka_mock = MagicMock()
        kafka_mock.flush.return_value = 0
        avg_prod = MagicMock()
        avg_prod.producer = kafka_mock
        drip_prod = MagicMock()
        drip_prod.producer = kafka_mock
        msi_prod = MagicMock()
        msi_prod.producer = kafka_mock
        sit_prod = MagicMock()
        sit_prod.producer = kafka_mock

        sm = StateManager(str(tmp_path / "state.json"))
        poller = NdwPoller(avg_prod, drip_prod, msi_prod, sit_prod, sm)

        tt_xml = _traveltime_xml("T1", duration=30.0)

        call_count = {"n": 0}

        def fake_download(session, url, **kwargs):
            call_count["n"] += 1
            if "trafficspeed" in url:
                raise Exception("speed feed down")
            return tt_xml

        with patch("ndw_road_traffic.ndw_road_traffic.download_gzip_xml", side_effect=fake_download):
            poller._poll_speed()
            poller._poll_traveltime()

        # Travel time should still be called even though speed failed
        assert avg_prod.send_nl_ndw_avg_travel_time_observation.called
