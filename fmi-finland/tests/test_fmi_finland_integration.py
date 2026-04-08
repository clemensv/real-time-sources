"""Integration tests for the FMI Finland bridge with mocked HTTP responses."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from fmi_finland.fmi_finland import FMIAirQualityAPI, run_feed_cycle

from tests.test_fmi_finland_unit import OBSERVATIONS_XML, STATIONS_XML

pytestmark = pytest.mark.integration


def _has_stored_query(expected: str):
    def matcher(request):
        return request.qs.get("storedquery_id") == [expected]

    return matcher


def test_run_feed_cycle_emits_station_and_observation_events(requests_mock):
    requests_mock.get("https://opendata.fmi.fi/wfs", additional_matcher=_has_stored_query("fmi::ef::stations"), text=STATIONS_XML)
    requests_mock.get(
        "https://opendata.fmi.fi/wfs",
        additional_matcher=_has_stored_query("urban::observations::airquality::hourly::simple"),
        text=OBSERVATIONS_XML,
    )

    api = FMIAirQualityAPI()
    event_producer = MagicMock()
    event_producer.producer = MagicMock()
    state = {}

    counts = run_feed_cycle(
        api,
        event_producer,
        state,
        now=datetime(2026, 4, 8, 11, 12, tzinfo=timezone.utc),
        force_station_emit=True,
    )

    assert counts == {"stations": 1, "observations": 1}
    event_producer.send_fi_fmi_opendata_airquality_station.assert_called_once()
    event_producer.send_fi_fmi_opendata_airquality_observation.assert_called_once()

    station_call = event_producer.send_fi_fmi_opendata_airquality_station.call_args
    assert station_call.args[0] == "100662"
    assert station_call.args[1].station_name == "Helsinki Kallio 2"
    assert station_call.args[1].municipality == "Helsinki"

    observation_call = event_producer.send_fi_fmi_opendata_airquality_observation.call_args
    assert observation_call.args[0] == "100662"
    observation = observation_call.args[1]
    assert observation.pm10_ug_m3 == 12.5
    assert observation.pm2_5_ug_m3 == 6.3
    assert observation.o3_ug_m3 is None
    assert observation.observation_time == "2024-01-15T13:00:00Z"


def test_run_feed_cycle_deduplicates_unchanged_observations(requests_mock):
    requests_mock.get("https://opendata.fmi.fi/wfs", additional_matcher=_has_stored_query("fmi::ef::stations"), text=STATIONS_XML)
    requests_mock.get(
        "https://opendata.fmi.fi/wfs",
        additional_matcher=_has_stored_query("urban::observations::airquality::hourly::simple"),
        text=OBSERVATIONS_XML,
    )

    api = FMIAirQualityAPI()
    event_producer = MagicMock()
    event_producer.producer = MagicMock()
    state = {}

    run_feed_cycle(
        api,
        event_producer,
        state,
        now=datetime(2026, 4, 8, 11, 12, tzinfo=timezone.utc),
        force_station_emit=True,
    )
    event_producer.reset_mock()
    event_producer.producer = MagicMock()

    counts = run_feed_cycle(
        api,
        event_producer,
        state,
        now=datetime(2026, 4, 8, 12, 12, tzinfo=timezone.utc),
        force_station_emit=False,
    )

    assert counts == {"stations": 0, "observations": 0}
    event_producer.send_fi_fmi_opendata_airquality_station.assert_not_called()
    event_producer.send_fi_fmi_opendata_airquality_observation.assert_not_called()
