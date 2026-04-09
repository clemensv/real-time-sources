# EAWS ALBINA Avalanche Bulletin Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the EAWS ALBINA avalanche bulletin system ([avalanche.report](https://avalanche.report)) and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches daily CAAMLv6 avalanche bulletins for European Alps regions and forwards them to the configured Kafka endpoints.

## EAWS ALBINA Avalanche Bulletin API

The European Avalanche Warning Services (EAWS) ALBINA system publishes daily avalanche danger bulletins in the CAAMLv6 standard format for the European Alps. Coverage includes Tirol (AT-07), South Tyrol (IT-32-BZ), Trentino (IT-32-TN), and Salzburg (AT-02). Bulletins are published twice daily during winter season (evening forecast + morning update) and include danger ratings on the 5-level EAWS scale, avalanche problem types, tendency forecasts, and snowpack analysis.

Data is freely available under Creative Commons Attribution (CC BY) license.

## Functionality

The bridge polls the ALBINA CAAMLv6 API at `https://avalanche.report/albina_files/` for today's and yesterday's bulletins and writes them to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md). Each bulletin is flattened into per-region events. Previously seen bulletin+region combinations are tracked in a state file to prevent duplicates.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-eaws-albina:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-eaws-albina:latest
```

## Using the Container Image

The container starts the bridge, polling the ALBINA API and writing avalanche bulletins to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-eaws-albina:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-eaws-albina:latest
```

### Preserving State Between Restarts

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e ALBINA_LAST_POLLED_FILE='/mnt/fileshare/albina_last_polled.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-eaws-albina:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

Comma-separated list of Kafka bootstrap servers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `KAFKA_ENABLE_TLS`

Enable TLS for Kafka connections (default: `true`). Set to `false` for plain connections.

### `ALBINA_LAST_POLLED_FILE`

File path for deduplication state. Default is `/mnt/fileshare/albina_last_polled.json`.

### `ALBINA_REGIONS`

Comma-separated region codes to monitor. Default: `AT-07,IT-32-BZ,IT-32-TN,AT-02`.

### `ALBINA_LANG`

Language for bulletin text. One of `en`, `de`, `it`. Default: `en`.
