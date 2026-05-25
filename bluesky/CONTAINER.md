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

---

## MQTT 5.0 / Unified-Namespace feeder (pilot)

A second container image, built from `Dockerfile.mqtt`, publishes the same
Bluesky firehose into an MQTT 5.0 broker using a Unified-Namespace
(UNS) topic tree. The Kafka image and contract are unchanged; the MQTT
sibling lives alongside, sharing nothing but the upstream subscription.

### Topic template

```
social/intl/bluesky/bluesky/{collection}/{lang}/{did}/{event}
```

* `{collection}` – AT Protocol NSID, e.g. `app.bsky.feed.post`
* `{lang}` – record language tag, lower-cased, defaults to `und`
* `{did}` – author DID (`did:plc:…` colons preserved as-is)
* `{event}` – literal tail baked per family: `post`, `like`, `repost`,
  `follow`, `block`, `profile`

The firehose is non-retained: every publish is **QoS 0** with
`retain=false`. Subscribers must be attached before publishers.

### CloudEvents binding

Binary mode – the CloudEvents attributes (`id`, `source`, `type`,
`subject`, `time`, `specversion`) ride as MQTT 5 user properties.
`ContentType` is `application/json`. `subject` equals the author DID.

### Pull & run

```bash
docker pull ghcr.io/clemensv/real-time-sources/bluesky-mqtt:latest

docker run --rm -e MQTT_BROKER_URL=mqtt://broker:1883 \
  ghcr.io/clemensv/real-time-sources/bluesky-mqtt:latest
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `MQTT_BROKER_URL` | `mqtt://host:port` or `mqtts://host:port` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional broker credentials |
| `MQTT_ENABLE_TLS` | `true` to force TLS (auto if scheme is `mqtts://`) |
| `BLUESKY_FIREHOSE_URL` | Override the AT Protocol Jetstream/firehose URL |
| `BLUESKY_MOCK` | `true` to emit one canned message per family (used by Docker E2E) |

## AMQP 1.0 container

The AMQP companion image publishes Bluesky Firehose CloudEvents to a single broker address. It supports SASL PLAIN for generic AMQP 1.0 brokers and CBS token authentication for Azure Service Bus (`AMQP_AUTH_MODE=entra` for managed identity, `AMQP_AUTH_MODE=sas` for emulator/SAS-key scenarios).

```bash
docker pull ghcr.io/clemensv/real-time-sources-bluesky-amqp:latest

docker run --rm   -e AMQP_BROKER_URL=amqp://user:password@broker:5672/bluesky   -e BLUESKY_MOCK=true   ghcr.io/clemensv/real-time-sources-bluesky-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full `amqp://` or `amqps://` URL. Path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URL is supplied. | `localhost` / 5672 or 5671 |
| `AMQP_ADDRESS` | Queue, topic, or link target address. | `bluesky` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_TLS` | Force TLS for generic brokers. | `false` |
| `AMQP_CONTENT_MODE` | CloudEvents AMQP binding mode: `binary` or `structured`. | `binary` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token scope for CBS/Entra authentication. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | User-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS key credentials for Service Bus emulator/SAS CBS. | empty |

### Deploy to Azure Service Bus

This template creates a Service Bus namespace and queue, user-assigned managed identity, role assignment for Azure Service Bus Data Sender, Log Analytics workspace, storage file share for state, and an Azure Container Instance running the AMQP image.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Finfra%2Fazure-template-amqp.json)
