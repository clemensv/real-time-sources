# Wikimedia EventStreams bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges Wikimedia Foundation's public
`recentchange` EventStreams feed into Apache Kafka, Azure Event Hubs, and
Microsoft Fabric Event Streams as CloudEvents.

## Wikimedia EventStreams

Wikimedia EventStreams is the public streaming interface for structured
event data emitted by Wikimedia projects. This container targets the
well-documented `recentchange` stream, which carries edits, new pages, log
actions, categorization changes, and related page activity across
Wikipedia, Wikidata, Commons, and sister projects.

- **Stream endpoint**: `https://stream.wikimedia.org/v2/stream/recentchange`
- **Protocol**: HTTP EventStreams, consumed as NDJSON
- **Authentication**: None
- **License**: Public Wikimedia stream; see upstream project and content
  licenses for downstream use constraints

## Functionality

The bridge opens a long-lived connection to the public recentchange stream,
normalizes the events into the checked-in xRegistry contract, and writes
them to the configured Kafka topic as CloudEvents documented in
[EVENTS.md](EVENTS.md).

It reconnects automatically, resumes with `?since=` using the last seen
event timestamp, and keeps a rolling dedupe cache of recent Wikimedia event
UUIDs to absorb replay after disconnects.

## Installing the Container Image

Pull the image from GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest
```

### With Plain Kafka for Docker E2E

```shell
$ docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=host:9092;EntityPath=wikimedia-eventstreams' \
    -e KAFKA_ENABLE_TLS='false' \
    ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest
```

## Environment Variables

### `CONNECTION_STRING`

Event Hubs / Fabric style connection string. If set, it overrides the
explicit Kafka arguments.

### `KAFKA_BOOTSTRAP_SERVERS`

Comma-separated Kafka bootstrap servers.

### `KAFKA_TOPIC`

Kafka topic name. Default in the manifest is `wikimedia-eventstreams`.

### `SASL_USERNAME`

SASL PLAIN username for Kafka authentication.

### `SASL_PASSWORD`

SASL PLAIN password for Kafka authentication.

### `KAFKA_ENABLE_TLS`

Set to `false` for plain Kafka. Default: `true`.

### `WIKIMEDIA_EVENTSTREAMS_STATE_FILE`

Path to the local state file used for resume and dedupe. Default:
`~/.wikimedia_eventstreams_state.json`.

### `WIKIMEDIA_EVENTSTREAMS_FLUSH_INTERVAL`

Flush Kafka every N events. Default: `250`.

### `WIKIMEDIA_EVENTSTREAMS_DEDUPE_SIZE`

Rolling dedupe window size in event IDs. Default: `5000`.

### `WIKIMEDIA_EVENTSTREAMS_MAX_RETRY_DELAY`

Maximum reconnect backoff in seconds. Default: `60`.

### `WIKIMEDIA_EVENTSTREAMS_USER_AGENT`

HTTP `User-Agent` header sent to Wikimedia. Wikimedia asks clients to set a
clear user agent; the bridge does so by default, and you can override it if
you need a more specific identifier.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-with-eventhub.json)


---

## MQTT 5.0 / Unified-Namespace feeder

A second container image, built from `Dockerfile.mqtt`, publishes the Wikimedia EventStreams `recentchange` feed to an MQTT 5.0 broker on a Unified-Namespace (UNS) topic tree. The Kafka image and contract are unchanged.

### Topic template

```
social/intl/wikimedia/wikimedia-eventstreams/{wiki}/{namespace_bucket}/{event_id}/recent-change
```

* `{wiki}` – wiki database name (e.g. `enwiki`, `commonswiki`, `wikidatawiki`)
* `{namespace_bucket}` – kebab-case bucket for the MediaWiki namespace number (`main`, `talk`, `file`, `category`, …; unknown values fall through to `ns-<n>`)
* `{event_id}` – upstream `meta.id`

Non-retained firehose: every publish is **QoS 0** with `retain=false`. Subscribers must be attached before the feeder starts. CloudEvents binary mode – CE attributes (`id`, `source`, `type`, `subject`, `time`, `specversion`) ride as MQTT 5 user properties. `ContentType=application/json`. `subject` equals `{wiki}/{namespace_bucket}/{event_id}`.

### Pull & run

```bash
docker pull ghcr.io/clemensv/real-time-sources/wikimedia-eventstreams-mqtt:latest

docker run --rm -e MQTT_BROKER_URL=mqtt://broker:1883 \
  ghcr.io/clemensv/real-time-sources/wikimedia-eventstreams-mqtt:latest
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `MQTT_BROKER_URL` | `mqtt://host:port` or `mqtts://host:port` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional broker credentials |
| `MQTT_ENABLE_TLS` | `true` to force TLS (auto if scheme is `mqtts://`) |
| `WIKIMEDIA_EVENTSTREAMS_URL` | Override the SSE source (default `https://stream.wikimedia.org/v2/stream/recentchange`) |
| `WIKIMEDIA_EVENTSTREAMS_USER_AGENT` | Custom User-Agent string |
| `WIKIMEDIA_EVENTSTREAMS_MAX_EVENTS` | Stop after this many publishes (0 = unbounded) |
| `WIKIMEDIA_EVENTSTREAMS_MOCK` | `true` to emit a synthetic corpus across namespace buckets then exit (used by Docker E2E) |

### Subscribe examples

```bash
# All wikis, all namespaces
mosquitto_sub -h broker -t 'social/intl/wikimedia/#'
# Only English Wikipedia main namespace
mosquitto_sub -h broker -t 'social/intl/wikimedia/wikimedia-eventstreams/enwiki/main/+/recent-change'
# All file uploads anywhere
mosquitto_sub -h broker -t 'social/intl/wikimedia/wikimedia-eventstreams/+/file/+/recent-change'
```
