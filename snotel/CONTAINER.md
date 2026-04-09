# USDA NRCS SNOTEL Snow Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the USDA Natural Resources Conservation Service (NRCS) SNOTEL (SNOwpack TELemetry) network and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches hourly snow and weather observations and forwards them to the configured Kafka endpoints.

## SNOTEL API

The SNOTEL network consists of over 900 automated snowpack monitoring sites in the western United States and Alaska, operated by the USDA NRCS. Stations report Snow Water Equivalent, snow depth, precipitation, and air temperature via satellite telemetry on an hourly basis. Data is publicly available through the NRCS Report Generator at `https://wcc.sc.egov.usda.gov/reportGenerator/`. No authentication is required.

## Functionality

The bridge polls the NRCS Report Generator API for each configured station and writes new observations to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen observation timestamps per station are tracked in a state file to prevent duplicates. Station reference data is emitted at startup before telemetry polling begins.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-snotel:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-snotel:latest
```

## Using the Container Image

The container starts the bridge, polling the SNOTEL API and writing observations to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-snotel:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use a connection string:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<key-name>;SharedAccessKey=<key>;EntityPath=<event-hub-name>' \
    ghcr.io/clemensv/real-time-sources-snotel:latest
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONNECTION_STRING` | Yes* | — | Kafka or Event Hubs connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes* | — | Kafka bootstrap servers (alternative to CONNECTION_STRING) |
| `KAFKA_TOPIC` | No | `snotel` | Kafka topic name |
| `SASL_USERNAME` | No | — | SASL username |
| `SASL_PASSWORD` | No | — | SASL password |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `STATE_FILE` | No | `snotel_state.json` | Path to state persistence file |
| `KAFKA_ENABLE_TLS` | No | — | Set to `false` to disable TLS |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` must be provided.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-with-eventhub.json)
