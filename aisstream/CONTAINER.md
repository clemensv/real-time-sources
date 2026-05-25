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

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-eventhub.json)


---

## MQTT 5.0 / Unified-Namespace feeder (pilot)

A second container image, built from `Dockerfile.mqtt`, publishes AIS
traffic into an MQTT 5.0 broker using a Unified-Namespace topic tree.
The Kafka image and the existing 23-message Kafka contract are unchanged;
the MQTT sibling is built on a new `IO.AISstream.mqtt.jstruct`
schemagroup (`PositionReport`, `ShipStatic`, `AidToNavigation`)
specifically enriched with the routing axes below. No existing Kafka
schemas were modified.

### Topic template

```
maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}
```

| Axis | Meaning |
|------|---------|
| `{flag}` | ISO-3166-1 alpha-2 (lower-case) derived from the MMSI MID; `xx` for special MMSIs (AtoN, SAR, …) or unknown MIDs |
| `{ship_type}` | Kebab bucket: `cargo`, `tanker`, `passenger`, `fishing`, `tug`, `pleasure-craft`, `high-speed`, `pilot`, `sar`, `aton`, `other`, `unknown` |
| `{geohash5}` | 5-character geohash of the last known position (`00000` if unknown for a static report) |
| `{mmsi}` | 9-digit MMSI |
| `{msg_type}` | Literal tail per family: `position-report`, `static`, `aid-to-navigation` |

The firehose is non-retained: every publish is **QoS 0** with
`retain=false`. CloudEvents binary binding (attributes as MQTT 5 user
properties); `ContentType` is `application/json`; `subject` equals the
MMSI.

### Ship-type & position caches

`ShipStatic` (Type 5 / 24) messages populate an in-memory MMSI →
ship-type cache; subsequent `PositionReport` messages from the same MMSI
inherit that bucket. Likewise the most recent position is cached so that
later static reports get a real `geohash5` instead of `00000`. Caches
are process-local and rebuild from the live stream after every restart.

### MID → ISO mapping

The MID-to-ISO table (`aisstream_mqtt/mid_iso.csv`) is a curated subset
of the public **ITU-R M.585** Maritime Identification Digits registry
(vintage `2024-01`). The ITU-R recommendation is openly published and
the digit→state mapping it contains is factual reference data and not
subject to copyright. Refresh the CSV when ITU publishes a new revision
and bump `MID_ISO_VERSION` in `enrichment.py`.

### Pull & run

```bash
docker pull ghcr.io/clemensv/real-time-sources/aisstream-mqtt:latest

docker run --rm \
  -e MQTT_BROKER_URL=mqtt://broker:1883 \
  -e AISSTREAM_API_KEY=$AISSTREAM_API_KEY \
  ghcr.io/clemensv/real-time-sources/aisstream-mqtt:latest
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `MQTT_BROKER_URL` | `mqtt://host:port` or `mqtts://host:port` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional broker credentials |
| `MQTT_ENABLE_TLS` | `true` to force TLS (auto if scheme is `mqtts://`) |
| `AISSTREAM_API_KEY` | Required for the AISstream.io WebSocket firehose |
| `AISSTREAM_BBOX` | Optional comma list `lat1,lon1,lat2,lon2` of bounding boxes |
| `AISSTREAM_MOCK` | `true` to emit one canned message per family (used by Docker E2E) |

## AMQP 1.0 companion feeder

Pull and run the AMQP image:

```bash
docker pull ghcr.io/clemensv/real-time-sources-aisstream-amqp:latest
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=aisstream \
  -e AMQP_USERNAME=user \
  -e AMQP_PASSWORD=secret \
  -e AMQP_AUTH_MODE=password \
  -e AISSTREAM_MOCK=true \
  ghcr.io/clemensv/real-time-sources-aisstream-amqp:latest
```

For Azure Service Bus, set `AMQP_AUTH_MODE=entra`, `AMQP_HOST=<namespace>.servicebus.windows.net`, `AMQP_PORT=5671`, `AMQP_TLS=true`, and optionally `AMQP_ENTRA_CLIENT_ID` for a user-assigned managed identity. For the Service Bus emulator or SAS-only namespaces, use `AMQP_AUTH_MODE=sas` with `AMQP_SAS_KEY_NAME` and `AMQP_SAS_KEY`.

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional full AMQP URL; path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port. | localhost / 5672 |
| `AMQP_ADDRESS` | Queue/topic/event-hub name. | `aisstream` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_TLS` | Enable TLS for AMQP. | false (`entra` implies TLS) |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | User-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | empty |

Deploy a new Service Bus queue plus managed identity with [`azure-template-with-servicebus.json`](azure-template-with-servicebus.json) or [`infra/azure-template-amqp.json`](infra/azure-template-amqp.json).
