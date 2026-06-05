# NASA FIRMS Fabric assets

Post-deploy artefacts for the **nasa-firms** real-time-sources bridge: a global
Fabric **Map** built for **OSINT fire monitoring**. It visualises the live state
of active fires worldwide — every VIIRS / MODIS thermal-anomaly detection from
[NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) — as fire hotspots and
individual detections coloured by Fire Radiative Power (FRP).

The data plane (ACI/notebook + Event Hubs/Eventstream + KQL database into
`_cloudevents_dispatch`) is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` (and `deploy-feeder-notebook.ps1`)
scripts, which also apply `kql/nasa-firms.kql` (the typed tables and
materialized views the map consumes). The generic deployer auto-discovers
`feeders/nasa-firms/fabric/post-deploy.ps1` via the common
`{source}/fabric/post-deploy.ps1` hook convention and calls it at the end of a
successful deploy.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by the generic deployer. Acquires a Kusto management token, applies the helper functions and caching policies in `helpers.kql` to the live `nasa-firms` database (one statement per call), then runs `build_map.py` with the workspace / KQL-db / cluster IDs taken from the deployer's `-Context` hashtable. Idempotent; can also be run standalone after a tweak. |
| `build_map.py` | Idempotently creates/updates the `Map` item *NASA FIRMS Global Fire Map*: a coarse 1-degree fire-hotspot bubble layer for the world/continental overview (world→zoom 5) plus a DWD-style 0.1-degree fire-intensity **tile** layer shown at all zoom levels, both Kusto-backed and coloured on the shared FRP heat ramp. The tile tooltip carries the full per-cell OSINT summary, so there is no separate per-detection point layer. |
| `helpers.kql` | Additive geometry/reference helper functions consumed by the map — `FireColor()`, `FireRadius()`, `ConfidenceRank()`, `RecentFireDetections()`, `FireFootprints()`, `FireGrid()`, `FireHeat()`, `FireHotspots()` — plus hot-cache policies sized for the OSINT dashboard window. Re-applied on every deploy by the hook. **Additive only:** it never alters the generated tables, mappings, materialized views, or update policies in `kql/nasa-firms.kql`. |

## Prerequisites

1. The generic per-source bootstrap has already run for `nasa-firms`, e.g.:

   ```powershell
   ./tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source nasa-firms -Workspace <ws-guid>
   ```

   This creates the `nasa-firms` KQL database, applies `kql/nasa-firms.kql`
   (the `NASA.FIRMS.FireDetection` / `NASA.FIRMS.DataAvailability` tables and
   their `*Latest` materialized views the map binds to), creates the
   Eventstream + `_cloudevents_dispatch` destination, and starts the feeder.
   Live detections require a valid `FIRMS_MAP_KEY` (free NASA Earthdata key).

2. `az login` to the tenant that owns the Fabric workspace, with permission to
   read/write Map items and run Kusto management commands on the database.

3. Python 3.10+ on `PATH` (the hook calls `python build_map.py`).

## Running standalone

```powershell
./feeders/nasa-firms/fabric/post-deploy.ps1 `
    -WorkspaceId  <workspace-guid> `
    -KqlDatabaseId <kql-db-guid> `
    -KustoUri     https://<eventhouse>.kusto.fabric.microsoft.com `
    -KustoDatabase nasa-firms
```

or, to (re)build only the map:

```powershell
python ./feeders/nasa-firms/fabric/build_map.py --workspace <ws-guid> --db <kql-db-guid>
```

## Map design (OSINT focus)

| Layer | Source | Symbology | Default | Purpose |
| ----- | ------ | --------- | ------- | ------- |
| **nasa-firms hotspots** | `FireHotspots(72h, 1.0)` | Grid-cell bubbles sized by detection count, coloured by total FRP (yellow→dark-red) | on, world→zoom 5 | Zoomed-out overview: spot the world's most active fire regions at a glance, where the 0.1° tiles are still sub-pixel. |
| **nasa-firms fire tiles** | `FireGrid(24h, 0.1)` | One filled square polygon per populated 0.1° grid cell, coloured on a continuous FRP `interpolate` ramp by the cell's peak FRP. Rich tooltip with peak/total FRP, max brightness, detection count, confidence breakdown (high/nominal/low), day-night split, contributing instruments / satellites / sources, and first/last-seen time | on, **all zoom levels** | The single all-zoom detail layer: a bounded, DWD-style tile field showing fire intensity *and* the full per-cell OSINT summary per region. Replaces both the per-pixel footprint layer and the per-detection point layer. |

> [!NOTE]
> **Tiles are the only detail layer — the per-detection point layer was
> removed.** Everything that used to live on individual detection bubbles
> (instrument, satellite, source, confidence, day/night, brightness, acquisition
> time) is now aggregated onto the tile tooltip per 0.1° cell, and the tiles
> render at **every** zoom level. The coarse 1° hotspot bubbles remain only as
> the zoomed-out overview (they are legible when a single tile is smaller than a
> pixel). `RecentFireDetections()` is still available as a helper for ad-hoc
> queries but is no longer wired as a map layer.

> [!IMPORTANT]
> **Why tiles, not raw per-pixel footprints (the DWD pattern).** A live Kusto
> map layer runs its query **globally** — Fabric does **not** inject the map
> viewport/zoom into the KQL, and `minZoom` only gates *rendering*, not the
> query — against a **hard 20 MB result cap** that cannot be raised. One GeoJSON
> polygon per raw detection (`FireFootprints()`, ~70k+ polygons/day ≈ 39 MB)
> trips that cap, and bounding it with a global `top-N by FRP` is lossy (a region
> of all-low-FRP fires shows nothing). The **DWD ICON-D2 map** never hits the cap
> because it draws **tiles**: a fixed lat/lon grid of square polygons whose row
> count is bounded by *grid resolution*, not by *event count*. This map adopts
> the same pattern — `FireGrid(24h, 0.1)` aggregates detections onto a 0.1° grid
> (the ICON-D2 tile size) and emits one tile per populated cell. At a busy 24 h
> (~75k raw detections) that is ~17k tiles ≈ **7 MB**, well under the cap, with
> **complete global coverage and no top-N truncation**.
>
> `FireFootprints()` (the exact `scan`×`track` per-pixel rectangle) is retained
> as a helper for the case where true per-pixel extent is required: render it as
> a **PMTiles vector tileset** (tiles fetched per-viewport → no 20 MB query cap),
> built locally in Python because the Fabric `BuildTileset` polygon path is
> broken. Tracked as a follow-up; it is **not** wired as a live Kusto layer.

A dark global basemap (`grayscale_dark`, centred near the equator) makes the
fire colours read clearly. Both layers refresh every 60 s. Tune the lookback
windows, the 1-degree hotspot grid, or the 0.1-degree tile grid by editing the
`KQL_HOTSPOTS` / `KQL_TILES` queries in `build_map.py` or the helper-function
defaults in `helpers.kql`.
