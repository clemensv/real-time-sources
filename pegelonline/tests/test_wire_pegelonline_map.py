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
        # v3.6: state, navigation, 1h/3h/6h/24h trend, freshness, labels.
        self.assertEqual(
            m.LAYER_NAMES,
            {m.NAME_STATE, m.NAME_NAV,
             m.NAME_TREND_1H, m.NAME_TREND_3H, m.NAME_TREND_6H, m.NAME_TREND,
             m.NAME_FRESH, m.NAME_LABELS},
        )
        for name in m.LAYER_NAMES:
            self.assertTrue(name.startswith(m.LAYER_PREFIX),
                            f"{name!r} missing prefix {m.LAYER_PREFIX!r}")
        # Legacy names are still cleaned up by the wire script.
        for legacy in (
            "pegelonline river backbone",
            "pegelonline real rivers",
            "pegelonline historical replay",
        ):
            self.assertIn(legacy, m.LEGACY_LAYER_NAMES)

    def test_each_kql_body_well_formed(self) -> None:
        m = self.mod
        segment_builders = {
            "state":      (m._kql_state_segments, "StateSegments"),
            "navigation": (m._kql_nav_segments,   "NavSegments"),
            "trend_1h":   (lambda: m._kql_trend_segments("1h"),  "TrendSegments1h"),
            "trend_3h":   (lambda: m._kql_trend_segments("3h"),  "TrendSegments3h"),
            "trend_6h":   (lambda: m._kql_trend_segments("6h"),  "TrendSegments6h"),
            "trend_24h":  (lambda: m._kql_trend_segments("24h"), "TrendSegments24h"),
            "freshness":  (m._kql_fresh_segments, "FreshSegments"),
        }
        for layer_name, (fn, helper) in segment_builders.items():
            with self.subTest(layer=layer_name):
                body = fn()
                self.assertIn(f"{helper}()", body, f"missing call to {helper}")
                self.assertIn("geometry", body)
                self.assertIn("station_id", body)
                self.assertIn("stroke_color", body)
                self.assertIn("stroke_weight", body)
                # Segment layers must NOT carry a point projection.
                self.assertNotIn('bag_pack("type","Point"', body)
        labels_body = m._kql_labels()
        self.assertIn("StationLabels()", labels_body)
        self.assertIn("geometry", labels_body)

    def test_layer_builders_v3_segment_shape(self) -> None:
        """Hydrological / navigation / trend / freshness layers must be line
        layers driven by the precomputed ``stroke_color`` / ``stroke_weight``
        columns. Labels layer stays a point bubble layer."""
        m = self.mod
        segment_layers = [
            m._state_layer(default_visible=True),
            m._navigation_layer(),
            m._trend_layer("1h"),
            m._trend_layer("3h"),
            m._trend_layer("6h"),
            m._trend_layer("24h"),
            m._freshness_layer(),
        ]
        for layer in segment_layers:
            with self.subTest(name=layer["name"]):
                opts = layer["options"]
                self.assertEqual(opts["type"], "vector")
                self.assertNotIn("pointLayerType", opts,
                                 "segment layers must not declare a point type")
                self.assertEqual(opts["color"], ["get", "stroke_color"])
                self.assertIn("lineOptions", opts)
                lo = opts["lineOptions"]
                self.assertEqual(lo["strokeColor"], ["get", "stroke_color"])
                self.assertEqual(lo["strokeWidth"], ["get", "stroke_weight"])
                self.assertEqual(layer["geometryColumnName"], "geometry")
                self.assertEqual(layer["filters"], [])
        # Labels stays a point bubble layer with an active text label.
        labels = m._labels_layer(default_visible=True)
        lopts = labels["options"]
        self.assertEqual(lopts["type"], "vector")
        self.assertEqual(lopts["pointLayerType"], "bubble")
        self.assertIn("bubbleOptions", lopts)
        self.assertTrue(lopts["dataLabelOptions"]["enabled"])

    def test_default_visibility(self) -> None:
        """Hydrological state + station labels default-on; the alternate
        metrics default-off so the user toggles between them."""
        m = self.mod
        layers = [
            (m._state_layer(default_visible=True),    True),
            (m._navigation_layer(),                   False),
            (m._trend_layer("1h"),                    False),
            (m._trend_layer("3h"),                    False),
            (m._trend_layer("6h"),                    False),
            (m._trend_layer("24h"),                   False),
            (m._freshness_layer(),                    False),
            (m._labels_layer(default_visible=True),   True),
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
