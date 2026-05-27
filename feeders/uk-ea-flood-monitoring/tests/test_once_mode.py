"""Verify the --once flag causes main() to exit after one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import uk_ea_flood_monitoring.uk_ea_flood_monitoring as bridge


SAMPLE_STATIONS = [
    {
        "@id": "http://environment.data.gov.uk/flood-monitoring/id/stations/1029TH",
        "stationReference": "1029TH",
        "notation": "1029TH",
        "label": "Kingston",
        "riverName": "Thames",
        "catchmentName": "Thames",
        "town": "Kingston",
        "lat": 51.41,
        "long": -0.30,
        "status": "Active",
        "dateOpened": "1900-01-01",
        "measures": [
            {"@id": "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD"}
        ],
    }
]

SAMPLE_READINGS = [
    {
        "measure": "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD",
        "dateTime": "2025-01-01T00:00:00Z",
        "value": 1.23,
    }
]


def _fake_get(url, *args, **kwargs):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    if "stations" in url:
        resp.json.return_value = {"items": SAMPLE_STATIONS}
    else:
        resp.json.return_value = {"items": SAMPLE_READINGS}
    return resp


def test_once_flag_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "uk-ea-flood-monitoring",
        "feed",
        "--kafka-bootstrap-servers", "localhost:9092",
        "--kafka-topic", "uk-ea-flood-monitoring",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "--once",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    fake_producer_module = MagicMock()
    fake_producer_module.Producer = MagicMock(return_value=MagicMock())
    with patch.dict(sys.modules, {"confluent_kafka": fake_producer_module}), \
         patch.object(bridge.requests.Session, "get", side_effect=_fake_get), \
         patch.object(bridge, "UKGovEnvironmentEAFloodMonitoringEventProducer") as ProdCls, \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProdCls.return_value = MagicMock()
        bridge.main()

    sleep_mock.assert_not_called()


def test_once_via_env_var_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "uk-ea-flood-monitoring",
        "feed",
        "--kafka-bootstrap-servers", "localhost:9092",
        "--kafka-topic", "uk-ea-flood-monitoring",
        "--state-file", str(state_file),
        "--polling-interval", "1",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    fake_producer_module = MagicMock()
    fake_producer_module.Producer = MagicMock(return_value=MagicMock())
    with patch.dict(sys.modules, {"confluent_kafka": fake_producer_module}), \
         patch.object(bridge.requests.Session, "get", side_effect=_fake_get), \
         patch.object(bridge, "UKGovEnvironmentEAFloodMonitoringEventProducer") as ProdCls, \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProdCls.return_value = MagicMock()
        bridge.main()

    sleep_mock.assert_not_called()
