"""Tests for the --once single-cycle exit path used by Fabric notebook hosting."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gracedb.gracedb import GraceDBPoller


@pytest.fixture
def poller(tmp_path):
    """A GraceDBPoller wired with a mock producer and a tmp state file."""
    state_file = tmp_path / "seen.json"
    p = GraceDBPoller(
        kafka_config=None,
        kafka_topic="test-gracedb",
        last_polled_file=str(state_file),
        poll_count=5,
        categories="MDC",
    )
    p.event_producer = MagicMock()
    p.event_producer.producer = MagicMock()
    return p


def test_once_mode_exits_after_single_cycle(poller):
    """poll_and_send(once=True) must return after exactly one fetch."""
    fetch_calls = 0

    async def fake_fetch(count=None):  # noqa: D401, ARG001
        nonlocal fetch_calls
        fetch_calls += 1
        return []

    with patch.object(poller, "fetch_superevents", side_effect=fake_fetch):
        async def runner():
            await asyncio.wait_for(poller.poll_and_send(once=True), timeout=5)

        asyncio.run(runner())

    assert fetch_calls == 1, f"Expected exactly one upstream fetch, got {fetch_calls}"
    poller.event_producer.producer.flush.assert_called_once()


def test_once_flag_in_argparse():
    """`main()` argparse must expose a --once flag wired to ONCE_MODE env."""
    import argparse
    import inspect

    from gracedb import gracedb as mod

    source = inspect.getsource(mod.main)
    assert "--once" in source, "main() argparse must declare --once"
    assert "ONCE_MODE" in source, "--once default must honor ONCE_MODE env var"
