# USGS Earthquake Hazards Program bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [USGS Earthquake Hazards
Program](https://earthquake.usgs.gov/) real-time GeoJSON feeds and Apache Kafka,
Azure Event Hubs, and Fabric Event Streams. The bridge fetches earthquake events
and forwards them to the configured Kafka endpoints.

## USGS Earthquake Hazards Program

The [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/) provides
real-time earthquake data via GeoJSON feeds. The feeds include data on
earthquakes worldwide for the past hour, day, week, and month, updated every
minute. The data includes location, magnitude, depth, felt reports, and
alert levels.

## Functionality

The bridge polls the USGS Earthquake GeoJSON feeds at regular intervals and
writes earthquake events to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading earthquake data
from the USGS feeds and writing it to Kafka, Azure Event Hubs, or Fabric Event
Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string from Azure Event Hubs or Microsoft Fabric Event
Streams:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

### Deploy to Azure

You can deploy the container to Azure Container Instances using the provided ARM
template:

[![Deploy to
Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template.json)

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

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `LOG_LEVEL`

The logging level. Default: `INFO`.

### `USGS_EQ_LAST_POLLED_FILE`

The file path where the bridge stores the IDs of previously processed events to
avoid duplication after restarts. Default:
`~/.usgs_earthquakes_last_polled.json`.
