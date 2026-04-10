"""Unit tests for the Seattle Fire 911 bridge."""

from unittest.mock import Mock, patch

import pytest

from seattle_911.seattle_911 import (
    DATASET_URL,
    DEFAULT_CONNECT_TIMEOUT_SECONDS,
    DEFAULT_READ_TIMEOUT_SECONDS,
    SeattleFire911Bridge,
    parse_connection_string,
    parse_incident,
)


SAMPLE_ROWS = [
    {
        "address": "5130 40th Ave Ne",
        "type": "Aid Response",
        "datetime": "2026-04-09T03:52:00.000",
        "latitude": "47.666481",
        "longitude": "-122.284803",
        "incident_number": "F260046986",
    },
    {
        "address": "1401 2nd Ave",
        "type": "Medic Response- Overdose",
        "datetime": "2026-04-09T03:34:00.000",
        "latitude": "47.608292",
        "longitude": "-122.337995",
        "incident_number": "F260046981",
    },
]


@pytest.mark.unit
class TestConnectionStringParsing:
    def test_parse_event_hubs_connection_string(self):
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=seattle-911"
        )
        result = parse_connection_string(connection_string)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "seattle-911"
        assert result["sasl.username"] == "$ConnectionString"

    def test_parse_plain_kafka_connection_string(self):
        result = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=topic1")
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "topic1"


@pytest.mark.unit
class TestIncidentParsing:
    def test_parse_incident(self):
        incident = parse_incident(SAMPLE_ROWS[0])
        assert incident.incident_number == "F260046986"
        assert incident.incident_type == "Aid Response"
        assert incident.latitude == pytest.approx(47.666481)
        assert incident.longitude == pytest.approx(-122.284803)


@pytest.mark.unit
class TestFetchIncidents:
    def test_fetch_incidents_uses_soda_endpoint(self):
        bridge = SeattleFire911Bridge()
        response = Mock()
        response.json.side_effect = [SAMPLE_ROWS, []]
        response.raise_for_status.return_value = None
        bridge.session.get = Mock(return_value=response)

        incidents = bridge.fetch_incidents()

        assert len(incidents) == 2
        first_call = bridge.session.get.call_args_list[0]
        assert first_call.args[0] == DATASET_URL
        assert first_call.kwargs["params"]["$order"] == "datetime ASC"
        assert first_call.kwargs["timeout"] == (
            DEFAULT_CONNECT_TIMEOUT_SECONDS,
            DEFAULT_READ_TIMEOUT_SECONDS,
        )


@pytest.mark.unit
class TestPolling:
    @patch("seattle_911.seattle_911._save_state")
    def test_poll_and_send_deduplicates_by_incident_number(self, _mock_save_state):
        bridge = SeattleFire911Bridge(state_file="state.json")
        bridge.fetch_incidents = Mock(return_value=[parse_incident(row) for row in SAMPLE_ROWS])
        producer = Mock()
        producer.producer = Mock()
        producer.producer.flush.return_value = 0

        bridge.poll_and_send(producer, once=True)
        bridge.fetch_incidents = Mock(return_value=[parse_incident(row) for row in SAMPLE_ROWS])
        bridge.poll_and_send(producer, once=True)

        assert producer.send_us_wa_seattle_fire911_incident.call_count == 2
        producer.send_us_wa_seattle_fire911_incident.assert_any_call(
            "F260046986",
            parse_incident(SAMPLE_ROWS[0]),
            flush_producer=False,
        )

    @patch("seattle_911.seattle_911._save_state")
    def test_poll_and_send_updates_last_seen_datetime(self, _mock_save_state):
        bridge = SeattleFire911Bridge(state_file="state.json")
        bridge.fetch_incidents = Mock(return_value=[parse_incident(row) for row in SAMPLE_ROWS])
        producer = Mock()
        producer.producer = Mock()
        producer.producer.flush.return_value = 0

        bridge.poll_and_send(producer, once=True)

        assert bridge.last_seen_datetime == "2026-04-09T03:52:00.000"

    @patch("seattle_911.seattle_911._save_state")
    def test_poll_and_send_does_not_advance_state_on_flush_timeout(self, mock_save_state):
        bridge = SeattleFire911Bridge(state_file="state.json")
        bridge.fetch_incidents = Mock(return_value=[parse_incident(row) for row in SAMPLE_ROWS])
        producer = Mock()
        producer.producer = Mock()
        producer.producer.flush.return_value = 1

        bridge.poll_and_send(producer, once=True)

        assert bridge.last_seen_datetime is None
        assert bridge.sent_incident_numbers == set()
        assert bridge.sent_incident_order == []
        mock_save_state.assert_not_called()
        assert producer.send_us_wa_seattle_fire911_incident.call_count == 2
