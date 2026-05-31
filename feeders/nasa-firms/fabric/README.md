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
| `build_map.py` | Idempotently creates/updates the `Map` item *NASA FIRMS Global Fire Map*: a 1-degree fire-hotspot bubble layer (world view) plus an individual fire-detection bubble layer (mid/high zoom), both Kusto-backed and coloured on the shared FRP heat ramp. |
| `helpers.kql` | Additive geometry/reference helper functions consumed by the map — `FireColor()`, `FireRadius()`, `ConfidenceRank()`, `RecentFireDetections()`, `FireFootprints()`, `FireHeat()`, `FireHotspots()` — plus hot-cache policies sized for the OSINT dashboard window. Re-applied on every deploy by the hook. **Additive only:** it never alters the generated tables, mappings, materialized views, or update policies in `kql/nasa-firms.kql`. |

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
| **nasa-firms hotspots** | `FireHotspots(72h, 1.0)` | Grid-cell bubbles sized by detection count, coloured by total FRP (yellow→dark-red) | on, world→zoom 5 | Spot the world's most active fire regions at a glance. |
| **nasa-firms detections** | `RecentFireDetections(24h, 0)` | One bubble per detection, sized + coloured by FRP, tooltip with instrument / satellite / confidence / day-night / acquisition time | on, zoom 3–8 | Reveal where a fire complex sits once zoomed in. |
| **nasa-firms footprints** | `FireFootprints(24h, 0)` | One filled polygon per detection — the true `scan`×`track` ground rectangle of the satellite pixel — coloured by FRP, outlined, tooltip adds the scan/track dimensions | on, zoom ≥ 8 | Show the real ground extent of each VIIRS/MODIS thermal-anomaly pixel at high zoom. |

A dark global basemap (`grayscale_dark`, centred near the equator) makes the
fire colours read clearly. Both layers refresh every 60 s. Tune the lookback
windows and the 1-degree hotspot grid by editing the `KQL_HOTSPOTS` /
`KQL_DETECTIONS` queries in `build_map.py` or the helper-function defaults in
`helpers.kql`.
