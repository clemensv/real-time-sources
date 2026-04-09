# USGS NWIS Water Quality - Continuous Water Quality Sensor Data

## Overview

**usgs-nwis-wq** is a bridge that polls the [USGS Water Services](https://waterservices.usgs.gov/)
Instantaneous Values Service API for continuous water quality sensor readings from over 3,000
monitoring sites across the United States. The bridge focuses specifically on water quality
parameters: dissolved oxygen, pH, water temperature, specific conductance, turbidity, and nitrate.

This is distinct from the [usgs-iv](../usgs-iv/) bridge which covers a broader set of instantaneous
values including streamflow, gage height, precipitation, and meteorological data.

## Key Features

- **Water Quality Monitoring**: Real-time dissolved oxygen, pH, temperature, turbidity, conductance, and nitrate readings.
- **Site Metadata**: Reference data for monitoring sites including location, type, and watershed info.
- **Kafka Integration**: Sends readings as CloudEvents to Kafka, Azure Event Hubs, or Fabric Event Streams.
- **Configurable Scope**: Filter by state, specific sites, or parameter codes.
- **Deduplication**: Tracks last-polled timestamps to avoid duplicate readings.

## Installation

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=usgs-nwis-wq
```

Or from a clone:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/usgs-nwis-wq
pip install .
```

For container deployment, see [CONTAINER.md](CONTAINER.md).

## Usage

### Feed to Kafka

```bash
usgs-nwis-wq feed --connection-string "<your_connection_string>"
```

Or with explicit Kafka settings:

```bash
usgs-nwis-wq feed \
  --kafka-bootstrap-servers "<servers>" \
  --kafka-topic "<topic>" \
  --sasl-username "<username>" \
  --sasl-password "<password>"
```

### Filter by State or Sites

```bash
usgs-nwis-wq feed --connection-string "<cs>" --states "MD,VA,DC"
usgs-nwis-wq feed --connection-string "<cs>" --sites "01646500,01578310"
```

### Environment Variables

- `CONNECTION_STRING`: Event Hubs / Fabric connection string
- `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, `SASL_PASSWORD`
- `USGS_WQ_STATES`: Comma-separated state codes
- `USGS_WQ_SITES`: Comma-separated site numbers
- `USGS_WQ_PARAMETER_CODES`: Comma-separated parameter codes
- `USGS_WQ_LAST_POLLED_FILE`: State persistence file path

## Water Quality Parameters

| Code | Parameter | Unit |
|------|-----------|------|
| 00010 | Water Temperature | °C |
| 00300 | Dissolved Oxygen | mg/L |
| 00400 | pH | standard units |
| 00095 | Specific Conductance | µS/cm @25°C |
| 63680 | Turbidity | FNU |
| 99133 | Nitrate+Nitrite | mg/L as N |
| 00480 | Salinity | PSU |
| 32295 | fDOM | µg/L QSE |

## Events

Events are documented in [EVENTS.md](EVENTS.md).

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template-with-eventhub.json)
