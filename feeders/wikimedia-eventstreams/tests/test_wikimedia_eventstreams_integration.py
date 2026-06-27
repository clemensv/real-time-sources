"""Integration-style tests for stream consumption with mocked payload source."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from wikimedia_eventstreams.wikimedia_eventstreams import StateStore, WikimediaRecentChangeBridge
from tests.test_wikimedia_eventstreams_unit import SAMPLE_EVENT


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stream_once_reads_ndjson_and_updates_resume_state(tmp_path: Path) -> None:
    event_producer = MagicMock()
    kafka_producer = MagicMock()
    state_store = StateStore(str(tmp_path / "state.json"), dedupe_size=10)

    async def fake_payloads(**_kwargs):
        yield SAMPLE_EVENT

    with patch(
        "wikimedia_eventstreams.wikimedia_eventstreams.RecentChange.from_serializer_dict",
        side_effect=lambda payload: payload,
    ), patch("wikimedia_eventstreams.wikimedia_eventstreams.iter_recentchange_payloads", fake_payloads):
        bridge = WikimediaRecentChangeBridge(
            event_producer,
            kafka_producer,
            state_store=state_store,
            flush_interval=1,
            dedupe_size=10,
        )
        await bridge.run()

    event_producer.send_wikimedia_event_streams_recent_change.assert_called_once()
    loaded = state_store.load()
    assert loaded.since == SAMPLE_EVENT["meta"]["dt"]
    assert loaded.recent_event_ids == [SAMPLE_EVENT["meta"]["id"]]
