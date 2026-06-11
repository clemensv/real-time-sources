"""Unit tests for the transport-agnostic ``noaa_core`` acquisition module.

``noaa_core`` is the shared upstream poller and record-normaliser consumed by
the MQTT and AMQP feeders. These tests exercise it directly (no generated
producer or ``proton`` dependency required) so the contract both transports
rely on is locked in.
"""

import datetime as dt

import noaa_core
from noaa_core import NOAAClient


def test_fetch_stations_raw_sanitizes_payload(requests_mock):
    requests_mock.get(
        noaa_core.STATIONS_URL,
        json={
            "stations": [
                {
                    "id": "9447130",
                    "name": "Seattle",
                    "tideType": "Subordinate",
                    "self": {"href": "https://example/9447130"},
                    "details": [{"href": "https://example/details"}],
                }
            ]
        },
    )
    stations = NOAAClient().fetch_stations_raw()
    assert len(stations) == 1
    s = stations[0]
    # id renamed to station_id, portscode backfilled.
    assert s["station_id"] == "9447130"
    assert "id" not in s
    assert s["portscode"] == ""
    # Nested link objects get region/station_id backfilled so the generated
    # Station schema (optional fields without None defaults) decodes cleanly.
    assert s["self"]["region"] is None
    assert s["self"]["station_id"] is None
    assert s["details"][0]["region"] is None


def test_datum_for_tide_type():
    assert NOAAClient.datum_for_tide_type("Great Lakes") == "IGLD"
    assert NOAAClient.datum_for_tide_type("Subordinate") == "MLLW"
    assert NOAAClient.datum_for_tide_type(None) == "MLLW"


def test_poll_product_water_level_returns_data(requests_mock):
    requests_mock.get(
        NOAAClient.BASE_URL,
        json={"data": [{"t": "2024-01-01 00:00", "v": "1.23", "s": "0.01", "f": "0,0,0,0", "q": "p"}]},
    )
    rows = NOAAClient().poll_product(
        "water_level", "9447130", "MLLW", dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc)
    )
    assert rows == [{"t": "2024-01-01 00:00", "v": "1.23", "s": "0.01", "f": "0,0,0,0", "q": "p"}]
    # Datum is included for water_level requests.
    assert "datum=MLLW" in requests_mock.last_request.url


def test_poll_product_currents_predictions_reads_nested_cp(requests_mock):
    requests_mock.get(
        NOAAClient.BASE_URL,
        json={"current_predictions": {"cp": [{"Time": "2024-01-01 00:00", "Velocity_Major": "1.0"}]}},
    )
    rows = NOAAClient().poll_product(
        "currents_predictions", "cb0102", "MLLW", dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc)
    )
    assert rows == [{"Time": "2024-01-01 00:00", "Velocity_Major": "1.0"}]
    assert "bin=1" in requests_mock.last_request.url


def test_poll_product_great_lakes_predictions_skipped():
    # IGLD datum + a predictions product short-circuits without any HTTP call.
    rows = NOAAClient().poll_product(
        "predictions", "9087044", "IGLD", dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc)
    )
    assert rows == []


def test_record_timestamp_field_selection():
    default = noaa_core.record_timestamp("water_level", {"t": "2024-03-04 05:06"})
    assert default == dt.datetime(2024, 3, 4, 5, 6, tzinfo=dt.timezone.utc)
    cp = noaa_core.record_timestamp("currents_predictions", {"Time": "2024-03-04 05:06"})
    assert cp == dt.datetime(2024, 3, 4, 5, 6, tzinfo=dt.timezone.utc)


def test_extract_fields_water_level_quality_and_flags():
    prelim = noaa_core.extract_fields(
        "water_level", {"v": "2.5", "s": "0.1", "f": "1,0,0,0", "q": "p"}
    )
    assert prelim["value"] == 2.5
    assert prelim["stddev"] == 0.1
    assert prelim["outside_sigma_band"] is True
    assert prelim["flat_tolerance_limit"] is False
    assert prelim["quality_preliminary"] is True

    verified = noaa_core.extract_fields(
        "water_level", {"v": "2.5", "f": "0,0,0,0", "q": "v"}
    )
    assert verified["quality_preliminary"] is False


def test_select_stations():
    class _S:
        def __init__(self, sid):
            self.station_id = sid

    stations = [_S("a"), _S("b"), _S("c")]
    # No filter returns all.
    assert [s.station_id for s in noaa_core.select_stations(stations, None)] == ["a", "b", "c"]
    # Comma-separated subset.
    assert [s.station_id for s in noaa_core.select_stations(stations, "a,c")] == ["a", "c"]
    # Requested-but-missing yields an empty list (fatal for the caller).
    assert noaa_core.select_stations(stations, "z") == []


def test_last_polled_roundtrip(tmp_path):
    path = str(tmp_path / "state.json")
    times = {"water_level": {"9447130": dt.datetime(2024, 1, 1, 12, 0, tzinfo=dt.timezone.utc)}}
    noaa_core.save_last_polled_times(path, times)
    loaded = noaa_core.load_last_polled_times(path)
    assert loaded["water_level"]["9447130"] == times["water_level"]["9447130"]
