import copy
import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "fabric" / "wire_aisstream_map.py"
SPEC = importlib.util.spec_from_file_location("wire_aisstream_map", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
wire_aisstream_map = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = wire_aisstream_map
SPEC.loader.exec_module(wire_aisstream_map)


def test_marker_icon_uses_schema_valid_scalar_icon():
    layer = next(
        layer
        for layer in wire_aisstream_map._layers()
        if layer.name == "aisstream live vessels"
    )
    options = copy.deepcopy(layer.options)

    wire_aisstream_map._apply_marker_icon(options, layer)

    marker_options = options["markerOptions"]
    assert marker_options["icon"] == "VehicleShip"
    assert "iconOptions" not in marker_options
    assert isinstance(marker_options["fillColor"], list)
