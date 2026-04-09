# AISstream.io Bridge Usage Guide

## Overview

**AISstream.io Bridge** connects to the AISstream.io WebSocket API for
real-time global AIS vessel tracking and forwards decoded messages to a
Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format.

This is a **streaming** bridge — it holds an open WebSocket connection and
continuously forwards AIS messages rather than polling an API.

> **⚠️ Reliability Warning:** AISstream.io is a free, community-run service
> with no SLA. During our testing on 2026-04-02, the WebSocket accepted
> connections and API keys without error but delivered **zero messages** over
> sustained periods — the data pipeline behind the socket was simply dry.
> This is consistent with the pattern of silent outages documented in
> [GitHub issue #134](https://github.com/aisstream/issues/issues/134). The
> bridge includes aggressive reconnection logic, but you should expect data
> gaps ranging from minutes to days. If you need reliable AIS data, consider
> the [Kystverket AIS bridge](../kystverket-ais/) for Norwegian waters or a
> commercial provider for global coverage.

## Key Features

- **Global AIS coverage**: Terrestrial AIS data from coastlines worldwide
  (~200 km from shore)
- **23 event types**: All ITU-R M.1371-5 AIS message types supported
- **Server-side filtering**: Geographic bounding boxes, MMSI lists, and
  message type filters applied at the source
- **Client-side MMSI filter**: Additional local filtering for fine-grained
  control
- **Auto-reconnect**: Exponential backoff on WebSocket failures (critical
  for this service)
- **Kafka Integration**: SASL PLAIN authentication for Event Hubs / Fabric
  Event Streams

## Data Source

[AISstream.io](https://aisstream.io/) provides a free WebSocket API for
global terrestrial AIS data. The service aggregates data from ground
stations worldwide and delivers pre-decoded JSON messages.

- **WebSocket endpoint**: `wss://stream.aisstream.io/v0/stream`
- **Authentication**: API key (free registration via GitHub OAuth)
- **Format**: Pre-decoded JSON with MetaData envelope
- **Coverage**: Global terrestrial (~200 km from coastlines)
- **Satellite AIS**: Not included — open ocean is dark

**Reliability warning**: This service has no SLA and has historically
experienced multi-day outages and Cloudflare-related connectivity issues.
The bridge includes aggressive reconnection logic, but data gaps are
expected.

## Installation

Requires Python 3.10 or later.

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/aisstream
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md)
instructions.

## How to Use

After installation, the tool can be run using the `aisstream` command.

The events sent to Kafka are formatted as CloudEvents, documented in
[EVENTS.md](EVENTS.md).

### Probe the Live Stream

Test connectivity and see decoded messages:

```bash
aisstream probe --api-key "<your_api_key>"
```

### Stream to Kafka

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
aisstream stream \
    --api-key "<your_api_key>" \
    --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
aisstream stream \
    --api-key "<your_api_key>" \
    --kafka-bootstrap-servers "<bootstrap_servers>" \
    --kafka-topic "<topic_name>" \
    --sasl-username "<username>" \
    --sasl-password "<password>"
```

### Command-Line Arguments (stream)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `--api-key` | `AISSTREAM_API_KEY` | AISstream.io API key (required) |
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `--bounding-boxes` | `AISSTREAM_BOUNDING_BOXES` | Bounding boxes as `lat1,lon1,lat2,lon2;...` (default: global) |
| `--message-types` | `AISSTREAM_MESSAGE_TYPES` | Comma-separated message type names (default: all) |
| `--mmsi-filter` | `AISSTREAM_FILTER_MMSI` | Comma-separated MMSIs to include (default: all) |
| `--flush-interval` | `AISSTREAM_FLUSH_INTERVAL` | Flush Kafka every N events (default: 1000) |

### Examples

#### Stream European Waters Only

```bash
aisstream stream \
    --api-key "<key>" \
    -c "<conn_string>" \
    --bounding-boxes "35,-15,72,45"
```

#### Track Specific Vessels

```bash
aisstream stream \
    --api-key "<key>" \
    -c "<conn_string>" \
    --mmsi-filter "311000255,258028380"
```

#### Position Reports Only

```bash
aisstream stream \
    --api-key "<key>" \
    -c "<conn_string>" \
    --message-types "PositionReport,StandardClassBPositionReport,ExtendedClassBPositionReport"
```

## AIS Message Types

### Vessel Position & Movement

| Type Name | AIS Type | Description |
|-----------|----------|-------------|
| `PositionReport` | 1, 2, 3 | Class A position reports (SOLAS vessels) |
| `StandardClassBPositionReport` | 18 | Class B CS position reports (smaller vessels) |
| `ExtendedClassBPositionReport` | 19 | Extended Class B position reports |
| `LongRangeAisBroadcastMessage` | 27 | Long-range AIS broadcast |
| `StandardSearchAndRescueAircraftReport` | 9 | SAR aircraft position |

### Vessel Identity & Static Data

| Type Name | AIS Type | Description |
|-----------|----------|-------------|
| `ShipStaticData` | 5 | Ship name, IMO, callsign, dimensions, destination |
| `StaticDataReport` | 24 | Class B static data (name, callsign, dimensions) |

### Infrastructure & Safety

| Type Name | AIS Type | Description |
|-----------|----------|-------------|
| `BaseStationReport` | 4 | Base station position and UTC time |
| `AidsToNavigationReport` | 21 | Buoys, lighthouses, navigational aids |
| `SafetyBroadcastMessage` | 14 | Safety-related text broadcasts |
| `AddressedSafetyMessage` | 12 | Addressed safety messages |

### Binary & Data Messages

| Type Name | AIS Type | Description |
|-----------|----------|-------------|
| `AddressedBinaryMessage` | 6 | Addressed binary data |
| `BinaryBroadcastMessage` | 8 | Binary broadcast data |
| `SingleSlotBinaryMessage` | 25 | Single-slot binary |
| `MultiSlotBinaryMessage` | 26 | Multi-slot binary |
| `GnssBroadcastBinaryMessage` | 17 | GNSS corrections broadcast |

### Protocol & Control

| Type Name | AIS Type | Description |
|-----------|----------|-------------|
| `BinaryAcknowledge` | 7, 13 | Binary message acknowledgement |
| `Interrogation` | 15 | AIS interrogation |
| `AssignedModeCommand` | 16 | Assigned mode command |
| `DataLinkManagementMessage` | 20 | Data link management |
| `ChannelManagement` | 22 | Channel management |
| `GroupAssignmentCommand` | 23 | Group assignment |
| `CoordinatedUTCInquiry` | 10 | UTC inquiry |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-eventhub.json)
