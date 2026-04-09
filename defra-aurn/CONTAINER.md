# Defra AURN Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges the UK Defra AURN SOS Timeseries API to Kafka
compatible endpoints. It emits CloudEvents in structured JSON mode for station
metadata, timeseries metadata, and hourly observations.

> The upstream API is public and does not require authentication.

## Functionality

At startup the container emits:

- `uk.gov.defra.aurn.Station` reference events for all monitoring stations
- `uk.gov.defra.aurn.Timeseries` reference events for all station × pollutant
  combinations

It then enters a polling loop and emits `uk.gov.defra.aurn.Observation` for new
values returned by the `getData` endpoint on each timeseries. Fresh containers
use a six-hour bootstrap lookback so the first run can still emit telemetry when
the public feed is a few hours behind, and later cycles return to the normal
two-hour polling window.

## Pulling the image

```powershell
docker pull ghcr.io/clemensv/real-time-sources-defra-aurn:latest
```

## Running with Azure Event Hubs or Fabric Event Streams

```powershell
docker run --rm `
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=defra-aurn" `
  ghcr.io/clemensv/real-time-sources-defra-aurn:latest
```

## Running with Kafka

```powershell
docker run --rm `
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=defra-aurn" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-defra-aurn:latest
```

## Preserving de-duplication state

Mount a volume and point `STATE_FILE` at it:

```powershell
docker run --rm `
  -v ${PWD}\state:C:\state `
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=defra-aurn" `
  -e KAFKA_ENABLE_TLS=false `
  -e STATE_FILE="C:\state\defra_aurn_state.json" `
  ghcr.io/clemensv/real-time-sources-defra-aurn:latest
```

## Polling interval

The default polling interval is 3600 seconds, matching the upstream hourly
update pattern. You can reduce or increase it:

```powershell
docker run --rm `
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=defra-aurn" `
  -e KAFKA_ENABLE_TLS=false `
  -e POLLING_INTERVAL=1800 `
  ghcr.io/clemensv/real-time-sources-defra-aurn:latest
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | No | Event Hubs connection string or `BootstrapServer=...;EntityPath=...` |
| `KAFKA_BOOTSTRAP_SERVERS` | No | Kafka bootstrap servers if not using `CONNECTION_STRING` |
| `KAFKA_TOPIC` | No | Kafka topic, default `defra-aurn` |
| `SASL_USERNAME` | No | SASL username |
| `SASL_PASSWORD` | No | SASL password |
| `POLLING_INTERVAL` | No | Polling interval in seconds, default `3600` |
| `STATE_FILE` | No | Path to the state file, default `~/.defra_aurn_state.json` |
| `KAFKA_ENABLE_TLS` | No | Use TLS for Kafka connectivity, default `true` |

## Data contract

The event contract is defined in [EVENTS.md](EVENTS.md). Keys and CloudEvents
subjects are stable identifiers:

- Station events use `{station_id}`
- Timeseries and observation events use `{timeseries_id}`

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template-with-eventhub.json)
