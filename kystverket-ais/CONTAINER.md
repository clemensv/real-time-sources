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

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template-with-eventhub.json)


---

## MQTT 5.0 / Unified-Namespace feeder

A second container image, built from `Dockerfile.mqtt`, publishes the
same Kystverket AIS firehose into an MQTT 5.0 broker using a
Unified-Namespace topic tree. The Kafka image and the existing Kafka
contract are **unchanged**; the MQTT sibling is built on a new
`NO.Kystverket.AIS.mqtt.jstruct` schemagroup (`PositionReport`,
`ShipStatic`, `AidToNavigation`) specifically enriched with the routing
axes below. No existing Kafka schemas were modified.

### Topic template

```
maritime/intl/kystverket/ais/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}
```

| Axis | Meaning |
|------|---------|
| `{flag}` | ISO-3166-1 alpha-2 (lower-case) derived from the MMSI MID; `xx` for special MMSIs or unknown MIDs |
| `{ship_type}` | Kebab bucket: `cargo`, `tanker`, `passenger`, `fishing`, `tug`, `pleasure-craft`, `high-speed`, `pilot`, `sar`, `aton`, `other`, `unknown` |
| `{geohash5}` | 5-character geohash of the last known position (`00000` if unknown for a static report) |
| `{mmsi}` | 9-digit MMSI |
| `{msg_type}` | Literal tail per family: `position-report`, `static`, `aid-to-navigation` |

The firehose is non-retained: every publish is **QoS 0** with
`retain=false`. CloudEvents binary binding (attributes as MQTT 5 user
properties); `ContentType` is `application/json`; `subject` equals the
MMSI.

### Ship-type & position caches

`ShipStatic` messages populate an in-memory MMSI → ship-type cache;
subsequent `PositionReport` messages from the same MMSI inherit that
bucket. Likewise the most recent position is cached so that later static
reports get a real `geohash5` instead of `00000`. Caches are
process-local and rebuild from the live TCP stream after every restart.

### MID → ISO mapping

Same curated subset of the public ITU-R M.585 MID registry as the
`aisstream` MQTT sibling (vintage `2024-01`). Refresh the CSV when ITU
publishes a new revision and bump `MID_ISO_VERSION` in `enrichment.py`.

### Pull & run

```bash
docker pull ghcr.io/clemensv/real-time-sources/kystverket-ais-mqtt:latest

docker run --rm \
  -e MQTT_BROKER_URL=mqtt://broker:1883 \
  ghcr.io/clemensv/real-time-sources/kystverket-ais-mqtt:latest
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `MQTT_BROKER_URL` | `mqtt://host:port` or `mqtts://host:port` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional broker credentials |
| `MQTT_ENABLE_TLS` | `true` to force TLS (auto if scheme is `mqtts://`) |
| `MQTT_CLIENT_ID` | Optional MQTT client id |
| `KYSTVERKET_AIS_TCP_HOST` / `KYSTVERKET_AIS_TCP_PORT` | Upstream Kystverket TCP NMEA endpoint (defaults match the Kafka bridge) |
| `KYSTVERKET_AIS_MOCK` | `true` to emit one canned message per family (used by Docker E2E) |

### Wildcard subscription examples

| Goal | Subscribe |
|------|-----------|
| Everything from Kystverket | `maritime/intl/kystverket/ais/#` |
| All Norwegian-flagged vessels | `maritime/intl/kystverket/ais/no/+/+/+/+` |
| All cargo movements anywhere | `maritime/intl/kystverket/ais/+/cargo/+/+/+` |
| All position reports in a 5-char cell `u4pru` | `maritime/intl/kystverket/ais/+/+/u4pru/+/position-report` |
| Aids-to-Navigation only | `maritime/intl/kystverket/ais/+/+/+/+/aid-to-navigation` |
