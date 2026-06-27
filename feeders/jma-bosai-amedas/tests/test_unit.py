"""Unit tests for the JMA Bosai AMeDAS bridge; no live JMA endpoints are called."""

from datetime import datetime, timezone, timedelta

import pytest

from jma_bosai_amedas.jma_bosai_amedas import (
    JmaBosaiAmedasAPI,
    LATEST_TIME_URL,
    STATION_TABLE_URL,
    decimal_degrees,
    enabled_measurements,
    parse_connection_string,
    parse_observation,
    parse_point_station_codes,
    parse_station,
    point_detail_time_to_utc,
    point_file_time,
)


class FakeResponse:
    def __init__(self, status_code=200, text=""):
        self.status_code = status_code
        self.text = text


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []

    def get(self, url, timeout=20):
        self.requests.append((url, timeout))
        return self.responses.pop(0)


class FakeEventProducer:
    def __init__(self):
        self.observations = []
        self.stations = []

    def send_jp_jma_amedas_station(self, **kwargs):
        self.stations.append(kwargs)

    def send_jp_jma_amedas_observation(self, **kwargs):
        self.observations.append(kwargs)


class FakeKafkaProducer:
    def __init__(self, flush_result=0):
        self.flush_result = flush_result
        self.flush_calls = 0

    def flush(self, timeout=60):
        self.flush_calls += 1
        return self.flush_result


@pytest.mark.unit
class TestConnectionStringParsing:
    def test_parse_event_hubs_connection_string(self):
        connection_string = (
            "Endpoint=sb://mynamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=abc123==;"
            "EntityPath=myeventhub"
        )
        result = parse_connection_string(connection_string)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myeventhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == connection_string
        assert result["security.protocol"] == "SASL_SSL"

    def test_parse_local_kafka_connection_string(self):
        result = parse_connection_string("BootstrapServer=localhost:9092;EntityPath=jma-bosai-amedas")
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "jma-bosai-amedas"
        assert "sasl.username" not in result

    def test_parse_invalid_connection_string_raises(self):
        with pytest.raises(ValueError, match="Invalid connection string format"):
            parse_connection_string("EndpointWithoutEquals;EntityPathAlsoInvalid")


@pytest.mark.unit
class TestParsingHelpers:
    def test_decimal_degree_conversion(self):
        assert decimal_degrees([43, 3.9]) == pytest.approx(43.065)
        assert decimal_degrees([141, 18.9]) == pytest.approx(141.315)
        assert decimal_degrees(None) is None

    def test_enabled_measurements_from_elems_bitmask(self):
        assert enabled_measurements("11112010") == [
            "precipitation",
            "wind",
            "temperature",
            "sunshine_duration",
            "snow_depth",
            "pressure",
        ]

    def test_station_parsing_from_fixture(self):
        station = parse_station(
            "11016",
            {
                "type": "A",
                "elems": "11111111",
                "lat": [45, 24.9],
                "lon": [141, 40.7],
                "alt": 3,
                "kjName": "稚内",
                "knName": "ワッカナイ",
                "enName": "Wakkanai",
            },
        )
        assert station.station_code == "11016"
        assert station.kj_name == "稚内"
        assert station.kana == "ワッカナイ"
        assert station.en_name == "Wakkanai"
        assert station.latitude == pytest.approx(45.415)
        assert station.longitude == pytest.approx(141.678333333)
        assert station.altitude_m == 3.0
        assert station.station_type == "A"
        assert "humidity" in station.enabled_measurements

    def test_observation_parsing_from_fixture(self):
        observed_at = datetime(2026, 5, 21, 5, 50, tzinfo=timezone(timedelta(hours=9)))
        observation = parse_observation(
            "11016",
            {
                "temp": [14.5, 0],
                "humidity": [80, 0],
                "wind": [4.5, 3, 0],
                "precipitation1h": [0.0, 0],
                "pressure": [1011.8, 0],
                "normalPressure": [1013.2, 0],
                "visibility": [18950.0, 0],
            },
            observed_at,
        )
        assert observation is not None
        assert observation.station_code == "11016"
        assert observation.observed_at == datetime(2026, 5, 20, 20, 50, tzinfo=timezone.utc)
        assert observation.observed_at_local == observed_at
        assert observation.temp == 14.5
        assert observation.temp_qc_flag == 0
        assert observation.precipitation1h == 0.0
        assert observation.precipitation1h_qc_flag == 0
        assert observation.wind_speed == 4.5
        assert observation.wind_direction == pytest.approx(67.5)

    def test_point_detail_time_rolls_back_when_clock_is_after_observation(self):
        observed_at = datetime(2026, 5, 21, 7, 0, tzinfo=timezone(timedelta(hours=9)))
        assert point_detail_time_to_utc(observed_at, {"hour": 21, "minute": 3}) == "2026-05-20T12:03:00Z"
        assert point_file_time(observed_at).hour == 6
        assert parse_point_station_codes("11016, 44132") == {"11016", "44132"}

    def test_observation_parsing_with_point_detail_fields(self):
        observed_at = datetime(2026, 5, 21, 7, 0, tzinfo=timezone(timedelta(hours=9)))
        observation = parse_observation(
            "11016",
            {
                "wind": [4.9, 0],
                "windDirection": [3, 0],
                "gust": [9.3, 0],
                "gustDirection": [4, 0],
                "gustTime": {"hour": 21, "minute": 3},
                "maxTemp": [9.5, 0],
                "maxTempTime": {"hour": 15, "minute": 29},
                "minTemp": [7.8, 0],
                "minTempTime": {"hour": 6, "minute": 12},
            },
            observed_at,
        )
        assert observation is not None
        assert observation.wind_speed == 4.9
        assert observation.wind_direction == pytest.approx(67.5)
        assert observation.wind_gust == 9.3
        assert observation.wind_gust_qc_flag == 0
        assert observation.wind_gust_direction == pytest.approx(90.0)
        assert observation.wind_gust_time == "2026-05-20T12:03:00Z"
        assert observation.max_temp == 9.5
        assert observation.max_temp_time == "2026-05-20T06:29:00Z"
        assert observation.min_temp == 7.8
        assert observation.min_temp_time == "2026-05-20T21:12:00Z"


@pytest.mark.unit
class TestPollingAndResilience:
    def test_snapshot_dedup_skips_existing_snapshot(self, tmp_path):
        api = JmaBosaiAmedasAPI(FakeSession([FakeResponse(200, "2026-05-21T05:50:00+09:00")]))
        state = {"last_snapshot_time": "2026-05-21T05:50:00+09:00"}
        event_producer = FakeEventProducer()
        emitted = api.poll_once(event_producer, FakeKafkaProducer(), state, str(tmp_path / "state.json"))
        assert emitted == 0
        assert event_producer.observations == []

    def test_http_5xx_returns_none_and_skips(self):
        api = JmaBosaiAmedasAPI(FakeSession([FakeResponse(503, "service unavailable")]))
        assert api.fetch_latest_time() is None

    def test_malformed_json_returns_none_and_skips(self):
        api = JmaBosaiAmedasAPI(FakeSession([FakeResponse(200, "not-json")]))
        assert api.fetch_station_table() is None

    def test_reference_refresh_failure_keeps_cached_stations(self, tmp_path):
        api = JmaBosaiAmedasAPI(FakeSession([FakeResponse(500, "fail")]))
        cached = parse_station("11016", {"type": "A", "elems": "11111111", "lat": [45, 0], "lon": [141, 0], "alt": 3, "kjName": "稚内", "knName": "ワッカナイ", "enName": "Wakkanai"})
        api.stations = {"11016": cached}
        state = {}
        ok = api.emit_station_reference(FakeEventProducer(), FakeKafkaProducer(), state, str(tmp_path / "state.json"), datetime.now(timezone.utc))
        assert ok is False
        assert api.stations == {"11016": cached}
        assert state == {}

    def test_poll_once_emits_observations_and_advances_state_after_flush(self, tmp_path):
        latest = "2026-05-21T05:50:00+09:00"
        api = JmaBosaiAmedasAPI(
            FakeSession([
                FakeResponse(200, latest),
                FakeResponse(200, '{"11016":{"temp":[14.5,0],"precipitation1h":[0.0,0]}}'),
            ])
        )
        state = {}
        event_producer = FakeEventProducer()
        emitted = api.poll_once(event_producer, FakeKafkaProducer(), state, str(tmp_path / "state.json"))
        assert emitted == 1
        assert state["last_snapshot_time"] == latest
        assert event_producer.observations[0]["_station_code"] == "11016"

    def test_poll_once_enriches_configured_station_from_point_endpoint(self, tmp_path):
        latest = "2026-05-21T07:00:00+09:00"
        api = JmaBosaiAmedasAPI(
            FakeSession([
                FakeResponse(200, latest),
                FakeResponse(200, '{"11016":{"temp":[8.4,0]},"44132":{"temp":[12.1,0]}}'),
                FakeResponse(200, '{"20260521070000":{"gust":[9.3,0],"gustDirection":[4,0],"gustTime":{"hour":21,"minute":3},"maxTemp":[9.5,0],"maxTempTime":{"hour":15,"minute":29},"minTemp":[7.8,0],"minTempTime":{"hour":6,"minute":12}}}'),
            ]),
            point_station_codes={"11016"},
            point_request_delay=0,
        )
        event_producer = FakeEventProducer()
        emitted = api.poll_once(event_producer, FakeKafkaProducer(), {}, str(tmp_path / "state.json"))
        assert emitted == 2
        enriched = event_producer.observations[0]["data"]
        assert enriched.station_code == "11016"
        assert enriched.wind_gust == 9.3
        assert event_producer.observations[1]["data"].wind_gust is None
        assert api.session.requests[2][0].endswith("/data/point/11016/20260521_06.json")

    def test_flush_failure_does_not_advance_snapshot_state(self, tmp_path):
        latest = "2026-05-21T05:50:00+09:00"
        api = JmaBosaiAmedasAPI(
            FakeSession([
                FakeResponse(200, latest),
                FakeResponse(200, '{"11016":{"temp":[14.5,0]}}'),
            ])
        )
        state = {}
        emitted = api.poll_once(FakeEventProducer(), FakeKafkaProducer(flush_result=1), state, str(tmp_path / "state.json"))
        assert emitted == 0
        assert "last_snapshot_time" not in state
