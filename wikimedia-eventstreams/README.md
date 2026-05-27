<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# Wikimedia EventStreams

<sub>Wikipedia, Wikidata, Commons recent changes · Kafka · MQTT · AMQP · <a href="https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams">upstream</a> · <a href="https://stream.wikimedia.org/?doc">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-2_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — Wikipedia, Wikidata, Commons recent changes

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#wikimedia-eventstreams) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/wikimedia_eventstreams.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams)

</td></tr></table>
<!-- source-hero:end -->

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams>
- API / data documentation: <https://stream.wikimedia.org/?doc>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

## Why this bridge

This bridge ingests **Wikimedia recentchange EventStreams SSE feed** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Capture Wikimedia edit activity in near real time for observability and analytics.
- Enrich moderation and trust/safety pipelines with normalized edit events.
- Feed search, trend, and knowledge-graph workflows from one stream contract.
- Ingest continuous open knowledge activity into Fabric/Eventhouse.
- Avoid custom SSE reconnect/dedupe handling in every consumer.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Maintains continuous stream consumption with reconnect/resume support.
- Bounded dedupe controls for recent-change IDs.
- Kafka, MQTT, and AMQP variants emit the same event family.
- Tunable retry and flush behavior for long-running streams.

## Repository layout

```text
wikimedia-eventstreams/
  xreg/wikimedia_eventstreams.xreg.json
  wikimedia_eventstreams/
  wikimedia_eventstreams_amqp/
  wikimedia_eventstreams_mqtt/
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
  ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/wikimedia-eventstreams" \
  ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `WIKIMEDIA_EVENTSTREAMS_USER_AGENT`, `WIKIMEDIA_EVENTSTREAMS_STATE_FILE`, `WIKIMEDIA_EVENTSTREAMS_DEDUPE_SIZE`, `WIKIMEDIA_EVENTSTREAMS_MAX_RETRY_DELAY`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `WIKIMEDIA_EVENTSTREAMS_URL`, `WIKIMEDIA_EVENTSTREAMS_USER_AGENT`
- **AMQP image:** `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_CONTENT_MODE`, `WIKIMEDIA_EVENTSTREAMS_URL`, `WIKIMEDIA_EVENTSTREAMS_USER_AGENT`

## Data model

- `Wikimedia.EventStreams.RecentChange` — normalized recent-change event payload from Wikimedia projects.


Primary message groups in xRegistry: `Wikimedia.EventStreams`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source wikimedia-eventstreams -Workspace <id> -ResourceGroup <azure-rg> -Location <azure-region>
```

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-with-eventhub.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
