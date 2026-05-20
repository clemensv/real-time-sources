# Seattle Fire 911 Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container polls the City of Seattle's official **Seattle Real Time Fire 911 Calls** dataset and emits incident events to Kafka-compatible endpoints as CloudEvents JSON.

## Upstream

- **Publisher:** City of Seattle
- **Dataset:** Seattle Real Time Fire 911 Calls
- **Dataset page:** https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj
- **API endpoint:** `https://data.seattle.gov/resource/kzjm-xkqj.json`
- **Cadence:** Updated every 5 minutes
- **Auth:** None
- **License:** Public Domain

## Behavior

The bridge polls the live JSON feed, keeps a short overlap window for safety, deduplicates by `incident_number`, and emits one event per dispatch record. The upstream does not expose a separate reference catalog, so this source emits telemetry events only.

## Running the Container

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=seattle-911" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-seattle-911:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=seattle-911" \
  ghcr.io/clemensv/real-time-sources-seattle-911:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka/Event Hubs/Fabric connection string |
| `KAFKA_ENABLE_TLS` | No | Set `false` for plain Kafka in local and Docker E2E runs |
| `SEATTLE_911_LAST_POLLED_FILE` | No | Path to persisted state file; default `/mnt/fileshare/seattle_911_last_polled.json` |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-with-eventhub.json)
