# Kystverket AIS Bridge Usage Guide

## Overview

**Kystverket AIS Bridge** connects to the Norwegian Coastal Administration's
(Kystverket) real-time AIS vessel tracking stream and forwards decoded messages
to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format.

Unlike the other bridges in this repository, this is a **streaming** bridge — it
connects to a raw TCP socket and continuously forwards AIS messages rather than
polling an API.

## Key Features

- **Real-time AIS streaming**: ~34 msg/sec, ~2.9 million messages/day
- **5 event types**: Position reports (Class A/B), static & voyage data,
  aids to navigation
- **Multi-sentence reassembly**: Handles fragmented AIS type 5 and type 24
  messages
- **MMSI filtering**: Optionally restrict to specific vessel MMSIs
- **Message type filtering**: Select which AIS message types to forward
- **Auto-reconnect**: Exponential backoff on TCP connection failures
- **Kafka Integration**: SASL PLAIN authentication for Event Hubs / Fabric
  Event Streams

## Data Source

The [Kystverket AIS stream](https://kystverket.no/navigasjonstjenester/ais/)
provides open access to real-time AIS data covering the Norwegian economic zone,
including Svalbard and Jan Mayen. The data is provided under the
[NLOD](https://data.norge.no/nlod/en/2.0) license.

- **TCP endpoint**: `153.44.253.27:5631` (open, no authentication)
- **Format**: NMEA AIVDM/AIVDO sentences with Kystverket tag blocks
- **Coverage**: Norwegian economic zone, 50+ terrestrial + offshore stations

## Installation

Requires Python 3.10 or later.

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=kystverket-ais
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/kystverket-ais
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `kystverket-ais` command.

The events sent to Kafka are formatted as CloudEvents, documented in
[EVENTS.md](EVENTS.md).

### Probe the Live Stream

Test connectivity and see decoded messages:

```bash
kystverket-ais probe
```

### Stream to Kafka

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
kystverket-ais stream --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
kystverket-ais stream \
    --kafka-bootstrap-servers "<bootstrap_servers>" \
    --kafka-topic "<topic_name>" \
    --sasl-username "<username>" \
    --sasl-password "<password>"
```

### Command-Line Arguments (stream)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `--tcp-host` | `AIS_TCP_HOST` | AIS TCP stream host (default: `153.44.253.27`) |
| `--tcp-port` | `AIS_TCP_PORT` | AIS TCP stream port (default: `5631`) |
| `--message-types` | `AIS_MESSAGE_TYPES` | Comma-separated AIS types (default: `1,2,3,5,18,19,24,21`) |
| `--mmsi-filter` | `AIS_FILTER_MMSI` | Comma-separated MMSIs to include (default: all) |
| `--flush-interval` | `AIS_FLUSH_INTERVAL` | Flush Kafka every N events (default: `1000`) |

### Examples

#### Stream Only Position Reports

```bash
kystverket-ais stream -c "<conn_string>" --message-types 1,2,3,18,19
```

#### Track Specific Vessels

```bash
kystverket-ais stream -c "<conn_string>" --mmsi-filter 258028380,257093980
```

## AIS Message Types

| Type | Event | Description |
|------|-------|-------------|
| 1, 2, 3 | `PositionReportClassA` | Class A position reports (SOLAS vessels) |
| 5 | `StaticVoyageData` | Ship name, IMO, callsign, dimensions, destination |
| 18, 19 | `PositionReportClassB` | Class B position reports (smaller vessels) |
| 24 | `StaticDataClassB` | Class B static data (name, callsign, dimensions) |
| 21 | `AidToNavigation` | Buoys, lighthouses, and other navigational aids |
