<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/be.png" alt="Belgium / Flanders" width="64" height="48"><br>
<sub><b>Belgium / Flanders</b></sub>
</td>
<td valign="middle">

# Waterinfo VMM

<sub>~1,785 stations · Kafka · MQTT · AMQP · <a href="https://www.waterinfo.be/">upstream</a> · <a href="https://www.waterinfo.be/default.aspx?path=NL/Rapporten/Downloaden">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Belgium / Flanders — ~1,785 stations

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#waterinfo-vmm) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#waterinfo-vmm/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/waterinfo_vmm.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.waterinfo.be/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the upstream Waterinfo VMM hydrology feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.waterinfo.be/>
- API / data documentation: <https://www.waterinfo.be/default.aspx?path=NL/Rapporten/Downloaden>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

This bridge publishes the Waterinfo VMM source as a transport-agnostic event stream so downstream systems subscribe once and avoid re-implementing poll scheduling, retry handling, dedupe state, CloudEvents mapping, and schema lifecycle management.

- **Flood and water-risk operations** — power near-real-time threshold monitoring and alert pipelines.
- **Infrastructure operations** — feed lock/port/river-management dashboards and operations centers.
- **Environmental analytics** — ingest standardized events into Fabric Eventhouse, ADX, or lakehouse systems.
- **Insurance and resilience workflows** — drive trigger-based monitoring and post-event replay analysis.
- **Research and public-data products** — maintain reproducible timelines without source-specific ETL glue.

## Overview

**Waterinfo VMM** is a poll-based bridge that emits CloudEvents across available transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-waterinfo-vmm` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | JSON CloudEvents on one topic, key = `{station_no}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-waterinfo-vmm-mqtt` | MQTT 5.0 broker (incl. Event Grid MQTT and Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic template `(see EVENTS.md)` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-waterinfo-vmm-amqp` | AMQP 1.0 (incl. Service Bus and Event Hubs via CBS auth) | Binary CloudEvents to AMQP node `waterinfo-vmm` |

All variants share:

- The same upstream polling logic and dedupe state model.
- The same xRegistry contract (`xreg/waterinfo_vmm.xreg.json`).
- The same CloudEvents event families described in [EVENTS.md](EVENTS.md).

## Key features

- Poll-based ingestion with restart-safe dedupe/checkpoint persistence via `STATE_FILE`.
- Consistent CloudEvents identities and schemas across transport variants.
- Contract-first event modeling from the checked-in xRegistry manifest.
- Deployment options for local Docker, Microsoft Fabric, and Azure Container Instances.
- Reference and telemetry event families aligned for downstream joins and enrichment.

## Repository layout

```text
waterinfo-vmm/
  xreg/waterinfo_vmm.xreg.json                 # shared xRegistry contract
  waterinfo_vmm/
  waterinfo_vmm_amqp/
  waterinfo_vmm_amqp_producer/
  waterinfo_vmm_mqtt/
  waterinfo_vmm_mqtt_producer/
  waterinfo_vmm_producer/
  Dockerfile                         # Kafka feeder image
  Dockerfile.mqtt                    # MQTT feeder image
  Dockerfile.amqp                    # AMQP feeder image
  kql/                               # KQL/Eventhouse schema
  notebook/                          # Fabric notebook feeder
  tests/                             # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or compatible OCI runtime).
- Outbound HTTPS access to the upstream source API.
- Network access to your Kafka broker / MQTT broker / AMQP 1.0 endpoint.
- A writable host directory mounted to persist `STATE_FILE` across container restarts.

## Quick start with Docker

> [!IMPORTANT]
> Mount a host volume for `STATE_FILE` so dedupe/checkpoint state survives restarts.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/waterinfo-vmm.json \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-waterinfo-vmm:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/waterinfo-vmm.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-waterinfo-vmm-mqtt:latest
```

Topic template:

```text
(see EVENTS.md)
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/waterinfo-vmm.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/waterinfo-vmm" \
  ghcr.io/clemensv/real-time-sources-waterinfo-vmm-amqp:latest
```

For Entra-ID and SAS-CBS AMQP authentication variants, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image).

## Configuration reference

The complete environment-variable matrix for each image is documented in [CONTAINER.md](CONTAINER.md). Runtime entry points come from image `CMD`: Kafka ["python", "-m", "waterinfo_vmm", "feed"] MQTT ["python", "-m", "waterinfo_vmm_mqtt", "feed"] AMQP ["python", "-m", "waterinfo_vmm_amqp", "feed"].

## Data model

This feeder emits the following event families:

- **BE.Vlaanderen.Waterinfo.VMM** — `Station`, `WaterLevelReading`.

Event field descriptions, schema references, and routing details are documented in [EVENTS.md](EVENTS.md).

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

Waterinfo VMM targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#waterinfo-vmm) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `waterinfo_vmm` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/waterinfo-vmm/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source waterinfo-vmm `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#waterinfo-vmm/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source waterinfo-vmm `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#waterinfo-vmm/fabric-aci)


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwaterinfo-vmm%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwaterinfo-vmm%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwaterinfo-vmm%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwaterinfo-vmm%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwaterinfo-vmm%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Review [EVENTS.md](EVENTS.md) before onboarding consumers.
- Use [CONTAINER.md](CONTAINER.md) for full per-image auth and environment settings.
- Select Fabric Notebook/Fabric ACI/Azure ACI based on your runtime and operational requirements.
