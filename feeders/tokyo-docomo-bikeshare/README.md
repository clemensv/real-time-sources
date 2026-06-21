<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/jp.png" alt="Tokyo" width="64" height="48"><br>
<sub><b>Tokyo</b></sub>
</td>
<td valign="middle">

# Tokyo Docomo Bikeshare

<sub>Configuration-only GBFS wrapper for docomo-cycle-tokyo via ODPT · Kafka · MQTT · AMQP · <a href="https://docomo-cycle.jp/tokyo/">upstream</a> · <a href="https://developer.odpt.org/info">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">

> Tokyo, Japan — Docomo Bikeshare GBFS feed running on the generalized gbfs-bikeshare feeder

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#tokyo-docomo-bikeshare) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/tokyo-docomo-bikeshare.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://docomo-cycle.jp/tokyo/)

</td></tr></table>
<!-- source-hero:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published thin-wrapper images, environment variables, and Azure deployment options.
- [EVENTS.md](EVENTS.md) — the consolidated `gbfs-bikeshare` CloudEvents contract used by this wrapper.

## Upstream

- Home page: <https://docomo-cycle.jp/tokyo/>
- API / data documentation: <https://developer.odpt.org/info>
- GBFS autodiscovery URL: <https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json>

## Why this wrapper

Tokyo Docomo Bikeshare publishes station metadata and live bike / dock availability through GBFS. Mobility operations teams, city dashboards, trip-planning systems, and analytics pipelines can use those events to monitor station health, detect shortages, and correlate bike-share supply with transit, weather, and demand signals.

This directory is now intentionally **configuration only**. The runtime, generated producers, xRegistry manifest, and schema maintenance live in [`../gbfs-bikeshare`](../gbfs-bikeshare); this wrapper only pins the Tokyo Docomo discovery URL and stable `docomo-cycle-tokyo` system id.

> **Wire-contract change:** the former bespoke event types `jp.odpt.docomo.bikeshare.*` / `JP.ODPT.DocomoBikeshare.*` are replaced by the consolidated GBFS event types `org.gbfs.SystemInformation`, `org.gbfs.StationInformation`, and `org.gbfs.StationStatus`. Existing consumers of the old per-source contract must migrate to the GBFS contract documented in [EVENTS.md](EVENTS.md).

## Overview

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest` | Apache Kafka / Event Hubs / Fabric Event Streams | topic `tokyo-docomo-bikeshare`; keys follow the GBFS CloudEvents subject (`{system_id}`, `{system_id}/{station_id}`) |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest` | MQTT 5.0 / Unified Namespace | `mobility/gbfs/docomo-cycle-tokyo/...` topic tree with retained reference events |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest` | AMQP 1.0 / Service Bus / Artemis / RabbitMQ AMQP 1.0 | address `tokyo-docomo-bikeshare`, binary-mode CloudEvents |

## Configuration baked into the thin images

| Variable | Value | Notes |
|---|---|---|
| `GBFS_FEEDS` | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json` | Tokyo Docomo GBFS autodiscovery URL. |
| `GBFS_SYSTEM_IDS` | `docomo-cycle-tokyo` | Stable subject/key prefix for this deployment. |

`GBFS_API_KEY` is intentionally **not** baked into the image. Provide the ODPT consumer key at runtime; the base `gbfs-bikeshare` runtime appends it as query parameter `acl:consumerKey` by default.

## Quick start with Docker

### Kafka

```bash
docker run --rm   -e GBFS_API_KEY="<odpt-consumer-key>"   -e CONNECTION_STRING="BootstrapServer=<host:port>;EntityPath=tokyo-docomo-bikeshare"   -e KAFKA_ENABLE_TLS=false   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

### MQTT

```bash
docker run --rm   -e GBFS_API_KEY="<odpt-consumer-key>"   -e MQTT_BROKER_URL="mqtts://<broker>:8883"   -e MQTT_USERNAME="<user>"   -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
```

### AMQP

```bash
docker run --rm   -e GBFS_API_KEY="<odpt-consumer-key>"   -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672"   -e AMQP_ADDRESS="tokyo-docomo-bikeshare"   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
```

## Repository layout

```text
tokyo-docomo-bikeshare/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
  README.md
  CONTAINER.md
  EVENTS.md
  kql/tokyo-docomo-bikeshare.kql
  azure-template*.json
```

## Data model

This wrapper emits the already-reviewed GBFS contract:

- `org.gbfs.SystemInformation` — GBFS system reference metadata.
- `org.gbfs.StationInformation` — station reference metadata.
- `org.gbfs.StationStatus` — live station availability telemetry.

The canonical schema source is [`../gbfs-bikeshare/xreg/gbfs-bikeshare.xreg.json`](../gbfs-bikeshare/xreg/gbfs-bikeshare.xreg.json).

## Deploy

Use the portal card for this source to deploy the thin wrapper images with the Tokyo configuration already set:

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#tokyo-docomo-bikeshare/fabric-aci)

Azure Container Instance templates are documented in [CONTAINER.md](CONTAINER.md). They expose `GBFS_API_KEY` as a runtime secret and keep `GBFS_FEEDS` / `GBFS_SYSTEM_IDS` pinned to the Tokyo Docomo values above.
