# Blitzortung bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container streams live lightning strokes from the public
LightningMaps / Blitzortung websocket feed into Apache Kafka, Azure Event Hubs,
and Microsoft Fabric Event Streams as CloudEvents.

## Upstream source

The bridge targets the public live websocket used by LightningMaps:

- `wss://live.lightningmaps.org:443/`
- `wss://live2.lightningmaps.org:443/`

The feed delivers batches of compact lightning-stroke objects with source-scoped
stroke identifiers, coordinates, event timestamps, delay and accuracy values,
and optionally a detector participation map.

The upstream documentation explicitly frames the public maps and data as
community-run, non-commercial, and not an official safety information service.

## Functionality

The bridge keeps a live websocket open, reconnects automatically, resumes from
the last source-specific stroke ids it has seen, deduplicates recent strokes
across reconnects, and emits CloudEvents documented in [EVENTS.md](EVENTS.md).

This source emits telemetry only. The public live surface exposes detector ids
inside stroke payloads, but no public station metadata endpoint was found that
would support separate reference-data events.

## Pull the image

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-blitzortung:latest
```

## Run with Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-blitzortung:latest
```

## Run with a Kafka broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<bootstrap-servers>' \
    -e KAFKA_TOPIC='<topic>' \
    -e SASL_USERNAME='<username>' \
    -e SASL_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-blitzortung:latest
```

## Run with plain Kafka for Docker E2E

```shell
$ docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=host:9092;EntityPath=blitzortung' \
    -e KAFKA_ENABLE_TLS='false' \
    ghcr.io/clemensv/real-time-sources-blitzortung:latest
```

## Environment variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric style connection string. Overrides explicit Kafka settings when set. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated Kafka bootstrap servers. |
| `KAFKA_TOPIC` | Kafka topic to send events to. Defaults to the manifest topic `blitzortung`. |
| `SASL_USERNAME` | SASL PLAIN username. |
| `SASL_PASSWORD` | SASL PLAIN password. |
| `KAFKA_ENABLE_TLS` | Set to `false` for plain Kafka. Default: `true`. |
| `BLITZORTUNG_WS_URLS` | Comma-separated websocket URLs to cycle through. Default: LightningMaps live and live2. |
| `BLITZORTUNG_BBOX` | Bounding box sent to the upstream socket as `north,east,south,west`. Default: global extent. |
| `BLITZORTUNG_INCLUDE_STATIONS` | Set to `false` to skip requesting detector participation details. Default: `true`. |
| `BLITZORTUNG_SOURCE_MASK` | Upstream source-mask integer passed through to the websocket request. Default: `4`, which matches the public LightningMaps live source observed during implementation. |
| `BLITZORTUNG_FLUSH_INTERVAL` | Flush Kafka every N strokes. Default: `250`. |
| `BLITZORTUNG_MAX_RETRY_DELAY` | Maximum reconnect backoff in seconds. Default: `60`. |
| `BLITZORTUNG_STATE_FILE` | Path to the local resume/dedupe state file. Default: `/tmp/blitzortung_state.json` in the container. |
| `LOG_LEVEL` | Python log level. Default: `INFO`. |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-eventhub.json)


---

## MQTT 5.0 / Unified-Namespace feeder

A second container image, built from `Dockerfile.mqtt`, publishes the
Blitzortung lightning firehose into an MQTT 5.0 broker using a
Unified-Namespace topic tree. The Kafka image and the existing Kafka
contract are **unchanged**; the MQTT sibling reuses the same
`LightningStroke` event family extended with `geohash5`/`geohash7`
spatial routing axes derived in the bridge from the upstream
latitude/longitude.

### Topic template

```
weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke
```

| Axis | Meaning |
|------|---------|
| `{geohash5}` | 5-character geohash (~5 km cell) of the strike position |
| `{geohash7}` | 7-character geohash (~150 m cell) of the strike position |
| `{stroke_id}` | Upstream stroke identifier, stringified |
| `stroke` | Literal leaf for the single event family |

The firehose is non-retained: every publish is **QoS 0** with
`retain=false`. CloudEvents binary binding (attributes as MQTT 5 user
properties); `ContentType` is `application/json`; `subject` is
`{geohash5}/{geohash7}/{stroke_id}`.

### Pull & run

```bash
docker pull ghcr.io/clemensv/real-time-sources/blitzortung-mqtt:latest

docker run --rm \
  -e MQTT_BROKER_URL=mqtt://broker:1883 \
  ghcr.io/clemensv/real-time-sources/blitzortung-mqtt:latest
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `MQTT_BROKER_URL` | `mqtt://host:port` or `mqtts://host:port` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional broker credentials |
| `MQTT_ENABLE_TLS` | `true` to force TLS (auto if scheme is `mqtts://`) |
| `MQTT_CLIENT_ID` | Optional MQTT client id |
| `BLITZORTUNG_MOCK` | `true` to emit one canned synthetic stroke and exit (used by Docker E2E) |

### Wildcard subscription examples

| Goal | Subscribe |
|------|-----------|
| Every lightning stroke worldwide | `weather/intl/blitzortung/#` |
| Strokes in the `u0yje` 5-char cell (~Frankfurt) | `weather/intl/blitzortung/blitzortung/u0yje/+/+/stroke` |
| Strokes in a specific 7-char cell `u0yjeyu` | `weather/intl/blitzortung/blitzortung/u0yje/u0yjeyu/+/stroke` |
| Strokes across all of central Europe via the `u` prefix | `weather/intl/blitzortung/blitzortung/u+/+/+/stroke` (note: MQTT wildcards do not support prefix matching; instead subscribe to `weather/intl/blitzortung/#` and filter client-side) |

## MQTT and AMQP companion transports

This source now ships Kafka plus dedicated MQTT and AMQP companion containers. MQTT publishes binary-mode CloudEvents into the source-specific UNS topic tree declared in `xreg/`; AMQP publishes the same CloudEvents to the configured queue or topic address (`blitzortung`). Docker E2E mock mode is available through `BLITZORTUNG_MOCK=true`.

- MQTT image: `ghcr.io/clemensv/real-time-sources/blitzortung-mqtt`
- AMQP image: `ghcr.io/clemensv/real-time-sources/blitzortung-amqp`
- MQTT templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`
- AMQP templates: `azure-template-amqp.json`, `azure-template-with-servicebus.json`
