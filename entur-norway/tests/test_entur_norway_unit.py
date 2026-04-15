"""Unit tests for the Entur Norway SIRI bridge."""

import xml.etree.ElementTree as ET

import pytest

from entur_norway.entur_norway import (
    EnturNorwayBridge,
    _bool_text,
    _find_multilingual_text,
    parse_connection_string,
    parse_duration_to_seconds,
)
from entur_norway_producer_data import (
    DatedServiceJourney,
    EstimatedVehicleJourney,
    MonitoredVehicleJourney,
    PtSituationElement,
)

SIRI_NS = 'http://www.siri.org.uk/siri'
S = f'{{{SIRI_NS}}}'


# ── parse_duration_to_seconds ─────────────────────────────────────────────────


@pytest.mark.unit
class TestParseDurationToSeconds:
    def test_none_returns_none(self):
        assert parse_duration_to_seconds(None) is None

    def test_empty_returns_none(self):
        assert parse_duration_to_seconds('') is None

    def test_minutes_only(self):
        assert parse_duration_to_seconds('PT2M') == 120

    def test_seconds_only(self):
        assert parse_duration_to_seconds('PT30S') == 30

    def test_hours_minutes_seconds(self):
        assert parse_duration_to_seconds('PT1H2M3S') == 3723

    def test_negative_duration(self):
        assert parse_duration_to_seconds('-PT2M') == -120

    def test_negative_with_seconds(self):
        assert parse_duration_to_seconds('-PT1M30S') == -90

    def test_hours_only(self):
        assert parse_duration_to_seconds('PT1H') == 3600

    def test_decimal_seconds(self):
        assert parse_duration_to_seconds('PT1.5S') == 1

    def test_invalid_returns_none(self):
        assert parse_duration_to_seconds('invalid') is None


# ── _bool_text ────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestBoolText:
    def test_none(self):
        assert _bool_text(None) is None

    def test_true(self):
        assert _bool_text('true') is True

    def test_True_caps(self):
        assert _bool_text('True') is True

    def test_1(self):
        assert _bool_text('1') is True

    def test_false(self):
        assert _bool_text('false') is False

    def test_0(self):
        assert _bool_text('0') is False

    def test_empty(self):
        assert _bool_text('') is False


# ── _find_multilingual_text ───────────────────────────────────────────────────


def _make_element_with_text(tag: str, text: str, lang: str = '') -> ET.Element:
    el = ET.Element(f'{S}{tag}')
    if lang:
        el.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
    el.text = text
    return el


@pytest.mark.unit
class TestFindMultilingualText:
    def _make_parent(self, entries):
        parent = ET.Element('parent')
        for lang, text in entries:
            parent.append(_make_element_with_text('Summary', text, lang))
        return parent

    def test_english_preferred(self):
        parent = self._make_parent([('nb', 'Norsk tekst'), ('en', 'English text')])
        assert _find_multilingual_text(parent, 'Summary') == 'English text'

    def test_fallback_to_first(self):
        parent = self._make_parent([('nb', 'Norsk tekst'), ('fr', 'Texte français')])
        assert _find_multilingual_text(parent, 'Summary') == 'Norsk tekst'

    def test_no_elements_returns_none(self):
        parent = ET.Element('parent')
        assert _find_multilingual_text(parent, 'Summary') is None

    def test_eng_lang_code(self):
        parent = self._make_parent([('nb', 'Norsk'), ('eng', 'English')])
        assert _find_multilingual_text(parent, 'Summary') == 'English'


# ── parse_connection_string ───────────────────────────────────────────────────


@pytest.mark.unit
class TestParseConnectionString:
    def test_bootstrap_server(self):
        cs = 'BootstrapServer=localhost:9092;EntityPath=my-topic'
        config, topic = parse_connection_string(cs)
        assert config['bootstrap.servers'] == 'localhost:9092'
        assert topic == 'my-topic'
        assert 'security.protocol' not in config

    def test_event_hubs_format(self):
        cs = 'Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=secret;EntityPath=my-topic'
        config, topic = parse_connection_string(cs)
        assert 'myhub.servicebus.windows.net:9093' in config['bootstrap.servers']
        assert topic == 'my-topic'
        assert config.get('security.protocol') == 'SASL_SSL'

    def test_missing_bootstrap_raises(self):
        with pytest.raises(ValueError):
            parse_connection_string('EntityPath=my-topic')

    def test_no_topic(self):
        cs = 'BootstrapServer=localhost:9092'
        config, topic = parse_connection_string(cs)
        assert config['bootstrap.servers'] == 'localhost:9092'
        assert topic is None


# ── parse_et_journeys ─────────────────────────────────────────────────────────


ET_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <EstimatedTimetableDelivery>
      <EstimatedJourneyVersionFrame>
        <EstimatedVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:1234</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:R10</LineRef>
          <OperatorRef>NSB</OperatorRef>
          <DirectionRef>Inbound</DirectionRef>
          <PublishedLineName xml:lang="en">R10</PublishedLineName>
          <OriginName xml:lang="en">Oslo S</OriginName>
          <DestinationName xml:lang="en">Bergen</DestinationName>
          <Monitored>true</Monitored>
          <IsCompleteStopSequence>true</IsCompleteStopSequence>
          <EstimatedCalls>
            <EstimatedCall>
              <StopPointRef>NSB:StopPlace:1</StopPointRef>
              <Order>1</Order>
              <StopPointName xml:lang="en">Oslo S</StopPointName>
              <AimedDepartureTime>2024-01-15T08:00:00</AimedDepartureTime>
              <ExpectedDepartureTime>2024-01-15T08:02:00</ExpectedDepartureTime>
            </EstimatedCall>
            <EstimatedCall>
              <StopPointRef>NSB:StopPlace:2</StopPointRef>
              <Order>2</Order>
              <AimedArrivalTime>2024-01-15T14:00:00</AimedArrivalTime>
              <ExpectedArrivalTime>2024-01-15T14:05:00</ExpectedArrivalTime>
            </EstimatedCall>
          </EstimatedCalls>
        </EstimatedVehicleJourney>
      </EstimatedJourneyVersionFrame>
    </EstimatedTimetableDelivery>
  </ServiceDelivery>
</Siri>"""


@pytest.mark.unit
class TestParseEtJourneys:
    def setup_method(self):
        self.bridge = EnturNorwayBridge.__new__(EnturNorwayBridge)

    def test_basic_parse(self):
        root = ET.fromstring(ET_XML)
        journeys = self.bridge.parse_et_journeys(root)
        assert len(journeys) == 1
        op_day, sj_id, evj = journeys[0]
        assert op_day == '2024-01-15'
        assert sj_id == 'NSB:ServiceJourney:1234'
        assert isinstance(evj, EstimatedVehicleJourney)
        assert evj.line_ref == 'NSB:Line:R10'
        assert evj.operator_ref == 'NSB'
        assert evj.direction_ref == 'Inbound'
        assert evj.published_line_name == 'R10'
        assert evj.origin_name == 'Oslo S'
        assert evj.destination_name == 'Bergen'
        assert evj.monitored is True
        assert evj.is_complete_stop_sequence is True
        assert evj.is_cancellation is False

    def test_estimated_calls_parsed(self):
        root = ET.fromstring(ET_XML)
        journeys = self.bridge.parse_et_journeys(root)
        evj = journeys[0][2]
        assert len(evj.estimated_calls) == 2
        assert evj.estimated_calls[0].stop_point_ref == 'NSB:StopPlace:1'
        assert evj.estimated_calls[0].order == 1
        assert evj.estimated_calls[0].stop_point_name == 'Oslo S'
        assert evj.estimated_calls[0].aimed_departure_time == '2024-01-15T08:00:00'
        assert evj.estimated_calls[0].expected_departure_time == '2024-01-15T08:02:00'
        assert evj.estimated_calls[1].stop_point_ref == 'NSB:StopPlace:2'

    def test_empty_xml_returns_empty_list(self):
        root = ET.fromstring(f'<Siri xmlns="{SIRI_NS}"><ServiceDelivery/></Siri>')
        assert self.bridge.parse_et_journeys(root) == []

    def test_missing_framed_ref_skipped(self):
        xml = f"""<Siri xmlns="{SIRI_NS}">
          <ServiceDelivery>
            <EstimatedTimetableDelivery>
              <EstimatedJourneyVersionFrame>
                <EstimatedVehicleJourney>
                  <LineRef>NSB:Line:R10</LineRef>
                </EstimatedVehicleJourney>
              </EstimatedJourneyVersionFrame>
            </EstimatedTimetableDelivery>
          </ServiceDelivery>
        </Siri>"""
        root = ET.fromstring(xml)
        assert self.bridge.parse_et_journeys(root) == []

    def test_cancellation_flag(self):
        xml = f"""<Siri xmlns="{SIRI_NS}">
          <ServiceDelivery>
            <EstimatedTimetableDelivery>
              <EstimatedJourneyVersionFrame>
                <EstimatedVehicleJourney>
                  <FramedVehicleJourneyRef>
                    <DataFrameRef>2024-01-15</DataFrameRef>
                    <DatedVehicleJourneyRef>NSB:ServiceJourney:9999</DatedVehicleJourneyRef>
                  </FramedVehicleJourneyRef>
                  <LineRef>NSB:Line:R10</LineRef>
                  <OperatorRef>NSB</OperatorRef>
                  <Cancellation>true</Cancellation>
                </EstimatedVehicleJourney>
              </EstimatedJourneyVersionFrame>
            </EstimatedTimetableDelivery>
          </ServiceDelivery>
        </Siri>"""
        root = ET.fromstring(xml)
        journeys = self.bridge.parse_et_journeys(root)
        assert len(journeys) == 1
        assert journeys[0][2].is_cancellation is True

    def test_extract_reference_journeys(self):
        root = ET.fromstring(ET_XML)
        et_journeys = self.bridge.parse_et_journeys(root)
        refs = self.bridge.extract_reference_journeys(et_journeys)
        assert len(refs) == 1
        op_day, sj_id, dsj = refs[0]
        assert op_day == '2024-01-15'
        assert sj_id == 'NSB:ServiceJourney:1234'
        assert isinstance(dsj, DatedServiceJourney)
        assert dsj.line_ref == 'NSB:Line:R10'
        assert dsj.external_line_ref is None

    def test_deduplicated_reference_journeys(self):
        # Two journeys with the same key → only one reference record
        xml = f"""<Siri xmlns="{SIRI_NS}">
          <ServiceDelivery>
            <EstimatedTimetableDelivery>
              <EstimatedJourneyVersionFrame>
                <EstimatedVehicleJourney>
                  <FramedVehicleJourneyRef>
                    <DataFrameRef>2024-01-15</DataFrameRef>
                    <DatedVehicleJourneyRef>NSB:ServiceJourney:1234</DatedVehicleJourneyRef>
                  </FramedVehicleJourneyRef>
                  <LineRef>NSB:Line:R10</LineRef>
                  <OperatorRef>NSB</OperatorRef>
                </EstimatedVehicleJourney>
                <EstimatedVehicleJourney>
                  <FramedVehicleJourneyRef>
                    <DataFrameRef>2024-01-15</DataFrameRef>
                    <DatedVehicleJourneyRef>NSB:ServiceJourney:1234</DatedVehicleJourneyRef>
                  </FramedVehicleJourneyRef>
                  <LineRef>NSB:Line:R10</LineRef>
                  <OperatorRef>NSB</OperatorRef>
                </EstimatedVehicleJourney>
              </EstimatedJourneyVersionFrame>
            </EstimatedTimetableDelivery>
          </ServiceDelivery>
        </Siri>"""
        root = ET.fromstring(xml)
        et_journeys = self.bridge.parse_et_journeys(root)
        refs = self.bridge.extract_reference_journeys(et_journeys)
        assert len(refs) == 1


# ── parse_vm_journeys ─────────────────────────────────────────────────────────


VM_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <VehicleMonitoringDelivery>
      <VehicleActivity>
        <RecordedAtTime>2024-01-15T08:05:00Z</RecordedAtTime>
        <MonitoredVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:5678</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:L1</LineRef>
          <OperatorRef>NSB</OperatorRef>
          <DirectionRef>Outbound</DirectionRef>
          <VehicleMode>rail</VehicleMode>
          <PublishedLineName xml:lang="en">L1</PublishedLineName>
          <OriginName xml:lang="en">Drammen</OriginName>
          <DestinationName xml:lang="nb">Lillestrøm</DestinationName>
          <Monitored>true</Monitored>
          <VehicleLocation>
            <Longitude>10.7522</Longitude>
            <Latitude>59.9139</Latitude>
          </VehicleLocation>
          <Bearing>45.0</Bearing>
          <Delay>PT2M30S</Delay>
          <VehicleRef>NSB:Vehicle:42</VehicleRef>
          <OccupancyStatus>seatsAvailable</OccupancyStatus>
        </MonitoredVehicleJourney>
      </VehicleActivity>
    </VehicleMonitoringDelivery>
  </ServiceDelivery>
</Siri>"""


@pytest.mark.unit
class TestParseVmJourneys:
    def setup_method(self):
        self.bridge = EnturNorwayBridge.__new__(EnturNorwayBridge)

    def test_basic_parse(self):
        root = ET.fromstring(VM_XML)
        journeys = self.bridge.parse_vm_journeys(root)
        assert len(journeys) == 1
        op_day, sj_id, mvj = journeys[0]
        assert op_day == '2024-01-15'
        assert sj_id == 'NSB:ServiceJourney:5678'
        assert isinstance(mvj, MonitoredVehicleJourney)

    def test_fields(self):
        root = ET.fromstring(VM_XML)
        mvj = self.bridge.parse_vm_journeys(root)[0][2]
        assert mvj.line_ref == 'NSB:Line:L1'
        assert mvj.operator_ref == 'NSB'
        assert mvj.vehicle_mode == 'rail'
        assert mvj.published_line_name == 'L1'
        assert mvj.origin_name == 'Drammen'
        assert mvj.destination_name == 'Lillestrøm'
        assert mvj.monitored is True
        assert mvj.latitude == pytest.approx(59.9139)
        assert mvj.longitude == pytest.approx(10.7522)
        assert mvj.bearing == pytest.approx(45.0)
        assert mvj.delay_seconds == 150  # PT2M30S
        assert mvj.vehicle_ref == 'NSB:Vehicle:42'
        assert mvj.occupancy_status == 'seatsAvailable'
        assert mvj.recorded_at_time == '2024-01-15T08:05:00Z'

    def test_empty_returns_empty_list(self):
        root = ET.fromstring(f'<Siri xmlns="{SIRI_NS}"><ServiceDelivery/></Siri>')
        assert self.bridge.parse_vm_journeys(root) == []

    def test_missing_line_ref_skipped(self):
        xml = f"""<Siri xmlns="{SIRI_NS}">
          <ServiceDelivery>
            <VehicleMonitoringDelivery>
              <VehicleActivity>
                <RecordedAtTime>2024-01-15T08:05:00Z</RecordedAtTime>
                <MonitoredVehicleJourney>
                  <FramedVehicleJourneyRef>
                    <DataFrameRef>2024-01-15</DataFrameRef>
                    <DatedVehicleJourneyRef>NSB:ServiceJourney:0001</DatedVehicleJourneyRef>
                  </FramedVehicleJourneyRef>
                  <Monitored>false</Monitored>
                </MonitoredVehicleJourney>
              </VehicleActivity>
            </VehicleMonitoringDelivery>
          </ServiceDelivery>
        </Siri>"""
        root = ET.fromstring(xml)
        assert self.bridge.parse_vm_journeys(root) == []

    def test_negative_delay(self):
        xml = VM_XML.replace('<Delay>PT2M30S</Delay>', '<Delay>-PT1M</Delay>')
        root = ET.fromstring(xml)
        mvj = self.bridge.parse_vm_journeys(root)[0][2]
        assert mvj.delay_seconds == -60


# ── parse_sx_situations ───────────────────────────────────────────────────────


SX_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <SituationExchangeDelivery>
      <Situations>
        <PtSituationElement>
          <SituationNumber>ENT:SituationNumber:12345</SituationNumber>
          <Version>1</Version>
          <CreationTime>2024-01-15T06:00:00Z</CreationTime>
          <Source>
            <SourceType>directReport</SourceType>
            <Name>Entur</Name>
          </Source>
          <Progress>open</Progress>
          <ValidityPeriod>
            <StartTime>2024-01-15T06:00:00Z</StartTime>
            <EndTime>2024-01-15T23:59:00Z</EndTime>
          </ValidityPeriod>
          <Severity>normal</Severity>
          <Keywords>incident disruption</Keywords>
          <Summary xml:lang="en">Service disruption on R10</Summary>
          <Description xml:lang="en">Trains delayed due to engineering works.</Description>
          <Affects>
            <Networks>
              <AffectedNetwork>
                <AffectedLine>
                  <LineRef>NSB:Line:R10</LineRef>
                </AffectedLine>
              </AffectedNetwork>
            </Networks>
            <StopPoints>
              <AffectedStopPoint>
                <StopPointRef>NSB:StopPlace:1</StopPointRef>
              </AffectedStopPoint>
              <AffectedStopPoint>
                <StopPointRef>NSB:StopPlace:2</StopPointRef>
              </AffectedStopPoint>
            </StopPoints>
          </Affects>
        </PtSituationElement>
      </Situations>
    </SituationExchangeDelivery>
  </ServiceDelivery>
</Siri>"""


@pytest.mark.unit
class TestParseSxSituations:
    def setup_method(self):
        self.bridge = EnturNorwayBridge.__new__(EnturNorwayBridge)

    def test_basic_parse(self):
        root = ET.fromstring(SX_XML)
        situations = self.bridge.parse_sx_situations(root)
        assert len(situations) == 1
        sit_num, sit = situations[0]
        assert sit_num == 'ENT:SituationNumber:12345'
        assert isinstance(sit, PtSituationElement)

    def test_fields(self):
        root = ET.fromstring(SX_XML)
        sit = self.bridge.parse_sx_situations(root)[0][1]
        assert sit.situation_number == 'ENT:SituationNumber:12345'
        assert sit.version == '1'
        assert sit.creation_time == '2024-01-15T06:00:00Z'
        assert sit.source_type == 'directReport'
        assert sit.source_name == 'Entur'
        assert sit.progress == 'open'
        assert sit.severity == 'normal'
        assert sit.keywords == 'incident disruption'
        assert sit.summary == 'Service disruption on R10'
        assert sit.description == 'Trains delayed due to engineering works.'
        assert len(sit.validity_periods) == 1
        assert sit.validity_periods[0].start_time == '2024-01-15T06:00:00Z'
        assert sit.validity_periods[0].end_time == '2024-01-15T23:59:00Z'
        assert sit.affects_line_refs == ['NSB:Line:R10']
        assert sit.affects_stop_point_refs == ['NSB:StopPlace:1', 'NSB:StopPlace:2']

    def test_empty_returns_empty_list(self):
        root = ET.fromstring(f'<Siri xmlns="{SIRI_NS}"><ServiceDelivery/></Siri>')
        assert self.bridge.parse_sx_situations(root) == []

    def test_missing_situation_number_skipped(self):
        xml = f"""<Siri xmlns="{SIRI_NS}">
          <ServiceDelivery>
            <SituationExchangeDelivery>
              <Situations>
                <PtSituationElement>
                  <CreationTime>2024-01-15T06:00:00Z</CreationTime>
                </PtSituationElement>
              </Situations>
            </SituationExchangeDelivery>
          </ServiceDelivery>
        </Siri>"""
        root = ET.fromstring(xml)
        assert self.bridge.parse_sx_situations(root) == []

    def test_no_situations_element(self):
        xml = f"""<Siri xmlns="{SIRI_NS}">
          <ServiceDelivery>
            <SituationExchangeDelivery>
            </SituationExchangeDelivery>
          </ServiceDelivery>
        </Siri>"""
        root = ET.fromstring(xml)
        assert self.bridge.parse_sx_situations(root) == []
