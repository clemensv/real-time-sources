<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/no.png" alt="Norway" width="64" height="48"><br>
<sub><b>Norway</b></sub>
</td>
<td valign="middle">

# Entur Norway

<sub>national real-time transit, SIRI ET/VM/SX · Kafka · MQTT · AMQP · <a href="https://entur.no/">upstream</a> · <a href="https://developer.entur.org/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Norway — national real-time transit, SIRI ET/VM/SX

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#entur-norway) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/entur-norway.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://entur.no/)

</td></tr></table>
<!-- source-hero:end -->

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://entur.no/>
- API / data documentation: <https://developer.entur.org/>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

> [!NOTE]
> Entur data is published under NLOD. Keep attribution and license obligations in downstream use.

## Why this bridge

This bridge ingests **Entur real-time SIRI ET/VM/SX feeds** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Power national or regional public-transport situation rooms with one feed.
- Blend ETA predictions, vehicle positions, and disruption notices in near real time.
- Feed transit analytics and passenger-information systems from a normalized contract.
- Stream alerts and journey updates into Eventhouse/Fabric for SLA and reliability tracking.
- Reduce bespoke API polling and SIRI parsing in downstream services.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-entur-norway:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-entur-norway-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-entur-norway-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Publishes ET, VM, and SX families as CloudEvents.
- Consistent contract across Kafka, MQTT, and AMQP builds.
- Supports batching/pagination controls for Entur payloads.
- Ready for Event Hubs/Fabric connection-string deployments.

## Repository layout

```text
entur-norway/
  xreg/entur-norway.xreg.json
  entur_norway/
  entur_norway_amqp/
  entur_norway_mqtt/
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
  ghcr.io/clemensv/real-time-sources-entur-norway:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-entur-norway-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/entur-norway" \
  ghcr.io/clemensv/real-time-sources-entur-norway-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING`, `KAFKA_ENABLE_TLS`, `POLLING_INTERVAL`, `STATE_FILE`, `MAX_SIZE`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `MQTT_CONTENT_MODE`
- **AMQP image:** `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_ENTRA_CLIENT_ID`, `AMQP_SAS_KEY_NAME / AMQP_SAS_KEY`

## Data model

- `no.entur.journeys.DatedServiceJourney` — reference journey context.
- `no.entur.journeys.EstimatedVehicleJourney` — ETA and prediction updates.
- `no.entur.journeys.MonitoredVehicleJourney` — live vehicle monitoring data.
- `no.entur.situations.PtSituationElement` — disruption and situation messages.


Primary message groups in xRegistry: `no.entur.journeys`, `no.entur.situations`.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

Entur Norway targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#entur-norway) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source entur-norway `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#entur-norway/fabric-aci)


### Deploying into Azure Container Instances

3 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentur-norway%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentur-norway%2Fazure-template-with-eventhub.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fentur-norway%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
