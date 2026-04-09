"""
End-to-end test for GraceDB bridge.
Calls the real GraceDB API (no authentication needed).
"""

import pytest
from gracedb.gracedb import GraceDBPoller


@pytest.mark.e2e
class TestGraceDBLiveAPI:
    """Tests that call the real GraceDB public API."""

    @pytest.mark.asyncio
    async def test_fetch_live_superevents(self):
        """Fetch real superevents from the GraceDB public API."""
        poller = GraceDBPoller(poll_count=5, categories="Production,MDC,Test")
        raw_events = await poller.fetch_superevents(count=5)

        # GraceDB should always have at least some events (MDC are generated continuously)
        assert len(raw_events) > 0

        # Parse at least one
        parsed = []
        for raw in raw_events:
            superevent = poller.parse_superevent(raw)
            if superevent:
                parsed.append(superevent)

        assert len(parsed) > 0
        event = parsed[0]
        assert event.superevent_id
        assert event.category in ("Production", "MDC", "Test")
        assert event.t_0 > 0
        assert event.far >= 0
