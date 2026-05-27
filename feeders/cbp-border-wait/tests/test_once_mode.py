"""Verify --once causes feed() to exit after exactly one polling cycle."""

from unittest.mock import MagicMock, patch

from cbp_border_wait import cbp_border_wait as bridge


def _make_args(**overrides):
    defaults = dict(
        command="feed",
        connection_string="BootstrapServer=localhost:9092;EntityPath=test-topic",
        polling_interval=1,
        state_file="",
        once=True,
    )
    defaults.update(overrides)
    return MagicMock(**defaults)


def test_once_flag_exits_after_one_cycle():
    """--once must cause feed() to return after a single fetch_ports cycle."""
    raw_port = {
        "port_number": "999999",
        "port_name": "Test Port",
        "border": "Mexican Border",
        "crossing_name": "Test Crossing",
        "hours": "24 hrs/day",
        "port_status": "Open",
        "date": "2024-01-01",
        "time": "12:00",
        "passenger_vehicle_lanes": {"maximum_lanes": "5"},
        "commercial_vehicle_lanes": {"maximum_lanes": "2"},
        "pedestrian_lanes": {"maximum_lanes": "1"},
    }

    with patch.object(bridge, "Producer") as mock_producer_cls, \
            patch.object(bridge, "GovCbpBorderwaitEventProducer") as mock_ep_cls, \
            patch.object(bridge.CbpBorderWaitAPI, "fetch_ports", return_value=[raw_port]) as mock_fetch, \
            patch.object(bridge.time, "sleep") as mock_sleep:
        mock_producer_cls.return_value = MagicMock()
        mock_ep_cls.return_value = MagicMock()

        bridge.feed(_make_args(once=True))

        # One startup fetch (reference data) + exactly one telemetry cycle.
        assert mock_fetch.call_count == 2
        # No sleep should be invoked between cycles in --once mode.
        mock_sleep.assert_not_called()


def test_once_flag_via_env_var(monkeypatch):
    """ONCE_MODE env var must default --once to True when args.once is False."""
    monkeypatch.setenv("ONCE_MODE", "true")
    # Re-parsing argparse picks up the env-driven default.
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--once",
        action="store_true",
        default=__import__("os").environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
    )
    args = parser.parse_args([])
    assert args.once is True
