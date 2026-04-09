# GraceDB Gravitational Wave Candidate Alert bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between
[GraceDB](https://gracedb.ligo.org/) (Gravitational-Wave Candidate Event
Database) and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The
bridge fetches gravitational wave candidate superevents and forwards them to the
configured Kafka endpoints.

## GraceDB

[GraceDB](https://gracedb.ligo.org/) is the public database of the
LIGO/Virgo/KAGRA collaboration that tracks gravitational wave candidate events
(superevents). Each superevent aggregates one or more pipeline detections into a
single candidate and carries false alarm rate, classification, detector
participation, and alert-lifecycle labels.

## Functionality

The bridge polls the GraceDB superevent API at regular intervals and writes
superevent records to a Kafka topic as [CloudEvents](https://cloudevents.io/) in
JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-gracedb:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-gracedb:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading superevent data
from GraceDB and writing it to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-gracedb:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string from Azure Event Hubs or Microsoft Fabric Event
Streams:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-gracedb:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`,
`SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `LOG_LEVEL`

The logging level. Default: `INFO`.

### `GRACEDB_LAST_POLLED_FILE`

The file path where the bridge stores the IDs of previously processed
superevents to avoid duplication after restarts. Default:
`~/.gracedb_last_polled.json`.
