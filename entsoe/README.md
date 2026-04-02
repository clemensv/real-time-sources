# ENTSO-E Transparency Platform Bridge

## Overview

The **ENTSO-E Transparency Platform Bridge** polls the [ENTSO-E Transparency Platform REST API](https://transparency.entsoe.eu/) for European electricity market data and emits it as [CloudEvents](https://cloudevents.io/) to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

The bridge covers eleven data categories:

| Document Type | Code | Description |
|---------------|------|-------------|
| Actual Generation per Type | A75 | Real-time power generation broken down by production type (wind, solar, nuclear, etc.) |
| Day-Ahead Prices | A44 | Day-ahead electricity market prices per bidding zone |
| Actual Total Load | A65 | Actual total electricity consumption per bidding zone |
| Wind & Solar Forecast | A69 | Day-ahead forecast for wind and solar generation per type |
| Load Forecast Margin | A70 | Day-ahead forecast margin (available capacity minus forecast load) |
| Generation Forecast | A71 | Day-ahead total generation forecast |
| Reservoir Filling Information | A72 | Hydro reservoir filling levels |
| Actual Generation (Aggregate) | A73 | Actual total generation (aggregated, no PSR breakdown) |
| Wind & Solar Generation | A74 | Actual wind and solar generation per type |
| Installed Generation Capacity per Type | A68 | Year-ahead installed generation capacity by production type |
| Cross-Border Physical Flows | A11 | Physical electricity flows between bidding zones |

Data is polled for configurable European bidding zones (default: DE-AT-LU, France, Netherlands, Spain, Germany) and emitted as delta-only events — only new data points since the last checkpoint are forwarded.

## Key Features

- **11 document types**: Generation, prices, load, forecasts, capacity, reservoir, cross-border flows
- **Cross-border flows**: Polls configurable domain pairs for physical electricity flows (A11)
- **Delta-only emission**: Tracks watermarks per (document_type, domain) to avoid duplicates
- **Persistent state**: Checkpoint state file survives restarts via mounted volume
- **IEC 62325 XML parsing**: Handles both `GL_MarketDocument` and `Publication_MarketDocument` response formats
- **Configurable polling**: Adjustable polling interval, lookback window, domains, and document types

## Installation

The tool requires Python 3.10 or later.

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=entsoe
```

Or from a local clone:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/entsoe
pip install .
```

For a container deployment, see [CONTAINER.md](CONTAINER.md).

## Prerequisites

You need an ENTSO-E Transparency Platform API security token. Register at [https://transparency.entsoe.eu/](https://transparency.entsoe.eu/) and request an API token via your account settings.

## Usage

The events sent to Kafka are formatted as CloudEvents, documented in [EVENTS.md](EVENTS.md).

### Command-Line Arguments

| Argument | Environment Variable | Description | Default |
|----------|---------------------|-------------|---------|
| `--security-token` | `ENTSOE_SECURITY_TOKEN` | ENTSO-E API security token | (required) |
| `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string | — |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | — |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic | — |
| `--sasl-username` | `SASL_USERNAME` | SASL username | — |
| `--sasl-password` | `SASL_PASSWORD` | SASL password | — |
| `--domains` | `ENTSOE_DOMAINS` | Comma-separated EIC domain codes | DE-AT-LU, FR, NL, ES, DE |
| `--document-types` | `ENTSOE_DOCUMENT_TYPES` | Comma-separated document type codes | A75, A44, A65, A69, A70, A71, A72, A73, A74, A68, A11 |
| `--cross-border-pairs` | `ENTSOE_CROSS_BORDER_PAIRS` | Semicolon-separated `in>out` domain pairs for A11 | 20 major European interconnections |
| `--polling-interval` | `POLLING_INTERVAL` | Seconds between poll cycles | 900 |
| `--lookback-hours` | `ENTSOE_LOOKBACK_HOURS` | Initial lookback window in hours | 24 |
| `--state-file` | `STATE_FILE` | Path to the delta state file | ~/.entsoe_state.json |

### Examples

#### Using a connection string (Event Hubs / Fabric Event Streams)

```bash
entsoe --security-token "<your-entsoe-token>" \
       --connection-string "<your-connection-string>"
```

#### Using Kafka parameters directly

```bash
entsoe --security-token "<your-entsoe-token>" \
       --kafka-bootstrap-servers "<bootstrap-servers>" \
       --kafka-topic "<topic>" \
       --sasl-username "<username>" \
       --sasl-password "<password>"
```

#### Using environment variables

```bash
export ENTSOE_SECURITY_TOKEN="<your-entsoe-token>"
export CONNECTION_STRING="<your-connection-string>"
entsoe
```

## Database Schemas

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Default Bidding Zones

| EIC Code | Region |
|----------|--------|
| `10YDE-AT-LU---Q` | Germany/Austria/Luxembourg |
| `10YFR-RTE------C` | France |
| `10YNL----------L` | Netherlands |
| `10YES-REE------0` | Spain |
| `10Y1001A1001A83F` | Germany |

## Additional Information

- **Source Code**: [GitHub Repository](https://github.com/clemensv/real-time-sources/tree/main/entsoe)
- **ENTSO-E API Documentation**: [Transparency Platform RESTful API Guide](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- **License**: MIT
