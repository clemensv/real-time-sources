"""Test that --once causes main() to exit after exactly one polling cycle."""

import sys
from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture
def fake_api_and_producer():
    """Patch external dependencies so main() can run without network or Kafka."""
    with patch('nve_hydro.nve_hydro.NVEHydroAPI') as api_cls, \
         patch('nve_hydro.nve_hydro.Producer') as producer_cls, \
         patch('nve_hydro.nve_hydro.NONVEHydrologyEventProducer') as nve_prod_cls, \
         patch('nve_hydro.nve_hydro.send_stations', return_value={}) as send_st, \
         patch('nve_hydro.nve_hydro.feed_observations', return_value=0) as feed_obs, \
         patch('nve_hydro.nve_hydro._load_state', return_value={}), \
         patch('nve_hydro.nve_hydro._save_state'), \
         patch('nve_hydro.nve_hydro.time.sleep') as sleep_mock:
        api_cls.return_value = MagicMock()
        producer_cls.return_value = MagicMock()
        nve_prod_cls.return_value = MagicMock()
        yield {
            'sleep': sleep_mock,
            'feed_observations': feed_obs,
            'send_stations': send_st,
        }


def test_once_flag_exits_after_one_cycle(fake_api_and_producer, monkeypatch):
    """--once must cause main() to return without ever calling time.sleep."""
    monkeypatch.setenv('NVE_API_KEY', 'test-key')
    monkeypatch.setenv('KAFKA_BROKER', 'localhost:9092')
    monkeypatch.setenv('KAFKA_TOPIC', 'test-nve-hydro')
    monkeypatch.delenv('CONNECTION_STRING', raising=False)
    monkeypatch.delenv('KAFKA_CONNECTION_STRING', raising=False)
    monkeypatch.delenv('ONCE_MODE', raising=False)

    from nve_hydro.nve_hydro import main

    with patch.object(sys, 'argv', ['nve-hydro', '--once', 'feed']):
        main()

    assert fake_api_and_producer['send_stations'].call_count == 1
    assert fake_api_and_producer['feed_observations'].call_count == 1
    # --once must skip the sleep that gates the next polling cycle
    assert fake_api_and_producer['sleep'].call_count == 0


def test_once_mode_env_var_exits_after_one_cycle(fake_api_and_producer, monkeypatch):
    """ONCE_MODE env var must also cause main() to exit after one cycle."""
    monkeypatch.setenv('NVE_API_KEY', 'test-key')
    monkeypatch.setenv('KAFKA_BROKER', 'localhost:9092')
    monkeypatch.setenv('KAFKA_TOPIC', 'test-nve-hydro')
    monkeypatch.setenv('ONCE_MODE', 'true')
    monkeypatch.delenv('CONNECTION_STRING', raising=False)
    monkeypatch.delenv('KAFKA_CONNECTION_STRING', raising=False)

    from nve_hydro.nve_hydro import main

    with patch.object(sys, 'argv', ['nve-hydro', 'feed']):
        main()

    assert fake_api_and_producer['feed_observations'].call_count == 1
    assert fake_api_and_producer['sleep'].call_count == 0
