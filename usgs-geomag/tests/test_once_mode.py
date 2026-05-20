"""Tests for the --once CLI flag added for Fabric notebook hosting."""

from unittest.mock import patch, MagicMock

from usgs_geomag.usgs_geomag import main as bridge_main


def test_once_flag_runs_single_cycle(monkeypatch):
    """--once must cause main() to return after exactly one polling cycle."""
    monkeypatch.setenv(
        "CONNECTION_STRING",
        "BootstrapServer=localhost:9092;EntityPath=test-topic",
    )
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.setenv("ONCE_MODE", "")  # do not let env override the CLI flag's default
    monkeypatch.setattr("sys.argv", ["usgs-geomag", "--once"])

    poller_instance = MagicMock()

    with patch("usgs_geomag.usgs_geomag.USGSGeomagPoller", return_value=poller_instance) as poller_cls, \
         patch("usgs_geomag.usgs_geomag.Producer", create=True):
        bridge_main()

    poller_cls.assert_called_once()
    poller_instance.poll_and_send.assert_called_once_with(once=True)


def test_no_once_flag_runs_loop(monkeypatch):
    """Without --once (and ONCE_MODE unset), the bridge must request loop mode."""
    monkeypatch.setenv(
        "CONNECTION_STRING",
        "BootstrapServer=localhost:9092;EntityPath=test-topic",
    )
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.delenv("ONCE_MODE", raising=False)
    monkeypatch.setattr("sys.argv", ["usgs-geomag"])

    poller_instance = MagicMock()
    with patch("usgs_geomag.usgs_geomag.USGSGeomagPoller", return_value=poller_instance), \
         patch("usgs_geomag.usgs_geomag.Producer", create=True):
        bridge_main()

    poller_instance.poll_and_send.assert_called_once_with(once=False)


def test_once_mode_env_var_enables_once(monkeypatch):
    """ONCE_MODE=true env var must enable single-cycle execution."""
    monkeypatch.setenv(
        "CONNECTION_STRING",
        "BootstrapServer=localhost:9092;EntityPath=test-topic",
    )
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr("sys.argv", ["usgs-geomag"])

    poller_instance = MagicMock()
    with patch("usgs_geomag.usgs_geomag.USGSGeomagPoller", return_value=poller_instance), \
         patch("usgs_geomag.usgs_geomag.Producer", create=True):
        bridge_main()

    poller_instance.poll_and_send.assert_called_once_with(once=True)
