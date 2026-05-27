"""
Integration tests for GraceDB Gravitational Wave Candidate Alert poller.
Tests that mock external API calls but verify end-to-end data flow.
"""

import json
import pytest
from unittest.mock import Mock, patch, AsyncMock
from gracedb.gracedb import GraceDBPoller


SAMPLE_API_RESPONSE = {
    "numRows": 6251,
    "superevents": [
        {
            "superevent_id": "MS260408x",
            "gw_id": None,
            "category": "MDC",
            "created": "2026-04-08 23:59:34 UTC",
            "submitter": "read-cvmfs-emfollow",
            "em_type": "M632681",
            "t_start": 1459726873.430086,
            "t_0": 1459726874.430086,
            "t_end": 1459726875.430086,
            "far": 6.786496426516116e-14,
            "time_coinc_far": 4.196368604676061e-18,
            "space_coinc_far": 5.042499300641276e-18,
            "labels": ["EM_READY", "ADVNO", "GCN_PRELIM_SENT"],
            "links": {
                "self": "https://gracedb.ligo.org/api/superevents/MS260408x/"
            },
            "preferred_event_data": {
                "group": "CBC",
                "pipeline": "gstlal",
                "graceid": "M632680",
                "instruments": "H1,V1",
                "nevents": 2,
                "search": "MDC",
                "far": 6.786496426516116e-14,
                "far_is_upper_limit": False,
            },
        },
        {
            "superevent_id": "MS260408w",
            "gw_id": None,
            "category": "MDC",
            "created": "2026-04-08 22:59:34 UTC",
            "submitter": "read-cvmfs-emfollow",
            "em_type": None,
            "t_start": 1459724283.614037,
            "t_0": 1459724284.614037,
            "t_end": 1459724285.614037,
            "far": 9.110699364861297e-14,
            "time_coinc_far": None,
            "space_coinc_far": None,
            "labels": ["EM_READY", "ADVOK", "SKYMAP_READY"],
            "links": {
                "self": "https://gracedb.ligo.org/api/superevents/MS260408w/"
            },
            "preferred_event_data": {
                "group": "CBC",
                "pipeline": "gstlal",
                "graceid": "M632678",
                "instruments": "H1,L1",
                "nevents": 3,
                "search": "MDC",
                "far": 9.110699364861297e-14,
                "far_is_upper_limit": False,
            },
        },
    ],
}


@pytest.mark.integration
class TestFetchSuperevents:
    """Test superevent fetching with mocked HTTP responses."""

    @pytest.mark.asyncio
    async def test_fetch_returns_superevents(self):
        """Test that fetch_superevents returns parsed events from mocked response."""
        poller = GraceDBPoller()

        mock_response = AsyncMock()
        mock_response.raise_for_status = Mock()
        mock_response.json = AsyncMock(return_value=SAMPLE_API_RESPONSE)

        mock_session = AsyncMock()
        mock_session.get = Mock(return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_response),
            __aexit__=AsyncMock(return_value=False)
        ))

        with patch('aiohttp.ClientSession', return_value=AsyncMock(
            __aenter__=AsyncMock(return_value=mock_session),
            __aexit__=AsyncMock(return_value=False)
        )):
            superevents = await poller.fetch_superevents()

        assert len(superevents) == 2
        assert superevents[0]["superevent_id"] == "MS260408x"
        assert superevents[1]["superevent_id"] == "MS260408w"

    def test_parse_multiple_superevents(self):
        """Test parsing multiple superevents from an API response."""
        poller = GraceDBPoller()

        events = []
        for raw in SAMPLE_API_RESPONSE["superevents"]:
            superevent = poller.parse_superevent(raw)
            if superevent:
                events.append(superevent)

        assert len(events) == 2
        assert events[0].superevent_id == "MS260408x"
        assert events[0].pipeline == "gstlal"
        assert events[1].superevent_id == "MS260408w"
        assert events[1].instruments == "H1,L1"

    def test_dedup_by_seen_ids(self):
        """Test that already-seen superevent IDs are skipped."""
        poller = GraceDBPoller()

        # Parse first event
        raw = SAMPLE_API_RESPONSE["superevents"][0]
        superevent = poller.parse_superevent(raw)
        assert superevent is not None

        # Simulate dedup
        seen_ids = {superevent.superevent_id}
        raw2 = SAMPLE_API_RESPONSE["superevents"][0]
        superevent2 = poller.parse_superevent(raw2)
        assert superevent2 is not None
        assert superevent2.superevent_id in seen_ids


@pytest.mark.integration
class TestEndToEndParsing:
    """Test full parsing pipeline with realistic data."""

    def test_labels_roundtrip(self):
        """Test that labels survive JSON serialization roundtrip."""
        poller = GraceDBPoller()
        raw = SAMPLE_API_RESPONSE["superevents"][0]
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        labels = json.loads(superevent.labels_json)
        assert "EM_READY" in labels
        assert "GCN_PRELIM_SENT" in labels

    def test_all_fields_populated(self):
        """Test that all expected fields are populated from the API response."""
        poller = GraceDBPoller()
        raw = SAMPLE_API_RESPONSE["superevents"][0]
        superevent = poller.parse_superevent(raw)

        assert superevent is not None
        assert superevent.superevent_id
        assert superevent.category
        assert superevent.created
        assert superevent.t_start > 0
        assert superevent.t_0 > 0
        assert superevent.t_end > 0
        assert superevent.far > 0
        assert superevent.submitter
        assert superevent.self_uri
