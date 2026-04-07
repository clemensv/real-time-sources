# German Waters Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between Germany's state-level hydrological
monitoring networks and Apache Kafka, Azure Event Hubs, and Fabric Event Streams.
The bridge aggregates water level, discharge, and related readings from ~2,724
gauging stations across 12 federal states — pulling exclusively from official
government open data portals — and forwards new observations as
[CloudEvents](https://cloudevents.io/) in JSON format.

> **Note:** The upstream data sources require no authentication or API keys. The
> bridge can start fetching data immediately with no additional registration.

## Functionality

The bridge polls 12 independent state-level water data providers — each with its
own API format (JSON, HTML scraping, GeoJSON, JavaScript arrays) — normalises the
readings, and writes them to a Kafka topic as [CloudEvents](https://cloudevents.io/)
in JSON format, documented in [EVENTS.md](EVENTS.md).

On startup, the bridge emits `DE.Waters.Hydrology.Station` events for all
monitoring stations (reference data). It then enters a polling loop, emitting
`DE.Waters.Hydrology.WaterLevelObservation` events only for new or changed
readings (delta emission via a de-duplication state file).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-german-waters:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-german-waters:latest
```

## Using the Container Image

The container starts the bridge in feed mode, reading data from the German state
water data portals and writing it to Kafka, Azure Event Hubs, or Fabric Event
Streams.

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### Preserving State Between Restarts

To preserve the de-duplication state between container restarts and avoid
re-sending observations, mount a volume and set the `STATE_FILE` environment
variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/german_waters_state.json' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### Filtering Providers

You can include or exclude specific state providers:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e PROVIDERS='bayern_gkd,nrw_hygon' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e EXCLUDE_PROVIDERS='sh_lkn,mv_lung' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

### Adjusting the Polling Interval

The default polling interval is 900 seconds (15 minutes). You can adjust it:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e POLLING_INTERVAL='600' \
    ghcr.io/clemensv/real-time-sources-german-waters:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for separate `KAFKA_BOOTSTRAP_SERVERS`
and topic configuration, since the bootstrap server and topic are extracted from the
connection string.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced. Must be provided via the
connection string or this variable when using a plain Kafka broker.

### `SASL_USERNAME`

Username for SASL PLAIN authentication against the Kafka broker.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication against the Kafka broker.

### `POLLING_INTERVAL`

The interval in seconds between polling cycles. Default: `900` (15 minutes).

### `STATE_FILE`

The file path where the bridge stores the de-duplication state. This tracks
which readings have already been forwarded, allowing the bridge to resume without
duplicating events after restarts. Default: `~/.german_waters_state.json`.

### `PROVIDERS`

Comma-separated list of provider keys to include. When set, only the listed
providers are polled. Available keys: `bayern_gkd`, `nrw_hygon`, `sh_lkn`,
`nds_nlwkn`, `sa_lhw`, `he_hlnug`, `sn_lfulg`, `bw_hvz`, `bb_lfu`,
`th_tlubn`, `mv_lung`, `be_senumvk`.

### `EXCLUDE_PROVIDERS`

Comma-separated list of provider keys to exclude from polling.

### `KAFKA_ENABLE_TLS`

Whether to use TLS for the Kafka connection. Default: `true`. Set to `false` for
plaintext connections to local brokers.
