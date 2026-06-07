"""Tests for the --once single-cycle exit path used by Fabric notebook hosting."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gracedb.gracedb import GraceDBPoller, SAMPLE_SUPEREVENTS, created_to_rfc3339


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


def test_mock_mode_returns_canned_superevents(tmp_path, monkeypatch):
    """GRACEDB_MOCK makes fetch_superevents return the deterministic corpus."""
    monkeypatch.setenv("GRACEDB_MOCK", "true")
    p = GraceDBPoller(last_polled_file=str(tmp_path / "seen.json"), categories="Production,MDC")
    assert p.mock is True

    raw = asyncio.run(p.fetch_superevents())
    assert len(raw) == len(SAMPLE_SUPEREVENTS) >= 1

    parsed = [p.parse_superevent(r) for r in raw]
    assert all(se is not None for se in parsed)
    assert parsed[0].superevent_id == "MS240101a"
    assert parsed[0].category == "Production"
    assert parsed[0].group == "CBC"


def test_mock_mode_forces_single_cycle(tmp_path, monkeypatch):
    """In mock mode poll_and_send exits after one cycle even without --once."""
    monkeypatch.setenv("GRACEDB_MOCK", "true")
    p = GraceDBPoller(last_polled_file=str(tmp_path / "seen.json"), categories="Production,MDC")
    p.event_producer = MagicMock()
    p.event_producer.producer = MagicMock()

    async def runner():
        await asyncio.wait_for(p.poll_and_send(once=False), timeout=5)

    asyncio.run(runner())
    # One Superevent emitted from the canned corpus, then exit.
    assert p.event_producer.send_org_ligo_gracedb_superevent.call_count == 1


def test_created_to_rfc3339_parses_gracedb_format():
    """GraceDB's 'YYYY-MM-DD HH:MM:SS UTC' must become Z-suffixed RFC 3339."""
    assert created_to_rfc3339("2024-01-01 00:00:00 UTC") == "2024-01-01T00:00:00Z"
    assert created_to_rfc3339("2024-06-15T12:30:45") == "2024-06-15T12:30:45Z"


def test_created_to_rfc3339_falls_back_on_bad_input():
    """Unparseable/empty input yields a valid RFC 3339 'now' rather than crashing."""
    import re
    pat = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
    assert pat.match(created_to_rfc3339(""))
    assert pat.match(created_to_rfc3339("not a date"))
    assert pat.match(created_to_rfc3339(None))


