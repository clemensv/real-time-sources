"""Tests for --once mode in the NASA FIRMS bridge."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from nasa_firms.nasa_firms import FirmsPoller


VIIRS_CSV = (
    "latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,"
    "instrument,confidence,version,bright_ti5,frp,daynight\n"
    "-12.345,34.567,330.1,0.45,0.39,2024-01-15,112,N,VIIRS,n,2.0NRT,295.0,12.7,D\n"
)
AVAILABILITY_CSV = "data_id,min_date,max_date\nVIIRS_SNPP_NRT,2024-01-01,2024-01-15\n"


@patch('nasa_firms.nasa_firms.NASAFIRMSEventProducer')
@patch('nasa_firms.nasa_firms.Producer')
def test_once_mode_exits_after_one_cycle(mock_producer_class, mock_event_producer_class):
    """poll_and_send(once=True) must return after a single fetch cycle."""
    mock_producer_class.return_value = Mock()
    mock_event_producer = Mock()
    mock_event_producer.producer = Mock()
    mock_event_producer.producer.flush = Mock(return_value=None)
    mock_event_producer_class.return_value = mock_event_producer

    poller = FirmsPoller(
        map_key='k',
        kafka_config={'bootstrap.servers': 'localhost:9092'},
        kafka_topic='test-topic',
        sources=['VIIRS_SNPP_NRT'],
        last_polled_file=None,
    )
    poller._fetch_text = AsyncMock(side_effect=[AVAILABILITY_CSV, VIIRS_CSV])

    import asyncio
    # Must complete promptly; --once must not enter the sleep loop.
    asyncio.run(asyncio.wait_for(poller.poll_and_send(once=True), timeout=10))

    assert mock_event_producer.send_nasa_firms_fire_detection.call_count == 1
    assert mock_event_producer.producer.flush.called
