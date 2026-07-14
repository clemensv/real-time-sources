# taipei-youbike Fabric assets

Post-deploy artefacts for the **taipei-youbike** real-time-sources feeder
(**YouBike 2.0 Taiwan** — Taiwan's dominant station-based public bikeshare): a
live Fabric **Map** visualisation of YouBike's ~9,348 **fixed** docking stations
and their live bike/dock availability. The data plane is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` script (ACI + Event Hubs + KQL database
+ Eventstream into `_cloudevents_dispatch`). The generic deployer auto-discovers
`taipei-youbike/fabric/post-deploy.ps1` via the common
"`{source}/fabric/post-deploy.ps1`" hook convention and calls it at the end of a
successful deploy.

Like the sibling **tfl-cycles** map it mirrors (structurally isomorphic — both
are bikeshare feeders with a `StationInformation` reference + `StationStatus`
telemetry keyed by `station_id`), taipei-youbike is a **fixed docking-station**
feed. Station *identity + location + capacity* arrive as `StationInformation`
reference records; live *bike / dock counts* arrive as `StationStatus`
telemetry. Both are keyed by the stable `station_id` (e.g. `500101001`), so every
station layer **joins** the two materialized views on `station_id`. The map is
parametric in the KQL database name and auto-discovers the source's bounding box
from `taipeiyoubike_bbox()` (falling back to the raw station footprint, then to
central Taipei).

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1`. Acquires Fabric + Kusto tokens, then runs `wire_taipei_youbike_map.py` with the workspace/db/cluster IDs from the deployer's `-Context` hashtable (keys `WorkspaceId`, `DatabaseId`, `EventhouseClusterUri`, `DatabaseName`). Auto-creates a blank Map item named `taipei-youbike-map` if `TAIPEI_YOUBIKE_FABRIC_MAP_ID` is not set (override the name with `TAIPEI_YOUBIKE_FABRIC_MAP_NAME`). Can also be run standalone. |
| `wire_taipei_youbike_map.py` | Installs the `taipeiyoubike_*` KQL helper functions in the target database and idempotently wires the corresponding Fabric Map vector layers via `getDefinition` / `updateDefinition`. Auto-centres the basemap on the source's bounding box. |

## Layers shipped

| # | Layer name | Default | Zoom | Source query | Geometry | Colour / label |
| - | ---------- | ------- | ---- | ------------ | -------- | -------------- |
| 1 | taipei-youbike station availability | on | any | `taipeiyoubike_stations()` | Point (bubble) | colour by `fill_state` (bike-availability band); **radius scales with `capacity`**; tooltip `name_en` / bikes / empty docks / capacity |
| 2 | taipei-youbike station labels | on | z14+ | `taipeiyoubike_stations()` | Point (tiny bubble + data label) | text label `name_en  -  N bikes / M docks` |
| 3 | taipei-youbike empty docks | **off** | any | `taipeiyoubike_stations()` | Point (bubble) | colour by `docks_state` (empty-dock supply); for riders returning a bike |

All three layers read the single enriched helper `taipeiyoubike_stations()` and
just pick a different colour column off it (exactly how the sibling tfl-cycles
map reuses `tflcycles_stations` for both its availability and empty-dock layers).
Only stations with non-null, non-`0,0` coordinates are shown; the "empty docks"
overlay recolours the same stations so the red `No docks` band highlights the
stations with `num_empty_docks == 0` (docks full) — and the availability layer's
red `No bikes` band highlights `num_bikes_available == 0`.

The **availability palette** (red → green, "not enough bikes" → "plenty of
bikes"): No bikes `#d7191c`, Few bikes `#fdae61`, Bikes available `#a6d96a`,
Plenty of bikes `#1a9641`. The **empty-docks palette** (red → blue, "nowhere to
return" → "plenty of docks"): No docks `#d7191c`, Few docks `#fdae61`, Docks
available `#74add1`, Plenty of docks `#2c7bb6`.

Bubble **radius** is data-driven from a KQL-computed `radius` column
(`4 + 1.4·√capacity`, clamped to 4–16 px) via a `["get", "radius"]` paint
expression — the same data-driven-radius pattern used by the tfl-cycles map and
`nasa-firms/fabric/build_map.py`. This honours "size by capacity".

## Schema assumed (freshly-deployed taipei_youbike database)

Bracketed, dotted CloudEvents tables created by
`taipei-youbike/kql/taipei-youbike.kql`:

  * `['TW.YouBike.StationInformation']` + MV
    `['TW.YouBike.StationInformationLatest']` — reference: `station_id`,
    `name_tw` / `name_en` / `name_cn`, `district_tw` / `district_en` /
    `district_cn`, `address_tw` / `address_en` / `address_cn`, `lat`, `lon`,
    `capacity`, `station_type`, `country_code`, `area_code`, `img`.
    **Location lives here only.**
  * `['TW.YouBike.StationStatus']` + MV
    `['TW.YouBike.StationStatusLatest']` — telemetry: `station_id`,
    `num_bikes_available`, `num_bikes_yb1`, `num_bikes_yb2`,
    `num_ebikes_available`, `num_empty_docks`, `num_forbidden_docks`,
    `availability_level`, `service_status`, `updated_at`, `snapshot_time`.
    **Availability lives here only.**

Both `<X>Latest` MVs are `arg_max(___time, *) by ___type, ___source, ___subject`
so each layer query is constant-time regardless of how long the source has been
ingesting. `station_id` (e.g. `500101001`) is stable across refreshes and is the
join key between the two views.

## The KQL the layers use

`taipeiyoubike_stations()` performs the reference⋈telemetry join and bakes the
colour bands, the capacity-scaled `radius`, and a human `label`:

```kql
.create-or-alter function with (folder = "Map", skipvalidation = "true") taipeiyoubike_stations() {
    ['TW.YouBike.StationInformationLatest']
    | where isnotnull(lat) and isnotnull(lon) and lat != 0.0 and lon != 0.0
    | project station_id, ['name_en'], ['name_tw'], ['district_en'], lat, lon, capacity
    | join kind=inner (
        ['TW.YouBike.StationStatusLatest']
        | project station_id, num_bikes_available, num_bikes_yb1, num_bikes_yb2,
                  num_ebikes_available, num_empty_docks, num_forbidden_docks,
                  availability_level, service_status, updated_at
      ) on station_id
    | extend ['total_docks'] = num_bikes_available + num_empty_docks
    | extend ['denom'] = iff(isnotnull(capacity) and capacity > 0, todouble(capacity), todouble(['total_docks']))
    | extend ['avail_ratio'] = iff(isnotnull(['denom']) and ['denom'] > 0.0, todouble(num_bikes_available) / ['denom'], real(null))
    | extend ['fill_state'] = case(
        num_bikes_available <= 0, "No bikes",
        isnull(['avail_ratio']),  "Bikes available",
        ['avail_ratio'] < 0.25,   "Few bikes",
        ['avail_ratio'] < 0.75,   "Bikes available",
        "Plenty of bikes")
    | extend ['radius'] = round(min_of(16.0, max_of(4.0, 4.0 + 1.4 * sqrt(coalesce(todouble(capacity), todouble(['total_docks']), 0.0)))), 1)
    | extend ['label'] = strcat(['name_en'], " - ", tostring(num_bikes_available), " bikes / ", tostring(num_empty_docks), " docks")
    | extend ['geometry'] = bag_pack("type", "Point", "coordinates", pack_array(lon, lat))
    | project ['geometry'], station_id, ['name_en'], ..., ['fill_state'], ['fill_color'],
              ['docks_state'], ['docks_color'], ['radius'], ['label']
}
```

`taipeiyoubike_bbox()` is `taipeiyoubike_stations() | summarize` of the 1 %/99 %
lat/lon quantiles used to auto-fit the basemap. The full bodies live in
`wire_taipei_youbike_map.py` (`TAIPEI_YOUBIKE_FUNCTIONS`).

### Column-naming / reserved-keyword notes

KQL rejects bare reserved words as identifiers with a generic HTTP 400 and no
syntax detail (this bit the hsl-hfp live test with `long`). taipei-youbike uses
`lon` (not `long`) so that specific collision does not apply, but as a matter of
hygiene **every derived/projected column is bracket-quoted** (`['fill_state']`,
`['avail_ratio']`, `['radius']`, `['geometry']`, `['total_docks']`, ...) and
given an explicit safe name — no computed column is ever called `kind`, `type`,
`bool`, etc. The bracketed, dotted table names (`['TW.YouBike.StationStatus']`)
are quoted everywhere. The availability bands use `fill_state` / `avail_ratio`;
the empty-dock bands use `docks_state` / `empty_ratio`.

## Prerequisites

1. The generic per-source bootstrap has already run for `taipei-youbike`:
   ```powershell
   ./tools/deploy-fabric/deploy-fabric.ps1 -Source taipei-youbike `
       -ResourceGroup rg-youbike -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```
   This applies `taipei-youbike/kql/taipei-youbike.kql` (database `taipei_youbike`)
   and stands up the rest of the data plane.

2. **A blank Fabric Map item exists** in the workspace, or you let the hook
   auto-create one. The Fabric REST API doesn't (yet) expose programmatic
   creation of `Map` items via the typed surface, but the generic `items` API
   accepts `type=Map`, so this hook does that transparently when
   `TAIPEI_YOUBIKE_FABRIC_MAP_ID` is empty.

3. The map item ID is exposed to the hook via the `TAIPEI_YOUBIKE_FABRIC_MAP_ID`
   environment variable. If absent the hook creates / reuses a Map named
   `taipei-youbike-map` (override with `TAIPEI_YOUBIKE_FABRIC_MAP_NAME`).

## Auto-invocation

```powershell
$env:TAIPEI_YOUBIKE_FABRIC_MAP_ID = "<map-guid>"  # optional; will be auto-created
./tools/deploy-fabric/deploy-fabric.ps1 -Source taipei-youbike `
    -ResourceGroup rg-youbike -Workspace "<ws-guid>"
# ...generic steps...
# [6/6] Running post-deploy hook (taipei-youbike/fabric/post-deploy.ps1)...
#   Creating 2 helper functions in taipei_youbike
#   Discovering bounding box from taipeiyoubike_bbox()
#     9348 stations; lat=[22.55, 25.17] lon=[120.18, 121.64]
#   layer taipei-youbike station availability
#     rows: 9348
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
centres on Taiwan instead of the fallback" step — is just:

```powershell
$env:TAIPEI_YOUBIKE_FABRIC_MAP_ID = "<map-guid>"
./feeders/taipei-youbike/fabric/post-deploy.ps1 `
    -WorkspaceId   "<ws-guid>" `
    -KqlDatabaseId "<kqldb-guid>" `
    -KustoUri      "https://trd-xxxxxxxx.z6.kusto.fabric.microsoft.com" `
    -KustoDatabase "taipei_youbike"
```

`FABRIC_TOKEN` and `KUSTO_TOKEN` are acquired via `az account get-access-token`
automatically if not already set in the environment.

The wiring script can also be invoked directly:

```powershell
python ./feeders/taipei-youbike/fabric/wire_taipei_youbike_map.py `
    --workspace-id <ws> --map-id <map> --kql-db-id <kqldb> `
    --kusto-uri https://<cluster>.kusto.fabric.microsoft.com --kusto-db taipei_youbike
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