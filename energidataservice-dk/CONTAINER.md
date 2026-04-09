# Energi Data Service (Energinet) Denmark Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Energi Data Service API (operated by Energinet) for the Danish power system and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches minute-level power system snapshots and hourly spot prices and forwards them to the configured Kafka endpoints.

## Energi Data Service API

Energi Data Service is a free, open data platform operated by Energinet (the Danish TSO). It provides real-time and historical data about the Danish electricity system, including generation by source, CO2 emissions, cross-border exchange flows, balancing market activations, and day-ahead spot prices. Data is updated approximately every minute for system snapshots and hourly for spot prices. No authentication is required.

## Functionality

The bridge polls two datasets:

1. **PowerSystemRightNow** — Minute-by-minute system-wide snapshots including CO2 emission intensity, solar and wind generation, exchange flows across all interconnectors, aFRR/mFRR activation, and grid imbalance.
2. **ElspotPrices** — Day-ahead spot prices in DKK and EUR per bidding zone (DK1 Western Denmark, DK2 Eastern Denmark).

Events are written to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen timestamps are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-energidataservice-dk:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-energidataservice-dk:latest
```

## Using the Container Image

The container starts the bridge, polling the Energi Data Service API and writing events to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-energidataservice-dk:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-energidataservice-dk:latest
```

### Preserving State Between Restarts

To preserve the last seen timestamps between restarts and avoid reprocessing events, mount a volume and set the `EDS_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e EDS_LAST_POLLED_FILE='/mnt/fileshare/eds_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-energidataservice-dk:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic to send messages to.

### `SASL_USERNAME`

The username for SASL PLAIN authentication with the Kafka broker.

### `SASL_PASSWORD`

The password for SASL PLAIN authentication with the Kafka broker.

### `EDS_LAST_POLLED_FILE`

The file path for storing last seen timestamps for deduplication. Defaults to `/mnt/fileshare/eds_last_polled.json` inside the container.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-eventhub.json)
