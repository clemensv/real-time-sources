"""Create or update the pegelonline Fabric Map item.

Wires 6 Kusto-backed point-symbol layers that visualise the live state of the
German Federal Waterways gauge network:

  1. Hydrological state    - circles coloured by ``stateMnwMhw`` (low / normal
                             / high / very-high / unknown). Default-on.
  2. Navigation state      - squares coloured by ``stateNswHsw`` (normal /
                             high / above-HSW / unknown).
  3. 24-hour trend         - circles coloured by direction (rising / steady /
                             falling); size scaled by absolute 24h delta in cm.
  4. Freshness             - rings coloured by data age (fresh / stale /
                             very-stale); diagnostic layer.
  5. Station labels        - text labels "shortname  NNN cm" shown at zoom
                             >= 9. Default-on.
  6. Historical replay     - same hydrological state encoding but reading from
                             ``MeasurementHistoryBuckets()`` with a single-
                             select text filter on ``Time (UTC, 15-min)``
                             seeded to the latest bucket. Drag the filter to
                             replay the last 24h of flood / drought waves
                             travelling down the river network.

All layers query the helper functions added by ``kql/pegelonline.kql``:

  * ``EnrichedMeasurements()``         - join of CurrentMeasurementLatest with
                                         StationLatest (lat/lon/name/agency/water).
  * ``MeasurementTrend24h()``          - adds delta_cm + direction columns.
  * ``MeasurementHistoryBuckets(24h)`` - 15-min bucketed history of the last
                                         24 hours for the time-slider layer.

Inputs (env vars or CLI args):

  FABRIC_WORKSPACE_ID   - GUID of the Fabric workspace containing the map
  FABRIC_MAP_ID         - GUID of the Fabric Map item to patch
  FABRIC_KQL_DB_ID      - GUID of the KQL database with the helper functions
  KUSTO_CLUSTER_URI     - https://<cluster>.kusto.fabric.microsoft.com
  KUSTO_DB              - KQL database name (default: pegelonline)
  FABRIC_TOKEN          - bearer token for the Fabric REST API
                          (https://api.fabric.microsoft.com/.default)
  KUSTO_TOKEN           - bearer token for the Kusto cluster
                          (https://kusto.fabric.microsoft.com/.default)
  FABRIC_API_BASE       - override (default: https://api.fabric.microsoft.com/v1)

If FABRIC_TOKEN / KUSTO_TOKEN are not set, the script falls back to
``azure.identity.DefaultAzureCredential`` to acquire them.

The script is idempotent: re-running drops every layer whose name belongs to
``LAYER_NAMES`` (matched exactly) and re-creates them with current colour
ramps, default filter values, and KQL bodies. The Fabric Map item itself must
already exist - this script does not create it from scratch (item creation
goes through ``post-deploy.ps1`` or the Fabric UI).
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

NAME_REAL_RIVERS = f"{LAYER_PREFIX}real rivers"
NAME_STATE   = f"{LAYER_PREFIX}hydrological state"
NAME_NAV     = f"{LAYER_PREFIX}navigation state"
NAME_TREND   = f"{LAYER_PREFIX}24h trend"
NAME_FRESH   = f"{LAYER_PREFIX}data freshness"
NAME_LABELS  = f"{LAYER_PREFIX}station labels"
NAME_REPLAY  = f"{LAYER_PREFIX}historical replay"

LAYER_NAMES = {NAME_REAL_RIVERS, NAME_STATE, NAME_NAV, NAME_TREND,
               NAME_FRESH, NAME_LABELS, NAME_REPLAY}

# Legacy layer names from previous map deployments that should be removed
# during the idempotent rewire (in addition to anything currently in
# LAYER_NAMES). These were created by older versions of this script or by
# one-off ad-hoc scripts.
LEGACY_LAYER_NAMES = {
    "pegelonline river backbone",                    # v1/v2 stitched-line backbone
    "pegelonline real rivers (Azure Maps geometry)", # v3 ad-hoc-script earlier name
}

# Common geometry projection appended to every KQL body.
GEOM_PROJECTION = (
    '| extend geometry = bag_pack("type","Point",'
    '"coordinates",pack_array(longitude, latitude))'
)


def _kql_state() -> str:
    return f"""EnrichedMeasurements()
| extend label = strcat(shortname, '  ', tostring(round(value, 0)), ' cm')
| extend state = coalesce(stateMnwMhw, "unknown")
{GEOM_PROJECTION}
| project geometry, value, state, label, water_shortname, agency, ___time, shortname, longname
"""


def _kql_navigation() -> str:
    return f"""EnrichedMeasurements()
| extend label = strcat(shortname, '  ', tostring(round(value, 0)), ' cm')
| extend nav_state = coalesce(stateNswHsw, "unknown")
{GEOM_PROJECTION}
| project geometry, value, nav_state, label, water_shortname, agency, ___time, shortname, longname
"""


def _kql_trend() -> str:
    return f"""MeasurementTrend24h()
| extend abs_delta = abs(coalesce(delta_cm, real(0)))
| extend label = strcat(shortname, '  ',
    case(direction=="rising",   strcat('+', tostring(round(abs_delta,0)), ' cm/24h'),
         direction=="falling",  strcat('-', tostring(round(abs_delta,0)), ' cm/24h'),
         direction=="steady",   '~ steady',
         'no 24h ref'))
{GEOM_PROJECTION}
| project geometry, value, direction, abs_delta, delta_cm, label, water_shortname, agency, shortname, longname
"""


def _kql_freshness() -> str:
    return f"""EnrichedMeasurements()
| extend age_min = datetime_diff('minute', now(), ___time)
| extend freshness = case(age_min <=  30, "fresh",
                          age_min <= 120, "stale",
                                          "very-stale")
| extend label = strcat(shortname, '  ', tostring(age_min), ' min ago')
{GEOM_PROJECTION}
| project geometry, freshness, age_min, label, water_shortname, agency, shortname, longname
"""


def _kql_labels() -> str:
    return f"""EnrichedMeasurements()
| extend label = strcat(shortname, '  ', tostring(round(value, 0)), ' cm')
{GEOM_PROJECTION}
| project geometry, label, water_shortname, agency, shortname, longname, value
"""


def _kql_replay() -> str:
    return f"""MeasurementHistoryBuckets(24h)
| extend label = strcat(shortname, '  ', tostring(round(value, 0)), ' cm')
| extend state = coalesce(stateMnwMhw, "unknown")
{GEOM_PROJECTION}
| project geometry, value, state, label, ['Time (UTC, 15-min)'],
          water_shortname, agency, shortname, longname
"""


def _kql_real_rivers() -> str:
    """RealRiverBackbones() projects a MultiLineString `geometry` sourced
    from Azure Maps tiles (where available) or a station-interpolated polyline
    fallback for canals/tributaries Azure Maps doesn't label. Stroke colour
    & width are computed here so the Fabric Map can use simple `["get", ...]`
    expressions."""
    return """RealRiverBackbones()
| extend stroke_color = case(
    worst_state == "very-high", "#d73027",
    worst_state == "high",      "#fc8d59",
    worst_state == "low",       "#91bfdb",
    worst_state == "normal",    "#1a9850",
                                "#9aa0a6")
| extend stroke_weight = todouble(case(
    n_gauges >= 30, 6,
    n_gauges >= 10, 4,
    n_gauges >=  3, 3,
                    2))
| project geometry, water_shortname, water_longname, label, worst_state,
          n_gauges, avg_value, stroke_color, stroke_weight
"""


# ---------------------------------------------------------------------------
# Layer styling (colour expressions, sizes)
# ---------------------------------------------------------------------------
#
# Fabric Map v2.0.0 schema only accepts `type: vector | raster`. Point
# rendering goes via `pointLayerType` ("bubble" | "marker" | "heatmap") with
# the corresponding `bubbleOptions` / `markerOptions` / `heatmapOptions`
# sub-object. Line and polygon styling goes via `lineOptions` / `polygonOptions`
# regardless of the geometry type.

# stateMnwMhw values per pegelonline docs: low / normal / high / unknown /
# commented / out-dated.  Map "very-high" (when present) to the same red as
# "high" but slightly darker.

STATE_COLOR = [
    "match", ["get", "state"],
    "low",       "#2c7bb6",
    "normal",    "#1a9850",
    "high",      "#fdae61",
    "very-high", "#d7191c",
    "commented", "#999999",
    "out-dated", "#bdbdbd",
    "#cccccc",
]

# Same palette but keyed on `worst_state` (used by the river-backbone layer).
WORST_STATE_COLOR = [
    "match", ["get", "worst_state"],
    "low",       "#2c7bb6",
    "normal",    "#1a9850",
    "high",      "#fdae61",
    "very-high", "#d7191c",
    "#7f7f7f",
]

NAV_COLOR = [
    "match", ["get", "nav_state"],
    "normal",    "#1a9850",
    "high",      "#fdae61",
    "very-high", "#d7191c",
    "commented", "#999999",
    "out-dated", "#bdbdbd",
    "#cccccc",
]

TREND_COLOR = [
    "match", ["get", "direction"],
    "rising",  "#d7191c",
    "falling", "#2c7bb6",
    "steady",  "#bdbdbd",
    "#eeeeee",
]

FRESH_COLOR = [
    "match", ["get", "freshness"],
    "fresh",      "#1a9850",
    "stale",      "#fdae61",
    "very-stale", "#999999",
    "#cccccc",
]

# Trend radius scales linearly from 4 px (no delta) to 18 px (>= 250 cm/24h).
TREND_RADIUS = ["interpolate", ["linear"], ["get", "abs_delta"],
                0, 4, 25, 7, 50, 10, 100, 14, 250, 18]

# River stroke width scales by gauge count (more gauges = trunk river).
# Beefier values so the river backbone reads clearly even at country zoom.
RIVER_STROKE_WIDTH = ["interpolate", ["linear"], ["get", "n_gauges"],
                       2, 3.5, 5, 5.0, 15, 7.5, 40, 10.0]

LABEL_OPTIONS_BASE = {
    "enabled": True,
    "size": 11,
    "color": "#1a1a1a",
    "textStrokeColor": "#FFFFFF",
    "textStrokeWidth": 2.5,
    "allowOverlap": False,
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


def _latest_replay_bucket(kusto_uri: str, kusto_db: str,
                          kusto_session: requests.Session) -> Optional[str]:
    """Return the most recent 15-min bucket label so the time-slider layer
    renders immediately when first toggled on."""
    q = (
        'MeasurementHistoryBuckets(2h) '
        '| summarize b = max(bucket) '
        "| project strcat(format_datetime(b, 'yyyy-MM-dd HH:mm'), ' UTC')"
    )
    try:
        r = kusto_session.post(
            f"{kusto_uri.rstrip('/')}/v2/rest/query",
            json={"db": kusto_db, "csl": q},
            timeout=30,
        )
    except requests.RequestException as exc:
        print(f"  [warn] replay bucket lookup failed: {exc}")
        return None
    if r.status_code != 200:
        return None
    for frame in r.json():
        if (frame.get("FrameType") == "DataTable"
                and frame.get("TableKind") == "PrimaryResult"):
            rows = frame.get("Rows") or []
            if rows and rows[0]:
                return rows[0][0]
    return None


# ---------------------------------------------------------------------------
# Layer builders
# ---------------------------------------------------------------------------

def _layer_state(default_visible: bool) -> dict:
    """Bubble signposts colour-coded by hydrological state. Bubble (not
    marker) because data-driven `fillColor` only works reliably on bubbles
    in Fabric Maps; custom marker icons silently fall back to the default
    blue pin and lose the colour mapping.

    Fabric Maps requires the data-driven colour expression at BOTH
    `options.color` (top-level) AND nested under the geometry-specific
    options object (`bubbleOptions` / `polygonOptions` / `lineOptions`) —
    only the nested form is applied if you set just one. Pattern verified
    against the live DWD ICON-D2 map in this workspace."""
    return {
        "name": NAME_STATE,
        "kql": _kql_state(),
        "options": {
            "type": "vector",
            "visible": default_visible,
            "pointLayerType": "bubble",
            "color": STATE_COLOR,
            "bubbleOptions": {
                "color": STATE_COLOR,
                "radius": 7,
                "strokeColor": "#1a1a1a",
                "strokeWidth": 1.2,
                "opacity": 0.95,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False, size=11),
            "tooltipKeys": ["shortname", "longname", "water_shortname",
                            "value", "state", "agency"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _layer_navigation() -> dict:
    return {
        "name": NAME_NAV,
        "kql": _kql_navigation(),
        "options": {
            "type": "vector",
            "visible": False,
            "pointLayerType": "bubble",
            "color": NAV_COLOR,
            "bubbleOptions": {
                "color": NAV_COLOR,
                "radius": 8,
                "strokeColor": "#1a1a1a",
                "strokeWidth": 1.2,
                "opacity": 0.95,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False),
            "tooltipKeys": ["shortname", "nav_state", "value"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _layer_trend() -> dict:
    """Bubble layer (not marker) because we need data-driven radius."""
    return {
        "name": NAME_TREND,
        "kql": _kql_trend(),
        "options": {
            "type": "vector",
            "visible": False,
            "pointLayerType": "bubble",
            "color": TREND_COLOR,
            "bubbleOptions": {
                "color": TREND_COLOR,
                "radius": TREND_RADIUS,
                "strokeColor": "#1a1a1a",
                "strokeWidth": 0.8,
                "opacity": 0.9,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False),
            "tooltipKeys": ["shortname", "direction", "delta_cm", "value"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _layer_freshness() -> dict:
    """Hollow ring overlay; diagnostic-only."""
    return {
        "name": NAME_FRESH,
        "kql": _kql_freshness(),
        "options": {
            "type": "vector",
            "visible": False,
            "pointLayerType": "bubble",
            "color": FRESH_COLOR,
            "bubbleOptions": {
                "color": "#ffffff00",
                "radius": 12,
                "strokeColor": FRESH_COLOR,
                "strokeWidth": 2.5,
                "opacity": 1.0,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=False),
            "tooltipKeys": ["shortname", "freshness", "age_min"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _layer_labels(default_visible: bool) -> dict:
    """Dense readable labels at deep zoom levels.

    The pins on the hydrological-state layer already carry a label, so this
    layer kicks in only when that layer is hidden or the user wants the
    plain-text view at street-level zoom.
    """
    return {
        "name": NAME_LABELS,
        "kql": _kql_labels(),
        "options": {
            "type": "vector",
            "visible": default_visible,
            "pointLayerType": "bubble",
            "minZoom": 9,
            "bubbleOptions": {
                "color": "#ffffff00",
                "radius": 2,
                "strokeColor": "#ffffff00",
                "strokeWidth": 0,
                "opacity": 0,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=True,
                                     size=12, allowOverlap=False),
        },
        "geometryColumnName": "geometry",
        "filters": [],
    }


def _layer_replay(default_bucket: Optional[str]) -> dict:
    filter_id = str(uuid.uuid4())
    return {
        "name": NAME_REPLAY,
        "kql": _kql_replay(),
        "options": {
            "type": "vector",
            "visible": False,
            "pointLayerType": "bubble",
            "color": STATE_COLOR,
            "bubbleOptions": {
                "color": STATE_COLOR,
                "radius": 8,
                "strokeColor": "#1a1a1a",
                "strokeWidth": 1.2,
                "opacity": 0.95,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=True, size=11),
            "tooltipKeys": ["shortname", "state", "value", "Time (UTC, 15-min)"],
            "enablePopups": True,
        },
        "geometryColumnName": "geometry",
        "filters": [{
            "id": filter_id,
            "type": "text",
            "field": "Time (UTC, 15-min)",
            "locked": False,
            "value": [default_bucket] if default_bucket else [],
        }],
    }


def _layer_real_rivers(default_visible: bool) -> dict:
    """Real meandering river polylines sourced from Azure Maps' own
    microsoft.base.labels vector tiles. Geometry aligns pixel-perfectly
    with the basemap, so a thick coloured overlay highlights the river's
    actual course rather than the straight gauge-to-gauge backbone.

    Requires the ``RiverGeometries`` table to be populated by
    ``build_river_geometries.py`` + the post-deploy hook. If the table is
    empty the layer simply renders nothing (no error).
    """
    return {
        "name": NAME_REAL_RIVERS,
        "kql": _kql_real_rivers(),
        "options": {
            "type": "vector",
            "visible": default_visible,
            "color": ["get", "stroke_color"],
            "lineOptions": {
                "strokeColor": ["get", "stroke_color"],
                "strokeWidth": ["get", "stroke_weight"],
                "strokeOpacity": 0.9,
                "lineJoin": "round",
                "lineCap": "round",
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": dict(LABEL_OPTIONS_BASE, enabled=True,
                                     size=12, allowOverlap=False),
            "tooltipKeys": ["water_longname", "n_gauges",
                            "worst_state", "avg_value"],
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

    # 4. Resolve the default time-slider bucket for the replay layer.
    default_bucket = _latest_replay_bucket(kusto_uri, kusto_db, ks)
    print(f"  replay default bucket = {default_bucket or '(none yet)'}")

    # 5. Build & append the layers in legend order. Real rivers go first so
    #    they render under the gauge-stitched backbone and the pins. The
    #    legacy stitched-line backbone is kept as a default-off fallback for
    #    rivers/canals not present in RiverGeometries.
    layers = [
        _layer_real_rivers(default_visible=True),
        _layer_state(default_visible=True),
        _layer_navigation(),
        _layer_trend(),
        _layer_freshness(),
        _layer_labels(default_visible=False),
        _layer_replay(default_bucket),
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
