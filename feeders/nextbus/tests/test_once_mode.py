"""Tests for the NextBus one-shot notebook contract."""

import sys
from unittest.mock import MagicMock, patch

import nextbus.nextbus as bridge


def test_feed_once_exits_after_one_cycle(monkeypatch):
    feed_client = MagicMock()
    reference_client = MagicMock()

    fake_from_connection_string = MagicMock(side_effect=[feed_client, reference_client])
    monkeypatch.setattr(bridge.EventHubProducerClient, "from_connection_string", fake_from_connection_string)
    monkeypatch.setattr(bridge, "poll_and_submit_route_config", lambda *args, **kwargs: None)
    monkeypatch.setattr(bridge, "poll_and_submit_schedule", lambda *args, **kwargs: None)
    monkeypatch.setattr(bridge, "poll_and_submit_messages", lambda *args, **kwargs: None)
    monkeypatch.setattr(bridge, "poll_and_submit_vehicle_locations", lambda *args, **kwargs: 0.0)

    bridge.feed("feed-cs", "feed-hub", "ref-cs", "ref-hub", "sf-muni", "*", once=True)

    assert fake_from_connection_string.call_count == 2
    feed_client.close.assert_called_once_with()
    reference_client.close.assert_called_once_with()


def test_main_respects_once_mode_env_var(monkeypatch):
    captured = {}

    monkeypatch.setenv("FEED_CONNECTION_STRING", "Endpoint=sb://example.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc==;EntityPath=feed-hub")
    monkeypatch.setenv("FEED_EVENT_HUB_NAME", "feed-hub")
    monkeypatch.setenv("AGENCY", "sf-muni")
    monkeypatch.setenv("ONCE_MODE", "true")
    monkeypatch.setattr(sys, "argv", ["nextbus", "feed"])
    monkeypatch.setattr(bridge, "launch_feed", lambda args: captured.setdefault("args", args))

    bridge.main()

    assert captured["args"].once is True
