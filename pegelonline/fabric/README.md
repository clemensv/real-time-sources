# pegelonline Fabric assets

Post-deploy artefacts for the **pegelonline** real-time-sources bridge: a
6-layer Fabric Map that visualises the live state of the German Federal
Waterways gauge network (~800 stations along the Rhein, Elbe, Donau, Main,
Weser, Mosel, Neckar, Oder and their tributaries).

The data plane (ACI + Event Hubs + KQL database + Eventstream into
`_cloudevents_dispatch`) is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` script. The generic deployer
auto-discovers `pegelonline/fabric/post-deploy.ps1` via the common
"`{source}/fabric/post-deploy.ps1`" hook convention and calls it at the end
of a successful deploy.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1`. Acquires Fabric + Kusto tokens, then runs `wire_pegelonline_map.py` with the workspace/db/cluster IDs from the deployer's `-Context` hashtable. Can also be run standalone after layer tweaks. |
| `wire_pegelonline_map.py` | Idempotently (re)wires 6 Kusto-backed vector layers onto an existing Fabric Map item: hydrological state, navigation state, 24h trend, data freshness, station labels, and a historical replay layer with a 15-minute time slider. |

## Prerequisites

1. The generic per-source bootstrap has already run for `pegelonline`:

   ```powershell
   ./tools/deploy-fabric/deploy-fabric.ps1 -Source pegelonline `
       -ResourceGroup rg-pegelonline -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```

   This creates the `pegelonline` KQL database, applies the schemas
   (`kql/pegelonline.kql` - including the `EnrichedMeasurements()`,
   `MeasurementTrend24h()`, and `MeasurementHistoryBuckets()` helper
   functions consumed by the map), creates the Eventstream + dispatch
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
#   replay default bucket = 2026-05-19 12:30 UTC
#   pegelonline hydrological state: wired (default-on=True)
#   pegelonline navigation state  : wired (default-on=False)
#   ...
#   Post-deploy hook completed
```

Skip with `-SkipPostDeployHook` if needed.

## Standalone re-wire

After tweaking colour ramps, KQL bodies, or adding layers in
`wire_pegelonline_map.py`:

```powershell
$env:PEGELONLINE_FABRIC_MAP_ID = "<map-item-guid>"
./pegelonline/fabric/post-deploy.ps1 `
    -WorkspaceId   "<workspace-guid>" `
    -KqlDatabaseId "<kql-db-guid>" `
    -KustoUri      "https://trd-xxxxxxxx.z1.kusto.fabric.microsoft.com"
```

The script removes its previously-managed layers (matched by the name
prefix `pegelonline `) before adding the current set, so re-runs are safe.

## What the map looks like

6 layers, all point-symbol, all driven by the KQL helper functions added to
`pegelonline/kql/pegelonline.kql`. Default-on layers are starred.

| Layer | Geometry | Colour encoding | Size | Default | Source function |
| ----- | -------- | --------------- | ---- | ------- | --------------- |
| Hydrological state * | Circle | Categorical on `stateMnwMhw` (low / normal / high / very-high) | 7 px | yes | `EnrichedMeasurements()` |
| Navigation state | Square marker | Categorical on `stateNswHsw` (normal / high / above-HSW) | 0.8 scale | no | `EnrichedMeasurements()` |
| 24h trend | Circle | Triadic on direction (rising / steady / falling) | Linear on \|delta_cm\| (4-18 px) | no | `MeasurementTrend24h()` |
| Data freshness | Ring | Categorical on age band (fresh / stale / very-stale) | 10 px | no | `EnrichedMeasurements()` |
| Station labels * | Text only | Black with white halo, shown at zoom >= 9 | 11 pt | yes | `EnrichedMeasurements()` |
| Historical replay | Circle | Same hydrological-state palette | 7 px | no | `MeasurementHistoryBuckets(24h)` |

### Colour rationale

* **Hydrological state** uses the `RdYlBu`/`RdYlGn` divergent palette
  reversed so the eye reads "blue = low, green = normal, orange = warning,
  red = flood" without needing the legend. The categorical source field
  (`stateMnwMhw`) is authoritative and pre-computed by WSV, so a
  categorical encoding is correct - rivers are not comparable cm-for-cm.
* **24h trend** uses the same red/blue diverging anchors as hydrological
  state to keep the visual vocabulary tight: red still means "more water
  recently", blue still means "less".
* **Freshness** is hollow (`fillColor = #ffffff00`, `strokeColor` only) so
  the layer can be toggled on as an overlay on top of the state layer
  without obscuring it.

### Filters

The map ships with one filter type per data layer that affects every layer
on the same source:

* **Water body** (multi-select on `water_shortname`) - e.g. RHEIN, ELBE,
  DONAU, MAIN, WESER, MOSEL, NECKAR, ODER.
* **Agency** (multi-select on `agency`) - e.g. WSA Mainz, WSA Bingen,
  WSA Koeln.

The **Historical replay** layer additionally carries its own
single-select text filter on `Time (UTC, 15-min)`, seeded to the most
recent 15-minute bucket so the layer renders immediately when first
toggled on. Drag through the dropdown to replay the last 24 hours of
flood / drought signal travelling down the river network - the most
visually striking use of the map for the Rhein, where a wave from Basel
typically reaches Koeln in ~30 hours.

Filters on `water_shortname` / `agency` are not applied by the wire
script - add them once in the Fabric portal and they persist across
re-runs because the script only manages `layerSettings` / `layerSources`
named with the `pegelonline ` prefix.
