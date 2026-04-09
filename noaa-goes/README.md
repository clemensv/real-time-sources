# NOAA SWPC Space Weather Poller

## Overview

**NOAA SWPC Space Weather Poller** polls the NOAA Space Weather Prediction Center (SWPC) API endpoints for space weather data and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen data timestamps to avoid sending duplicates.

## Data Sources

The poller fetches three types of space weather data:

1. **Space Weather Alerts** — Alerts and warnings issued by SWPC for solar flares, geomagnetic storms, and other space weather events.
2. **Planetary K-index** — A measure of geomagnetic activity on a scale of 0–9, computed from ground-based magnetometer stations worldwide.
3. **Solar Wind Summary** — Real-time solar wind speed and interplanetary magnetic field (IMF) measurements from upstream spacecraft.

## Key Features

- **Multi-endpoint Polling**: Fetches alerts, planetary K-index, and solar wind data from SWPC.
- **Deduplication**: Tracks last-seen timestamps per data type to avoid reprocessing.
- **Kafka Integration**: Sends space weather data to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=noaa-goes
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/noaa-goes
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m noaa_goes`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where last-polled timestamps are stored. Defaults to `~/.swpc_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m noaa_goes --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m noaa_goes --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `SWPC_LAST_POLLED_FILE`: File to store last-polled timestamps for deduplication.

## SWPC Data Fields

### Space Weather Alert

| Property | Description |
|----------|-------------|
| `product_id` | Alert product ID |
| `issue_datetime` | When the alert was issued |
| `message` | Full alert message text |

### Planetary K-Index

| Property | Description |
|----------|-------------|
| `time_tag` | Timestamp of the measurement |
| `kp` | Planetary K-index value (0-9) |
| `kp_fraction` | Fractional K-index |
| `a_running` | Running A-index |
| `station_count` | Number of stations used |

### Solar Wind Summary

| Property | Description |
|----------|-------------|
| `timestamp` | Timestamp of the measurement |
| `wind_speed` | Solar wind speed in km/s |
| `bt` | Total magnetic field strength in nT |
| `bz` | North-south magnetic field component in nT |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-with-eventhub.json)
