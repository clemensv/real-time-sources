"""Build a RiverGeometries Kusto script from Azure Maps vector tiles.

Source: Azure Maps tileset ``microsoft.base.labels`` exposes a ``River label``
layer with named LineString geometries that exactly match what the Fabric Map
basemap renders. This means our overlay rivers visually align with the
underlying basemap rivers - no jitter, no mismatched bends.

Process:
  1. Cover Germany at zoom 12 (~17,940 tiles - parallelised, ~15 min wallclock).
  2. Fetch each MVT tile, decode, extract "River label" features.
  3. Convert per-tile pixel coords (0..4096) to lon/lat using tile bounds.
  4. Group LineStrings by ``name``; merge segments that share endpoints.
  5. Match against the pegelonline river names with aliases.
  6. Emit per-row ``.append`` commands. The output is ~1 MB and exceeds the
     Kusto mgmt-API per-command limit, so post-deploy splits it on blank
     lines and posts each command separately.

Auth: requires environment variable ``MAPS_KEY`` (Azure Maps shared key) or a
``--maps-key`` argument. The key for any Azure Maps account in the
subscription works; the API charges per-tile transactions (~18k tiles per
full run, well under the S1 free tier).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import mapbox_vector_tile
import mercantile

# (water_shortname, water_longname) -> aliases to look up in MVT
ALIASES: List[Tuple[str, str, Sequence[str]]] = [
    ("RHEIN", "RHEIN", ("Rhein", "Rhine", "Rhin", "Niederrhein", "Oberrhein", "Hochrhein")),
    ("ELBE", "ELBE", ("Elbe", "Norderelbe", "Süderelbe", "Suederelbe")),
    ("DONAU", "DONAU", ("Donau", "Danube")),
    ("MOSEL", "MOSEL", ("Mosel", "Moselle")),
    ("WESER", "WESER", ("Weser",)),
    ("MAIN", "MAIN", ("Main",)),
    ("EMS", "EMS", ("Ems",)),
    ("ODER", "ODER", ("Oder", "Odra")),
    ("HAVEL", "UNTERE HAVEL-WASSERSTRASSE", ("Havel",)),
    ("HAVEL", "OBERE HAVEL-WASSERSTRASSE", ("Havel",)),
    ("HAVEL", "HAVEL-ODER-WASSERSTRASSE", ("Havel",)),
    ("SAALE", "SAALE", ("Saale",)),
    ("WERRA", "WERRA", ("Werra",)),
    ("FULDA", "FULDA", ("Fulda",)),
    ("LAHN", "LAHN", ("Lahn",)),
    ("SAAR", "SAAR", ("Saar", "Sarre")),
    ("NECKAR", "NECKAR", ("Neckar",)),
    ("ALLER", "ALLER", ("Aller",)),
    ("RUHR", "RUHR", ("Ruhr",)),
    ("LEINE", "LEINE", ("Leine",)),
    ("ISAR", "ISAR", ("Isar",)),
    ("INN", "INN", ("Inn",)),
    ("SPREE", "SPREE-ODER-WASSERSTRASSE", ("Spree",)),
    ("PEENE", "PEENE", ("Peene",)),
    ("REGEN", "REGEN", ("Regen",)),
]

GERMANY_BBOX = (5.5, 47.0, 15.5, 55.5)  # lon_min, lat_min, lon_max, lat_max
DEFAULT_ZOOM = 12
EXTENT = 4096
PARALLEL_WORKERS = 24


def fetch_tile(z: int, x: int, y: int, key: str) -> bytes:
    url = (
        "https://atlas.microsoft.com/map/tile?api-version=2.1"
        f"&tilesetId=microsoft.base.labels&zoom={z}&x={x}&y={y}"
        f"&subscription-key={key}"
    )
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read()


def tile_pixel_to_lonlat(
    px: float, py: float, bounds: mercantile.LngLatBbox
) -> Tuple[float, float]:
    """Convert MVT pixel coords (0..EXTENT, origin bottom-left) to lon/lat."""
    lon = bounds.west + (px / EXTENT) * (bounds.east - bounds.west)
    lat = bounds.south + (py / EXTENT) * (bounds.north - bounds.south)
    return lon, lat


def extract_river_segments(
    raw: bytes, bounds: mercantile.LngLatBbox
) -> Dict[str, List[List[Tuple[float, float]]]]:
    """Return {river_name: [list-of-linestrings-in-lonlat]}."""
    try:
        tile = mapbox_vector_tile.decode(raw)
    except Exception:
        return {}
    out: Dict[str, List[List[Tuple[float, float]]]] = defaultdict(list)
    layer = tile.get("River label") or {}
    for ft in layer.get("features", []):
        name = (ft.get("properties") or {}).get("name")
        if not name:
            continue
        g = ft.get("geometry") or {}
        gtype = g.get("type")
        coords = g.get("coordinates") or []
        if gtype == "LineString":
            lines = [coords]
        elif gtype == "MultiLineString":
            lines = coords
        else:
            continue
        for line in lines:
            converted = [tile_pixel_to_lonlat(p[0], p[1], bounds) for p in line]
            if len(converted) >= 2:
                out[name].append(converted)
    return out


def tiles_for_bbox(bbox: Tuple[float, float, float, float], zoom: int) -> Iterable[mercantile.Tile]:
    return mercantile.tiles(*bbox, zooms=[zoom])


def merge_segments(
    segments: List[List[Tuple[float, float]]], tol: float = 0.005
) -> List[List[Tuple[float, float]]]:
    """Greedy join of segments whose endpoints are within ``tol`` degrees."""
    remaining = [list(s) for s in segments]
    merged: List[List[Tuple[float, float]]] = []
    while remaining:
        current = remaining.pop(0)
        changed = True
        while changed:
            changed = False
            for i, other in enumerate(remaining):
                if not other:
                    continue
                if _close(current[-1], other[0], tol):
                    current.extend(other[1:])
                    remaining.pop(i)
                    changed = True
                    break
                if _close(current[-1], other[-1], tol):
                    current.extend(list(reversed(other))[1:])
                    remaining.pop(i)
                    changed = True
                    break
                if _close(current[0], other[-1], tol):
                    current = other + current[1:]
                    remaining.pop(i)
                    changed = True
                    break
                if _close(current[0], other[0], tol):
                    current = list(reversed(other)) + current[1:]
                    remaining.pop(i)
                    changed = True
                    break
        merged.append(current)
    return merged


def _close(a: Tuple[float, float], b: Tuple[float, float], tol: float) -> bool:
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def round_coords(line: List[Tuple[float, float]], digits: int = 5) -> List[List[float]]:
    return [[round(x, digits), round(y, digits)] for x, y in line]


def crawl(zoom: int, key: str, bbox=GERMANY_BBOX) -> Dict[str, List[List[Tuple[float, float]]]]:
    tiles = list(tiles_for_bbox(bbox, zoom))
    print(f"crawling {len(tiles)} tiles at zoom {zoom} with {PARALLEL_WORKERS} workers", file=sys.stderr)
    rivers: Dict[str, List[List[Tuple[float, float]]]] = defaultdict(list)

    def fetch_and_parse(t: mercantile.Tile):
        try:
            raw = fetch_tile(t.z, t.x, t.y, key)
        except Exception as exc:
            return t, exc, {}
        bounds = mercantile.bounds(t)
        return t, None, extract_river_segments(raw, bounds)

    done = 0
    with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as pool:
        futs = [pool.submit(fetch_and_parse, t) for t in tiles]
        for fut in as_completed(futs):
            t, err, per_tile = fut.result()
            done += 1
            if err is not None:
                if done % 200 == 0:
                    print(f"  tile {t.z}/{t.x}/{t.y} ERR {err}", file=sys.stderr)
            for name, segs in per_tile.items():
                rivers[name].extend(segs)
            if done % 250 == 0:
                print(
                    f"  {done}/{len(tiles)} tiles, {len(rivers)} river-names",
                    file=sys.stderr,
                )
    return rivers


def build_table_rows(
    rivers: Dict[str, List[List[Tuple[float, float]]]]
) -> List[Tuple[str, str, dict]]:
    """Match Azure Maps river names against our ALIASES and emit table rows."""
    # Lower-case index of MVT names -> merged geometry
    indexed: Dict[str, List[List[Tuple[float, float]]]] = {
        name.lower(): merge_segments(segs) for name, segs in rivers.items()
    }
    rows: List[Tuple[str, str, dict]] = []
    for short, longn, aliases in ALIASES:
        match_segs: List[List[Tuple[float, float]]] = []
        matched_alias = None
        for alias in aliases:
            segs = indexed.get(alias.lower())
            if segs:
                match_segs.extend(segs)
                matched_alias = alias
                break
        if not match_segs:
            print(f"  MISSING: {short} / {longn} (aliases={list(aliases)})", file=sys.stderr)
            continue
        # final merge across alias variants
        final = merge_segments(match_segs)
        # keep only segments with at least 4 vertices to drop noise
        final = [s for s in final if len(s) >= 4]
        if not final:
            print(f"  EMPTY: {short} / {longn}", file=sys.stderr)
            continue
        coords = [round_coords(s) for s in final]
        geometry = (
            {"type": "LineString", "coordinates": coords[0]}
            if len(coords) == 1
            else {"type": "MultiLineString", "coordinates": coords}
        )
        total = sum(len(s) for s in coords)
        print(
            f"  OK {short:15s}/{longn:35s} alias={matched_alias:8s} segs={len(coords)} coords={total}",
            file=sys.stderr,
        )
        rows.append((short, longn, geometry))
    return rows


def emit_kql(rows: List[Tuple[str, str, dict]]) -> str:
    """Emit per-river .append commands to stay under the mgmt payload limit.

    The first command drops + recreates the table; subsequent ones append one
    row each. The driver script splits on the blank-line separator and posts
    each command individually.
    """
    parts = [
        ".drop table RiverGeometries ifexists",
        ".create table RiverGeometries"
        " (water_shortname:string, water_longname:string, geometry:dynamic)"
        " with (folder='Map')",
    ]
    for short, longn, geom in rows:
        geom_lit = "dynamic(" + json.dumps(geom, separators=(",", ":")) + ")"
        parts.append(
            ".append RiverGeometries <|\n"
            "print water_shortname=\"" + short + "\","
            " water_longname=\"" + longn + "\","
            " geometry=" + geom_lit
        )
    return "\n\n".join(parts) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="river_geometries.kql", type=Path)
    ap.add_argument("--zoom", default=DEFAULT_ZOOM, type=int)
    ap.add_argument("--maps-key", default=os.environ.get("MAPS_KEY"))
    args = ap.parse_args()

    if not args.maps_key:
        print("ERROR: provide MAPS_KEY env var or --maps-key", file=sys.stderr)
        return 2

    rivers = crawl(args.zoom, args.maps_key)
    rows = build_table_rows(rivers)
    kql = emit_kql(rows)
    args.out.write_text(kql, encoding="utf-8")
    print(
        f"wrote {args.out.resolve()} ({len(kql)} chars, {len(rows)} rivers)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
