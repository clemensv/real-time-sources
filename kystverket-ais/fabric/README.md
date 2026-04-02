# Fabric Event Stream + KQL Database Setup

Sets up a Microsoft Fabric Event Stream and KQL (Eventhouse) database to receive
AIS vessel tracking data from the Kystverket AIS bridge.

## Architecture

```
┌──────────────────────────────────────────────────┐
│  ACI Container / Docker                          │
│  ┌────────────────────────────────────────────┐  │
│  │  Kystverket AIS Bridge                     │  │
│  │  TCP 153.44.253.27:5631 → NMEA → Kafka    │  │
│  └───────────────────┬────────────────────────┘  │
│                      │ CONNECTION_STRING          │
└──────────────────────┼───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  Fabric Event Stream: kystverket-ais-ingest      │
│                                                  │
│  ┌─────────────────┐    ┌─────────────────────┐  │
│  │ Custom Input     │───▶│ Default Stream       │  │
│  │ ais-input        │    │                      │  │
│  │ (CloudEvents     │    └──────────┬───────────┘  │
│  │  5 AIS types)    │               │              │
│  └─────────────────┘               │              │
│                          ┌──────────▼───────────┐  │
│                          │ dispatch-kql          │  │
│                          │ → _cloudevents_       │  │
│                          │   dispatch            │  │
│                          └──────────────────────┘  │
└──────────────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  KQL Eventhouse: kystverket-ais                  │
│  ┌────────────────────────────────────────────┐  │
│  │  Database: kystverket-ais                  │  │
│  │                                            │  │
│  │  Ingestion:                                │  │
│  │  └── _cloudevents_dispatch                 │  │
│  │       ├─ update policy → PositionClassA    │  │
│  │       ├─ update policy → StaticVoyageData  │  │
│  │       ├─ update policy → PositionClassB    │  │
│  │       ├─ update policy → StaticDataClassB  │  │
│  │       └─ update policy → AidToNavigation   │  │
│  │                                            │  │
│  │  Materialized Views:                       │  │
│  │  ├── PositionClassALatest                  │  │
│  │  ├── PositionClassBLatest                  │  │
│  │  ├── StaticVoyageDataLatest                │  │
│  │  ├── StaticDataClassBLatest                │  │
│  │  └── AidToNavigationLatest                 │  │
│  │                                            │  │
│  │  Functions:                                │  │
│  │  ├── VesselPositions()                     │  │
│  │  └── AISStatistics()                       │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

## Data Model

The bridge emits five CloudEvents types, each routed to its own KQL table via
update policies on the `_cloudevents_dispatch` ingestion table.

| Table | AIS Types | Description | Rate |
|---|---|---|---|
| `PositionReportClassA` | 1, 2, 3 | Class A vessel positions (SOLAS vessels) | ~20 msg/s |
| `StaticVoyageData` | 5 | Class A static info + voyage (name, dimensions, destination) | ~1 msg/s |
| `PositionReportClassB` | 18, 19 | Class B vessel positions (small craft) | ~3 msg/s |
| `StaticDataClassB` | 24 | Class B static info (name, callsign) | ~1 msg/s |
| `AidToNavigation` | 21 | Buoys, lights, and other navigation aids | ~1 msg/s |

Estimated volume: ~2.9 million events/day (~248 MB/day).

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
- A KQL database with 5 typed tables, materialized views, and analysis functions
- An Event Stream with Custom Endpoint → `_cloudevents_dispatch` table
- KQL update policies that split events by CloudEvents `type` into typed tables

Retrieve the Custom Endpoint connection string from the Fabric portal.

### 2. Deploy the container

**ARM template (ACI):**
```bash
az deployment group create \
    --resource-group kystverket-ais-rg \
    --template-file ../azure-template.json \
    --parameters connectionStringSecret="Endpoint=sb://..."
```

**Docker:**
```bash
docker run -e CONNECTION_STRING="Endpoint=sb://..." \
    ghcr.io/clemensv/real-time-sources-kystverket-ais:latest
```

**Local:**
```bash
CONNECTION_STRING="Endpoint=sb://..." python -m kystverket_ais stream
```

### 3. Query the data

In a Fabric KQL queryset or Azure Data Explorer:

```kusto
// Live vessel map — latest position + static info for all vessels
VesselPositions()
| where speed_over_ground > 0
| project mmsi, ship_name, latitude, longitude, speed_over_ground,
          course_over_ground, destination, last_update

// Message rate statistics
AISStatistics()

// All vessels currently in a geographic bounding box (e.g. Oslo fjord)
VesselPositions()
| where latitude between (59.5 .. 60.0) and longitude between (10.0 .. 11.0)

// Vessel track history for a specific MMSI
PositionReportClassA
| where mmsi == 257123456 and ___time > ago(24h)
| order by ___time asc
| project ___time, latitude, longitude, speed_over_ground, course_over_ground

// Unique vessels seen in the last hour
PositionReportClassA
| where ___time > ago(1h)
| summarize count() by mmsi
| count

// Aid-to-navigation positions
AidToNavigationLatest
| project mmsi, name, aid_type, latitude, longitude
```
