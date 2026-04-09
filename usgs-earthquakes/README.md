# USGS Earthquake Hazards Program - Real-time Earthquake Feed

## Overview

**USGS-Earthquakes** is a tool designed to interact with the [USGS Earthquake
Hazards Program](https://earthquake.usgs.gov/) real-time GeoJSON feeds to fetch
earthquake event data. The tool can list recent earthquakes, display available
feeds, or continuously poll the API to send earthquake events to a Kafka topic.

The USGS provides real-time earthquake data updated every minute for various
magnitude thresholds and time windows. This bridge converts those events into
[CloudEvents](https://cloudevents.io/) structured JSON format and publishes them
to Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

## Key Features:
- **Earthquake Event Fetching**: Retrieve real-time earthquake data from 20+ USGS GeoJSON feeds.
- **Magnitude Filtering**: Filter events client-side by minimum magnitude.
- **Deduplication**: Tracks seen events by ID and update timestamp — only new or updated events are forwarded.
- **Kafka Integration**: Send earthquake events as CloudEvents to a Kafka topic, supporting Microsoft Event Hubs and Microsoft Fabric Event Streams.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can
download Python from [here](https://www.python.org/downloads/) or get it from
the Microsoft Store if you are on Windows.

### Installation Steps

Once Python is installed, you can install the tool from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=usgs-earthquakes
```

If you clone the repository, you can install the tool as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/usgs-earthquakes
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `usgs-earthquakes` command. It
supports multiple subcommands:
- **List Events (`events`)**: Fetch and display recent earthquake events.
- **List Feeds (`feeds`)**: Show all available USGS GeoJSON feeds.
- **Feed Events (`feed`)**: Continuously poll USGS earthquake feeds and send updates to a Kafka topic.

### **List Events (`events`)**

Fetches and displays recent earthquake events from a specified USGS feed.

#### Example Usage:

```bash
usgs-earthquakes events
usgs-earthquakes events --feed m4.5_day
usgs-earthquakes events --feed all_hour --min-magnitude 3.0
```

### **List Feeds (`feeds`)**

Lists all available USGS earthquake GeoJSON feeds and their URLs.

```bash
usgs-earthquakes feeds
```

### **Feed Events (`feed`)**

Polls a USGS earthquake feed and sends earthquake events as CloudEvents to a
Kafka topic. The events are formatted using CloudEvents structured JSON format
and described in [EVENTS.md](EVENTS.md).

- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream [connection string](#connection-string-for-microsoft-event-hubs-or-fabric-event-streams) (overrides other Kafka parameters).
- `--feed`: Feed to poll (default: `all_hour`). See `usgs-earthquakes feeds` for options.
- `--min-magnitude`: Optional client-side minimum magnitude filter.

#### Example Usage:

```bash
usgs-earthquakes feed --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

Alternatively, using a connection string for Microsoft Event Hubs or Microsoft
Fabric Event Streams:

```bash
usgs-earthquakes feed --connection-string "<your_connection_string>"
```

To poll only significant earthquakes (M4.5+) from the past day:

```bash
usgs-earthquakes feed --connection-string "<your_connection_string>" --feed m4.5_day
```

### Connection String for Microsoft Event Hubs or Fabric Event Streams

The connection string format is as follows:

```
Endpoint=sb://<your-event-hubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy-name>;SharedAccessKey=<access-key>;EntityPath=<event-hub-name>
```

When provided, the connection string is parsed to extract the Kafka configuration parameters:
- **Bootstrap Servers**: Derived from the `Endpoint` value.
- **Kafka Topic**: Derived from the `EntityPath` value.
- **SASL Username and Password**: The username is set to `'$ConnectionString'`, and the password is the entire connection string.

### Environment Variables

The tool supports the following environment variables to avoid passing them via the command line:
- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `USGS_EQ_LAST_POLLED_FILE`: Path to file storing the last polled event IDs (default: `~/.usgs_earthquakes_last_polled.json`).
- `LOG_LEVEL`: Logging level (default: INFO).

## Available Feeds

The following USGS GeoJSON feeds are available:

| Feed | Description |
|------|-------------|
| `all_hour` | All earthquakes, past hour (default) |
| `all_day` | All earthquakes, past day |
| `all_week` | All earthquakes, past week |
| `all_month` | All earthquakes, past month |
| `m1.0_hour` | M1.0+ earthquakes, past hour |
| `m1.0_day` | M1.0+ earthquakes, past day |
| `m2.5_hour` | M2.5+ earthquakes, past hour |
| `m2.5_day` | M2.5+ earthquakes, past day |
| `m4.5_hour` | M4.5+ earthquakes, past hour |
| `m4.5_day` | M4.5+ earthquakes, past day |
| `significant_hour` | Significant earthquakes, past hour |
| `significant_day` | Significant earthquakes, past day |

... and more variations for week and month time periods.

## State Management

The tool tracks event IDs and their last update timestamps in a local JSON file.
Only new events or events that have been updated since last seen are forwarded to
Kafka. Old entries are pruned after 30 days.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-with-eventhub.json)
