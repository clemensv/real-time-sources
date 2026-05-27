<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/gb.png" alt="London" width="64" height="48"><br>
<sub><b>London</b></sub>
</td>
<td valign="middle">

# LAQN London

<sub>site metadata, species, hourly measurements · Kafka · MQTT · AMQP · <a href="https://www.londonair.org.uk/">upstream</a> · <a href="https://api.erg.ic.ac.uk/AirQuality/help">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> London, UK — site metadata, species, hourly measurements

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#laqn-london) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#laqn-london/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/laqn_london.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.londonair.org.uk/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the upstream LAQN London air-quality feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.londonair.org.uk/>
- API / data documentation: <https://api.erg.ic.ac.uk/AirQuality/help>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

The upstream source is open and operationally useful, but every downstream team otherwise has to rebuild polling, dedupe, schema normalization, retry handling, and transport-specific publishing. This bridge centralizes that work and republishes a stable CloudEvents contract for subscribers.

- **Public-health operations** — power near-real-time air-quality dashboards and incident triage for municipal, regional, or national teams.
- **Compliance and reporting** — persist normalized observations into Eventhouse / ADX / data lakes for regulatory and policy reporting.
- **Industrial and facility response** — trigger ventilation, activity restrictions, or maintenance workflows from threshold-based alerts.
- **Research and forecasting** — join air-quality observations with weather, mobility, and health indicators for modelling.
- **Citizen-information products** — feed apps, kiosks, and map tiles with a stable event contract instead of custom API pollers.

## Overview

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-laqn-london` | Apache Kafka 2.x compatible (including Azure Event Hubs and Microsoft Fabric Event Streams) | One topic with CloudEvents JSON and xRegistry-defined keying |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-laqn-london-mqtt` | MQTT 5.0 broker (including Azure Event Grid MQTT namespace) | Unified-Namespace-style topic publishing with CloudEvents metadata as MQTT user properties |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-laqn-london-amqp` | AMQP 1.0 brokers (generic + Azure Service Bus / Event Hubs) | Single AMQP node/address with binary CloudEvents |

All variants share:

- The same upstream poller semantics and dedupe model.
- The same xRegistry contract in `xreg/laqn_london.xreg.json`.
- The same event families in [EVENTS.md](EVENTS.md).

## Key features

- Poll-based ingestion with stateful resume across restarts.
- One contract, three transport options (Kafka, MQTT, AMQP).
- CloudEvents-compatible envelope and schema metadata.
- Azure-ready deployment options (Fabric, Event Hubs, Service Bus, Event Grid MQTT).

## Repository layout

```text
laqn-london/
  xreg/laqn_london.xreg.json                # shared xRegistry contract
  laqn_london/                        # Kafka feeder application
  laqn_london_mqtt/                        # MQTT/UNS feeder application
  laqn_london_amqp/                        # AMQP 1.0 feeder application
  laqn_london_producer/               # xRegistry-generated Kafka producer
  laqn_london_mqtt_producer/               # xRegistry-generated MQTT producer
  laqn_london_amqp_producer/               # xRegistry-generated AMQP producer
  Dockerfile                      # builds the Kafka feeder image
  Dockerfile.mqtt                 # builds the MQTT feeder image
  Dockerfile.amqp                 # builds the AMQP feeder image
  kql/                            # Eventhouse / KQL schema and update policies
  notebook/                       # Fabric notebook feeder
  tests/                          # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or another OCI-compatible runtime).
- Outbound network access to the upstream LAQN London endpoints.
- Network access to your target Kafka/MQTT/AMQP broker.
- A writable host folder mounted to `/state` for persistent `STATE_FILE`.

## Quick start with Docker

> [!IMPORTANT]
> Mount a host volume for `STATE_FILE` so poller resume/dedupe state survives container restarts.

### Kafka

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/laqn-london.json   -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>"   ghcr.io/clemensv/real-time-sources-laqn-london:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/laqn-london.json   -e MQTT_BROKER_URL="mqtts://<broker-host>:8883"   -e MQTT_USERNAME="<username>"   -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-laqn-london-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/laqn-london.json   -e AMQP_BROKER_URL="amqp://<user>:<password>@<host>:5672/laqn-london"   ghcr.io/clemensv/real-time-sources-laqn-london-amqp:latest
```

## Configuration reference

See [CONTAINER.md](CONTAINER.md) for the full per-image environment-variable matrix and all supported auth modes (Kafka SASL/Event Hubs, MQTT password/Entra, AMQP password/Entra-CBS/SAS-CBS).

## Data model

This source emits the following event types:

- **`Site`**
- **`Measurement`**
- **`DailyIndex`**
- **`Species`**

Kafka key template `{site_code}`; Kafka key template `{species_code}`

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

LAQN London targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#laqn-london) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `laqn_london` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/laqn-london/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source laqn-london `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#laqn-london/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source laqn-london `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#laqn-london/fabric-aci)


### Deploying into Azure Container Instances

6 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Flaqn-london%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Flaqn-london%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Flaqn-london%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Flaqn-london%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Flaqn-london%2Fazure-template-with-servicebus.json)

#### AMQP — bring your own AMQP 1.0 peer

Deploy the AMQP container against an existing AMQP 1.0 peer (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs). You pass the broker URL and credentials; the template provisions only the container.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Flaqn-london%2Fazure-template-amqp.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Choose a hosting model (Fabric Notebook, Fabric ACI, or direct Azure template deployment).
- Review [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for full auth-mode and environment-variable details.
