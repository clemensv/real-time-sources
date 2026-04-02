# Hub'Eau Hydrométrie Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the French Hub'Eau Hydrométrie API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge polls real-time water level and flow data from approximately 6,300 hydrometric stations across France and forwards them to the configured Kafka endpoint.

## Hub'Eau Hydrométrie API

Hub'Eau is an open data platform from the French Ministry for Ecological Transition. The Hydrométrie API provides free, unauthenticated access to real-time river discharge (flow) and water level data from the French national hydrometric network, updated every 10–15 minutes.

## Functionality

The bridge fetches hydrometric data from the Hub'Eau API and writes it to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Station reference data is emitted at startup, followed by continuous hydrometric observations. Previously seen readings are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-hubeau-hydrometrie:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-hubeau-hydrometrie:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-hubeau-hydrometrie:latest
```

### Preserving State Between Restarts

Mount a volume and set the `STATE_FILE` environment variable to persist deduplication state:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e STATE_FILE='/mnt/fileshare/hubeau_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-hubeau-hydrometrie:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds. Default: `600` (10 minutes).

### `STATE_FILE`

Path to the deduplication state file.

## Azure Deployment

Deploy using the provided ARM template:

```shell
$ az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters connectionStringSecret='<connection-string>'
```

