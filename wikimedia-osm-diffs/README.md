# OpenStreetMap Minutely Diffs Bridge

## Overview

**OpenStreetMap Minutely Diffs Bridge** polls the OSM replication feed and
forwards every element change (node, way, relation creates, modifies,
deletes) to Kafka as [CloudEvents](https://cloudevents.io/).

## Data Source

- **State endpoint**: `https://planet.openstreetmap.org/replication/minute/state.txt`
- **Diff files**: `https://planet.openstreetmap.org/replication/minute/NNN/NNN/NNN.osc.gz`
- **Protocol**: HTTP polling with gzip-compressed OsmChange XML
- **Authentication**: None
- **Freshness**: Updated every 60 seconds
- **License**: ODbL 1.0
- **Upstream docs**:
  - <https://wiki.openstreetmap.org/wiki/Planet.osm/diffs>
  - <https://wiki.openstreetmap.org/wiki/OsmChange>

## Key Features

- **Minutely polling**: Checks for new replication sequences every 60 seconds
- **Sequence tracking**: Persists the last processed sequence number to avoid
  re-processing after restarts
- **Gzip decompression**: Downloads and decompresses `.osc.gz` diff files
- **XML parsing**: Parses OsmChange XML for create/modify/delete operations on
  nodes, ways, and relations
- **Kafka integration**: Works with direct Kafka settings or
  Event Hubs / Fabric connection strings
- **Typed contract**: Emits `Org.OpenStreetMap.Diffs.MapChange` and
  `Org.OpenStreetMap.Diffs.ReplicationState` CloudEvents documented in
  [EVENTS.md](EVENTS.md)

## Installation

Requires Python 3.10 or later.

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/wikimedia-osm-diffs
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md)
instructions.

## How to Use

After installation, the tool can be run with `wikimedia-osm-diffs`.

### Probe the Current State

Print the current replication state and a few sample changes:

```bash
wikimedia-osm-diffs probe
```

Limit the output:

```bash
wikimedia-osm-diffs probe --max-events 3
```

### Stream to Kafka

#### Using a Connection String

```bash
wikimedia-osm-diffs feed \
    --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
wikimedia-osm-diffs feed \
    --kafka-bootstrap-servers "<bootstrap_servers>" \
    --kafka-topic "<topic_name>" \
    --sasl-username "<username>" \
    --sasl-password "<password>"
```

### Command-Line Arguments

| Argument | Env Var | Description |
|----------|---------|-------------|
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `--state-file` | `OSM_DIFFS_STATE_FILE` | State file for sequence tracking |
| `--poll-interval` | `OSM_DIFFS_POLL_INTERVAL` | Polling interval in seconds (default: 60) |
| `--max-retry-delay` | `OSM_DIFFS_MAX_RETRY_DELAY` | Maximum retry delay in seconds (default: 120) |
| `--user-agent` | `OSM_DIFFS_USER_AGENT` | HTTP `User-Agent` header |

## Event Model

Two event types are emitted:

1. **`Org.OpenStreetMap.Diffs.ReplicationState`** — one per poll cycle,
   recording the sequence number and timestamp of the latest processed diff.
   Keyed by the constant `replication_state`.

2. **`Org.OpenStreetMap.Diffs.MapChange`** — one per element change (create,
   modify, or delete of a node, way, or relation). Keyed by
   `{element_type}/{element_id}`.

Each minutely diff can contain thousands of changes. The bridge emits them all;
filtering is left to downstream consumers.
