# NVE Hydrology Bridge Usage Guide

## Overview

**NVE Hydrology Bridge** connects to the Norwegian Water Resources and Energy
Directorate's (NVE) hydrological monitoring network — via the
[HydAPI](https://hydapi.nve.no) REST API — and forwards water level and
discharge observations to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format.

This is a **polling** bridge. The upstream API provides access to real-time
readings from NVE's network of river and lake gauging stations across Norway. The
bridge polls for the latest measurements, de-duplicates them against local state,
and emits only new or changed readings.

## Key Features

- **Norwegian national coverage**: Active hydrological monitoring stations on
  rivers and lakes throughout Norway
- **Two measurement parameters**: Water level (m) and discharge (m³/s)
- **Two event types**: Station reference data and water level observations
- **Delta-only emission**: De-duplicates against a local state file — only new
  readings are forwarded
- **Parallel fetching**: Concurrent observation retrieval across stations (10
  workers)
- **Configurable polling interval**: Default 600 seconds (10 minutes)
- **Kafka integration**: SASL PLAIN authentication for Event Hubs / Fabric Event
  Streams

## Data Source

The bridge reads from the [NVE HydAPI](https://hydapi.nve.no/), the official
hydrological data API provided by the Norwegian Water Resources and Energy
Directorate (Norges vassdrags- og energidirektorat).

- **API base URL**: `https://hydapi.nve.no/api/v1`
- **Endpoints used**: `/Stations` (station metadata) and `/Observations` (current
  readings)
- **Authentication**: API key required (register at
  [hydapi.nve.no](https://hydapi.nve.no/UserDocumentation/))
- **Update frequency**: ~10 minutes
- **License**: Norwegian Licence for Open Government Data (NLOD)

## Installation

Requires Python 3.10 or later.

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=nve-hydro
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/nve-hydro
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md)
instructions.

## How to Use

After installation, the tool can be run using `python -m nve_hydro`. It
supports two subcommands:

- **List Stations (`list`)**: Fetch and display all available monitoring
  stations.
- **Feed to Kafka (`feed`)**: Continuously poll the API and send water level
  updates to a Kafka topic.

The events sent to Kafka are formatted as CloudEvents, documented in
[EVENTS.md](EVENTS.md).

### List Stations

Fetches and displays all available monitoring stations:

```bash
python -m nve_hydro list --api-key "<your_api_key>"
```

Output shows station ID, name, river, coordinates, and available parameters.

### Feed to Kafka

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
python -m nve_hydro feed \
    --api-key "<your_api_key>" \
    --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m nve_hydro feed \
    --api-key "<your_api_key>" \
    --connection-string "BootstrapServer=<bootstrap_servers>;EntityPath=<topic>"
```

Or via environment variables:

```bash
export NVE_API_KEY="<your_api_key>"
export KAFKA_BROKER="<bootstrap_servers>"
export KAFKA_TOPIC="<topic_name>"
python -m nve_hydro feed
```

### Command-Line Arguments (feed)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `--connection-string` | `CONNECTION_STRING` or `KAFKA_CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string |
| `--topic` | `KAFKA_TOPIC` | Kafka topic name (default: `nve-hydro`) |
| `--polling-interval` | `POLLING_INTERVAL` | Polling interval in seconds (default: `600`) |
| `--state-file` | `STATE_FILE` | Path to the de-duplication state file (default: `~/.nve_hydro_state.json`) |
| `--api-key` | `NVE_API_KEY` | NVE HydAPI key (required) |

## Event Types

| CloudEvents `type` | Description |
|---------------------|-------------|
| `NO.NVE.Hydrology.Station` | Station reference data: ID, name, river, coordinates, elevation, municipality |
| `NO.NVE.Hydrology.WaterLevelObservation` | Observation: water level and discharge with timestamps |

All events use `{station_id}` as the Kafka key and CloudEvents `subject`.

### Station

Emitted once at startup for each monitoring station.

| Field | Type | Description |
|-------|------|-------------|
| `station_id` | string | NVE station identifier |
| `station_name` | string | Station name |
| `river_name` | string | Name of the river |
| `latitude` | double | WGS84 latitude |
| `longitude` | double | WGS84 longitude |
| `masl` | double | Meters above sea level |
| `council_name` | string | Municipality (kommune) name |
| `county_name` | string | County (fylke) name |
| `drainage_basin_area` | double | Drainage basin area (km²) |

### WaterLevelObservation

Emitted on each polling cycle for stations with new readings.

| Field | Type | Description |
|-------|------|-------------|
| `station_id` | string | NVE station identifier |
| `water_level` | double | Water level reading |
| `water_level_unit` | string | Unit of measurement (`m`) |
| `water_level_timestamp` | datetime | Timestamp of the water level reading |
| `discharge` | double | Water discharge reading |
| `discharge_unit` | string | Unit of measurement (`m3/s`) |
| `discharge_timestamp` | datetime | Timestamp of the discharge reading |

## State Management

The bridge maintains a JSON state file (default: `~/.nve_hydro_state.json`)
that tracks which readings have already been forwarded. This ensures that only
new observations are emitted after restarts. The state file is automatically
pruned to the most recent 50,000 entries to prevent unbounded growth.

## Connection String Format

The connection string format for Azure Event Hubs or Fabric Event Streams:

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

When provided, the connection string is parsed to extract:
- **Bootstrap Servers**: Derived from the `Endpoint` value
- **Kafka Topic**: Derived from the `EntityPath` value
- **SASL credentials**: Configured automatically for SASL_SSL/PLAIN

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template-with-eventhub.json)
