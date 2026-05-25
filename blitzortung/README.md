# Blitzortung live lightning bridge

This bridge connects to the public LightningMaps / Blitzortung live websocket
feed and forwards live lightning strokes to Kafka as CloudEvents.

## Upstream

- **Public live transport kept**: `wss://live.lightningmaps.org:443/` and
  `wss://live2.lightningmaps.org:443/`
- **Public HTTP fallback reviewed and dropped**: `https://live*.lightningmaps.org/l/`
  is the browser fallback for the same live stroke stream, not a distinct data
  family
- **Archive paths reviewed and dropped**: the historical archive is not the
  real-time surface this source implements
- **Raw signal data reviewed and dropped**: contributor-oriented raw signal
  channels are not the public live-stroke stream and are not openly documented
  enough for this bridge
- **Reference data**: no public station metadata endpoint was found for the
  detector IDs exposed in the live `sta` map, so this source emits telemetry
  only

## Event model

The bridge emits one event family:

- **`Blitzortung.Lightning.LightningStroke`** — one located lightning stroke
  from the public live feed

The public websocket identifies strokes by source-scoped ids. The CloudEvents
subject and Kafka key therefore use the compound identity `{source_id}/{stroke_id}`.

The bridge keeps the detector-participation details from the public `sta` map
as a normalized array of `{station_id, status}` objects. The upstream does not
currently publish a public bit-level definition for the integer `status` value,
so the bridge preserves it verbatim and documents the gap rather than inventing
meanings.

## How to use

After installation, the command-line entry point is `blitzortung`.

### Probe the live feed

```bash
blitzortung probe --max-strokes 5
```

### Stream to Kafka

```bash
blitzortung feed --connection-string "<your-connection-string>"
```

or:

```bash
blitzortung feed \
    --kafka-bootstrap-servers "<bootstrap-servers>" \
    --kafka-topic "<topic>"
```

See [CONTAINER.md](CONTAINER.md) for container usage and [EVENTS.md](EVENTS.md)
for the emitted CloudEvents contract.

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


## MQTT 5.0 / UNS feeder

In addition to the Kafka producer, a non-retained MQTT 5.0 feeder
publishes the Blitzortung lightning firehose into a Unified-Namespace
topic tree:

```
weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke
```

The MQTT contract uses a separate schemagroup
(`Blitzortung.Lightning.mqtt.jstruct`) with one event family
(`LightningStroke`) carrying the spatial routing axes (`geohash5`,
`geohash7`) as required fields. The existing Kafka contract is
untouched. QoS 0, `retain=false`. CloudEvents binary mode; CE attributes
ride as MQTT 5 user properties; `subject` is
`{geohash5}/{geohash7}/{stroke_id}`.

See `CONTAINER.md` for the container image, environment variables, and
wildcard subscription patterns.

## MQTT and AMQP companion transports

This source now ships Kafka plus dedicated MQTT and AMQP companion containers. MQTT publishes binary-mode CloudEvents into the source-specific UNS topic tree declared in `xreg/`; AMQP publishes the same CloudEvents to the configured queue or topic address (`blitzortung`). Docker E2E mock mode is available through `BLITZORTUNG_MOCK=true`.

- MQTT image: `ghcr.io/clemensv/real-time-sources/blitzortung-mqtt`
- AMQP image: `ghcr.io/clemensv/real-time-sources/blitzortung-amqp`
- MQTT templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`
- AMQP templates: `azure-template-amqp.json`, `azure-template-with-servicebus.json`
