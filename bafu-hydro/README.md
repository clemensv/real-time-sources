# BAFU Hydrology Bridge Usage Guide

## Overview

**BAFU Hydrology Bridge** connects to the Swiss Federal Office for the
Environment's (BAFU/FOEN) hydrological monitoring network — via the
[existenz.ch](https://api.existenz.ch) community API — and forwards water level,
discharge, and temperature observations to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format.

This is a **polling** bridge. The upstream API aggregates readings from BAFU's
network of river and lake gauging stations across Switzerland. The bridge polls
for the latest measurements, de-duplicates them against local state, and emits
only new or changed readings.

## Key Features

- **Swiss national coverage**: ~300 hydrological monitoring stations on rivers
  and lakes throughout Switzerland
- **Three measurement parameters**: Water level (m), discharge (m³/s), and water
  temperature (°C)
- **Two event types**: Station reference data and water level observations
- **Delta-only emission**: De-duplicates against a local state file — only new
  readings are forwarded
- **Configurable polling interval**: Default 600 seconds (10 minutes), matching
  the upstream update cadence
- **Kafka integration**: SASL PLAIN authentication for Event Hubs / Fabric Event
  Streams

## Data Source

The bridge reads from the [existenz.ch Hydro API](https://api.existenz.ch),
which wraps the official BAFU/FOEN data published at
[hydrodaten.admin.ch](https://www.hydrodaten.admin.ch). The data is provided by
the Swiss Confederation's Federal Office for the Environment.

- **API base URL**: `https://api.existenz.ch/apiv1/hydro`
- **Endpoints used**: `/locations` (station metadata) and `/latest` (current
  readings)
- **Authentication**: None required
- **Update frequency**: ~10 minutes
- **License**: Swiss Open Government Data

## Installation

Requires Python 3.10 or later.

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=bafu-hydro
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/bafu-hydro
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md)
instructions.

## How to Use

After installation, the tool can be run using `python -m bafu_hydro`. It
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
python -m bafu_hydro list
```

Output shows station ID, name, water body, and coordinates.

### Feed to Kafka

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
python -m bafu_hydro feed --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m bafu_hydro feed \
    --connection-string "BootstrapServer=<bootstrap_servers>;EntityPath=<topic>"
```

Or via environment variables:

```bash
export KAFKA_BROKER="<bootstrap_servers>"
export KAFKA_TOPIC="<topic_name>"
python -m bafu_hydro feed
```

### Command-Line Arguments (feed)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `--connection-string` | `CONNECTION_STRING` or `KAFKA_CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string |
| `--topic` | `KAFKA_TOPIC` | Kafka topic name (default: `bafu-hydro`) |
| `--polling-interval` | `POLLING_INTERVAL` | Polling interval in seconds (default: `600`) |
| `--state-file` | `STATE_FILE` | Path to the de-duplication state file (default: `~/.bafu_hydro_state.json`) |

## Event Types

| CloudEvents `type` | Description |
|---------------------|-------------|
| `CH.BAFU.Hydrology.Station` | Station reference data: ID, name, water body, coordinates |
| `CH.BAFU.Hydrology.WaterLevelObservation` | Observation: water level, discharge, water temperature with timestamps |

All events use `{station_id}` as the Kafka key and CloudEvents `subject`.

### Station

Emitted once at startup for each monitoring station.

| Field | Type | Description |
|-------|------|-------------|
| `station_id` | string | BAFU station identifier |
| `name` | string | Station name |
| `water_body_name` | string | Name of the river or lake |
| `water_body_type` | string | Water body classification |
| `latitude` | double | WGS84 latitude |
| `longitude` | double | WGS84 longitude |

### WaterLevelObservation

Emitted on each polling cycle for stations with new readings.

| Field | Type | Description |
|-------|------|-------------|
| `station_id` | string | BAFU station identifier |
| `water_level` | double | Water level reading |
| `water_level_unit` | string | Unit of measurement (`m`) |
| `water_level_timestamp` | datetime | Timestamp of the water level reading |
| `discharge` | double | Water discharge reading |
| `discharge_unit` | string | Unit of measurement (`m3/s`) |
| `discharge_timestamp` | datetime | Timestamp of the discharge reading |
| `water_temperature` | double | Water temperature reading |
| `water_temperature_unit` | string | Unit of measurement (`C`) |
| `water_temperature_timestamp` | datetime | Timestamp of the temperature reading |

## State Management

The bridge maintains a JSON state file (default: `~/.bafu_hydro_state.json`)
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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template-with-eventhub.json)
