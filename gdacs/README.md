# GDACS — Global Disaster Alert and Coordination System

## Overview

**GDACS** is a bridge that polls the [Global Disaster Alert and Coordination
System](https://www.gdacs.org) RSS feed to fetch real-time disaster alert data.
The bridge converts alerts into [CloudEvents](https://cloudevents.io/) structured
JSON format and publishes them to Kafka, Azure Event Hubs, or Microsoft Fabric
Event Streams.

GDACS aggregates disaster information from multiple scientific sources worldwide,
covering six event types: earthquakes (EQ), tropical cyclones (TC), floods (FL),
volcanic eruptions (VO), forest fires (FF), and droughts (DR). The RSS feed
typically contains ~220 items and is updated within minutes of event detection.
No API key is required.

## Key Features

- **Multi-hazard coverage**: Earthquakes, tropical cyclones, floods, volcanoes, forest fires, and droughts in a single feed.
- **Episode-level tracking**: State file tracks each event+episode combination by version number — only new or updated episodes are emitted.
- **Three-tier alert levels**: Green (low), Orange (moderate), Red (high humanitarian impact).
- **Kafka integration**: Sends disaster alerts as CloudEvents, supporting Azure Event Hubs and Fabric Event Streams.

## Installation

The tool is written in Python and requires Python 3.10 or later.

### From Source

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/gdacs
pip install .
```

For a containerized deployment, see [CONTAINER.md](CONTAINER.md).

## How to Use

After installation, the bridge can be run with `python -m gdacs`.

### With Azure Event Hubs or Fabric Event Streams

```bash
python -m gdacs --connection-string '<connection-string>'
```

### With a Kafka Broker

```bash
python -m gdacs \
    --bootstrap-servers '<kafka-bootstrap-servers>' \
    --topic 'gdacs' \
    --sasl-username '<username>' \
    --sasl-password '<password>'
```

### One-shot Mode

Poll once and exit (useful for testing or scheduled runs):

```bash
python -m gdacs --connection-string '<connection-string>' --once
```

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` or `GDACS_CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated list of Kafka bootstrap servers |
| `KAFKA_TOPIC` | Kafka topic name |
| `SASL_USERNAME` | SASL PLAIN username |
| `SASL_PASSWORD` | SASL PLAIN password |
| `GDACS_STATE_FILE` | Path to state file for tracking seen events (default: `~/.gdacs_state.json`) |
| `LOG_LEVEL` | Logging level (default: `INFO`) |
| `KAFKA_ENABLE_TLS` | Enable TLS for Kafka (default: `true`) |

## CLI Arguments

| Argument | Description |
|---|---|
| `--connection-string` | Azure Event Hubs or Fabric Event Stream connection string |
| `--bootstrap-servers` | Comma-separated Kafka bootstrap servers |
| `--topic` | Kafka topic |
| `--sasl-username` | SASL PLAIN username |
| `--sasl-password` | SASL PLAIN password |
| `--state-file` | Path to persist seen-event state |
| `--poll-interval` | Polling interval in seconds (default: 300) |
| `--once` | Poll once and exit |
| `--log-level` | Logging level |

## Events

The event format is documented in [EVENTS.md](EVENTS.md).

## Testing

Run the unit tests:

```bash
cd gdacs
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

## Data Source

- **Provider**: [GDACS](https://www.gdacs.org) — a joint UN/European Commission initiative
- **Feed**: `https://www.gdacs.org/xml/rss.xml`
- **Update frequency**: Within minutes of event detection
- **Authentication**: None required
- **License**: Public data for humanitarian use
