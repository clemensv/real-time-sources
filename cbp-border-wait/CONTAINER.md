# US CBP Border Wait Times Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the US Customs and Border Protection (CBP) Border Wait Time API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches wait times at US land border crossings with Canada and Mexico and forwards them to the configured Kafka endpoints.

## CBP Border Wait Time API

The US CBP publishes real-time wait times at approximately 81 land border ports of entry along the US-Canada and US-Mexico borders. Data includes wait times for passenger vehicles, pedestrians, and commercial vehicles, broken down by lane type (standard, SENTRI/NEXUS, Ready Lane, FAST). Data is updated approximately every hour.

- **API**: `https://bwt.cbp.gov/api/bwtnew`
- **Format**: JSON
- **Auth**: None (US Government public domain)
- **Update Frequency**: Approximately hourly

## Functionality

The bridge polls the CBP Border Wait Time API and writes wait time updates to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen wait time timestamps per port are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-cbp-border-wait:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-cbp-border-wait:latest
```

## Using the Container Image

The container starts the bridge, polling the CBP API and writing wait times to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-cbp-border-wait:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-cbp-border-wait:latest
```

### Preserving State Between Restarts

To preserve the last seen timestamps between restarts and avoid reprocessing:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e STATE_FILE='/mnt/fileshare/cbp_state.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-cbp-border-wait:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic to send messages to.

### `SASL_USERNAME`

The username for SASL PLAIN authentication with the Kafka broker.

### `SASL_PASSWORD`

The password for SASL PLAIN authentication with the Kafka broker.

### `POLLING_INTERVAL`

How often to poll the CBP API, in seconds. Defaults to `3600` (one hour).

### `STATE_FILE`

The file path for storing last seen timestamps per port for deduplication.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-with-eventhub.json)
