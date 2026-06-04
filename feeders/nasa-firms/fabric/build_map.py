#!/usr/bin/env python3
"""Create and wire the NASA FIRMS global Fabric Map item against the live
`nasa-firms` KQL DB.

Two Kusto-backed layers give an OSINT-oriented global view of active fires:

  1. **Fire hotspots** (default-on, world->zoom 5) — one bubble per 1-degree
     grid cell (`FireHotspots()`), sized by detection count and coloured on a
     yellow->dark-red Fire-Radiative-Power ramp. The zoomed-out overview that
     lets an analyst spot the world's most active fire regions at a glance,
     where the fine 0.1-degree tiles are still sub-pixel.
  2. **Fire intensity tiles** (default-on, all zoom levels) — one filled square
     GeoJSON polygon per populated 0.1-degree grid cell (`FireGrid()`),
     coloured on a continuous Fire-Radiative-Power ramp by the cell's peak FRP.
     This mirrors the DWD ICON-D2 map's tile pattern: a live Kusto map layer
     runs its query globally with no viewport binding against a hard 20 MB
     result cap, and aggregating detections onto a fixed grid bounds the
     rendered row count by *grid resolution* (a few thousand cells) rather than
     by *detection count* (tens of thousands of raw pixels), so the layer never
     approaches the cap while still covering every fire region. Each tile
     carries the full per-cell OSINT summary (peak/total FRP, max brightness,
     detection count, confidence breakdown, day/night split, contributing
     instruments / satellites / sources, first & last seen), so the tiles are
     the single all-zoom detail layer and there is no separate per-detection
     point layer. The raw per-pixel scan x track footprint (`FireFootprints()`)
     remains available as a helper for a viewport-scoped PMTiles tileset (see
     README) but is not wired as a live Kusto layer because it is unbounded.

Both layers query helper functions applied to the live DB by
`feeders/nasa-firms/fabric/helpers.kql`.

Idempotent: re-running drops the nasa-firms layers by name (including the
retired per-detection point layer and per-pixel footprint layer) and re-creates
the current set. Creates the Map item if it does not yet exist.

Auth: uses `az account get-access-token` for the Fabric API (run `az login`).
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

FABRIC = "https://api.fabric.microsoft.com/v1"

MAP_NAME = "NASA FIRMS Global Fire Map"
MAP_DESC = ("Global active-fire / thermal-anomaly detections from NASA FIRMS "
            "(VIIRS + MODIS) for OSINT monitoring — a coarse fire-hotspot "
            "overview plus an all-zoom 0.1-degree fire-intensity tile field "
            "coloured by Fire Radiative Power.")

NAME_HOTSPOTS = "nasa-firms hotspots"
NAME_DETECTIONS = "nasa-firms detections"
NAME_TILES = "nasa-firms fire tiles"
# Old layer name kept here only so re-running this script removes the previous,
# unbounded per-pixel footprint layer from any map it was already wired onto.
NAME_FOOTPRINTS = "nasa-firms footprints"
LAYER_NAMES = {NAME_HOTSPOTS, NAME_DETECTIONS, NAME_TILES, NAME_FOOTPRINTS}

# Yellow (low FRP) -> dark red (extreme FRP). Must match FireColor() in
# helpers.kql so the map `match` expressions stay finite and aligned.
FIRE_COLORS = ["#FFE08A", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C", "#BD0026", "#800026"]

# Human-readable total-FRP bands for the hotspot-layer legend, in ascending
# order. The labels MUST match FireHotspots()'s `frp_band` case() in helpers.kql
# and the colours MUST stay in step with FIRE_COLORS, so the legend shows
# meaningful MW ranges instead of raw hex codes.
FIRE_BANDS = [
    ("< 25 MW", "#FFE08A"),
    ("25-100 MW", "#FEB24C"),
    ("100-250 MW", "#FD8D3C"),
    ("250-500 MW", "#FC4E2A"),
    ("500-1500 MW", "#E31A1C"),
    ("1500-5000 MW", "#BD0026"),
    (">= 5000 MW", "#800026"),
]

# FRP (MW) breakpoints aligned with FireColor()'s case() thresholds, used to
# build the continuous DWD-style `interpolate` ramp for the fire-tile layer.
FRP_STOPS = [0.0, 5.0, 20.0, 50.0, 100.0, 300.0, 1000.0]


def tok(resource: str) -> str:
    out = subprocess.run(
        ["az", "account", "get-access-token", "--resource", resource,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True, shell=True)
    return out.stdout.strip()


def api(method: str, url: str, token: str, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read().decode()
        return resp.status, dict(resp.headers), (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        return e.code, dict(e.headers), (json.loads(raw) if raw else {"error": raw})


def poll_lro(headers: dict, token: str):
    loc = headers.get("Location")
    if not loc:
        return None
    while True:
        time.sleep(2)
        _, _, body = api("GET", loc, token)
        st = body.get("status")
        if st in ("Succeeded", "Completed"):
            _, _, res = api("GET", loc + "/result", token)
            return res
        if st in ("Failed", "Cancelled"):
            raise RuntimeError(f"LRO failed: {json.dumps(body)[:400]}")


# --- layer KQL --------------------------------------------------------------
# Hotspots aggregate onto a 1-degree grid; sized by count via radius column.
KQL_HOTSPOTS = """FireHotspots(72h, 1.0)
| extend radius = todouble(min_of(26.0, 5.0 + log10(todouble(detections) + 1.0) * 9.0))
| project geometry, label, detections, total_frp, max_frp, high_conf, frp_band, radius
"""

# Fire intensity tiles: detections aggregated onto a fixed 0.1-degree grid and
# emitted as one square GeoJSON polygon per populated cell, exactly mirroring
# the DWD ICON-D2 map's tile pattern. A live Kusto map layer runs its query
# GLOBALLY (no viewport binding) against a hard 20 MB result cap; aggregating
# onto a fixed grid bounds the row count by GRID RESOLUTION (a few thousand
# populated cells) instead of by DETECTION COUNT (tens of thousands of raw
# pixels), so the layer stays well under the cap with full global coverage and
# no lossy top-N guard. Cells are coloured by peak FRP via a continuous ramp.
KQL_TILES = """FireGrid(24h, 0.1)
| project geometry, frp_max, frp_total, brightness_max, detections, high_conf,
          nominal_conf, low_conf, day_count, night_count, daynight,
          instruments, satellites, sources, first_seen, last_seen, label
"""


def _band_match_expr(get_col: str, bands: list[tuple[str, str]]) -> list:
    # Map a labelled band column (e.g. "100-250 MW") to its heat colour.
    expr = ["match", ["get", get_col]]
    for label, color in bands:
        expr += [label, color]
    expr.append("#888888")  # fallback
    return expr


def _interpolate_expr(get_col: str, stops: list[float], colors: list[str]) -> list:
    # DWD-style continuous colour ramp: interpolate linearly over the numeric
    # value column through (stop, colour) pairs.
    expr = ["interpolate", ["linear"], ["get", get_col]]
    for v, c in zip(stops, colors):
        expr += [v, c]
    return expr


def hotspots_layer() -> dict:
    return {
        "name": NAME_HOTSPOTS, "kql": KQL_HOTSPOTS, "geometryColumnName": "geometry",
        "filters": [],
        "options": {
            "type": "vector", "visible": True, "pointLayerType": "bubble",
            "maxZoom": 5.0,
            "bubbleOptions": {
                "color": _band_match_expr("frp_band", FIRE_BANDS),
                "radius": ["get", "radius"], "strokeColor": "#1a1a1a", "strokeWidth": 1,
                "opacity": 0.85, "enableSeriesGroup": True,
                "seriesGroup": "frp_band",
                "customColors": {label: color for label, color in FIRE_BANDS},
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": {"enabled": False, "size": 11, "color": "#f5f5f5",
                                  "textStrokeColor": "#000000", "textStrokeWidth": 2.5,
                                  "allowOverlap": False},
            "tooltipKeys": ["label", "detections", "total_frp", "max_frp", "high_conf"],
            "enablePopups": True,
        },
    }


def tiles_layer() -> dict:
    # DWD-style polygon tile field, now the single all-zoom fire layer: one
    # filled square per populated 0.1-deg grid cell, coloured on a continuous
    # FRP interpolate ramp. No pointLayerType (fill via polygonOptions); a
    # hairline outline keeps adjacent tiles legible without breaking the raster
    # look. Bounded by grid resolution, so safe against the 20 MB live-layer
    # cap. Each tile carries the full per-cell OSINT summary (the detail that
    # used to live on the now-removed per-detection point layer), so the tooltip
    # answers "what is burning here" at every zoom level. Rendered at all zooms
    # (no minZoom) so the tiles are visible the moment you zoom past the coarse
    # hotspot overview.
    color = _interpolate_expr("frp_max", FRP_STOPS, FIRE_COLORS)
    return {
        "name": NAME_TILES, "kql": KQL_TILES, "geometryColumnName": "geometry",
        "filters": [],
        "options": {
            "type": "vector", "visible": True,
            "color": color,
            "polygonOptions": {"fillColor": color, "fillOpacity": 0.6},
            "lineOptions": {
                "strokeColor": "#000000", "strokeWidth": 0, "strokeOpacity": 0.0,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": {"enabled": False, "size": 11, "color": "#f5f5f5",
                                  "textStrokeColor": "#000000", "textStrokeWidth": 2.5,
                                  "allowOverlap": False},
            "tooltipKeys": ["label", "frp_max", "frp_total", "brightness_max",
                            "detections", "high_conf", "nominal_conf", "low_conf",
                            "daynight", "instruments", "satellites", "sources",
                            "first_seen", "last_seen"],
            "enablePopups": True,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True, help="Fabric workspace GUID")
    ap.add_argument("--db", required=True, help="KQL database (Eventhouse) GUID")
    ap.add_argument("--name", default=MAP_NAME)
    args = ap.parse_args()

    ft = tok("https://api.fabric.microsoft.com")

    # find or create the Map item
    _, _, body = api("GET", f"{FABRIC}/workspaces/{args.workspace}/items?type=Map", ft)
    existing = next((i for i in body.get("value", []) if i.get("displayName") == args.name), None)
    if existing:
        map_id = existing["id"]
        print(f"Reusing Map {map_id}")
    else:
        print("Creating Map item ...")
        st, hdr, b = api("POST", f"{FABRIC}/workspaces/{args.workspace}/items", ft,
                         {"displayName": args.name, "type": "Map", "description": MAP_DESC})
        if st == 202:
            res = poll_lro(hdr, ft); map_id = (res or {}).get("id")
        elif st in (200, 201):
            map_id = b.get("id")
        else:
            print("ERROR creating map", st, json.dumps(b)); sys.exit(1)
        if not map_id:
            _, _, body = api("GET", f"{FABRIC}/workspaces/{args.workspace}/items?type=Map", ft)
            map_id = next(i["id"] for i in body["value"] if i["displayName"] == args.name)
        print(f"Created Map {map_id}")

    # get current definition
    st, hdr, _ = api("POST",
                     f"{FABRIC}/workspaces/{args.workspace}/items/{map_id}/getDefinition", ft)
    res = poll_lro(hdr, ft) if st == 202 else None
    if res is None:
        st2, _, body2 = api("POST",
                            f"{FABRIC}/workspaces/{args.workspace}/items/{map_id}/getDefinition", ft)
        res = body2
    parts = {p["path"]: p for p in res["definition"]["parts"]}

    if "map.json" in parts:
        mp = json.loads(base64.b64decode(parts["map.json"]["payload"]))
    else:
        mp = {"layerSources": [], "layerSettings": [], "dataSources": []}
        parts["map.json"] = {"path": "map.json", "payload": "", "payloadType": "InlineBase64"}

    # drop previously-wired nasa-firms layers (idempotent)
    removed = set()
    mp["layerSettings"] = [ls for ls in mp.get("layerSettings", [])
                           if (ls.get("name") in LAYER_NAMES and removed.add(ls.get("sourceId")))
                           is None and ls.get("name") not in LAYER_NAMES]
    mp["layerSources"] = [s for s in mp.get("layerSources", []) if s["id"] not in removed]
    for p in list(parts):
        if p.startswith("queries/layerSource-"):
            sid = p.split("layerSource-")[1].split(".kql")[0]
            if sid in removed:
                del parts[p]

    # register KQL DB
    if not any(d.get("itemId") == args.db for d in mp.get("dataSources", [])):
        mp.setdefault("dataSources", []).append(
            {"itemType": "KqlDatabase", "workspaceId": args.workspace, "itemId": args.db})

    # global dark basemap so fires pop
    bm = mp.setdefault("basemap", {})
    o = bm.setdefault("options", {})
    o.setdefault("style", "grayscale_dark")
    o.setdefault("center", [10.0, 22.0])
    o.setdefault("zoom", 1.6)
    o.setdefault("showLabels", True)
    c = bm.setdefault("controls", {})
    for k in ("zoom", "scale", "style", "compass"):
        c.setdefault(k, True)

    # wire layers: coarse hotspot bubbles for the world/continental overview
    # (where 0.1-deg tiles are sub-pixel), then the all-zoom fire-tile field
    # that carries the full per-cell detail. The per-detection point layer was
    # removed — its info now lives on the tiles.
    for layer in (hotspots_layer(), tiles_layer()):
        src_id = str(uuid.uuid4())
        mp.setdefault("layerSources", []).append({
            "id": src_id, "name": layer["name"].replace(" ", "_") + "_kusto",
            "type": "kusto", "options": {"cluster": False},
            "itemId": args.db, "refreshIntervalMs": 60_000})
        mp.setdefault("layerSettings", []).append({
            "id": str(uuid.uuid4()), "name": layer["name"], "sourceId": src_id,
            "geometryColumnName": layer["geometryColumnName"],
            "filters": layer["filters"], "options": layer["options"]})
        parts[f"queries/layerSource-{src_id}.kql"] = {
            "path": f"queries/layerSource-{src_id}.kql",
            "payload": base64.b64encode(layer["kql"].encode()).decode(),
            "payloadType": "InlineBase64"}
        print(f"  wired layer: {layer['name']}")

    parts["map.json"]["payload"] = base64.b64encode(
        json.dumps(mp, indent=2).encode()).decode()

    st, hdr, b = api("POST",
                     f"{FABRIC}/workspaces/{args.workspace}/items/{map_id}/updateDefinition",
                     ft, {"definition": {"parts": list(parts.values())}})
    if st == 202:
        poll_lro(hdr, ft)
    elif st >= 300:
        print("ERROR updateDefinition", st, json.dumps(b)); sys.exit(1)

    url = f"https://app.fabric.microsoft.com/groups/{args.workspace}/mapItems/{map_id}"
    print(f"\nOK  Map ready\n    id : {map_id}\n    url: {url}")


if __name__ == "__main__":
    main()
