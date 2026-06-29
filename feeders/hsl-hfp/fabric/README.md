# hsl-hfp Fabric assets

Post-deploy artefacts for the **hsl-hfp** real-time-sources feeder (Helsinki
Region Transport **HFP** — High-Frequency Positioning): a live Fabric **Map**
visualisation of HSL's ~1,700 transit vehicles streaming GPS at ~1 Hz, plus the
HSL stop network. The data plane is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` script (ACI + Event Hubs + KQL database
+ Eventstream into `_cloudevents_dispatch`). The generic deployer auto-discovers
`hsl-hfp/fabric/post-deploy.ps1` via the common
"`{source}/fabric/post-deploy.ps1`" hook convention and calls it at the end of a
successful deploy.

This map mirrors the **gtfs** transit map: it is parametric in the KQL database
name, auto-discovers the source's bounding box from `['fi.hsl.gtfs.StopLatest']`
(falling back to live vehicle positions, then the Helsinki city centre), and
assumes the canonical schema laid down by `hsl-hfp/kql/hsl-hfp.kql`.

There are **no route-line layers**: the HSL feeder ships no GTFS Shapes
(polyline geometry), so unlike the generic gtfs map there is nothing to draw for
route paths. Vehicle motion is conveyed instead by heading-oriented vehicle
rectangles at street zoom.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1`. Acquires Fabric + Kusto tokens, then runs `wire_hsl_hfp_map.py` with the workspace/db/cluster IDs from the deployer's `-Context` hashtable (keys `WorkspaceId`, `DatabaseId`, `EventhouseClusterUri`, `DatabaseName`). Auto-creates a blank Map item named `hsl-hfp-map` if `HSL_HFP_FABRIC_MAP_ID` is not set (override the name with `HSL_HFP_FABRIC_MAP_NAME`). Can also be run standalone. |
| `wire_hsl_hfp_map.py` | Installs the `hslhfp_*` KQL helper functions in the target database and idempotently wires the corresponding Fabric Map vector layers via `getDefinition` / `updateDefinition`. Auto-centres the basemap on the source's bounding box. |

## Layers shipped

| # | Layer name | Default | Zoom | Source query | Geometry | Colour / label |
| - | ---------- | ------- | ---- | ------------ | -------- | -------------- |
| 1 | HSL - Live vehicles | on | z8–16 | `hslhfp_vehicle_points(5m)` | Point (bubble) | colour by `transport_mode`; tooltip `desi` / `route_id` / `headsign` / speed / delay |
| 2 | HSL - Live vehicles (detail) | on | z16+ | `hslhfp_vehicle_rectangles(5m)` | Polygon (heading-oriented rectangle) | colour by `transport_mode`; label `route_label` (= `desi`) |
| 3 | HSL - Transit stops | on | z13+ | `hslhfp_stops_for_map()` | Point (bubble) | colour by `location_type`; label `stop_name` (`stop_code`) |
| 4 | HSL - Vehicle punctuality | **off** | z11+ | `hslhfp_vehicle_points(5m)` | Point (bubble) | colour by delay band (early / on-time / late) |
| 5 | HSL - Vehicle density | **off** | any | `hslhfp_vehicle_grid(5m, 0.01)` | Polygon (grid cell) | colour by live-vehicle count per ~1 km cell |
| 6 | HSL - Traffic-signal priority | **off** | z12+ | `hslhfp_tlp_events(30m)` | Point (bubble) | colour by `tlr`/`tla` request / grant / reject |

The live-vehicle layers filter the shared `['fi.hsl.hfp.VehicleEvent']` table to
the `vp` GPS heartbeat (`___type in ('fi.hsl.hfp.vp','fi.hsl.hfp.upstream.vp')`),
drop null and `0,0` coordinates, bound to the last 5 minutes by `___time`, and
dedupe to the latest row per vehicle (`arg_max(___time, *) by ___subject`).

The **transport_mode palette** (HSL house colours): bus `#007AC9` (blue), tram
`#00985F` (green), commuter train `#8C4799` (purple), metro `#FF6319` (orange),
ferry `#00B9E4` (cyan), U-line bus `#9E9E9E` and robot bus `#616161` (greys).

## Schema assumed (freshly-deployed hsl_hfp database)

Bracketed, dotted CloudEvents tables created by `hsl-hfp/kql/hsl-hfp.kql`:

  * `['fi.hsl.hfp.VehicleEvent']` + MV `['fi.hsl.hfp.VehicleEventLatest']` —
    the hero telemetry (`vp` heartbeat shares this table with the stop / door /
    sign events). Geo `lat` / `long` (both nullable). `hdg`, `spd`, `dl`,
    `desi`, `headsign`, `route_id`, `transport_mode`, `occu`, `temporal_type`,
    identity `operator_id` / `vehicle_number` (`___subject` =
    `{operator_id}/{vehicle_number}`).
  * `['fi.hsl.gtfs.Stop']` + MV `['fi.hsl.gtfs.StopLatest']` — reference stops
    (`stop_lat` / `stop_lon`, `stop_name`, `stop_code`, `location_type`,
    `parent_station`).
  * `['fi.hsl.gtfs.Route']` + MV `['fi.hsl.gtfs.RouteLatest']` — route lookup
    (left-joined for `route_short_name` / `route_long_name`).
  * `['fi.hsl.hfp.TrafficLightEvent']` + MV `…Latest` — transit-signal-priority
    `tlr` / `tla` events.

All `<X>Latest` MVs are `arg_max(___time, *) by ___type, ___source, ___subject`.
The wire script reads the `*Latest` MVs directly so each layer query is
constant-time regardless of how long the source has been ingesting.

> **`dl` (delay) sign convention.** Per the HSL HFP spec and the
> `hsl-hfp.kql` column docstring, a **positive** `dl` means the vehicle is
> running **ahead** of schedule (early) and a **negative** `dl` means it is
> **behind** schedule (late). The punctuality banding and the "N min late /
> early" labels follow this convention.

## Prerequisites

1. The generic per-source bootstrap has already run for `hsl-hfp`:
   ```powershell
   ./tools/deploy-fabric/deploy-fabric.ps1 -Source hsl-hfp `
       -ResourceGroup rg-hsl -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```
   This applies `hsl-hfp/kql/hsl-hfp.kql` (database `hsl_hfp`) and stands up the
   rest of the data plane.

2. **A blank Fabric Map item exists** in the workspace, or you let the hook
   auto-create one. The Fabric REST API doesn't (yet) expose programmatic
   creation of `Map` items via the typed surface, but the generic `items` API
   accepts `type=Map`, so this hook does that transparently when
   `HSL_HFP_FABRIC_MAP_ID` is empty.

3. The map item ID is exposed to the hook via the `HSL_HFP_FABRIC_MAP_ID`
   environment variable. If absent the hook creates / reuses a Map named
   `hsl-hfp-map` (override with `HSL_HFP_FABRIC_MAP_NAME`).

## Auto-invocation

```powershell
$env:HSL_HFP_FABRIC_MAP_ID = "<map-guid>"  # optional; will be auto-created
./tools/deploy-fabric/deploy-fabric.ps1 -Source hsl-hfp `
    -ResourceGroup rg-hsl -Workspace "<ws-guid>"
# ...generic steps...
# [7/7] Running post-deploy hook (hsl-hfp/fabric/post-deploy.ps1)...
#   Creating 7 helper functions in hsl_hfp
#   Discovering bounding box from hslhfp_bbox()
#     6943 features; lat=[60.10, 60.40] lon=[24.55, 25.25]
#   layer HSL - Live vehicles
#     rows: 1683
#     palette mode_label: 6 colors
#   ...
#   OK - map <map-guid> updated with 6 layers
```

Skip with `-SkipPostDeployHook` if you only want the data plane.

## Standalone re-wire

After tweaking a layer query or colour ramp in `wire_hsl_hfp_map.py`:

```powershell
$env:HSL_HFP_FABRIC_MAP_ID = "<map-guid>"
./hsl-hfp/fabric/post-deploy.ps1 `
    -WorkspaceId   "<ws-guid>" `
    -KqlDatabaseId "<kqldb-guid>" `
    -KustoUri      "https://trd-xxxxxxxx.z1.kusto.fabric.microsoft.com" `
    -KustoDatabase "hsl_hfp"
```

`FABRIC_TOKEN` and `KUSTO_TOKEN` are acquired via `az account get-access-token`
automatically if not already set in the environment. Re-running is safe: the
script removes the layers it previously wired (matched by their KQL source's
`itemId` binding) and recreates them, so this is the normal edit loop.

The script can also be invoked directly:

```powershell
python ./hsl-hfp/fabric/wire_hsl_hfp_map.py `
    --workspace-id <ws> --map-id <map> --kql-db-id <kqldb> `
    --kusto-uri https://<cluster>.kusto.fabric.microsoft.com --kusto-db hsl_hfp
```

## Why both `seriesGroup` AND a `match` expression?

Empirically, Fabric Maps' documented `enableSeriesGroup` + `seriesGroup` +
`customColors` schema populates the Data Layers panel legend correctly but does
**not** drive per-feature paint colour — all bubbles/polygons fall back to the
static fallback `color` (grey). What actually renders is a MapLibre-style
`["match", ["get", column], v1, c1, ..., fallback]` expression on the paint
property.

The wire script writes **both** at deploy time: `customColors` (for the panel
legend) and the `match` expression (for the renderer). The distinct values are
enumerated from the live query result so the palette stays in sync with the
data — colour by `transport_mode` picks up any new mode automatically.