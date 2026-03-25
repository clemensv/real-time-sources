# IMGW-PIB Hydrological Data Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the IMGW-PIB hydrological data
API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge
reads real-time water level data from the IMGW-PIB public API and writes it to a
Kafka topic.

## IMGW-PIB API

The IMGW-PIB (Instytut Meteorologii i Gospodarki Wodnej – Państwowy Instytut
Badawczy) public data API provides real-time hydrological data for Polish rivers
and waterways. It provides water level, water temperature, and discharge data for
hundreds of stations across Poland.

## Functionality

The bridge fetches hydrological data from the IMGW-PIB API and writes the data
to a Kafka topic as structured JSON [CloudEvents](https://cloudevents.io/) in a
JSON format documented in [EVENTS.md](EVENTS.md).

## Database Schemas and handling

If you want to build a full data pipeline with all events ingested into
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-imgw-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-imgw-hydro:latest
```

## Using the Container Image

The container image defines a single command that starts the bridge. It reads
data from the IMGW-PIB API and writes it to a Kafka topic, Azure Event Hubs, or
Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='imgw-hydro' \
    ghcr.io/clemensv/real-time-sources-imgw-hydro:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-imgw-hydro:latest
```

## Environment Variables

### `CONNECTION_STRING`

The connection string for Azure Event Hubs or Fabric Event Streams custom input
endpoint. The connection string can be obtained from the Azure portal or through
the Azure CLI.

### `KAFKA_BROKER`

The Kafka bootstrap server address. Use this when connecting to a plain Kafka
broker.

### `KAFKA_TOPIC`

The Kafka topic to write events to. Default: `imgw-hydro`.

### `POLLING_INTERVAL`

The polling interval in seconds. Default: `600` (10 minutes).
