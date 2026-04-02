# DWD Open Data Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the DWD (Deutscher Wetterdienst) open-data file server and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge polls weather observations, station metadata, and weather alerts from ~1,450 German weather stations and forwards them to the configured Kafka endpoint.

## DWD Open Data

The DWD Climate Data Center (CDC) provides free access to weather and climate data from German weather stations at [opendata.dwd.de](https://opendata.dwd.de/). Data includes 10-minute observations (temperature, precipitation, wind, solar), hourly observations, and CAP weather alerts.

## Functionality

The bridge retrieves data from the DWD open-data file server and writes it to a Kafka topic as [CloudEvents](https://cloudevents.io/) in a JSON format, which is documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-dwd:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-dwd:latest
```

## Using the Container Image

The container starts the bridge, reading data from the DWD open-data server and writing it to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-dwd:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-dwd:latest
```

### Selecting Modules

Enable or disable specific data modules:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DWD_MODULES='station_metadata,weather_alerts' \
    ghcr.io/clemensv/real-time-sources-dwd:latest
```

### Preserving State Between Restarts

Mount a volume and set the `STATE_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e STATE_FILE='/mnt/fileshare/dwd_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-dwd:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `STATE_FILE`

Path to the state file for checkpoint persistence. Defaults to `~/.dwd_state.json`.

### `DWD_MODULES`

Comma-separated list of module names to enable. Available modules: `station_metadata`, `station_obs_10min`, `station_obs_hourly`, `weather_alerts`.

### `DWD_MODULES_DISABLED`

Comma-separated list of module names to disable.

### `DWD_10MIN_PARAMS`

Comma-separated list of 10-minute observation categories. Default: `air_temperature,precipitation,wind,solar`.

### `DWD_STATIONS`

Comma-separated list of station IDs to filter. Default: all stations.

### `DWD_BASE_URL`

DWD server base URL. Default: `https://opendata.dwd.de`.
