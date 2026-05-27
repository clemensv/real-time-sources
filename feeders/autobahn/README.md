<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/de.png" alt="Germany" width="64" height="48"><br>
<sub><b>Germany</b></sub>
</td>
<td valign="middle">

# Autobahn

<sub>roadworks, warnings, closures, webcams · Kafka · MQTT · AMQP · <a href="https://autobahn.de/">upstream</a> · <a href="https://autobahn.api.bund.dev/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Germany — roadworks, warnings, closures, webcams

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#autobahn) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#autobahn/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/autobahn.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://autobahn.de/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns German Autobahn APIs into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://autobahn.de/>
- API / data documentation: <https://autobahn.api.bund.dev/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

German motorway operations teams, logistics platforms, emergency planners, navigation systems, and insurers use Autobahn status data for closures, incidents, and restrictions. This bridge standardizes polling, normalization, dedupe, CloudEvents shaping, and transport delivery so consumers subscribe once and reuse the same contract across platforms.

- **Traffic and mobility operations** — live dashboards and operational control-room views.
- **Route and dispatch optimization** — dynamic rerouting and ETA management under disruptions.
- **Analytics and planning** — long-running ingestion into Fabric Eventhouse / ADX / lakes.
- **Compliance and reporting** — auditable event history for public-sector and regulated workflows.
- **Cross-domain correlation** — fuse mobility events with weather, safety, and infrastructure feeds.

## Overview

**Autobahn** is a poll-based bridge that ingests upstream data from [German Autobahn APIs](https://verkehr.autobahn.de/o/autobahn) and re-emits normalized CloudEvents.

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-autobahn` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | JSON CloudEvents (binary mode), key templates `{identifier}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-autobahn-mqtt` | MQTT 5.0 broker (incl. Azure Event Grid MQTT) | Unified-Namespace topic tree rooted under `traffic/de/autobahn/...` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-autobahn-amqp` | AMQP 1.0 brokers incl. Azure Service Bus / Event Hubs | Binary CloudEvents to AMQP address `autobahn` |

All variants share:

- The same xRegistry contract (`xreg/autobahn.xreg.json`).
- The same event-family model and schema set.
- Poll-based acquisition logic with periodic refresh cycles.

## Key features

- Poll-based bridge with CloudEvents-first contract design.
- Shared event contract across Kafka, MQTT, and AMQP transports.
- Fabric-ready deployment path (Notebook and ACI hosting options).
- ARM templates for direct Azure Container Instance deployment targets.
- Source-specific event families and stable domain key templates.

## Repository layout

```text
autobahn/
  xreg/autobahn.xreg.json
  autobahn/
  autobahn_mqtt/
  autobahn_amqp/
  autobahn_producer/
  autobahn_mqtt_producer/
  autobahn_amqp_producer/
  kql/
  notebook/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS connectivity to the upstream API at `https://verkehr.autobahn.de/o/autobahn`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.
- A writable host directory mounted at `/state` for persistent polling/dedupe state.

## Quick start with Docker

> [!IMPORTANT]
> This source is poll-based. Mount a host volume and set `AUTOBAHN_STATE_FILE` so state survives container restarts.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e CONNECTION_STRING="<event-hubs-or-kafka-connection-string>" \
  ghcr.io/clemensv/real-time-sources-autobahn:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-autobahn-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/autobahn' \
  ghcr.io/clemensv/real-time-sources-autobahn-amqp:latest
```

## Configuration reference

The complete environment-variable matrix for Kafka, MQTT, and AMQP images (including authentication-mode differences and Azure deployment assumptions) is documented in [CONTAINER.md](CONTAINER.md).

## Data model

This source emits the following event families (see [EVENTS.md](EVENTS.md) for full schema-level detail):

- **DE.Autobahn** — 30 event type(s): DE.Autobahn.RoadworkAppeared, DE.Autobahn.RoadworkUpdated, DE.Autobahn.RoadworkResolved, DE.Autobahn.ShortTermRoadworkAppeared….

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

Autobahn targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#autobahn) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `autobahn` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/autobahn/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source autobahn `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#autobahn/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source autobahn `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#autobahn/fabric-aci)


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Use [CONTAINER.md](CONTAINER.md) for full auth-mode and environment-variable details.
- Validate transport-specific routing and key templates against your downstream topology.
- Review upstream usage guidance at [German Autobahn APIs](https://verkehr.autobahn.de/o/autobahn).
