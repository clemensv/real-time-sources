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
