# USGS Geomagnetism Program Bridge

## Overview

**USGS Geomagnetism Program Bridge** polls the USGS Geomagnetism web-service for real-time 1-minute geomagnetic field variation data from 14 US observatories and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen observation timestamps per observatory to avoid sending duplicates.

## Key Features

- **Real-Time Geomagnetic Data**: Fetch 1-minute variation data (H, D, Z, F components) from the USGS Geomagnetism web-service at `https://geomag.usgs.gov/ws/data/`.
- **Observatory Reference Data**: Emit observatory metadata from `https://geomag.usgs.gov/ws/observatories/` as reference events.
- **Deduplication**: Tracks last seen timestamp per observatory in a state file to avoid reprocessing.
- **Kafka Integration**: Send readings to a Kafka topic using SASL PLAIN authentication.
- **CloudEvents**: All events are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).
- **Fabric notebook hosting**: Optionally schedule this feeder as a Microsoft Fabric notebook using [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1); see [`notebook/usgs-geomag-feed.ipynb`](notebook/usgs-geomag-feed.ipynb).

## Observatories

The bridge polls 14 USGS-operated magnetic observatories:

| Code | Name | Location |
|------|------|----------|
| BOU | Boulder | Colorado |
| BRW | Barrow | Alaska |
| BSL | Stennis Space Center | Mississippi |
| CMO | College | Alaska |
| DED | Deadhorse | Alaska |
| FRD | Fredericksburg | Virginia |
| FRN | Fresno | California |
| GUA | Guam | Pacific |
| HON | Honolulu | Hawaii |
| NEW | Newport | Washington |
| SHU | Shumagin | Alaska |
| SIT | Sitka | Alaska |
| SJG | San Juan | Puerto Rico |
| TUC | Tucson | Arizona |

## Installation

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/) or from the Microsoft Store if you are on Windows.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=usgs-geomag
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/usgs-geomag
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using `python -m usgs_geomag`. It supports several arguments for configuring the polling process and sending data to Kafka.

### Command-Line Arguments

- `--last-polled-file`: Path to the file where last seen timestamps per observatory are stored. Defaults to `~/.usgs_geomag_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: The Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string (overrides other Kafka parameters).
- `--observatories`: Comma-separated list of IAGA observatory codes to poll (default: all USGS).

### Example Usage

#### Using a Connection String

```bash
python -m usgs_geomag --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
python -m usgs_geomag --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Connection String Format

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `GEOMAG_LAST_POLLED_FILE`: File to store last seen timestamps per observatory for deduplication.
- `GEOMAG_OBSERVATORIES`: Comma-separated list of IAGA observatory codes to poll.

## Data Source

The USGS Geomagnetism Program operates 14 magnetic observatories across the United States and territories. Each observatory continuously records geomagnetic field variations at 1-minute cadence. The data is freely available through an INTERMAGNET-compatible web-service.

- **Data API**: `https://geomag.usgs.gov/ws/data/`
- **Observatories API**: `https://geomag.usgs.gov/ws/observatories/`
- **Program home page**: `https://www.usgs.gov/programs/geomagnetism`

## License

[MIT](../LICENSE.md)

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-with-eventhub.json)

## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-usgs-geomag-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variants for USGS geomagnetic observatory reference data and one-minute readings. Topics are retained QoS-1 leaves under space-weather/us/usgs/usgs-geomag/{iaga_code}/..., where {iaga_code} in the topic is the lowercased IAGA observatory code; the payload field may carry the canonical upstream code. Producers MUST lowercase {iaga_code} for the topic and consumers MUST treat topic filters as case-sensitive. The info leaf is retained reference metadata with no expiry. The reading leaf is a latched current 1-minute observation with Message Expiry Interval 7200 seconds; if the retained value expires, interpret the empty topic as observatory or bridge silence for at least two hours, not a zero magnetic-field reading. The iaga_code is the join key between retained info and readings.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/usgs_geomag.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `space-weather/us/usgs/usgs-geomag/{iaga_code}/info` | `gov.usgs.geomag.Observatory` | QoS 1, retain=true |
| `space-weather/us/usgs/usgs-geomag/{iaga_code}/reading` | `gov.usgs.geomag.MagneticFieldReading` | QoS 1, retain=true, expiry=7200s |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.
