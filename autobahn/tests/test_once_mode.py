"""Tests for the --once single-cycle mode used by the Fabric notebook host."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.modules.pop("autobahn", None)

from autobahn.autobahn import AutobahnPoller


def test_poll_and_send_once_runs_single_cycle(tmp_path):
    state_file = tmp_path / "state.json"
    poller = AutobahnPoller(
        kafka_config=None,
        kafka_topic="test-autobahn",
        state_file=str(state_file),
        poll_interval_seconds=900,
        resources=("roadworks",),
        roads=["A1"],
        request_concurrency=1,
    )

    poll_once_mock = AsyncMock(return_value={"roadworks": {"appeared": 0, "updated": 0, "resolved": 0}})
    sleep_mock = AsyncMock()

    with patch.object(poller, "poll_once", poll_once_mock), \
         patch("autobahn.autobahn.asyncio.sleep", sleep_mock):
        asyncio.run(poller.poll_and_send(once=True))

    assert poll_once_mock.await_count == 1
    assert sleep_mock.await_count == 0
