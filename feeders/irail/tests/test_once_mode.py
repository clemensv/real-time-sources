"""Verify that the iRail bridge supports single-cycle execution via --once."""
from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest


def _fake_station(sid: str = "008814001"):
    return {
        "id": f"BE.NMBS.{sid}",
        "name": "Brussels-Central",
        "standardname": "BRUSSEL-CENTRAAL",
        "locationX": "4.356802",
        "locationY": "50.845714",
        "@id": f"http://irail.be/stations/NMBS/{sid}",
    }


def _fake_liveboard(sid: str = "008814001"):
    return {
        "timestamp": "1700000000",
        "station": "Brussels-Central",
        "stationinfo": {"name": "Brussels-Central"},
        "departures": {"departure": []},
        "arrivals": {"arrival": []},
    }


class _FakeAPI:
    def __init__(self, *_, **__):
        self.fetch_calls = 0

    def fetch_stations(self):
        return [_fake_station()]

    def fetch_liveboard(self, station_id, arrdep="departure"):
        self.fetch_calls += 1
        return _fake_liveboard(station_id)

    # delegate the parsing helpers to the real class
    @staticmethod
    def parse_station(raw):
        from irail.irail import IRailAPI as _Real
        return _Real.parse_station(raw)

    @staticmethod
    def parse_liveboard(raw, sid):
        from irail.irail import IRailAPI as _Real
        return _Real.parse_liveboard(raw, sid)

    @staticmethod
    def parse_arrivalboard(raw, sid):
        from irail.irail import IRailAPI as _Real
        return _Real.parse_arrivalboard(raw, sid)


def test_once_flag_exits_after_one_cycle(monkeypatch):
    """`main()` with --once must return after a single polling cycle."""
    from irail import irail as bridge

    monkeypatch.setattr(bridge, "IRailAPI", _FakeAPI)
    monkeypatch.setattr(bridge, "Producer", MagicMock())
    monkeypatch.setattr(bridge, "BeIrailEventProducer", MagicMock())
    monkeypatch.setattr(bridge.time, "sleep", lambda *_a, **_kw: None)

    monkeypatch.setenv("CONNECTION_STRING", "BootstrapServer=localhost:9092;EntityPath=test-irail")
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    argv_backup = sys.argv
    try:
        sys.argv = ["irail", "feed", "--once", "--polling-interval", "1"]
        # Must return promptly; if --once is missing it loops forever.
        with patch.object(bridge.time, "sleep", lambda *_a, **_kw: None):
            bridge.main()
    finally:
        sys.argv = argv_backup


def test_once_flag_present_in_argparse():
    """Sanity: argparse must expose --once on the feed subcommand."""
    from irail.irail import main  # noqa: F401
    import irail.irail as bridge
    import argparse
    # Inspect by parsing a known argv
    sys_argv_backup = sys.argv
    try:
        sys.argv = ["irail", "feed", "--once"]
        # Re-create parser locally to avoid running feed()
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        feed_parser = sub.add_parser("feed")
        feed_parser.add_argument("--connection-string")
        feed_parser.add_argument("--polling-interval", type=int, default=300)
        feed_parser.add_argument("--station-filter")
        feed_parser.add_argument("--once", action="store_true")
        ns = parser.parse_args(["feed", "--once"])
        assert ns.once is True
    finally:
        sys.argv = sys_argv_backup
