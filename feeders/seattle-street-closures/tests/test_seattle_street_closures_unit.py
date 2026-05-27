"""Unit tests for the Seattle street closures bridge."""

from unittest.mock import Mock, patch

import pytest

from seattle_street_closures.seattle_street_closures import (
    DATASET_URL,
    DEFAULT_CONNECT_TIMEOUT_SECONDS,
    DEFAULT_READ_TIMEOUT_SECONDS,
    SeattleStreetClosuresBridge,
    build_closure_id,
    normalize_date,
    parse_closure,
)


SAMPLE_ROWS = [
    {
        "permit_number": "SUFUN0006110",
        "permit_type": "Play Street",
        "project_name": "Play Street | 3/27/26-9/30/26 Fri & Wed | N 81ST ST b/t FREMONT AVE N & LINDEN AVE N",
        "project_description": "Play Street on 81st Street between Linden Ave N and Fremont Ave N.",
        "start_date": "2026-04-01T00:00:00.000",
        "end_date": "2026-09-30T00:00:00.000",
        "wednesday": "5PM-9PM",
        "friday": "5PM-9PM",
        "street_on": "N 81ST ST",
        "street_from": "FREMONT AVE N",
        "street_to": "LINDEN AVE N",
        "segkey": "15915",
        "line_string": {
            "type": "LineString",
            "coordinates": [[-122.3499, 47.6876], [-122.3472, 47.6876]],
        },
    }
]


@pytest.mark.unit
class TestHelpers:
    def test_normalize_date(self):
        assert normalize_date("2026-04-01T00:00:00.000") == "2026-04-01"

    def test_build_closure_id(self):
        assert build_closure_id(SAMPLE_ROWS[0]) == "SUFUN0006110|15915|2026-04-01|2026-09-30"

    def test_parse_closure(self):
        closure = parse_closure(SAMPLE_ROWS[0])
        assert closure.closure_id == "SUFUN0006110|15915|2026-04-01|2026-09-30"
        assert closure.geometry_json is not None
        assert closure.permit_type == "Play Street"


@pytest.mark.unit
class TestFetchClosures:
    def test_fetch_closures_uses_soda_endpoint(self):
        bridge = SeattleStreetClosuresBridge()
        response = Mock()
        response.json.side_effect = [SAMPLE_ROWS, []]
        response.raise_for_status.return_value = None
        bridge.session.get = Mock(return_value=response)

        closures = bridge.fetch_closures()

        assert len(closures) == 1
        first_call = bridge.session.get.call_args_list[0]
        assert first_call.args[0] == DATASET_URL
        assert first_call.kwargs["params"]["$order"] == "permit_number ASC"
        assert first_call.kwargs["timeout"] == (
            DEFAULT_CONNECT_TIMEOUT_SECONDS,
            DEFAULT_READ_TIMEOUT_SECONDS,
        )


@pytest.mark.unit
class TestPolling:
    @patch("seattle_street_closures.seattle_street_closures._save_state")
    def test_poll_and_send_only_emits_changed_rows(self, _mock_save_state):
        bridge = SeattleStreetClosuresBridge(state_file="state.json")
        bridge.fetch_closures = Mock(return_value=[parse_closure(SAMPLE_ROWS[0])])
        producer = Mock()
        producer.producer = Mock()
        producer.producer.flush.return_value = 0

        bridge.poll_and_send(producer, once=True)
        bridge.poll_and_send(producer, once=True)

        assert producer.send_us_wa_seattle_street_closures_street_closure.call_count == 1

    @patch("seattle_street_closures.seattle_street_closures._save_state")
    def test_poll_and_send_does_not_advance_state_on_flush_timeout(self, mock_save_state):
        bridge = SeattleStreetClosuresBridge(state_file="state.json")
        closure = parse_closure(SAMPLE_ROWS[0])
        bridge.fetch_closures = Mock(return_value=[closure])
        producer = Mock()
        producer.producer = Mock()
        producer.producer.flush.return_value = 1

        bridge.poll_and_send(producer, once=True)

        assert bridge.previous_digests == {}
        mock_save_state.assert_not_called()
        assert producer.send_us_wa_seattle_street_closures_street_closure.call_count == 1
