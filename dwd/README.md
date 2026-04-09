# DWD Open Data Bridge Usage Guide

## Overview

**DWD Open Data Bridge** polls the [Deutscher Wetterdienst (DWD) Climate Data
Center](https://opendata.dwd.de/) open-data file server for weather
observations, station metadata, and weather alerts from ~1,450 stations across
Germany. The data is forwarded to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format.

## Key Features

- **10-Minute Observations**: Air temperature, precipitation, wind, and solar
  radiation updated every 10 minutes from the DWD "now" dataset.
- **Station Metadata**: Station list with coordinates, elevation, and state for
  all reporting stations.
- **Weather Alerts**: CAP (Common Alerting Protocol) weather alerts from the DWD
  warning system.
- **Hourly Observations** (optional): Recent hourly data including cloud cover.
- **Modular Architecture**: Enable or disable individual data modules.
- **Kafka Integration**: Send data to Apache Kafka, Azure Event Hubs, or
  Microsoft Fabric Event Streams using SASL PLAIN authentication.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can
download Python from [here](https://www.python.org/downloads/) or from the
Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=dwd
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/dwd
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `dwd` command. It supports
several subcommands.

The events sent to Kafka are formatted as CloudEvents, documented in
[EVENTS.md](EVENTS.md).

### List Available Modules

```bash
dwd list-modules
```

Output:

```
  station_metadata          ON   poll=3600s
  station_obs_10min         ON   poll=600s
  station_obs_hourly        OFF  poll=3600s
  weather_alerts            ON   poll=300s
```

### Start the Feed

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
dwd feed --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
dwd feed \
    --kafka-bootstrap-servers "<bootstrap_servers>" \
    --kafka-topic "<topic_name>" \
    --sasl-username "<username>" \
    --sasl-password "<password>"
```

### Command-Line Arguments (feed)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `-i`, `--polling-interval` | `POLLING_INTERVAL` | Global poll interval override (seconds) |
| `--state-file` | `STATE_FILE` | Path to state checkpoint file (default: `~/.dwd_state.json`) |
| `--modules` | `DWD_MODULES` | Comma-separated list of modules to enable |
| `--modules-disabled` | `DWD_MODULES_DISABLED` | Comma-separated list of modules to disable |
| `--10min-params` | `DWD_10MIN_PARAMS` | Comma-separated 10-min categories (default: air_temperature,precipitation,wind,solar) |
| `--stations` | `DWD_STATIONS` | Comma-separated station IDs to include (default: all) |
| `--base-url` | `DWD_BASE_URL` | DWD server base URL (default: `https://opendata.dwd.de`) |

### Examples

#### Poll Only Weather Alerts

```bash
dwd feed -c "<conn_string>" --modules weather_alerts
```

#### Poll Only Air Temperature for Specific Stations

```bash
dwd feed -c "<conn_string>" --modules station_obs_10min --10min-params air_temperature --stations 44,73,433
```

## Modules

### station_metadata (default: ON, poll: 3600s)

Fetches station lists from the DWD CDC station description files, merges them,
and emits a `StationMetadata` event for each station when changes are detected.
Covers ~1,450 stations across all 16 German states.

### station_obs_10min (default: ON, poll: 600s)

Polls the DWD 10-minute "now" datasets. Downloads ZIP archives containing
semicolon-delimited CSV files with recent observations. Tracks the latest
timestamp per station per category to emit only new measurements.

Categories: `air_temperature`, `precipitation`, `wind`, `solar`,
`extreme_wind`, `extreme_temperature`.

### station_obs_hourly (default: OFF, poll: 3600s)

Polls hourly "recent" datasets. Disabled by default because the data only
updates once per day and is not truly real-time.

### weather_alerts (default: ON, poll: 300s)

Downloads the LATEST CAP alert bundle from DWD, extracts individual XML alert
files, and emits new alerts. Tracks seen alert identifiers to avoid duplicates.

## Data Source

All data originates from the [DWD Open Data Server](https://opendata.dwd.de/)
which provides free access to weather and climate data under the
[GeoNutzV](https://www.gesetze-im-internet.de/geonutzv/) license.

## Data Management

The bridge maintains a state file (default `~/.dwd_state.json`) to track:
- Last-seen timestamps per station per category (for deduplication)
- Seen alert identifiers (to avoid re-emitting active alerts)
- Directory listing timestamps (to skip unchanged directories)

This ensures the bridge only emits new data on each poll cycle.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-eventhub.json)
