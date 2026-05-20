from __future__ import annotations

from pathlib import Path

import pytest

from tepco_denkiyoho.tepco_denkiyoho import (
    DAILY_CSV_URL,
    DenkiyohoState,
    PEAK_FORECAST_TIME_SENTINEL,
    SUPPLY_CAPACITY_TIME_SENTINEL,
    TepcoDenkiyohoAPI,
    actual_key,
    decode_shift_jis_csv,
    forecast_key,
    jp_unit_to_mw,
    jst_to_rfc3339,
    parse_denkiyoho_csv,
    split_sections,
)

SAMPLE_TEXT = """2026/5/21 6:30 UPDATE
ピーク時供給力(万kW),時間帯,供給力情報更新日,供給力情報更新時刻,ピーク時予備率(%),ピーク時使用率(%)
3839,13:00-14:00,5/21,6:10,14,87

予想最大電力(万kW),時間帯,予想最大電力情報更新日,予想最大電力情報更新時刻
3363,13:00-14:00,5/21,6:10

DATE,TIME,当日実績(万kW),予測値(万kW),使用率(%),供給力(万kW)
2026/5/21,0:00,2489,2447,86,2866
2026/5/21,1:00,2363,2330,85,2765

最大使用率(%),時間帯
88,4:00-5:00

DATE,TIME,当日実績(５分間隔値)(万kW),太陽光発電実績(５分間隔値)(万kW),太陽光発電量(電力使用量に対する割合)(%)
2026/5/21,0:00,2562,0,0
2026/5/21,0:05,0,,
2026/5/21,0:10,2552,0,0
2026/5/21,0:15,2550,,
"""


@pytest.fixture()
def shift_jis_fixture():
    fixture = Path(__file__).parent / "fixtures" / "juyo-d1-j-sample.csv"
    fixture.write_bytes(SAMPLE_TEXT.encode("cp932"))
    return fixture


class FakeEventProducer:
    def __init__(self, flush_remaining: int = 0):
        self.events = []
        self.flush_remaining = flush_remaining

    def send_jp_tepco_denkiyoho_supply_capacity(self, **kwargs):
        self.events.append(("supply", kwargs))

    def send_jp_tepco_denkiyoho_peak_demand_forecast(self, **kwargs):
        self.events.append(("peak_forecast", kwargs))

    def send_jp_tepco_denkiyoho_demand_actual(self, **kwargs):
        self.events.append(("actual", kwargs))

    def send_jp_tepco_denkiyoho_demand_forecast(self, **kwargs):
        self.events.append(("forecast", kwargs))

    def flush(self, timeout=30.0):
        return self.flush_remaining


class StubAPI(TepcoDenkiyohoAPI):
    def __init__(self, content: bytes):
        super().__init__(url=DAILY_CSV_URL)
        self.content = content

    def fetch_daily_csv(self) -> bytes:
        return self.content


def test_shift_jis_csv_decoding(shift_jis_fixture):
    decoded = decode_shift_jis_csv(shift_jis_fixture.read_bytes())
    assert "ピーク時供給力(万kW)" in decoded
    assert "予想最大電力(万kW)" in decoded
    assert "最大使用率(%)" in decoded
    assert "当日実績(５分間隔値)(万kW)" in decoded


def test_section_splitting(shift_jis_fixture):
    hourly, actual, _ = split_sections(decode_shift_jis_csv(shift_jis_fixture.read_bytes()))
    assert hourly[0][:6] == ["DATE", "TIME", "当日実績(万kW)", "予測値(万kW)", "使用率(%)", "供給力(万kW)"]
    assert actual[0][2] == "当日実績(５分間隔値)(万kW)"
    assert len(hourly) == 3
    assert len(actual) == 5


def test_unit_conversion_and_jst_to_utc():
    assert jp_unit_to_mw(3839) == 38390.0
    utc_value, local_value = jst_to_rfc3339("2026-05-21", "0:05")
    assert utc_value == "2026-05-20T15:05:00Z"
    assert local_value == "2026-05-21T00:05:00+09:00"


def test_parse_csv_covers_all_sections_and_zero_pads_times(shift_jis_fixture):
    parsed = parse_denkiyoho_csv(decode_shift_jis_csv(shift_jis_fixture.read_bytes()))

    assert parsed.supply_capacity.time == SUPPLY_CAPACITY_TIME_SENTINEL
    assert parsed.supply_capacity.peak_supply_capacity_jp_unit_value == 3839
    assert parsed.supply_capacity.peak_supply_capacity_mw == 38390.0
    assert parsed.supply_capacity.peak_time_slot == "13:00-14:00"
    assert parsed.supply_capacity.peak_reserve_margin_pct == 14.0
    assert parsed.supply_capacity.peak_usage_pct == 87.0
    assert parsed.supply_capacity.daily_max_usage_pct == 88.0
    assert parsed.supply_capacity.daily_max_usage_time_slot == "4:00-5:00"
    assert parsed.supply_capacity.update_datetime == "2026-05-20T21:10:00Z"

    assert parsed.peak_demand_forecast.time == PEAK_FORECAST_TIME_SENTINEL
    assert parsed.peak_demand_forecast.peak_demand_forecast_jp_unit_value == 3363
    assert parsed.peak_demand_forecast.peak_demand_forecast_mw == 33630.0
    assert parsed.peak_demand_forecast.peak_time_slot == "13:00-14:00"
    assert parsed.peak_demand_forecast.update_datetime_local == "2026-05-21T06:10:00+09:00"

    assert [actual.time for actual in parsed.actuals] == ["00:00", "01:00", "00:00", "00:10", "00:15"]
    hourly_actual = parsed.actuals[0]
    assert hourly_actual.usage_pct == 86.0
    assert hourly_actual.supply_capacity_jp_unit_value == 2866
    assert hourly_actual.supply_capacity_mw == 28660.0
    assert hourly_actual.solar_generation_mw is None

    five_min_actual = parsed.actuals[2]
    assert five_min_actual.solar_generation_jp_unit_value == 0
    assert five_min_actual.solar_generation_mw == 0.0
    assert five_min_actual.solar_share_pct == 0.0
    assert five_min_actual.usage_pct is None
    assert five_min_actual.supply_capacity_mw is None

    blank_solar_actual = parsed.actuals[-1]
    assert blank_solar_actual.time == "00:15"
    assert blank_solar_actual.solar_generation_jp_unit_value is None
    assert blank_solar_actual.solar_generation_mw is None
    assert blank_solar_actual.solar_share_pct is None

    assert [forecast.forecast_demand_jp_unit_value for forecast in parsed.forecasts] == [2447, 2330]
    assert parsed.forecasts[0].usage_pct == 86.0
    assert parsed.forecasts[0].supply_capacity_jp_unit_value == 2866


def test_poll_once_emits_and_deduplicates_per_type(shift_jis_fixture):
    api = StubAPI(shift_jis_fixture.read_bytes())
    producer = FakeEventProducer()
    state = DenkiyohoState()

    state = api.poll_once(producer, state)
    assert [event_type for event_type, _ in producer.events] == [
        "supply",
        "peak_forecast",
        "actual",
        "actual",
        "actual",
        "actual",
        "actual",
        "forecast",
        "forecast",
    ]
    assert len(state.supply_capacity_seen) == 1
    assert len(state.peak_forecast_seen) == 1
    assert len(state.actual_seen) == 5
    assert len(state.forecast_seen) == 2

    supply_event = producer.events[0][1]
    assert supply_event["_time"] == SUPPLY_CAPACITY_TIME_SENTINEL
    assert supply_event["data"].daily_max_usage_pct == 88.0
    peak_event = producer.events[1][1]
    assert peak_event["_time"] == PEAK_FORECAST_TIME_SENTINEL
    assert peak_event["data"].peak_demand_forecast_jp_unit_value == 3363
    five_min_actual_event = producer.events[4][1]
    assert five_min_actual_event["_time"] == "00:00"
    assert five_min_actual_event["data"].solar_generation_jp_unit_value == 0
    assert five_min_actual_event["data"].solar_generation_mw == 0.0
    assert five_min_actual_event["data"].solar_share_pct == 0.0

    producer.events.clear()
    state = api.poll_once(producer, state)
    assert producer.events == []


def test_forecast_reissued_with_new_value_reemits(shift_jis_fixture):
    api = StubAPI(shift_jis_fixture.read_bytes())
    state = api.poll_once(FakeEventProducer(), DenkiyohoState())
    changed = SAMPLE_TEXT.replace("2026/5/21,1:00,2363,2330,85,2765", "2026/5/21,1:00,2363,2400,85,2765")
    producer = FakeEventProducer()

    new_state = StubAPI(changed.encode("cp932")).poll_once(producer, state)
    assert [event_type for event_type, _ in producer.events] == ["forecast"]
    assert len(new_state.forecast_seen) == 3


def test_flush_failure_does_not_advance_state(shift_jis_fixture):
    api = StubAPI(shift_jis_fixture.read_bytes())
    state = DenkiyohoState()
    with pytest.raises(RuntimeError):
        api.poll_once(FakeEventProducer(flush_remaining=1), state)
    assert state.to_dict() == {"supply_capacity_seen": [], "peak_forecast_seen": [], "actual_seen": [], "forecast_seen": []}


def test_state_caps_dedup_sets():
    state = DenkiyohoState(actual_seen=[f"old-{i}" for i in range(2000)])
    parsed = parse_denkiyoho_csv(SAMPLE_TEXT)
    state.mark_actual(parsed.actuals[0])
    assert len(state.actual_seen) == 2000
    assert "old-0" not in state.actual_seen
    assert actual_key(parsed.actuals[0]) in state.actual_seen


def test_parse_error_is_explicit_and_state_unchanged():
    state = DenkiyohoState(forecast_seen=["existing"])
    with pytest.raises(ValueError):
        StubAPI("not a tepco csv".encode("cp932")).poll_once(FakeEventProducer(), state)
    assert state.forecast_seen == ["existing"]


def test_forecast_key_includes_value_and_hourly_context(shift_jis_fixture):
    forecast = parse_denkiyoho_csv(decode_shift_jis_csv(shift_jis_fixture.read_bytes())).forecasts[0]
    assert forecast_key(forecast) == "2026-05-21|00:00|2447|86.0|2866"
