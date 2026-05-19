# dwd Fabric assets

Post-deploy artefacts for the **dwd** real-time-sources bridge: the ICON-D2
forecast map. The data plane is handled by the generic
`tools/deploy-fabric/deploy-fabric.ps1` script (ACI + Event Hubs + KQL
database + Eventstream into `_cloudevents_dispatch`). The generic deployer
auto-discovers `dwd/fabric/post-deploy.ps1` via the common
"`{source}/fabric/post-deploy.ps1`" hook convention and calls it at the end
of a successful deploy.

## Files

| File | Purpose |
| ---- | ------- |
| `post-deploy.ps1` | Hook auto-invoked by `tools/deploy-fabric/deploy-fabric.ps1`. Acquires Fabric + Kusto tokens, then runs `wire_icond2_map.py` with the workspace/db/cluster IDs from the deployer's `-Context` hashtable. Can also be run standalone. |
| `wire_icond2_map.py` | Idempotently (re)wires 8 ICON-D2 Kusto-backed vector layers (t_2m, tot_prec, vmax_10m, clct, cape_ml, dbz_cmax, pmsl, h_snow) onto an existing Fabric Map item. Each layer queries `['de.dwd.icond2.GridPoints']` for the latest model run of its parameter, so the map auto-refreshes as the bridge ingests new runs. |

## Prerequisites

1. The generic per-source bootstrap has already run for `dwd`:
   ```powershell
   ./tools/deploy-fabric/deploy-fabric.ps1 -Source dwd `
       -ResourceGroup rg-dwd -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```

2. **A blank Fabric Map item exists** in the workspace. The Fabric REST API
   doesn't (yet) expose programmatic creation of Map items, so create one
   once via the portal (`+ New > Map`) and note its item ID.

3. The map item ID is exposed to the hook via the `DWD_FABRIC_MAP_ID`
   environment variable. If the variable isn't set, the hook exits 0 with a
   notice rather than failing the bootstrap.

## Auto-invocation

```powershell
$env:DWD_FABRIC_MAP_ID = "39abf7e3-1df6-4cbf-ab92-93d6d4cf07e5"
./tools/deploy-fabric/deploy-fabric.ps1 -Source dwd `
    -ResourceGroup rg-dwd -Workspace "<ws-guid>"
# ...generic 6 steps...
# [7/7] Running post-deploy hook (dwd/fabric/post-deploy.ps1)...
#   t_2m     : default filter = 2026-05-18 00:00 UTC
#   tot_prec : default filter = 2026-05-18 00:00 UTC
#   ...
#   Post-deploy hook completed
```

Skip with `-SkipPostDeployHook` if needed.

## Standalone re-wire

After tweaking colour ramps or adding layers in `wire_icond2_map.py`:

```powershell
$env:DWD_FABRIC_MAP_ID = "39abf7e3-1df6-4cbf-ab92-93d6d4cf07e5"
./dwd/fabric/post-deploy.ps1 `
    -WorkspaceId   "a26c1440-1c4a-4774-b944-fd62f7380d62" `
    -KqlDatabaseId "8c202901-5346-4faf-88a6-9c15d737a91b" `
    -KustoUri      "https://trd-mq16rbrpv3c4x4r4h1.z1.kusto.fabric.microsoft.com"
```

## What the map looks like

8 vector layers, all polygon (0.1deg lat/lon cells), all label-on:

| Layer | Parameter | Unit | Default-on |
| ----- | --------- | ---- | ---------- |
| 2 m temperature | `t_2m` | degC | yes |
| Total precipitation | `tot_prec` | mm | no |
| 10 m wind gust | `vmax_10m` | m/s | no |
| Total cloud cover | `clct` | % | no |
| CAPE (ML) | `cape_ml` | J/kg | no |
| Simulated max radar refl. | `dbz_cmax` | dBZ | no |
| Mean sea-level pressure | `pmsl` | hPa | no |
| Snow depth | `h_snow` | m | no |

Each layer has a single-select text filter on `Forecast time (UTC)` so the
user can pick which lead hour to display; the script seeds the filter with
the first forecast hour of the parameter's latest run so the layer renders
immediately when toggled on.


## Files

| File | Purpose |
| ---- | ------- |
| `wire_icond2_map.py` | Idempotently (re)wires 8 ICON-D2 Kusto-backed vector layers (t_2m, tot_prec, vmax_10m, clct, cape_ml, dbz_cmax, pmsl, h_snow) onto an existing Fabric Map item. Each layer queries `['de.dwd.icond2.GridPoints']` for the latest model run of its parameter (`toscalar(... | summarize max(run))`), so the map auto-refreshes as the bridge ingests new runs. |
| `setup.ps1` | Thin PowerShell wrapper that acquires Fabric + Kusto bearer tokens via `az account get-access-token` and invokes `wire_icond2_map.py`. |

## Prerequisites

1. The generic per-source bootstrap has already been run for `dwd`:
   ```powershell
   ../../tools/deploy-fabric/deploy-fabric.ps1 -Source dwd `
       -ResourceGroup rg-dwd -Workspace <ws-guid> -Eventhouse <eh-guid>
   ```
   This creates the `dwd` KQL database, applies the schemas (including
   `kql/icond2.kql`), creates the Eventstream + dispatch destination, and
   deploys the ACI with `DWD_MODULES=...,icond2_grid` (the ARM templates
   already include `icond2_grid` in their default value).

2. A blank Fabric Map item exists in the workspace. Create one via the Fabric
   portal (New > Map). Note its item ID.

3. `python` is on `PATH`, with `requests` available. If `FABRIC_TOKEN` /
   `KUSTO_TOKEN` are not pre-set, the script will fall back to
   `azure.identity.DefaultAzureCredential` (so `pip install azure-identity`).

## Usage

```powershell
./setup.ps1 `
    -WorkspaceId   "a26c1440-1c4a-4774-b944-fd62f7380d62" `
    -MapId         "39abf7e3-1df6-4cbf-ab92-93d6d4cf07e5" `
    -KqlDatabaseId "8c202901-5346-4faf-88a6-9c15d737a91b" `
    -KustoUri      "https://trd-mq16rbrpv3c4x4r4h1.z1.kusto.fabric.microsoft.com"
```

Re-run any time you change the layer set, colour ramps or label format in
`wire_icond2_map.py` - the script removes its previously-managed layers (by
name) before adding the current set, so it's safe to apply repeatedly.

## What the map looks like

8 vector layers, all polygon (0.1deg lat/lon cells), all label-on:

| Layer | Parameter | Unit | Default-on |
| ----- | --------- | ---- | ---------- |
| 2 m temperature | `t_2m` | degC | yes |
| Total precipitation | `tot_prec` | mm | no |
| 10 m wind gust | `vmax_10m` | m/s | no |
| Total cloud cover | `clct` | % | no |
| CAPE (ML) | `cape_ml` | J/kg | no |
| Simulated max radar refl. | `dbz_cmax` | dBZ | no |
| Mean sea-level pressure | `pmsl` | hPa | no |
| Snow depth | `h_snow` | m | no |

Each layer has a single-select text filter on `Forecast time (UTC)`
(label-formatted `yyyy-MM-dd HH:mm UTC`) so the user can pick which lead
hour to display; the script seeds the filter with the first forecast hour
of the parameter's latest run so the layer renders immediately when toggled
on.
