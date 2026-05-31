"""
Integration tests for the NASA FIRMS active-fire poller.
Mocks the FIRMS HTTP layer but exercises the full fetch -> parse -> send flow.
"""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest

from nasa_firms.nasa_firms import FirmsPoller, InstrumentEnum


VIIRS_CSV = (
    "latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,"
    "instrument,confidence,version,bright_ti5,frp,daynight\n"
    "-12.345,34.567,330.1,0.45,0.39,2024-01-15,112,N,VIIRS,n,2.0NRT,295.0,12.7,D\n"
    "10.000,20.000,350.0,0.5,0.4,2024-01-15,113,N,VIIRS,h,2.0NRT,300.0,55.0,D\n"
)

AVAILABILITY_CSV = (
    "data_id,min_date,max_date\n"
    "VIIRS_SNPP_NRT,2024-01-01,2024-01-15\n"
    "MODIS_NRT,2024-01-01,2024-01-15\n"
)


@pytest.mark.integration
class TestFetchDetections:
    @pytest.mark.asyncio
    async def test_fetch_parses_rows(self):
        poller = FirmsPoller(map_key='k', sources=['VIIRS_SNPP_NRT'])
        poller._fetch_text = AsyncMock(return_value=VIIRS_CSV)
        detections = await poller.fetch_detections(Mock(), 'VIIRS_SNPP_NRT')
        assert len(detections) == 2
        assert all(d.instrument == InstrumentEnum.VIIRS for d in detections)
        assert {d.confidence_level.value for d in detections} == {'nominal', 'high'}

    @pytest.mark.asyncio
    async def test_fetch_handles_error_body(self):
        poller = FirmsPoller(map_key='k', sources=['VIIRS_SNPP_NRT'])
        poller._fetch_text = AsyncMock(return_value="Invalid MAP_KEY.")
        detections = await poller.fetch_detections(Mock(), 'VIIRS_SNPP_NRT')
        assert detections == []


@pytest.mark.integration
class TestFetchAvailability:
    @pytest.mark.asyncio
    async def test_fetch_filters_to_configured_sources(self):
        poller = FirmsPoller(map_key='k', sources=['VIIRS_SNPP_NRT'])
        poller._fetch_text = AsyncMock(return_value=AVAILABILITY_CSV)
        records = await poller.fetch_availability(Mock())
        assert len(records) == 1
        rec = records[0]
        assert rec.source == 'VIIRS_SNPP_NRT'
        assert rec.record_id == 'coverage'
        assert rec.min_date == '2024-01-01'
        assert rec.instrument == InstrumentEnum.VIIRS


@pytest.mark.integration
class TestPollAndSend:
    @pytest.mark.asyncio
    async def test_emits_reference_then_detections_with_dedupe(self):
        event_producer = Mock()
        event_producer.producer = Mock()
        event_producer.producer.flush = Mock(return_value=None)

        poller = FirmsPoller(map_key='k', sources=['VIIRS_SNPP_NRT'],
                             event_producer=event_producer)
        poller._fetch_text = AsyncMock(side_effect=[
            AVAILABILITY_CSV,  # availability fetch
            VIIRS_CSV,         # detection fetch
        ])

        await poller.poll_and_send(once=True)

        assert event_producer.send_nasa_firms_data_availability.call_count == 1
        assert event_producer.send_nasa_firms_fire_detection.call_count == 2
        # Reference must be sent before any detection.
        names = [c[0] for c in event_producer.method_calls]
        first_av = names.index('send_nasa_firms_data_availability')
        first_det = names.index('send_nasa_firms_fire_detection')
        assert first_av < first_det

    @pytest.mark.asyncio
    async def test_seen_state_suppresses_duplicates(self, tmp_path):
        state = tmp_path / "seen.json"
        event_producer = Mock()
        event_producer.producer = Mock()
        event_producer.producer.flush = Mock(return_value=None)

        poller = FirmsPoller(map_key='k', sources=['VIIRS_SNPP_NRT'],
                             event_producer=event_producer,
                             last_polled_file=str(state))
        poller._fetch_text = AsyncMock(side_effect=[AVAILABILITY_CSV, VIIRS_CSV])
        await poller.poll_and_send(once=True)
        assert event_producer.send_nasa_firms_fire_detection.call_count == 2

        # Second cycle with identical data emits no new detections.
        event_producer.send_nasa_firms_fire_detection.reset_mock()
        poller._fetch_text = AsyncMock(side_effect=[AVAILABILITY_CSV, VIIRS_CSV])
        await poller.poll_and_send(once=True)
        assert event_producer.send_nasa_firms_fire_detection.call_count == 0
