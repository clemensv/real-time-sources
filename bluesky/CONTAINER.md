# Bluesky Firehose Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [Bluesky AT Protocol firehose](https://atproto.com/) and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge connects to the Bluesky firehose WebSocket stream and forwards events to the configured Kafka endpoints.

## Functionality

The bridge connects to the Bluesky firehose at `wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos` and processes repository commit events containing posts, likes, reposts, follows, blocks, and profile updates. It writes these events to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, which is documented in [EVENTS.md](EVENTS.md). You can filter which collection types to process using the `BLUESKY_COLLECTIONS` environment variable.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-bluesky:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-bluesky:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading data from the Bluesky firehose and writing it to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-bluesky:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-bluesky:latest
```

### Filtering Collection Types

By default, all collection types are processed. To filter specific types, set the `BLUESKY_COLLECTIONS` environment variable:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e BLUESKY_COLLECTIONS='app.bsky.feed.post,app.bsky.feed.like' \
    ghcr.io/clemensv/real-time-sources-bluesky:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. Ensure your Kafka brokers support SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `BLUESKY_FIREHOSE_URL`

The WebSocket URL of the Bluesky firehose. Default is `wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos`.

### `BLUESKY_COLLECTIONS`

Comma-separated list of collection types to process. Available types:
- `app.bsky.feed.post` - Posts
- `app.bsky.feed.like` - Likes
- `app.bsky.feed.repost` - Reposts
- `app.bsky.graph.follow` - Follows
- `app.bsky.graph.block` - Blocks
- `app.bsky.actor.profile` - Profile updates

Default: All types are processed.

### `BLUESKY_SAMPLE_RATE`

Sampling rate for events (0.0 to 1.0). For example, `0.1` processes 10% of events. Default is `1.0` (100%).

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-with-eventhub.json)