<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/jp.png" alt="Japan" width="64" height="48"><br>
<sub><b>Japan</b></sub>
</td>
<td valign="middle">

# JMA Bosai Quake

<sub>JMA earthquake bulletins (hypocenter, magnitude, JMA intensity) · Kafka · MQTT · AMQP · <a href="https://www.jma.go.jp/bosai/map.html?contents=earthquake_map">upstream</a> · <a href="https://www.jma.go.jp/bosai/quake/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-4_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Japan — JMA earthquake bulletins (hypocenter, magnitude, JMA intensity)

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#jma-bosai-quake) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#jma-bosai-quake/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/jma-bosai-quake.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.jma.go.jp/bosai/map.html?contents=earthquake_map)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns JMA Bosai earthquake and seismic-intensity feeds into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.jma.go.jp/bosai/map.html?contents=earthquake_map>
- API / data documentation: <https://www.jma.go.jp/bosai/quake/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

JMA earthquake and intensity publications are critical for situational awareness and downstream analytics. This feeder exposes them as CloudEvents across three transports so subscribers can integrate without managing JMA feed polling and state logic directly.

## Overview

**JMA Bosai Quake** ships three transport variants from one source bridge:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-jma-bosai-quake` | Apache Kafka 2.x compatible (Azure Event Hubs, Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic, JSON CloudEvents (binary mode) |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-jma-bosai-quake-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Fabric MQTT broker) | Unified-Namespace topic tree defined in `xreg/jma-bosai-quake.xreg.json` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-jma-bosai-quake-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, Artemis, Qpid Dispatch, Azure Service Bus / Event Hubs) | Single AMQP address, binary CloudEvents |

All three variants share the same source contract in `xreg/jma-bosai-quake.xreg.json`.

## Key features

- Poll-based feeder with checkpointed state to avoid duplicate publication across restarts.
- Kafka, MQTT, and AMQP transport variants that share one xRegistry event contract.
- CloudEvents output suitable for Event Hubs, Fabric Event Streams, or self-managed brokers.
- Reference/telemetry publishing behavior and schemas documented in [EVENTS.md](EVENTS.md).

## Repository layout

```text
jma-bosai-quake/
  xreg/jma-bosai-quake.xreg.json
  jma_bosai_quake/
  jma_bosai_quake_mqtt/
  jma_bosai_quake_amqp/
  jma_bosai_quake_producer/
  jma_bosai_quake_mqtt_producer/
  jma_bosai_quake_amqp_producer/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
  notebook/
  tests/
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS access to the upstream source APIs.
- Network access to your target Kafka broker, MQTT broker, or AMQP endpoint.
- A writable host directory mounted to persist the source state file across restarts.

## Quick start with Docker

> [!IMPORTANT]
> Mount a writable host volume for state persistence. Without it, dedupe/checkpoint state resets on every restart.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/jma-bosai-quake.json \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-jma-bosai-quake:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e JMA_BOSAI_QUAKE_MQTT_STATE_FILE=/state/jma-bosai-quake.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-jma-bosai-quake-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e JMA_BOSAI_QUAKE_AMQP_STATE_FILE=/state/jma-bosai-quake.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/jma-bosai-quake" \
  ghcr.io/clemensv/real-time-sources-jma-bosai-quake-amqp:latest
```

## Configuration reference

For full transport/auth matrices (Kafka, MQTT, AMQP), source-specific options, and deployment options, see [CONTAINER.md](CONTAINER.md).

## Upstream source

Japan Meteorological Agency Bosai earthquake and seismic-intensity feeds.

## Data model

This feeder emits the following event families:

- **`EarthquakeReport`**

See [EVENTS.md](EVENTS.md) for field-level schemas, subject templates, and key mapping per transport.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

JMA Bosai Quake targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#jma-bosai-quake) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `jma_bosai_quake` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/jma-bosai-quake/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source jma-bosai-quake `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#jma-bosai-quake/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source jma-bosai-quake `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#jma-bosai-quake/fabric-aci)


### Deploying into Azure Container Instances

4 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fjma-bosai-quake%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fjma-bosai-quake%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fjma-bosai-quake%2Fazure-template-with-servicebus.json)

#### AMQP — bring your own AMQP 1.0 peer

Deploy the AMQP container against an existing AMQP 1.0 peer (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs). You pass the broker URL and credentials; the template provisions only the container.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fjma-bosai-quake%2Fazure-template-amqp.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Review [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for complete env-var matrices and auth-mode examples.
