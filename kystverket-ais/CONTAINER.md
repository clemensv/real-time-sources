# Kystverket AIS Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the Norwegian Coastal Administration's (Kystverket) real-time AIS vessel tracking stream and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge connects to a raw TCP socket broadcasting AIS NMEA sentences and forwards decoded vessel position reports, static data, and navigational aid information to the configured Kafka endpoint.

## Kystverket AIS Data

Kystverket provides open, real-time AIS data from 50+ terrestrial and offshore stations covering the Norwegian economic zone, Svalbard, and Jan Mayen. The stream delivers ~34 messages/second (~2.9 million/day) of decoded vessel tracking data.

## Functionality

The bridge connects to the Kystverket AIS TCP stream, decodes NMEA AIS sentences (including multi-sentence reassembly), and writes them to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-kystverket-ais:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-kystverket-ais:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-kystverket-ais:latest
```

### Filtering Message Types

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e AIS_MESSAGE_TYPES='1,2,3,18,19' \
    ghcr.io/clemensv/real-time-sources-kystverket-ais:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `AIS_TCP_HOST`

Kystverket AIS TCP stream host. Default: `153.44.253.27`.

### `AIS_TCP_PORT`

Kystverket AIS TCP stream port. Default: `5631`.

### `AIS_MESSAGE_TYPES`

Comma-separated list of AIS message type numbers to forward. Default: `1,2,3,5,18,19,24,21`.

### `AIS_FILTER_MMSI`

Comma-separated list of MMSI numbers to include. Default: all vessels.

### `AIS_FLUSH_INTERVAL`

Number of events to buffer before flushing the Kafka producer. Default: `1000`.
