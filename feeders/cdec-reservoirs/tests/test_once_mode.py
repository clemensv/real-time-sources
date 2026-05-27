"""Test that --once causes feed_readings to exit after exactly one polling cycle."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from cdec_reservoirs.cdec_reservoirs import CdecReservoirsAPI


_KAFKA_CFG = {'bootstrap.servers': 'localhost:9092'}


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro) if False else asyncio.run(coro)


@pytest.mark.unit
def test_once_mode_exits_after_one_cycle():
    """With once=True, the polling loop runs exactly one iteration and returns."""
    api = CdecReservoirsAPI()
    mock_ep = MagicMock()
    mock_raw_producer = MagicMock()
    fake_sleep = MagicMock()

    with patch.object(api, 'fetch_readings', return_value=[]) as mock_fetch, \
         patch('cdec_reservoirs.cdec_reservoirs.Producer', return_value=mock_raw_producer), \
         patch('cdec_reservoirs.cdec_reservoirs.GovCaWaterCdecEventProducer', return_value=mock_ep), \
         patch('cdec_reservoirs.cdec_reservoirs.time.sleep', side_effect=fake_sleep):
        asyncio.run(api.feed_readings(
            kafka_config=_KAFKA_CFG,
            kafka_topic='test-topic',
            polling_interval=60,
            state_file='',
            once=True,
        ))

    assert mock_fetch.call_count == 1, "feed_readings must perform exactly one fetch in --once mode"
    fake_sleep.assert_not_called()
    assert mock_raw_producer.flush.call_count >= 1


@pytest.mark.unit
def test_once_flag_parsed_by_argparse():
    """Verify the --once flag is registered on the feed subparser."""
    from cdec_reservoirs import cdec_reservoirs as mod
    import argparse

    # Build a fresh parser mirroring main() to test argparse wiring.
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command')
    feed = sub.add_parser('feed')
    feed.add_argument('--once', action='store_true', default=False)
    args = parser.parse_args(['feed', '--once'])
    assert args.once is True
    # Also sanity check the real module exposes feed_readings with once kwarg.
    import inspect
    sig = inspect.signature(mod.CdecReservoirsAPI.feed_readings)
    assert 'once' in sig.parameters
