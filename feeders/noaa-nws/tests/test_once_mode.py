"""Tests for --once mode in the NOAA NWS bridge.

Verifies that `poll_and_send(once=True)` runs exactly one polling cycle
and exits without sleeping or re-entering the loop. Used by the Fabric
notebook hosting path which schedules single-cycle execution.
"""

import time as _time
from unittest.mock import MagicMock, patch

import pytest

from noaa_nws.noaa_nws import NWSAlertPoller


@pytest.fixture
def mock_kafka_config():
    return {'bootstrap.servers': 'localhost:9092'}


def _make_poller(mock_kafka_config, tmp_path):
    state_file = str(tmp_path / 'state.json')
    with patch('confluent_kafka.Producer') as mock_producer_class:
        mock_producer_class.return_value = MagicMock()
        poller = NWSAlertPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=state_file,
        )
    poller.alerts_producer = MagicMock()
    poller.zones_producer = MagicMock()
    poller.observations_producer = MagicMock()
    poller.kafka_producer = MagicMock()
    return poller


def test_once_mode_runs_one_cycle_and_exits(mock_kafka_config, tmp_path):
    poller = _make_poller(mock_kafka_config, tmp_path)

    with patch.object(poller, 'fetch_zones', return_value=[]) as mock_zones, \
         patch.object(poller, 'fetch_observation_stations', return_value=[]) as mock_stations, \
         patch.object(poller, 'poll_alerts', return_value=[]) as mock_poll, \
         patch.object(_time, 'sleep') as mock_sleep:
        poller.poll_and_send(once=True)

    mock_zones.assert_called_once()
    mock_stations.assert_called_once()
    assert mock_poll.call_count == 1, "poll_alerts must be called exactly once in --once mode"
    mock_sleep.assert_not_called(), "time.sleep must not be called in --once mode"


def test_default_mode_does_not_break_after_one_cycle(mock_kafka_config, tmp_path):
    """Without once=True the loop must continue (we break it via sleep raising)."""
    poller = _make_poller(mock_kafka_config, tmp_path)

    call_log = {'count': 0}

    def _raise_after_first_sleep(*_args, **_kwargs):
        call_log['count'] += 1
        raise KeyboardInterrupt("stop loop for test")

    with patch.object(poller, 'fetch_zones', return_value=[]), \
         patch.object(poller, 'fetch_observation_stations', return_value=[]), \
         patch.object(poller, 'poll_alerts', return_value=[]), \
         patch.object(_time, 'sleep', side_effect=_raise_after_first_sleep):
        with pytest.raises(KeyboardInterrupt):
            poller.poll_and_send(once=False)

    assert call_log['count'] == 1, "default mode must reach time.sleep after one iteration"
