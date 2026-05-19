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


# ---------------------------------------------------------------------------
# Per-station segmentation
# ---------------------------------------------------------------------------

def _dist_sq(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def _interp(p: Tuple[float, float], q: Tuple[float, float], t: float) -> Tuple[float, float]:
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def assign_stations_to_lines(
    lines: List[List[Tuple[float, float]]],
    stations: List[Tuple[str, float, float]],
    max_dist_deg: float = 0.5,
) -> Dict[int, List[Tuple[int, str, float, float]]]:
    """For each station, find its nearest vertex across all lines and route it
    to that line. Returns ``{line_index: [(vertex_index, station_id, lon, lat)]}``.
    Stations whose nearest vertex is more than ``max_dist_deg`` away are
    dropped (probably belong to a different water or an off-channel oxbow).
    """
    per_line: Dict[int, List[Tuple[int, str, float, float]]] = defaultdict(list)
    max_d_sq = max_dist_deg * max_dist_deg
    for sid, sx, sy in stations:
        best = (float("inf"), -1, -1)  # (dist_sq, line_idx, vertex_idx)
        for li, line in enumerate(lines):
            for vi, v in enumerate(line):
                d = _dist_sq((sx, sy), v)
                if d < best[0]:
                    best = (d, li, vi)
        if best[1] < 0 or best[0] > max_d_sq:
            continue
        per_line[best[1]].append((best[2], sid, sx, sy))
    return per_line


def split_polyline_per_station(
    line: List[Tuple[float, float]],
    assignments: List[Tuple[int, str, float, float]],
) -> List[Tuple[str, List[List[float]]]]:
    """Split a single polyline into one segment per station.

    The boundary between adjacent stations is placed at the midpoint of the
    segment between their nearest-vertex indices. Each emitted segment
    includes the midpoint vertices on both sides so adjacent segments share
    endpoints (no visual gaps in the rendered ribbon).
    """
    if len(line) < 2 or not assignments:
        return []

    # If two stations share the same nearest vertex, keep insertion order but
    # nudge subsequent ones to the next vertex so each gets a distinct slice.
    assignments = sorted(assignments, key=lambda a: a[0])
    seen_idx: Dict[int, int] = {}
    nudged: List[Tuple[int, str, float, float]] = []
    for idx, sid, sx, sy in assignments:
        cur = idx
        while cur in seen_idx and cur + 1 < len(line):
            cur += 1
        seen_idx[cur] = 1
        nudged.append((cur, sid, sx, sy))
    nudged.sort(key=lambda a: a[0])

    out: List[Tuple[str, List[List[float]]]] = []
    n = len(nudged)
    for i, (vidx, sid, _sx, _sy) in enumerate(nudged):
        # boundary to previous neighbour
        if i == 0:
            start_idx = 0
            start_mid: Optional[Tuple[float, float]] = None
        else:
            prev_vidx = nudged[i - 1][0]
            mid_idx = (prev_vidx + vidx) // 2
            start_idx = mid_idx + 1
            if mid_idx + 1 < len(line):
                # midpoint between vertices mid_idx and mid_idx+1
                start_mid = _interp(line[mid_idx], line[mid_idx + 1], 0.5)
            else:
                start_mid = None
        # boundary to next neighbour
        if i == n - 1:
            end_idx = len(line) - 1
            end_mid: Optional[Tuple[float, float]] = None
        else:
            next_vidx = nudged[i + 1][0]
            mid_idx = (vidx + next_vidx) // 2
            end_idx = mid_idx
            if mid_idx + 1 < len(line):
                end_mid = _interp(line[mid_idx], line[mid_idx + 1], 0.5)
            else:
                end_mid = None

        seg: List[Tuple[float, float]] = []
        if start_mid is not None:
            seg.append(start_mid)
        seg.extend(line[start_idx:end_idx + 1])
        if end_mid is not None:
            seg.append(end_mid)
        if len(seg) >= 2:
            out.append((sid, round_coords(seg)))
    return out


def fetch_stations_per_water() -> Dict[Tuple[str, str], List[Tuple[str, float, float]]]:
    """Return {(water_shortname, water_longname): [(station_id, lon, lat), ...]}.

    Uses arg_max per station_id so each station appears once with its latest
    coordinates. Stations with invalid coords are filtered out.
    """
    csl = (
        "Station "
        "| extend ws=tostring(water.shortname), wl=tostring(water.longname) "
        "| where isnotempty(ws) and isnotempty(wl) "
        "| where longitude > 0 and latitude > 0 "
        "| summarize arg_max(___time, longitude, latitude, km, ws, wl) by station_id "
        "| project ws, wl, station_id, km, longitude, latitude "
        "| order by ws asc, wl asc, km asc"
    )
    rows = kusto_query(csl)
    out: Dict[Tuple[str, str], List[Tuple[str, float, float]]] = defaultdict(list)
    for ws, wl, sid, _km, lon, lat in rows:
        out[(ws, wl)].append((sid, float(lon), float(lat)))
    return out


def build_segment_rows(
    rivers: Dict[str, List[List[Tuple[float, float]]]],
) -> List[Tuple[str, str, str, dict, str]]:
    """End-to-end: MVT lines + station-backbone fallback, then per-station split.

    Returns list of ``(water_shortname, water_longname, station_id, geometry, source)``.
    """
    # Build per-water polylines: MVT-matched first, then station-backbone fallback.
    indexed: Dict[str, List[List[Tuple[float, float]]]] = {
        name.lower(): merge_segments(segs) for name, segs in rivers.items()
    }
    print("  querying Kusto for per-water stations...", file=sys.stderr)
    stations_per_water = fetch_stations_per_water()
    print(f"  got {sum(len(v) for v in stations_per_water.values())} unique stations "
          f"across {len(stations_per_water)} waters", file=sys.stderr)

    water_lines: Dict[Tuple[str, str], Tuple[List[List[Tuple[float, float]]], str]] = {}

    # 1. MVT-matched waters
    matched: set = set()
    for short, longn, aliases in ALIASES:
        segs: List[List[Tuple[float, float]]] = []
        matched_alias = None
        for alias in aliases:
            cand = indexed.get(alias.lower())
            if cand:
                segs.extend(cand)
                matched_alias = alias
                break
        if not segs:
            continue
        final = [s for s in merge_segments(segs) if len(s) >= 4]
        if not final:
            continue
        water_lines[(short, longn)] = (final, "mvt")
        matched.add((short, longn))
        print(f"  MVT  {short:15s}/{longn:35s} alias={matched_alias:18s} lines={len(final)}",
              file=sys.stderr)

    # 2. Station-backbone fallback for remaining waters
    skipped_lake = skipped_few = 0
    for (ws, wl), stations in sorted(stations_per_water.items()):
        if (ws, wl) in matched:
            continue
        if wl in SKIP_WATERS or ws in SKIP_WATERS:
            skipped_lake += 1
            continue
        coords = [[lon, lat] for _sid, lon, lat in stations]
        deduped: List[List[float]] = []
        for c in coords:
            if not deduped or deduped[-1] != c:
                deduped.append(c)
        if len(deduped) < MIN_STATIONS_FOR_BACKBONE:
            skipped_few += 1
            continue
        water_lines[(ws, wl)] = ([[tuple(c) for c in deduped]], "stations")
        print(f"  STN  {ws:15s}/{wl:35s} stations={len(deduped)}", file=sys.stderr)
    print(f"  station-backbone: {sum(1 for k,v in water_lines.items() if v[1]=='stations')} emitted, "
          f"{skipped_lake} lakes/seas skipped, {skipped_few} too few stations", file=sys.stderr)

    # 3. For each water polyline, split into per-station segments.
    rows: List[Tuple[str, str, str, dict, str]] = []
    n_seg = 0
    for (ws, wl), (lines, source) in sorted(water_lines.items()):
        stations = stations_per_water.get((ws, wl), [])
        if not stations:
            print(f"  NO-STATIONS {ws}/{wl}", file=sys.stderr)
            continue
        per_line = assign_stations_to_lines(lines, stations)
        emitted = 0
        for li, line in enumerate(lines):
            assigns = per_line.get(li, [])
            if not assigns:
                continue
            segs = split_polyline_per_station(list(line), assigns)
            for sid, coords in segs:
                geometry = {"type": "LineString", "coordinates": coords}
                rows.append((ws, wl, sid, geometry, source))
                emitted += 1
        if emitted:
            n_seg += emitted
    print(f"  total segments: {n_seg} across {len(water_lines)} waters", file=sys.stderr)
    return rows


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


def emit_segments_kql(rows: List[Tuple[str, str, str, dict, str]]) -> str:
    """Emit per-segment .append commands to stay under the mgmt payload limit.

    The first command drops + recreates RiverSegments; subsequent ones append
    one row each. The driver script (post-deploy.ps1) splits on the blank-line
    separator and posts each command individually.
    """
    parts = [
        ".drop table RiverSegments ifexists",
        ".create table RiverSegments"
        " (water_shortname:string, water_longname:string, station_id:string,"
        " geometry:dynamic, source:string)"
        " with (folder='Map')",
    ]
    for ws, wl, sid, geom, source in rows:
        geom_lit = "dynamic(" + json.dumps(geom, separators=(",", ":")) + ")"
        ws_lit  = ws.replace("\\", "\\\\").replace('"', '\\"')
        wl_lit  = wl.replace("\\", "\\\\").replace('"', '\\"')
        sid_lit = sid.replace("\\", "\\\\").replace('"', '\\"')
        parts.append(
            ".append RiverSegments <|\n"
            f'print water_shortname="{ws_lit}",'
            f' water_longname="{wl_lit}",'
            f' station_id="{sid_lit}",'
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
        "--mvt-cache", type=Path, default=None,
        help="Cache decoded MVT segments to/from this JSON file for re-runs.",
    )
    args = ap.parse_args()

    if not args.maps_key:
        print("ERROR: provide MAPS_KEY env var or --maps-key", file=sys.stderr)
        return 2

    rivers = crawl(args.zoom, args.maps_key, cache_path=args.mvt_cache)
    rows = build_segment_rows(rivers)
    kql = emit_segments_kql(rows)
    args.out.write_text(kql, encoding="utf-8")
    mvt_n = sum(1 for r in rows if r[4] == "mvt")
    stn_n = sum(1 for r in rows if r[4] == "stations")
    waters = {(r[0], r[1]) for r in rows}
    print(
        f"wrote {args.out.resolve()} ({len(kql)} chars, {len(rows)} segment-rows "
        f"across {len(waters)} waters: {mvt_n} mvt + {stn_n} station-backbone)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
