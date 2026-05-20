"""Verify the ``--once`` flag exits the polling loop after one cycle.

This guards the contract relied on by the Fabric notebook hosting option,
which runs ``kmi-belgium feed --once`` on a schedule and expects the
process to exit after a single polling cycle.
"""

from __future__ import annotations

import sys
from unittest.mock import patch

# Re-use the stubs configured in test_kmi_belgium so the bridge module imports.
from . import test_kmi_belgium  # noqa: F401

from kmi_belgium import kmi_belgium as bridge


def test_feed_once_exits_after_single_cycle():
    call_count = {"feed": 0, "sleep": 0}

    def fake_feed(api, producer, previous_readings):
        call_count["feed"] += 1
        return 0

    def fake_sleep(_seconds):
        call_count["sleep"] += 1
        raise AssertionError("time.sleep must not be called when --once is set")

    argv = [
        "kmi-belgium",
        "--connection-string", "BootstrapServer=localhost:9092;EntityPath=kmi-belgium",
        "--state-file", "/tmp/kmi-belgium-test-state.json",
        "feed", "--once",
    ]

    with patch.object(bridge, "Producer", lambda *a, **kw: object()), \
         patch.object(bridge, "BEGovKMIWeatherEventProducer", lambda *a, **kw: object()), \
         patch.object(bridge, "KMIBelgiumAPI", lambda *a, **kw: object()), \
         patch.object(bridge, "send_stations", lambda api, producer: None), \
         patch.object(bridge, "feed_observations", fake_feed), \
         patch.object(bridge, "_load_state", lambda path: {}), \
         patch.object(bridge, "_save_state", lambda path, state: None), \
         patch.object(bridge.time, "sleep", fake_sleep), \
         patch.object(sys, "argv", argv):
        bridge.main()

    assert call_count["feed"] == 1, f"expected exactly one feed cycle, got {call_count['feed']}"
    assert call_count["sleep"] == 0, "time.sleep must not run in --once mode"
