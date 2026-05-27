"""Unit tests for the French Road Traffic bridge."""

import json
import xml.etree.ElementTree as ET

import pytest

from french_road_traffic.french_road_traffic import (
    parse_traffic_flow_xml,
    parse_road_events_xml,
    parse_connection_string,
    _find,
    _findall,
    _text,
    _extract_comments,
    _extract_location,
    DATEX2_NS,
    XSI_NS,
    SOAP_NS,
)


# ---------------------------------------------------------------------------
# Sample XML fixtures
# ---------------------------------------------------------------------------

TRAFFIC_FLOW_XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<d2LogicalModel modelBaseVersion="2" xmlns="http://datex2.eu/schema/2/2_0">
    <exchange>
        <supplierIdentification>
            <country>fr</country>
            <nationalIdentifier>TIPI</nationalIdentifier>
        </supplierIdentification>
    </exchange>
    <payloadPublication xsi:type="MeasuredDataPublication" lang="fre"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <publicationTime>2026-04-09T00:42:00.000+02:00</publicationTime>
        <publicationCreator>
            <country>fr</country>
            <nationalIdentifier>TIPI</nationalIdentifier>
        </publicationCreator>
        <headerInformation>
            <confidentiality>noRestriction</confidentiality>
            <informationStatus>real</informationStatus>
        </headerInformation>
        <siteMeasurements>
            <measurementSiteReference targetClass="MeasurementSiteRecord" id="MUM76.h1" version="1.0"/>
            <measurementTimeDefault>2026-04-09T00:48:00.000+02:00</measurementTimeDefault>
            <measuredValue index="0">
                <measuredValue>
                    <basicData xsi:type="TrafficFlow">
                        <vehicleFlow numberOfInputValuesUsed="7">
                            <vehicleFlowRate>70</vehicleFlowRate>
                        </vehicleFlow>
                    </basicData>
                </measuredValue>
            </measuredValue>
            <measuredValue index="0">
                <measuredValue>
                    <basicData xsi:type="TrafficSpeed">
                        <averageVehicleSpeed numberOfInputValuesUsed="7">
                            <speed>92.0</speed>
                        </averageVehicleSpeed>
                    </basicData>
                </measuredValue>
            </measuredValue>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference targetClass="MeasurementSiteRecord" id="MB631.B8" version="1.0"/>
            <measurementTimeDefault>2026-04-09T00:48:00.000+02:00</measurementTimeDefault>
            <measuredValue index="0">
                <measuredValue>
                    <basicData xsi:type="TrafficFlow">
                        <vehicleFlow numberOfInputValuesUsed="82">
                            <vehicleFlowRate>820</vehicleFlowRate>
                        </vehicleFlow>
                    </basicData>
                </measuredValue>
            </measuredValue>
            <measuredValue index="0">
                <measuredValue>
                    <basicData xsi:type="TrafficSpeed">
                        <averageVehicleSpeed numberOfInputValuesUsed="82">
                            <speed>82.166664</speed>
                        </averageVehicleSpeed>
                    </basicData>
                </measuredValue>
            </measuredValue>
        </siteMeasurements>
    </payloadPublication>
</d2LogicalModel>"""

TRAFFIC_FLOW_ONLY_SPEED_XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<d2LogicalModel modelBaseVersion="2" xmlns="http://datex2.eu/schema/2/2_0">
    <payloadPublication xsi:type="MeasuredDataPublication" lang="fre"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <siteMeasurements>
            <measurementSiteReference id="SPEED_ONLY" version="1.0"/>
            <measurementTimeDefault>2026-01-01T00:00:00.000+02:00</measurementTimeDefault>
            <measuredValue index="0">
                <measuredValue>
                    <basicData xsi:type="TrafficSpeed">
                        <averageVehicleSpeed numberOfInputValuesUsed="5">
                            <speed>110.5</speed>
                        </averageVehicleSpeed>
                    </basicData>
                </measuredValue>
            </measuredValue>
        </siteMeasurements>
    </payloadPublication>
</d2LogicalModel>"""

TRAFFIC_FLOW_EMPTY_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<d2LogicalModel modelBaseVersion="2" xmlns="http://datex2.eu/schema/2/2_0">
    <payloadPublication xsi:type="MeasuredDataPublication"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    </payloadPublication>
</d2LogicalModel>"""

TRAFFIC_FLOW_NO_PAYLOAD_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<d2LogicalModel modelBaseVersion="2" xmlns="http://datex2.eu/schema/2/2_0">
    <exchange/>
</d2LogicalModel>"""


ROAD_EVENT_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
<soap:Body>
<d2LogicalModel xmlns:ns2="http://datex2.eu/schema/2/2_0" modelBaseVersion="2">
<ns2:exchange>
    <ns2:supplierIdentification>
        <ns2:country>fr</ns2:country>
        <ns2:nationalIdentifier>Tipi</ns2:nationalIdentifier>
    </ns2:supplierIdentification>
</ns2:exchange>
<ns2:payloadPublication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:type="ns2:SituationPublication" lang="fr">
    <ns2:publicationTime>2026-04-09T00:06:54.064+02:00</ns2:publicationTime>
    <ns2:situation id="230814-001797" version="4">
        <ns2:overallSeverity>medium</ns2:overallSeverity>
        <ns2:headerInformation>
            <ns2:confidentiality>noRestriction</ns2:confidentiality>
            <ns2:informationStatus>real</ns2:informationStatus>
        </ns2:headerInformation>
        <ns2:situationRecord xsi:type="ns2:RoadOrCarriagewayOrLaneManagement"
            id="230814-001797-1" version="4">
            <ns2:situationRecordCreationTime>2023-08-14T16:55:00.071+02:00</ns2:situationRecordCreationTime>
            <ns2:situationRecordObservationTime>2025-03-06T08:40:04.071+01:00</ns2:situationRecordObservationTime>
            <ns2:probabilityOfOccurrence>certain</ns2:probabilityOfOccurrence>
            <ns2:source>
                <ns2:sourceIdentification>DIR Sud-Ouest</ns2:sourceIdentification>
                <ns2:reliable>true</ns2:reliable>
            </ns2:source>
            <ns2:validity>
                <ns2:validityStatus>definedByValidityTimeSpec</ns2:validityStatus>
                <ns2:validityTimeSpecification>
                    <ns2:overallStartTime>2023-08-14T16:55:00.071+02:00</ns2:overallStartTime>
                </ns2:validityTimeSpecification>
            </ns2:validity>
            <ns2:generalPublicComment>
                <ns2:comment>
                    <ns2:values><ns2:value lang="fr">DIR Sud-Ouest/District Sud</ns2:value></ns2:values>
                </ns2:comment>
                <ns2:commentType>locationDescriptor</ns2:commentType>
            </ns2:generalPublicComment>
            <ns2:generalPublicComment>
                <ns2:comment>
                    <ns2:values><ns2:value lang="fr">Weight restriction active</ns2:value></ns2:values>
                </ns2:comment>
                <ns2:commentType>description</ns2:commentType>
            </ns2:generalPublicComment>
            <ns2:groupOfLocations xsi:type="ns2:Point">
                <ns2:tpegPointLocation xsi:type="ns2:TpegSimplePoint">
                    <ns2:tpegDirection>bothWays</ns2:tpegDirection>
                    <ns2:point xsi:type="ns2:TpegNonJunctionPoint">
                        <ns2:pointCoordinates>
                            <ns2:latitude>42.844486</ns2:latitude>
                            <ns2:longitude>1.601671</ns2:longitude>
                        </ns2:pointCoordinates>
                        <ns2:name>
                            <ns2:descriptor><ns2:values><ns2:value lang="fr">Tarascon-sur-Ariege</ns2:value></ns2:values></ns2:descriptor>
                            <ns2:tpegOtherPointDescriptorType>townName</ns2:tpegOtherPointDescriptorType>
                        </ns2:name>
                        <ns2:name>
                            <ns2:descriptor><ns2:values><ns2:value lang="fr">N20</ns2:value></ns2:values></ns2:descriptor>
                            <ns2:tpegOtherPointDescriptorType>linkName</ns2:tpegOtherPointDescriptorType>
                        </ns2:name>
                    </ns2:point>
                </ns2:tpegPointLocation>
                <ns2:pointAlongLinearElement>
                    <ns2:linearElement>
                        <ns2:roadNumber>N0020</ns2:roadNumber>
                    </ns2:linearElement>
                </ns2:pointAlongLinearElement>
            </ns2:groupOfLocations>
        </ns2:situationRecord>
    </ns2:situation>
    <ns2:situation id="250428-001558" version="1">
        <ns2:overallSeverity>high</ns2:overallSeverity>
        <ns2:situationRecord xsi:type="ns2:Accident" id="250428-001558-1" version="1">
            <ns2:situationRecordCreationTime>2026-04-01T10:00:00.000+02:00</ns2:situationRecordCreationTime>
            <ns2:probabilityOfOccurrence>certain</ns2:probabilityOfOccurrence>
            <ns2:groupOfLocations xsi:type="ns2:Point">
                <ns2:tpegPointLocation xsi:type="ns2:TpegSimplePoint">
                    <ns2:tpegDirection>positive</ns2:tpegDirection>
                    <ns2:point xsi:type="ns2:TpegNonJunctionPoint">
                        <ns2:pointCoordinates>
                            <ns2:latitude>48.856</ns2:latitude>
                            <ns2:longitude>2.352</ns2:longitude>
                        </ns2:pointCoordinates>
                    </ns2:point>
                </ns2:tpegPointLocation>
            </ns2:groupOfLocations>
        </ns2:situationRecord>
    </ns2:situation>
</ns2:payloadPublication>
</d2LogicalModel>
</soap:Body>
</soap:Envelope>"""


ROAD_EVENT_NO_LOCATION_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
<soap:Body>
<d2LogicalModel xmlns:ns2="http://datex2.eu/schema/2/2_0" modelBaseVersion="2">
<ns2:payloadPublication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:type="ns2:SituationPublication" lang="fr">
    <ns2:situation id="TEST-NOLOC" version="1">
        <ns2:situationRecord xsi:type="ns2:MaintenanceWorks" id="TEST-NOLOC-1" version="1">
            <ns2:situationRecordCreationTime>2026-01-01T00:00:00.000+02:00</ns2:situationRecordCreationTime>
        </ns2:situationRecord>
    </ns2:situation>
</ns2:payloadPublication>
</d2LogicalModel>
</soap:Body>
</soap:Envelope>"""

ROAD_EVENT_EMPTY_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
<soap:Body>
<d2LogicalModel xmlns:ns2="http://datex2.eu/schema/2/2_0" modelBaseVersion="2">
<ns2:payloadPublication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:type="ns2:SituationPublication" lang="fr">
</ns2:payloadPublication>
</d2LogicalModel>
</soap:Body>
</soap:Envelope>"""

ROAD_EVENT_MULTI_LOCATION_DESC_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
<soap:Body>
<d2LogicalModel xmlns:ns2="http://datex2.eu/schema/2/2_0" modelBaseVersion="2">
<ns2:payloadPublication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:type="ns2:SituationPublication" lang="fr">
    <ns2:situation id="MULTI-DESC" version="2">
        <ns2:overallSeverity>low</ns2:overallSeverity>
        <ns2:situationRecord xsi:type="ns2:ConstructionWorks" id="MULTI-DESC-1" version="2">
            <ns2:situationRecordCreationTime>2026-02-01T00:00:00+01:00</ns2:situationRecordCreationTime>
            <ns2:generalPublicComment>
                <ns2:comment><ns2:values><ns2:value lang="fr">Location A</ns2:value></ns2:values></ns2:comment>
                <ns2:commentType>locationDescriptor</ns2:commentType>
            </ns2:generalPublicComment>
            <ns2:generalPublicComment>
                <ns2:comment><ns2:values><ns2:value lang="fr">Location B</ns2:value></ns2:values></ns2:comment>
                <ns2:commentType>locationDescriptor</ns2:commentType>
            </ns2:generalPublicComment>
            <ns2:generalPublicComment>
                <ns2:comment><ns2:values><ns2:value lang="fr">Road works ahead</ns2:value></ns2:values></ns2:comment>
                <ns2:commentType>description</ns2:commentType>
            </ns2:generalPublicComment>
        </ns2:situationRecord>
    </ns2:situation>
</ns2:payloadPublication>
</d2LogicalModel>
</soap:Body>
</soap:Envelope>"""

ROAD_EVENT_WITH_END_TIME_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
<soap:Body>
<d2LogicalModel xmlns:ns2="http://datex2.eu/schema/2/2_0" modelBaseVersion="2">
<ns2:payloadPublication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:type="ns2:SituationPublication" lang="fr">
    <ns2:situation id="ENDTIME-001" version="3">
        <ns2:overallSeverity>low</ns2:overallSeverity>
        <ns2:situationRecord xsi:type="ns2:SpeedManagement" id="ENDTIME-001-1" version="3">
            <ns2:situationRecordCreationTime>2026-03-01T08:00:00+01:00</ns2:situationRecordCreationTime>
            <ns2:validity>
                <ns2:validityStatus>active</ns2:validityStatus>
                <ns2:validityTimeSpecification>
                    <ns2:overallStartTime>2026-03-01T08:00:00+01:00</ns2:overallStartTime>
                    <ns2:overallEndTime>2026-03-15T18:00:00+01:00</ns2:overallEndTime>
                </ns2:validityTimeSpecification>
            </ns2:validity>
        </ns2:situationRecord>
    </ns2:situation>
</ns2:payloadPublication>
</d2LogicalModel>
</soap:Body>
</soap:Envelope>"""


# ---------------------------------------------------------------------------
# Tests — Traffic Flow XML parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseTrafficFlowXml:
    """Tests for parse_traffic_flow_xml()."""

    def test_parses_two_sites(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert len(results) == 2

    def test_first_site_id(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert results[0]["site_id"] == "MUM76.h1"

    def test_second_site_id(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert results[1]["site_id"] == "MB631.B8"

    def test_measurement_time(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert results[0]["measurement_time"] == "2026-04-09T00:48:00.000+02:00"

    def test_vehicle_flow_rate(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert results[0]["vehicle_flow_rate"] == 70
        assert results[1]["vehicle_flow_rate"] == 820

    def test_average_speed(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert results[0]["average_speed"] == 92.0
        assert abs(results[1]["average_speed"] - 82.166664) < 0.001

    def test_input_values_flow(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert results[0]["input_values_flow"] == 7
        assert results[1]["input_values_flow"] == 82

    def test_input_values_speed(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_XML)
        assert results[0]["input_values_speed"] == 7
        assert results[1]["input_values_speed"] == 82

    def test_speed_only_site(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_ONLY_SPEED_XML)
        assert len(results) == 1
        assert results[0]["site_id"] == "SPEED_ONLY"
        assert results[0]["vehicle_flow_rate"] is None
        assert results[0]["input_values_flow"] is None
        assert results[0]["average_speed"] == 110.5
        assert results[0]["input_values_speed"] == 5

    def test_empty_payload(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_EMPTY_XML)
        assert results == []

    def test_no_payload(self):
        results = parse_traffic_flow_xml(TRAFFIC_FLOW_NO_PAYLOAD_XML)
        assert results == []

    def test_missing_site_id_skipped(self):
        xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0">
            <payloadPublication xsi:type="MeasuredDataPublication"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <siteMeasurements>
                    <measurementSiteReference id="" version="1.0"/>
                    <measurementTimeDefault>2026-01-01T00:00:00+00:00</measurementTimeDefault>
                </siteMeasurements>
            </payloadPublication>
        </d2LogicalModel>"""
        results = parse_traffic_flow_xml(xml)
        assert len(results) == 0

    def test_missing_time_skipped(self):
        xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0">
            <payloadPublication xsi:type="MeasuredDataPublication"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <siteMeasurements>
                    <measurementSiteReference id="NOTIME" version="1.0"/>
                </siteMeasurements>
            </payloadPublication>
        </d2LogicalModel>"""
        results = parse_traffic_flow_xml(xml)
        assert len(results) == 0

    def test_invalid_flow_rate_returns_none(self):
        xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0">
            <payloadPublication xsi:type="MeasuredDataPublication"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <siteMeasurements>
                    <measurementSiteReference id="BADVAL" version="1.0"/>
                    <measurementTimeDefault>2026-01-01T00:00:00+00:00</measurementTimeDefault>
                    <measuredValue index="0">
                        <measuredValue>
                            <basicData xsi:type="TrafficFlow">
                                <vehicleFlow>
                                    <vehicleFlowRate>NOT_A_NUMBER</vehicleFlowRate>
                                </vehicleFlow>
                            </basicData>
                        </measuredValue>
                    </measuredValue>
                </siteMeasurements>
            </payloadPublication>
        </d2LogicalModel>"""
        results = parse_traffic_flow_xml(xml)
        assert len(results) == 1
        assert results[0]["vehicle_flow_rate"] is None


# ---------------------------------------------------------------------------
# Tests — Road Events XML parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseRoadEventsXml:
    """Tests for parse_road_events_xml()."""

    def test_parses_two_situations(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert len(results) == 2

    def test_first_situation_id(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["situation_id"] == "230814-001797"

    def test_first_record_id(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["record_id"] == "230814-001797-1"

    def test_first_version(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["version"] == "4"

    def test_first_severity(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["severity"] == "medium"

    def test_first_record_type(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["record_type"] == "RoadOrCarriagewayOrLaneManagement"

    def test_first_probability(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["probability"] == "certain"

    def test_first_latitude(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert abs(results[0]["latitude"] - 42.844486) < 0.0001

    def test_first_longitude(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert abs(results[0]["longitude"] - 1.601671) < 0.0001

    def test_first_road_number(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["road_number"] == "N0020"

    def test_first_town_name(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["town_name"] == "Tarascon-sur-Ariege"

    def test_first_direction(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["direction"] == "bothWays"

    def test_first_description(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["description"] == "Weight restriction active"

    def test_first_location_description(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["location_description"] == "DIR Sud-Ouest/District Sud"

    def test_first_source_name(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["source_name"] == "DIR Sud-Ouest"

    def test_first_validity_status(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["validity_status"] == "definedByValidityTimeSpec"

    def test_first_overall_start_time(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["overall_start_time"] == "2023-08-14T16:55:00.071+02:00"

    def test_first_overall_end_time_none(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["overall_end_time"] is None

    def test_first_creation_time(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["creation_time"] == "2023-08-14T16:55:00.071+02:00"

    def test_first_observation_time(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[0]["observation_time"] == "2025-03-06T08:40:04.071+01:00"

    def test_second_situation_is_accident(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[1]["situation_id"] == "250428-001558"
        assert results[1]["record_type"] == "Accident"
        assert results[1]["severity"] == "high"
        assert abs(results[1]["latitude"] - 48.856) < 0.001
        assert abs(results[1]["longitude"] - 2.352) < 0.001

    def test_no_location_event(self):
        results = parse_road_events_xml(ROAD_EVENT_NO_LOCATION_XML)
        assert len(results) == 1
        assert results[0]["latitude"] is None
        assert results[0]["longitude"] is None
        assert results[0]["road_number"] is None
        assert results[0]["town_name"] is None
        assert results[0]["direction"] is None
        assert results[0]["record_type"] == "MaintenanceWorks"

    def test_empty_situations(self):
        results = parse_road_events_xml(ROAD_EVENT_EMPTY_XML)
        assert results == []

    def test_multi_location_descriptors_concatenated(self):
        results = parse_road_events_xml(ROAD_EVENT_MULTI_LOCATION_DESC_XML)
        assert len(results) == 1
        assert results[0]["location_description"] == "Location A | Location B"
        assert results[0]["description"] == "Road works ahead"
        assert results[0]["record_type"] == "ConstructionWorks"

    def test_end_time_present(self):
        results = parse_road_events_xml(ROAD_EVENT_WITH_END_TIME_XML)
        assert len(results) == 1
        assert results[0]["overall_end_time"] == "2026-03-15T18:00:00+01:00"
        assert results[0]["overall_start_time"] == "2026-03-01T08:00:00+01:00"
        assert results[0]["validity_status"] == "active"
        assert results[0]["record_type"] == "SpeedManagement"

    def test_second_situation_no_comments(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[1]["description"] is None
        assert results[1]["location_description"] is None
        assert results[1]["source_name"] is None

    def test_second_situation_direction(self):
        results = parse_road_events_xml(ROAD_EVENT_XML)
        assert results[1]["direction"] == "positive"


# ---------------------------------------------------------------------------
# Tests — Connection string parsing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestParseConnectionString:
    """Tests for parse_connection_string()."""

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=mykey;SharedAccessKey=secret;EntityPath=mytopic"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "myhub.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "mytopic"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["security.protocol"] == "SASL_SSL"

    def test_plain_bootstrap_connection_string(self):
        cs = "BootstrapServer=localhost:9092;EntityPath=test-topic"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "test-topic"
        assert "sasl.username" not in result

    def test_bootstrap_only(self):
        cs = "BootstrapServer=broker:19092"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "broker:19092"
        assert "kafka_topic" not in result

    def test_empty_string_returns_empty_config(self):
        result = parse_connection_string("")
        assert "bootstrap.servers" not in result


# ---------------------------------------------------------------------------
# Tests — XML helper functions
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestXmlHelpers:
    """Tests for _find, _findall, _text helpers."""

    def test_find_with_namespace(self):
        xml = f'<root xmlns="{DATEX2_NS}"><child>hello</child></root>'
        root = ET.fromstring(xml)
        result = _find(root, "child")
        assert result is not None
        assert result.text == "hello"

    def test_findall_returns_multiple(self):
        xml = f'<root xmlns="{DATEX2_NS}"><item>a</item><item>b</item></root>'
        root = ET.fromstring(xml)
        results = _findall(root, "item")
        assert len(results) == 2

    def test_text_returns_content(self):
        xml = f'<root xmlns="{DATEX2_NS}"><value>42</value></root>'
        root = ET.fromstring(xml)
        assert _text(root, "value") == "42"

    def test_text_returns_none_for_missing(self):
        xml = f'<root xmlns="{DATEX2_NS}"></root>'
        root = ET.fromstring(xml)
        assert _text(root, "nonexistent") is None

    def test_find_without_namespace(self):
        xml = '<root><child>world</child></root>'
        root = ET.fromstring(xml)
        result = _find(root, "child", ns=None)
        assert result is not None
        assert result.text == "world"


# ---------------------------------------------------------------------------
# Tests — Comment extraction
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestExtractComments:
    """Tests for _extract_comments()."""

    def test_extracts_description_and_location(self):
        xml = f"""<record xmlns="{DATEX2_NS}">
            <generalPublicComment>
                <comment><values><value>My description</value></values></comment>
                <commentType>description</commentType>
            </generalPublicComment>
            <generalPublicComment>
                <comment><values><value>My location</value></values></comment>
                <commentType>locationDescriptor</commentType>
            </generalPublicComment>
        </record>"""
        record = ET.fromstring(xml)
        desc, loc = _extract_comments(record)
        assert desc == "My description"
        assert loc == "My location"

    def test_no_comments_returns_nones(self):
        xml = f'<record xmlns="{DATEX2_NS}"></record>'
        record = ET.fromstring(xml)
        desc, loc = _extract_comments(record)
        assert desc is None
        assert loc is None

    def test_multiple_location_descriptors_concatenated(self):
        xml = f"""<record xmlns="{DATEX2_NS}">
            <generalPublicComment>
                <comment><values><value>Loc A</value></values></comment>
                <commentType>locationDescriptor</commentType>
            </generalPublicComment>
            <generalPublicComment>
                <comment><values><value>Loc B</value></values></comment>
                <commentType>locationDescriptor</commentType>
            </generalPublicComment>
        </record>"""
        record = ET.fromstring(xml)
        desc, loc = _extract_comments(record)
        assert desc is None
        assert loc == "Loc A | Loc B"


# ---------------------------------------------------------------------------
# Tests — Location extraction
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestExtractLocation:
    """Tests for _extract_location()."""

    def test_extracts_coordinates(self):
        xml = f"""<record xmlns="{DATEX2_NS}">
            <groupOfLocations>
                <tpegPointLocation>
                    <tpegDirection>positive</tpegDirection>
                    <point>
                        <pointCoordinates>
                            <latitude>48.8566</latitude>
                            <longitude>2.3522</longitude>
                        </pointCoordinates>
                    </point>
                </tpegPointLocation>
            </groupOfLocations>
        </record>"""
        record = ET.fromstring(xml)
        lat, lon, road, town, direction = _extract_location(record)
        assert abs(lat - 48.8566) < 0.0001
        assert abs(lon - 2.3522) < 0.0001
        assert direction == "positive"

    def test_no_group_returns_nones(self):
        xml = f'<record xmlns="{DATEX2_NS}"></record>'
        record = ET.fromstring(xml)
        lat, lon, road, town, direction = _extract_location(record)
        assert lat is None
        assert lon is None
        assert road is None
        assert town is None
        assert direction is None

    def test_road_number_from_linear_element(self):
        xml = f"""<record xmlns="{DATEX2_NS}">
            <groupOfLocations>
                <pointAlongLinearElement>
                    <linearElement>
                        <roadNumber>A10</roadNumber>
                    </linearElement>
                </pointAlongLinearElement>
            </groupOfLocations>
        </record>"""
        record = ET.fromstring(xml)
        _, _, road, _, _ = _extract_location(record)
        assert road == "A10"


# ---------------------------------------------------------------------------
# Tests — Data class construction
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestDataClassConstruction:
    """Tests that generated data classes can be constructed correctly."""

    def test_traffic_flow_measurement(self):
        from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement
        m = TrafficFlowMeasurement(
            site_id="TEST01",
            measurement_time="2026-01-01T00:00:00+00:00",
            vehicle_flow_rate=100,
            average_speed=80.5,
            input_values_flow=10,
            input_values_speed=10,
        )
        assert m.site_id == "TEST01"
        assert m.vehicle_flow_rate == 100
        assert m.average_speed == 80.5

    def test_traffic_flow_measurement_nulls(self):
        from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement
        m = TrafficFlowMeasurement(
            site_id="TEST02",
            measurement_time="2026-01-01T00:00:00+00:00",
            vehicle_flow_rate=None,
            average_speed=None,
            input_values_flow=None,
            input_values_speed=None,
        )
        assert m.vehicle_flow_rate is None
        assert m.average_speed is None

    def test_road_event(self):
        from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent
        ev = RoadEvent(
            situation_id="SIT-001",
            record_id="SIT-001-1",
            version="1",
            severity="high",
            record_type="Accident",
            probability="certain",
            latitude=48.856,
            longitude=2.352,
            road_number="A1",
            town_name="Paris",
            direction="positive",
            description="Major accident",
            location_description="Near exit 5",
            source_name="DIR IdF",
            validity_status="active",
            overall_start_time="2026-01-01T08:00:00+01:00",
            overall_end_time="2026-01-01T12:00:00+01:00",
            creation_time="2026-01-01T08:00:00+01:00",
            observation_time="2026-01-01T08:30:00+01:00",
        )
        assert ev.situation_id == "SIT-001"
        assert ev.record_type == "Accident"
        assert ev.latitude == 48.856

    def test_road_event_all_nulls(self):
        from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent
        ev = RoadEvent(
            situation_id="SIT-002",
            record_id="SIT-002-1",
            version="1",
            severity=None,
            record_type="MaintenanceWorks",
            probability=None,
            latitude=None,
            longitude=None,
            road_number=None,
            town_name=None,
            direction=None,
            description=None,
            location_description=None,
            source_name=None,
            validity_status=None,
            overall_start_time=None,
            overall_end_time=None,
            creation_time="2026-01-01T00:00:00+00:00",
            observation_time=None,
        )
        assert ev.severity is None
        assert ev.latitude is None

    def test_traffic_flow_to_json(self):
        from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement
        m = TrafficFlowMeasurement(
            site_id="JSON01",
            measurement_time="2026-01-01T00:00:00+00:00",
            vehicle_flow_rate=50,
            average_speed=60.0,
            input_values_flow=5,
            input_values_speed=5,
        )
        j = json.loads(m.to_json())
        assert j["site_id"] == "JSON01"
        assert j["vehicle_flow_rate"] == 50

    def test_road_event_to_json(self):
        from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent
        ev = RoadEvent(
            situation_id="JSON-SIT",
            record_id="JSON-SIT-1",
            version="1",
            severity="low",
            record_type="ConstructionWorks",
            probability=None,
            latitude=43.0,
            longitude=1.0,
            road_number="D906",
            town_name="Toulouse",
            direction=None,
            description="Works",
            location_description=None,
            source_name=None,
            validity_status=None,
            overall_start_time=None,
            overall_end_time=None,
            creation_time="2026-01-01T00:00:00+00:00",
            observation_time=None,
        )
        j = json.loads(ev.to_json())
        assert j["situation_id"] == "JSON-SIT"
        assert j["record_type"] == "ConstructionWorks"
        assert j["latitude"] == 43.0
