
from __future__ import annotations

import pytest
from requests import Timeout

from jma_bosai_volcano.jma_bosai_volcano import (
    JMABosaiVolcanoAPI,
    ConditionEnum,
    EruptionTypeenum,
    decimal_degrees,
    to_utc,
    alert_level_description,
    map_condition,
    parse_volcano_catalog,
    parse_warning_record,
    parse_eruption_record,
    load_state,
)


VOLCANO_FIXTURE = {
    "506": {
        "nameJp": "桜島",
        "nameEn": "Sakurajima",
        "lat": [31, 35.5],
        "lon": [130, 39.5],
        "levelOperation": True,
        "elevation": 1117,
    },
    "105": {
        "name_jp": "雌阿寒岳",
        "name_en": "Meakandake",
        "latlon": ["43.386", "144.009"],
        "levelOperation": True,
    },
}

WARNING_FIXTURE = {
    "reportDatetime": "2022-07-27T20:00:00+09:00",
    "eventId": "506",
    "areas": ["4620100"],
    "volcanoInfos": [
        {
            "type": "噴火警報・予報（対象火山）",
            "items": [
                {
                    "name": "レベル３（入山規制）",
                    "code": "13",
                    "lastCode": "15",
                    "condition": "引下げ",
                    "areas": [{"name": "桜島", "code": "506"}],
                }
            ],
        },
        {
            "type": "噴火警報・予報（対象市町村等）",
            "items": [{"name": "火口周辺警報", "code": "02", "areas": [{"code": "4620100"}]}],
        },
    ],
}

ERUPTION_FIXTURE = {
    "reportDatetime": "2025-01-02T03:04:05+09:00",
    "eventId": "506",
    "areas": ["4620100"],
    "volcanoInfos": [
        {
            "type": "噴火に関する火山観測報",
            "items": [
                {
                    "name": "噴火",
                    "eruptionDatetime": "2025-01-02T03:00:00+09:00",
                    "description": "有色噴煙：火口上2000m（海抜10100FT）\n流　　向：直上\n---\n火口：南岳山頂火口\n噴火開始以降の最高噴煙高度：火口上3000m（海抜13400FT）\n噴煙量：やや多量\n火砕流を火口南西約2kmまで確認",
                    "areas": [{"name": "桜島", "code": "506"}],
                }
            ],
        }
    ],
}


class FlushHandle:
    def __init__(self, result=0):
        self.result = result
        self.calls = 0

    def flush(self, timeout=None):
        self.calls += 1
        return self.result


class FakeProducer:
    def __init__(self, flush_result=0):
        self.producer = FlushHandle(flush_result)
        self.events = []

    def send_jp_jma_volcano_volcano(self, **kwargs):
        self.events.append(("volcano", kwargs))

    def send_jp_jma_volcano_volcanic_warning(self, **kwargs):
        self.events.append(("warning", kwargs))

    def send_jp_jma_volcano_volcanic_eruption(self, **kwargs):
        self.events.append(("eruption", kwargs))


def test_decimal_degree_conversion():
    assert decimal_degrees([31, 35.5]) == pytest.approx(31.5916666667)
    assert decimal_degrees("43.386") == pytest.approx(43.386)


def test_jst_to_utc_conversion():
    assert to_utc("2022-07-27T20:00:00+09:00").isoformat() == "2022-07-27T11:00:00+00:00"


def test_alert_level_mapping():
    expected = {
        "02": "Crater-area warning",
        "03": "Eruption warning for surrounding sea area",
        "04": "Eruption forecast: warning lifted",
        "13": "Mountain access restriction",
        "36": "Surrounding waters warning for submarine or island volcanoes",
        "43": "Crater-area warning: entry restrictions and similar measures",
        "44": "Eruption warning for surrounding sea area: surrounding sea area warning",
        "45": "Active volcano; pay attention",
        "49": "Crater-area warning: caution around the crater",
    }
    for code, label in expected.items():
        assert alert_level_description(code) == label


def test_condition_mapping():
    assert map_condition("引上げ") is ConditionEnum.RAISED
    assert map_condition("引下げ") is ConditionEnum.LOWERED
    assert map_condition("継続") is ConditionEnum.CONTINUED
    assert map_condition("発表") is ConditionEnum.ISSUED
    assert map_condition("切替") is ConditionEnum.SWITCHED
    assert map_condition("解除") is ConditionEnum.CANCELLED


def test_parse_volcano_metadata_fixture():
    catalog = parse_volcano_catalog(VOLCANO_FIXTURE)
    assert set(catalog) == {"506", "105"}
    sakurajima = catalog["506"]
    assert sakurajima.name_jp == "桜島"
    assert sakurajima.latitude == pytest.approx(31.5916666667)
    assert sakurajima.longitude == pytest.approx(130.6583333333)
    assert sakurajima.elevation_m == 1117
    assert sakurajima.level_operation is True


def test_parse_warning_fixture():
    warnings = parse_warning_record(WARNING_FIXTURE)
    assert len(warnings) == 1
    warning = warnings[0]
    assert warning.volcano_code == "506"
    assert warning.event_id == "506"
    assert warning.report_datetime.isoformat() == "2022-07-27T11:00:00+00:00"
    assert warning.alert_level_code == "13"
    assert warning.previous_level_code == "15"
    assert warning.condition is ConditionEnum.LOWERED
    assert warning.area_codes == ["4620100"]


@pytest.mark.parametrize(
    ("code", "name", "condition", "expected_condition"),
    [
        ("02", "火口周辺警報", "切替", ConditionEnum.SWITCHED),
        ("03", "噴火警報（周辺海域）", "切替", ConditionEnum.SWITCHED),
        ("04", "噴火予報：警報解除", "解除", ConditionEnum.CANCELLED),
        ("43", "火口周辺警報：入山規制等", "発表", ConditionEnum.ISSUED),
        ("44", "噴火警報（周辺海域）：周辺海域警戒", "継続", ConditionEnum.CONTINUED),
        ("45", "活火山であることに留意", "解除", ConditionEnum.CANCELLED),
        ("49", "火口周辺警報：火口周辺警戒", "継続", ConditionEnum.CONTINUED),
    ],
)
def test_parse_warning_live_code_and_condition_fixtures(code, name, condition, expected_condition):
    fixture = {
        **WARNING_FIXTURE,
        "volcanoInfos": [
            {
                "type": "噴火警報・予報（対象火山）",
                "items": [
                    {
                        "name": name,
                        "code": code,
                        "lastCode": code,
                        "condition": condition,
                        "areas": [{"name": "テスト火山", "code": "506"}],
                    }
                ],
            }
        ],
    }
    warning = parse_warning_record(fixture)[0]
    assert warning.alert_level_code == code
    assert warning.alert_level_name == name
    assert warning.condition is expected_condition


def test_parse_eruption_fixture():
    eruptions = parse_eruption_record(ERUPTION_FIXTURE)
    assert len(eruptions) == 1
    eruption = eruptions[0]
    assert eruption.volcano_code == "506"
    assert eruption.report_datetime.isoformat() == "2025-01-01T18:04:05+00:00"
    assert eruption.eruption_datetime.isoformat() == "2025-01-01T18:00:00+00:00"
    assert eruption.eruption_type is EruptionTypeenum.ERUPTION
    assert eruption.colored_plume_height_m == 2000
    assert eruption.maximum_plume_height_since_start_m == 3000
    assert eruption.plume_direction == "直上"
    assert eruption.crater_name == "南岳山頂火口"
    assert eruption.pyroclastic_flow_observed is True
    assert eruption.plume_amount_jp == "やや多量"
    assert "噴火" in eruption.description
    assert eruption.info_type_jp == "噴火に関する火山観測報"


def test_dedup_state_advances_after_successful_flush(tmp_path):
    class API(JMABosaiVolcanoAPI):
        def fetch_warnings(self):
            return [WARNING_FIXTURE]
        def fetch_eruptions(self):
            return [ERUPTION_FIXTURE]

    state_file = tmp_path / "state.json"
    state = {"warnings": [], "eruptions": [], "last_metadata_refresh": None}
    producer = FakeProducer()
    counts = API().poll_once(producer, state, str(state_file))
    assert counts == (1, 1)
    assert state["warnings"] == ["506|2022-07-27T20:00:00+09:00"]
    assert state["eruptions"] == ["506|2025-01-02T03:04:05+09:00"]
    persisted = load_state(str(state_file))
    assert persisted["warnings"] == state["warnings"]


def test_flush_failure_does_not_advance_dedup_state(tmp_path):
    class API(JMABosaiVolcanoAPI):
        def fetch_warnings(self):
            return [WARNING_FIXTURE]
        def fetch_eruptions(self):
            return []

    state_file = tmp_path / "state.json"
    state = {"warnings": [], "eruptions": [], "last_metadata_refresh": None}
    with pytest.raises(RuntimeError):
        API().poll_once(FakeProducer(flush_result=1), state, str(state_file))
    assert state["warnings"] == []
    assert not state_file.exists()


def test_reference_refresh_failure_keeps_cached_catalog(tmp_path):
    api = JMABosaiVolcanoAPI()
    api.volcano_catalog = parse_volcano_catalog(VOLCANO_FIXTURE)
    def fail_refresh():
        raise Timeout("metadata timeout")
    api.refresh_catalog = fail_refresh
    state = {"warnings": [], "eruptions": [], "last_metadata_refresh": "2000-01-01T00:00:00+00:00"}
    api.maybe_refresh_reference_data(FakeProducer(), state, str(tmp_path / "state.json"), 1)
    assert set(api.volcano_catalog) == {"506", "105"}


def test_one_endpoint_failure_skips_only_that_slice(tmp_path):
    class API(JMABosaiVolcanoAPI):
        def fetch_warnings(self):
            raise Timeout("warning timeout")
        def fetch_eruptions(self):
            return [ERUPTION_FIXTURE]

    state = {"warnings": [], "eruptions": [], "last_metadata_refresh": None}
    producer = FakeProducer()
    counts = API().poll_once(producer, state, str(tmp_path / "state.json"))
    assert counts == (0, 1)
    assert [kind for kind, _ in producer.events] == ["eruption"]
    assert state["warnings"] == []
    assert state["eruptions"] == ["506|2025-01-02T03:04:05+09:00"]


def test_error_resilience_for_bad_payloads():
    assert parse_warning_record({"eventId": "x"}) == []
    assert parse_eruption_record({"eventId": "x", "reportDatetime": "bad"}) == []
