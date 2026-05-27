"""Unit tests for the Defra AURN bridge."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import requests

from defra_aurn.defra_aurn import (
    DefraAURNAPI,
    convert_timestamp_ms_to_iso,
    create_retrying_session,
    parse_connection_string,
    refresh_reference_data,
)


class FakeResponse:
    """Minimal fake requests response."""

    def __init__(self, payload, status_code: int = 200):
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self.payload


class FakeSession:
    """Fake requests session that returns queued responses."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.headers = {}

    def get(self, url, params=None, timeout=None):
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        if not self.responses:
            raise AssertionError("No fake response queued")
        return self.responses.pop(0)


class FakeProducerWrapper:
    """Fake generated producer wrapper."""

    def __init__(self):
        self.sent = []
        self.producer = self
        self.flush_count = 0

    def send_uk_gov_defra_aurn_station(self, _station_id, data, flush_producer=False):
        self.sent.append(("station", _station_id, data, flush_producer))

    def send_uk_gov_defra_aurn_timeseries(self, _timeseries_id, data, flush_producer=False):
        self.sent.append(("timeseries", _timeseries_id, data, flush_producer))

    def send_uk_gov_defra_aurn_observation(self, _timeseries_id, data, flush_producer=False):
        self.sent.append(("observation", _timeseries_id, data, flush_producer))

    def flush(self):
        self.flush_count += 1


@pytest.mark.unit
class TestDefraAURNAPIInitialization:
    """Initialization tests."""

    def test_init_sets_defaults(self):
        api = DefraAURNAPI()
        assert api.base_url == "https://uk-air.defra.gov.uk/sos-ukair/api/v1"
        assert api.timeout == 30
        assert api.page_limit == 1000
        assert hasattr(api.session, "get")

    def test_create_retrying_session(self):
        session = create_retrying_session()
        https_adapter = session.get_adapter("https://uk-air.defra.gov.uk")

        assert session.headers["User-Agent"] == "GitHub-Copilot-CLI/1.0"
        assert https_adapter.max_retries.total == 3
        assert https_adapter.max_retries.backoff_factor == 1

    def test_refresh_reference_data_falls_back_to_existing_catalog(self):
        api = Mock()
        api.emit_reference_data.side_effect = requests.RequestException("timeout")

        catalog, refreshed = refresh_reference_data(api, Mock(), Mock(), {"ts-1": Mock()})

        assert refreshed is False
        assert "ts-1" in catalog

    def test_refresh_reference_data_raises_without_existing_catalog(self):
        api = Mock()
        api.emit_reference_data.side_effect = requests.RequestException("timeout")

        with pytest.raises(requests.RequestException):
            refresh_reference_data(api, Mock(), Mock(), {})


@pytest.mark.unit
class TestConnectionStringParsing:
    """Connection string parsing tests."""

    def test_parse_event_hubs_connection_string(self):
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=defra-aurn"
        )

        result = parse_connection_string(connection_string)

        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "defra-aurn"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == connection_string
        assert result["security.protocol"] == "SASL_SSL"
        assert result["sasl.mechanism"] == "PLAIN"

    def test_parse_bootstrap_connection_string(self):
        result = parse_connection_string("BootstrapServer=broker1:9092;EntityPath=defra-aurn")
        assert result["bootstrap.servers"] == "broker1:9092"
        assert result["kafka_topic"] == "defra-aurn"
        assert "sasl.username" not in result


@pytest.mark.unit
class TestTimestampConversion:
    """Timestamp helper tests."""

    def test_convert_timestamp_ms_to_iso(self):
        assert convert_timestamp_ms_to_iso(1743980400000) == "2025-04-06T23:00:00+00:00"


@pytest.mark.unit
class TestPaginationLogic:
    """Pagination tests."""

    def test_list_timeseries_uses_limit_and_offset_until_short_page(self):
        session = FakeSession(
            [
                FakeResponse([{"id": "1"}]),
            ]
        )
        api = DefraAURNAPI(session=session, page_limit=1000)

        result = api.list_timeseries()

        assert result == [{"id": "1"}]
        assert session.calls == [
            {
                "url": "https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries",
                "params": {"limit": 1000, "offset": 0},
                "timeout": 30,
            }
        ]

    def test_list_stations_fetches_multiple_pages(self):
        session = FakeSession(
            [
                FakeResponse([{"properties": {"id": 1}}, {"properties": {"id": 2}}]),
                FakeResponse([{"properties": {"id": 3}}]),
            ]
        )
        api = DefraAURNAPI(session=session, page_limit=2)

        result = api.list_stations()

        assert [item["properties"]["id"] for item in result] == [1, 2, 3]
        assert session.calls[0]["params"] == {"limit": 2, "offset": 0}
        assert session.calls[1]["params"] == {"limit": 2, "offset": 2}


@pytest.mark.unit
class TestObservationWindowSelection:
    """Observation polling window tests."""

    def test_get_timeseries_data_uses_default_two_hour_window(self):
        session = FakeSession([FakeResponse({"values": []})])
        api = DefraAURNAPI(session=session)

        api.get_timeseries_data("3", datetime(2025, 4, 8, 10, 0, tzinfo=timezone.utc))

        assert session.calls[0]["params"] == {"timespan": "PT2H/2025-04-08T10:00:00Z"}

    def test_emit_observations_uses_bootstrap_lookback_for_unseen_timeseries(self):
        session = FakeSession([FakeResponse({"values": []})])
        api = DefraAURNAPI(session=session)
        producer = FakeProducerWrapper()
        timeseries = api.normalize_timeseries(
            {
                "id": "3",
                "label": "NO2",
                "uom": "ug.m-3",
                "station": {
                    "properties": {"id": 804, "label": "Camden Kerbside-Nitrogen dioxide (air)"},
                    "geometry": {"coordinates": [51.544233, -0.175227999994221, "NaN"]},
                },
                "parameters": {
                    "phenomenon": {"id": "8", "label": "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8"},
                    "category": {"id": "8", "label": "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8"},
                },
            }
        )

        count = api.emit_observations(
            producer,
            {"3": timeseries},
            {},
            end_time=datetime(2025, 4, 8, 10, 0, tzinfo=timezone.utc),
        )

        assert count == 0
        assert session.calls[0]["params"] == {"timespan": "PT6H/2025-04-08T10:00:00Z"}
        assert producer.flush_count == 1


@pytest.mark.unit
class TestObservationDeduplication:
    """Observation de-duplication tests."""

    def test_emit_observations_skips_seen_values_and_keeps_new_ones(self):
        session = FakeSession(
            [
                FakeResponse(
                    {
                        "values": [
                            {"timestamp": 1743980400000, "value": 10.901},
                            {"timestamp": 1743984000000, "value": 9.371},
                        ]
                    }
                )
            ]
        )
        api = DefraAURNAPI(session=session)
        producer = FakeProducerWrapper()
        timeseries = api.normalize_timeseries(
            {
                "id": "3",
                "label": "NO2",
                "uom": "ug.m-3",
                "station": {
                    "properties": {"id": 804, "label": "Camden Kerbside-Nitrogen dioxide (air)"},
                    "geometry": {"coordinates": [51.544233, -0.175227999994221, "NaN"]},
                },
                "parameters": {
                    "phenomenon": {"id": "8", "label": "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8"},
                    "category": {"id": "8", "label": "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8"},
                },
            }
        )
        state = {"3": 1743980400000}

        count = api.emit_observations(
            producer,
            {"3": timeseries},
            state,
            end_time=datetime(2025, 4, 8, 10, 0, tzinfo=timezone.utc),
        )

        assert count == 1
        assert len(producer.sent) == 1
        event_kind, key, data, flush_producer = producer.sent[0]
        assert event_kind == "observation"
        assert key == "3"
        assert data.timestamp == "2025-04-07T00:00:00+00:00"
        assert data.value == pytest.approx(9.371)
        assert flush_producer is False
        assert state["3"] == 1743984000000
        assert producer.flush_count == 1
