"""Verify the --once flag causes main() to exit after one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import hubeau_hydrometrie.hubeau_hydrometrie as bridge


SAMPLE_STATIONS = {
    "data": [
        {
            "code_station": "A123456789",
            "libelle_station": "Test Station",
            "code_site": "A1234567",
            "longitude_station": 2.0,
            "latitude_station": 48.0,
            "libelle_cours_eau": "Seine",
            "libelle_commune": "Paris",
            "code_departement": "75",
            "en_service": True,
            "date_ouverture_station": "2000-01-01",
        }
    ],
    "next": None,
}

SAMPLE_OBSERVATIONS = {
    "data": [
        {
            "code_station": "A123456789",
            "date_obs": "2024-01-01T00:00:00Z",
            "grandeur_hydro": "H",
            "resultat_obs": 100.0,
            "libelle_methode_obs": "Mesure",
            "libelle_qualification_obs": "Bonne",
        }
    ],
    "next": None,
}


def _fake_session_get(self, url, *args, **kwargs):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    if "stations" in url:
        resp.json.return_value = SAMPLE_STATIONS
    else:
        resp.json.return_value = SAMPLE_OBSERVATIONS
    return resp


def _run_main(monkeypatch, argv, extra_env=None):
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    for k, v in (extra_env or {}).items():
        monkeypatch.setenv(k, v)

    sleep_mock = MagicMock()
    fake_producer = MagicMock()
    with patch("confluent_kafka.Producer", return_value=fake_producer), \
         patch.object(bridge.requests.Session, "get", _fake_session_get), \
         patch.object(bridge.time, "sleep", sleep_mock):
        bridge.main()
    return sleep_mock


def test_once_flag_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "hubeau-hydrometrie",
        "feed",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--state-file", str(state_file),
        "--polling-interval", "1",
        "--once",
    ]
    sleep_mock = _run_main(monkeypatch, argv)
    # The single-cycle exit must skip the inter-cycle sleep.
    sleep_mock.assert_not_called()


def test_once_via_env_var_exits_after_one_cycle(tmp_path, monkeypatch):
    state_file = tmp_path / "state.json"
    argv = [
        "hubeau-hydrometrie",
        "feed",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--state-file", str(state_file),
        "--polling-interval", "1",
    ]
    sleep_mock = _run_main(monkeypatch, argv, extra_env={"ONCE_MODE": "true"})
    sleep_mock.assert_not_called()
