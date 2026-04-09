# DWD Pollenflug (German Pollen Forecast) Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the DWD Pollenflug (German pollen forecast) API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches daily pollen forecasts from the Deutscher Wetterdienst (DWD) for 27 German regions and forwards them to the configured Kafka endpoints.

## DWD Pollenflug API

The Deutscher Wetterdienst (DWD) publishes a daily pollen forecast index for Germany via the open data endpoint at `https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json`. The forecast covers eight pollen types (Hazel, Alder, Birch, Ash, Grasses, Rye, Mugwort, Ragweed) across 27 forecast regions. Intensity values range from 0 (none) to 3 (high) with intermediate half-step values (0-1, 1-2, 2-3). Forecasts are updated daily on weekdays around 11:00 CET.

## Functionality

The bridge polls the DWD Pollenflug API and writes pollen forecasts to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen forecast timestamps are tracked in a state file to prevent duplicate emission.

At startup, the bridge emits Region reference data for all 27 forecast areas before entering the polling loop.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-dwd-pollenflug:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-dwd-pollenflug:latest
```

## Using the Container Image

The container starts the bridge, polling the DWD API and writing pollen forecasts to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e CONNECTION_STRING="BootstrapServer=mybroker:9092;EntityPath=dwd-pollenflug" \
    -e KAFKA_ENABLE_TLS=false \
    ghcr.io/clemensv/real-time-sources-dwd-pollenflug:latest
```

### With Azure Event Hubs

```shell
$ docker run --rm \
    -e CONNECTION_STRING="Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=<key>;EntityPath=dwd-pollenflug" \
    ghcr.io/clemensv/real-time-sources-dwd-pollenflug:latest
```

### With Microsoft Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING="<Fabric Event Stream connection string>" \
    ghcr.io/clemensv/real-time-sources-dwd-pollenflug:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka/Event Hubs/Fabric connection string |
| `KAFKA_ENABLE_TLS` | No | Set to `false` to disable TLS (default: `true`) |
| `DWD_POLLENFLUG_LAST_POLLED_FILE` | No | Path to state file (default: `/mnt/fileshare/dwd_pollenflug_last_polled.json`) |

## Azure Container Instance Deployment

```shell
$ az container create \
    --resource-group myResourceGroup \
    --name dwd-pollenflug-bridge \
    --image ghcr.io/clemensv/real-time-sources-dwd-pollenflug:latest \
    --environment-variables \
        CONNECTION_STRING="<connection-string>" \
    --restart-policy Always
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template-with-eventhub.json)
