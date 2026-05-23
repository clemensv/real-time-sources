from __future__ import annotations

from datetime import datetime, timezone

import pytest

from noaa_swpc_l1_core import EXPECTED_COLUMNS, SwpcL1API, parse_row


@pytest.mark.unit
def test_fetch_rows_validates_header_drift(upstream_payload, fake_session_factory):
    payload = [EXPECTED_COLUMNS.copy(), *upstream_payload[1:]]
    payload[0][1] = "plasma_speed"
    api = SwpcL1API(session=fake_session_factory(payload))

    with pytest.raises(ValueError, match="header changed"):
        api.fetch_rows("dscovr")


@pytest.mark.unit
def test_fetch_rows_normalizes_timestamps_and_nulls(upstream_payload, fake_session_factory):
    api = SwpcL1API(session=fake_session_factory(upstream_payload), request_timeout=7.5)

    rows = api.fetch_rows("dscovr")

    assert len(rows) == 2
    first = rows[0]
    assert first.spacecraft == "dscovr"
    assert first.time_tag == datetime(2025, 1, 2, 3, 4, 5, 123000, tzinfo=timezone.utc)
    assert first.propagated_time_tag == datetime(2025, 1, 2, 3, 44, 5, 123000, tzinfo=timezone.utc)
    assert first.speed == 410.5
    assert first.density == 6.2
    assert first.temperature == 123456.0
    assert first.bz is None
    assert first.vx is None
    assert first.vy is None
    assert first.vz is None
    assert api._session.calls == [(api.feed_url, 7.5)]
    assert api._session.response.raise_for_status_called is True


@pytest.mark.unit
def test_fetch_rows_sorts_chronologically(upstream_payload, fake_session_factory):
    payload = [upstream_payload[0], upstream_payload[2], upstream_payload[1]]
    api = SwpcL1API(session=fake_session_factory(payload))

    rows = api.fetch_rows("ace")

    assert [row.time_tag.minute for row in rows] == [4, 5]
    assert {row.spacecraft for row in rows} == {"ace"}


@pytest.mark.unit
def test_fetch_new_rows_filters_strictly_newer(upstream_payload, fake_session_factory):
    api = SwpcL1API(session=fake_session_factory(upstream_payload))
    since = datetime(2025, 1, 2, 3, 4, 5, 123000, tzinfo=timezone.utc)

    rows = list(api.fetch_new_rows("dscovr", since=since))

    assert len(rows) == 1
    assert rows[0].time_tag == datetime(2025, 1, 2, 3, 5, 5, tzinfo=timezone.utc)


@pytest.mark.unit
def test_parse_row_rejects_short_or_unparseable_rows(upstream_payload):
    assert parse_row([], "dscovr") is None
    bad = upstream_payload[1].copy()
    bad[0] = "not-a-date"
    assert parse_row(bad, "dscovr") is None
