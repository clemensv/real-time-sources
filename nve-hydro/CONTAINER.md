# NVE Hydrology Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Norwegian Water Resources and
Energy Directorate's (NVE) hydrological monitoring network and Apache Kafka, Azure
Event Hubs, and Fabric Event Streams. The bridge polls the
[NVE HydAPI](https://hydapi.nve.no) for water level and discharge readings from
Norwegian gauging stations and forwards new observations as
[CloudEvents](https://cloudevents.io/) in JSON format.

> **Note:** The upstream data source requires an API key. Register at
> [hydapi.nve.no](https://hydapi.nve.no/UserDocumentation/) to obtain a free
> API key, then pass it via the `NVE_API_KEY` environment variable.

## Functionality

The bridge retrieves hydrological data from the NVE HydAPI — the official REST
API for hydrological observations in Norway — and writes entries to a Kafka topic
as [CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

On startup, the bridge emits `NO.NVE.Hydrology.Station` events for all active
monitoring stations (reference data). It then enters a polling loop, emitting
`NO.NVE.Hydrology.WaterLevelObservation` events only for new or changed readings
(delta emission).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

## Using the Container Image

The container starts the bridge in feed mode, reading data from the NVE HydAPI
and writing it to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e NVE_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e NVE_API_KEY='<your-api-key>' \
    -e KAFKA_BROKER='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

### Preserving State Between Restarts

To preserve the de-duplication state between container restarts and avoid
re-sending observations, mount a volume and set the `STATE_FILE` environment
variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/nve_hydro_state.json' \
    -e NVE_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

### Adjusting the Polling Interval

The default polling interval is 600 seconds (10 minutes). You can adjust it:

```shell
$ docker run --rm \
    -e NVE_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    -e POLLING_INTERVAL='300' \
    ghcr.io/clemensv/real-time-sources-nve-hydro:latest
```

## Environment Variables

### `NVE_API_KEY`

The API key for the NVE HydAPI. Required. Register at
[hydapi.nve.no](https://hydapi.nve.no/UserDocumentation/) to obtain a free key.

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for separate `KAFKA_BROKER` and
topic configuration, since the bootstrap server and topic are extracted from the
connection string.

### `KAFKA_BROKER`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced. Default: `nve-hydro`.

### `POLLING_INTERVAL`

The interval in seconds between polling cycles. Default: `600` (10 minutes).

### `STATE_FILE`

The file path where the bridge stores the de-duplication state. This tracks
which readings have already been forwarded, allowing the bridge to resume without
duplicating events after restarts. Default: `~/.nve_hydro_state.json`.

### `KAFKA_ENABLE_TLS`

Whether to use TLS for the Kafka connection. Default: `true`. Set to `false` for
plaintext connections to local brokers.
