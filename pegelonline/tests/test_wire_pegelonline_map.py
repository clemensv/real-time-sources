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
        # Set must equal the eight declared constants (v3 adds real rivers).
        self.assertEqual(
            m.LAYER_NAMES,
            {m.NAME_STATE, m.NAME_NAV, m.NAME_TREND,
             m.NAME_FRESH, m.NAME_LABELS, m.NAME_REPLAY,
             m.NAME_RIVERS, m.NAME_REAL_RIVERS},
        )
        # All layer names must share the common prefix used for the
        # idempotent drop-and-replace logic.
        for name in m.LAYER_NAMES:
            self.assertTrue(name.startswith(m.LAYER_PREFIX),
                            f"{name!r} missing prefix {m.LAYER_PREFIX!r}")

    def test_each_kql_body_well_formed(self) -> None:
        m = self.mod
        point_builders = {
            "state":      m._kql_state,
            "navigation": m._kql_navigation,
            "trend":      m._kql_trend,
            "freshness":  m._kql_freshness,
            "labels":     m._kql_labels,
            "replay":     m._kql_replay,
        }
        for layer_name, fn in point_builders.items():
            with self.subTest(layer=layer_name):
                body = fn()
                self.assertIn("geometry", body, "geometry alias missing")
                self.assertIn('bag_pack("type","Point"', body,
                              "point projection missing")
                self.assertIn("pack_array(longitude, latitude)", body,
                              "coordinates must be (lon, lat)")
                if layer_name == "replay":
                    self.assertIn("Time (UTC, 15-min)", body)
                else:
                    self.assertNotIn("Time (UTC, 15-min)", body)
        # Rivers layer just wraps the dedicated KQL function.
        rivers_body = m._kql_rivers()
        self.assertIn("RiverBackbones()", rivers_body)
        self.assertIn("geometry", rivers_body)
        # Real rivers layer wraps the RealRiverBackbones() function and
        # adds data-driven stroke colour + weight as plain columns.
        real_body = m._kql_real_rivers()
        self.assertIn("RealRiverBackbones()", real_body)
        self.assertIn("stroke_color", real_body)
        self.assertIn("stroke_weight", real_body)

    def test_layer_builders_v2_schema_shape(self) -> None:
        """Every layer must follow the Fabric Map 2.0.0 vector-layer shape:
        type='vector' + geometry-specific options (bubble/line). Data-driven
        colour expressions must appear at BOTH options.color and inside the
        nested options block — only the dual-write form is honoured by the
        Fabric Map renderer (verified live against ContosoRealTimeTest)."""
        m = self.mod
        bubble_layers = [
            m._layer_state(default_visible=True),
            m._layer_navigation(),
            m._layer_trend(),
            m._layer_freshness(),
            m._layer_labels(default_visible=True),
            m._layer_replay("2026-05-19 12:30 UTC"),
        ]
        for layer in bubble_layers:
            with self.subTest(name=layer["name"]):
                opts = layer["options"]
                self.assertEqual(opts["type"], "vector")
                self.assertEqual(opts["pointLayerType"], "bubble")
                self.assertIn("bubbleOptions", opts)
                self.assertIn("color", opts["bubbleOptions"])
                # All point layers share a single geometry column.
                self.assertEqual(layer["geometryColumnName"], "geometry")
                self.assertIn("filters", layer)
                self.assertIsInstance(layer["filters"], list)
        # Rivers layer is a line layer, not point.
        rivers = m._layer_rivers(default_visible=True)
        ropts = rivers["options"]
        self.assertEqual(ropts["type"], "vector")
        self.assertNotIn("pointLayerType", ropts)
        self.assertIn("lineOptions", ropts)
        self.assertIn("strokeColor", ropts["lineOptions"])
        self.assertIn("strokeWidth", ropts["lineOptions"])
        # Dual-write of the colour expression.
        self.assertEqual(ropts["color"], ropts["lineOptions"]["strokeColor"])
        # Real-rivers is also a line layer with data-driven stroke colour/width.
        real_rivers = m._layer_real_rivers(default_visible=True)
        rropts = real_rivers["options"]
        self.assertEqual(rropts["type"], "vector")
        self.assertIn("lineOptions", rropts)
        self.assertEqual(rropts["color"], ["get", "stroke_color"])
        self.assertEqual(rropts["lineOptions"]["strokeColor"], ["get", "stroke_color"])
        self.assertEqual(rropts["lineOptions"]["strokeWidth"], ["get", "stroke_weight"])
        # Replay carries the time-slider filter seeded to the bucket.
        replay = bubble_layers[-1]
        self.assertEqual(len(replay["filters"]), 1)
        self.assertEqual(replay["filters"][0]["field"], "Time (UTC, 15-min)")
        self.assertEqual(replay["filters"][0]["value"], ["2026-05-19 12:30 UTC"])

    def test_replay_with_no_default_bucket_emits_empty_value(self) -> None:
        replay = self.mod._layer_replay(None)
        self.assertEqual(replay["filters"][0]["value"], [])

    def test_default_visibility(self) -> None:
        """Real rivers + hydrological state default-on; everything else
        default-off (incl. the legacy stitched backbone and the dense labels
        layer — the latter is gated by minZoom anyway)."""
        m = self.mod
        layers = [
            (m._layer_real_rivers(default_visible=True), True),
            (m._layer_rivers(default_visible=False),  False),
            (m._layer_state(default_visible=True),    True),
            (m._layer_navigation(),                   False),
            (m._layer_trend(),                        False),
            (m._layer_freshness(),                    False),
            (m._layer_labels(default_visible=False),  False),
            (m._layer_replay(None),                   False),
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
