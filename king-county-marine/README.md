<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="Washington State / Puget Sound" width="64" height="48"><br>
<sub><b>Washington State / Puget Sound</b></sub>
</td>
<td valign="middle">

# King County Marine

<sub>buoy and mooring telemetry · Kafka · MQTT · AMQP · <a href="https://green2.kingcounty.gov/marine/">upstream</a> · <a href="https://data.kingcounty.gov/Environment-Waste-Management/Marine-Buoy-Data/9j7t-rs5d">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Washington State / Puget Sound — buoy and mooring telemetry

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#king-county-marine) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#king-county-marine/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/king_county_marine.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://green2.kingcounty.gov/marine/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the upstream King County Marine hydrology feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://green2.kingcounty.gov/marine/>
- API / data documentation: <https://data.kingcounty.gov/Environment-Waste-Management/Marine-Buoy-Data/9j7t-rs5d>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

This bridge publishes the King County Marine source as a transport-agnostic event stream so downstream systems subscribe once and avoid re-implementing poll scheduling, retry handling, dedupe state, CloudEvents mapping, and schema lifecycle management.

- **Flood and water-risk operations** — power near-real-time threshold monitoring and alert pipelines.
- **Infrastructure operations** — feed lock/port/river-management dashboards and operations centers.
- **Environmental analytics** — ingest standardized events into Fabric Eventhouse, ADX, or lakehouse systems.
- **Insurance and resilience workflows** — drive trigger-based monitoring and post-event replay analysis.
- **Research and public-data products** — maintain reproducible timelines without source-specific ETL glue.

## Overview

**King County Marine** is a poll-based bridge that emits CloudEvents across available transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-king-county-marine` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | JSON CloudEvents on one topic, key = `{station_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources/king-county-marine-mqtt` | MQTT 5.0 broker (incl. Event Grid MQTT and Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic template `(see EVENTS.md)` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-king-county-marine-amqp` | AMQP 1.0 (incl. Service Bus and Event Hubs via CBS auth) | Binary CloudEvents to AMQP node `king-county-marine` |

All variants share:

- The same upstream polling logic and dedupe state model.
- The same xRegistry contract (`xreg/king_county_marine.xreg.json`).
- The same CloudEvents event families described in [EVENTS.md](EVENTS.md).

## Key features

- Poll-based ingestion with restart-safe dedupe/checkpoint persistence via `KING_COUNTY_MARINE_STATE_FILE`.
- Consistent CloudEvents identities and schemas across transport variants.
- Contract-first event modeling from the checked-in xRegistry manifest.
- Deployment options for local Docker, Microsoft Fabric, and Azure Container Instances.
- Reference and telemetry event families aligned for downstream joins and enrichment.

## Repository layout

```text
king-county-marine/
  xreg/king_county_marine.xreg.json                 # shared xRegistry contract
  king_county_marine/
  king_county_marine_amqp/
  king_county_marine_amqp_producer/
  king_county_marine_mqtt/
  king_county_marine_mqtt_producer/
  king_county_marine_producer/
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
- A writable host directory mounted to persist `KING_COUNTY_MARINE_STATE_FILE` across container restarts.

## Quick start with Docker

> [!IMPORTANT]
> Mount a host volume for `KING_COUNTY_MARINE_STATE_FILE` so dedupe/checkpoint state survives restarts.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-king-county-marine:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources/king-county-marine-mqtt:latest
```

Topic template:

```text
(see EVENTS.md)
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/king-county-marine" \
  ghcr.io/clemensv/real-time-sources-king-county-marine-amqp:latest
```

For Entra-ID and SAS-CBS AMQP authentication variants, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image).

## Configuration reference

The complete environment-variable matrix for each image is documented in [CONTAINER.md](CONTAINER.md). Runtime entry points come from image `CMD`: Kafka ["python", "-m", "king_county_marine"] MQTT ["python", "-m", "king_county_marine_mqtt", "feed"] AMQP ["python", "-m", "king_county_marine_amqp", "feed"].

## Data model

This feeder emits the following event families:

- **US.WA.KingCounty.Marine** — `Station`, `WaterQualityReading`.

Event field descriptions, schema references, and routing details are documented in [EVENTS.md](EVENTS.md).

## Deploying into Microsoft Fabric

King County Marine supports both Fabric hosting patterns used in this repository.

### Fabric Notebook feeder

This source includes a notebook feeder under [`notebook/`](notebook/) and `catalog.json` marks `notebook: true`.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#king-county-marine/fabric-notebook)

### Fabric ACI feeder

Use the ACI deployment flow for always-on container execution into a Fabric Event Stream custom endpoint.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#king-county-marine/fabric-aci)

## Deploying into Azure Container Instances

Azure templates shipped with this source:

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before onboarding consumers.
- Use [CONTAINER.md](CONTAINER.md) for full per-image auth and environment settings.
- Select Fabric Notebook/Fabric ACI/Azure ACI based on your runtime and operational requirements.
