# USGS Water Services - Instantaneous Value Service Usage Guide

## Overview

**USGS-IV** is a tool designed to interact with the [USGS Water Services](https://waterservices.usgs.gov/) Instantaneous Value Service API to fetch water level data for rivers in the United States. The tool can retrieve water level data from individual stations, list available stations, or continuously poll the API to send water level updates to a Kafka topic.

## Key Features:
- **Water Level Fetching**: Retrieve current water level data for specific stations from the USGS Instantaneous Value Service API.
- **Station Listing**: List all available monitoring stations.
- **Kafka Integration**: Send water level updates as CloudEvents to a Kafka topic, supporting Microsoft Event Hubs and Microsoft Fabric Event Streams.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or get it from the Microsoft Store if you are on Windows.

### Installation Steps

Once Python is installed, you can install the tool from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=usgs-iv
```

If you clone the repository, you can install the tool as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/usgs-iv
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

### Fabric notebook hosting

A scheduled-execution variant runs the bridge inside a Microsoft Fabric notebook (`notebook/usgs-iv-feed.ipynb`) deployed via [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1); the notebook invokes `usgs-iv feed --once` per scheduled tick and persists dedupe state to the attached Lakehouse.

## How to Use

After installation, the tool can be run using the `usgs-iv` command. It supports multiple subcommands:
- **List Stations (`sites`)**: Fetch and display all available monitoring stations.
- **Feed Stations (`feed`)**: Continuously poll usgs-iv API for water levels and send updates to a Kafka topic.

### **List Stations (`sites`)**

Fetches and displays all available monitoring stations from the usgs-iv API.

#### Example Usage:

```bash
usgs-iv sites
```

### **Feed Stations (`feed`)**

Polls the usgs-iv API for water level measurements and sends them as
CloudEvents to a Kafka topic. The events are formatted using CloudEvents
structured JSON format and described in [EVENTS.md](EVENTS.md).

- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream [connection string](#connection-string-for-microsoft-event-hubs-or-fabric-event-streams) (overrides other Kafka parameters).


#### Example Usage:

```bash
usgs-iv feed --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>" --polling-interval 60
```

Alternatively, using a connection string for Microsoft Event Hubs or Microsoft Fabric Event Streams:

```bash
usgs-iv feed --connection-string "<your_connection_string>" --polling-interval 60
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
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers (comma-separated list).
- `KAFKA_TOPIC`: Kafka topic for publishing.
- `SASL_USERNAME`: SASL username for Kafka authentication.
- `SASL_PASSWORD`: SASL password for Kafka authentication.
- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `POLLING_INTERVAL`: Polling interval in seconds.

## State Management

The tool handles state internally for efficient API polling and sending updates.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template-with-eventhub.json)

## Transports

This source now ships separate Kafka, MQTT, and AMQP containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-usgs-iv-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variants for USGS site metadata. Topics are retained QoS-1 site info leaves under hydro/us/usgs/usgs-iv/{site_no}/info. The manifest intentionally uses existing schema field names site_no and parameter_cd rather than adding aliases.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/usgs_iv.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `hydro/us/usgs/usgs-iv/{site_no}/info` | `USGS.Sites.Site` | QoS 1, retain=true, expiry=2592000s |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.

## AMQP 1.0 companion feeder

This source also ships an AMQP 1.0 companion container, `ghcr.io/clemensv/real-time-sources-usgs-iv-amqp:latest`, for queue-oriented consumers using generic AMQP brokers or Azure Service Bus. It emits the same CloudEvents and payload schemas as the Kafka and MQTT variants on a single broker address (default `usgs-iv`).

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=usgs-iv   ghcr.io/clemensv/real-time-sources-usgs-iv-amqp:latest
```

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template-amqp.json)

