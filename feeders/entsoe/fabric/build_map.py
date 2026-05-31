#!/usr/bin/env python3
"""Create and wire the ENTSO-E Fabric Map item against the live `entsoe` KQL DB.

Two Kusto-backed layers visualise the live European electricity market:

  1. **Cross-border flows** (default-on) — one polyline per measured
     interconnector flow (`ZoneFlowLines()`), drawn exporting-zone →
     importing-zone, coloured by flow magnitude (light→dark blue) and
     labelled with the MW figure.
  2. **Zone day-ahead prices** (default-on) — one bubble per bidding zone
     (`ZonePriceMarkers()`), coloured on a green→red price ramp and labelled
     with the zone code and €/MWh.

Both layers query helper functions applied to the live DB by
`feeders/entsoe/fabric/helpers.kql`.

Idempotent: re-running drops the two entsoe layers by name and re-creates
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

WORKSPACE = "c98acd97-4363-4296-8323-b6ab21e53903"
KQL_DB_ID = "a08303ed-4148-4c4d-b0fd-7ad5eb882e68"
MAP_NAME = "ENTSO-E Market Map"
MAP_DESC = "Live European electricity market — cross-border physical flows and day-ahead bidding-zone prices (ENTSO-E Transparency Platform)."

NAME_FLOWS = "entsoe cross-border flows"
NAME_PRICES = "entsoe zone prices"
LAYER_NAMES = {NAME_FLOWS, NAME_PRICES}

# Bounded colour buckets so the map `match` expressions stay finite.
# Cross-border flows use a dark, multi-hue magnitude ramp (blue = light load
# -> purple -> red = heavy load) so direction-paired arrows differentiate
# strongly against the grey basemap.
FLOW_COLORS = ["#67001f", "#b2182b", "#762a83", "#225ea8", "#2b8cbe"]  # >=2500 / >=1200 / >=600 / >=200 / <200 MW
PRICE_COLORS = ["#1a9641", "#a6d96a", "#ffffbf", "#fdae61", "#d7191c"]  # cheap→expensive


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
KQL_FLOWS = """ZoneFlowLines()
| extend stroke_color = case(abs(quantity) >= 2500, '%s', abs(quantity) >= 1200, '%s', abs(quantity) >= 600, '%s', abs(quantity) >= 200, '%s', '%s')
| project geometry, label, out_zone, in_zone, quantity, stroke_weight, stroke_color
""" % (FLOW_COLORS[0], FLOW_COLORS[1], FLOW_COLORS[2], FLOW_COLORS[3], FLOW_COLORS[4])

KQL_PRICES = """ZonePriceMarkers()
| extend fill_color = case(price >= 150, '%s', price >= 120, '%s', price >= 90, '%s', price >= 60, '%s', '%s')
| project geometry, label, zone, price, fill_color
""" % (PRICE_COLORS[4], PRICE_COLORS[3], PRICE_COLORS[2], PRICE_COLORS[1], PRICE_COLORS[0])


def _match_expr(get_col: str, colors: list[str]) -> list:
    expr = ["match", ["get", get_col]]
    for c in colors:
        expr += [c, c]
    expr.append("#888888")  # fallback
    return expr


def _custom_colors(colors: list[str]) -> dict:
    return {c: c for c in colors}


def flows_layer() -> dict:
    return {
        "name": NAME_FLOWS, "kql": KQL_FLOWS, "geometryColumnName": "geometry",
        "filters": [],
        "options": {
            "type": "vector", "visible": True,
            "lineOptions": {
                "strokeWidth": 3, "strokeOpacity": 0.9,
                "strokeColor": _match_expr("stroke_color", FLOW_COLORS),
                "enableSeriesGroup": True, "seriesGroup": "stroke_color",
                "customColors": _custom_colors(FLOW_COLORS),
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": {"enabled": True, "size": 11, "color": "#1a1a1a",
                                  "textStrokeColor": "#FFFFFF", "textStrokeWidth": 2.5,
                                  "allowOverlap": False},
            "tooltipKeys": ["label", "out_zone", "in_zone", "quantity"],
            "enablePopups": True,
        },
    }


def prices_layer() -> dict:
    return {
        "name": NAME_PRICES, "kql": KQL_PRICES, "geometryColumnName": "geometry",
        "filters": [],
        "options": {
            "type": "vector", "visible": True, "pointLayerType": "bubble",
            "bubbleOptions": {
                "color": _match_expr("fill_color", PRICE_COLORS),
                "radius": 11, "strokeColor": "#FFFFFF", "strokeWidth": 2,
                "opacity": 0.95, "enableSeriesGroup": True,
                "seriesGroup": "fill_color", "customColors": _custom_colors(PRICE_COLORS),
            },
            "dataLabelKeys": ["label"],
            "dataLabelOptions": {"enabled": True, "size": 13, "color": "#111111",
                                  "textStrokeColor": "#FFFFFF", "textStrokeWidth": 2.5,
                                  "allowOverlap": True},
            "tooltipKeys": ["zone", "price"],
            "enablePopups": True,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=WORKSPACE)
    ap.add_argument("--db", default=KQL_DB_ID)
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
        print("Creating Map item …")
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
        # non-LRO direct response path
        st2, _, body2 = api("POST",
                            f"{FABRIC}/workspaces/{args.workspace}/items/{map_id}/getDefinition", ft)
        res = body2
    parts = {p["path"]: p for p in res["definition"]["parts"]}

    if "map.json" in parts:
        mp = json.loads(base64.b64decode(parts["map.json"]["payload"]))
    else:
        mp = {"layerSources": [], "layerSettings": [], "dataSources": []}
        parts["map.json"] = {"path": "map.json", "payload": "", "payloadType": "InlineBase64"}

    # drop previously-wired entsoe layers (idempotent)
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

    # basemap centred on Europe
    bm = mp.setdefault("basemap", {})
    o = bm.setdefault("options", {})
    o.setdefault("style", "road_shaded_relief")
    o.setdefault("center", [9.0, 50.2])
    o.setdefault("zoom", 4.2)
    o.setdefault("showLabels", True)
    c = bm.setdefault("controls", {})
    for k in ("zoom", "scale", "style", "compass"):
        c.setdefault(k, True)

    # wire layers (flows under prices)
    for layer in (flows_layer(), prices_layer()):
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
