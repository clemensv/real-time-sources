#!/usr/bin/env python3
"""Create and wire the NASA FIRMS global Fabric Map item against the live
`nasa-firms` KQL DB.

Two Kusto-backed layers give an OSINT-oriented global view of active fires:

  1. **Fire hotspots** (default-on, world view) — one bubble per 1-degree grid
     cell (`FireHotspots()`), sized by detection count and coloured on a
     yellow->dark-red Fire-Radiative-Power ramp. Lets an analyst spot the
     world's most active fire regions at a glance.
  2. **Active fire detections** (default-on, mid zoom 3-8) — one bubble per
     individual VIIRS/MODIS detection (`RecentFireDetections()`), coloured by
     FRP and labelled with instrument / FRP / confidence. Reveals where a fire
     complex sits once the analyst zooms in.
  3. **Fire pixel footprints** (default-on, high zoom >= 8) — one filled GeoJSON
     polygon per detection (`FireFootprints()`), the true scan x track ground
     rectangle of the satellite pixel rather than a point, so the real extent of
     each thermal anomaly is visible at high zoom.

Both layers query helper functions applied to the live DB by
`feeders/nasa-firms/fabric/helpers.kql`.

Idempotent: re-running drops the two nasa-firms layers by name and re-creates
them. Creates the Map item if it does not yet exist.

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
            "(VIIRS + MODIS) for OSINT monitoring — fire hotspots and "
            "individual detections coloured by Fire Radiative Power.")

NAME_HOTSPOTS = "nasa-firms hotspots"
NAME_DETECTIONS = "nasa-firms detections"
NAME_FOOTPRINTS = "nasa-firms footprints"
LAYER_NAMES = {NAME_HOTSPOTS, NAME_DETECTIONS, NAME_FOOTPRINTS}

# Yellow (low FRP) -> dark red (extreme FRP). Must match FireColor() in
# helpers.kql so the map `match` expressions stay finite and aligned.
FIRE_COLORS = ["#FFE08A", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C", "#BD0026", "#800026"]


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
| project geometry, label, detections, total_frp, max_frp, high_conf, fill_color, radius
"""

# Individual detections over the last 24h; colour + radius come from helpers.
KQL_DETECTIONS = """RecentFireDetections(24h, 0)
| project geometry, label, frp, brightness, confidence_level, daynight, satellite, instrument, source, acq_datetime, fill_color, radius
"""

# True pixel footprints (scan x track rectangle) as GeoJSON polygons; shown at
# high zoom where the real ground extent of each VIIRS/MODIS pixel is visible.
KQL_FOOTPRINTS = """FireFootprints(24h, 0)
| project geometry, label, frp, brightness, confidence_level, daynight, satellite, instrument, source, scan, track, acq_datetime, fill_color
"""


def _match_expr(get_col: str, colors: list[str]) -> list:
    expr = ["match", ["get", get_col]]
    for c in colors:
        expr += [c, c]
    expr.append("#888888")  # fallback
    return expr


def _custom_colors(colors: list[str]) -> dict:
    return {c: c for c in colors}


def hotspots_layer() -> dict:
    return {
        "name": NAME_HOTSPOTS, "kql": KQL_HOTSPOTS, "geometryColumnName": "geometry",
        "filters": [],
        "options": {
            "type": "vector", "visible": True, "pointLayerType": "bubble",
            "maxZoom": 5.0,
            "bubbleOptions": {
                "color": _match_expr("fill_color", FIRE_COLORS),
                "radius": ["get", "radius"], "strokeColor": "#1a1a1a", "strokeWidth": 1,
                "opacity": 0.85, "enableSeriesGroup": True,
                "seriesGroup": "fill_color", "customColors": _custom_colors(FIRE_COLORS),
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": {"enabled": False, "size": 11, "color": "#f5f5f5",
                                  "textStrokeColor": "#000000", "textStrokeWidth": 2.5,
                                  "allowOverlap": False},
            "tooltipKeys": ["label", "detections", "total_frp", "max_frp", "high_conf"],
            "enablePopups": True,
        },
    }


def detections_layer() -> dict:
    return {
        "name": NAME_DETECTIONS, "kql": KQL_DETECTIONS, "geometryColumnName": "geometry",
        "filters": [],
        "options": {
            "type": "vector", "visible": True, "pointLayerType": "bubble",
            "minZoom": 3.0, "maxZoom": 8.0,
            "bubbleOptions": {
                "color": _match_expr("fill_color", FIRE_COLORS),
                "radius": ["get", "radius"], "strokeColor": "#000000", "strokeWidth": 1,
                "opacity": 0.9, "enableSeriesGroup": True,
                "seriesGroup": "fill_color", "customColors": _custom_colors(FIRE_COLORS),
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": {"enabled": False, "size": 11, "color": "#f5f5f5",
                                  "textStrokeColor": "#000000", "textStrokeWidth": 2.5,
                                  "allowOverlap": True},
            "tooltipKeys": ["label", "frp", "brightness", "confidence_level", "daynight",
                            "satellite", "instrument", "source", "acq_datetime"],
            "enablePopups": True,
        },
    }


def footprints_layer() -> dict:
    # Polygon (fill) layer: no pointLayerType; fill via polygonOptions, outline
    # via the sibling lineOptions block (polygonOptions has no stroke fields).
    return {
        "name": NAME_FOOTPRINTS, "kql": KQL_FOOTPRINTS, "geometryColumnName": "geometry",
        "filters": [],
        "options": {
            "type": "vector", "visible": True,
            "minZoom": 8.0,
            "polygonOptions": {
                "fillColor": _match_expr("fill_color", FIRE_COLORS),
                "fillOpacity": 0.55, "enableSeriesGroup": True,
                "seriesGroup": "fill_color", "customColors": _custom_colors(FIRE_COLORS),
            },
            "lineOptions": {
                "strokeColor": "#000000", "strokeWidth": 1, "strokeOpacity": 0.9,
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": {"enabled": False, "size": 11, "color": "#f5f5f5",
                                  "textStrokeColor": "#000000", "textStrokeWidth": 2.5,
                                  "allowOverlap": True},
            "tooltipKeys": ["label", "frp", "brightness", "confidence_level", "daynight",
                            "satellite", "instrument", "source", "scan", "track", "acq_datetime"],
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

    # wire layers (hotspots under detections under footprints)
    for layer in (hotspots_layer(), detections_layer(), footprints_layer()):
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
