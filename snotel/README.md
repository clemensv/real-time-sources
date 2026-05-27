<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="Western US & Alaska" width="64" height="48"><br>
<sub><b>Western US & Alaska</b></sub>
</td>
<td valign="middle">

# SNOTEL Snow

<sub>~900 snowpack stations, NRCS · Kafka · MQTT · AMQP · <a href="https://www.nrcs.usda.gov/wps/portal/wcc/home/">upstream</a> · <a href="https://wcc.sc.egov.usda.gov/awdbRestWebService/swagger-ui/index.html">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Western US & Alaska — ~900 snowpack stations, NRCS

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#snotel) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#snotel/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/snotel.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.nrcs.usda.gov/wps/portal/wcc/home/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the upstream SNOTEL Snow hydrology feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.nrcs.usda.gov/wps/portal/wcc/home/>
- API / data documentation: <https://wcc.sc.egov.usda.gov/awdbRestWebService/swagger-ui/index.html>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

This bridge publishes the SNOTEL Snow source as a transport-agnostic event stream so downstream systems subscribe once and avoid re-implementing poll scheduling, retry handling, dedupe state, CloudEvents mapping, and schema lifecycle management.

- **Flood and water-risk operations** — power near-real-time threshold monitoring and alert pipelines.
- **Infrastructure operations** — feed lock/port/river-management dashboards and operations centers.
- **Environmental analytics** — ingest standardized events into Fabric Eventhouse, ADX, or lakehouse systems.
- **Insurance and resilience workflows** — drive trigger-based monitoring and post-event replay analysis.
- **Research and public-data products** — maintain reproducible timelines without source-specific ETL glue.

## Overview

**SNOTEL Snow** is a poll-based bridge that emits CloudEvents across available transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-snotel` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | JSON CloudEvents on one topic, key = `{station_triplet}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-snotel-mqtt` | MQTT 5.0 broker (incl. Event Grid MQTT and Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic template `(see EVENTS.md)` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-snotel-amqp` | AMQP 1.0 (incl. Service Bus and Event Hubs via CBS auth) | Binary CloudEvents to AMQP node `snotel` |

All variants share:

- The same upstream polling logic and dedupe state model.
- The same xRegistry contract (`xreg/snotel.xreg.json`).
- The same CloudEvents event families described in [EVENTS.md](EVENTS.md).

## Key features

- Poll-based ingestion with restart-safe dedupe/checkpoint persistence via `STATE_FILE`.
- Consistent CloudEvents identities and schemas across transport variants.
- Contract-first event modeling from the checked-in xRegistry manifest.
- Deployment options for local Docker, Microsoft Fabric, and Azure Container Instances.
- Reference and telemetry event families aligned for downstream joins and enrichment.

## Repository layout

```text
snotel/
  xreg/snotel.xreg.json                 # shared xRegistry contract
  snotel/
  snotel_amqp/
  snotel_amqp_producer/
  snotel_mqtt/
  snotel_mqtt_producer/
  snotel_producer/
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
  -e STATE_FILE=/state/snotel.json \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-snotel:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/snotel.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-snotel-mqtt:latest
```

Topic template:

```text
(see EVENTS.md)
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/snotel.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/snotel" \
  ghcr.io/clemensv/real-time-sources-snotel-amqp:latest
```

For Entra-ID and SAS-CBS AMQP authentication variants, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image).

## Configuration reference

The complete environment-variable matrix for each image is documented in [CONTAINER.md](CONTAINER.md). Runtime entry points come from image `CMD`: Kafka ["python", "-m", "snotel", "feed"] MQTT ["python", "-m", "snotel_mqtt", "feed"] AMQP ["python", "-m", "snotel_amqp", "feed"].

## Data model

This feeder emits the following event families:

- **gov.usda.nrcs.snotel** — `Station`, `SnowObservation`.

Event field descriptions, schema references, and routing details are documented in [EVENTS.md](EVENTS.md).

## Deploying into Microsoft Fabric

SNOTEL Snow supports both Fabric hosting patterns used in this repository.

### Fabric Notebook feeder

This source includes a notebook feeder under [`notebook/`](notebook/) and `catalog.json` marks `notebook: true`.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#snotel/fabric-notebook)

### Fabric ACI feeder

Use the ACI deployment flow for always-on container execution into a Fabric Event Stream custom endpoint.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#snotel/fabric-aci)

## Deploying into Azure Container Instances

Azure templates shipped with this source:

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before onboarding consumers.
- Use [CONTAINER.md](CONTAINER.md) for full per-image auth and environment settings.
- Select Fabric Notebook/Fabric ACI/Azure ACI based on your runtime and operational requirements.
