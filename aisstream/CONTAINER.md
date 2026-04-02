# AISstream.io Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between AISstream.io's real-time global AIS vessel tracking WebSocket API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge connects to the AISstream.io WebSocket and forwards pre-decoded AIS messages to the configured Kafka endpoint.

> **⚠️ Reliability Warning:** AISstream.io is a free, community-run service
> with no SLA. During our testing on 2026-04-02, the WebSocket accepted
> connections and API keys without error but delivered **zero messages** over
> sustained periods. Silent outages lasting hours to days have been
> [reported by multiple users](https://github.com/aisstream/issues/issues/134).
> The bridge reconnects automatically, but data gaps are expected.

## AISstream.io Data

AISstream.io provides free, real-time terrestrial AIS data from ground stations worldwide, covering approximately 200 km from coastlines. The service delivers pre-decoded JSON messages for all 23 standard AIS message types.

## Functionality

The bridge connects to the AISstream.io WebSocket API, subscribes to AIS messages with configurable geographic and message type filters, and writes them to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-aisstream:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e AISSTREAM_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-aisstream:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e AISSTREAM_API_KEY='<your-api-key>' \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-aisstream:latest
```

### Filtering by Region

```shell
$ docker run --rm \
    -e AISSTREAM_API_KEY='<your-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    -e AISSTREAM_BOUNDING_BOXES='35,-15,72,45' \
    ghcr.io/clemensv/real-time-sources-aisstream:latest
```

## Environment Variables

### `AISSTREAM_API_KEY`

AISstream.io API key. Obtain one by registering at [aisstream.io](https://aisstream.io/) via GitHub OAuth.

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

### `AISSTREAM_BOUNDING_BOXES`

Geographic filter as semicolon-separated bounding boxes: `lat1,lon1,lat2,lon2;...`. Default: `-90,-180,90,180` (global).

### `AISSTREAM_MESSAGE_TYPES`

Comma-separated list of AIS message type names to subscribe to. Default: all types.

### `AISSTREAM_FILTER_MMSI`

Comma-separated list of MMSI numbers to include. Default: all vessels.

### `AISSTREAM_FLUSH_INTERVAL`

Number of events to buffer before flushing the Kafka producer. Default: `1000`.
