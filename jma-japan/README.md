# JMA Japan Weather Bulletins Poller

## Overview

**JMA Japan Weather Bulletins Poller** polls the Japan Meteorological Agency
(JMA) Atom XML feeds for weather bulletins—forecasts, warnings, advisories, and
risk notifications—and sends them to a Kafka topic as CloudEvents. The tool
tracks previously seen bulletin IDs to avoid sending duplicates.

## Key Features

- **Dual Atom Feed Polling**: Fetches weather bulletins from both the *regular*
  feed (`regular.xml` — scheduled forecasts) and the *extra* feed
  (`extra.xml` — warnings and advisories).
- **Deduplication**: Tracks seen bulletin IDs in a state file to avoid
  reprocessing.
- **Japanese Text Support**: Handles Japanese (UTF-8) titles, author names, and
  content text natively.
- **Kafka Integration**: Sends bulletins to a Kafka topic using SASL PLAIN
  authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in
  [EVENTS.md](EVENTS.md).

## Data Sources

| Feed | URL | Description |
|------|-----|-------------|
| Regular | `https://www.data.jma.go.jp/developer/xml/feed/regular.xml` | Scheduled forecasts, risk notifications |
| Extra | `https://www.data.jma.go.jp/developer/xml/feed/extra.xml` | Warnings, advisories, typhoon bulletins |

Both feeds are Atom XML documents updated every minute by JMA.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can
download Python from [here](https://www.python.org/downloads/) or from the
Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=jma-japan
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/jma-japan
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m jma_japan`. It supports
several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where seen bulletin IDs are stored.
  Defaults to `~/.jma_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream
  connection string (overrides other Kafka parameters).

### Example Usage

#### Using a Connection String

```bash
python -m jma_japan --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m jma_japan --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream
  connection string.
- `JMA_LAST_POLLED_FILE`: File to store seen bulletin IDs for deduplication.

## Weather Bulletin Properties

Each weather bulletin includes these properties:

| Property | Description |
|----------|-------------|
| `bulletin_id` | Stable hash-based ID derived from the Atom entry ID |
| `title` | Bulletin title in Japanese (e.g., "気象特別警報・警報・注意報") |
| `author` | Issuing authority name (e.g., "気象庁", "松江地方気象台") |
| `updated` | When the bulletin was last updated (ISO 8601) |
| `link` | URL to the full XML document |
| `content` | Brief text summary in Japanese |
| `feed_type` | Feed origin: "regular" or "extra" |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template-with-eventhub.json)
