"""Lightweight sanity tests for pegelonline/fabric/wire_pegelonline_map.py.

We don't have a live Fabric Map item in CI, so these tests only validate the
in-process invariants of the wire script - that every layer name is unique,
every KQL body is non-empty, the geometry projection is present, and
``LAYER_NAMES`` matches the actual layers built by ``wire()``.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import types
import unittest
from unittest import mock

MOD_PATH = (pathlib.Path(__file__).resolve().parents[1]
            / "fabric" / "wire_pegelonline_map.py")


def _load_module() -> types.ModuleType:
    spec = importlib.util.spec_from_file_location("wire_pegelonline_map", MOD_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["wire_pegelonline_map"] = module
    spec.loader.exec_module(module)
    return module


class WirePegelonlineMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = _load_module()

    def test_layer_names_unique_and_complete(self) -> None:
        m = self.mod
        # Set must equal the six declared constants.
        self.assertEqual(
            m.LAYER_NAMES,
            {m.NAME_STATE, m.NAME_NAV, m.NAME_TREND,
             m.NAME_FRESH, m.NAME_LABELS, m.NAME_REPLAY},
        )
        # All layer names must share the common prefix used for the
        # idempotent drop-and-replace logic.
        for name in m.LAYER_NAMES:
            self.assertTrue(name.startswith(m.LAYER_PREFIX),
                            f"{name!r} missing prefix {m.LAYER_PREFIX!r}")

    def test_each_kql_body_well_formed(self) -> None:
        m = self.mod
        builders = {
            "state":      m._kql_state,
            "navigation": m._kql_navigation,
            "trend":      m._kql_trend,
            "freshness":  m._kql_freshness,
            "labels":     m._kql_labels,
            "replay":     m._kql_replay,
        }
        for layer_name, fn in builders.items():
            with self.subTest(layer=layer_name):
                body = fn()
                self.assertIn("geometry", body, "geometry alias missing")
                self.assertIn('bag_pack("type","Point"', body,
                              "point projection missing")
                self.assertIn("pack_array(longitude, latitude)", body,
                              "coordinates must be (lon, lat)")
                # Replay layer must declare the time-slider column;
                # everything else must not.
                if layer_name == "replay":
                    self.assertIn("Time (UTC, 15-min)", body)
                else:
                    self.assertNotIn("Time (UTC, 15-min)", body)

    def test_layer_builders_return_filters_list(self) -> None:
        m = self.mod
        layers = [
            m._layer_state(default_visible=True),
            m._layer_navigation(),
            m._layer_trend(),
            m._layer_freshness(),
            m._layer_labels(default_visible=True),
            m._layer_replay("2026-05-19 12:30 UTC"),
        ]
        for layer in layers:
            with self.subTest(name=layer["name"]):
                self.assertIn("filters", layer)
                self.assertIsInstance(layer["filters"], list)
                self.assertIn("options", layer)
                self.assertIn("kql", layer)
        # Replay must carry the time-slider filter seeded to the bucket.
        replay = layers[-1]
        self.assertEqual(len(replay["filters"]), 1)
        self.assertEqual(replay["filters"][0]["field"], "Time (UTC, 15-min)")
        self.assertEqual(replay["filters"][0]["value"], ["2026-05-19 12:30 UTC"])

    def test_replay_with_no_default_bucket_emits_empty_value(self) -> None:
        replay = self.mod._layer_replay(None)
        self.assertEqual(replay["filters"][0]["value"], [])

    def test_default_visibility(self) -> None:
        """Exactly the two headline layers should default-on."""
        m = self.mod
        layers = [
            (m._layer_state(default_visible=True),   True),
            (m._layer_navigation(),                  False),
            (m._layer_trend(),                       False),
            (m._layer_freshness(),                   False),
            (m._layer_labels(default_visible=True),  True),
            (m._layer_replay(None),                  False),
        ]
        for layer, expected in layers:
            with self.subTest(name=layer["name"]):
                self.assertEqual(layer["options"]["visible"], expected)

    def test_main_requires_core_inputs(self) -> None:
        # Strip env so argparse defaults don't smuggle in values.
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(SystemExit):
                self.mod.main([])


if __name__ == "__main__":
    unittest.main()
