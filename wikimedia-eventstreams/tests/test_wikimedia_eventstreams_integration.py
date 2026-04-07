"""Integration-style tests for stream consumption with mocked aiohttp objects."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from wikimedia_eventstreams.wikimedia_eventstreams import StateStore, WikimediaRecentChangeBridge
from tests.test_wikimedia_eventstreams_unit import SAMPLE_EVENT


class FakeContent:
    """Async iterator over byte lines."""

    def __init__(self, lines):
        self._lines = lines

    def __aiter__(self):
        self._iter = iter(self._lines)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration as exc:
            raise StopAsyncIteration from exc


class FakeResponse:
    """Minimal aiohttp response stub."""

    def __init__(self, lines):
        self.content = FakeContent(lines)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def raise_for_status(self):
        return None


class FakeSession:
    """Minimal aiohttp session stub."""

    def __init__(self, lines):
        self._lines = lines
        self.requested_urls = []

    def get(self, url):
        self.requested_urls.append(url)
        return FakeResponse(self._lines)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stream_once_reads_ndjson_and_updates_resume_state(tmp_path: Path) -> None:
    event_producer = MagicMock()
    kafka_producer = MagicMock()
    state_store = StateStore(str(tmp_path / "state.json"), dedupe_size=10)
    session = FakeSession([(json.dumps(SAMPLE_EVENT) + "\n").encode("utf-8")])

    with patch(
        "wikimedia_eventstreams.wikimedia_eventstreams.RecentChange.from_serializer_dict",
        side_effect=lambda payload: payload,
    ):
        bridge = WikimediaRecentChangeBridge(
            event_producer,
            kafka_producer,
            state_store=state_store,
            flush_interval=1,
            dedupe_size=10,
        )
        processed = await bridge._stream_once(session, max_events=1)

    assert processed == 1
    assert session.requested_urls == ["https://stream.wikimedia.org/v2/stream/recentchange"]
    event_producer.send_wikimedia_event_streams_recent_change.assert_called_once()
    loaded = state_store.load()
    assert loaded.since == SAMPLE_EVENT["meta"]["dt"]
    assert loaded.recent_event_ids == [SAMPLE_EVENT["meta"]["id"]]
