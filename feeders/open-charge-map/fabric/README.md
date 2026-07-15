# open-charge-map Fabric assets

Post-deploy artefacts for the **open-charge-map** real-time-sources feeder (Open
Charge Map — the largest global open registry of EV charging equipment): a live
Fabric **Map** visualisation of the world's electric-vehicle **charging
locations** and their operational status, usage type and bay count. The data
plane is handled by the generic `tools/deploy-fabric/deploy-fabric.ps1` script
(ACI + Event Hubs + KQL database + Eventstream into `_cloudevents_dispatch`). The
generic deployer auto-discovers `open-charge-map/fabric/post-deploy.ps1` via the
common "`{source}/fabric/post-deploy.ps1`" hook convention and calls it at the
end of a successful deploy.

Like the fixed-dock **tfl-cycles** map this mirrors, open-charge-map is a
**static point** feed — charging stations do not move — so it is styled like a
station network (coloured, sized bubbles), **not** like moving vehicles. Every
attribute the map paints (identity, WGS84 location, operational status, usage
type) lives on a single materialized view, so — unlike tfl-cycles, which JOINs a
station-information view to a station-status view — every open-charge-map layer
reads that one view directly. The map is parametric in the KQL database name and
auto-discovers the source's bounding box from `ocm_bbox()` (falling back to the
raw location footprint, then to a neutral Europe view). The current test data is
Ireland-scoped, but the source is global.

> **Dotted / qualified names.** The KQL schema was generated with
> `-Qualified -Namespace IO.OpenChargeMap`, so **every table and materialized-view
> name literally contains dots** and MUST be bracket-quoted everywhere, e.g.
> `['IO.OpenChargeMap.ChargingLocationLatest']`. A bare reference fails with a
> generic HTTP 400 BadRequest.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1`. Acquires Fabric + Kusto tokens, then runs `wire_open_charge_map_map.py` with the workspace/db/cluster IDs from the deployer's `-Context` hashtable (keys `WorkspaceId`, `DatabaseId`, `EventhouseClusterUri`, `DatabaseName`). Bakes ContosoRealTimeTest standalone defaults so it runs with zero arguments; an explicit param or `-Context` value overrides them. Auto-creates a blank Map item named `open-charge-map-map` if `OPEN_CHARGE_MAP_FABRIC_MAP_ID` is not set (override the name with `OPEN_CHARGE_MAP_FABRIC_MAP_NAME`). Can also be run standalone. |
| `wire_open_charge_map_map.py` | Installs the `ocm_*` KQL helper functions in the target database and idempotently wires the corresponding Fabric Map vector layers via `getDefinition` / `updateDefinition`. Auto-centres the basemap on the source's bounding box. |

## Layers shipped

| # | Layer name | Default | Zoom | Source query | Geometry | Colour / label |
| - | ---------- | ------- | ---- | ------------ | -------- | -------------- |
| 1 | open-charge-map charging locations | on | any | `ocm_stations()` | Point (bubble) | colour by `oper_state` (green = operational, red = out of service, grey = unknown); **radius scales with `number_of_points`**; tooltip `label` / status / operator / usage / bays / town / country |
| 2 | open-charge-map labels | on | z13+ | `ocm_stations()` | Point (tiny bubble + data label) | text label = `operator_title` (fallback `address_title`, then `POI <id>`) |
| 3 | open-charge-map usage type | **off** | any | `ocm_stations()` | Point (bubble) | colour by `usage_family` (Public / Private / Other / Unspecified) |
| 4 | open-charge-map non-operational | **off** | any | `ocm_stations() \| where is_operational == false` | Point (bubble) | standout red `#d7191c` overlay of planned / out-of-service sites |

Layers 1–3 read the single enriched helper `ocm_stations()` and just pick a
different colour column off it (exactly how tfl-cycles reuses
`tflcycles_stations()` for its availability and empty-dock layers). Layer 4 reads
the same helper with a `| where is_operational == false` filter appended. Only
locations with non-null, non-`0,0` coordinates are shown.

The **operational palette** (from live `is_operational`): Operational `#1a9641`
(green), Non-operational `#d7191c` (red), Unknown `#9e9e9e` (grey). The **usage
palette** (Public vs Private families, from `usage_type_title`): Public `#1f78b4`
(blue), Private `#ff7f00` (orange), Other `#6a3d9a` (purple), Unspecified
`#9e9e9e` (grey). The **non-operational** overlay is a single standout colour
(`#d7191c` fill, `#4D0000` stroke) rather than a palette — it is a mono-state
alert layer, so a rich tooltip (`status_title`, `general_comments`,
`date_last_status_update`) carries the detail.

Bubble **radius** is data-driven from a KQL-computed `radius` column
(`4 + 1.6·√number_of_points`, clamped to 4–18 px) via a `["get", "radius"]` paint
expression — the same data-driven-radius pattern tfl-cycles uses to "size by
capacity". Open Charge Map's `number_of_points` runs 1 → 80 (avg ≈ 3.7), so the
clamp keeps single-bay sites legible while capping the largest hubs.

## Schema assumed (freshly-deployed open_charge_map database)

Bracketed, dotted CloudEvents schema created by
`open-charge-map/kql/open-charge-map.kql`:

  * `['IO.OpenChargeMap.ChargingLocation']` — base table: one event per charging
    location (`poi_id`), with identity, the parsed/flattened address + WGS84
    `latitude` / `longitude`, denormalized `operator_title` / `usage_type_title`
    / `status_title`, `is_operational`, `number_of_points`, editorial/freshness
    timestamps, and the itemized `connections` array.
  * `['IO.OpenChargeMap.ChargingLocationLatest']` — materialized view
    `arg_max(___time, *) by ___type, ___source, ___subject` over the base table,
    i.e. **one row per `poi_id` in its latest state**. This is the **single
    source** for every map layer (identity, location, status and connections all
    live on one record — no join needed).

Reading the MV directly is constant-time regardless of how long the source has
been ingesting. `poi_id` is the stable identity across refreshes.

Reference/lookup MVs also exist (`OperatorLatest`, `ConnectionTypeLatest`,
`CurrentTypeLatest`, `ChargerTypeLatest`, `CountryLatest`, `UsageTypeLatest`,
`StatusTypeLatest`, …) but the map does not need them: the POI record is already
denormalized with the operator/usage/status **titles**, so no reference join is
required.

## The KQL the layers use

`ocm_stations()` reads the latest-state MV, drops null / `0,0` coordinates, and
bakes the operational colour band, the usage family + colour, the
`number_of_points`-scaled `radius`, a human `label` and the GeoJSON `geometry`:

```kql
.create-or-alter function with (folder = "Map", skipvalidation = "true") ocm_stations() {
    ['IO.OpenChargeMap.ChargingLocationLatest']
    | where isnotnull(latitude) and isnotnull(longitude) and latitude != 0.0 and longitude != 0.0
    | extend ['oper_state'] = case(
        is_operational == true,  "Operational",
        is_operational == false, "Non-operational",
        "Unknown")
    | extend ['oper_color'] = case(
        ['oper_state'] == "Operational",     "#1a9641",
        ['oper_state'] == "Non-operational", "#d7191c",
        "#9e9e9e")
    | extend ['usage_family'] = case(
        isempty(usage_type_title),             "Unspecified",
        usage_type_title startswith "Public",  "Public",
        usage_type_title startswith "Private", "Private",
        "Other")
    | extend ['usage_color'] = case(
        ['usage_family'] == "Public",  "#1f78b4",
        ['usage_family'] == "Private", "#ff7f00",
        ['usage_family'] == "Other",   "#6a3d9a",
        "#9e9e9e")
    | extend ['radius'] = round(min_of(18.0, max_of(4.0, 4.0 + 1.6 * sqrt(coalesce(todouble(number_of_points), 1.0)))), 1)
    | extend ['label'] = case(
        isnotempty(operator_title), operator_title,
        isnotempty(address_title),  address_title,
        strcat("POI ", tostring(poi_id)))
    | extend ['geometry'] = bag_pack("type", "Point", "coordinates", pack_array(longitude, latitude))
    | project ['geometry'], poi_id, ['label'], operator_title, usage_type_title, usage_cost,
              status_title, is_operational, number_of_points,
              address_title, address_line1, town, state_or_province, postcode,
              country_title, country_iso_code, latitude, longitude,
              date_last_status_update, general_comments,
              ['oper_state'], ['oper_color'], ['usage_family'], ['usage_color'], ['radius']
}
```

`ocm_bbox()` is `ocm_stations() | summarize` of the 1 %/99 % lat/lon quantiles
used to auto-fit the basemap:

```kql
.create-or-alter function with (folder = "Map", skipvalidation = "true") ocm_bbox() {
    ocm_stations()
    | summarize lat_p01 = percentile(latitude, 1), lat_p99 = percentile(latitude, 99),
                lon_p01 = percentile(longitude, 1), lon_p99 = percentile(longitude, 99),
                cnt = count()
}
```

Both bodies live verbatim in `wire_open_charge_map_map.py` (`OPEN_CHARGE_MAP_FUNCTIONS`).

### Exact query behind each layer

| Layer | Query stored in the Map part (`queries/layerSource-<id>.kql`) |
| ----- | ------------------------------------------------------------- |
| charging locations | `ocm_stations()` |
| labels | `ocm_stations()` |
| usage type | `ocm_stations()` |
| non-operational | `ocm_stations()`<br>`\| where is_operational == false` |

The wire script also validates each of these against the cluster at deploy time
(`<query> | count`) and enumerates the live colour domain
(`<query> | where isnotempty(<col>) | distinct <col>, <colorcol>`) before writing
the layer, so a broken query is caught before the definition is saved.

### Dotted-name / reserved-keyword notes

Because the schema is `-Qualified -Namespace IO.OpenChargeMap`, the table and MV
names literally contain dots and are **always bracket-quoted**
(`['IO.OpenChargeMap.ChargingLocationLatest']`); a bare reference returns a
generic HTTP 400. Separately, KQL rejects bare reserved words as identifiers with
the same generic 400. open-charge-map uses `latitude` / `longitude` (not `lat` /
`long`) so the classic `long` collision does not apply, but as a matter of
hygiene **every derived/projected column is bracket-quoted** (`['oper_state']`,
`['usage_family']`, `['radius']`, `['geometry']`, …) and given an explicit safe
name — no computed column is ever called `kind`, `type`, `bool`, etc. Fabric's
`skipvalidation` skips only semantic checks, not the parser, so each layer's KQL
is validated against the cluster (`| count`) before the definition is saved.

## Prerequisites

1. The generic per-source bootstrap has already run for `open-charge-map`:
   ```powershell
   ./tools/deploy-fabric/deploy-fabric.ps1 -Source open-charge-map `
       -ResourceGroup rg-ocm -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```
   This applies `open-charge-map/kql/open-charge-map.kql` (database
   `open_charge_map`) and stands up the rest of the data plane.

2. **A blank Fabric Map item exists** in the workspace, or you let the hook
   auto-create one. The Fabric REST API doesn't (yet) expose programmatic
   creation of `Map` items via the typed surface, but the generic `items` API
   accepts `type=Map`, so this hook does that transparently when
   `OPEN_CHARGE_MAP_FABRIC_MAP_ID` is empty.

3. The map item ID is exposed to the hook via the `OPEN_CHARGE_MAP_FABRIC_MAP_ID`
   environment variable. If absent the hook creates / reuses a Map named
   `open-charge-map-map` (override with `OPEN_CHARGE_MAP_FABRIC_MAP_NAME`).

## Auto-invocation

```powershell
$env:OPEN_CHARGE_MAP_FABRIC_MAP_ID = "<map-guid>"  # optional; will be auto-created
./tools/deploy-fabric/deploy-fabric.ps1 -Source open-charge-map `
    -ResourceGroup rg-ocm -Workspace "<ws-guid>"
# ...generic steps...
# [6/6] Running post-deploy hook (open-charge-map/fabric/post-deploy.ps1)...
#   Creating 2 helper functions in open_charge_map
#   Discovering bounding box from ocm_bbox()
#     2407 locations; lat=[51.55, 55.20] lon=[-9.85, -6.05]
#   layer open-charge-map charging locations
#     rows: 2407
#     palette oper_state: 3 colors
#   ...
#   OK - map <map-guid> updated with 4 layers
```

Skip with `-SkipPostDeployHook` if you only want the data plane.

## Standalone re-wire / re-fit the bbox

Re-running is safe and idempotent: the script removes the layers it previously
wired (matched by their KQL source's `itemId` binding) and recreates them, and
re-fits the basemap bounding box to whatever locations are currently indexed. The
ContosoRealTimeTest workspace / database / cluster IDs are baked in as parameter
defaults, so re-wiring after data arrives is just:

```powershell
$env:OPEN_CHARGE_MAP_FABRIC_MAP_ID = "<map-guid>"
./feeders/open-charge-map/fabric/post-deploy.ps1
```

To target a different environment, override any of the baked defaults:

```powershell
$env:OPEN_CHARGE_MAP_FABRIC_MAP_ID = "<map-guid>"
./feeders/open-charge-map/fabric/post-deploy.ps1 `
    -WorkspaceId   "<ws-guid>" `
    -KqlDatabaseId "<kqldb-guid>" `
    -KustoUri      "https://trd-xxxxxxxx.z6.kusto.fabric.microsoft.com" `
    -KustoDatabase "open_charge_map"
```

`FABRIC_TOKEN` and `KUSTO_TOKEN` are acquired via `az account get-access-token`
automatically if not already set in the environment.

The wiring script can also be invoked directly:

```powershell
python ./feeders/open-charge-map/fabric/wire_open_charge_map_map.py `
    --workspace-id <ws> --map-id <map> --kql-db-id <kqldb> `
    --kusto-uri https://<cluster>.kusto.fabric.microsoft.com --kusto-db open_charge_map
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
data — colouring by `oper_state` / `usage_family` picks up the exact set of
bands present, mapped through the KQL-computed `oper_color` / `usage_color`.

## Future enhancement: connector-power layer

A fifth layer colouring locations by **max connector power** (DC-fast vs slow)
was considered and deliberately **omitted**. Connector power lives inside the
`connections` dynamic array; each element documents standard, level, current
type, electrical rating (`power_kw`), status and quantity — but that element
schema is not materialized as verified table columns (the column docstring notes
the connection schema is too large to inline). An `mv-apply` over unverified
dynamic field names would be fragile and could silently mis-colour or fail, so it
is left as a future enhancement. When added it would look like:

```kql
// SKETCH ONLY - verify the connections element field names against the cluster first.
ocm_stations()
| mv-apply c = connections on ( summarize max_kw = max(toreal(c.power_kw)) )
| extend ['power_class'] = case(max_kw >= 50.0, "DC fast", max_kw >= 7.0, "Fast AC", "Slow")
```

Prefer robust over clever: ship the four verified layers now, add power once the
`connections` element shape is confirmed live.
