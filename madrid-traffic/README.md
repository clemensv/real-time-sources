<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/es.png" alt="Madrid" width="64" height="48"><br>
<sub><b>Madrid</b></sub>
</td>
<td valign="middle">

# Madrid Traffic

<sub>~4,000 sensors, Informo · Kafka · MQTT · AMQP · <a href="https://datos.madrid.es/">upstream</a> · <a href="https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=02f2c23866b93410VgnVCM1000000b205a0aRCRD">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-4_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Madrid, Spain — ~4,000 sensors, Informo

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#madrid-traffic) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#madrid-traffic/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/madrid_traffic.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://datos.madrid.es/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns Madrid Informo traffic sensor feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://datos.madrid.es/>
- API / data documentation: <https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=02f2c23866b93410VgnVCM1000000b205a0aRCRD>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

City traffic-control teams, route-planning systems, mobility dashboards, and researchers use Madrid sensor data for congestion monitoring and trend analysis. This bridge standardizes polling, normalization, dedupe, CloudEvents shaping, and transport delivery so consumers subscribe once and reuse the same contract across platforms.

- **Traffic and mobility operations** — live dashboards and operational control-room views.
- **Route and dispatch optimization** — dynamic rerouting and ETA management under disruptions.
- **Analytics and planning** — long-running ingestion into Fabric Eventhouse / ADX / lakes.
- **Compliance and reporting** — auditable event history for public-sector and regulated workflows.
- **Cross-domain correlation** — fuse mobility events with weather, safety, and infrastructure feeds.

## Overview

**Madrid Traffic** is a poll-based bridge that ingests upstream data from [Madrid Informo traffic sensor feed](https://informo.madrid.es/informo/tmadrid/pm.xml) and re-emits normalized CloudEvents.

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-madrid-traffic` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | JSON CloudEvents (binary mode), key templates `{sensor_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-madrid-traffic-mqtt` | MQTT 5.0 broker (incl. Azure Event Grid MQTT) | Unified-Namespace topic tree rooted under `traffic/es/madrid/informo/...` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-madrid-traffic-amqp` | AMQP 1.0 brokers incl. Azure Service Bus / Event Hubs | Binary CloudEvents to AMQP address `madrid-traffic` |

All variants share:

- The same xRegistry contract (`xreg/madrid_traffic.xreg.json`).
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
madrid-traffic/
  xreg/madrid_traffic.xreg.json
  madrid_traffic/
  madrid_traffic_mqtt/
  madrid_traffic_amqp/
  madrid_traffic_producer/
  madrid_traffic_mqtt_producer/
  madrid_traffic_amqp_producer/
  kql/
  notebook/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS connectivity to the upstream API at `https://informo.madrid.es/informo/tmadrid/pm.xml`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.
- A writable host directory mounted at `/state` for persistent polling/dedupe state.

## Quick start with Docker

> [!IMPORTANT]
> This source is poll-based. Mount a host volume and set `STATE_FILE` so state survives container restarts.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/madrid-traffic.json \
  -e CONNECTION_STRING="<event-hubs-or-kafka-connection-string>" \
  ghcr.io/clemensv/real-time-sources-madrid-traffic:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/madrid-traffic.json \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-madrid-traffic-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/madrid-traffic.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/madrid-traffic' \
  ghcr.io/clemensv/real-time-sources-madrid-traffic-amqp:latest
```

## Configuration reference

The complete environment-variable matrix for Kafka, MQTT, and AMQP images (including authentication-mode differences and Azure deployment assumptions) is documented in [CONTAINER.md](CONTAINER.md).

## Data model

This source emits the following event families (see [EVENTS.md](EVENTS.md) for full schema-level detail):

- **es.madrid.informo** — 2 event type(s): es.madrid.informo.MeasurementPoint, es.madrid.informo.TrafficReading.

## Deploying into Microsoft Fabric

Madrid Traffic supports both Fabric hosting models via the source card on the [project portal](https://clemensv.github.io/real-time-sources/#madrid-traffic).

### Fabric Notebook feeder

Because this source is poll-based and ships a notebook asset (`notebook/`), you can run scheduled ingestion in-Fabric with:

`tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source madrid-traffic -Workspace <id> -ResourceGroup <azure-rg> -Location <azure-region>`

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#madrid-traffic/fabric-notebook)

### Fabric ACI feeder

For always-on execution, deploy a long-running Azure Container Instance feeder with:

`tools/deploy-fabric/deploy-fabric-aci.ps1 -Source madrid-traffic -Workspace <id> -ResourceGroup <azure-rg> -Location <azure-region>`

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#madrid-traffic/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source directory and have matching deploy buttons:

### MQTT — bring your own broker

Deploy MQTT against an existing MQTT 5.0 broker endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid MQTT broker

Deploy MQTT plus an Event Grid namespace broker and managed-identity role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

Deploy Kafka plus a new Event Hubs namespace and event hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-with-eventhub.json)

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Event Hubs/Fabric/Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Use [CONTAINER.md](CONTAINER.md) for full auth-mode and environment-variable details.
- Validate transport-specific routing and key templates against your downstream topology.
- Review upstream usage guidance at [Madrid Informo traffic sensor feed](https://informo.madrid.es/informo/tmadrid/pm.xml).
