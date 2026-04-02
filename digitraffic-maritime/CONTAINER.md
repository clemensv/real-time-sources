# Digitraffic Marine AIS Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between Finland's Digitraffic Marine real-time AIS vessel tracking MQTT stream and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge connects to the Digitraffic MQTT WebSocket and forwards vessel positions and metadata to the configured Kafka endpoint.

## Digitraffic Marine Data

Digitraffic Marine is an open data service from [Fintraffic](https://www.fintraffic.fi) providing real-time AIS data for the Finnish coastal zone and Baltic Sea. No API key or registration is required. The data is licensed under Creative Commons 4.0 BY.

> Source: Fintraffic / digitraffic.fi, license CC 4.0 BY

## Functionality

The bridge connects to the Digitraffic MQTT endpoint at `wss://meri.digitraffic.fi:443/mqtt`, subscribes to vessel location and metadata topics, and writes messages to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### Position Updates Only

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DIGITRAFFIC_SUBSCRIBE='location' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### Track Specific Vessels

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DIGITRAFFIC_FILTER_MMSI='230629000,219598000' \
    ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
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

### `DIGITRAFFIC_SUBSCRIBE`

Comma-separated list of message types to subscribe to: `location`, `metadata`, or both. Default: `location,metadata`.

### `DIGITRAFFIC_FILTER_MMSI`

Comma-separated list of MMSI numbers to include. When set, the bridge subscribes to specific vessel topics rather than wildcard topics. Default: all vessels.

### `DIGITRAFFIC_FLUSH_INTERVAL`

Number of events to buffer before flushing the Kafka producer. Default: `1000`.
