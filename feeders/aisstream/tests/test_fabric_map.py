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


def test_point_layers_bind_latitude_and_longitude_columns():
    point_layers = [
        layer
        for layer in wire_aisstream_map._layers()
        if layer.options.get("pointLayerType") in {"bubble", "marker"}
    ]

    assert point_layers
    for layer in point_layers:
        assert wire_aisstream_map._location_binding(layer) == {
            "latitudeColumnName": "latitude",
            "longitudeColumnName": "longitude",
        }


def test_polygon_layers_bind_geometry_column():
    polygon_layers = [
        layer
        for layer in wire_aisstream_map._layers()
        if layer.options.get("pointLayerType") not in {"bubble", "marker"}
    ]

    assert polygon_layers
    for layer in polygon_layers:
        assert wire_aisstream_map._location_binding(layer) == {
            "geometryColumnName": "geometry"
        }


def test_get_definition_downgrades_unsupported_map_schema():
    map_definition = {
        "$schema": (
            "https://developer.microsoft.com/json-schemas/fabric/item/map/"
            "definition/2.1.0/schema.json"
        ),
        "basemap": {},
        "dataSources": [],
        "iconSources": [],
        "layerSources": [],
        "layerSettings": [],
    }
    response = type(
        "Response",
        (),
        {
            "status_code": 200,
            "content": b"{}",
            "json": lambda self: {
                "definition": {
                    "parts": [
                        {
                            "path": "map.json",
                            "payload": wire_aisstream_map._b64(
                                wire_aisstream_map.json.dumps(map_definition)
                            ),
                            "payloadType": "InlineBase64",
                        }
                    ]
                }
            },
            "raise_for_status": lambda self: None,
        },
    )()
    fabric = type("Session", (), {"post": lambda self, url: response})()

    actual, _ = wire_aisstream_map._get_definition(
        fabric,
        "https://api.fabric.microsoft.com/v1",
        "workspace",
        "map",
    )

    assert actual["$schema"] == wire_aisstream_map.MAP_SCHEMA
