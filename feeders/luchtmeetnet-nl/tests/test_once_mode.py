"""Verify that --once causes the bridge to exit after a single polling cycle."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from luchtmeetnet_nl.luchtmeetnet_nl import LuchtmeetnetAPI, ReferenceSnapshot, main


@pytest.mark.unit
def test_feed_once_mode_exits_after_single_cycle(monkeypatch):
    api = LuchtmeetnetAPI()

    snapshot = ReferenceSnapshot(stations=[], components=[])
    api.fetch_reference_snapshot = MagicMock(return_value=snapshot)  # type: ignore[method-assign]
    api.emit_reference_data = MagicMock()  # type: ignore[method-assign]
    api.emit_telemetry_once = MagicMock(return_value=(0, 0))  # type: ignore[method-assign]

    producer_mock = MagicMock()
    monkeypatch.setattr(
        "luchtmeetnet_nl.luchtmeetnet_nl.Producer",
        MagicMock(return_value=producer_mock),
    )
    monkeypatch.setattr(
        "luchtmeetnet_nl.luchtmeetnet_nl.NlRivmLuchtmeetnetEventProducer",
        MagicMock(),
    )
    monkeypatch.setattr(
        "luchtmeetnet_nl.luchtmeetnet_nl.NlRivmLuchtmeetnetComponentsEventProducer",
        MagicMock(),
    )

    sleep_mock = MagicMock()
    monkeypatch.setattr("luchtmeetnet_nl.luchtmeetnet_nl.time.sleep", sleep_mock)

    api.feed(
        kafka_config={"bootstrap.servers": "localhost:9092"},
        kafka_topic="luchtmeetnet-nl",
        polling_interval=1,
        state_file="",
        station_refresh_interval=24,
        station_limit=0,
        once=True,
    )

    assert api.emit_telemetry_once.call_count == 1
    sleep_mock.assert_not_called()


@pytest.mark.unit
def test_main_passes_once_flag(monkeypatch):
    feed_mock = MagicMock()
    monkeypatch.setattr(LuchtmeetnetAPI, "feed", feed_mock)
    monkeypatch.setenv("ONCE_MODE", "")
    monkeypatch.setattr(
        "sys.argv",
        [
            "luchtmeetnet_nl",
            "feed",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=luchtmeetnet-nl",
            "--once",
        ],
    )

    with patch("luchtmeetnet_nl.luchtmeetnet_nl.Producer"):
        main()

    assert feed_mock.call_args.kwargs["once"] is True
