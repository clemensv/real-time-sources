from datetime import datetime, timezone
from unittest.mock import MagicMock, Mock

import pytest
import requests

from usgs_waterdata_core.capture import _points, capture, parse_rdb
from usgs_waterdata_core.client import WaterDataClient


def legacy_response(text="", document=None):
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.text = text
    response.json.return_value = document
    response.__enter__.return_value = response
    return response


def test_capture_removes_ogc_key_from_all_legacy_requests():
    session = Mock(spec=requests.Session)
    session.headers = {}
    session.get.side_effect = [
        legacy_response("agency_cd\tsite_no\tstation_nm\n5s\t15s\t50s\nUSGS\t01646500\tPotomac"),
        legacy_response(document={"value": {"timeSeries": []}}),
        legacy_response("agency_cd\tsite_no\t69928_00060\n5s\t15s\t14n\nUSGS\t01646500\t1520"),
    ]
    client = WaterDataClient(session=session, api_key="fixture-key")
    client.observations = Mock(return_value=iter([]))
    client.features = Mock(return_value=iter([]))
    data = capture(
        client,
        sites=["01646500"],
        parameters="00060",
        start=datetime(2026, 11, 16, 12, tzinfo=timezone.utc),
        end=datetime(2026, 11, 16, 14, tzinfo=timezone.utc),
    )
    assert data["legacy_rdb_identities"] == ["USGS/01646500/00060/69928"]
    assert data["series"] == {}
    assert session.headers["X-Api-Key"] == "fixture-key"
    assert len(session.get.call_args_list) == 3
    assert all(call.kwargs["headers"] == {"X-Api-Key": None} for call in session.get.call_args_list)


def test_conflicting_points_cannot_create_a_crosswalk_candidate():
    with pytest.raises(ValueError, match="Conflicting"):
        _points(
            [
                {"time": "2026-11-16T12:00:00Z", "value": "1"},
                {"time": "2026-11-16T07:00:00-05:00", "value": "2"},
            ]
        )


@pytest.mark.parametrize("text", ["<html>Unavailable</html>", "agency_cd\tsite_no\n5s\t15s\nUSGS"])
def test_failed_or_truncated_legacy_table_is_not_a_valid_snapshot(text):
    with pytest.raises(ValueError):
        parse_rdb(text)
