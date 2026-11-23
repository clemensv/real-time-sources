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
    p.site_producer.producer.flush.return_value = 0
    p.timeseries_producer = MagicMock()
    p.timeseries_producer.producer.flush.return_value = 0
    p.values_producer = MagicMock()
    p.values_producer.producer = MagicMock()
    p.values_producer.producer.flush.return_value = 0
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


@pytest.mark.parametrize("failed_flush", [1, 2, None])
def test_one_record_series_is_confirmed_before_telemetry_and_checkpoint(poller, tmp_path, monkeypatch, failed_flush):
    from datetime import datetime, timezone

    monkeypatch.setenv("USGS_API_MODE", "legacy")
    poller.last_polled_file = str(tmp_path / "state.json")
    operations = []
    series_flushes = []

    async def records():
        yield [{
            "agency_cd": "USGS", "site_no": "99000001", "tz_cd": "UTC",
            "datetime": datetime.now(timezone.utc).isoformat(), "11111_00010": "2.125",
        }]

    def flush_series(timeout):
        series_flushes.append(timeout)
        operations.append("series-confirm")
        return 1 if len(series_flushes) == failed_flush else 0

    poller.timeseries_producer.producer.flush.side_effect = flush_series
    poller.timeseries_producer.send_usgs_sites_site_timeseries.side_effect = lambda **kwargs: operations.append("series-send")
    poller.values_producer.send_usgs_instantaneous_values_water_temperature.side_effect = lambda **kwargs: operations.append("telemetry-send")
    with patch.object(poller, "get_data_by_state", return_value=records()), \
         patch.object(poller, "get_sites_in_state", return_value=_empty_sites()), \
         patch.object(poller, "save_last_polled_times") as save:
        if failed_flush is not None:
            with pytest.raises(RuntimeError, match="checkpoint retained"):
                asyncio.run(poller.poll_and_send())
            save.assert_not_called()
            assert not (tmp_path / "state.json").exists()
        else:
            asyncio.run(poller.poll_and_send())
            save.assert_called_once()
    if failed_flush == 1:
        assert operations == ["series-send", "series-confirm"]
    else:
        assert operations == ["series-send", "series-confirm", "telemetry-send", "series-confirm"]
    assert all(timeout == 120 for timeout in series_flushes)


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
