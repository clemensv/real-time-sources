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
    def test_once_flag_returns_after_one_cycle(self):
        from eaws_albina import eaws_albina as bridge

        fake_poller = MagicMock()
        fake_poller.get_region_catalog.return_value = []
        fake_poller.fetch_for_date.return_value = []
        argv = [
            "eaws-albina",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=t",
            "--last-polled-file",
            os.devnull,
            "--once",
        ]
        with patch.object(sys, "argv", argv), \
             patch.object(bridge, "AlbinaPoller", return_value=fake_poller), \
             patch.object(bridge, "KafkaProducer"), \
             patch.object(bridge, "OrgEAWSALBINABulletinsEventProducer"), \
             patch("eaws_albina.eaws_albina.time.sleep") as sleep_mock:
            bridge.main()

        sleep_mock.assert_not_called()
        self.assertEqual(fake_poller.fetch_for_date.call_count, 2)
        fake_poller.get_region_catalog.assert_called_once()

    def test_main_accepts_once_flag(self):
        from eaws_albina import eaws_albina as bridge

        captured = {}

        class _FakePoller:
            def __init__(self, **kwargs):
                captured["init"] = kwargs

            def get_region_catalog(self):
                return []

            def fetch_for_date(self, date_str):
                captured.setdefault("fetch_dates", []).append(date_str)
                return []

        argv = [
            "eaws-albina",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=t",
            "--last-polled-file",
            os.devnull,
            "--once",
        ]
        with patch.object(sys, "argv", argv), \
             patch.object(bridge, "AlbinaPoller", _FakePoller), \
             patch.object(bridge, "KafkaProducer"), \
             patch.object(bridge, "OrgEAWSALBINABulletinsEventProducer"), \
             patch("eaws_albina.eaws_albina.time.sleep") as sleep_mock:
            bridge.main()

        sleep_mock.assert_not_called()
        self.assertEqual(len(captured.get("fetch_dates", [])), 2)

    def test_main_honors_once_mode_env_var(self):
        from eaws_albina import eaws_albina as bridge

        captured = {}

        class _FakePoller:
            def __init__(self, **kwargs):
                pass

            def get_region_catalog(self):
                return []

            def fetch_for_date(self, date_str):
                captured.setdefault("fetch_dates", []).append(date_str)
                return []

        argv = [
            "eaws-albina",
            "--connection-string",
            "BootstrapServer=localhost:9092;EntityPath=t",
            "--last-polled-file",
            os.devnull,
        ]
        with patch.dict(os.environ, {"ONCE_MODE": "true"}, clear=False), \
             patch.object(sys, "argv", argv), \
             patch.object(bridge, "AlbinaPoller", _FakePoller), \
             patch.object(bridge, "KafkaProducer"), \
             patch.object(bridge, "OrgEAWSALBINABulletinsEventProducer"), \
             patch("eaws_albina.eaws_albina.time.sleep") as sleep_mock:
            bridge.main()

        sleep_mock.assert_not_called()
        self.assertEqual(len(captured.get("fetch_dates", [])), 2)


if __name__ == "__main__":
    unittest.main()
