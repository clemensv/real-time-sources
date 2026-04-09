# Paris Bicycle Counters Poller

## Overview

**Paris Bicycle Counters Poller** polls the Paris Open Data platform for hourly bicycle counts from 141 permanent counting stations across Paris and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen observations to avoid sending duplicates.

## Key Features

- **Bicycle Count Polling**: Fetch hourly bicycle counts from `https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs/records`.
- **Counter Reference Data**: Fetch counter location metadata from `https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-compteurs/records`.
- **Deduplication**: Tracks seen counter_id + date pairs in a state file to avoid reprocessing.
- **Kafka Integration**: Send bicycle counts to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=paris-bicycle-counters
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/paris-bicycle-counters
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m paris_bicycle_counters`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where last seen state is stored. Defaults to `~/.paris_velo_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m paris_bicycle_counters --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m paris_bicycle_counters --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `PARIS_VELO_LAST_POLLED_FILE`: File to store last seen state for deduplication.

## Bicycle Count Properties

Each bicycle count observation includes these properties:

| Property | Type | Description |
|----------|------|-------------|
| `counter_id` | string | Unique counter channel identifier |
| `counter_name` | string | Human-readable counter name with street and direction |
| `count` | integer | Number of bicycles counted in the one-hour window |
| `date` | datetime | Start of the one-hour counting window (ISO 8601) |
| `longitude` | double | Counter longitude (WGS 84) |
| `latitude` | double | Counter latitude (WGS 84) |

## Counter Reference Properties

| Property | Type | Description |
|----------|------|-------------|
| `counter_id` | string | Unique counter channel identifier |
| `counter_name` | string | Human-readable counter name |
| `channel_name` | string | Directional channel label (e.g., "SE-NO") |
| `installation_date` | string | Installation date (YYYY-MM-DD) |
| `longitude` | double | Counter longitude (WGS 84) |
| `latitude` | double | Counter latitude (WGS 84) |

## Data Source

The City of Paris maintains a network of 141 permanent bicycle counting stations that measure bicycle traffic with hourly resolution. Data is published daily (J-1) under the Licence Ouverte 2.0.

- **Counter data**: `https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs`
- **Counter locations**: `https://opendata.paris.fr/explore/dataset/comptage-velo-compteurs`
- **Paris Open Data**: `https://opendata.paris.fr/`

## License

[MIT](../LICENSE.md)

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template-with-eventhub.json)
