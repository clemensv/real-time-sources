# tfl-cycles Fabric assets

Post-deploy artefacts for the **tfl-cycles** real-time-sources feeder (Transport
for London **Santander Cycles** — London public bikeshare): a live Fabric
**Map** visualisation of TfL's ~798 **fixed** BikePoint docking stations and
their live bike/dock availability. The data plane is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` script (ACI + Event Hubs + KQL database
+ Eventstream into `_cloudevents_dispatch`). The generic deployer auto-discovers
`tfl-cycles/fabric/post-deploy.ps1` via the common
"`{source}/fabric/post-deploy.ps1`" hook convention and calls it at the end of a
successful deploy.

Unlike the moving-vehicle **hsl-hfp** map this mirrors, tfl-cycles is a
**fixed docking-station** feed. Station *identity + location + capacity* arrive
as `StationInformation` reference records; live *bike / dock counts* arrive as
`StationStatus` telemetry. Both are keyed by the stable `station_id` (e.g.
`BikePoints_1`), so every station layer **joins** the two materialized views on
`station_id`. The map is parametric in the KQL database name and auto-discovers
the source's bounding box from `tflcycles_bbox()` (falling back to the raw
station footprint, then to central London).

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1`. Acquires Fabric + Kusto tokens, then runs `wire_tfl_cycles_map.py` with the workspace/db/cluster IDs from the deployer's `-Context` hashtable (keys `WorkspaceId`, `DatabaseId`, `EventhouseClusterUri`, `DatabaseName`). Auto-creates a blank Map item named `tfl-cycles-map` if `TFL_CYCLES_FABRIC_MAP_ID` is not set (override the name with `TFL_CYCLES_FABRIC_MAP_NAME`). Can also be run standalone. |
| `wire_tfl_cycles_map.py` | Installs the `tflcycles_*` KQL helper functions in the target database and idempotently wires the corresponding Fabric Map vector layers via `getDefinition` / `updateDefinition`. Auto-centres the basemap on the source's bounding box. |

## Layers shipped

| # | Layer name | Default | Zoom | Source query | Geometry | Colour / label |
| - | ---------- | ------- | ---- | ------------ | -------- | -------------- |
| 1 | tfl-cycles station availability | on | any | `tflcycles_stations()` | Point (bubble) | colour by `fill_state` (bike-availability band); **radius scales with `capacity`**; tooltip `name` / bikes / empty docks / capacity |
| 2 | tfl-cycles station labels | on | z14+ | `tflcycles_stations()` | Point (tiny bubble + data label) | text label `name  -  N bikes / M docks` |
| 3 | tfl-cycles empty docks | **off** | any | `tflcycles_stations()` | Point (bubble) | colour by `docks_state` (empty-dock supply); for riders returning a bike |

All three layers read the single enriched helper `tflcycles_stations()` and just
pick a different colour column off it (exactly how hsl-hfp reuses
`hslhfp_vehicle_points` for both its vehicles and punctuality layers). Only
`is_installed` stations with non-null, non-`0,0` coordinates are shown.

The **availability palette** (red → green, "not enough bikes" → "plenty of
bikes"): No bikes `#d7191c`, Few bikes `#fdae61`, Bikes available `#a6d96a`,
Plenty of bikes `#1a9641`. The **empty-docks palette** (red → blue, "nowhere to
return" → "plenty of docks"): No docks `#d7191c`, Few docks `#fdae61`, Docks
available `#74add1`, Plenty of docks `#2c7bb6`.

Bubble **radius** is data-driven from a KQL-computed `radius` column
(`4 + 1.4·√capacity`, clamped to 4–16 px) via a `["get", "radius"]` paint
expression — the same data-driven-radius pattern used by
`nasa-firms/fabric/build_map.py`. This is the one deliberate departure from
hsl-hfp's fixed-radius bubbles, needed to honour "size by capacity".

## Schema assumed (freshly-deployed tfl_cycles database)

Bracketed, dotted CloudEvents tables created by `tfl-cycles/kql/tfl-cycles.kql`:

  * `['UK.Gov.TfL.Cycles.StationInformation']` + MV
    `['UK.Gov.TfL.Cycles.StationInformationLatest']` — reference: `station_id`,
    `name`, `lat`, `lon`, `terminal_name`, `capacity`, `temporary`,
    `install_date`, `removal_date`. **Location lives here only.**
  * `['UK.Gov.TfL.Cycles.StationStatus']` + MV
    `['UK.Gov.TfL.Cycles.StationStatusLatest']` — telemetry: `station_id`,
    `num_bikes_available`, `num_standard_bikes_available`, `num_ebikes_available`,
    `num_empty_docks`, `num_docks`, `is_installed`, `is_locked`, `modified`.
    **Availability lives here only.**

Both `<X>Latest` MVs are `arg_max(___time, *) by ___type, ___source, ___subject`
so each layer query is constant-time regardless of how long the source has been
ingesting. `station_id` (e.g. `BikePoints_1`) is stable across refreshes and is
the join key between the two views.

## The KQL the layers use

`tflcycles_stations()` performs the reference⋈telemetry join and bakes the
colour bands, the capacity-scaled `radius`, and a human `label`:

```kql
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
    | extend ['fill_state'] = case(
        num_bikes_available <= 0, "No bikes",
        isnull(['avail_ratio']),  "Bikes available",
        ['avail_ratio'] < 0.25,   "Few bikes",
        ['avail_ratio'] < 0.75,   "Bikes available",
        "Plenty of bikes")
    | extend ['radius'] = round(min_of(16.0, max_of(4.0, 4.0 + 1.4 * sqrt(coalesce(todouble(capacity), todouble(num_docks), 0.0)))), 1)
    | extend ['label'] = strcat(['name'], " - ", tostring(num_bikes_available), " bikes / ", tostring(num_empty_docks), " docks")
    | extend ['geometry'] = bag_pack("type", "Point", "coordinates", pack_array(lon, lat))
    | project ['geometry'], station_id, ['name'], ... , ['fill_state'], ['fill_color'],
              ['docks_state'], ['docks_color'], ['radius'], ['label']
}
```

`tflcycles_bbox()` is `tflcycles_stations() | summarize` of the 1 %/99 %
lat/lon quantiles used to auto-fit the basemap. The full bodies live in
`wire_tfl_cycles_map.py` (`TFL_CYCLES_FUNCTIONS`).

### Column-naming / reserved-keyword notes

KQL rejects bare reserved words as identifiers with a generic HTTP 400 and no
syntax detail (this bit the hsl-hfp live test with `long`). tfl-cycles uses
`lon` (not `long`) so that specific collision does not apply, but as a matter of
hygiene **every derived/projected column is bracket-quoted** (`['fill_state']`,
`['avail_ratio']`, `['radius']`, `['geometry']`, ...) and given an explicit safe
name — no computed column is ever called `kind`, `type`, `bool`, etc. The
availability bands use `fill_state` / `avail_ratio`; the empty-dock bands use
`docks_state` / `empty_ratio`.

## Prerequisites

1. The generic per-source bootstrap has already run for `tfl-cycles`:
   ```powershell
   ./tools/deploy-fabric/deploy-fabric.ps1 -Source tfl-cycles `
       -ResourceGroup rg-tfl -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```
   This applies `tfl-cycles/kql/tfl-cycles.kql` (database `tfl_cycles`) and
   stands up the rest of the data plane.

2. **A blank Fabric Map item exists** in the workspace, or you let the hook
   auto-create one. The Fabric REST API doesn't (yet) expose programmatic
   creation of `Map` items via the typed surface, but the generic `items` API
   accepts `type=Map`, so this hook does that transparently when
   `TFL_CYCLES_FABRIC_MAP_ID` is empty.

3. The map item ID is exposed to the hook via the `TFL_CYCLES_FABRIC_MAP_ID`
   environment variable. If absent the hook creates / reuses a Map named
   `tfl-cycles-map` (override with `TFL_CYCLES_FABRIC_MAP_NAME`).

## Auto-invocation

```powershell
$env:TFL_CYCLES_FABRIC_MAP_ID = "<map-guid>"  # optional; will be auto-created
./tools/deploy-fabric/deploy-fabric.ps1 -Source tfl-cycles `
    -ResourceGroup rg-tfl -Workspace "<ws-guid>"
# ...generic steps...
# [6/6] Running post-deploy hook (tfl-cycles/fabric/post-deploy.ps1)...
#   Creating 2 helper functions in tfl_cycles
#   Discovering bounding box from tflcycles_bbox()
#     798 stations; lat=[51.46, 51.55] lon=[-0.24, 0.00]
#   layer tfl-cycles station availability
#     rows: 796
#     palette fill_state: 4 colors
#   ...
#   OK - map <map-guid> updated with 3 layers
```

Skip with `-SkipPostDeployHook` if you only want the data plane.

## Standalone re-wire / re-fit the bbox

Re-running is safe and idempotent: the script removes the layers it previously
wired (matched by their KQL source's `itemId` binding) and recreates them, and
re-fits the basemap bounding box to whatever stations are currently indexed. So
the normal edit loop — and the "run it again once data has arrived so the map
centres on London instead of the fallback" step — is just:

```powershell
$env:TFL_CYCLES_FABRIC_MAP_ID = "<map-guid>"
./feeders/tfl-cycles/fabric/post-deploy.ps1 `
    -WorkspaceId   "<ws-guid>" `
    -KqlDatabaseId "<kqldb-guid>" `
    -KustoUri      "https://trd-xxxxxxxx.z1.kusto.fabric.microsoft.com" `
    -KustoDatabase "tfl_cycles"
```

`FABRIC_TOKEN` and `KUSTO_TOKEN` are acquired via `az account get-access-token`
automatically if not already set in the environment.

The wiring script can also be invoked directly:

```powershell
python ./feeders/tfl-cycles/fabric/wire_tfl_cycles_map.py `
    --workspace-id <ws> --map-id <map> --kql-db-id <kqldb> `
    --kusto-uri https://<cluster>.kusto.fabric.microsoft.com --kusto-db tfl_cycles
```

## Why both `seriesGroup` AND a `match` expression?

Empirically, Fabric Maps' documented `enableSeriesGroup` + `seriesGroup` +
`customColors` schema populates the Data Layers panel legend correctly but does
**not** drive per-feature paint colour — all bubbles fall back to the static
fallback `color` (grey). What actually renders is a MapLibre-style
`["match", ["get", column], v1, c1, ..., fallback]` expression on the paint
property.

The wire script writes **both** at deploy time: `customColors` (for the panel
legend) and the `match` expression (for the renderer). The distinct values are
enumerated from the live query result so the palette stays in sync with the
data — colouring by `fill_state` / `docks_state` picks up the exact set of
bands present.
