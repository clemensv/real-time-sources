# Fabric Event Stream + KQL Database Setup

Sets up a Microsoft Fabric Event Stream and KQL (Eventhouse) database to receive
AIS vessel tracking data from the Digitraffic Maritime bridge.

## Architecture

```
┌──────────────────────────────────────────────────┐
│  Container / Docker                              │
│  ┌────────────────────────────────────────────┐  │
│  │  Digitraffic Maritime Bridge               │  │
│  │  MQTT meri.digitraffic.fi → Kafka          │  │
│  └───────────────────┬────────────────────────┘  │
│                      │ CONNECTION_STRING          │
└──────────────────────┼───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  Fabric Event Stream: digitraffic-maritime-ingest│
│                                                  │
│  ┌─────────────────┐    ┌─────────────────────┐  │
│  │ Custom Input     │───▶│ Default Stream       │  │
│  │ ais-input        │    │                      │  │
│  │ (CloudEvents     │    └──────────┬───────────┘  │
│  │  2 AIS types)    │               │              │
│  └─────────────────┘               │              │
│                          ┌──────────▼───────────┐  │
│                          │ dispatch-kql          │  │
│                          │ → _cloudevents_       │  │
│                          │   dispatch            │  │
│                          └──────────────────────┘  │
└──────────────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  KQL Eventhouse: digitraffic-maritime            │
│  ┌────────────────────────────────────────────┐  │
│  │  Database: digitraffic-maritime            │  │
│  │                                            │  │
│  │  Ingestion:                                │  │
│  │  └── _cloudevents_dispatch                 │  │
│  │       ├─ update policy → VesselLocation    │  │
│  │       └─ update policy → VesselMetadata    │  │
│  │                                            │  │
│  │  Materialized Views:                       │  │
│  │  ├── VesselLocationLatest                  │  │
│  │  └── VesselMetadataLatest                  │  │
│  │                                            │  │
│  │  Functions:                                │  │
│  │  ├── VesselPositions()                     │  │
│  │  ├── AISStatistics()                       │  │
│  │  └── VesselTrack()                         │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

## Data Model

The bridge emits two CloudEvents types, each routed to its own KQL table via
update policies on the `_cloudevents_dispatch` ingestion table.

| Table | Description | Rate |
|---|---|---|
| `VesselLocation` | Vessel positions (lat, lon, SOG, COG, heading, nav status) | ~35 msg/s |
| `VesselMetadata` | Static vessel data (name, IMO, callsign, dimensions, destination) | ~3 msg/s |

Estimated volume: ~3.3 million events/day (~300 MB/day).

## Files

| File | Description |
|---|---|
| `setup.ps1` | PowerShell setup script (Azure CLI + Fabric REST API) |
| `setup.sh` | Bash setup script (Azure CLI + Fabric REST API) |
| `kql_database.kql` | KQL schema: tables, update policies, materialized views, functions |
| `README.md` | This file |

## Usage

### Prerequisites

- Azure CLI (`az`) installed and authenticated (`az login`)
- `jq` installed (for bash script)
- Permissions to create items in the Fabric workspace
- An existing Eventhouse in the workspace

### 1. Set up Fabric resources

```powershell
# PowerShell
./setup.ps1 -WorkspaceId "<workspace-guid>" -EventhouseId "<eventhouse-guid>"
```

```bash
# Bash
./setup.sh <workspace-guid> <eventhouse-guid>
```

This creates:
- A KQL database with 2 typed tables, materialized views, and analysis functions
- An Event Stream with Custom Endpoint → `_cloudevents_dispatch` table
- KQL update policies that split events by CloudEvents `type` into typed tables

Retrieve the Custom Endpoint connection string from the Fabric portal.

### 2. Deploy the container

**Docker:**
```bash
docker run -e CONNECTION_STRING="Endpoint=sb://..." \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

**Local:**
```bash
CONNECTION_STRING="Endpoint=sb://..." python -m digitraffic_maritime stream
```

### 3. Query the data

In a Fabric KQL queryset or Azure Data Explorer:

```kusto
// Live vessel map — latest position + static info for all vessels
VesselPositions()
| where sog > 0
| project mmsi, name, latitude, longitude, sog, cog,
          ship_type_name, destination, last_update

// Message rate statistics
AISStatistics()

// All vessels currently near Helsinki
VesselPositions()
| where latitude between (59.9 .. 60.5) and longitude between (24.5 .. 25.5)

// Vessel track history for a specific MMSI (last 24 hours)
VesselTrack(230629000)

// Custom time window track
VesselTrack(230629000, 7d)

// Unique vessels seen in the last hour
VesselLocation
| where ___time > ago(1h)
| summarize count() by mmsi
| count

// Vessel type distribution
VesselPositions()
| summarize vessels = count() by ship_type_name
| order by vessels desc
```

## Coverage

The Digitraffic Marine AIS system covers the Baltic Sea region:
Finland, Sweden, Estonia, Latvia, Lithuania, Denmark, Germany, Poland,
and international transit traffic.

This complements the [Kystverket AIS](../../kystverket-ais/fabric/)
Fabric setup which covers Norwegian waters.
