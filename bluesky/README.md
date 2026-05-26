# Bluesky Firehose feeder

Companion docs:

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

## Why this bridge

This bridge ingests **AT Protocol Bluesky firehose websocket** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Ingest social activity streams for trend and moderation analytics.
- Power near-real-time content and graph observability pipelines.
- Apply collection-level filters before data reaches downstream systems.
- Publish high-volume stream data into Kafka/MQTT/AMQP from one bridge.
- Use cursor-based resume behavior to reduce replay gaps after restarts.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-bluesky:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-bluesky-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-bluesky-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Supports key AT Protocol collections (posts, likes, reposts, follows, blocks, profiles).
- Streaming transport variants share one CloudEvents contract family.
- Filter and sample controls for high-throughput scenarios.
- Cursor persistence support on Kafka variant.

## Repository layout

```text
bluesky/
  xreg/bluesky.xreg.json
  bluesky/
  bluesky_amqp/
  bluesky_mqtt/
  botfinder/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
  README.md
  CONTAINER.md
  EVENTS.md
```

## Prerequisites

- Docker 20.10+ (or compatible OCI runtime).
- Outbound connectivity to the upstream source endpoint(s).
- Network access to your target messaging broker (Kafka, MQTT, or AMQP).

## Quick start with Docker

### Kafka
```bash
docker run --rm \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-bluesky:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-bluesky-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/bluesky" \
  ghcr.io/clemensv/real-time-sources-bluesky-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING`, `BLUESKY_FIREHOSE_URL`, `BLUESKY_COLLECTIONS`, `BLUESKY_SAMPLE_RATE`, `BLUESKY_CURSOR_FILE`, `KAFKA_ENABLE_TLS`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `BLUESKY_COLLECTIONS`
- **AMQP image:** `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_CONTENT_MODE`, `BLUESKY_COLLECTIONS`

## Data model

- `Bluesky.Feed.Post`, `Bluesky.Feed.Like`, `Bluesky.Feed.Repost` telemetry events.
- `Bluesky.Graph.Follow`, `Bluesky.Graph.Block` relationship events.
- `Bluesky.Actor.Profile` profile metadata updates.


Primary message groups in xRegistry: `BlueskyFirehose`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source bluesky -WorkspaceId <id> -CapacityId <id>
```

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-with-eventhub.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
