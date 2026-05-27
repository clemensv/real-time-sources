<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="North America" width="64" height="48"><br>
<sub><b>North America</b></sub>
</td>
<td valign="middle">

# Nextbus

<sub>public transit arrivals · Kafka · MQTT · AMQP · <a href="https://www.umoiq.com/">upstream</a> · <a href="https://retro.umoiq.com/xmlFeedDocs/NextBusXMLFeed.pdf">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-4_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> North America — public transit arrivals

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#nextbus) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.umoiq.com/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the upstream Nextbus feed into a real-time CloudEvents stream over KAFKA / MQTT / AMQP.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.umoiq.com/>
- API / data documentation: <https://retro.umoiq.com/xmlFeedDocs/NextBusXMLFeed.pdf>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

Nextbus publishes operational real-time data that is useful across hazard and mobility analytics workflows, but each consumer otherwise has to build and operate its own source connector, transport adapter, and schema normalization.

This bridge provides one reusable feed for common scenarios:

- **Operations dashboards** — power near-real-time fleet, traffic, or incident views.
- **Streaming analytics** — ingest directly into Eventhouse, ADX, or a lakehouse pipeline.
- **Cross-source correlation** — join this stream with weather, hydrology, and public-safety feeds in this repository.
- **Alerting and automation** — trigger rules based on stable CloudEvents payloads and keys.
- **Research and reporting** — keep a reproducible event archive for retrospective analysis.

## Overview

**Nextbus** in this repository is a streaming bridge and ships in the transport variants below:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-nextbus` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Fabric Event Streams) | Topic(s): `nextbus`, key = `{agency_id}/{route_tag}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-nextbus-mqtt` | MQTT 5.0 broker (incl. Azure Event Grid MQTT and Fabric Real-Time Hub MQTT source) | Unified Namespace topic tree `transit/intl/nextbus/nextbus/{agency_id}/{route_tag}/{event_type}/{stop_or_vehicle_id}` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-nextbus-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch, Azure Service Bus/Event Hubs) | AMQP node `nextbus`, CloudEvents binary mode |

All variants share:

- The xRegistry contract (`xreg/nextbus.xreg.json`).
- A common upstream acquisition path and normalized event payloads.
- Stable CloudEvents subject/key identity derived from source-native identifiers.

## Key features

- Real-time source ingestion for **North America — public transit arrivals**.
- Contract-first CloudEvents output with JsonStructure schemas.
- Transport variants aligned to the same core event model.
- Deployment-ready container images for local, Azure, and Fabric-aligned topologies.

## Repository layout

```text
nextbus/
  xreg/                           # xRegistry contracts
  nextbus/
  nextbus_amqp/
  nextbus_amqp_producer/
  nextbus_mqtt/
  nextbus_mqtt_producer/
  nextbus_producer/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Network access to the upstream data endpoint(s).
- Network access to your target broker (Kafka, MQTT, or AMQP).

This source is handled as a streaming feeder in this batch; no notebook runtime section is included.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-nextbus:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-nextbus-mqtt:latest
```

Topics follow the contract templates in [EVENTS.md](EVENTS.md); primary template: `transit/intl/nextbus/nextbus/{agency_id}/{route_tag}/{event_type}/{stop_or_vehicle_id}`.

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/nextbus' \
  ghcr.io/clemensv/real-time-sources-nextbus-amqp:latest
```

## Configuration reference

The complete environment-variable contract per image is documented in [CONTAINER.md](CONTAINER.md), including connection-string mode, direct broker parameters, authentication options, and transport-specific knobs.

## Data model

This source exposes **4 event type(s)** across **1 base message group(s)**:

- `nextbus.VehiclePosition`
- `nextbus.RouteConfig`
- `nextbus.Schedule`
- `nextbus.Message`

See [EVENTS.md](EVENTS.md) for the full field-level schema contract and routing metadata.

## Deploying into Microsoft Fabric

This source is documented as a streaming feeder for this rollout. Use the **Fabric ACI feeder** model to host the container and route into a Fabric Event Stream custom endpoint, then materialize into Eventhouse with the checked-in KQL assets.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#nextbus/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source folder:

- **azure-template-mqtt.json** (mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-mqtt.json)
- **azure-template-with-eventgrid-mqtt.json** (with eventgrid mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-eventgrid-mqtt.json)
- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full env-var matrix and auth variants.
- Choose Fabric ACI or direct Azure deployment based on your runtime target.
