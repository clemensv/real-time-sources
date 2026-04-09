# Ireland OPW waterlevel.ie Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Ireland OPW waterlevel.ie
GeoJSON API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The
bridge reads real-time water level, temperature, and voltage data from Irish
hydrometric stations and writes it to a Kafka topic.

## Ireland OPW waterlevel.ie API

The Office of Public Works (OPW) in Ireland operates a network of hydrometric
stations across rivers, lakes, and canals. The waterlevel.ie service provides
real-time GeoJSON data at `https://waterlevel.ie/geojson/latest/` updated every
15 minutes. Data is published under CC BY 4.0.

## Functionality

The bridge polls the waterlevel.ie GeoJSON endpoint and writes data to a Kafka
topic as structured JSON [CloudEvents](https://cloudevents.io/) documented in
[EVENTS.md](EVENTS.md). Station reference data is emitted at startup and
refreshed every 6 hours. Sensor readings are deduplicated by station, sensor,
and timestamp.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-ireland-opw-waterlevel:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-ireland-opw-waterlevel:latest
```

## Using the Container Image

The container starts the bridge, reading data from the OPW waterlevel.ie API and
writing it to a Kafka topic, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-ireland-opw-waterlevel:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-ireland-opw-waterlevel:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to establish a connection to
Azure Event Hubs or Fabric Event Streams. This replaces the need for
`KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds (default: 300).

### `STATE_FILE`

Path to the JSON state file for deduplication (default: `~/.ireland_opw_waterlevel_state.json`).
