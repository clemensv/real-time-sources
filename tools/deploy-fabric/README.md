# Deploy to Fabric — Cloud Shell Script

One-click **Fabric-only** deployment of a Real-Time Sources bridge. Runs in
Azure Cloud Shell. The script deploys **only** to Microsoft Fabric — it
creates **no** Azure resources (no Resource Group, no Container Instance,
no Event Hubs namespace). The feeder that pushes upstream data into the
resulting Event Stream is your responsibility: run the source's Docker
image anywhere (laptop, on-prem, ACI, Kubernetes, …) using the connection
string this script writes out, or deploy the Fabric-notebook feeder via
the sibling `deploy-feeder-notebook.ps1`.

## What it does

```
┌────────────────────────────────────────────────────────────────┐
│  Steps 1–2: Fabric REST API + KQL                              │
│   → Eventhouse (auto-created if missing) + KQL database        │
│   → _cloudevents_dispatch table + typed tables + update        │
│     policies + materialized views (from source kql/ script)    │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│  Steps 3–4: Fabric Event Stream                                │
│   → Custom Endpoint source                                     │
│   → Default stream → Eventhouse → _cloudevents_dispatch        │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│  Step 5: Connection string                                     │
│   → Retrieve Custom Endpoint connection string                 │
│   → Optionally write to -OutCsFile                             │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│  Step 6: Optional post-deploy hook                             │
│   → Auto-discover {Source}/fabric/post-deploy.ps1              │
│     (local working tree first, then $RawBase fallback)         │
│   → Invoke with a -Context hashtable of all created IDs        │
│   → Used by sources that need extra Fabric wiring (maps,       │
│     dashboards, environments, …). Disable with                 │
│     -SkipPostDeployHook.                                       │
└────────────────────────────────────────────────────────────────┘
```

## Optional per-source post-deploy hooks

A source MAY ship a `{Source}/fabric/post-deploy.ps1` script. After a
successful deployment, both `deploy-fabric.ps1` and
`deploy-feeder-notebook.ps1` look for that file (first in the local working
tree, then via raw GitHub for cloud-shell scenarios) and invoke it with:

```powershell
param([hashtable] $Context, ...)
```

The `$Context` hashtable contains keys the hook may need without having to
re-discover them:

| Key | Description |
| --- | --- |
| `Source` | Source name (e.g. `dwd`, `pegelonline`). |
| `RawBase`, `Repo`, `Branch` | Raw GitHub URL base for downloading siblings. |
| `FabricApi`, `TempDir` | Constants. |
| `WorkspaceId`, `WorkspaceName` | Fabric workspace. |
| `EventhouseId`, `EventhouseName`, `EventhouseClusterUri` | Eventhouse + query URI. |
| `DatabaseId`, `DatabaseName` | KQL database. |
| `EventstreamId`, `EventstreamName` | Eventstream item. |
| `ConnectionString` | Eventstream custom-endpoint CS (if retrievable). |
| `SubscriptionId` | Azure subscription used to acquire the Fabric token (may be empty). |
| `NotebookId`, `NotebookName` | Notebook item (deploy-feeder-notebook only). |

Hooks should ignore keys they don't care about and may consume additional
context from environment variables (e.g. `DWD_FABRIC_MAP_ID`). A hook that
chooses to no-op should `exit 0` so the bootstrap remains green.

If the hook throws, the deployment is treated as failed (re-run with
`-SkipPostDeployHook` to bypass and re-run the hook manually later).

Example: see [`pegelonline/fabric/post-deploy.ps1`](../../pegelonline/fabric/post-deploy.ps1)
(wires a Fabric Map item and ingests static river-segment reference data).

## Prerequisites

- Azure Cloud Shell (PowerShell) — already authenticated via `az`
- A Microsoft Fabric **Workspace** (you need the workspace name or GUID)
- *(Optional)* An existing **Eventhouse** in that workspace. If you don't
  pass `-Eventhouse`, or pass a name that doesn't exist yet, the script
  will create one with the source name. Pass an existing Eventhouse name
  or GUID to reuse one.

## Usage

### From Azure Cloud Shell

```powershell
# Download and run
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/clemensv/real-time-sources/main/tools/deploy-fabric/deploy-fabric.ps1' -OutFile deploy-fabric.ps1

./deploy-fabric.ps1 `
    -Source pegelonline `
    -Workspace "ContosoRealTime" `
    -Eventhouse "ContosoRealTime-eh" `
    -OutCsFile pegelonline-eventstream-cs.txt
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `-Source` | Yes | — | Source directory name (e.g., `pegelonline`, `usgs-earthquakes`) |
| `-Workspace` | Yes | — | Fabric workspace name OR GUID |
| `-Eventhouse` | No | Source name | Fabric Eventhouse name OR GUID (created on demand) |
| `-DatabaseName` | No | Source name | KQL database name |
| `-SubscriptionId` | No | active | Azure subscription for Fabric token acquisition |
| `-OutCsFile` | No | — | Path to write the Event Stream connection string |
| `-SkipPostDeployHook` | No | `$false` | Skip the source-specific post-deploy hook |

> **Note:** `-ResourceGroup`, `-Location`, and `-SkipArm` are accepted but
> ignored. They were used when this script also deployed an ACI feeder,
> which it no longer does. Old portal commands continue to work; a warning
> is printed when any of these are supplied.

## What happens end-to-end

The script creates / reuses Eventhouse + KQL DB + Event Stream in Fabric,
applies the source's KQL schema (landing table + typed tables + update
policies + materialized views), and writes the Event Stream Custom
Endpoint connection string to `-OutCsFile` (if provided). The Event Stream
is ready to receive CloudEvents the moment the script finishes.

Wire up a feeder of your choice using that connection string (the
[CONTAINER.md](https://github.com/clemensv/real-time-sources) for each
source shows the exact `docker run` invocation), or deploy the Fabric
notebook variant via `deploy-feeder-notebook.ps1` which runs the feeder
inside Fabric on a schedule (no Azure resources required).

Data flows into the `_cloudevents_dispatch` landing table, and KQL update
policies automatically fan events out into per-type tables with materialized
views for latest-state queries.

## Sister script: deploy-fabric-aci.ps1 (ACI + Fabric, one click)

For users who want both the Fabric backend AND an ACI feeder in a single
call, use `deploy-fabric-aci.ps1`. It is a thin wrapper:

1. Calls `deploy-fabric.ps1` to provision Fabric (Eventhouse + KQL DB +
   Event Stream + post-deploy hook) and captures the Event Stream Custom
   Endpoint connection string.
2. Creates the Azure Resource Group on demand, then deploys the source's
   `azure-template.json` (ACI + storage + Log Analytics) with that
   connection string wired into the container as `CONNECTION_STRING`.

The container streams data directly into the Fabric Event Stream — **no
Event Hubs namespace is created**.

```powershell
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/clemensv/real-time-sources/main/tools/deploy-fabric/deploy-fabric-aci.ps1' -OutFile deploy-fabric-aci.ps1

./deploy-fabric-aci.ps1 `
    -Source pegelonline `
    -ResourceGroup rg-streams `
    -Location westeurope `
    -Workspace ContosoRealTime `
    -Eventhouse ContosoRealTime-eh
```

Sources requiring a secret (`aisstream`, `nve-hydro`, `wsdot`, `entsoe`)
pass it through with `-ApiKeyParamName <template-param> -ApiKey <secret>`,
e.g.:

```powershell
./deploy-fabric-aci.ps1 -Source aisstream `
    -ResourceGroup rg-streams -Location westeurope `
    -Workspace ContosoRealTime -Eventhouse ContosoRealTime-eh `
    -ApiKeyParamName aisstreamApiKey -ApiKey 'sk_…'
```

## Sources requiring API keys

These sources require an additional secret when you run the feeder
(passed as an environment variable to the bridge container):

| Source | Environment Variable | How to obtain |
|--------|---------------------|---------------|
| `aisstream` | `AISSTREAM_API_KEY` | Register at [aisstream.io](https://aisstream.io/) |
| `entsoe` | `ENTSOE_SECURITY_TOKEN` | Register at [ENTSO-E](https://transparency.entsoe.eu/) |
| `nve-hydro` | `NVE_API_KEY` | Register at [NVE](https://api.nve.no/) |
| `wsdot` | `WSDOT_ACCESS_CODE` | Register at [WSDOT](https://www.wsdot.wa.gov/traffic/api/) |
