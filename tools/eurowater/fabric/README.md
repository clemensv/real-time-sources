# Fabric Event Stream + KQL Database Setup

Sets up a Microsoft Fabric Event Stream with SQL normalization operators and a
KQL (Eventhouse) database to receive normalized European water data from all 8
source services.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ACI Container Group / Docker Compose                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │Pegelonline│ │CHMI Hydro│ │IMGW Hydro│ │SMHI Hydro│ │ Hub'Eau  │ ... │
│  └─────┬─────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘     │
│        └──────────────┴────────────┴────────────┴────────────┘          │
│                                    │ CONNECTION_STRING                   │
└────────────────────────────────────┼────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Fabric Event Stream: eurowater-ingest                                  │
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────────────────┐                 │
│  │ Custom Input     │───▶│ SQL Operator: normalize      │                │
│  │ eurowater-input  │    │                               │                │
│  │ (mixed events    │    │ normalize_stations.sql        │                │
│  │  from 8 sources) │    │  → EU.Eurowater.Station       │                │
│  └─────────────────┘    │                               │                │
│                          │ normalize_measurements.sql    │                │
│                          │  → EU.Eurowater.Measurement   │                │
│                          └──────────┬────────────────────┘                │
│                                     │                                    │
│                          ┌──────────┴──────────┐                         │
│                          ▼                     ▼                         │
│                   ┌─────────────┐      ┌──────────────────┐             │
│                   │ StationOutput│      │MeasurementOutput │             │
│                   └──────┬──────┘      └────────┬─────────┘             │
└──────────────────────────┼──────────────────────┼───────────────────────┘
                           ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  KQL Eventhouse: eurowater                                              │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  Database: eurowater                                         │       │
│  │                                                              │       │
│  │  Tables:              Materialized Views:                    │       │
│  │  ├── Stations         ├── StationsLatest                     │       │
│  │  └── Measurements     └── MeasurementsLatest                 │       │
│  │                                                              │       │
│  │  Functions:                                                  │       │
│  │  └── StationMeasurements() — joined view                    │       │
│  └──────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────┘
```

## Normalized Data Model

The SQL operator remaps all 8 heterogeneous input formats into two consistent
output types defined in [eurowater.xreg.json](eurowater.xreg.json):

### EU.Eurowater.Station

| Field | Type | Description |
|---|---|---|
| `station_id` | string | `{country_code}-{source_id}`, e.g. `de-2480010`, `cz-0-203-1-001000` |
| `country_code` | string | ISO 3166-1 alpha-2: de, cz, pl, se, fr, gb, nl, be |
| `source_station_id` | string | Original ID from the source system |
| `station_name` | string | Display name |
| `river_name` | string | River/waterway name (null if unavailable) |
| `latitude` | number | WGS84 |
| `longitude` | number | WGS84 |
| `source_system` | string | Source identifier (e.g. `pegelonline`, `chmi-hydro`) |
| `source_url` | string | Source API URL |

### EU.Eurowater.Measurement

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Normalized station ID matching Stations table |
| `country_code` | string | ISO 3166-1 alpha-2 |
| `timestamp` | datetime | Measurement time (ISO 8601 UTC) |
| `parameter` | string | `water_level`, `discharge`, or `water_temperature` |
| `value` | number | Measured value |
| `unit` | string | `cm`, `m`, `m3/s`, or `C` |
| `quality` | string | Quality indicator from source (null if unavailable) |
| `source_system` | string | Source identifier |

### Unit normalization

| Source | Parameter | Source Unit | Normalized |
|---|---|---|---|
| Hub'Eau (FR) | water_level | mm | cm (÷10) |
| Hub'Eau (FR) | discharge | L/s | m³/s (÷1000) |
| UK EA (GB) | water_level | m | m (as-is) |
| All others | water_level | cm | cm (as-is) |
| All | discharge | m³/s | m³/s (as-is) |
| All | water_temperature | °C | C (as-is) |

## Files

| File | Description |
|---|---|
| `setup.ps1` | PowerShell setup script (Azure CLI + Fabric REST API) |
| `setup.sh` | Bash setup script (Azure CLI + Fabric REST API) |
| `eurowater.xreg.json` | xRegistry definition for the normalized output model |
| `normalize_stations.sql` | SQL operator query for station normalization |
| `normalize_measurements.sql` | SQL operator query for measurement normalization |
| `kql_database.kql` | KQL commands to create tables, mappings, views, and functions |

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

This creates a KQL database in the existing Eventhouse, an Event Stream with
Custom Endpoint source, SQL normalization operator, and Eventhouse destinations.
Retrieve the Custom Endpoint connection string from the Fabric portal.

### 2. Deploy the container group

Use the connection string from step 1:

```powershell
# ACI deployment
../deploy.ps1 -ResourceGroupName eurowater-rg -ConnectionString "<connection-string>"

# Or Docker Compose
$env:CONNECTION_STRING = "<connection-string>"
docker compose -f ../docker-compose.yml up -d
```

### 3. Query the data

In the Fabric KQL queryset or Azure Data Explorer:

```kusto
// Latest measurements joined with station metadata
StationMeasurements()
| where country_code == "de"
| project station_name, river_name, parameter, value, unit, timestamp

// All water level readings in the last hour
Measurements
| where timestamp > ago(1h) and parameter == "water_level"
| join kind=inner StationsLatest on station_id
| project station_name, country_code, value, unit, timestamp, latitude, longitude

// Station count by country
StationsLatest
| summarize count() by country_code
| render piechart

// Measurement rate by source
Measurements
| where ingestion_time > ago(1h)
| summarize count() by source_system, bin(ingestion_time, 5m)
| render timechart
```
