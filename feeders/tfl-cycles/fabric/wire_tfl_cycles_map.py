"""Idempotently (re)wire a Fabric Map item with Kusto-backed vector layers
for a freshly-deployed tfl-cycles (TfL / Santander Cycles, London public
bikeshare) source.

Unlike the moving-vehicle hsl-hfp map this mirrors, tfl-cycles is a **fixed
docking-station** feed: ~798 stationary BikePoint docks whose *identity and
location* arrive as ``StationInformation`` reference records and whose *live
bike/dock counts* arrive as ``StationStatus`` telemetry. A fresh
``tfl-cycles/kql/tfl-cycles.kql`` deployment lays down the following schema in
the target Eventhouse (KQL database ``tfl_cycles``):

  * Bracketed, dotted CloudEvents-shaped base tables:
    ``['UK.Gov.TfL.Cycles.StationInformation']`` - station identity, WGS84
                                                    location and physical
                                                    capacity (reference),
    ``['UK.Gov.TfL.Cycles.StationStatus']``      - live availability counts
                                                    (telemetry).
  * Per-table ``<X>Latest`` materialized views that pre-aggregate
    ``arg_max(___time, *) by ___type, ___source, ___subject`` so callers get
    the latest snapshot per station without scanning history.

Location lives ONLY on ``StationInformationLatest`` and availability lives ONLY
on ``StationStatusLatest``, so every station layer JOINs the two views on the
stable ``station_id`` key.

This script wires the following layers (all parametric, no hand-wiring):

  1.  Station availability - bubbles coloured by bike-availability state
      (red = no bikes -> green = plenty), sized by station capacity. On.
  2.  Station labels       - station name + live bike/dock counts, shown as a
      data label at street zoom (z14+). On.
  3.  Empty docks          - the same stations recoloured by empty-dock supply
      (for riders returning a bike). Off by default.

The map's basemap centre + zoom are auto-discovered from the bounding box of
``tflcycles_bbox()`` (falling back to the raw station footprint, and finally to
central London) so the script needs no manual tuning.

The Fabric Map item must already exist (see ``post-deploy.ps1`` which
auto-creates it). This script is idempotent: re-running drops the layers it
manages (matched by their KQL source's ``itemId`` binding) and recreates them,
so colour ramps, query changes and viewport tweaks land cleanly.

Inputs (env vars or CLI args, mirroring ``hsl-hfp/fabric/wire_hsl_hfp_map.py``):

  FABRIC_WORKSPACE_ID   - GUID of the Fabric workspace containing the Map
  FABRIC_MAP_ID         - GUID of the Fabric Map item to patch
  FABRIC_KQL_DB_ID      - GUID of the KQL database with the tfl-cycles tables
  KUSTO_CLUSTER_URI     - https://<cluster>.kusto.fabric.microsoft.com
  KUSTO_DB              - KQL database name (default ``tfl_cycles``)
  FABRIC_TOKEN          - bearer token for the Fabric REST API
  KUSTO_TOKEN           - bearer token for the Kusto cluster
  FABRIC_API_BASE       - override (default https://api.fabric.microsoft.com/v1)
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass
from typing import Any, Optional

import requests


# ---------------------------------------------------------------------------
# Token + HTTP helpers (factored to match the hsl-hfp / pegelonline hook style).
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


def _session(token: str) -> requests.Session:
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {token}"
    s.headers["Content-Type"] = "application/json"
    return s


def _poll_lro(session: requests.Session, response: requests.Response) -> Any:
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
            raise RuntimeError(f"Fabric LRO failed: {json.dumps(status)[:600]}")
        time.sleep(2)


def _kql_mgmt(ks: requests.Session, kusto_uri: str, db: str, csl: str) -> dict[str, Any]:
    r = ks.post(f"{kusto_uri.rstrip('/')}/v1/rest/mgmt", json={"db": db, "csl": csl})
    if r.status_code >= 400:
        raise RuntimeError(f"KQL mgmt failed ({db}): HTTP {r.status_code} {r.text[:800]}")
    return r.json()


def _kql_query(ks: requests.Session, kusto_uri: str, db: str, csl: str) -> Optional[dict[str, Any]]:
    r = ks.post(f"{kusto_uri.rstrip('/')}/v2/rest/query", json={"db": db, "csl": csl})
    if r.status_code >= 400:
        raise RuntimeError(f"KQL query failed ({db}): HTTP {r.status_code} {r.text[:800]}")
    for frame in r.json():
        if (frame.get("FrameType") == "DataTable"
                and frame.get("TableKind") == "PrimaryResult"):
            return frame
    return None


# ---------------------------------------------------------------------------
# KQL helper functions installed in the target database.
#
# We lean on the materialized views (``['UK.Gov.TfL.Cycles.StationInformationLatest']``
# and ``['UK.Gov.TfL.Cycles.StationStatusLatest']``) created by tfl-cycles.kql.
# Each MV reduces a CloudEvents-shaped table to one row per (___type, ___source,
# ___subject) - i.e. one row per station. Reading the MV directly is
# constant-time regardless of how long the source has ingested.
#
# ``tflcycles_stations()`` is the single enriched JOIN (StationInformationLatest
# JOIN StationStatusLatest on station_id) that every layer reuses; different
# layers just pick a different colour column off it (like hsl-hfp reuses
# ``hslhfp_vehicle_points`` for both its vehicle and punctuality layers).
#
# Reserved-keyword note: KQL rejects bare reserved words as identifiers with a
# generic HTTP 400 and no syntax detail. tfl-cycles uses ``lon`` (not ``long``)
# so the classic ``long`` collision does not apply, but every derived/projected
# column is bracket-quoted and given an explicit safe name (``avail_ratio``,
# ``fill_state``, ``docks_state``, ...) so no computed column can ever alias a
# keyword.
# ---------------------------------------------------------------------------

TFL_CYCLES_FUNCTIONS: list[str] = [
    # ------------------------------------------------------------------
    # Every installed, located docking station enriched with its live
    # availability. Location comes from StationInformationLatest, counts from
    # StationStatusLatest; the two are joined on the stable station_id. Null /
    # 0,0 coordinates are dropped up front and only ``is_installed`` stations
    # are kept. Precomputes bike-availability + empty-dock colour ramps, a
    # capacity-scaled bubble ``radius`` and a human ``label``.
    r"""
.create-or-alter function with (folder = "Map", skipvalidation = "true") tflcycles_stations() {
    ['UK.Gov.TfL.Cycles.StationInformationLatest']
    | where isnotnull(lat) and isnotnull(lon) and lat != 0.0 and lon != 0.0
    | project station_id, ['name'], lat, lon, capacity, terminal_name, temporary
    | join kind=inner (
        ['UK.Gov.TfL.Cycles.StationStatusLatest']
        | project station_id, num_bikes_available, num_standard_bikes_available,
                  num_ebikes_available, num_empty_docks, num_docks,
                  is_installed, is_locked, modified
      ) on station_id
    | where is_installed == true
    | extend ['denom'] = iff(isnotnull(capacity) and capacity > 0, todouble(capacity), todouble(num_docks))
    | extend ['avail_ratio'] = iff(isnotnull(['denom']) and ['denom'] > 0.0, todouble(num_bikes_available) / ['denom'], real(null))
    | extend ['empty_ratio'] = iff(isnotnull(['denom']) and ['denom'] > 0.0, todouble(num_empty_docks) / ['denom'], real(null))
    | extend ['avail_percent'] = iff(isnull(['avail_ratio']), real(null), round(['avail_ratio'] * 100.0, 0))
    | extend ['docks_percent'] = iff(isnull(['empty_ratio']), real(null), round(['empty_ratio'] * 100.0, 0))
    | extend ['fill_state'] = case(
        num_bikes_available <= 0,     "No bikes",
        isnull(['avail_ratio']),      "Bikes available",
        ['avail_ratio'] < 0.25,       "Few bikes",
        ['avail_ratio'] < 0.75,       "Bikes available",
        "Plenty of bikes")
    | extend ['fill_color'] = case(
        ['fill_state'] == "No bikes",         "#d7191c",
        ['fill_state'] == "Few bikes",        "#fdae61",
        ['fill_state'] == "Bikes available",  "#a6d96a",
        ['fill_state'] == "Plenty of bikes",  "#1a9641",
        "#9e9e9e")
    | extend ['docks_state'] = case(
        num_empty_docks <= 0,         "No docks",
        isnull(['empty_ratio']),      "Docks available",
        ['empty_ratio'] < 0.25,       "Few docks",
        ['empty_ratio'] < 0.75,       "Docks available",
        "Plenty of docks")
    | extend ['docks_color'] = case(
        ['docks_state'] == "No docks",         "#d7191c",
        ['docks_state'] == "Few docks",        "#fdae61",
        ['docks_state'] == "Docks available",  "#74add1",
        ['docks_state'] == "Plenty of docks",  "#2c7bb6",
        "#9e9e9e")
    | extend ['radius'] = round(min_of(16.0, max_of(4.0, 4.0 + 1.4 * sqrt(coalesce(todouble(capacity), todouble(num_docks), 0.0)))), 1)
    | extend ['label'] = strcat(['name'], " - ", tostring(num_bikes_available), " bikes / ", tostring(num_empty_docks), " docks")
    | extend ['geometry'] = bag_pack("type", "Point", "coordinates", pack_array(lon, lat))
    | project ['geometry'], station_id, ['name'], terminal_name, lat, lon, capacity,
              num_bikes_available, num_standard_bikes_available, num_ebikes_available,
              num_empty_docks, num_docks, is_locked, modified,
              ['avail_ratio'], ['avail_percent'], ['empty_ratio'], ['docks_percent'],
              ['fill_state'], ['fill_color'], ['docks_state'], ['docks_color'],
              ['radius'], ['label']
}
""",
    # ------------------------------------------------------------------
    # Map bounding box: queried once at deploy time so the basemap centre and
    # zoom auto-fit the station footprint. 1 % / 99 % quantiles guard against a
    # single mislocated station dragging the box across the country.
    r"""
.create-or-alter function with (folder = "Map", skipvalidation = "true") tflcycles_bbox() {
    tflcycles_stations()
    | summarize lat_p01 = percentile(lat, 1), lat_p99 = percentile(lat, 99),
                lon_p01 = percentile(lon, 1), lon_p99 = percentile(lon, 99),
                cnt = count()
}
""",
]

# ---------------------------------------------------------------------------
# Layer styling. As with hsl-hfp, Fabric Maps' ``seriesGroup`` + ``customColors``
# schema populates the Data Layers legend but does NOT drive per-feature paint
# colour, so we write BOTH: ``customColors`` (legend) AND a MapLibre-style
# ``["match", ["get", column], ...]`` expression on the paint property (what
# actually renders). Bubble ``radius`` accepts a data-driven ``["get", col]``
# expression (proven in-repo by nasa-firms/fabric/build_map.py), which is how
# "size by capacity" is honoured without inventing new schema fields.
# ---------------------------------------------------------------------------

LABEL_BASE = {
    "enabled": False,
    "size": 11,
    "color": "#111111",
    "textStrokeColor": "#FFFFFF",
    "textStrokeWidth": 2,
    "allowOverlap": False,
}

# Seed palettes (keyed on the legend label). Re-enumerated from live data at
# deploy time; the seeds document the expected domain and act as a fallback.
AVAIL_PALETTE_SEED = {
    "No bikes": "#d7191c", "Few bikes": "#fdae61",
    "Bikes available": "#a6d96a", "Plenty of bikes": "#1a9641",
}
DOCKS_PALETTE_SEED = {
    "No docks": "#d7191c", "Few docks": "#fdae61",
    "Docks available": "#74add1", "Plenty of docks": "#2c7bb6",
}


def _series(column: str, palette: dict[str, str],
            paint_column: str | None = None) -> dict[str, Any]:
    series: dict[str, Any] = {
        "enableSeriesGroup": True,
        "seriesGroup": column,
        "customColors": dict(palette),
    }
    # When the legend column (seriesGroup) differs from the column that carries
    # the paint colour, record the paint column so _populate_palette can map
    # legend-label -> colour. This non-Fabric key is consumed and removed before
    # the definition is serialised.
    if paint_column and paint_column != column:
        series["_paintColorColumn"] = paint_column
    return series


def _color_match(column: str, palette: dict[str, str], fallback: str = "#9e9e9e") -> list[Any]:
    expr: list[Any] = ["match", ["get", column]]
    for value, color in palette.items():
        expr.append(value)
        expr.append(color)
    expr.append(fallback)
    return expr


def bubble_options(*, visible: bool, radius: Any = 4,
                   labels: bool = False, label_size: int = 11,
                   min_zoom: float | None = None, max_zoom: float | None = None,
                   color: str = "#1A1A1A",
                   color_column: str = "fill_color",
                   legend_column: str | None = None,
                   palette: dict[str, str] | None = None,
                   tooltip_keys: list[str] | None = None,
                   stroke_color: str = "#FFFFFF") -> dict[str, Any]:
    bubble: dict[str, Any] = {
        "color": color,
        "radius": radius,
        "strokeColor": stroke_color,
        "strokeWidth": 1,
        "opacity": 0.92,
    }
    # Only bind a series group when there is a palette to colour by; a plain
    # anchor bubble (e.g. the labels layer) stays a scalar colour so
    # _populate_palette skips it.
    if palette is not None:
        legend = legend_column or color_column
        bubble["color"] = "#888888"
        bubble.update(_series(legend, palette, paint_column=color_column))
    opts: dict[str, Any] = {
        "type": "vector",
        "visible": visible,
        "pointLayerType": "bubble",
        "bubbleOptions": bubble,
        "dataLabelKeys": ["label"],
        "dataLabelOptions": dict(LABEL_BASE, enabled=labels, size=label_size),
        "tooltipKeys": tooltip_keys or ["label"],
        "enablePopups": True,
    }
    if min_zoom is not None:
        opts["minZoom"] = min_zoom
    if max_zoom is not None:
        opts["maxZoom"] = max_zoom
    return opts


def _text_filter(field: str) -> dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "type": "text",
        "field": field,
        "locked": False,
        "value": [],
    }


def _number_filter(field: str, minimum: float, maximum: float) -> dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "type": "number",
        "field": field,
        "locked": False,
        "min": minimum,
        "max": maximum,
    }


# ---------------------------------------------------------------------------
# Layer declarations - one entry per Fabric Map vector layer.
# ---------------------------------------------------------------------------

@dataclass
class Layer:
    name: str
    kql: str
    options: dict[str, Any]
    filters: list[dict[str, Any]]


def _layers() -> list[Layer]:
    return [
        Layer(
            "tfl-cycles station availability",
            "tflcycles_stations()",
            bubble_options(
                visible=True, radius=["get", "radius"],
                color_column="fill_color", legend_column="fill_state",
                palette=AVAIL_PALETTE_SEED,
                tooltip_keys=[
                    "name", "fill_state", "num_bikes_available", "num_empty_docks",
                    "capacity", "num_docks", "num_ebikes_available", "avail_percent",
                ],
            ),
            [_text_filter("fill_state"), _number_filter("avail_percent", 0, 100)],
        ),
        Layer(
            "tfl-cycles station labels",
            "tflcycles_stations()",
            bubble_options(
                visible=True, radius=2, labels=True, label_size=11, min_zoom=14,
                color="#1A1A1A", palette=None,
                tooltip_keys=[
                    "name", "num_bikes_available", "num_empty_docks", "capacity",
                ],
            ),
            [],
        ),
        Layer(
            "tfl-cycles empty docks",
            "tflcycles_stations()",
            bubble_options(
                visible=False, radius=["get", "radius"],
                color_column="docks_color", legend_column="docks_state",
                palette=DOCKS_PALETTE_SEED,
                tooltip_keys=[
                    "name", "docks_state", "num_empty_docks", "num_bikes_available",
                    "capacity", "num_docks", "docks_percent",
                ],
            ),
            [_text_filter("docks_state"), _number_filter("docks_percent", 0, 100)],
        ),
    ]

# ---------------------------------------------------------------------------
# Map definition patching.
# ---------------------------------------------------------------------------

LONDON_CENTER = [-0.1278, 51.5074]  # lon, lat - final basemap fallback


def _b64(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")


def _get_definition(fab: requests.Session, api_base: str, workspace_id: str,
                    map_id: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    res = _poll_lro(
        fab,
        fab.post(f"{api_base}/workspaces/{workspace_id}/items/{map_id}/getDefinition"),
    )
    parts = {p["path"]: p for p in res["definition"]["parts"]}
    if "map.json" not in parts:
        raise RuntimeError("Map definition has no map.json part")
    mp = json.loads(base64.b64decode(parts["map.json"]["payload"]).decode("utf-8"))
    mp.setdefault("dataSources", [])
    mp.setdefault("iconSources", [])
    mp.setdefault("layerSources", [])
    mp.setdefault("layerSettings", [])
    if "$schema" not in mp:
        mp["$schema"] = ("https://developer.microsoft.com/json-schemas/fabric/item/map/"
                         "definition/2.0.0/schema.json")
    return mp, parts


def _put_definition(fab: requests.Session, api_base: str, workspace_id: str,
                    map_id: str, mp: dict[str, Any],
                    parts: dict[str, dict[str, Any]]) -> None:
    parts["map.json"] = {
        "path": "map.json",
        "payload": _b64(json.dumps(mp, indent=2)),
        "payloadType": "InlineBase64",
    }
    r = fab.post(
        f"{api_base}/workspaces/{workspace_id}/items/{map_id}/updateDefinition",
        json={"definition": {"parts": list(parts.values())}},
    )
    print(f"updateDefinition HTTP {r.status_code}")
    _poll_lro(fab, r)


def _bbox(ks: requests.Session, kusto_uri: str,
          kusto_db: str) -> Optional[tuple[float, float, float, float, int]]:
    """Return (lat_p01, lat_p99, lon_p01, lon_p99, n) or None.

    Tries the joined station bounding box first, then falls back to the raw
    StationInformationLatest footprint (a brand-new database may have location
    reference before any StationStatus telemetry has arrived, so the inner join
    could be empty)."""
    candidates = (
        "tflcycles_bbox()",
        ("['UK.Gov.TfL.Cycles.StationInformationLatest'] "
         "| where isnotnull(lat) and isnotnull(lon) and lat != 0.0 and lon != 0.0 "
         "| summarize lat_p01 = percentile(lat, 1), lat_p99 = percentile(lat, 99), "
         "lon_p01 = percentile(lon, 1), lon_p99 = percentile(lon, 99), cnt = count()"),
    )
    for csl in candidates:
        try:
            frame = _kql_query(ks, kusto_uri, kusto_db, csl)
        except Exception as exc:
            print(f"  bbox lookup failed ({csl[:24]}...): {exc}")
            continue
        if not frame or not frame.get("Rows"):
            continue
        cols = [c["ColumnName"] for c in frame["Columns"]]
        rec = dict(zip(cols, frame["Rows"][0]))
        if not rec.get("cnt"):
            continue
        try:
            return (
                float(rec["lat_p01"]), float(rec["lat_p99"]),
                float(rec["lon_p01"]), float(rec["lon_p99"]), int(rec["cnt"]),
            )
        except (TypeError, ValueError):
            continue
    return None


def _zoom_for_extent(lat_span: float, lon_span: float) -> float:
    """Pick a sensible default zoom for the bounding box. Tuned for a
    ~1600x1000 viewport; errs on the side of zooming OUT slightly so the full
    source is visible at first render."""
    span = max(lat_span, lon_span / 2.0)  # account for Mercator distortion
    if span >= 30:  return 3.5
    if span >= 15:  return 4.5
    if span >= 8:   return 5.5
    if span >= 4:   return 6.7
    if span >= 2:   return 8.0
    if span >= 1:   return 9.5
    if span >= 0.5: return 10.6
    if span >= 0.2: return 11.5
    return 12.5


def _set_basemap(mp: dict[str, Any],
                 bbox: Optional[tuple[float, float, float, float, int]]) -> None:
    if bbox is None:
        center = list(LONDON_CENTER)
        zoom = 11.0
    else:
        lat_p01, lat_p99, lon_p01, lon_p99, _ = bbox
        center = [(lon_p01 + lon_p99) / 2.0, (lat_p01 + lat_p99) / 2.0]
        zoom = _zoom_for_extent(lat_p99 - lat_p01, lon_p99 - lon_p01)
    mp["basemap"] = {
        "options": {
            "center": center,
            "zoom": zoom,
            "style": "grayscale_light",
            "showLabels": True,
        },
        "controls": {
            "zoom": True, "pitch": True, "compass": True, "scale": True,
            "traffic": False, "style": True,
        },
        "backgroundColor": "#FFFFFF",
        "theme": "light",
    }
    print(f"  basemap center={center} zoom={zoom}")


def _populate_palette(ks: requests.Session, kusto_uri: str, kusto_db: str,
                      layer: Layer) -> None:
    """For each seriesGroup-bound paint property on the layer, fetch the
    distinct values from the live data and populate ``customColors`` as an
    identity map. Also write a MapLibre ``match`` expression to the paint
    property (Fabric's ``seriesGroup`` populates the legend but does not
    actually drive paint colour)."""
    paint_key_for = {
        "bubbleOptions": "color",
        "lineOptions": "strokeColor",
        "polygonOptions": "fillColor",
    }
    for sub, paint_key in paint_key_for.items():
        block = layer.options.get(sub)
        if not block or not block.get("enableSeriesGroup"):
            continue
        column = block.get("seriesGroup")
        if not column:
            continue
        # Non-Fabric marker: when present the legend column (seriesGroup) is a
        # human label distinct from the column carrying the paint colour.
        paint_column = block.pop("_paintColorColumn", None)
        if paint_column and paint_column != column:
            block["customColors"] = {}
        try:
            if paint_column and paint_column != column:
                frame = _kql_query(
                    ks, kusto_uri, kusto_db,
                    f"{layer.kql}\n| where isnotempty({column}) and isnotempty({paint_column})"
                    f"\n| distinct {column}, {paint_column}\n| take 200",
                )
                pairs = [(row[0], row[1]) for row in (frame.get("Rows") or [])
                         if row and row[0] and row[1]]
            else:
                frame = _kql_query(
                    ks, kusto_uri, kusto_db,
                    f"{layer.kql}\n| where isnotempty({column})"
                    f"\n| distinct {column}\n| take 50",
                )
                pairs = [(row[0], row[0]) for row in (frame.get("Rows") or [])
                         if row and row[0]]
        except Exception as exc:
            print(f"    palette enumeration failed for {layer.name}/{column}: {exc}")
            pairs = []
        if not pairs:
            continue
        block.setdefault("customColors", {})
        for label, color in pairs:
            block["customColors"].setdefault(label, color)
        block[paint_key] = _color_match(column, block["customColors"])
        print(f"    palette {column}: {len(block['customColors'])} colors")


# ---------------------------------------------------------------------------
# Top-level wiring entry point.
# ---------------------------------------------------------------------------

def wire(*, workspace_id: str, map_id: str, kql_db_id: str,
         kusto_uri: str, kusto_db: str,
         fabric_token: str, kusto_token: str,
         api_base: str = "https://api.fabric.microsoft.com/v1") -> None:
    fab = _session(fabric_token)
    ks = _session(kusto_token)

    # 1. Create/refresh the helper KQL functions in the target database.
    print(f"Creating {len(TFL_CYCLES_FUNCTIONS)} helper functions in {kusto_db}")
    for f in TFL_CYCLES_FUNCTIONS:
        head = next((line.strip() for line in f.splitlines() if line.strip()), "")
        print(f"  {head[:110]}")
        _kql_mgmt(ks, kusto_uri, kusto_db, f)

    # 2. Look up the source's geographic footprint to centre the basemap.
    print("Discovering bounding box from tflcycles_bbox()")
    bbox = _bbox(ks, kusto_uri, kusto_db)
    if bbox is None:
        print("  no stations indexed yet; centring on London")
    else:
        lat_p01, lat_p99, lon_p01, lon_p99, n = bbox
        print(f"  {n} stations; lat=[{lat_p01:.3f}, {lat_p99:.3f}]"
              f" lon=[{lon_p01:.3f}, {lon_p99:.3f}]")

    # 3. Patch the map definition idempotently.
    mp, parts = _get_definition(fab, api_base, workspace_id, map_id)
    _set_basemap(mp, bbox)

    # Drop previously-wired layers whose source is bound to this KQL DB so we
    # don't accumulate stale layers across re-runs.
    removed_src_ids = {
        s["id"] for s in mp.get("layerSources", [])
        if s.get("itemId") == kql_db_id
    }
    if removed_src_ids:
        print(f"  removing {len(removed_src_ids)} pre-existing tfl-cycles layer source(s)")
    mp["layerSettings"] = [ls for ls in mp.get("layerSettings", [])
                           if ls.get("sourceId") not in removed_src_ids]
    mp["layerSources"] = [s for s in mp.get("layerSources", [])
                          if s["id"] not in removed_src_ids]
    for path in list(parts):
        if path.startswith("queries/layerSource-"):
            sid = path.split("layerSource-", 1)[1].split(".kql", 1)[0]
            if sid in removed_src_ids:
                del parts[path]

    # Ensure this KQL DB is registered as a data source.
    if not any(d.get("itemId") == kql_db_id for d in mp["dataSources"]):
        mp["dataSources"].append({
            "itemType": "KqlDatabase",
            "workspaceId": workspace_id,
            "itemId": kql_db_id,
        })

    # 4. Add each layer, validating the query and populating the palette.
    for layer in _layers():
        print(f"  layer {layer.name}")
        try:
            cnt_frame = _kql_query(ks, kusto_uri, kusto_db, f"{layer.kql}\n| count")
            cnt = cnt_frame["Rows"][0][0] if cnt_frame and cnt_frame.get("Rows") else "?"
            print(f"    rows: {cnt}")
        except Exception as exc:
            print(f"    validation failed (skipping): {exc}")
            continue

        _populate_palette(ks, kusto_uri, kusto_db, layer)

        src_id = str(uuid.uuid4())
        mp["layerSources"].append({
            "id": src_id,
            "name": f"{layer.name}_source",
            "type": "kusto",
            "options": {"cluster": False},
            "itemId": kql_db_id,
            "refreshIntervalMs": 0,
        })
        mp["layerSettings"].append({
            "id": str(uuid.uuid4()),
            "name": layer.name,
            "sourceId": src_id,
            "geometryColumnName": "geometry",
            "filters": layer.filters,
            "options": layer.options,
        })
        parts[f"queries/layerSource-{src_id}.kql"] = {
            "path": f"queries/layerSource-{src_id}.kql",
            "payload": _b64(layer.kql),
            "payloadType": "InlineBase64",
        }

    _put_definition(fab, api_base, workspace_id, map_id, mp, parts)
    print(f"OK - map {map_id} updated with {len(_layers())} layers")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--workspace-id", default=os.environ.get("FABRIC_WORKSPACE_ID"))
    ap.add_argument("--map-id",       default=os.environ.get("FABRIC_MAP_ID"))
    ap.add_argument("--kql-db-id",    default=os.environ.get("FABRIC_KQL_DB_ID"))
    ap.add_argument("--kusto-uri",    default=os.environ.get("KUSTO_CLUSTER_URI"))
    ap.add_argument("--kusto-db",     default=os.environ.get("KUSTO_DB", "tfl_cycles"))
    ap.add_argument("--api-base",     default=os.environ.get(
        "FABRIC_API_BASE", "https://api.fabric.microsoft.com/v1"))
    args = ap.parse_args(argv)

    missing = [n for n in ("workspace_id", "map_id", "kql_db_id", "kusto_uri")
               if not getattr(args, n)]
    if missing:
        ap.error("missing required: " + ", ".join("--" + m.replace("_", "-") for m in missing))
        return 2

    fabric_token = _get_token("FABRIC_TOKEN", "https://api.fabric.microsoft.com/.default")
    kusto_token = _get_token("KUSTO_TOKEN", "https://kusto.fabric.microsoft.com/.default")

    wire(
        workspace_id=args.workspace_id,
        map_id=args.map_id,
        kql_db_id=args.kql_db_id,
        kusto_uri=args.kusto_uri,
        kusto_db=args.kusto_db,
        fabric_token=fabric_token,
        kusto_token=kusto_token,
        api_base=args.api_base,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
