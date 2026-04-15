# Deploy to Fabric — Cloud Shell Script

One-click deployment of a Real-Time Sources bridge with Microsoft Fabric
integration. Runs in Azure Cloud Shell.

## What it does

```
┌────────────────────────────────────────────────────────────────┐
│  Step 1: ARM Template (az deployment group create)             │
│   → Azure Container Instance (bridge container)                │
│   → Event Hub namespace + event hub                            │
│   → Storage account (bridge state)                             │
│   → Log Analytics workspace                                    │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│  Steps 2–3: Fabric REST API + KQL                              │
│   → KQL database in existing Eventhouse                        │
│   → _cloudevents_dispatch table + typed tables + update         │
│     policies + materialized views (from source kql/ script)    │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│  Steps 4–5: Fabric Event Stream                                │
│   → Custom Endpoint source                                     │
│   → Default stream → Eventhouse → _cloudevents_dispatch         │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│  Steps 6–7: Wire it up                                         │
│   → Retrieve Custom Endpoint connection string                  │
│   → Update ACI container to send directly to Fabric             │
└────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Azure Cloud Shell (PowerShell) — already authenticated via `az`
- An existing Microsoft Fabric **Workspace** (you need the workspace ID)
- An existing **Eventhouse** in that workspace (you need the eventhouse ID)
- The **Capacity ID** for the workspace (from Fabric admin portal or workspace settings)
- Contributor access to an Azure subscription / resource group

## Usage

### From Azure Cloud Shell

```powershell
# Download and run
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/clemensv/real-time-sources/main/tools/deploy-fabric/deploy-fabric.ps1' -OutFile deploy-fabric.ps1

./deploy-fabric.ps1 `
    -Source pegelonline `
    -ResourceGroup rg-streams `
    -WorkspaceId "c98acd97-4363-4296-8323-b6ab21e53903" `
    -EventhouseId "dbfd2819-2879-4ae7-bff2-95619ad7b8e7" `
    -CapacityId "a1b2c3d4-5678-9abc-def0-123456789abc"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `-Source` | Yes | — | Source directory name (e.g., `pegelonline`, `usgs-earthquakes`) |
| `-ResourceGroup` | Yes | — | Azure resource group for ACI + Event Hubs |
| `-Location` | No | RG location | Azure region |
| `-WorkspaceId` | Yes | — | Fabric workspace ID (GUID) |
| `-EventhouseId` | Yes | — | Fabric Eventhouse ID (GUID) |
| `-CapacityId` | Yes | — | Fabric capacity ID (GUID) |
| `-DatabaseName` | No | Source name | KQL database name |
| `-SkipArm` | No | `$false` | Skip ARM deployment (if ACI + EH already exist) |

## What happens end-to-end

The script deploys the ACI container initially connected to Event Hubs (via
the ARM template), then sets up the Fabric side. Once the Event Stream is
configured, the script retrieves the Custom Endpoint connection string and
updates the ACI container to send data directly to Fabric. If the connection
string retrieval fails, the script provides manual instructions as a fallback.

Data flows into the `_cloudevents_dispatch` landing table, and KQL update
policies automatically fan events out into per-type tables with materialized
views for latest-state queries.

## Sources requiring API keys

These sources require an additional secret during ARM deployment:

| Source | Environment Variable | How to obtain |
|--------|---------------------|---------------|
| `aisstream` | `AISSTREAM_API_KEY` | Register at [aisstream.io](https://aisstream.io/) |
| `entsoe` | `ENTSOE_SECURITY_TOKEN` | Register at [ENTSO-E](https://transparency.entsoe.eu/) |
| `nve-hydro` | `NVE_API_KEY` | Register at [NVE](https://api.nve.no/) |
| `wsdot` | `WSDOT_ACCESS_CODE` | Register at [WSDOT](https://www.wsdot.wa.gov/traffic/api/) |
