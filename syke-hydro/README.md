# SYKE Hydrology Bridge Usage Guide

## Overview

**SYKE Hydrology Bridge** connects to the Finnish Environment Institute's (SYKE)
hydrological monitoring network — via the
[Hydrology OData API](https://rajapinnat.ymparisto.fi/api/Hydrologiarajapinta/1.1/odata)
— and forwards water level and discharge observations to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format.

This is a **polling** bridge. The upstream API exposes real-time readings from
SYKE's network of river and lake gauging stations across Finland. The bridge
polls for the latest measurements, de-duplicates them against local state, and
emits only new or changed readings.

## Key Features

- **Finnish national coverage**: Active hydrological monitoring stations on
  rivers and lakes throughout Finland
- **Two measurement parameters**: Water level (cm) and discharge (m³/s)
- **Two event types**: Station reference data and water level observations
- **Delta-only emission**: De-duplicates against a local state file — only new
  readings are forwarded
- **OData pagination**: Automatically pages through large result sets from the
  upstream API
- **Configurable polling interval**: Default 3600 seconds (1 hour), matching the
  upstream update cadence
- **Kafka integration**: SASL PLAIN authentication for Event Hubs / Fabric Event
  Streams

## Data Source

The bridge reads from the [SYKE Open Data Hydrology
API](https://rajapinnat.ymparisto.fi/api/Hydrologiarajapinta/1.1/odata),
provided by the Finnish Environment Institute (Suomen ympäristökeskus).

- **API base URL**:
  `https://rajapinnat.ymparisto.fi/api/Hydrologiarajapinta/1.1/odata`
- **Endpoints used**: `Paikka` (station metadata), `Vedenkorkeus` (water
  levels), and `Virtaama` (discharge)
- **Authentication**: None required
- **Update frequency**: ~1 hour
- **License**: Finnish Open Data

## Installation

Requires Python 3.10 or later.

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=syke-hydro
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/syke-hydro
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md)
instructions.

## How to Use

After installation, the tool can be run using `python -m syke_hydro`. It
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
python -m syke_hydro list
```

Output shows station ID, name, main water area, and coordinates.

### Feed to Kafka

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
python -m syke_hydro feed --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m syke_hydro feed \
    --connection-string "BootstrapServer=<bootstrap_servers>;EntityPath=<topic>"
```

Or via environment variables:

```bash
export KAFKA_BROKER="<bootstrap_servers>"
export KAFKA_TOPIC="<topic_name>"
python -m syke_hydro feed
```

### Command-Line Arguments (feed)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `--connection-string` | `CONNECTION_STRING` or `KAFKA_CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string |
| `--topic` | `KAFKA_TOPIC` | Kafka topic name (default: `syke-hydro`) |
| `--polling-interval` | `POLLING_INTERVAL` | Polling interval in seconds (default: `3600`) |
| `--state-file` | `STATE_FILE` | Path to the de-duplication state file (default: `~/.syke_hydro_state.json`) |

## Event Types

| CloudEvents `type` | Description |
|---------------------|-------------|
| `FI.SYKE.Hydrology.Station` | Station reference data: ID, name, water area, municipality, coordinates |
| `FI.SYKE.Hydrology.WaterLevelObservation` | Observation: water level and discharge with timestamps |

All events use `{station_id}` as the Kafka key and CloudEvents `subject`.

### Station

Emitted once at startup for each monitoring station.

| Field | Type | Description |
|-------|------|-------------|
| `station_id` | string | SYKE station identifier (Paikka_Id) |
| `name` | string | Station name |
| `river_name` | string | Main water area name |
| `water_area_name` | string | Water area name |
| `municipality` | string | Municipality name |
| `latitude` | double | WGS84 latitude |
| `longitude` | double | WGS84 longitude |

### WaterLevelObservation

Emitted on each polling cycle for stations with new readings.

| Field | Type | Description |
|-------|------|-------------|
| `station_id` | string | SYKE station identifier (Paikka_Id) |
| `water_level` | double | Water level reading |
| `water_level_unit` | string | Unit of measurement (`cm`) |
| `water_level_timestamp` | datetime | Timestamp of the water level reading |
| `discharge` | double | Water discharge reading |
| `discharge_unit` | string | Unit of measurement (`m3/s`) |
| `discharge_timestamp` | datetime | Timestamp of the discharge reading |

## State Management

The bridge maintains a JSON state file (default: `~/.syke_hydro_state.json`)
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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template-with-eventhub.json)
