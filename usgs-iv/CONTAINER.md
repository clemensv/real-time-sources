# USGS Water Services - Instantaneous Values Service bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [USGS Water Services](https://waterservices.usgs.gov/) Instantaneous Values
Service and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge
fetches entries from specified feeds and forwards them to the configured Kafka
endpoints.

## Functionality

The bridge retrieves data from the USGS Instantaneous Values Service and writes the entries to a
Kafka topic as [CloudEvents](https://cloudevents.io/) in a JSON format, which is
documented in [EVENTS.md](EVENTS.md). You can specify multiple feed URLs by
providing them in the configuration.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-usgs-iv:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-usgs-iv:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading data from the
USGS services and writing it to Kafka, Azure Event Hubs, or
Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-usgs-iv:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, Azure CLI, or the "custom endpoint" of
a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-usgs-iv:latest
```

### Preserving State Between Restarts

To preserve the state between restarts and avoid reprocessing feed entries,
mount a volume to the container and set the `USGS_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e USGS_LAST_POLLED_FILE='/mnt/state/usgs_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-usgs-iv:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`,
`SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with
TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. Ensure your Kafka brokers support SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `USGS_LAST_POLLED_FILE`

The file path where the bridge stores the state of processed entries. This helps
in resuming data fetching without duplication after restarts. Default is
`/mnt/state/usgs_last_polled.json`.

## Deploying into Azure Container Instances

You can deploy the USGS Instananeous Values Service bridge as a container directly to Azure Container
Instances providing the information explained above. Just click the button below and go.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs_iv%2Fazure-template.json)
