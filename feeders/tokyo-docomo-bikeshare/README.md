<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/jp.png" alt="Tokyo" width="64" height="48"><br>
<sub><b>Tokyo</b></sub>
</td>
<td valign="middle">

# Tokyo Docomo Bikeshare

<sub>1,794 stations, GBFS 2.3 via ODPT · Kafka · MQTT · AMQP · <a href="https://docomo-cycle.jp/tokyo/">upstream</a> · <a href="https://developer.odpt.org/info">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-2_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Tokyo, Japan — 1,794 stations, GBFS 2.3 via ODPT

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#tokyo-docomo-bikeshare) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://docomo-cycle.jp/tokyo/)

</td></tr></table>
<!-- source-hero:end -->

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://docomo-cycle.jp/tokyo/>
- API / data documentation: <https://developer.odpt.org/info>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

## Why this bridge

This bridge ingests **Tokyo Docomo Bikeshare GBFS feed via ODPT** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Build station-availability dashboards for bike-share operations in Tokyo.
- Trigger mobility workflows when stations run low on bikes or docks.
- Ingest bike-share status into Fabric/Eventhouse without building custom pollers.
- Correlate bike-share utilization with weather, transit, or event demand.
- Feed low-latency APIs and map experiences from one normalized stream.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Emits system, station metadata, and live station status as CloudEvents.
- Shared data contract across Kafka, MQTT, and AMQP variants.
- Connection-string support for Event Hubs/Fabric Event Streams.
- Transport-specific binaries with the same source model.

## Repository layout

```text
tokyo-docomo-bikeshare/
  xreg/tokyo-docomo-bikeshare.xreg.json
  tokyo_docomo_bikeshare/
  tokyo_docomo_bikeshare_amqp/
  tokyo_docomo_bikeshare_mqtt/
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
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/tokyo-docomo-bikeshare" \
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING`, `KAFKA_ENABLE_TLS`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_TLS`
- **AMQP image:** `AMQP_BROKER_URL or AMQP_HOST/AMQP_PORT/AMQP_ADDRESS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_AUTH_MODE`

## Data model

- `JP.ODPT.DocomoBikeshare.BikeshareSystem` — operator/system reference data.
- `JP.ODPT.DocomoBikeshare.BikeshareStation` — station reference metadata.
- `JP.ODPT.DocomoBikeshare.BikeshareStationStatus` — live bike/dock availability telemetry.


Primary message groups in xRegistry: `JP.ODPT.DocomoBikeshare.System`, `JP.ODPT.DocomoBikeshare.Stations`.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

Tokyo Docomo Bikeshare targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract.

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#tokyo-docomo-bikeshare) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source tokyo-docomo-bikeshare `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#tokyo-docomo-bikeshare/fabric-aci)


### Deploying into Azure Container Instances

2 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventgrid-mqtt.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
