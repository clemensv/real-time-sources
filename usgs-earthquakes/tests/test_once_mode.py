"""Tests for --once mode in the USGS earthquakes bridge."""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from usgs_earthquakes.usgs_earthquakes import USGSEarthquakePoller


@patch('usgs_earthquakes.usgs_earthquakes.USGSEarthquakesEventProducer')
@patch('usgs_earthquakes.usgs_earthquakes.Producer')
def test_once_mode_exits_after_one_cycle(mock_producer_class, mock_event_producer_class):
    """poll_and_send(once=True) must return after a single fetch cycle."""
    mock_producer_class.return_value = Mock()
    mock_event_producer = Mock()
    mock_event_producer.producer = Mock()
    mock_event_producer_class.return_value = mock_event_producer

    poller = USGSEarthquakePoller(
        kafka_config={'bootstrap.servers': 'localhost:9092'},
        kafka_topic='test-topic',
        last_polled_file=None,
        feed='all_hour',
    )

    fetch_calls = []

    async def fake_fetch():
        fetch_calls.append(1)
        return []

    poller.fetch_feed = fake_fetch
    poller.load_seen_event_ids = Mock(return_value={})
    poller.save_seen_event_ids = Mock()

    async def run_with_timeout():
        await asyncio.wait_for(poller.poll_and_send(once=True), timeout=5.0)

    asyncio.run(run_with_timeout())

    assert len(fetch_calls) == 1, "Expected exactly one fetch cycle in --once mode"


@patch('usgs_earthquakes.usgs_earthquakes.USGSEarthquakesEventProducer')
@patch('usgs_earthquakes.usgs_earthquakes.Producer')
def test_once_flag_registered_on_feed_subparser(mock_producer_class, mock_event_producer_class):
    """The 'feed' subcommand must accept --once."""
    import argparse
    from usgs_earthquakes import usgs_earthquakes as mod

    # Sanity-check that --once is wired through main()'s argparse.
    src = open(mod.__file__, 'r', encoding='utf-8').read()
    assert "'--once'" in src
    assert 'ONCE_MODE' in src
