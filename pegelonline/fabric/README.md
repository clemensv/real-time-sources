# pegelonline Fabric assets

Post-deploy artefacts for the **pegelonline** real-time-sources bridge: an
8-layer Fabric Map that visualises the live state of the German Federal
Waterways gauge network (~800 stations along the Rhein, Elbe, Donau, Main,
Weser, Mosel, Neckar, Oder and their tributaries, plus all federal
shipping canals).

The data plane (ACI + Event Hubs + KQL database + Eventstream into
`_cloudevents_dispatch`) is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` script, which also applies
`kql/pegelonline.kql` (containing every helper function the map consumes).
The generic deployer auto-discovers `pegelonline/fabric/post-deploy.ps1`
via the common `{source}/fabric/post-deploy.ps1` hook convention and calls
it at the end of a successful deploy.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1`. Acquires Fabric + Kusto tokens, ingests `river_geometries.kql` into the `RiverSegments` table (with per-command retry on HTTP 429), then runs `wire_pegelonline_map.py` with the workspace/db/cluster IDs from the deployer's `-Context` hashtable. Can also be run standalone after layer tweaks. |
| `wire_pegelonline_map.py` | Idempotently (re)wires 8 Kusto-backed vector layers onto an existing Fabric Map item: hydrological state, navigation state, 1h / 3h / 6h / 24h trend, data freshness, station labels. |
| `build_river_geometries.py` | Generates `river_geometries.kql` from an Azure Maps MVT crawl of `microsoft.base.labels` (named river / canal polylines) with a pegelonline station-backbone fallback for waters Azure Maps doesn't label. Run once per release; output is committed. Requires `MAPS_KEY`. |
| `river_geometries.kql` | Committed output of the build script. ~1.4 MB, ~1 950 `.append` rows declaring one polyline per gauge across ~75 waters (Mittellandkanal, Nord-Ostsee-Kanal, Müritz-Elde-Wasserstrasse, etc. all included). Replayed on every deploy by the hook. |

## Prerequisites

1. The generic per-source bootstrap has already run for `pegelonline`:

   ```powershell
   ./tools/deploy-fabric/deploy-fabric.ps1 -Source pegelonline `
       -ResourceGroup rg-pegelonline -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```

   This creates the `pegelonline` KQL database, applies the schemas
   (`kql/pegelonline.kql`, including the `EnrichedMeasurements()`,
   `CurrentByStation()`, `StateSegments()`, `NavSegments()`, `TrendBase()`,
   `TrendSegments1h/3h/6h/24h()`, `FreshSegments()`, and `StationLabels()`
   helper functions consumed by the map), creates the Eventstream + dispatch
   destination, and deploys the ACI.

2. **A blank Fabric Map item exists** in the workspace. The Fabric REST API
   does not (yet) expose programmatic creation of Map items, so create one
   once via the portal (`+ New > Map`) and note its item ID.

3. The map item ID is exposed to the hook via the `PEGELONLINE_FABRIC_MAP_ID`
   environment variable. If the variable is not set, the hook exits 0 with a
   notice rather than failing the bootstrap.

## Auto-invocation

```powershell
$env:PEGELONLINE_FABRIC_MAP_ID = "<map-item-guid>"
./tools/deploy-fabric/deploy-fabric.ps1 -Source pegelonline `
    -ResourceGroup rg-pegelonline -Workspace "<ws-guid>"
# ...generic 6 steps...
# [7/7] Running post-deploy hook (pegelonline/fabric/post-deploy.ps1)...
#   [pegelonline post-deploy] Ingesting RiverSegments from river_geometries.kql ...
#   [pegelonline post-deploy] RiverSegments: 1949 ok / 0 failed (of 1949 commands).
#   pegelonline hydrological state: wired (default-on=True)
#   pegelonline navigation state  : wired (default-on=False)
#   pegelonline 1h trend          : wired (default-on=False)
#   pegelonline 3h trend          : wired (default-on=False)
#   pegelonline 6h trend          : wired (default-on=False)
#   pegelonline 24h trend         : wired (default-on=False)
#   pegelonline data freshness    : wired (default-on=False)
#   pegelonline station labels    : wired (default-on=True)
#   Map updated.
```

Skip with `-SkipPostDeployHook` if needed.

## Standalone re-wire

After tweaking colour ramps, KQL bodies, or adding layers in
`wire_pegelonline_map.py`:

```powershell
$env:PEGELONLINE_FABRIC_MAP_ID = "<map-item-guid>"
./pegelonline/fabric/post-deploy.ps1 `
    -Workspace   "<workspace-guid>" `
    -KqlDatabaseId "<kql-db-guid>" `
    -KustoUri      "https://trd-xxxxxxxx.z1.kusto.fabric.microsoft.com"
```

The script removes its previously-managed layers (matched by the name
prefix `pegelonline `) before adding the current set, so re-runs are safe.

## What the map looks like

8 layers, all driven by the KQL helper functions in
`pegelonline/kql/pegelonline.kql`. Default-on layers are starred.

| # | Layer | Geometry | Colour encoding | Default | Source function |
| - | ----- | -------- | --------------- | ------- | --------------- |
| 1 | Hydrological state * | River line segments (one per gauge) | Diverging RdYlBu on `stateMnwMhw` (very-low / low / normal / high / very-high) | yes | `StateSegments()` |
| 2 | Navigation state | River line segments | Same RdYlBu palette on `stateNswHsw` (below GlW / NSW / normal / approaching HSW / above HSW) | no | `NavSegments()` |
| 3 | 1 h trend | River line segments | Direction over last 1 h; width ~ \|delta\| | no | `TrendSegments1h()` |
| 4 | 3 h trend | River line segments | Direction over last 3 h | no | `TrendSegments3h()` |
| 5 | 6 h trend | River line segments | Direction over last 6 h | no | `TrendSegments6h()` |
| 6 | 24 h trend | River line segments | Direction over last 24 h | no | `TrendSegments24h()` |
| 7 | Data freshness | River line segments | Categorical on age band (fresh / stale / old / very-old / no-data) | no | `FreshSegments()` |
| 8 | Station labels * | Text bubble | `shortname  NNN cm`; black with white halo, shown at zoom >= 9 | yes | `StationLabels()` |

### Colour rationale

* **Hydrological / Navigation state** use the ColorBrewer 5-class diverging
  `RdYlBu` palette, anchored at "normal = green" so a healthy river is
  visually calm and both extremes are loud:
  `very-high #d7191c` -> `high #fdae61` -> `normal #1a9850` ->
  `low #2c7bb6` -> `very-low #08306b`. Stations with no published reference
  marks are grey `#7f7f7f`. The two state layers reuse the same hex codes
  so once the eye has learned "red = attention, blue = unusually low,
  green = nominal", toggling between them only changes *what kind* of
  trouble each level represents.
* **Trend layers** (1h / 3h / 6h / 24h) share a 5-class diverging palette
  where red and dark blue are reserved for *extreme* rates (sustained
  > 3 cm/h, e.g. flash floods, dam releases, tidal ebb on the Weser
  estuary): `extreme-rise #d7191c` -> `rising #fdae61` ->
  `steady #ffffbf` -> `falling #abd9e9` -> `extreme-fall #2c7bb6`. Grey
  is reserved strictly for "no reference reading available" - never used
  for an actual measured trend.
* **Freshness** is a green -> amber -> red traffic-light that fades to
  grey once a station is stale enough to be considered offline, so a
  long-dead gauge doesn't scream louder than a real flood on the state
  layer above it.

### Trend computation

All trend layers are computed from our own ingested `CurrentMeasurement`
table (no external feed). Shared parametrised helper
`TrendBase(window:timespan)` picks per station the reading closest to
`(now - window)` that falls inside the tolerance band
`[0.5*window, max(1.5*window, window+6h)]`, converts the delta to a rate
in cm/h, and bucketises it:

| Rate (cm/h) | Bucket | Colour |
| ----------- | ------ | ------ |
| > +3.0 | extreme-rise | red |
| +0.25 to +3.0 | rising | orange |
| -0.25 to +0.25 | steady | pale yellow |
| -3.0 to -0.25 | falling | light blue |
| < -3.0 | extreme-fall | blue |
| (no reading in tolerance) | unknown | grey |

Stroke width scales with `|delta_cm|` over a per-window cap
(`window * 10 cm/h`), so a 100 cm/24h move and a 100 cm/1h move don't
render identically. Labels always carry the actual elapsed window
(e.g. `KOELN  + +12 cm/3h`).

### Filters

Filters on `water_shortname` / `agency` are not applied by the wire
script - add them once in the Fabric portal and they persist across
re-runs because the script only manages `layerSettings` / `layerSources`
named with the `pegelonline ` prefix.
