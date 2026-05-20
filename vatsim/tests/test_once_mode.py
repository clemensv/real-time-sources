"""Tests for --once single-cycle execution mode (Fabric notebook hosting)."""

import os
import sys
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from vatsim.vatsim import VatsimBridge, main


SAMPLE_DATA = {
    "general": {
        "version": 3,
        "update_timestamp": "2026-05-17T07:48:40.5031859Z",
        "connected_clients": 2,
        "unique_users": 2,
    },
    "pilots": [
        {
            "cid": 1,
            "callsign": "AAL1",
            "latitude": 1.0,
            "longitude": 2.0,
            "altitude": 30000,
            "groundspeed": 400,
            "heading": 90,
            "transponder": "1200",
            "qnh_mb": 1013,
            "pilot_rating": 1,
            "last_updated": "2026-05-17T07:48:40Z",
            "flight_plan": None,
        }
    ],
    "controllers": [
        {
            "cid": 2,
            "callsign": "KLAX_TWR",
            "frequency": "120.950",
            "facility": 4,
            "rating": 3,
            "text_atis": ["Hello"],
            "last_updated": "2026-05-17T07:48:40Z",
        }
    ],
}


@pytest.mark.unit
def test_feed_once_mode_exits_after_one_cycle():
    """When once=True, feed() must return after a single polling cycle."""
    bridge = VatsimBridge()
    bridge.fetch_data = MagicMock(return_value=SAMPLE_DATA)

    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = os.path.join(tmpdir, 'state.json')
        with patch('vatsim.vatsim.Producer') as MockProducer, \
             patch('vatsim.vatsim.NetVatsimPilotsEventProducer'), \
             patch('vatsim.vatsim.NetVatsimControllersEventProducer'), \
             patch('vatsim.vatsim.NetVatsimStatusEventProducer'), \
             patch('vatsim.vatsim.time.sleep') as mock_sleep:
            MockProducer.return_value = MagicMock()

            bridge.feed(
                kafka_config={'bootstrap.servers': 'localhost:9092'},
                kafka_topic='test',
                polling_interval=60,
                state_file=state_file,
                once=True,
            )

        # Single cycle: exactly one upstream fetch, no sleeping between cycles.
        assert bridge.fetch_data.call_count == 1
        mock_sleep.assert_not_called()
        assert os.path.exists(state_file)


@pytest.mark.unit
def test_once_flag_via_cli_argument(monkeypatch):
    """`--once` CLI flag must propagate into bridge.feed(once=True)."""
    captured = {}

    def fake_feed(self, kafka_config, kafka_topic, polling_interval, state_file='', once=False):
        captured['once'] = once
        captured['topic'] = kafka_topic

    monkeypatch.setattr(VatsimBridge, 'feed', fake_feed)
    monkeypatch.setattr(sys, 'argv', [
        'vatsim', 'feed',
        '--kafka-bootstrap-servers', 'localhost:9092',
        '--kafka-topic', 'test',
        '--once',
    ])
    monkeypatch.delenv('CONNECTION_STRING', raising=False)
    monkeypatch.delenv('ONCE_MODE', raising=False)

    main()
    assert captured == {'once': True, 'topic': 'test'}


@pytest.mark.unit
def test_once_flag_via_env_var(monkeypatch):
    """ONCE_MODE env var must set the --once default to True."""
    captured = {}

    def fake_feed(self, kafka_config, kafka_topic, polling_interval, state_file='', once=False):
        captured['once'] = once

    monkeypatch.setattr(VatsimBridge, 'feed', fake_feed)
    monkeypatch.setenv('ONCE_MODE', 'true')
    monkeypatch.setattr(sys, 'argv', [
        'vatsim', 'feed',
        '--kafka-bootstrap-servers', 'localhost:9092',
        '--kafka-topic', 'test',
    ])
    monkeypatch.delenv('CONNECTION_STRING', raising=False)

    main()
    assert captured == {'once': True}
