"""Tests that the bridge supports single-cycle execution via --once / ONCE_MODE.

These cover the contract required by the Fabric notebook scheduler: the
``poll_and_send`` loop must return after exactly one polling cycle when
``once=True``, and the ``main()`` argparse plumbing must accept the
``--once`` flag and the ``ONCE_MODE`` env var.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch


class OnceModeUnitTests(unittest.TestCase):
    def test_poll_and_send_once_returns_after_one_cycle(self):
        from eaws_albina.eaws_albina import AlbinaPoller

        with patch.object(AlbinaPoller, "__init__", lambda self, *a, **kw: None):
            poller = AlbinaPoller.__new__(AlbinaPoller)
            poller.regions = ["AT-07"]
            poller.lang = "en"
            poller.kafka_topic = "test"
            poller.emit_region_catalog = MagicMock(return_value=1)
            poller.fetch_and_send = MagicMock(return_value=0)

            with patch("eaws_albina.eaws_albina.time.sleep") as sleep_mock:
                poller.poll_and_send(once=True)

            sleep_mock.assert_not_called()
            # Today + yesterday => exactly 2 fetch_and_send calls in one cycle
            self.assertEqual(poller.fetch_and_send.call_count, 2)
            poller.emit_region_catalog.assert_called_once()

    def test_main_accepts_once_flag(self):
        from eaws_albina import eaws_albina as bridge

        captured = {}

        class _FakePoller:
            def __init__(self, **kwargs):
                captured["init"] = kwargs

            def poll_and_send(self, once=False):
                captured["once"] = once

        argv = [
            "eaws-albina",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=t",
            "--last-polled-file",
            os.devnull,
            "--once",
        ]
        with patch.object(sys, "argv", argv), \
             patch.object(bridge, "AlbinaPoller", _FakePoller):
            bridge.main()

        self.assertTrue(captured.get("once"))

    def test_main_honors_once_mode_env_var(self):
        from eaws_albina import eaws_albina as bridge

        captured = {}

        class _FakePoller:
            def __init__(self, **kwargs):
                pass

            def poll_and_send(self, once=False):
                captured["once"] = once

        argv = [
            "eaws-albina",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=t",
            "--last-polled-file",
            os.devnull,
        ]
        with patch.dict(os.environ, {"ONCE_MODE": "true"}, clear=False), \
             patch.object(sys, "argv", argv), \
             patch.object(bridge, "AlbinaPoller", _FakePoller):
            bridge.main()

        self.assertTrue(captured.get("once"))


if __name__ == "__main__":
    unittest.main()
