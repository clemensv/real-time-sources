# King County Marine Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container polls current King County marine buoy and mooring raw-data datasets and emits station reference events plus normalized water-quality readings as CloudEvents JSON.

## Upstream

- **Publisher:** King County Water and Land Resources Division
- **Platform:** Socrata datasets on `data.kingcounty.gov`
- **Cadence:** 15-minute telemetry for current buoy/mooring datasets
- **Auth:** None
- **License:** Public Domain

## Behavior

At startup the bridge discovers active raw buoy/mooring datasets from the King County Socrata catalog, fetches dataset metadata, and emits station reference events. It then polls the current datasets and emits normalized water-quality readings keyed by `station_id`.

Historical-only raw-output datasets and periodic non-buoy monitoring programs are intentionally excluded from this source.

## Running the Container

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=king-county-marine" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-king-county-marine:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=king-county-marine" \
  ghcr.io/clemensv/real-time-sources-king-county-marine:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka/Event Hubs/Fabric connection string |
| `KAFKA_ENABLE_TLS` | No | Set `false` for plain Kafka in local and Docker E2E runs |
| `KING_COUNTY_MARINE_STATE_FILE` | No | Path to dedupe state; default `/mnt/fileshare/king_county_marine_state.json` |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-with-eventhub.json)
