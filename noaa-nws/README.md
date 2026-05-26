# NOAA NWS Weather Alerts Poller

## Overview

**NOAA NWS Weather Alerts Poller** polls the National Weather Service (NWS) Weather Alerts API for active weather alerts across the United States and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen alert IDs to avoid sending duplicates.

## Key Features

- **NWS Alerts Polling**: Fetch active weather alerts from the NWS API at `https://api.weather.gov/alerts/active`.
- **Deduplication**: Tracks seen alert IDs in a state file to avoid reprocessing.
- **Kafka Integration**: Send weather alerts to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).
- **Fabric notebook hosting**: A Fabric notebook (`notebook/noaa-nws-feed.ipynb`) is provided for scheduled single-cycle execution inside Microsoft Fabric via [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1).

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=noaa-nws
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/noaa-nws
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m noaa_nws`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where seen alert IDs are stored. Defaults to `~/.nws_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m noaa_nws --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m noaa_nws --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `NWS_LAST_POLLED_FILE`: File to store seen alert IDs for deduplication.

## NWS Alert Properties

Each weather alert includes these properties:

| Property | Description |
|----------|-------------|
| `alert_id` | NWS alert ID |
| `area_desc` | Description of affected area |
| `sent` | When the alert was sent |
| `effective` | When the alert becomes effective |
| `expires` | When the alert expires |
| `status` | Alert status (Actual, Exercise, System, Test, Draft) |
| `message_type` | Message type (Alert, Update, Cancel) |
| `category` | Category (Met, Geo, Safety, etc.) |
| `severity` | Severity (Extreme, Severe, Moderate, Minor, Unknown) |
| `certainty` | Certainty (Observed, Likely, Possible, Unlikely, Unknown) |
| `urgency` | Urgency (Immediate, Expected, Future, Past, Unknown) |
| `event` | Event type name |
| `sender_name` | Name of the sending office |
| `headline` | Alert headline |
| `description` | Full description |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-eventhub.json)

## MQTT and AMQP companion transports

This source now ships Kafka plus dedicated MQTT and AMQP companion containers. MQTT publishes binary-mode CloudEvents into the source-specific UNS topic tree declared in `xreg/`; AMQP publishes the same CloudEvents to the configured queue or topic address (`noaa-nws`). Docker E2E mock mode is available through `NOAA_NWS_MOCK=true`.

- MQTT image: `ghcr.io/clemensv/real-time-sources/noaa-nws-mqtt`
- AMQP image: `ghcr.io/clemensv/real-time-sources/noaa-nws-amqp`
- MQTT templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`
- AMQP templates: `azure-template-amqp.json`, `azure-template-with-servicebus.json`
