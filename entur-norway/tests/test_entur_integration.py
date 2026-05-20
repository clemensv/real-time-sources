"""Integration tests for the Entur Norway SIRI bridge using requests_mock."""

import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, patch

import pytest
import requests_mock as requests_mock_module

from entur_norway.entur_norway import EnturNorwayBridge
from entur_norway_producer_data import (
    EstimatedVehicleJourney,
    MonitoredVehicleJourney,
    PtSituationElement,
)

SIRI_NS = 'http://www.siri.org.uk/siri'

ET_RESPONSE = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>false</MoreData>
    <EstimatedTimetableDelivery>
      <EstimatedJourneyVersionFrame>
        <EstimatedVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:1</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:R10</LineRef>
          <OperatorRef>NSB</OperatorRef>
          <Monitored>true</Monitored>
          <EstimatedCalls>
            <EstimatedCall>
              <StopPointRef>NSB:StopPlace:1</StopPointRef>
              <Order>1</Order>
              <AimedDepartureTime>2024-01-15T08:00:00</AimedDepartureTime>
            </EstimatedCall>
          </EstimatedCalls>
        </EstimatedVehicleJourney>
        <EstimatedVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:2</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:L1</LineRef>
          <OperatorRef>NSB</OperatorRef>
          <Cancellation>true</Cancellation>
        </EstimatedVehicleJourney>
      </EstimatedJourneyVersionFrame>
    </EstimatedTimetableDelivery>
  </ServiceDelivery>
</Siri>"""

VM_RESPONSE = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>false</MoreData>
    <VehicleMonitoringDelivery>
      <VehicleActivity>
        <RecordedAtTime>2024-01-15T08:10:00Z</RecordedAtTime>
        <MonitoredVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:1</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:R10</LineRef>
          <OperatorRef>NSB</OperatorRef>
          <Monitored>true</Monitored>
          <VehicleLocation>
            <Longitude>10.75</Longitude>
            <Latitude>59.91</Latitude>
          </VehicleLocation>
          <Delay>PT3M</Delay>
        </MonitoredVehicleJourney>
      </VehicleActivity>
    </VehicleMonitoringDelivery>
  </ServiceDelivery>
</Siri>"""

SX_RESPONSE = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>false</MoreData>
    <SituationExchangeDelivery>
      <Situations>
        <PtSituationElement>
          <SituationNumber>ENT:SituationNumber:1</SituationNumber>
          <CreationTime>2024-01-15T06:00:00Z</CreationTime>
          <Progress>open</Progress>
          <Severity>normal</Severity>
          <Summary xml:lang="en">Track work on R10</Summary>
          <ValidityPeriod>
            <StartTime>2024-01-15T06:00:00Z</StartTime>
            <EndTime>2024-01-15T20:00:00Z</EndTime>
          </ValidityPeriod>
          <Affects>
            <Networks>
              <AffectedNetwork>
                <AffectedLine>
                  <LineRef>NSB:Line:R10</LineRef>
                </AffectedLine>
              </AffectedNetwork>
            </Networks>
          </Affects>
        </PtSituationElement>
      </Situations>
    </SituationExchangeDelivery>
  </ServiceDelivery>
</Siri>"""


@pytest.mark.integration
class TestFetchAndParseEt:
    def test_fetch_et_parses_journeys(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/et', text=ET_RESPONSE)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('et')
            assert root is not None
            journeys = bridge.parse_et_journeys(root)
            assert len(journeys) == 2

    def test_et_journey_fields(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/et', text=ET_RESPONSE)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('et')
            journeys = bridge.parse_et_journeys(root)
            # First journey
            op_day, sj_id, evj = journeys[0]
            assert op_day == '2024-01-15'
            assert sj_id == 'NSB:ServiceJourney:1'
            assert isinstance(evj, EstimatedVehicleJourney)
            assert evj.line_ref == 'NSB:Line:R10'
            assert len(evj.estimated_calls) == 1
            # Second journey (cancelled)
            assert journeys[1][2].is_cancellation is True

    def test_et_reference_journeys(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/et', text=ET_RESPONSE)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('et')
            journeys = bridge.parse_et_journeys(root)
            refs = bridge.extract_reference_journeys(journeys)
            assert len(refs) == 2  # two distinct service journeys
            assert refs[0][1] == 'NSB:ServiceJourney:1'

    def test_fetch_returns_none_on_http_error(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/et', status_code=500)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('et')
            assert root is None


@pytest.mark.integration
class TestFetchAndParseVm:
    def test_fetch_vm_parses_journeys(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/vm', text=VM_RESPONSE)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('vm')
            assert root is not None
            journeys = bridge.parse_vm_journeys(root)
            assert len(journeys) == 1

    def test_vm_journey_fields(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/vm', text=VM_RESPONSE)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('vm')
            op_day, sj_id, mvj = bridge.parse_vm_journeys(root)[0]
            assert op_day == '2024-01-15'
            assert sj_id == 'NSB:ServiceJourney:1'
            assert isinstance(mvj, MonitoredVehicleJourney)
            assert mvj.latitude == pytest.approx(59.91)
            assert mvj.longitude == pytest.approx(10.75)
            assert mvj.delay_seconds == 180  # PT3M
            assert mvj.monitored is True


@pytest.mark.integration
class TestFetchAndParseSx:
    def test_fetch_sx_parses_situations(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/sx', text=SX_RESPONSE)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('sx')
            assert root is not None
            situations = bridge.parse_sx_situations(root)
            assert len(situations) == 1

    def test_sx_situation_fields(self):
        with requests_mock_module.Mocker() as m:
            m.get('https://api.entur.io/realtime/v1/rest/sx', text=SX_RESPONSE)
            bridge = EnturNorwayBridge()
            root = bridge.fetch_siri('sx')
            sit_num, sit = bridge.parse_sx_situations(root)[0]
            assert sit_num == 'ENT:SituationNumber:1'
            assert isinstance(sit, PtSituationElement)
            assert sit.summary == 'Track work on R10'
            assert len(sit.validity_periods) == 1
            assert sit.affects_line_refs == ['NSB:Line:R10']


@pytest.mark.integration
class TestMoreDataPagination:
    """Verify that _has_more_data correctly drives pagination."""

    def test_more_data_true(self):
        xml = f"""<Siri xmlns="{SIRI_NS}">
          <ServiceDelivery>
            <MoreData>true</MoreData>
          </ServiceDelivery>
        </Siri>"""
        from entur_norway.entur_norway import _has_more_data
        assert _has_more_data(ET.fromstring(xml)) is True

    def test_more_data_false(self):
        from entur_norway.entur_norway import _has_more_data
        assert _has_more_data(ET.fromstring(ET_RESPONSE)) is False

    def test_more_data_absent(self):
        xml = f'<Siri xmlns="{SIRI_NS}"><ServiceDelivery/></Siri>'
        from entur_norway.entur_norway import _has_more_data
        assert _has_more_data(ET.fromstring(xml)) is False

    def test_pagination_fetches_twice(self):
        """Bridge should keep fetching while MoreData is true."""
        page1 = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>true</MoreData>
    <EstimatedTimetableDelivery>
      <EstimatedJourneyVersionFrame>
        <EstimatedVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:A</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:R10</LineRef>
          <OperatorRef>NSB</OperatorRef>
        </EstimatedVehicleJourney>
      </EstimatedJourneyVersionFrame>
    </EstimatedTimetableDelivery>
  </ServiceDelivery>
</Siri>"""
        page2 = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>false</MoreData>
    <EstimatedTimetableDelivery>
      <EstimatedJourneyVersionFrame>
        <EstimatedVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:B</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:L1</LineRef>
          <OperatorRef>NSB</OperatorRef>
        </EstimatedVehicleJourney>
      </EstimatedJourneyVersionFrame>
    </EstimatedTimetableDelivery>
  </ServiceDelivery>
</Siri>"""
        with requests_mock_module.Mocker() as m:
            m.get(
                'https://api.entur.io/realtime/v1/rest/et',
                [{'text': page1}, {'text': page2}],
            )
            bridge = EnturNorwayBridge()
            # Simulate the pagination loop
            all_journeys = []
            req_id = None
            more = True
            while more:
                root = bridge.fetch_siri('et', req_id, 1000)
                assert root is not None
                more = __import__('entur_norway.entur_norway', fromlist=['_has_more_data'])._has_more_data(root)
                req_id = 'test-id'
                all_journeys.extend(bridge.parse_et_journeys(root))
            assert len(all_journeys) == 2
            ids = [j[1] for j in all_journeys]
            assert 'NSB:ServiceJourney:A' in ids
            assert 'NSB:ServiceJourney:B' in ids
