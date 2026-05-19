"""Build a RiverGeometries Kusto script from Azure Maps tiles + station fallback.

Two-source pipeline that covers every pegelonline water-body with a polyline:

1. **MVT geometry** (preferred): Azure Maps ``microsoft.base.labels`` exposes a
   ``River label`` layer with named LineStrings that match the basemap pixel-
   for-pixel. Used for the ~30 named rivers/canals it actually labels.

2. **Station backbone** (fallback): for canals and tributaries Azure Maps does
   *not* label (e.g. Mittellandkanal, Dortmund-Ems-Kanal, Rhein-Herne-Kanal,
   Elbeseitenkanal, Küstenkanal, Stör, Hunte, Aller, Eider, ...), the script
   queries the pegelonline ``Station`` table and synthesises a polyline by
   connecting station coordinates ordered by river-km.

Coverage:
  * MVT bbox extends to NL (Waal/Lek/IJssel) and CZ (Vltava/Ohře/Jizera).
  * Station fallback covers every water with ≥2 stations that have valid
    coordinates and km.
  * Lakes / coastal areas (OSTSEE, NORDSEE, BODENSEE, KLEINES HAFF, ...) are
    explicitly skipped — they aren't lineable.

The output is ~1-2 MB and exceeds the Kusto mgmt-API per-command limit, so
post-deploy splits it on blank lines and posts each command separately.

Auth: requires ``MAPS_KEY`` env var (any Azure Maps key in the sub) for the
MVT crawl, and ``KUSTO_TOKEN`` (bearer token for the Fabric cluster) for the
station-backbone fallback. If ``KUSTO_TOKEN`` is unset, the script will try
``az account get-access-token --resource <cluster>``.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import mapbox_vector_tile
import mercantile

# (water_shortname, water_longname) -> aliases to look up in MVT.
# Names observed in microsoft.base.labels River label layer across DE/NL/CZ
# (zoom 12 sample, May 2026).
ALIASES: List[Tuple[str, str, Sequence[str]]] = [
    ("RHEIN", "RHEIN", ("Rhein", "Rhine", "Rhin", "Niederrhein", "Oberrhein", "Hochrhein")),
    ("ELBE", "ELBE", ("Elbe", "Labe", "Norderelbe", "Süderelbe", "Suederelbe")),
    ("DONAU", "DONAU", ("Donau", "Danube", "Alte Donau")),
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
    ("SAAR", "SAAR", ("Saar", "Sarre", "La Sarre")),
    ("NECKAR", "NECKAR", ("Neckar",)),
    ("ALLER", "ALLER", ("Aller",)),
    ("RUHR", "RUHR", ("Ruhr",)),
    ("LEINE", "LEINE", ("Leine",)),
    ("ISAR", "ISAR", ("Isar",)),
    ("INN", "INN", ("Inn",)),
    ("SPREE", "SPREE-ODER-WASSERSTRASSE", ("Spree", "Spréva")),
    ("PEENE", "PEENE", ("Peene",)),
    ("REGEN", "REGEN", ("Regen",)),
    # Newly-discovered MVT names that map to pegelonline waters.
    ("NOK", "NORD-OSTSEE-KANAL", ("Nord-Ostsee-Kanal",)),
    ("MDK", "MAIN-DONAU-KANAL", ("Main-Donau-Kanal",)),
    ("WAAL", "WAAL", ("Waal", "Boven-Merwede", "Nieuwe-Merwede")),
    ("IJSSEL", "IJSSEL", ("IJssel",)),
    ("LEK", "LEK", ("Lek", "Neder-Rijn")),
    ("ALTE_MAAS", "ALTE MAAS", ("Maas", "Bergsche Maas")),
    ("NEUE_MAAS", "NEUE MAAS", ("Nieuwe Maas", "Nieuwe Waterweg")),
    ("EGER", "OHRE", ("Ohře", "Ohre", "Eger")),
    ("MOLDAU", "VLATAVA", ("Vltava", "Vlatava", "Moldau")),
    ("Jizera", "JIZERA", ("Jizera",)),
    ("Orlice", "ORLICE", ("Orlice",)),
    ("Ploucnice", "PLOUCNICE", ("Ploučnice", "Ploucnice")),
]

# Waters to skip entirely (lakes, seas, single-point stations, named bays).
SKIP_WATERS = {
    "OSTSEE", "NORDSEE", "BODENSEE", "KLEINES HAFF",
    "DYHRSSENMOOR",  # single-point moor pond, all stations within 30 m
}

# Fabric Kusto cluster URI for pegelonline workspace
KUSTO_CLUSTER = "https://trd-3exhyahspeuvzukrju.z1.kusto.fabric.microsoft.com"
KUSTO_DB = "pegelonline"

# bbox covers DE + NL (Waal/Lek/IJssel) + CZ borders (Vltava/Ohře/Jizera/Ploučnice)
GERMANY_BBOX = (3.5, 46.8, 16.5, 55.5)
DEFAULT_ZOOM = 12
EXTENT = 4096
PARALLEL_WORKERS = 24
MIN_STATIONS_FOR_BACKBONE = 2


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


def crawl(zoom: int, key: str, bbox=GERMANY_BBOX, cache_path: Optional[Path] = None) -> Dict[str, List[List[Tuple[float, float]]]]:
    if cache_path and cache_path.exists():
        print(f"loading MVT cache from {cache_path}", file=sys.stderr)
        raw = json.loads(cache_path.read_text(encoding="utf-8"))
        return {name: [[tuple(p) for p in seg] for seg in segs] for name, segs in raw.items()}

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
    if cache_path:
        cache_path.write_text(json.dumps(rivers), encoding="utf-8")
        print(f"wrote MVT cache to {cache_path}", file=sys.stderr)
    return rivers


def build_table_rows(
    rivers: Dict[str, List[List[Tuple[float, float]]]]
) -> Tuple[List[Tuple[str, str, dict, str]], set]:
    """Match Azure Maps river names against ALIASES and emit (short, long, geom, source) rows.

    Returns ``(rows, matched_keys)`` where ``matched_keys`` is the set of
    ``(water_shortname, water_longname)`` tuples covered by MVT so the caller
    can synthesise station-backbone polylines for the rest.
    """
    indexed: Dict[str, List[List[Tuple[float, float]]]] = {
        name.lower(): merge_segments(segs) for name, segs in rivers.items()
    }
    rows: List[Tuple[str, str, dict, str]] = []
    matched: set = set()
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
            print(f"  MVT-MISS: {short} / {longn} (aliases={list(aliases)})", file=sys.stderr)
            continue
        final = merge_segments(match_segs)
        final = [s for s in final if len(s) >= 4]
        if not final:
            print(f"  MVT-EMPTY: {short} / {longn}", file=sys.stderr)
            continue
        coords = [round_coords(s) for s in final]
        geometry = (
            {"type": "LineString", "coordinates": coords[0]}
            if len(coords) == 1
            else {"type": "MultiLineString", "coordinates": coords}
        )
        total = sum(len(s) for s in coords)
        print(
            f"  MVT OK  {short:15s}/{longn:35s} alias={matched_alias:18s} segs={len(coords)} coords={total}",
            file=sys.stderr,
        )
        rows.append((short, longn, geometry, "mvt"))
        matched.add((short, longn))
    return rows, matched


def kusto_token() -> str:
    tok = os.environ.get("KUSTO_TOKEN")
    if tok:
        return tok
    out = subprocess.run(
        ["az", "account", "get-access-token", "--resource", KUSTO_CLUSTER, "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, shell=True,
    )
    if out.returncode != 0:
        raise RuntimeError("Could not obtain Kusto token: " + out.stderr)
    return out.stdout.strip()


def kusto_query(csl: str) -> List[List]:
    body = json.dumps({"db": KUSTO_DB, "csl": csl}).encode("utf-8")
    req = urllib.request.Request(
        f"{KUSTO_CLUSTER}/v1/rest/query",
        data=body,
        headers={
            "Authorization": "Bearer " + kusto_token(),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    return data["Tables"][0]["Rows"]


def fetch_station_backbones(matched: set) -> List[Tuple[str, str, dict, str]]:
    """Build station-interpolated polylines for waters not covered by MVT.

    Queries pegelonline Station table (collapsing snapshots per station_id via
    arg_max(___time)), groups stations per (water_shortname, water_longname),
    filters out invalid coords / km, orders by km, and emits a LineString per
    water with ≥2 valid stations.
    """
    csl = (
        "Station "
        "| extend ws=tostring(water.shortname), wl=tostring(water.longname) "
        "| where isnotempty(ws) and isnotempty(wl) "
        "| where longitude > 0 and latitude > 0 "
        "| where isnotnull(km) and km > -1 "
        "| summarize arg_max(___time, longitude, latitude, km, ws, wl) by station_id "
        "| project ws, wl, station_id, km, longitude, latitude "
        "| order by ws asc, wl asc, km asc"
    )
    print("  querying Kusto for station backbones...", file=sys.stderr)
    rows = kusto_query(csl)
    print(f"  got {len(rows)} unique stations from Kusto", file=sys.stderr)

    by_water: Dict[Tuple[str, str], List[Tuple[float, float, float]]] = defaultdict(list)
    for ws, wl, _station_id, km, lon, lat in rows:
        by_water[(ws, wl)].append((float(km), float(lon), float(lat)))

    out: List[Tuple[str, str, dict, str]] = []
    skipped_lake = 0
    skipped_few = 0
    for (ws, wl), pts in sorted(by_water.items()):
        if (ws, wl) in matched:
            continue
        if wl in SKIP_WATERS or ws in SKIP_WATERS:
            skipped_lake += 1
            continue
        pts.sort(key=lambda p: p[0])
        coords = [[round(p[1], 5), round(p[2], 5)] for p in pts]
        # Dedupe consecutive duplicates
        deduped: List[List[float]] = []
        for c in coords:
            if not deduped or deduped[-1] != c:
                deduped.append(c)
        if len(deduped) < MIN_STATIONS_FOR_BACKBONE:
            skipped_few += 1
            continue
        geometry = {"type": "LineString", "coordinates": deduped}
        out.append((ws, wl, geometry, "stations"))
        print(
            f"  STN OK  {ws:15s}/{wl:35s} stations={len(deduped)}",
            file=sys.stderr,
        )
    print(
        f"  station backbones: {len(out)} emitted, "
        f"{skipped_lake} lakes/seas skipped, {skipped_few} too few stations",
        file=sys.stderr,
    )
    return out


def emit_kql(rows: List[Tuple[str, str, dict, str]]) -> str:
    """Emit per-river .append commands to stay under the mgmt payload limit.

    The first command drops + recreates the table; subsequent ones append one
    row each. The driver script splits on the blank-line separator and posts
    each command individually. ``source`` is ``mvt`` or ``stations`` so the
    KQL helpers and the map UI can distinguish high-fidelity from synthesised
    polylines.
    """
    parts = [
        ".drop table RiverGeometries ifexists",
        ".create table RiverGeometries"
        " (water_shortname:string, water_longname:string, geometry:dynamic, source:string)"
        " with (folder='Map')",
    ]
    for short, longn, geom, source in rows:
        geom_lit = "dynamic(" + json.dumps(geom, separators=(",", ":")) + ")"
        # KQL string literals: escape backslashes and double quotes
        short_lit = short.replace("\\", "\\\\").replace('"', '\\"')
        longn_lit = longn.replace("\\", "\\\\").replace('"', '\\"')
        parts.append(
            ".append RiverGeometries <|\n"
            f'print water_shortname="{short_lit}",'
            f' water_longname="{longn_lit}",'
            f' geometry={geom_lit},'
            f' source="{source}"'
        )
    return "\n\n".join(parts) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="river_geometries.kql", type=Path)
    ap.add_argument("--zoom", default=DEFAULT_ZOOM, type=int)
    ap.add_argument("--maps-key", default=os.environ.get("MAPS_KEY"))
    ap.add_argument(
        "--skip-stations", action="store_true",
        help="Skip station-backbone fallback (MVT-only output)",
    )
    ap.add_argument(
        "--mvt-cache", type=Path, default=None,
        help="Cache decoded MVT segments to/from this JSON file for re-runs.",
    )
    args = ap.parse_args()

    if not args.maps_key:
        print("ERROR: provide MAPS_KEY env var or --maps-key", file=sys.stderr)
        return 2

    rivers = crawl(args.zoom, args.maps_key, cache_path=args.mvt_cache)
    mvt_rows, matched = build_table_rows(rivers)
    if args.skip_stations:
        rows = mvt_rows
    else:
        try:
            station_rows = fetch_station_backbones(matched)
        except Exception as exc:
            print(f"  WARN: station fallback failed: {exc}", file=sys.stderr)
            station_rows = []
        rows = mvt_rows + station_rows
    kql = emit_kql(rows)
    args.out.write_text(kql, encoding="utf-8")
    mvt_n = sum(1 for r in rows if r[3] == "mvt")
    stn_n = sum(1 for r in rows if r[3] == "stations")
    print(
        f"wrote {args.out.resolve()} ({len(kql)} chars, {len(rows)} rows: "
        f"{mvt_n} mvt + {stn_n} station-backbone)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
