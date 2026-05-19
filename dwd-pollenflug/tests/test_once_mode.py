"""Tests for the --once / ONCE_MODE single-cycle execution path.

Used by the Fabric notebook host, which invokes the bridge once per
scheduled run instead of running an in-process polling loop.
"""

import json
import sys
from unittest.mock import patch, MagicMock

import pytest


SAMPLE_RESPONSE = {
    "last_update": "2025-04-08 11:00 Uhr",
    "next_update": "2025-04-09 11:00 Uhr",
    "sender": "Deutscher Wetterdienst - Medizin-Meteorologie",
    "content": [
        {
            "region_id": 10,
            "region_name": "Schleswig-Holstein und Hamburg",
            "partregion_id": 11,
            "partregion_name": "Inseln und Marschen",
            "Pollen": {
                "Hasel": {"today": "0", "tomorrow": "0", "dayafter_to": "0"},
            },
        },
    ],
}


def _patched_main_returns(argv, env=None):
    """Invoke main() with the given argv/env and a fully mocked stack.

    The polling loop must exit after exactly one cycle. The test fails
    fast (via the time.sleep mock raising) if the loop iterates again.
    """
    env = env or {}

    def _fake_sleep(_seconds):
        raise AssertionError("Polling loop should not sleep when --once is set")

    fake_response = MagicMock()
    fake_response.json.return_value = SAMPLE_RESPONSE
    fake_response.raise_for_status.return_value = None

    fake_producer_cls = MagicMock()
    fake_kafka_producer_cls = MagicMock()

    with patch.dict(sys.modules, {
        "confluent_kafka": MagicMock(Producer=fake_kafka_producer_cls),
    }), patch.dict("os.environ", env, clear=False), \
         patch("dwd_pollenflug.dwd_pollenflug.requests.get", return_value=fake_response), \
         patch("dwd_pollenflug.dwd_pollenflug.DEDWDPollenflugEventProducer", fake_producer_cls), \
         patch("dwd_pollenflug.dwd_pollenflug.time.sleep", side_effect=_fake_sleep), \
         patch.object(sys, "argv", argv):
        from dwd_pollenflug.dwd_pollenflug import main
        main()


def test_once_flag_exits_after_one_cycle(tmp_path):
    state_file = tmp_path / "state.json"
    argv = [
        "dwd-pollenflug",
        "--once",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--last-polled-file", str(state_file),
    ]
    # Disable TLS so the bridge does not try to configure SSL.
    _patched_main_returns(argv, env={"KAFKA_ENABLE_TLS": "false"})
    # State must have been persisted on the single cycle.
    assert state_file.exists()
    persisted = json.loads(state_file.read_text())
    assert persisted.get("last_update") == SAMPLE_RESPONSE["last_update"]


def test_once_mode_env_var_exits_after_one_cycle(tmp_path):
    state_file = tmp_path / "state.json"
    argv = [
        "dwd-pollenflug",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=test-topic",
        "--last-polled-file", str(state_file),
    ]
    _patched_main_returns(argv, env={"KAFKA_ENABLE_TLS": "false", "ONCE_MODE": "true"})
    assert state_file.exists()
