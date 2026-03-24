# USGS Earthquake Hazards Program bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [USGS Earthquake Hazards
Program](https://earthquake.usgs.gov/) real-time GeoJSON feeds and Apache Kafka,
Azure Event Hubs, and Fabric Event Streams. The bridge fetches earthquake events
and forwards them to the configured Kafka endpoints.

## Functionality

The bridge polls the USGS Earthquake GeoJSON feeds at regular intervals and
writes earthquake events to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

## Database Schemas and handling

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

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Microsoft Event Hubs or Fabric Event Stream connection string |
| `LOG_LEVEL` | Logging level (default: INFO) |
| `USGS_EQ_LAST_POLLED_FILE` | Path to the file storing the last polled event IDs |
