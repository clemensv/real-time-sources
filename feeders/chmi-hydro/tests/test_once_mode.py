"""Verify the --once flag causes main() to exit after one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import chmi_hydro.chmi_hydro as bridge


SAMPLE_META_PAYLOAD = {
    "data": {
        "data": {
            "header": (
                "objID,DBC,STATION_NAME,STREAM_NAME,GEOGR1,GEOGR2,"
                "SPA_TYP,SPAH_DS,SPAH_UNIT,DRYH,SPA1H,SPA2H,SPA3H,SPA4H,"
                "SPAQ_DS,SPAQ_UNIT,DRYQ,SPA1Q,SPA2Q,SPA3Q,SPA4Q,ISFORECAST"
            ),
            "values": [
                [
                    "0-203-1-001000", "001000", "Test", "TestStream",
                    50.0, 15.0,
                    "H", "vodní stav", "CM", 88,
                    165, 200, 220, 297,
                    "průtok", "M3_S", 0.419,
                    19.3, 39.4, 54.5, 137,
                    0,
                ],
            ],
        }
    }
}

SAMPLE_STATION_DATA = {
    "objList": [{
        "objID": "0-203-1-001000",
        "tsList": [
            {
                "tsConID": "H",
                "tsData": [{"dt": "2024-01-01T00:00:00Z", "value": 100}],
            }
        ],
    }]
}


def _fake_get(url, *args, **kwargs):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    if "meta1.json" in url:
        resp.json.return_value = SAMPLE_META_PAYLOAD
    elif url.rstrip("/").endswith("/data"):
        resp.text = '<a href="0-203-1-001000.json">0-203-1-001000.json</a>'
    else:
        resp.json.return_value = SAMPLE_STATION_DATA
    return resp


def test_once_flag_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "chmi-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--topic", "chmi-hydro",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "feed",
        "--once",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    with patch.object(bridge, "Producer") as ProducerCls, \
         patch("chmi_hydro.chmi_hydro.requests.Session") as SessionCls, \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProducerCls.return_value = MagicMock()
        session_instance = MagicMock()
        session_instance.get.side_effect = _fake_get
        SessionCls.return_value = session_instance
        bridge.main()

    sleep_mock.assert_not_called()


def test_once_via_env_var_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "chmi-hydro",
        "--connection-string", "BootstrapServer=localhost:9092",
        "--topic", "chmi-hydro",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "feed",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    sleep_mock = MagicMock()
    with patch.object(bridge, "Producer") as ProducerCls, \
         patch("chmi_hydro.chmi_hydro.requests.Session") as SessionCls, \
         patch.object(bridge.time, "sleep", sleep_mock):
        ProducerCls.return_value = MagicMock()
        session_instance = MagicMock()
        session_instance.get.side_effect = _fake_get
        SessionCls.return_value = session_instance
        bridge.main()

    sleep_mock.assert_not_called()
