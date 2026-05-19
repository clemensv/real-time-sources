"""Create or update the pegelonline Fabric Map item.

Wires 5 Kusto-backed map layers that visualise the live state of the German
Federal Waterways gauge network as **river-segment ribbons** (one polyline
per gauge, sourced from ``RiverSegments``), plus station labels:

  1. Hydrological state  - river segments coloured by ``stateMnwMhw``
                           (low / normal / high / very-high / unknown). Default-on.
  2. Navigation state    - segments coloured by ``stateNswHsw``.
  3. 24-hour trend       - segments coloured by direction (rising / steady /
                           falling); stroke width scales with |delta_cm/24h|.
  4. Data freshness      - segments coloured by data age (fresh / stale /
                           old / very-old / no-data); diagnostic layer.
  5. Station labels      - text labels ``shortname  NNN cm`` at zoom >= 9.
                           Default-on.

All layers query helper functions in ``kql/pegelonline.kql``:

  * ``StateSegments()``, ``NavSegments()``, ``TrendSegments()``,
    ``FreshSegments()`` - per-station river segments enriched with the
    current metric value and a precomputed ``stroke_color`` / ``stroke_weight``.
  * ``StationLabels()``  - one point per station with the value-string label.

Inputs (env vars or CLI args):

  FABRIC_WORKSPACE_ID   - GUID of the Fabric workspace containing the map
  FABRIC_MAP_ID         - GUID of the Fabric Map item to patch
  FABRIC_KQL_DB_ID      - GUID of the KQL database with the helper functions
  KUSTO_CLUSTER_URI     - https://<cluster>.kusto.fabric.microsoft.com
  KUSTO_DB              - KQL database name (default: pegelonline)
  FABRIC_TOKEN          - bearer token for the Fabric REST API
  KUSTO_TOKEN           - bearer token for the Kusto cluster
  FABRIC_API_BASE       - override (default: https://api.fabric.microsoft.com/v1)

If FABRIC_TOKEN / KUSTO_TOKEN are not set, the script falls back to
``azure.identity.DefaultAzureCredential`` to acquire them.

The script is idempotent: re-running drops every layer whose name belongs to
``LAYER_NAMES | LEGACY_LAYER_NAMES`` and re-creates them with current colour
ramps and KQL bodies. The Fabric Map item itself must already exist.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import uuid
from typing import Optional

import requests


# ---------------------------------------------------------------------------
# Layer catalogue
# ---------------------------------------------------------------------------
# Names must be globally unique inside the Fabric Map; they are used to detect
# previously-wired layers and replace them on re-run.

LAYER_PREFIX = "pegelonline "

NAME_STATE    = f"{LAYER_PREFIX}hydrological state"
NAME_NAV      = f"{LAYER_PREFIX}navigation state"
NAME_TREND_1H = f"{LAYER_PREFIX}1h trend"
NAME_TREND_3H = f"{LAYER_PREFIX}3h trend"
NAME_TREND_6H = f"{LAYER_PREFIX}6h trend"
NAME_TREND    = f"{LAYER_PREFIX}24h trend"
NAME_FRESH    = f"{LAYER_PREFIX}data freshness"
NAME_LABELS   = f"{LAYER_PREFIX}station labels"

LAYER_NAMES = {
    NAME_STATE, NAME_NAV,
    NAME_TREND_1H, NAME_TREND_3H, NAME_TREND_6H, NAME_TREND,
    NAME_FRESH, NAME_LABELS,
}

# Layer names from previous map deployments that should be cleaned up during
# the idempotent rewire. Includes both the v1/v2 stitched backbone and the
# v3 dot-based metric layers replaced by per-station river segments here.
LEGACY_LAYER_NAMES = {
    "pegelonline river backbone",
    "pegelonline real rivers",
    "pegelonline real rivers (Azure Maps geometry)",
    "pegelonline historical replay",
}

# Common KQL projection for the station-labels point layer.
LABEL_GEOM_PROJECTION = (
    '| extend geometry = bag_pack("type","Point",'
    '"coordinates",pack_array(longitude, latitude))'
)


def _kql_state_segments() -> str:
    """Per-station river segment coloured by hydrological state."""
    return """StateSegments()
| project geometry, station_id, water_shortname, shortname, longname,
          value, state, stroke_color, stroke_weight, label
"""


def _kql_nav_segments() -> str:
    """Per-station river segment coloured by shipping-navigation state."""
    return """NavSegments()
| project geometry, station_id, water_shortname, shortname, longname,
          value, nav_state, stroke_color, stroke_weight, label
"""


def _kql_trend_segments(window: str = "24h") -> str:
    """Per-station river segment coloured by `window`-trend direction;
    stroke weight scales with absolute delta over that window."""
    func = {
        "1h":  "TrendSegments1h",
        "3h":  "TrendSegments3h",
        "6h":  "TrendSegments6h",
        "24h": "TrendSegments24h",
    }[window]
    return f"""{func}()
| project geometry, station_id, water_shortname, shortname, longname,
          value, direction, delta_cm, abs_delta, stroke_color, stroke_weight, label
"""


def _kql_fresh_segments() -> str:
    """Per-station river segment coloured by data freshness (age bucket)."""
    return """FreshSegments()
| project geometry, station_id, water_shortname, shortname, longname,
          value, freshness, age_min, stroke_color, stroke_weight, label
"""


def _kql_labels() -> str:
    """Station-label points: shortname + current value."""
    return """StationLabels()
| project geometry, station_id, shortname, longname, value, state,
          water_shortname, label
"""


# ---------------------------------------------------------------------------
# Layer styling
# ---------------------------------------------------------------------------
#
# Fabric Map v2.0.0 only accepts ``type: vector | raster``. Line styling lives
# in ``lineOptions`` and accepts data-driven expressions via ``["get", ...]``.
# Each metric KQL helper precomputes ``stroke_color`` (hex string) and
# ``stroke_weight`` (number) per row, so the map just passes them through.

LABEL_OPTIONS_BASE = {
    "enabled": True,
    "size": 11,
    "color": "#1a1a1a",
    "textStrokeColor": "#FFFFFF",
    "textStrokeWidth": 2.5,
    "allowOverlap": False,
}


def _line_options() -> dict:
    """Reusable lineOptions block: thick, rounded, data-driven."""
    return {
        "strokeColor": ["get", "stroke_color"],
        "strokeWidth": ["get", "stroke_weight"],
        "strokeOpacity": 0.9,
        "lineJoin": "round",
        "lineCap": "round",
    }



# ---------------------------------------------------------------------------
# Plumbing: tokens, LRO, default-filter lookup
# ---------------------------------------------------------------------------

def _get_token(env_name: str, scope: str) -> str:
    tok = os.environ.get(env_name)
    if tok:
        return tok.strip()
    try:
        from azure.identity import DefaultAzureCredential
    except ImportError as exc:
        raise SystemExit(
            f"{env_name} not set and azure-identity not installed; "
            f"either set {env_name} or `pip install azure-identity`."
        ) from exc
    return DefaultAzureCredential().get_token(scope).token


def _poll_lro(session: requests.Session, response: requests.Response):
    if response.status_code != 202:
        response.raise_for_status()
        return response.json() if response.content else None
    op_url = response.headers["Location"]
    while True:
        status = session.get(op_url).json()
        s = status.get("status")
        if s == "Succeeded":
            r = session.get(op_url + "/result")
            return r.json() if r.content else None
        if s == "Failed":
            raise RuntimeError(f"LRO failed: {json.dumps(status)[:400]}")
        time.sleep(2)



# ---------------------------------------------------------------------------
# Layer builders
# ---------------------------------------------------------------------------

def _state_layer(default_visible: bool) -> dict:
    """River segments coloured by hydrological state at the nearest station."""
    return {
        "name": NAME_STATE,
        "kql": _kql_state_segments(),
        "options": {
            "type": "vector",
            "visible": default_visible,
            "color": ["get", "stroke_color"],
            "lineOptions": _line_options(),
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False),
            "tooltipKeys": ["shortname", "longname", "water_shortname",
                             "value", "state"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _navigation_layer() -> dict:
    """River segments coloured by shipping-navigation state."""
    return {
        "name": NAME_NAV,
        "kql": _kql_nav_segments(),
        "options": {
            "type": "vector",
            "visible": False,
            "color": ["get", "stroke_color"],
            "lineOptions": _line_options(),
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False),
            "tooltipKeys": ["shortname", "water_shortname", "nav_state",
                             "value"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _trend_layer(window: str = "24h") -> dict:
    """River segments coloured by `window`-trend direction; thickness scales
    with |delta|. `window` in {"1h","3h","6h","24h"}."""
    name = {
        "1h":  NAME_TREND_1H,
        "3h":  NAME_TREND_3H,
        "6h":  NAME_TREND_6H,
        "24h": NAME_TREND,
    }[window]
    return {
        "name": name,
        "kql": _kql_trend_segments(window),
        "options": {
            "type": "vector",
            "visible": False,
            "color": ["get", "stroke_color"],
            "lineOptions": _line_options(),
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False),
            "tooltipKeys": ["shortname", "water_shortname", "direction",
                             "delta_cm", "value"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _freshness_layer() -> dict:
    """River segments coloured by age of the latest reading per station."""
    return {
        "name": NAME_FRESH,
        "kql": _kql_fresh_segments(),
        "options": {
            "type": "vector",
            "visible": False,
            "color": ["get", "stroke_color"],
            "lineOptions": _line_options(),
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False),
            "tooltipKeys": ["shortname", "water_shortname", "freshness",
                             "age_min", "value"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _labels_layer(default_visible: bool) -> dict:
    """Tiny anchor bubble + text label at zoom >= 9 so the river-segment
    layers stay readable when you zoom in."""
    return {
        "name": NAME_LABELS,
        "kql": _kql_labels(),
        "options": {
            "type": "vector",
            "visible": default_visible,
            "pointLayerType": "bubble",
            "minZoom": 9,
            "bubbleOptions": {
                "color": "#1a1a1a",
                "radius": 2,
                "strokeColor": "#ffffff",
                "strokeWidth": 1,
                "opacity": 0.85,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=True,
                                     size=12, allowOverlap=False),
            "tooltipKeys": ["shortname", "longname", "water_shortname",
                             "value", "state"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }



# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def wire(workspace_id: str, map_id: str, kql_db_id: str,
         kusto_uri: str, kusto_db: str,
         fabric_token: str, kusto_token: str,
         api_base: str = "https://api.fabric.microsoft.com/v1") -> None:

    fab = requests.Session()
    fab.headers["Authorization"] = f"Bearer {fabric_token}"
    fab.headers["Content-Type"]  = "application/json"
    ks = requests.Session()
    ks.headers["Authorization"] = f"Bearer {kusto_token}"
    ks.headers["Content-Type"]  = "application/json"

    # 1. Fetch current map definition.
    res = _poll_lro(fab, fab.post(
        f"{api_base}/workspaces/{workspace_id}/items/{map_id}/getDefinition"))
    parts = {p["path"]: p for p in res["definition"]["parts"]}
    mp = json.loads(base64.b64decode(parts["map.json"]["payload"]))

    # 2. Drop any previously-wired pegelonline layers (idempotent). Includes
    #    legacy/ad-hoc layer names from earlier deployments.
    removed_src_ids = set()
    kept_settings = []
    drop_names = LAYER_NAMES | LEGACY_LAYER_NAMES
    for ls in mp.get("layerSettings", []):
        if ls.get("name") in drop_names:
            removed_src_ids.add(ls.get("sourceId"))
        else:
            kept_settings.append(ls)
    mp["layerSettings"] = kept_settings
    mp["layerSources"] = [s for s in mp.get("layerSources", [])
                          if s["id"] not in removed_src_ids]
    for p in list(parts):
        if p.startswith("queries/layerSource-"):
            sid = p.split("layerSource-")[1].split(".kql")[0]
            if sid in removed_src_ids:
                del parts[p]

    # 3. Ensure the KQL database is registered as a data source.
    if not any(d.get("itemId") == kql_db_id for d in mp.get("dataSources", [])):
        mp.setdefault("dataSources", []).append({
            "itemType": "KqlDatabase",
            "workspaceId": workspace_id,
            "itemId": kql_db_id,
        })

    # 3b. Set a beautiful default basemap centered on Germany.  Only seed
    # fields the user has not already customised so re-runs are non-destructive.
    bm = mp.setdefault("basemap", {})
    bm_opts = bm.setdefault("options", {})
    bm_opts.setdefault("style", "road_shaded_relief")
    bm_opts.setdefault("center", [10.45, 51.16])  # geographic centre of Germany
    bm_opts.setdefault("zoom", 5.6)
    bm_opts.setdefault("showLabels", True)
    bm_opts.setdefault("language", "de-DE")
    bm_ctrl = bm.setdefault("controls", {})
    bm_ctrl.setdefault("zoom", True)
    bm_ctrl.setdefault("scale", True)
    bm_ctrl.setdefault("style", True)
    bm_ctrl.setdefault("compass", True)

    # 4. Build & append the layers in legend order. State on by default;
    #    metric layers stack on top of each other so the user toggles between
    #    them. Labels render only at deeper zoom.
    layers = [
        _state_layer(default_visible=True),
        _navigation_layer(),
        _trend_layer("1h"),
        _trend_layer("3h"),
        _trend_layer("6h"),
        _trend_layer("24h"),
        _freshness_layer(),
        _labels_layer(default_visible=True),
    ]

    for layer in layers:
        src_id = str(uuid.uuid4())
        mp.setdefault("layerSources", []).append({
            "id": src_id,
            "name": layer["name"].replace(" ", "_") + "_kusto",
            "type": "kusto",
            "options": {"cluster": False},
            "itemId": kql_db_id,
            "refreshIntervalMs": 60_000,
        })
        mp["layerSettings"].append({
            "id": str(uuid.uuid4()),
            "name": layer["name"],
            "sourceId": src_id,
            "geometryColumnName": layer.get("geometryColumnName", "geometry"),
            "filters": layer["filters"],
            "options": layer["options"],
        })
        parts[f"queries/layerSource-{src_id}.kql"] = {
            "path": f"queries/layerSource-{src_id}.kql",
            "payload": base64.b64encode(layer["kql"].encode()).decode(),
            "payloadType": "InlineBase64",
        }
        print(f"  {layer['name']}: wired (default-on={layer['options'].get('visible', False)})")

    # 6. Push the updated definition.
    parts["map.json"]["payload"] = base64.b64encode(
        json.dumps(mp, indent=2).encode()).decode()
    print(f"definition: {len(mp['layerSources'])} sources, "
          f"{len(mp['layerSettings'])} settings")
    r = fab.post(
        f"{api_base}/workspaces/{workspace_id}/items/{map_id}/updateDefinition",
        json={"definition": {"parts": list(parts.values())}},
    )
    _poll_lro(fab, r)
    print("Map updated.")


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace-id", default=os.environ.get("FABRIC_WORKSPACE_ID"))
    ap.add_argument("--map-id",       default=os.environ.get("FABRIC_MAP_ID"))
    ap.add_argument("--kql-db-id",    default=os.environ.get("FABRIC_KQL_DB_ID"))
    ap.add_argument("--kusto-uri",    default=os.environ.get("KUSTO_CLUSTER_URI"))
    ap.add_argument("--kusto-db",     default=os.environ.get("KUSTO_DB", "pegelonline"))
    ap.add_argument("--api-base",     default=os.environ.get(
        "FABRIC_API_BASE", "https://api.fabric.microsoft.com/v1"))
    args = ap.parse_args(argv)

    missing = [n for n in ("workspace_id", "map_id", "kql_db_id", "kusto_uri")
               if not getattr(args, n)]
    if missing:
        ap.error("missing required arg(s): " + ", ".join("--" + m.replace("_", "-")
                                                          for m in missing))

    fab_tok = _get_token("FABRIC_TOKEN", "https://api.fabric.microsoft.com/.default")
    # Use the specific cluster URI as the audience: the generic
    # https://kusto.fabric.microsoft.com is not a registered AAD resource
    # principal in every tenant.
    ks_tok  = _get_token("KUSTO_TOKEN",  args.kusto_uri.rstrip("/") + "/.default")

    wire(args.workspace_id, args.map_id, args.kql_db_id,
         args.kusto_uri, args.kusto_db,
         fab_tok, ks_tok, args.api_base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
