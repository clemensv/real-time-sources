"""Integration tests for the UBA AirData bridge with mocked HTTP responses."""

from unittest.mock import patch

import pytest
import requests_mock

from uba_airdata.uba_airdata import (
    UBAAirDataAPI,
    feed_measures,
    send_reference_data,
)

from tests.test_uba_airdata_unit import COMPONENTS_PAYLOAD, MEASURES_PAYLOAD, STATIONS_PAYLOAD


@pytest.mark.integration
class TestAPIRequests:
    """Test mocked API requests."""

    def test_fetch_payloads(self):
        api = UBAAirDataAPI()
        with requests_mock.Mocker() as mocker:
            mocker.get("https://www.umweltbundesamt.de/api/air_data/v3/stations/json", json=STATIONS_PAYLOAD)
            mocker.get("https://www.umweltbundesamt.de/api/air_data/v3/components/json", json=COMPONENTS_PAYLOAD)
            stations_payload = api.get_stations_payload()
            components_payload = api.get_components_payload()
            assert "data" in stations_payload
            assert stations_payload["data"]["21"][1] == "DEBE021"
            assert components_payload["5"][1] == "NO2"

    def test_fetch_measures_payload(self):
        api = UBAAirDataAPI()
        with requests_mock.Mocker() as mocker:
            mocker.get("https://www.umweltbundesamt.de/api/air_data/v3/measures/json", json=MEASURES_PAYLOAD)
            payload = api.get_measures_payload(5, "2026-04-07", "2026-04-08")
            assert "21" in payload["data"]


@pytest.mark.integration
class TestProducerWiring:
    """Test reference and telemetry emission with fake producers."""

    def test_send_reference_data(self):
        api = UBAAirDataAPI()

        class FakeProducer:
            def __init__(self):
                self.sent = []
                self.producer = self

            def send_de_uba_airdata_station(self, **kwargs):
                self.sent.append(("station", kwargs))

            def send_de_uba_airdata_components_component(self, **kwargs):
                self.sent.append(("component", kwargs))

            def flush(self):
                return None

        station_producer = FakeProducer()
        component_producer = FakeProducer()

        with patch.object(api, "get_stations_payload", return_value=STATIONS_PAYLOAD), patch.object(
            api, "get_components_payload", return_value=COMPONENTS_PAYLOAD
        ):
            stations, components, active_station_ids = send_reference_data(api, station_producer, component_producer)

        assert len(stations) == 2
        assert len(components) == 2
        assert active_station_ids == {21}
        assert len(station_producer.sent) == 2
        assert len(component_producer.sent) == 2
        assert station_producer.sent[0][1]["_station_id"] in {3, 21}
        assert component_producer.sent[0][1]["_component_id"] in {1, 5}

    def test_feed_measures_deduplicates(self):
        api = UBAAirDataAPI()

        class FakeProducer:
            def __init__(self):
                self.sent = []
                self.producer = self

            def send_de_uba_airdata_measure(self, **kwargs):
                self.sent.append(kwargs)

            def flush(self):
                return None

        producer = FakeProducer()
        previous_readings = {"21:5:2026-04-07 12:00:00": "2026-04-07 13:00:00"}

        class Component:
            def __init__(self, component_id: int):
                self.component_id = component_id

        with patch.object(api, "get_measures_payload", return_value=MEASURES_PAYLOAD):
            sent = feed_measures(
                api,
                producer,
                components=[Component(5)],
                active_station_ids={21},
                previous_readings=previous_readings,
            )

        assert sent == 1
        assert len(producer.sent) == 1
        assert producer.sent[0]["_station_id"] == 21
        assert producer.sent[0]["data"].date_start == "2026-04-07 13:00:00"
