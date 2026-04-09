# INPE DETER Brazil deforestation alerts bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between [INPE
TerraBrasilis DETER](http://terrabrasilis.dpi.inpe.br/) deforestation alert
feeds and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge
fetches deforestation alerts from the Amazon and Cerrado biomes and forwards
them to the configured Kafka endpoints.

## INPE TerraBrasilis DETER

[INPE DETER](http://terrabrasilis.dpi.inpe.br/) is Brazil's National Institute
for Space Research (INPE) real-time deforestation detection system. It monitors
the Amazon and Cerrado biomes using satellite imagery and publishes detected
deforestation polygons via OGC WFS (Web Feature Service) endpoints.

## Functionality

The bridge polls the INPE DETER WFS endpoints at regular intervals and writes
deforestation alerts to a Kafka topic as [CloudEvents](https://cloudevents.io/)
in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-inpe-deter-brazil:latest
```

## Using the Container Image

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-inpe-deter-brazil:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-inpe-deter-brazil:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `LOG_LEVEL`

The logging level. Default: `INFO`.

### `INPE_DETER_LAST_POLLED_FILE`

The file path where the bridge stores the last polled state. Default:
`~/.inpe_deter_brazil_last_polled.json`.
