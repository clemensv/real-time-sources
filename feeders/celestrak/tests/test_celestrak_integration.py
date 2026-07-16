"""Integration tests for the CelesTrak core HTTP client.

The upstream API is mocked via ``requests_mock``; no Kafka, MQTT or AMQP is
involved. These tests pin the two behaviours the polling loops depend on: the
per-family dedup semantics (SATCAT/GP deduped by NORAD id, SupGP not) and the
usage-policy hard stop that trips :attr:`CelesTrakAPI.halted` on 403/429/503.
"""

import pytest
import requests_mock

from celestrak_core import GP_URL, SATCAT_URL, SUPGP_URL, CelesTrakAPI


def _gp_row(norad, epoch="2026-07-16T12:00:00"):
    return {"NORAD_CAT_ID": norad, "EPOCH": epoch, "OBJECT_NAME": f"OBJ-{norad}"}


@pytest.mark.integration
class TestGetSatcat:
    def test_merges_and_dedupes_by_norad(self):
        api = CelesTrakAPI()
        with requests_mock.Mocker() as m:
            m.get(SATCAT_URL, [
                {"json": [{"NORAD_CAT_ID": 25544}, {"NORAD_CAT_ID": 20580}]},
                {"json": [{"NORAD_CAT_ID": 25544}]},  # 25544 repeats in 2nd group
            ])
            rows = api.get_satcat(["stations", "active"])
        assert sorted(r["NORAD_CAT_ID"] for r in rows) == [20580, 25544]

    def test_skips_rows_without_norad(self):
        api = CelesTrakAPI()
        with requests_mock.Mocker() as m:
            m.get(SATCAT_URL, json=[{"OBJECT_NAME": "no-id"}, {"NORAD_CAT_ID": 1}])
            rows = api.get_satcat(["stations"])
        assert [r["NORAD_CAT_ID"] for r in rows] == [1]


@pytest.mark.integration
class TestGetGp:
    def test_dedupes_by_norad_across_groups(self):
        api = CelesTrakAPI()
        with requests_mock.Mocker() as m:
            m.get(GP_URL, [
                {"json": [_gp_row(25544, "e1")]},
                {"json": [_gp_row(25544, "e2")]},  # later group wins
            ])
            rows = api.get_gp(["stations", "active"])
        assert len(rows) == 1
        assert rows[0]["EPOCH"] == "e2"

    def test_non_json_200_body_returns_empty(self):
        api = CelesTrakAPI()
        with requests_mock.Mocker() as m:
            m.get(GP_URL, text="Invalid query. No GP data found for GROUP=nope.")
            assert api.get_gp(["nope"]) == []


@pytest.mark.integration
class TestGetSupgp:
    def test_does_not_dedupe_by_norad(self):
        api = CelesTrakAPI()
        with requests_mock.Mocker() as m:
            m.get(SUPGP_URL, json=[
                {"NORAD_CAT_ID": 25544, "DATA_SOURCE": "a", "EPOCH": "e1"},
                {"NORAD_CAT_ID": 25544, "DATA_SOURCE": "a", "EPOCH": "e2"},
            ])
            rows = api.get_supgp(["SpaceX-E"])
        assert len(rows) == 2


@pytest.mark.integration
class TestUsagePolicyHardStop:
    @pytest.mark.parametrize("status", [403, 429, 503])
    def test_hard_stop_status_sets_halted(self, status):
        api = CelesTrakAPI()
        with requests_mock.Mocker() as m:
            m.get(GP_URL, status_code=status)
            rows = api.get_gp(["stations"])
        assert rows == []
        assert api.halted is True

    def test_halted_short_circuits_further_requests(self):
        api = CelesTrakAPI()
        api.halted = True
        with requests_mock.Mocker() as m:
            m.get(GP_URL, json=[_gp_row(1)])
            assert api.get_gp(["stations"]) == []
            assert not m.called

    def test_non_hard_stop_error_does_not_halt(self):
        api = CelesTrakAPI()
        with requests_mock.Mocker() as m:
            m.get(GP_URL, status_code=404)
            assert api.get_gp(["stations"]) == []
        assert api.halted is False
