# RSS/Atom Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between RSS and Atom feeds and Apache
Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches entries
from specified feeds and forwards them to the configured Kafka endpoints.

The bridge can be configured with a list of RSS feed URLs or OPML file URLs.

The most convenient way to manage a list of RSS feeds is to use an
[OPML](https://en.wikipedia.org/wiki/OPML) file that contains a list of feeds
and is available via HTTP. The bridge can fetch the OPML file and extract the
feed URLs from it. If the OPML file shall not be public, you can host it on a
cloud storage service like Azure Blob Storage or AWS S3 and provide the URL
including an access token.

An example OPML file is part of the repository and can be found at
[world_news.opml](opml/world_news.opml). If you want to reference it directly from the container, you need
to use the ["raw" URL](https://raw.githubusercontent.com/clemensv/real-time-sources/main/rss/opml/world_news.opml)

## Functionality

The bridge retrieves data from RSS and Atom feeds and writes the entries to a
Kafka topic as [CloudEvents](https://cloudevents.io/) in a JSON format, which is
documented in [EVENTS.md](EVENTS.md). You can specify multiple feed URLs by
providing them in the configuration.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-rss:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-rss:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading data from the
specified RSS and Atom feeds and writing it to Kafka, Azure Event Hubs, or
Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e FEED_URLS='<feed-urls>' \
    ghcr.io/clemensv/real-time-sources-rss:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, Azure CLI, or the "custom endpoint" of
a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e FEED_URLS='<feed-urls>' \
    ghcr.io/clemensv/real-time-sources-rss:latest
```

### Preserving State Between Restarts

To preserve the state between restarts and avoid reprocessing feed entries,
mount a volume to the container and set the `STATE_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/rssbridge_state.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-rss:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`,
`SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with
TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. Ensure your Kafka brokers support SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `FEED_URLS`

A comma-separated list of RSS or Atom feed URLs to fetch entries from.

### `STATE_FILE`

The file path where the bridge stores the state of processed entries. This helps
in resuming data fetching without duplication after restarts. Default is
`/mnt/state/rssbridge_state.json`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-with-eventhub.json)

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-rss-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `Microsoft.OpenData.RssFeeds.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-rss-mqtt:latest
```

### MQTT environment variables

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL including host, port, and TLS scheme, for example `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional username/password credentials for brokers that require user authentication. Leave unset for anonymous brokers. |
| `MQTT_CLIENT_ID` | Optional MQTT client identifier. Set it explicitly on shared brokers and Event Grid namespaces. |
| `MQTT_CONTENT_MODE` | CloudEvents content mode, `binary` by default. Keep `binary` for MQTT 5 user-property metadata. |
| `POLLING_INTERVAL` | Source polling interval in seconds, when supported by the feeder. |
| `STATE_FILE` | Optional path for source dedupe/checkpoint state, when the feeder maintains local state. |
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `news/intl/rss/rss`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `news/intl/rss/rss/{feed_slug}/{item}` | `Microsoft.OpenData.RssFeeds.FeedItem` | `false` | `1` | `` |

### Subscription patterns

```text
# Everything from this source
news/intl/rss/rss/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-with-eventgrid-mqtt.json)


## AMQP 1.0 container

The AMQP companion image publishes RSS/Atom feeds CloudEvents to a single broker address. It supports SASL PLAIN for generic AMQP 1.0 brokers and CBS token authentication for Azure Service Bus (`AMQP_AUTH_MODE=entra` for managed identity, `AMQP_AUTH_MODE=sas` for emulator/SAS-key scenarios).

```bash
docker pull ghcr.io/clemensv/real-time-sources-rss-amqp:latest

docker run --rm   -e AMQP_BROKER_URL=amqp://user:password@broker:5672/rss   -e RSS_SAMPLE_MODE=true   ghcr.io/clemensv/real-time-sources-rss-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full `amqp://` or `amqps://` URL. Path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URL is supplied. | `localhost` / 5672 or 5671 |
| `AMQP_ADDRESS` | Queue, topic, or link target address. | `rss` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_TLS` | Force TLS for generic brokers. | `false` |
| `AMQP_CONTENT_MODE` | CloudEvents AMQP binding mode: `binary` or `structured`. | `binary` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token scope for CBS/Entra authentication. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | User-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS key credentials for Service Bus emulator/SAS CBS. | empty |

### Deploy to Azure Service Bus

This template creates a Service Bus namespace and queue, user-assigned managed identity, role assignment for Azure Service Bus Data Sender, Log Analytics workspace, storage file share for state, and an Azure Container Instance running the AMQP image.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Finfra%2Fazure-template-amqp.json)
