import pytest

from jma_bosai_warning.jma_bosai_warning import (
    BridgeState,
    JmaBosaiWarningAPI,
    WARNING_OFFICE_CODES,
    jst_to_utc,
    parse_tsunami_alert,
    parse_weather_warning_payload,
    prefecture_for_office,
    status_to_severity,
)


class DictData(dict):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.__dict__.update(kwargs)


class FakeKafka:
    def __init__(self, flush_result=0):
        self.flush_result = flush_result
        self.flushes = 0

    def flush(self, timeout=None):
        self.flushes += 1
        return self.flush_result


class FakeProducer:
    def __init__(self):
        self.calls = []

    def send_jp_jma_warning_office(self, **kwargs):
        self.calls.append(("office", kwargs))

    def send_jp_jma_warning_weather_warning(self, **kwargs):
        self.calls.append(("weather", kwargs))

    def send_jp_jma_tsunami_tsunami_alert(self, **kwargs):
        self.calls.append(("tsunami", kwargs))


class FakeSession:
    def __init__(self, responses):
        self.responses = responses

    def get(self, url, timeout=20):
        value = self.responses[url]
        if isinstance(value, Exception):
            raise value
        return FakeResponse(value)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_prefecture_code_list_contains_jma_warning_offices():
    assert len(WARNING_OFFICE_CODES) == 58
    assert "011000" in WARNING_OFFICE_CODES
    assert "130000" in WARNING_OFFICE_CODES
    assert "270000" in WARNING_OFFICE_CODES
    assert "474000" in WARNING_OFFICE_CODES


def test_jst_to_utc_conversion():
    assert jst_to_utc("2026-05-21T04:02:00+09:00") == "2026-05-20T19:02:00Z"


def test_prefecture_for_office_uses_ascii_romanized_axis():
    assert prefecture_for_office("130000", "東京都") == "tokyo"
    assert prefecture_for_office("270000", "大阪府") == "osaka"
    assert prefecture_for_office("471000", "沖縄本島地方") == "okinawa"


@pytest.mark.parametrize(
    ("status", "code", "severity"),
    [("注意報", "10", "advisory"), ("警報", "03", "warning"), ("特別警報", "32", "emergency"), ("継続", "38", "emergency"), ("発表警報・注意報はなし", None, "advisory")],
)
def test_status_to_severity(status, code, severity):
    assert status_to_severity(status, code) == severity


def warning_fixture():
    return {
        "reportDatetime": "2026-05-21T04:02:00+09:00",
        "targetArea": "130000",
        "headlineText": "東京地方では急な強い雨や落雷に注意してください。",
        "timeSeries": [
            {
                "timeDefines": ["2026-05-21T04:00:00+09:00"],
                "areas": [
                    {"code": "1310100", "name": "東京地方", "warnings": [{"code": "10", "status": "注意報"}, {"code": "32", "status": "特別警報"}, {"status": "発表警報・注意報はなし"}]}
                ],
            }
        ],
    }


def test_warning_fixture_parsing():
    records = parse_weather_warning_payload("130000", warning_fixture())
    assert len(records) == 1
    record = records[0]
    assert record["prefecture"] == "tokyo"
    assert record["severity"] == "emergency"
    assert record["event"] == "warning"
    assert record["office_code"] == "130000"
    assert record["area_code"] == "1310100"
    assert record["report_datetime"] == "2026-05-20T19:02:00Z"
    assert record["time_defines"] == ["2026-05-20T19:00:00Z"]
    assert record["warnings"][0]["code_description_en"] == "Thunderstorm"
    assert record["warnings"][1]["severity"] == "emergency"
    assert record["warnings"][2]["code"] is None
    assert record["warnings"][2]["status"] == "NO_WARNINGS_OR_ADVISORIES"
    assert record["warnings"][2]["severity"] == "advisory"


def test_warning_live_shape_area_types_parsing():
    payload = {
        "reportDatetime": "2026-05-21T04:02:00+09:00",
        "timeSeries": [{"timeDefines": ["2026-05-21T04:00:00+09:00"], "areaTypes": [{"areas": [{"code": "130010", "warnings": [{"code": "14"}]}]}]}],
    }
    record = parse_weather_warning_payload("130000", payload, {"130010": "東京地方"})[0]
    assert record["area_name"] == "東京地方"
    assert record["warnings"][0]["status"] == "CONTINUED"


def tsunami_detail_fixture():
    return {
        "Head": {"EventID": "20260521000100", "Serial": "2"},
        "Body": {"Tsunami": {"Forecast": {"Item": [{"Area": {"Code": "100", "Name": "北海道太平洋沿岸東部"}, "Category": "津波警報", "MaxHeight": "3m", "FirstHeightArrivalTime": "2026-05-21T05:30:00+09:00"}]}}},
    }


def test_tsunami_fixture_parsing():
    entry = {"eid": "20260521000100", "ser": "2", "rdt": "2026-05-21T04:10:00+09:00", "ttl": "津波警報・注意報・予報", "ift": "発表", "json": "20260521041000_0_VTSE41_010000.json"}
    record = parse_tsunami_alert(entry, tsunami_detail_fixture())
    assert record["event_id"] == "20260521000100"
    assert record["serial"] == 2
    assert record["info_type"] == "ISSUED"
    assert record["report_datetime"] == "2026-05-20T19:10:00Z"
    assert record["bulletin_type"] == "VTSE41"
    assert record["affected_coastal_regions"][0]["expected_max_wave_height_m"] == 3.0
    assert record["affected_coastal_regions"][0]["category"] == "WARNING"
    assert record["observations"] == []


def test_tsunami_observation_fixture_parsing():
    entry = {"eid": "20260521000100", "ser": "3", "rdt": "2026-05-21T04:20:00+09:00", "ttl": "津波情報", "ift": "発表", "json": "20260521042000_0_VTSE51_010000.json"}
    detail = {
        "Head": {"EventID": "20260521000100", "Serial": "3"},
        "Body": {"Tsunami": {"Observation": {"Item": [{"Station": {"Code": "43101", "Name": "釧路"}, "MaxHeight": "0.4m", "MaxHeightArrivalTime": "2026-05-21T05:45:00+09:00"}]}}},
    }
    record = parse_tsunami_alert(entry, detail)
    assert record["observations"][0]["station_code"] == "43101"
    assert record["observations"][0]["observed_max_wave_height_m"] == 0.4
    assert record["observations"][0]["observed_at"] == "2026-05-20T20:45:00Z"
    assert record["observations"][0]["arrival_status"] == "MAX_WAVE_OBSERVED"


def test_weather_dedup_and_flush_success():
    api = JmaBosaiWarningAPI()
    api.fetch_warning_payload = lambda office: warning_fixture()
    state = BridgeState()
    producer = FakeProducer()
    count = api.emit_warning_cycle(producer, DictData, FakeKafka(), state, ["130000"])
    assert count == 1
    assert len(state.seen_weather) == 1
    assert api.emit_warning_cycle(producer, DictData, FakeKafka(), state, ["130000"]) == 0


def test_weather_flush_failure_does_not_advance_state():
    api = JmaBosaiWarningAPI()
    api.fetch_warning_payload = lambda office: warning_fixture()
    state = BridgeState()
    with pytest.raises(RuntimeError):
        api.emit_warning_cycle(FakeProducer(), DictData, FakeKafka(flush_result=1), state, ["130000"])
    assert state.seen_weather == []


def test_tsunami_dedup():
    api = JmaBosaiWarningAPI()
    api.fetch_tsunami_list = lambda: [{"eid": "20260521000100", "ser": "1", "rdt": "2026-05-21T04:10:00+09:00", "ttl": "津波情報", "ift": "発表", "json": "x_VTSE51.json"}]
    api.fetch_tsunami_detail = lambda filename: {}
    state = BridgeState()
    assert api.emit_tsunami_cycle(FakeProducer(), DictData, FakeKafka(), state) == 1
    assert api.emit_tsunami_cycle(FakeProducer(), DictData, FakeKafka(), state) == 0


def test_reference_refresh_failure_keeps_cached_catalog():
    api = JmaBosaiWarningAPI()
    api.area_catalog = {"offices": {"130000": {"name": "東京都", "enName": "Tokyo", "parent": "010300"}}}
    api.fetch_area_catalog = lambda: (_ for _ in ()).throw(RuntimeError("timeout"))
    assert api.refresh_area_catalog() is False
    office = api.office_records()[0]
    assert office["office_code"] == "130000"
    assert office["prefecture"] == "tokyo"
    assert office["severity"] == "info"
    assert office["event"] == "info"


def test_one_failed_office_does_not_abort_cycle():
    api = JmaBosaiWarningAPI()

    def fetch(office):
        if office == "011000":
            raise RuntimeError("connection reset")
        return warning_fixture()

    api.fetch_warning_payload = fetch
    state = BridgeState()
    count = api.emit_warning_cycle(FakeProducer(), DictData, FakeKafka(), state, ["011000", "130000"])
    assert count == 1
    assert len(state.seen_weather) == 1


