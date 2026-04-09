"""Unit tests for the nextbus bridge — no external network calls."""

import xml.etree.ElementTree as ET
from urllib.parse import parse_qs, urlparse
from unittest.mock import MagicMock, patch

import pytest

import nextbus.nextbus as nb

BASE_URL = "https://retro.umoiq.com/service/publicXMLFeed"

AGENCY_LIST_XML = b"""<?xml version="1.0" encoding="utf-8" ?>
<body>
  <agency tag="sf-muni" title="San Francisco Municipal Railway"/>
  <agency tag="portland-sc" title="Portland Streetcar"/>
</body>"""

ROUTE_LIST_XML = b"""<?xml version="1.0" encoding="utf-8" ?>
<body>
  <route tag="1" title="Route 1"/>
  <route tag="2" title="Route 2"/>
</body>"""

ROUTE_CONFIG_XML = b"""<?xml version="1.0" encoding="utf-8" ?>
<body>
  <route tag="1" title="Route 1">
    <stop tag="100" title="Stop A" lat="37.7749" lon="-122.4194"/>
  </route>
</body>"""

VEHICLE_LOCATIONS_XML = b"""<?xml version="1.0" encoding="utf-8" ?>
<body>
  <vehicle id="1234" routeTag="1" dirTag="1_OB0" lat="37.7749" lon="-122.4194"
           secsSinceReport="5" predictable="true" heading="270" speedKmHr="20"/>
  <lastTime time="1700000000000"/>
</body>"""


@pytest.fixture(autouse=True)
def reset_global_state():
    """Clear module-level checksum/state dicts so tests don't bleed into each other."""
    nb.route_checksums.clear()
    nb.schedule_checksums.clear()
    nb.messages_checksums.clear()
    nb.vehicle_last_report_times.clear()
    yield
    nb.route_checksums.clear()
    nb.schedule_checksums.clear()
    nb.messages_checksums.clear()
    nb.vehicle_last_report_times.clear()


# ---------------------------------------------------------------------------
# element_to_dict
# ---------------------------------------------------------------------------

class TestElementToDict:
    """element_to_dict converts an XML element tree to a plain Python dict."""

    def test_attributes_become_top_level_keys(self):
        elem = ET.fromstring('<route tag="1" title="Route 1"/>')
        result = nb.element_to_dict(elem)
        assert result["tag"] == "1"
        assert result["title"] == "Route 1"

    def test_child_with_attributes_becomes_nested_dict(self):
        elem = ET.fromstring(
            '<body><stop tag="100" title="Stop A" lat="37.7" lon="-122.4"/></body>'
        )
        result = nb.element_to_dict(elem)
        assert isinstance(result["stop"], dict)
        assert result["stop"]["tag"] == "100"
        assert result["stop"]["lat"] == "37.7"

    def test_child_with_text_only_becomes_string_value(self):
        elem = ET.fromstring("<body><note>Some text</note></body>")
        result = nb.element_to_dict(elem)
        assert result["note"] == "Some text"

    def test_repeated_child_tags_collapse_into_list(self):
        elem = ET.fromstring(
            "<body>"
            '<stop tag="100" title="A"/>'
            '<stop tag="101" title="B"/>'
            "</body>"
        )
        result = nb.element_to_dict(elem)
        assert isinstance(result["stop"], list)
        assert len(result["stop"]) == 2
        assert result["stop"][0]["tag"] == "100"
        assert result["stop"][1]["tag"] == "101"

    def test_empty_element_returns_empty_dict(self):
        elem = ET.fromstring("<body/>")
        assert nb.element_to_dict(elem) == {}

    def test_nested_children_are_recursed(self):
        elem = ET.fromstring(
            "<route tag='1'>"
            "  <direction tag='d1'><stop tag='100'/></direction>"
            "</route>"
        )
        result = nb.element_to_dict(elem)
        assert result["tag"] == "1"
        assert isinstance(result["direction"], dict)
        assert result["direction"]["tag"] == "d1"
        assert result["direction"]["stop"]["tag"] == "100"

    def test_child_attributes_and_parent_attributes_are_merged(self):
        # Sibling children of different tags each become their own key alongside
        # the parent's own attributes.
        elem = ET.fromstring(
            '<route tag="r1">'
            '  <direction tag="d1" name="Outbound"/>'
            "</route>"
        )
        result = nb.element_to_dict(elem)
        assert result["tag"] == "r1"
        assert result["direction"]["tag"] == "d1"
        assert result["direction"]["name"] == "Outbound"


# ---------------------------------------------------------------------------
# Print / list helpers
# ---------------------------------------------------------------------------

class TestPrintHelpers:
    """CLI listing functions (print_agencies, print_routes) hit the API and
    print results; they must handle 404 gracefully without raising."""

    def test_print_agencies_sends_correct_command(self, requests_mock):
        requests_mock.get(BASE_URL, content=AGENCY_LIST_XML)
        nb.print_agencies()
        qs = parse_qs(urlparse(requests_mock.last_request.url).query)
        assert qs["command"] == ["agencyList"]

    def test_print_agencies_404_returns_silently(self, requests_mock):
        requests_mock.get(BASE_URL, status_code=404)
        nb.print_agencies()  # must not raise

    def test_print_routes_sends_agency_tag(self, requests_mock):
        requests_mock.get(BASE_URL, content=ROUTE_LIST_XML)
        nb.print_routes("sf-muni")
        qs = parse_qs(urlparse(requests_mock.last_request.url).query)
        assert qs["command"] == ["routeList"]
        assert qs["a"] == ["sf-muni"]

    def test_print_routes_404_returns_silently(self, requests_mock):
        requests_mock.get(BASE_URL, status_code=404)
        nb.print_routes("sf-muni")  # must not raise


# ---------------------------------------------------------------------------
# poll_and_submit_route_config
# ---------------------------------------------------------------------------

def _make_route_api_handler(route_config_xml=ROUTE_CONFIG_XML):
    """Returns a requests-mock callback that dispatches by 'command' query param."""
    def handler(request, context):
        cmd = parse_qs(urlparse(request.url).query).get("command", [None])[0]
        if cmd == "routeList":
            return ROUTE_LIST_XML
        if cmd == "routeConfig":
            return route_config_xml
        context.status_code = 404
        return b""
    return handler


class TestPollAndSubmitRouteConfig:
    """poll_and_submit_route_config fetches routeList then routeConfig per route
    and calls producer.send_event for each new/changed route."""

    def test_sends_event_for_each_route(self, requests_mock):
        requests_mock.get(BASE_URL, content=_make_route_api_handler())
        producer = MagicMock()

        nb.poll_and_submit_route_config(producer, "sf-muni")

        assert producer.send_event.call_count == 2
        partition_keys = {c.kwargs["partition_key"] for c in producer.send_event.call_args_list}
        assert "route/sf-muni/1" in partition_keys
        assert "route/sf-muni/2" in partition_keys

    def test_event_data_carries_cloudevents_subject_property(self, requests_mock):
        requests_mock.get(BASE_URL, content=_make_route_api_handler())
        producer = MagicMock()

        nb.poll_and_submit_route_config(producer, "sf-muni")

        first_event_data = producer.send_event.call_args_list[0].args[0]
        assert "cloudEvents:subject" in first_event_data.properties
        assert "sf-muni" in first_event_data.properties["cloudEvents:subject"]

    def test_dedupe_skips_unchanged_content_on_second_call(self, requests_mock):
        requests_mock.get(BASE_URL, content=_make_route_api_handler())
        producer = MagicMock()

        nb.poll_and_submit_route_config(producer, "sf-muni")
        nb.poll_and_submit_route_config(producer, "sf-muni")

        # Both routes are seen once each — second poll is entirely deduped.
        assert producer.send_event.call_count == 2

    def test_404_on_route_list_returns_without_sending(self, requests_mock):
        requests_mock.get(BASE_URL, status_code=404)
        producer = MagicMock()

        nb.poll_and_submit_route_config(producer, "sf-muni")

        producer.send_event.assert_not_called()


# ---------------------------------------------------------------------------
# poll_and_submit_vehicle_locations
# ---------------------------------------------------------------------------

class TestPollAndSubmitVehicleLocations:
    """poll_and_submit_vehicle_locations creates an EventData batch, adds one
    entry per new vehicle position, and sends the batch."""

    def _make_producer(self):
        producer = MagicMock()
        mock_batch = MagicMock()
        mock_batch.__len__ = lambda self: 1
        producer.create_batch.return_value = mock_batch
        return producer, mock_batch

    def test_creates_batch_and_sends_it(self, requests_mock):
        requests_mock.get(BASE_URL, content=VEHICLE_LOCATIONS_XML)
        producer, mock_batch = self._make_producer()

        nb.poll_and_submit_vehicle_locations(producer, "sf-muni", "*", None)

        producer.create_batch.assert_called_once_with(partition_key="sf-muni")
        mock_batch.add.assert_called_once()
        producer.send_batch.assert_called_once_with(mock_batch)

    def test_returns_last_time_from_feed(self, requests_mock):
        requests_mock.get(BASE_URL, content=VEHICLE_LOCATIONS_XML)
        producer, _ = self._make_producer()

        result = nb.poll_and_submit_vehicle_locations(producer, "sf-muni", "*", None)

        assert result == 1700000000000.0

    def test_dedupe_skips_vehicle_already_seen_at_same_timestamp(self, requests_mock):
        requests_mock.get(BASE_URL, content=VEHICLE_LOCATIONS_XML)

        producer1, batch1 = self._make_producer()
        nb.poll_and_submit_vehicle_locations(producer1, "sf-muni", "*", None)
        first_add_count = batch1.add.call_count

        producer2, batch2 = self._make_producer()
        nb.poll_and_submit_vehicle_locations(producer2, "sf-muni", "*", None)

        assert first_add_count == 1   # vehicle was new on first call
        assert batch2.add.call_count == 0  # same timestamp — skipped on second call

    def test_404_returns_none(self, requests_mock):
        requests_mock.get(BASE_URL, status_code=404)
        producer, mock_batch = self._make_producer()

        result = nb.poll_and_submit_vehicle_locations(producer, "sf-muni", "*", None)

        assert result is None
        producer.send_batch.assert_not_called()
