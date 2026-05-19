"""Unit tests for the --once / ONCE_MODE single-cycle exit added for Fabric
notebook hosting. Asserts that ``poll_and_send`` returns after exactly one
polling cycle when ``once=True`` and that the ``--once`` CLI flag wires
through correctly."""

import asyncio
import sys
from unittest.mock import MagicMock, patch

import pytest

from usgs_iv.usgs_iv import USGSDataPoller, main


async def _empty_records():
    if False:
        yield  # pragma: no cover - generator stub


async def _empty_sites():
    if False:
        yield  # pragma: no cover - generator stub


@pytest.fixture
def poller():
    p = USGSDataPoller(state='NY', once=True)
    p.site_producer = MagicMock()
    p.site_producer.producer = MagicMock()
    p.values_producer = MagicMock()
    p.values_producer.producer = MagicMock()
    p.last_polled_file = None
    return p


def test_once_mode_exits_after_one_cycle(poller, tmp_path):
    """With once=True, poll_and_send must return after a single cycle (no sleep, no infinite loop)."""
    poller.last_polled_file = str(tmp_path / 'state.json')

    with patch.object(poller, 'get_data_by_state', return_value=_empty_records()), \
         patch.object(poller, 'get_sites_in_state', return_value=_empty_sites()), \
         patch('usgs_iv.usgs_iv.asyncio.sleep') as mock_sleep:
        # If --once is honored, asyncio.sleep MUST NOT be called and the
        # coroutine must complete in well under the poll interval.
        asyncio.run(asyncio.wait_for(poller.poll_and_send(), timeout=10))
        assert mock_sleep.await_count == 0, "asyncio.sleep called - bridge did not exit after one cycle"


def test_once_flag_is_parsed_from_cli():
    """`usgs-iv feed --once` must set args.once=True and propagate it to the poller."""
    captured = {}

    class _StopAfterInit(Exception):
        pass

    def _fake_poller_init(self, **kwargs):
        captured.update(kwargs)
        raise _StopAfterInit()

    argv_backup = sys.argv
    try:
        sys.argv = ['usgs-iv', 'feed', '--connection-string',
                    'BootstrapServer=localhost:9092;EntityPath=t', '--once']
        with patch.object(USGSDataPoller, '__init__', _fake_poller_init), \
             pytest.raises(_StopAfterInit):
            main()
    finally:
        sys.argv = argv_backup

    assert captured.get('once') is True


def test_once_flag_defaults_false_from_env(monkeypatch):
    """Absence of --once and ONCE_MODE env must yield once=False (preserves long-running default)."""
    monkeypatch.delenv('ONCE_MODE', raising=False)
    captured = {}

    class _StopAfterInit(Exception):
        pass

    def _fake_poller_init(self, **kwargs):
        captured.update(kwargs)
        raise _StopAfterInit()

    argv_backup = sys.argv
    try:
        sys.argv = ['usgs-iv', 'feed', '--connection-string',
                    'BootstrapServer=localhost:9092;EntityPath=t']
        with patch.object(USGSDataPoller, '__init__', _fake_poller_init), \
             pytest.raises(_StopAfterInit):
            main()
    finally:
        sys.argv = argv_backup

    assert captured.get('once') is False
