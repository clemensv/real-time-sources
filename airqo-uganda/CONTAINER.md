# AirQo Uganda Air Quality Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the AirQo Uganda air quality monitoring network and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches air quality measurements from AirQo sensors across Uganda and East Africa and forwards them to the configured Kafka endpoints.

## AirQo API

AirQo operates a network of low-cost air quality sensors primarily deployed in Uganda and expanding across East Africa. The network monitors PM2.5, PM10, temperature, and humidity. Data is updated approximately every hour. The API provides both raw and machine-learning-calibrated particulate matter readings.

## Functionality

The bridge fetches site reference data from the public AirQo grids summary endpoint at startup, then polls the measurements endpoint periodically and writes new observations to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Previously seen measurement timestamps per device are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-airqo-uganda:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-airqo-uganda:latest
```

## Using the Container Image

The container starts the bridge, polling the AirQo API and writing measurements to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e AIRQO_API_KEY='<your-airqo-api-key>' \
    ghcr.io/clemensv/real-time-sources-airqo-uganda:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e AIRQO_API_KEY='<your-airqo-api-key>' \
    ghcr.io/clemensv/real-time-sources-airqo-uganda:latest
```

### Preserving State Between Restarts

To preserve the last seen timestamps between restarts and avoid reprocessing observations, mount a volume and set the `STATE_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e STATE_FILE='/mnt/fileshare/airqo_uganda_state.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-airqo-uganda:latest
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

### `AIRQO_API_KEY`

API key for authenticated AirQo endpoints. Required for fetching measurement data. Obtain a free key by registering at [AirQo Analytics](https://platform.airqo.net/).

### `STATE_FILE`

The file path for storing last seen timestamps per device for deduplication. Defaults to `/mnt/fileshare/airqo_uganda_state.json` inside the container.

### `POLLING_INTERVAL`

Polling interval in seconds. Defaults to `300` (5 minutes).
