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
