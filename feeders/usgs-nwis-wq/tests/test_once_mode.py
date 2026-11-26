"""Test that the --once flag causes the bridge to exit after one polling cycle."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from usgs_nwis_wq.usgs_nwis_wq import USGSWaterQualityPoller


@pytest.mark.asyncio
async def test_once_mode_exits_after_one_cycle():
    """poll_and_send(once=True) must return after exactly one cycle, not loop."""
    poller = USGSWaterQualityPoller(
        kafka_config={'bootstrap.servers': 'unused:9092'},
        kafka_topic='test',
        last_polled_file='',
        states=['DC'],
        sites=None,
        parameter_codes=None,
    )

    # Stub out HTTP + Kafka I/O so the cycle is a pure no-op.
    poller.load_last_polled_times = MagicMock(return_value={})
    poller.save_last_polled_times = MagicMock()
    poller.fetch_json = AsyncMock(return_value=None)
    poller.site_producer = None
    poller.readings_producer = None

    sleep_mock = AsyncMock()
    with patch('asyncio.sleep', sleep_mock):
        await asyncio.wait_for(poller.poll_and_send(once=True), timeout=5.0)

    # If --once worked, asyncio.sleep(300) at end of loop was skipped.
    assert sleep_mock.await_count == 0, (
        "poll_and_send(once=True) should exit before the inter-cycle sleep"
    )


def test_legacy_checkpoint_routes_reads_and_writes_to_keyless_rest(monkeypatch, tmp_path):
    from unittest.mock import Mock
    from usgs_waterdata_core import azure_files, state
    from usgs_nwis_wq.usgs_nwis_wq import USGSWaterQualityPoller

    path = str(tmp_path / "legacy.json")
    poller = USGSWaterQualityPoller(last_polled_file=path)
    monkeypatch.setenv("STATE_BACKEND", "azure-files-rest")
    read = Mock(return_value={"01646500/00010": "2026-11-25T12:00:00+00:00"})
    write = Mock()
    monkeypatch.setattr(azure_files, "read_json", read)
    monkeypatch.setattr(state, "write_json", write)
    loaded = poller.load_last_polled_times()
    poller.save_last_polled_times(loaded)
    assert str(read.call_args.args[0]) == path
    assert str(write.call_args.args[0]) == path
    assert write.call_args.args[1] == read.return_value
