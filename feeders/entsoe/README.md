<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/eu.png" alt="Europe" width="64" height="48"><br>
<sub><b>Europe</b></sub>
</td>
<td valign="middle">

# ENTSO-E

<sub>electricity generation, prices, load, flows (requires token) · Kafka · MQTT · AMQP · <a href="https://transparency.entsoe.eu/">upstream</a> · <a href="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-7_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-4_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Europe — electricity generation, prices, load, flows (requires token)

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#entsoe) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/entsoe.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://transparency.entsoe.eu/)

</td></tr></table>
<!-- source-hero:end -->

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://transparency.entsoe.eu/>
- API / data documentation: <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

## Why this bridge

This bridge ingests **ENTSO-E Transparency Platform REST API** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Stream power-market transparency data into operational and analytical systems.
- Correlate load, generation, and cross-border flows in one event contract.
- Build market monitoring and forecasting pipelines over continuously refreshed data.
- Feed Fabric/Eventhouse with typed electricity-domain events.
- Replace repeated XML pull/parsing logic across consuming teams.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Covers by-domain, by-domain+PSR-type, and cross-border document families.
- Supports Kafka, MQTT/UNS, and AMQP outputs from the same acquisition core.
- Filterable domains, document types, and cross-border pairs.
- State-backed incremental polling with configurable lookback.

## Repository layout

```text
entsoe/
  xreg/entsoe.xreg.json
  entsoe/
  entsoe_amqp/
  entsoe_core/
  entsoe_kafka/
  entsoe_mqtt/
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
  -e ENTSOE_SECURITY_TOKEN="<token>" -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest
```

### MQTT
```bash
docker run --rm \
  -e ENTSOE_SECURITY_TOKEN="<token>" -e MQTT_BROKER_URL="mqtt://<broker>:1883" \
  ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e ENTSOE_SECURITY_TOKEN="<token>" -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/entsoe" \
  ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `ENTSOE_SECURITY_TOKEN`, `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `ENTSOE_DOMAINS`, `ENTSOE_DOCUMENT_TYPES`, `ENTSOE_CROSS_BORDER_PAIRS`, `POLLING_INTERVAL`, `STATE_FILE`
- **MQTT image:** `ENTSOE_SECURITY_TOKEN`, `MQTT_BROKER_URL`, `MQTT_AUTH_MODE`, `MQTT_USERNAME / MQTT_PASSWORD`, `MQTT_ENTRA_CLIENT_ID`
- **AMQP image:** `ENTSOE_SECURITY_TOKEN`, `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_ENTRA_CLIENT_ID`, `AMQP_SAS_KEY_NAME / AMQP_SAS_KEY`

## Data model

- `eu.entsoe.transparency.ByDomain.*` families (prices, load, forecasts, generation, reservoirs).
- `eu.entsoe.transparency.ByDomainPsrType.*` families (PSR-type specific generation/capacity).
- `eu.entsoe.transparency.CrossBorder.CrossBorderPhysicalFlows` telemetry.


Primary message groups in xRegistry: `eu.entsoe.transparency.ByDomain`, `eu.entsoe.transparency.ByDomainPsrType`, `eu.entsoe.transparency.CrossBorder`.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

ENTSO-E targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#entsoe) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source entsoe `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#entsoe/fabric-aci)


### Deploying into Azure Container Instances

6 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentsoe%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentsoe%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentsoe%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentsoe%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentsoe%2Fazure-template-with-servicebus.json)

#### AMQP — bring your own AMQP 1.0 peer

Deploy the AMQP container against an existing AMQP 1.0 peer (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs). You pass the broker URL and credentials; the template provisions only the container.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentsoe%2Fazure-template-amqp.json)


### Self-hosted

Pull and run any of the 4 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
