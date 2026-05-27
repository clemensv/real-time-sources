"""Test that the bridge exits after a single polling cycle in --once mode."""

from __future__ import annotations

import gzip
from unittest.mock import MagicMock, patch

import pytest

from wikimedia_osm_diffs.wikimedia_osm_diffs import (
    OsmDiffsBridge,
    StateStore,
    build_parser,
    main,
)


SAMPLE_STATE_TXT = (
    "#header\n"
    "sequenceNumber=7062480\n"
    "timestamp=2026-04-09T01\\:32\\:55Z\n"
)

SAMPLE_OSC_XML = (
    b"<?xml version='1.0' encoding='UTF-8'?>"
    b"<osmChange version='0.6'>"
    b"<create>"
    b"<node id='1' version='1' timestamp='2026-04-09T01:30:00Z' "
    b"uid='1' user='u' changeset='1' lat='0.0' lon='0.0'/>"
    b"</create>"
    b"</osmChange>"
)


def test_once_flag_parses() -> None:
    parser = build_parser()
    args = parser.parse_args(["feed", "--connection-string", "x", "--once"])
    assert args.once is True


def test_once_flag_default_false_without_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ONCE_MODE", raising=False)
    parser = build_parser()
    args = parser.parse_args(["feed", "--connection-string", "x"])
    assert args.once is False


def test_bridge_run_exits_after_one_cycle_when_once(tmp_path) -> None:
    """OsmDiffsBridge.run() must return after exactly one _poll_cycle when once=True."""
    diffs_producer = MagicMock()
    state_producer = MagicMock()
    kafka_producer = MagicMock()
    state_store = StateStore(str(tmp_path / "state.json"))

    bridge = OsmDiffsBridge(
        diffs_producer,
        state_producer,
        kafka_producer,
        state_store=state_store,
        poll_interval=60,
        once=True,
    )

    # Mock the HTTP session: state.txt then a single .osc.gz
    state_resp = MagicMock()
    state_resp.text = SAMPLE_STATE_TXT
    state_resp.raise_for_status = MagicMock()

    diff_resp = MagicMock()
    diff_resp.content = gzip.compress(SAMPLE_OSC_XML)
    diff_resp.raise_for_status = MagicMock()

    bridge._session = MagicMock()
    bridge._session.get = MagicMock(side_effect=[state_resp, diff_resp])

    with patch("wikimedia_osm_diffs.wikimedia_osm_diffs.time.sleep") as sleep_mock:
        bridge.run()

    # Run must return without ever calling time.sleep (sleep would mean looping)
    sleep_mock.assert_not_called()
    # Exactly one cycle: one state fetch + one diff fetch
    assert bridge._session.get.call_count == 2
    # State was advanced
    assert bridge._last_sequence == 7062480


def test_main_feed_once_returns(monkeypatch: pytest.MonkeyPatch) -> None:
    """End-to-end: `feed --once -c X` must invoke bridge.run() once and exit cleanly."""
    monkeypatch.setattr(
        "sys.argv",
        ["wikimedia-osm-diffs", "feed", "--connection-string",
         "BootstrapServer=localhost:9092;EntityPath=test", "--once"],
    )
    monkeypatch.setenv("KAFKA_ENABLE_TLS", "false")

    fake_bridge = MagicMock()
    fake_bridge_cls = MagicMock(return_value=fake_bridge)

    with patch("wikimedia_osm_diffs.wikimedia_osm_diffs.OsmDiffsBridge", fake_bridge_cls), \
         patch("wikimedia_osm_diffs.wikimedia_osm_diffs.Producer"):
        rc = main()

    assert rc == 0
    # Once flag forwarded to bridge constructor
    assert fake_bridge_cls.call_args.kwargs["once"] is True
    fake_bridge.run.assert_called_once()
    fake_bridge.flush.assert_called_once()
