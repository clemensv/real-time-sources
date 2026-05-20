"""Wiring tests: verify the bridge correctly calls the generated producers."""

import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, call, patch

import pytest

from entur_norway.entur_norway import EnturNorwayBridge
from entur_norway_producer_data import (
    DatedServiceJourney,
    EstimatedVehicleJourney,
    MonitoredVehicleJourney,
    PtSituationElement,
)

SIRI_NS = 'http://www.siri.org.uk/siri'

ET_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>false</MoreData>
    <EstimatedTimetableDelivery>
      <EstimatedJourneyVersionFrame>
        <EstimatedVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:10</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:R10</LineRef>
          <OperatorRef>NSB</OperatorRef>
        </EstimatedVehicleJourney>
      </EstimatedJourneyVersionFrame>
    </EstimatedTimetableDelivery>
  </ServiceDelivery>
</Siri>"""

VM_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>false</MoreData>
    <VehicleMonitoringDelivery>
      <VehicleActivity>
        <RecordedAtTime>2024-01-15T08:00:00Z</RecordedAtTime>
        <MonitoredVehicleJourney>
          <FramedVehicleJourneyRef>
            <DataFrameRef>2024-01-15</DataFrameRef>
            <DatedVehicleJourneyRef>NSB:ServiceJourney:10</DatedVehicleJourneyRef>
          </FramedVehicleJourneyRef>
          <LineRef>NSB:Line:R10</LineRef>
          <OperatorRef>NSB</OperatorRef>
          <Monitored>true</Monitored>
        </MonitoredVehicleJourney>
      </VehicleActivity>
    </VehicleMonitoringDelivery>
  </ServiceDelivery>
</Siri>"""

SX_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<Siri xmlns="{SIRI_NS}" version="2.0">
  <ServiceDelivery>
    <MoreData>false</MoreData>
    <SituationExchangeDelivery>
      <Situations>
        <PtSituationElement>
          <SituationNumber>ENT:SituationNumber:99</SituationNumber>
          <CreationTime>2024-01-15T07:00:00Z</CreationTime>
          <Progress>open</Progress>
          <Severity>normal</Severity>
        </PtSituationElement>
      </Situations>
    </SituationExchangeDelivery>
  </ServiceDelivery>
</Siri>"""


@pytest.mark.unit
class TestBridgeProducerWiring:
    """Verify that the bridge calls the correct producer methods with the right args."""

    def _make_bridge_with_mocked_fetch(self):
        bridge = EnturNorwayBridge.__new__(EnturNorwayBridge)
        call_count = {'et': 0, 'vm': 0, 'sx': 0}

        def fake_fetch(feed, requestor_id=None, max_size=1000):
            call_count[feed] += 1
            xmls = {'et': ET_XML, 'vm': VM_XML, 'sx': SX_XML}
            return ET.fromstring(xmls[feed])

        bridge.fetch_siri = fake_fetch
        return bridge, call_count

    def test_first_run_emits_reference_and_et_events(self):
        bridge, _ = self._make_bridge_with_mocked_fetch()
        mock_producer = MagicMock()
        journeys_ep = MagicMock()
        situations_ep = MagicMock()

        # Simulate one pass of the ET portion of the feed loop
        et_root = bridge.fetch_siri('et')
        et_journeys = bridge.parse_et_journeys(et_root)
        refs = bridge.extract_reference_journeys(et_journeys)

        assert len(refs) == 1
        assert refs[0][0] == '2024-01-15'
        assert refs[0][1] == 'NSB:ServiceJourney:10'
        assert isinstance(refs[0][2], DatedServiceJourney)

        # Verify the ET telemetry is also present
        assert len(et_journeys) == 1
        assert isinstance(et_journeys[0][2], EstimatedVehicleJourney)

    def test_vm_produces_monitored_vehicle_journey(self):
        bridge, _ = self._make_bridge_with_mocked_fetch()
        vm_root = bridge.fetch_siri('vm')
        vm_journeys = bridge.parse_vm_journeys(vm_root)
        assert len(vm_journeys) == 1
        op_day, sj_id, mvj = vm_journeys[0]
        assert op_day == '2024-01-15'
        assert sj_id == 'NSB:ServiceJourney:10'
        assert isinstance(mvj, MonitoredVehicleJourney)
        assert mvj.monitored is True

    def test_sx_produces_pt_situation_element(self):
        bridge, _ = self._make_bridge_with_mocked_fetch()
        sx_root = bridge.fetch_siri('sx')
        situations = bridge.parse_sx_situations(sx_root)
        assert len(situations) == 1
        sit_num, sit = situations[0]
        assert sit_num == 'ENT:SituationNumber:99'
        assert isinstance(sit, PtSituationElement)

    def test_feed_calls_producer_methods(self):
        """Verify the full feed() wiring calls the correct producer send methods."""
        bridge, _ = self._make_bridge_with_mocked_fetch()

        mock_producer = MagicMock()
        journeys_ep = MagicMock()
        situations_ep = MagicMock()

        # Patch the Producer constructor and the event producers
        # Use a long polling_interval so time.sleep is always called after the
        # first iteration, letting KeyboardInterrupt stop the loop cleanly.
        with patch('entur_norway.entur_norway.Producer', return_value=mock_producer), \
             patch(
                 'entur_norway.entur_norway.NoEnturJourneysEventProducer',
                 return_value=journeys_ep,
             ), \
             patch(
                 'entur_norway.entur_norway.NoEnturSituationsEventProducer',
                 return_value=situations_ep,
             ), \
             patch('time.sleep', side_effect=KeyboardInterrupt), \
             patch('time.monotonic', side_effect=[0.0, 0.0]):

            try:
                bridge.feed(
                    kafka_config={'bootstrap.servers': 'localhost:9092'},
                    kafka_topic='test-topic',
                    polling_interval=60,
                )
            except KeyboardInterrupt:
                pass

        # On first run: reference (DatedServiceJourney) + ET telemetry + VM + SX
        dsj_calls = journeys_ep.send_no_entur_dated_service_journey.call_args_list
        et_calls = journeys_ep.send_no_entur_estimated_vehicle_journey.call_args_list
        vm_calls = journeys_ep.send_no_entur_monitored_vehicle_journey.call_args_list
        sx_calls = situations_ep.send_no_entur_pt_situation_element.call_args_list

        assert len(dsj_calls) == 1
        assert dsj_calls[0].kwargs['_operating_day'] == '2024-01-15'
        assert dsj_calls[0].kwargs['_service_journey_id'] == 'NSB:ServiceJourney:10'
        assert isinstance(dsj_calls[0].kwargs['data'], DatedServiceJourney)
        assert dsj_calls[0].kwargs['flush_producer'] is False

        assert len(et_calls) == 1
        assert et_calls[0].kwargs['_operating_day'] == '2024-01-15'
        assert et_calls[0].kwargs['flush_producer'] is False

        assert len(vm_calls) == 1
        assert vm_calls[0].kwargs['_operating_day'] == '2024-01-15'
        assert vm_calls[0].kwargs['flush_producer'] is False

        assert len(sx_calls) == 1
        assert sx_calls[0].kwargs['_situation_number'] == 'ENT:SituationNumber:99'
        assert sx_calls[0].kwargs['flush_producer'] is False

        # Producer.flush() should be called at each boundary
        assert mock_producer.flush.call_count >= 3
