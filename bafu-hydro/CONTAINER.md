# BAFU Hydrology Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Swiss Federal Office for the
Environment's (BAFU/FOEN) hydrological monitoring network and Apache Kafka, Azure
Event Hubs, and Fabric Event Streams. The bridge polls the
[existenz.ch](https://api.existenz.ch) Hydro API for water level, discharge, and
temperature readings from ~300 Swiss gauging stations and forwards new
observations as [CloudEvents](https://cloudevents.io/) in JSON format.

> **Note:** The upstream data source requires no authentication or API key. The
> bridge can start fetching data immediately with no additional registration.

## Functionality

The bridge retrieves hydrological data from the existenz.ch API — which wraps
the official BAFU/FOEN measurements published at
[hydrodaten.admin.ch](https://www.hydrodaten.admin.ch) — and writes entries to a
Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented
in [EVENTS.md](EVENTS.md).

On startup, the bridge emits `CH.BAFU.Hydrology.Station` events for all
monitoring stations (reference data). It then enters a polling loop, emitting
`CH.BAFU.Hydrology.WaterLevelObservation` events only for new or changed
readings (delta emission).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-bafu-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-bafu-hydro:latest
```

## Using the Container Image

The container starts the bridge in feed mode, reading data from the existenz.ch
Hydro API and writing it to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-bafu-hydro:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    ghcr.io/clemensv/real-time-sources-bafu-hydro:latest
```

### Preserving State Between Restarts

To preserve the de-duplication state between container restarts and avoid
re-sending observations, mount a volume and set the `STATE_FILE` environment
variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/bafu_hydro_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-bafu-hydro:latest
```

### Adjusting the Polling Interval

The default polling interval is 600 seconds (10 minutes), matching the upstream
data update cadence. You can adjust it:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e POLLING_INTERVAL='300' \
    ghcr.io/clemensv/real-time-sources-bafu-hydro:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for separate `KAFKA_BROKER` and
topic configuration, since the bootstrap server and topic are extracted from the
connection string.

### `KAFKA_BROKER`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced. Default: `bafu-hydro`.

### `POLLING_INTERVAL`

The interval in seconds between polling cycles. Default: `600` (10 minutes).

### `STATE_FILE`

The file path where the bridge stores the de-duplication state. This tracks
which readings have already been forwarded, allowing the bridge to resume without
duplicating events after restarts. Default: `~/.bafu_hydro_state.json`.

### `KAFKA_ENABLE_TLS`

Whether to use TLS for the Kafka connection. Default: `true`. Set to `false` for
plaintext connections to local brokers.
