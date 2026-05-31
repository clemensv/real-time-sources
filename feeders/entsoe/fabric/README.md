# ENTSO-E Fabric assets

Post-deploy artefacts for the **entsoe** real-time-sources bridge: a 3-page
Fabric **Real-Time Dashboard** and a Fabric **Map** that visualise the live
state of the pan-European wholesale electricity market — day-ahead prices,
generation mix, system load, and cross-border physical flows from the
[ENTSO-E Transparency Platform](https://transparency.entsoe.eu/).

The data plane (ACI/notebook + Event Hubs/Eventstream + KQL database into
`_cloudevents_dispatch`) is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` (and `deploy-feeder-notebook.ps1`)
scripts, which also apply `kql/entsoe.kql` (the typed tables and
materialized views the dashboard and map consume). The generic deployer
auto-discovers `feeders/entsoe/fabric/post-deploy.ps1` via the common
`{source}/fabric/post-deploy.ps1` hook convention and calls it at the end of
a successful deploy.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1` and `deploy-feeder-notebook.ps1`. Acquires a Kusto management token, applies the five helper functions in `helpers.kql` to the live `entsoe` database (one `.create-or-alter` per call), then runs `build_dashboard.py` and `build_map.py` with the workspace / KQL-db / cluster IDs taken from the deployer's `-Context` hashtable. Idempotent; can also be run standalone after a tweak. |
| `build_dashboard.py` | Idempotently creates/updates the 3-page `KQLDashboard` item *ENTSO-E European Electricity Market*. Every tile binds to a real table / materialized view / helper function and a validated KQL query. |
| `build_map.py` | Idempotently creates/updates the `Map` item *ENTSO-E Market Map*: a directional cross-border physical-flow arrow layer plus a day-ahead price-bubble layer, both Kusto-backed. |
| `helpers.kql` | Five reference / geometry helper functions consumed by both the dashboard and the map: `PsrType()`, `EICZone()`, `PriceColor()`, `ZonePriceMarkers()`, `ZoneFlowLines()`. Re-applied on every deploy by the hook. |

## Prerequisites

1. The generic per-source bootstrap has already run for `entsoe`, e.g.:

   ```powershell
   ./tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source entsoe -Workspace <ws-guid>
   ```

   This creates the `entsoe` KQL database, applies `kql/entsoe.kql` (the
   `DayAheadPricesLatest`, `ActualGenerationPerTypeLatest`,
   `WindSolarGenerationLatest`, `ActualTotalLoadLatest`, and
   `CrossBorderPhysicalFlowsLatest` materialized views the tiles bind to),
   creates the Eventstream + `_cloudevents_dispatch` destination, and starts
   the feeder. Cross-border flow and day-ahead price data require a valid
   ENTSO-E Transparency Platform security token (`ENTSOE_API_TOKEN`).

2. **A blank Fabric Map item exists** in the workspace. The Fabric REST API
   does not (yet) expose programmatic creation of Map items, so create one
   once via the portal (`+ New > Map`) and note its item ID, or pass the
   map name to `build_map.py` (it reuses an existing item of that name).

## Auto-invocation

```powershell
./tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source entsoe -Workspace "<ws-guid>"
# ...generic bootstrap stages...
# [6/6] Running post-deploy hook (entsoe/fabric/post-deploy.ps1)...
#   [1/3] Applying helpers.kql ...
#         applied PsrType / EICZone / PriceColor / ZonePriceMarkers / ZoneFlowLines
#   [2/3] Building Real-Time Dashboard ...
#   [3/3] Building Map ...
#   Done. Open the items from the Real-Time Open Data workspace.
```

Skip with `-SkipPostDeployHook` if needed.

## Standalone re-build

After tweaking helper bodies, colour ramps, tile queries, or map layers:

```powershell
./feeders/entsoe/fabric/post-deploy.ps1 `
    -WorkspaceId   "<workspace-guid>" `
    -KqlDatabaseId "<kql-db-guid>" `
    -KustoUri      "https://trd-xxxxxxxx.z2.kusto.fabric.microsoft.com" `
    -KustoDatabase entsoe
```

Both `build_dashboard.py` and `build_map.py` update the existing item in
place when one of the same display name already exists, so re-runs are safe.

## What the dashboard looks like

3 pages, every tile backed by a `kql/entsoe.kql` materialized view (and the
`helpers.kql` reference functions for zone / fuel / colour lookups).

| Page | Focus | Representative tiles |
| ---- | ----- | -------------------- |
| **Prices & Market** | Day-ahead wholesale price per bidding zone | Price multistat, cheapest→dearest ranking, geographic price map, per-zone detail table, price spread / extremes congestion signal |
| **Generation Mix & Renewables** | What is being generated and how green it is | Renewable-share headline, current fuel-mix pie, wind & solar forecast-vs-actual columns, generation by zone & fuel stacked column |
| **System Balance & Cross-Border** | Imports, exports and interconnector load | Net position per zone (import +/export −), actual total load per zone, top interconnector flows, full cross-border flow matrix |

## What the map looks like

2 Kusto-backed layers, both driven by the helper functions in `helpers.kql`.

| Layer | Geometry | Encoding | Source function |
| ----- | -------- | -------- | --------------- |
| Cross-border physical flows | Directional arrow line per ordered zone pair (left-offset so opposite directions don't overlap) | 5-bucket dark magnitude ramp on \|MW\| (`<200` → `≥2500`); compact `OUT→IN MW` label | `ZoneFlowLines()` |
| Day-ahead price bubbles | Point per bidding-zone centroid | Green→red ramp on €/MWh | `ZonePriceMarkers()` + `PriceColor()` |

### Colour rationale

* **Flow magnitude** uses a dark, multi-hue 5-class ramp so heavy
  interconnectors read instantly and low flows recede:
  `≥2500 MW #67001f` → `≥1200 #b2182b` → `≥600 #762a83` →
  `≥200 #225ea8` → `<200 #2b8cbe`. The diverging blue→red progression keeps
  the busiest borders (e.g. NO2↔GB, FR↔ES) loud against the basemap while
  the long tail of small exchanges stays legible.
* **Day-ahead price** uses a green→amber→red ramp anchored so cheap zones
  are calm green and scarcity-priced zones are loud red, matching the
  intuition that red = expensive.

### Flow geometry

`ZoneFlowLines()` projects each ordered exporter→importer pair onto a local
equirectangular plane (`lon × cos(mean lat)`), draws the shaft from t=0.16 to
t=0.80 of the great-circle chord, offsets it to the left of the direction of
travel so the opposing flow on the same border renders as a separate arrow,
and caps the arrowhead size (`hb = min(0.22, 0.08·L)`) so short borders don't
get oversized heads. Labels carry the direction and magnitude
(`DK2→SE4 521`) and use overlap-avoidance so dense regions stay readable.

### Reference data

Zone centroids and fuel/production-type lookups are baked into the
`EICZone()` and `PsrType()` helper functions (EIC bidding-zone code →
zone / country / lat / lon, and ENTSO-E B-code → fuel / renewable flag /
colour). Edit those functions and re-run the hook to extend coverage.
