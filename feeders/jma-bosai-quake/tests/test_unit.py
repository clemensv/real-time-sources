import os
from pathlib import Path

import pytest
import requests

from jma_bosai_quake.jma_bosai_quake import (
    DEFAULT_STATE_FILE,
    JmaBosaiQuakeAPI,
    extract_tsunami_possible,
    magnitude_bucket,
    map_info_type,
    parse_control_datetime,
    parse_iso6709_location,
    prefecture_slug,
    to_utc_rfc3339,
)


SAMPLE_ENTRY = {
    "ctt": "20260521011147",
    "eid": "20260521010824",
    "rdt": "2026-05-21T01:11:00+09:00",
    "ttl": "震源・震度情報",
    "ift": "発表",
    "ser": "1",
    "at": "2026-05-21T01:08:00+09:00",
    "anm": "京都府南部",
    "acd": "511",
    "cod": "+35.0+135.5-10000/",
    "mag": "2.4",
    "maxi": "1",
    "int": [{"code": "27", "maxi": "1", "city": [{"code": "2732200", "maxi": "1"}]}],
    "json": "20260521011147_20260521010824_VXSE5k_1.json",
    "en_ttl": "Earthquake and Seismic Intensity Information",
    "en_anm": "Southern Kyoto Prefecture",
}

DETAIL_NO_TSUNAMI = {
    "Body": {
        "Comments": {
            "ForecastComment": {
                "Text": "この地震による津波の心配はありません。",
                "enText": "This earthquake poses no tsunami risk.\n",
            }
        }
    }
}


class FakeKafkaProducer:
    def __init__(self, remainder=0):
        self.remainder = remainder
        self.flush_calls = 0

    def flush(self, timeout=None):
        self.flush_calls += 1
        return self.remainder


class FakeEventProducer:
    def __init__(self):
        self.sent = []

    def send_jp_jma_quake_earthquake_report(self, **kwargs):
        self.sent.append(kwargs)


class StubAPI(JmaBosaiQuakeAPI):
    def __init__(self, reports, detail=None, detail_error=None, state_file=""):
        super().__init__(state_file=state_file)
        self._reports = reports
        self._detail = detail
        self._detail_error = detail_error

    def list_reports(self):
        return self._reports

    def fetch_detail(self, filename):
        if self._detail_error:
            raise self._detail_error
        return self._detail


def test_iso6709_parser_positive_coords_depth_conversion():
    assert parse_iso6709_location("+35.0+135.5-10000/") == (35.0, 135.5, 10.0)


def test_iso6709_parser_negative_coords_and_positive_depth():
    assert parse_iso6709_location("-12.5-077.25+30000/") == (-12.5, -77.25, 30.0)


def test_iso6709_parser_rejects_bad_values():
    with pytest.raises(ValueError):
        parse_iso6709_location("35.0,135.5,-10000")


def test_jst_to_utc_conversion():
    assert to_utc_rfc3339("2026-05-21T01:11:00+09:00") == "2026-05-20T16:11:00+00:00"


def test_control_datetime_conversion_from_compact_jst():
    assert parse_control_datetime("20260521011147") == (
        "2026-05-20T16:11:47+00:00",
        "2026-05-21T01:11:47+09:00",
    )


def test_info_type_mapping():
    assert map_info_type("発表") == "ISSUED"
    assert map_info_type("訂正") == "CORRECTED"
    assert map_info_type("取消") == "CANCELLED"
    with pytest.raises(ValueError):
        map_info_type("不明")


def test_prefecture_slug_and_magnitude_bucket_for_topic_axes():
    assert prefecture_slug("Southern Kyoto Prefecture", []) == "kyoto"
    assert magnitude_bucket(2.4) == "magnitude-2"
    assert magnitude_bucket(None) == "magnitude-unknown"
    assert magnitude_bucket(0.4) == "magnitude-lt1"
    assert magnitude_bucket(9.1) == "magnitude-9plus"
    assert magnitude_bucket(8.9) == "magnitude-8"


def test_list_entry_normalization_from_fixture():
    api = JmaBosaiQuakeAPI(state_file="")
    report = api.normalize_report(SAMPLE_ENTRY, DETAIL_NO_TSUNAMI)
    assert report.prefecture == "kyoto"
    assert report.magnitude_bucket == "magnitude-2"
    assert report.event_id == "20260521010824"
    assert report.report_id == "20260521010824_1"
    assert report.serial == 1
    assert report.info_type.value == "ISSUED"
    assert report.report_datetime.isoformat() == "2026-05-20T16:11:00+00:00"
    assert report.control_datetime.isoformat() == "2026-05-20T16:11:47+00:00"
    assert report.control_datetime_local.isoformat() == "2026-05-21T01:11:47+09:00"
    assert report.origin_datetime.isoformat() == "2026-05-20T16:08:00+00:00"
    assert report.latitude == 35.0
    assert report.longitude == 135.5
    assert report.depth_km == 10.0
    assert report.magnitude == 2.4
    assert report.max_intensity.value == "1"
    assert report.bulletin_type.value == "VXSE5k"
    assert report.tsunami_possible is False
    assert report.affected_prefectures[0].code == "27"
    assert report.affected_cities[0].city_code == "2732200"


def test_nullable_fields_are_explicit_for_intensity_bulletin_without_hypocenter_or_english_title():
    entry = dict(SAMPLE_ENTRY)
    entry.update(
        {
            "ttl": "震度速報",
            "json": "20260521011147_20260521010824_VXSE51_1.json",
            "maxi": None,
        }
    )
    for key in ("en_ttl", "en_anm", "anm", "acd", "cod", "mag"):
        entry.pop(key, None)

    report = JmaBosaiQuakeAPI(state_file="").normalize_report(entry)

    assert report.prefecture == "osaka"
    assert report.magnitude_bucket == "magnitude-unknown"
    assert report.title_en is None
    assert report.epicenter_area_code is None
    assert report.epicenter_area_jp is None
    assert report.epicenter_area_en is None
    assert report.latitude is None
    assert report.longitude is None
    assert report.depth_km is None
    assert report.magnitude is None
    assert report.max_intensity is None
    assert report.bulletin_type.value == "VXSE51"


def test_tsunami_possible_detection():
    assert extract_tsunami_possible(DETAIL_NO_TSUNAMI) is False
    assert extract_tsunami_possible({"Body": {"Comments": {"ForecastComment": {"Text": "津波に注意してください"}}}}) is True
    assert extract_tsunami_possible({"Body": {"Comments": {}}}) is None


def test_dedup_skips_seen_report():
    api = StubAPI([SAMPLE_ENTRY], DETAIL_NO_TSUNAMI)
    event_producer = FakeEventProducer()
    kafka_producer = FakeKafkaProducer()
    assert api.poll_once(event_producer, kafka_producer) == 1
    assert len(event_producer.sent) == 1
    assert api.poll_once(event_producer, kafka_producer) == 0
    assert len(event_producer.sent) == 1


def test_unsupported_bulletin_type_is_warned_and_skipped(caplog):
    entry = dict(SAMPLE_ENTRY)
    entry["json"] = "20260521011147_20260521010824_VXSE99_1.json"
    api = StubAPI([entry], DETAIL_NO_TSUNAMI)

    assert api.poll_once(FakeEventProducer(), FakeKafkaProducer()) == 0
    assert "Skipping unsupported JMA earthquake bulletin type VXSE99" in caplog.text


def test_detail_fetch_error_still_emits_report():
    api = StubAPI([SAMPLE_ENTRY], detail_error=requests.Timeout("boom"))
    event_producer = FakeEventProducer()
    assert api.poll_once(event_producer, FakeKafkaProducer()) == 1
    assert event_producer.sent[0]["data"].tsunami_possible is None


def test_flush_failure_does_not_advance_dedup_state():
    api = StubAPI([SAMPLE_ENTRY], DETAIL_NO_TSUNAMI)
    event_producer = FakeEventProducer()
    with pytest.raises(RuntimeError):
        api.poll_once(event_producer, FakeKafkaProducer(remainder=1))
    assert (SAMPLE_ENTRY["eid"], int(SAMPLE_ENTRY["ser"])) not in api.seen
    assert api.poll_once(event_producer, FakeKafkaProducer()) == 1


def test_state_file_persists_seen_keys():
    state_path = Path("state") / "test-jma-bosai-quake-state.json"
    if state_path.exists():
        state_path.unlink()
    try:
        api = StubAPI([SAMPLE_ENTRY], DETAIL_NO_TSUNAMI, state_file=str(state_path))
        assert api.poll_once(FakeEventProducer(), FakeKafkaProducer()) == 1
        reloaded = StubAPI([SAMPLE_ENTRY], DETAIL_NO_TSUNAMI, state_file=str(state_path))
        assert reloaded.poll_once(FakeEventProducer(), FakeKafkaProducer()) == 0
    finally:
        if state_path.exists():
            state_path.unlink()
        if state_path.parent.exists() and not any(state_path.parent.iterdir()):
            state_path.parent.rmdir()


def test_default_state_file_matches_repo_contract():
    assert DEFAULT_STATE_FILE == ".\\state\\jma-bosai-quake.json"
