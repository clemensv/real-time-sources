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
│  Step 2: Fabric REST API                                       │
│   → KQL database in existing Eventhouse                        │
│   → _cloudevents_dispatch table + typed tables + update         │
│     policies + materialized views (from source kql/ script)    │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│  Step 3: Fabric Event Stream                                   │
│   → Custom Endpoint source                                     │
│   → Default stream                                             │
│   → Eventhouse destination → _cloudevents_dispatch              │
└────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Azure Cloud Shell (PowerShell) — already authenticated via `az`
- An existing Microsoft Fabric **Workspace** (you need the workspace ID)
- An existing **Eventhouse** in that workspace (you need the eventhouse ID)
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
    -EventhouseId "dbfd2819-2879-4ae7-bff2-95619ad7b8e7"
```

### One-click launch

Open Cloud Shell with the script pre-loaded:

```
https://shell.azure.com/powershell
```

Then paste the commands above.

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `-Source` | Yes | — | Source directory name (e.g., `pegelonline`, `usgs-earthquakes`) |
| `-ResourceGroup` | Yes | — | Azure resource group for ACI + Event Hubs |
| `-Location` | No | RG location | Azure region |
| `-WorkspaceId` | Yes | — | Fabric workspace ID (GUID) |
| `-EventhouseId` | Yes | — | Fabric Eventhouse ID (GUID) |
| `-DatabaseName` | No | Source name | KQL database name |
| `-SkipArm` | No | `$false` | Skip ARM deployment (if ACI + EH already exist) |

## After deployment

The script creates the ACI container with an Event Hub connection string.
To wire data through Fabric:

1. Open the Event Stream in the Fabric portal
2. Either:
   - **Add an Event Hub source** pointing at the deployed Event Hub
     (the bridge is already sending data there), or
   - Copy the **Custom Endpoint connection string** and update the ACI
     container to send directly to Fabric

## Sources requiring API keys

These sources require an additional secret parameter during ARM deployment.
The script will prompt for it:

| Source | Environment Variable | How to obtain |
|--------|---------------------|---------------|
| `aisstream` | `AISSTREAM_API_KEY` | Register at [aisstream.io](https://aisstream.io/) |
| `entsoe` | `ENTSOE_SECURITY_TOKEN` | Register at [ENTSO-E](https://transparency.entsoe.eu/) |
| `nve-hydro` | `NVE_API_KEY` | Register at [NVE](https://api.nve.no/) |
| `wsdot` | `WSDOT_ACCESS_CODE` | Register at [WSDOT](https://www.wsdot.wa.gov/traffic/api/) |
