# Digitraffic Marine Bridge Usage Guide

## Overview

**Digitraffic Marine Bridge** connects to Finland's
[Digitraffic](https://www.digitraffic.fi/) MQTT stream for real-time AIS
vessel tracking and also polls Digitraffic's Port Call REST APIs for vessel
visit and companion reference data. Both paths are forwarded to Kafka as
[CloudEvents](https://cloudevents.io/) in JSON format.

The bridge has two delivery modes:

- `stream` keeps an open MQTT WebSocket connection to `meri.digitraffic.fi`
  and continuously forwards vessel position and metadata messages.
- `port-calls` polls the Portnet-backed REST APIs and emits vessel details,
  port locations, and port call visit updates.

## Key Features

- **Real-time MQTT stream**: ~35 messages/second from Digitraffic's
  government-operated AIS infrastructure
- **Port Call polling**: Digitraffic REST polling for vessel visits and
  companion reference data
- **No authentication required**: Open data under Creative Commons 4.0 BY
- **Baltic Sea coverage**: Finnish waters, Sweden, Estonia, Latvia,
  Lithuania, Denmark, Germany, Poland, and transit traffic
- **Five event types**: AIS vessel positions, AIS vessel metadata, port calls,
  vessel details, and port locations
- **MMSI filtering**: Subscribe to specific vessels via MQTT topic filters
- **Auto-reconnect**: Exponential backoff on connection failures
- **Reference data ahead of visits**: The `port-calls` command emits vessel
  details and port locations before port call visit events in each cycle
- **Kafka integration**: SASL PLAIN authentication for Event Hubs / Fabric
  Event Streams

## Event Families

The bridge emits these CloudEvents families. Full field documentation lives in
[EVENTS.md](EVENTS.md).

| Event Type | Command | Identity |
|------------|---------|----------|
| `fi.digitraffic.marine.ais.VesselLocation` | `stream` | `{mmsi}` |
| `fi.digitraffic.marine.ais.VesselMetadata` | `stream` | `{mmsi}` |
| `fi.digitraffic.marine.portcall.PortCall` | `port-calls` | `{port_call_id}` |
| `fi.digitraffic.marine.portcall.VesselDetails` | `port-calls` | `{vessel_id}` |
| `fi.digitraffic.marine.portcall.PortLocation` | `port-calls` | `{locode}` |

## Data Source

[Digitraffic Marine](https://www.digitraffic.fi/en/marine-traffic/) is
operated by [Fintraffic](https://www.fintraffic.fi) — Finland's
state-owned transport infrastructure company. The AIS data is collected
from VTS Finland's shore-based AIS receivers.

- **MQTT endpoint**: `wss://meri.digitraffic.fi:443/mqtt`
- **Protocol**: MQTT over WebSocket with TLS
- **Authentication**: None
- **Coverage**: Finnish territorial waters and Baltic Sea
- **License**: Creative Commons 4.0 BY
- **Throughput**: ~35 position updates/second, ~2,100/minute

**Attribution (required by license):**

> Source: Fintraffic / digitraffic.fi, license CC 4.0 BY

## Installation

Requires Python 3.10 or later.

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/digitraffic-maritime
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md)
instructions.

## How to Use

After installation, the tool can be run using the `digitraffic-maritime`
command.

The events sent to Kafka are formatted as CloudEvents, documented in
[EVENTS.md](EVENTS.md).

### Probe the Live Stream

Test connectivity and see live vessel data:

```bash
digitraffic-maritime probe
```

Probe only vessel positions (no metadata):

```bash
digitraffic-maritime probe --subscribe location
```

Track a specific vessel:

```bash
digitraffic-maritime probe --mmsi-filter 230629000
```

### Stream to Kafka

#### Using a Connection String (Event Hubs / Fabric Event Streams)

```bash
digitraffic-maritime stream \
    --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
digitraffic-maritime stream \
    --kafka-bootstrap-servers "<bootstrap_servers>" \
    --kafka-topic "<topic_name>" \
    --sasl-username "<username>" \
    --sasl-password "<password>"
```

### Command-Line Arguments (stream)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `--subscribe` | `DIGITRAFFIC_SUBSCRIBE` | Comma-separated: `location,metadata` (default: both) |
| `--mmsi-filter` | `DIGITRAFFIC_FILTER_MMSI` | Comma-separated MMSIs to include (default: all) |
| `--flush-interval` | `DIGITRAFFIC_FLUSH_INTERVAL` | Flush Kafka every N events (default: 1000) |

### Examples

#### Stream Position Updates Only

```bash
digitraffic-maritime stream \
    -c "<conn_string>" \
    --subscribe location
```

#### Track Specific Vessels

```bash
digitraffic-maritime stream \
    -c "<conn_string>" \
    --mmsi-filter "230629000,219598000"
```

### Poll Port Calls and Reference Data

Poll the Portnet-backed REST APIs and emit vessel details, port locations, and
port calls to Kafka:

```bash
digitraffic-maritime port-calls \
  -c "<conn_string>"
```

### Command-Line Arguments (port-calls)

| Argument | Env Var | Description |
|----------|---------|-------------|
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `--poll-interval` | `DIGITRAFFIC_PORTCALL_POLL_INTERVAL` | Port call polling interval in seconds |
| `--state-file` | `DIGITRAFFIC_PORTCALL_STATE_FILE` | JSON file used to persist last-seen reference and visit timestamps |

## MQTT Topics

The bridge subscribes to Digitraffic's MQTT topics:

| Topic Pattern | Description |
|--------------|-------------|
| `vessels-v2/+/location` | All vessel position updates |
| `vessels-v2/+/metadata` | All vessel metadata updates |
| `vessels-v2/<mmsi>/location` | Single vessel positions (when MMSI filter active) |
| `vessels-v2/<mmsi>/metadata` | Single vessel metadata (when MMSI filter active) |

The MMSI is extracted from the MQTT topic path and used as the Kafka
partition key.

## Coverage Area

The Digitraffic Marine AIS system covers the Baltic Sea region. Vessels
observed include those registered in:

- 🇫🇮 Finland, 🇸🇪 Sweden, 🇪🇪 Estonia, 🇱🇻 Latvia, 🇱🇹 Lithuania
- 🇩🇰 Denmark, 🇩🇪 Germany, 🇵🇱 Poland, 🇷🇺 Russia (Baltic ports)
- International vessels transiting the Baltic

This complements the [Kystverket AIS bridge](../kystverket-ais/) which
covers Norwegian waters. Between the two, the entire Nordic/Baltic
maritime region is covered.
