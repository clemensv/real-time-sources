"""Unit and integration tests for NDW Netherlands Road Traffic bridge."""

from __future__ import annotations

import gzip
import json
import os
import textwrap
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from ndl_netherlands.ndl_netherlands import (
    parse_traffic_speed_xml,
    parse_travel_time_xml,
    parse_situation_xml,
    parse_connection_string,
    _build_kafka_config,
    download_gzip_xml,
    StateManager,
    NdwPoller,
    BASE_URL,
    SPEED_FILE,
    TRAVELTIME_FILE,
    SITUATION_FILE,
    DATEX2_NS,
    D3_SIT,
    D3_COM,
)
from ndl_netherlands_producer_data import TrafficSpeed, TravelTime, TrafficSituation


# ---------------------------------------------------------------------------
# Helpers – minimal DATEX II v2 speed XML
# ---------------------------------------------------------------------------

def _speed_xml(site_id="SITE01", mtime="2024-06-01T12:00:00Z",
               speeds=None, flows=None):
    """Build a minimal DATEX II v2 speed XML."""
    if speeds is None:
        speeds = [80]
    if flows is None:
        flows = [120]
    mvs = ""
    idx = 1
    for f in flows:
        mvs += f"""
        <siteMeasurements xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        """  # we build inline
        break  # handled below

    flow_mvs = ""
    for i, f in enumerate(flows, 1):
        flow_mvs += textwrap.dedent(f"""\
            <measuredValue index="{i}">
              <measuredValue>
                <basicData xsi:type="TrafficFlow">
                  <vehicleFlow><vehicleFlowRate>{f}</vehicleFlowRate></vehicleFlow>
                </basicData>
              </measuredValue>
            </measuredValue>
        """)
    speed_mvs = ""
    for i, s in enumerate(speeds, len(flows) + 1):
        speed_mvs += textwrap.dedent(f"""\
            <measuredValue index="{i}">
              <measuredValue>
                <basicData xsi:type="TrafficSpeed">
                  <averageVehicleSpeed numberOfInputValuesUsed="1"><speed>{s}</speed></averageVehicleSpeed>
                </basicData>
              </measuredValue>
            </measuredValue>
        """)

    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP:Body>
        <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <payloadPublication xsi:type="MeasuredDataPublication" lang="nl">
          <siteMeasurements xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <measurementSiteReference id="{site_id}" version="1" targetClass="MeasurementSiteRecord"/>
            <measurementTimeDefault>{mtime}</measurementTimeDefault>
            {flow_mvs}
            {speed_mvs}
          </siteMeasurements>
        </payloadPublication>
        </d2LogicalModel>
        </SOAP:Body>
        </SOAP:Envelope>
    """).strip().encode("utf-8")


def _traveltime_xml(site_id="TT_SITE01", mtime="2024-06-01T12:00:00Z",
                     duration=26.2, ref_duration=21.4, accuracy=100.0,
                     data_quality=41.3, n_input=13, data_error=False):
    """Build a minimal DATEX II v2 travel time XML."""
    dur_val = -1.0 if data_error else duration
    ref_val = -1.0 if data_error else ref_duration
    error_tag = "<dataError>true</dataError>" if data_error else ""
    ref_error_tag = "<dataError>true</dataError>" if data_error else ""

    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP:Body>
        <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <payloadPublication xsi:type="MeasuredDataPublication" lang="nl">
          <siteMeasurements xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <measurementSiteReference targetClass="MeasurementSiteRecord" id="{site_id}" version="1"/>
            <measurementTimeDefault>{mtime}</measurementTimeDefault>
            <measuredValue index="1">
              <measuredValue>
                <basicData xsi:type="TravelTimeData">
                  <travelTimeType>reconstituted</travelTimeType>
                  <travelTime accuracy="{accuracy}" numberOfInputValuesUsed="{n_input}" supplierCalculatedDataQuality="{data_quality}">
                    {error_tag}
                    <duration>{dur_val}</duration>
                  </travelTime>
                </basicData>
                <measuredValueExtension>
                  <measuredValueExtended>
                    <basicDataReferenceValue>
                      <referenceValueType>staticReferenceValue</referenceValueType>
                      <travelTimeData>
                        <travelTime accuracy="{accuracy}" numberOfInputValuesUsed="{n_input}" supplierCalculatedDataQuality="{data_quality}">
                          {ref_error_tag}
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
        </SOAP:Body>
        </SOAP:Envelope>
    """).strip().encode("utf-8")


def _situation_xml(sit_id="RWS01_SM001", version_time="2024-06-01T10:00:00Z",
                    severity="medium", record_type="RoadOrCarriagewayOrLaneManagement",
                    cause="roadMaintenance", info_status="real",
                    start_time="2024-06-01T08:00:00Z",
                    end_time="2024-07-01T10:00:00Z"):
    """Build a minimal DATEX II v3 situation XML."""
    cause_block = ""
    if cause:
        cause_block = f"<sit:cause><sit:causeType>{cause}</sit:causeType></sit:cause>"
    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <mc:messageContainer xmlns:sit="http://datex2.eu/schema/3/situation"
            xmlns:mc="http://datex2.eu/schema/3/messageContainer"
            xmlns:com="http://datex2.eu/schema/3/common"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <mc:payload xsi:type="sit:SituationPublication" lang="nl">
            <sit:situation id="{sit_id}">
              <sit:overallSeverity>{severity}</sit:overallSeverity>
              <sit:situationVersionTime>{version_time}</sit:situationVersionTime>
              <sit:headerInformation>
                <com:informationStatus>{info_status}</com:informationStatus>
              </sit:headerInformation>
              <sit:situationRecord xsi:type="sit:{record_type}" id="REC001" version="1">
                {cause_block}
                <sit:validity>
                  <com:validityTimeSpecification>
                    <com:overallStartTime>{start_time}</com:overallStartTime>
                    <com:overallEndTime>{end_time}</com:overallEndTime>
                  </com:validityTimeSpecification>
                </sit:validity>
              </sit:situationRecord>
            </sit:situation>
          </mc:payload>
        </mc:messageContainer>
    """).strip().encode("utf-8")


# ═══════════════════════════════════════════════════════════════════════════
# 1. parse_traffic_speed_xml
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
class TestParseTrafficSpeedXml:

    def test_basic_parsing(self):
        records = parse_traffic_speed_xml(_speed_xml(speeds=[80], flows=[120]))
        assert len(records) == 1
        r = records[0]
        assert r["site_id"] == "SITE01"
        assert r["measurement_time"] == "2024-06-01T12:00:00Z"
        assert r["average_speed"] == 80.0
        assert r["vehicle_flow_rate"] == 120
        assert r["number_of_lanes_with_data"] == 1

    def test_multiple_lanes(self):
        records = parse_traffic_speed_xml(_speed_xml(speeds=[80, 90, 70], flows=[100, 200, 150]))
        r = records[0]
        assert r["average_speed"] == 80.0  # (80+90+70)/3
        assert r["vehicle_flow_rate"] == 450  # 100+200+150
        assert r["number_of_lanes_with_data"] == 3

    def test_negative_speed_excluded(self):
        records = parse_traffic_speed_xml(_speed_xml(speeds=[-1, 80, -1], flows=[0, 120, 0]))
        r = records[0]
        assert r["average_speed"] == 80.0
        assert r["vehicle_flow_rate"] == 120
        assert r["number_of_lanes_with_data"] == 3  # 3 flows parsed

    def test_all_negative_speeds(self):
        records = parse_traffic_speed_xml(_speed_xml(speeds=[-1, -1], flows=[0, 0]))
        r = records[0]
        assert r["average_speed"] is None
        assert r["vehicle_flow_rate"] == 0
        assert r["number_of_lanes_with_data"] == 2

    def test_no_flows(self):
        records = parse_traffic_speed_xml(_speed_xml(speeds=[60], flows=[]))
        r = records[0]
        assert r["average_speed"] == 60.0
        assert r["vehicle_flow_rate"] is None
        assert r["number_of_lanes_with_data"] == 1

    def test_empty_xml(self):
        xml = b"""<?xml version="1.0"?>
        <SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP:Body>
        <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0">
        <payloadPublication/>
        </d2LogicalModel>
        </SOAP:Body></SOAP:Envelope>"""
        assert parse_traffic_speed_xml(xml) == []

    def test_site_id_preserved(self):
        records = parse_traffic_speed_xml(_speed_xml(site_id="PZH01_MST_0029-00"))
        assert records[0]["site_id"] == "PZH01_MST_0029-00"

    def test_measurement_time_preserved(self):
        records = parse_traffic_speed_xml(_speed_xml(mtime="2026-04-08T23:16:00Z"))
        assert records[0]["measurement_time"] == "2026-04-08T23:16:00Z"


# ═══════════════════════════════════════════════════════════════════════════
# 2. parse_travel_time_xml
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
class TestParseTravelTimeXml:

    def test_basic_parsing(self):
        records = parse_travel_time_xml(_traveltime_xml())
        assert len(records) == 1
        r = records[0]
        assert r["site_id"] == "TT_SITE01"
        assert r["measurement_time"] == "2024-06-01T12:00:00Z"
        assert r["duration"] == 26.2
        assert r["reference_duration"] == 21.4
        assert r["accuracy"] == 100.0
        assert r["data_quality"] == 41.3
        assert r["number_of_input_values"] == 13

    def test_data_error_sets_null(self):
        records = parse_travel_time_xml(_traveltime_xml(data_error=True))
        r = records[0]
        assert r["duration"] is None
        assert r["reference_duration"] is None

    def test_site_id_with_special_chars(self):
        records = parse_travel_time_xml(_traveltime_xml(site_id="PNB05_BRE_Keizerstraat_N01"))
        assert records[0]["site_id"] == "PNB05_BRE_Keizerstraat_N01"

    def test_empty_xml(self):
        xml = b"""<?xml version="1.0"?>
        <SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP:Body>
        <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0">
        <payloadPublication/>
        </d2LogicalModel>
        </SOAP:Body></SOAP:Envelope>"""
        assert parse_travel_time_xml(xml) == []

    def test_zero_duration_valid(self):
        records = parse_travel_time_xml(_traveltime_xml(duration=0.0))
        assert records[0]["duration"] == 0.0


# ═══════════════════════════════════════════════════════════════════════════
# 3. parse_situation_xml
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
class TestParseSituationXml:

    def test_basic_parsing(self):
        records = parse_situation_xml(_situation_xml())
        assert len(records) == 1
        r = records[0]
        assert r["situation_id"] == "RWS01_SM001"
        assert r["version_time"] == "2024-06-01T10:00:00Z"
        assert r["severity"] == "medium"
        assert r["record_type"] == "RoadOrCarriagewayOrLaneManagement"
        assert r["cause_type"] == "roadMaintenance"
        assert r["start_time"] == "2024-06-01T08:00:00Z"
        assert r["end_time"] == "2024-07-01T10:00:00Z"
        assert r["information_status"] == "real"

    def test_no_cause(self):
        records = parse_situation_xml(_situation_xml(cause=None))
        assert records[0]["cause_type"] is None

    def test_high_severity(self):
        records = parse_situation_xml(_situation_xml(severity="high"))
        assert records[0]["severity"] == "high"

    def test_test_information_status(self):
        records = parse_situation_xml(_situation_xml(info_status="test"))
        assert records[0]["information_status"] == "test"

    def test_empty_xml(self):
        xml = b"""<?xml version="1.0"?>
        <mc:messageContainer xmlns:mc="http://datex2.eu/schema/3/messageContainer"
            xmlns:sit="http://datex2.eu/schema/3/situation">
          <mc:payload/>
        </mc:messageContainer>"""
        assert parse_situation_xml(xml) == []

    def test_multiple_situations(self):
        xml = b"""<?xml version="1.0"?>
        <mc:messageContainer xmlns:mc="http://datex2.eu/schema/3/messageContainer"
            xmlns:sit="http://datex2.eu/schema/3/situation"
            xmlns:com="http://datex2.eu/schema/3/common"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <mc:payload xsi:type="sit:SituationPublication" lang="nl">
            <sit:situation id="SIT_A">
              <sit:overallSeverity>low</sit:overallSeverity>
              <sit:situationVersionTime>2024-01-01T00:00:00Z</sit:situationVersionTime>
              <sit:headerInformation>
                <com:informationStatus>real</com:informationStatus>
              </sit:headerInformation>
            </sit:situation>
            <sit:situation id="SIT_B">
              <sit:overallSeverity>high</sit:overallSeverity>
              <sit:situationVersionTime>2024-01-02T00:00:00Z</sit:situationVersionTime>
              <sit:headerInformation>
                <com:informationStatus>real</com:informationStatus>
              </sit:headerInformation>
            </sit:situation>
          </mc:payload>
        </mc:messageContainer>"""
        records = parse_situation_xml(xml)
        assert len(records) == 2
        assert records[0]["situation_id"] == "SIT_A"
        assert records[1]["situation_id"] == "SIT_B"


# ═══════════════════════════════════════════════════════════════════════════
# 4. Data class construction
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
class TestDataClasses:

    def test_traffic_speed_roundtrip(self):
        ts = TrafficSpeed(
            site_id="S1", measurement_time="2024-01-01T00:00:00Z",
            average_speed=80.5, vehicle_flow_rate=200, number_of_lanes_with_data=3,
        )
        d = ts.to_serializer_dict()
        assert d["site_id"] == "S1"
        assert d["average_speed"] == 80.5
        ts2 = TrafficSpeed.from_serializer_dict(d)
        assert ts2.site_id == ts.site_id

    def test_traffic_speed_null_speed(self):
        ts = TrafficSpeed(
            site_id="S2", measurement_time="2024-01-01T00:00:00Z",
            average_speed=None, vehicle_flow_rate=None, number_of_lanes_with_data=0,
        )
        d = ts.to_serializer_dict()
        assert d["average_speed"] is None
        assert d["vehicle_flow_rate"] is None

    def test_travel_time_roundtrip(self):
        tt = TravelTime(
            site_id="TT1", measurement_time="2024-01-01T00:00:00Z",
            duration=26.2, reference_duration=21.4, accuracy=100.0,
            data_quality=41.3, number_of_input_values=13,
        )
        d = tt.to_serializer_dict()
        assert d["duration"] == 26.2
        assert d["reference_duration"] == 21.4
        tt2 = TravelTime.from_serializer_dict(d)
        assert tt2.site_id == tt.site_id

    def test_travel_time_null_fields(self):
        tt = TravelTime(
            site_id="TT2", measurement_time="2024-01-01T00:00:00Z",
            duration=None, reference_duration=None,
            accuracy=None, data_quality=None, number_of_input_values=None,
        )
        d = tt.to_serializer_dict()
        assert d["duration"] is None

    def test_traffic_situation_roundtrip(self):
        sit = TrafficSituation(
            situation_id="SIT1", version_time="2024-06-01T10:00:00Z",
            severity="medium", record_type="RoadOrCarriagewayOrLaneManagement",
            cause_type="roadMaintenance", start_time="2024-06-01T08:00:00Z",
            end_time="2024-07-01T10:00:00Z", information_status="real",
        )
        d = sit.to_serializer_dict()
        assert d["situation_id"] == "SIT1"
        sit2 = TrafficSituation.from_serializer_dict(d)
        assert sit2.situation_id == sit.situation_id

    def test_traffic_situation_null_fields(self):
        sit = TrafficSituation(
            situation_id="SIT2", version_time="2024-06-01T10:00:00Z",
            severity=None, record_type=None, cause_type=None,
            start_time=None, end_time=None, information_status="real",
        )
        d = sit.to_serializer_dict()
        assert d["severity"] is None
        assert d["cause_type"] is None

    def test_traffic_speed_json_roundtrip(self):
        ts = TrafficSpeed(
            site_id="S3", measurement_time="2024-01-01T00:00:00Z",
            average_speed=60.0, vehicle_flow_rate=100, number_of_lanes_with_data=2,
        )
        json_bytes = ts.to_byte_array("application/json")
        ts2 = TrafficSpeed.from_data(json_bytes, "application/json")
        assert ts2.site_id == "S3"
        assert ts2.average_speed == 60.0


# ═══════════════════════════════════════════════════════════════════════════
# 5. Connection string parsing
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
class TestConnectionString:

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=key;SharedAccessKey=secret;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert "myhub.servicebus.windows.net:9093" in result["bootstrap.servers"]
        assert result["entity_path"] == "topic1"

    def test_build_kafka_config_simple(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        config, topic = _build_kafka_config(cs, enable_tls=False)
        assert config["bootstrap.servers"] == "localhost:9092"
        assert topic == "test-topic"

    def test_build_kafka_config_tls_disabled(self):
        cs = "BootstrapServer=broker:9092;EntityPath=t"
        config, _ = _build_kafka_config(cs, enable_tls=False)
        assert config.get("security.protocol") == "PLAINTEXT"


# ═══════════════════════════════════════════════════════════════════════════
# 6. StateManager deduplication
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
class TestStateManager:

    def test_new_speed_detected(self, tmp_path):
        sm = StateManager(str(tmp_path / "state.json"))
        assert sm.is_new_speed("S1", "T1") is True
        assert sm.is_new_speed("S1", "T1") is False
        assert sm.is_new_speed("S1", "T2") is True

    def test_new_traveltime_detected(self, tmp_path):
        sm = StateManager(str(tmp_path / "state.json"))
        assert sm.is_new_traveltime("TT1", "T1") is True
        assert sm.is_new_traveltime("TT1", "T1") is False

    def test_new_situation_detected(self, tmp_path):
        sm = StateManager(str(tmp_path / "state.json"))
        assert sm.is_new_situation("SIT1", "V1") is True
        assert sm.is_new_situation("SIT1", "V1") is False
        assert sm.is_new_situation("SIT1", "V2") is True

    def test_save_and_load(self, tmp_path):
        path = str(tmp_path / "state.json")
        sm1 = StateManager(path)
        sm1.is_new_speed("S1", "T1")
        sm1.save()

        sm2 = StateManager(path)
        assert sm2.is_new_speed("S1", "T1") is False
        assert sm2.is_new_speed("S1", "T2") is True

    def test_corrupt_state_file(self, tmp_path):
        path = str(tmp_path / "state.json")
        with open(path, "w") as f:
            f.write("NOT JSON")
        sm = StateManager(path)
        assert sm.is_new_speed("S1", "T1") is True


# ═══════════════════════════════════════════════════════════════════════════
# 7. NdwPoller integration
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.unit
class TestNdwPoller:

    def _make_poller(self, tmp_path):
        mock_meas = MagicMock()
        mock_meas.producer = MagicMock()
        mock_sit = MagicMock()
        mock_sit.producer = MagicMock()
        state = StateManager(str(tmp_path / "state.json"))
        poller = NdwPoller(mock_meas, mock_sit, state, poll_interval=60)
        return poller, mock_meas, mock_sit

    @patch("ndl_netherlands.ndl_netherlands.download_gzip_xml")
    def test_poll_speed_emits_events(self, mock_dl, tmp_path):
        mock_dl.return_value = _speed_xml(speeds=[90], flows=[200])
        poller, mock_meas, _ = self._make_poller(tmp_path)
        count = poller._poll_speed()
        assert count == 1
        mock_meas.send_nl_ndw_traffic_traffic_speed.assert_called_once()
        call_args = mock_meas.send_nl_ndw_traffic_traffic_speed.call_args
        assert call_args[0][0] == "SITE01"

    @patch("ndl_netherlands.ndl_netherlands.download_gzip_xml")
    def test_poll_speed_dedup(self, mock_dl, tmp_path):
        mock_dl.return_value = _speed_xml()
        poller, mock_meas, _ = self._make_poller(tmp_path)
        poller._poll_speed()
        mock_meas.reset_mock()
        mock_dl.return_value = _speed_xml()
        count = poller._poll_speed()
        assert count == 0
        mock_meas.send_nl_ndw_traffic_traffic_speed.assert_not_called()

    @patch("ndl_netherlands.ndl_netherlands.download_gzip_xml")
    def test_poll_traveltime_emits_events(self, mock_dl, tmp_path):
        mock_dl.return_value = _traveltime_xml()
        poller, mock_meas, _ = self._make_poller(tmp_path)
        count = poller._poll_traveltime()
        assert count == 1
        mock_meas.send_nl_ndw_traffic_travel_time.assert_called_once()

    @patch("ndl_netherlands.ndl_netherlands.download_gzip_xml")
    def test_poll_situations_emits_events(self, mock_dl, tmp_path):
        mock_dl.return_value = _situation_xml()
        poller, _, mock_sit = self._make_poller(tmp_path)
        count = poller._poll_situations()
        assert count == 1
        mock_sit.send_nl_ndw_traffic_traffic_situation.assert_called_once()

    @patch("ndl_netherlands.ndl_netherlands.download_gzip_xml")
    def test_poll_and_send_first_cycle(self, mock_dl, tmp_path):
        """First cycle polls speed + traveltime + situations (since last_situation_poll=0)."""
        def side_effect(url, **kw):
            if "trafficspeed" in url:
                return _speed_xml()
            elif "traveltime" in url:
                return _traveltime_xml()
            elif "actueel_beeld" in url:
                return _situation_xml()
            return b""
        mock_dl.side_effect = side_effect
        poller, mock_meas, mock_sit = self._make_poller(tmp_path)
        s, t, sit = poller.poll_and_send()
        assert s == 1
        assert t == 1
        assert sit == 1

    @patch("ndl_netherlands.ndl_netherlands.download_gzip_xml")
    def test_download_failure_returns_zero(self, mock_dl, tmp_path):
        mock_dl.side_effect = Exception("Network error")
        poller, _, _ = self._make_poller(tmp_path)
        assert poller._poll_speed() == 0
        assert poller._poll_traveltime() == 0
        assert poller._poll_situations() == 0
