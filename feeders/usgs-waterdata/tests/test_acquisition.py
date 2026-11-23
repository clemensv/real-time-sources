from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import requests

from usgs_waterdata_core.client import BASE_URL, WaterDataClient, time_interval
from usgs_waterdata_core.state import DeliveryState


def feature(value="1", modified="2026-11-16T12:00:00Z", feature_id="ephemeral"):
    return {
        "type": "Feature",
        "id": feature_id,
        "properties": {
            "time_series_id": "series",
            "time": "2026-11-16T12:00:00Z",
            "value": value,
            "last_modified": modified,
        },
    }


def response(data, status=200):
    result = Mock(status_code=status)
    result.json.return_value = data
    return result


def test_follows_opaque_next_link_without_reapplying_initial_filters():
    next_url = f"{BASE_URL}/collections/continuous/items?cursor=a%2Bb%3D&limit=1"
    session = Mock(spec=requests.Session)
    session.headers = {}
    session.get.side_effect = [
        response({"features": [feature()], "links": [{"rel": "next", "href": next_url}]}),
        response({"features": [feature("2")], "links": []}),
    ]
    client = WaterDataClient(session=session, api_key="test-key")
    assert len(list(client.features("continuous", state_code="10"))) == 2
    assert session.get.call_args_list[1].args == (next_url,)
    assert session.get.call_args_list[1].kwargs["params"] is None
    assert session.headers["X-Api-Key"] == "test-key"


@pytest.mark.parametrize(
    "url",
    [
        "https://unrelated.example/items",
        "http://api.waterdata.usgs.gov/ogcapi/v1/items",
        "https://api.waterdata.usgs.gov@unrelated.example/ogcapi/v1/items",
        "https://api.waterdata.usgs.gov/another-api/items",
    ],
)
def test_does_not_forward_credentials_to_foreign_continuation(url):
    session = Mock(spec=requests.Session)
    session.headers = {}
    session.get.return_value = response({"features": [], "links": [{"rel": "next", "href": url}]})
    client = WaterDataClient(session=session)
    with pytest.raises(ValueError, match="outside"):
        list(client.features("continuous"))
    assert session.get.call_count == 1


def test_paging_failure_does_not_commit_partial_cycle(tmp_path):
    state = DeliveryState(tmp_path / "state.json")
    sent = []

    def incomplete():
        yield feature()
        raise requests.Timeout("second page timed out")

    with pytest.raises(requests.Timeout):
        state.deliver(incomplete(), sent.append, lambda: None)
    assert len(sent) == 1
    assert state.data["observations"] == {}
    assert not state.path.exists()


def test_delivery_failure_keeps_observation_eligible_after_restart(tmp_path):
    state = DeliveryState(tmp_path / "state.json")

    def failed_flush():
        raise RuntimeError("broker did not acknowledge")

    with pytest.raises(RuntimeError, match="acknowledge"):
        state.deliver([feature()], lambda _: None, failed_flush)
    sent = []
    restarted = DeliveryState(state.path)
    assert restarted.deliver([feature()], sent.append, lambda: None) == 1
    assert DeliveryState(state.path).deliver([feature()], sent.append, lambda: None) == 0


def test_database_refresh_is_deduplicated_but_measurement_correction_is_sent():
    state = DeliveryState()
    sent = []
    assert state.deliver([feature()], sent.append, lambda: None) == 1
    assert state.deliver(
        [feature(modified="2026-11-16T13:00:00Z", feature_id="new-uuid")],
        sent.append,
        lambda: None,
    ) == 0
    assert state.deliver([feature("2")], sent.append, lambda: None) == 1
    assert len(sent) == 2


def test_nonzero_kafka_flush_remainder_blocks_checkpoint(tmp_path):
    state = DeliveryState(tmp_path / "state.json")
    with pytest.raises(RuntimeError, match="unacknowledged"):
        state.deliver([feature()], lambda _: None, lambda: 1)
    assert state.data["observations"] == {}
    assert not state.path.exists()


def test_equivalent_offsets_do_not_create_corrections():
    state = DeliveryState()
    sent = []
    original = feature()
    state.deliver([original], sent.append, lambda: None)
    original["properties"]["time"] = "2026-11-16T07:00:00-05:00"
    assert state.deliver([original], sent.append, lambda: None) == 0


def test_uses_fixed_time_window_not_datetime_duration():
    session = Mock(spec=requests.Session)
    session.headers = {}
    session.get.return_value = response({"features": [], "links": []})
    client = WaterDataClient(session=session)
    start = datetime(2026, 11, 16, 12, tzinfo=timezone.utc)
    end = datetime(2026, 11, 16, 14, tzinfo=timezone.utc)
    list(client.observations(start, end, location_ids="USGS-01646500"))
    params = session.get.call_args.kwargs["params"]
    assert params["time"] == "2026-11-16T12:00:00+00:00/2026-11-16T14:00:00+00:00"
    assert "datetime" not in params
    with pytest.raises(ValueError):
        time_interval(end, start)


def test_update_time_query_does_not_exclude_old_observation_corrections():
    session = Mock(spec=requests.Session)
    session.headers = {}
    old = feature()
    old["properties"]["time"] = "2020-01-01T12:00:00Z"
    session.get.return_value = response({"features": [old], "links": []})
    client = WaterDataClient(session=session)
    start = datetime(2026, 11, 16, 12, tzinfo=timezone.utc)
    end = datetime(2026, 11, 16, 14, tzinfo=timezone.utc)
    assert list(client.changes(start, end, state_code="10")) == [old]
    params = session.get.call_args.kwargs["params"]
    assert params["last_modified"] == time_interval(start, end)
    assert "time" not in params


def test_repeated_continuation_is_an_error():
    session = Mock(spec=requests.Session)
    session.headers = {}
    session.get.return_value = response(
        {"features": [], "links": [{"rel": "next", "href": f"{BASE_URL}/collections/continuous/items?cursor=x"}]}
    )
    with pytest.raises(ValueError, match="repeated"):
        list(WaterDataClient(session=session).features("continuous"))


def test_corrupt_state_does_not_silently_reset(tmp_path):
    path = tmp_path / "state.json"
    path.write_text('{"version": 999, "observations": {}}', encoding="utf-8")
    with pytest.raises(ValueError, match="corrupt"):
        DeliveryState(path)
