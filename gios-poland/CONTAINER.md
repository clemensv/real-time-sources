# GIOŚ Poland Air Quality Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Polish Chief Inspectorate of Environmental Protection (GIOŚ) air quality monitoring network and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches station metadata, sensor reference data, hourly measurements (PM10, PM2.5, SO₂, NO₂, O₃, CO, benzene), and the Polish Air Quality Index from ~250 stations nationwide.

## GIOŚ API

The GIOŚ air quality API provides publicly available air quality data from Poland's national monitoring network. Approximately 250 stations report hourly measurements of key pollutants. Data is updated hourly.

## Functionality

The bridge polls the GIOŚ REST API at `https://api.gios.gov.pl/pjp-api/v1/rest/` and writes events to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen measurement timestamps per sensor are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-gios-poland:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-gios-poland:latest
```

## Using the Container Image

The container starts the bridge, polling the GIOŚ API and writing events to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-gios-poland:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-gios-poland:latest
```

### Preserving State Between Restarts

To preserve the last seen timestamps between restarts and avoid reprocessing measurements, mount a volume and set the `GIOS_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e GIOS_LAST_POLLED_FILE='/mnt/fileshare/gios_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-gios-poland:latest
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

### `GIOS_LAST_POLLED_FILE`

The file path for storing last seen timestamps per sensor for deduplication. Defaults to `/mnt/fileshare/gios_last_polled.json` inside the container.
