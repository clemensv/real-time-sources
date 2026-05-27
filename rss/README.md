# RSS/Atom feeder

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.rssboard.org/rss-specification>
- API / data documentation: <https://www.rssboard.org/rss-specification>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

## Why this bridge

This bridge ingests **RSS/Atom feed URLs and OPML lists** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Convert heterogeneous RSS/Atom feeds into one CloudEvents stream.
- Feed news/event-monitoring systems without custom parser logic per feed.
- Run lightweight monitoring with configurable sample mode and intervals.
- Stream normalized entries into Fabric/Eventhouse for search and enrichment.
- Maintain feed-state continuity with persisted feed state storage.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-rss:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-rss-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-rss-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Parses RSS and Atom feeds (plus OPML input lists).
- Tracks per-feed state for efficient repeated polling.
- Kafka, MQTT, and AMQP variants share the same event contract.
- Supports one-shot and continuous processing modes.

## Repository layout

```text
rss/
  xreg/feeds.xreg.json
  rssbridge/
  rssbridge_amqp/
  rssbridge_mqtt/
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
  -e CONNECTION_STRING="<connection-string>" -e FEED_URLS="https://example.com/feed.xml" \
  ghcr.io/clemensv/real-time-sources-rss:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" -e FEED_URLS="https://example.com/feed.xml" \
  ghcr.io/clemensv/real-time-sources-rss-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/rss" -e FEED_URLS="https://example.com/feed.xml" \
  ghcr.io/clemensv/real-time-sources-rss-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME / SASL_PASSWORD`, `KAFKA_ENABLE_TLS`, `FEED_URLS`, `STATE_DIR`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `MQTT_CONTENT_MODE`, `FEED_URLS`, `STATE_DIR`
- **AMQP image:** `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_CONTENT_MODE`, `FEED_URLS`, `STATE_DIR`

## Data model

- `Microsoft.OpenData.RssFeeds.FeedItem` — normalized feed entry payload with source/feed metadata.


Primary message groups in xRegistry: `Microsoft.OpenData.RssFeeds`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source rss -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>
```

The script provisions the Fabric Eventhouse, applies the source KQL schema when the source checks one in, creates the Event Stream custom endpoint, and deploys the Azure Container Instance with the resulting connection string wired into the feeder container.

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-with-eventhub.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
