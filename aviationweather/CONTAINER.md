# AviationWeather.gov Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the NOAA AviationWeather.gov API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge polls aviation weather data (METAR observations, SIGMET advisories, and station metadata) and forwards it to the configured Kafka endpoints.

## AviationWeather.gov API

The Aviation Weather Center (AWC), operated by NOAA's National Weather Service, provides publicly available aviation weather data. The API delivers METAR surface observations from thousands of global airports, TAF forecasts, and SIGMET advisories covering hazardous weather. Data updates approximately every minute for METARs and SIGMETs.

## Functionality

The bridge polls the AviationWeather.gov JSON API for METAR observations and SIGMET advisories and writes them to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Station reference data is emitted at startup and refreshed periodically. Previously seen observations are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-aviationweather:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-aviationweather:latest
```

## Using the Container Image

The container starts the bridge, polling the AviationWeather.gov API and writing observations to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-aviationweather:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-aviationweather:latest
```

### Preserving State Between Restarts

To preserve deduplication state between restarts, mount a volume and set the `AVIATIONWEATHER_LAST_POLLED_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e AVIATIONWEATHER_LAST_POLLED_FILE='/mnt/fileshare/aviationweather_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-aviationweather:latest
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

### `AVIATIONWEATHER_LAST_POLLED_FILE`

The file path for storing deduplication state. Defaults to `/mnt/fileshare/aviationweather_last_polled.json` inside the container.

### `AVIATIONWEATHER_STATIONS`

Comma-separated list of ICAO station IDs to monitor. Defaults to `KJFK,KLAX,KORD,KATL,EGLL,LFPG,EDDF,RJTT,YSSY,ZBAA`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-eventhub.json)
