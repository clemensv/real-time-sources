# NOAA SWPC Space Weather Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the NOAA Space Weather Prediction Center (SWPC) API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches space weather alerts, planetary K-index data, and solar wind measurements and forwards them to the configured Kafka endpoints.

## NOAA SWPC API

The NOAA Space Weather Prediction Center provides public JSON API endpoints for accessing real-time space weather data. Data includes space weather alerts, planetary K-index measurements, and solar wind speed and magnetic field summaries. No authentication is required.

## Functionality

The bridge polls multiple SWPC API endpoints and writes new data to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen timestamps are tracked in a state file to prevent duplicates.

Endpoints polled:
- `https://services.swpc.noaa.gov/products/alerts.json` — Space weather alerts
- `https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json` — Planetary K-index
- `https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json` — Solar wind speed
- `https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json` — Solar wind magnetic field

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-noaa-goes:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-noaa-goes:latest
```

## Using the Container Image

The container starts the bridge, polling the SWPC API endpoints and writing data to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-noaa-goes:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-noaa-goes:latest
```

### Preserving State Between Restarts

To preserve last-polled timestamps between restarts and avoid reprocessing data, mount a volume and set the `SWPC_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e SWPC_LAST_POLLED_FILE='/mnt/fileshare/swpc_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-noaa-goes:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic to send messages to.

### `SASL_USERNAME`

The SASL PLAIN username for Kafka authentication.

### `SASL_PASSWORD`

The SASL PLAIN password for Kafka authentication.

### `SWPC_LAST_POLLED_FILE`

The path to the file where last-polled timestamps are stored for deduplication. Defaults to `/mnt/fileshare/swpc_last_polled.json`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-with-eventhub.json)
