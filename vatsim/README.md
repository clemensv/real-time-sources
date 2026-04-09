# VATSIM Live Data Feed Bridge

## Overview

The VATSIM bridge polls the VATSIM v3 live data feed and emits pilot positions,
controller positions, and network status as CloudEvents to Apache Kafka, Azure
Event Hubs, or Fabric Event Streams.

## Data Source

[VATSIM](https://vatsim.net) is the world's largest virtual aviation network.
The live data feed at `https://data.vatsim.net/v3/vatsim-data.json` provides a
JSON snapshot updated every ~15 seconds with all connected pilots and
controllers. No authentication or API key is required. Typically 1000–2000+
pilots are connected during peak hours.

## Event Types

| Type | Description | Key |
|------|-------------|-----|
| `net.vatsim.PilotPosition` | Position, speed, altitude, and flight plan summary for each pilot | `{callsign}` |
| `net.vatsim.ControllerPosition` | Frequency, facility, and ATIS for each controller | `{callsign}` |
| `net.vatsim.NetworkStatus` | Aggregate status counts emitted once per poll cycle | `status` |

See [EVENTS.md](EVENTS.md) for full schema details.

## Installation

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=vatsim
```

Or from a local clone:

```bash
cd real-time-sources/vatsim
pip install .
```

For containerized deployment, see [CONTAINER.md](CONTAINER.md).

## Usage

```bash
vatsim feed --connection-string "<connection-string>" --polling-interval 60
```

Or with explicit Kafka parameters:

```bash
vatsim feed --kafka-bootstrap-servers "<servers>" --kafka-topic "<topic>" \
    --sasl-username "<user>" --sasl-password "<pass>"
```

### Environment Variables

- `CONNECTION_STRING` — Event Hubs / Fabric connection string
- `KAFKA_BOOTSTRAP_SERVERS` — Kafka bootstrap servers
- `KAFKA_TOPIC` — Target topic
- `SASL_USERNAME` / `SASL_PASSWORD` — SASL credentials
- `POLLING_INTERVAL` — Poll interval in seconds (default: 60)

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventhub.json)
