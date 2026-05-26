# NINA/BBK feeder

This feeder turns the upstream NINA/BBK feed into a real-time CloudEvents stream over KAFKA / MQTT / AMQP.

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

NINA/BBK publishes operational real-time data that is useful across hazard and mobility analytics workflows, but each consumer otherwise has to build and operate its own source connector, transport adapter, and schema normalization.

This bridge provides one reusable feed for common scenarios:

- **Operations dashboards** — power near-real-time fleet, traffic, or incident views.
- **Streaming analytics** — ingest directly into Eventhouse, ADX, or a lakehouse pipeline.
- **Cross-source correlation** — join this stream with weather, hydrology, and public-safety feeds in this repository.
- **Alerting and automation** — trigger rules based on stable CloudEvents payloads and keys.
- **Research and reporting** — keep a reproducible event archive for retrospective analysis.

## Overview

**NINA/BBK** in this repository is a streaming bridge and ships in the transport variants below:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-nina-bbk` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Fabric Event Streams) | Topic(s): `nina-bbk`, key = `{warning_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-nina-bbk-mqtt` | MQTT 5.0 broker (incl. Azure Event Grid MQTT and Fabric Real-Time Hub MQTT source) | Unified Namespace topic tree `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-nina-bbk-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch, Azure Service Bus/Event Hubs) | AMQP node `nina-bbk`, CloudEvents binary mode |

All variants share:

- The xRegistry contract (`xreg/nina_bbk.xreg.json`).
- A common upstream acquisition path and normalized event payloads.
- Stable CloudEvents subject/key identity derived from source-native identifiers.

## Key features

- Real-time source ingestion for **Germany — MOWAS, KATWARN, BIWAPP, DWD, LHP, Police**.
- Contract-first CloudEvents output with JsonStructure schemas.
- Transport variants aligned to the same core event model.
- Deployment-ready container images for local, Azure, and Fabric-aligned topologies.

## Repository layout

```text
nina-bbk/
  xreg/                           # xRegistry contracts
  kql/
  nina_bbk/
  nina_bbk_amqp/
  nina_bbk_amqp_producer/
  nina_bbk_mqtt/
  nina_bbk_mqtt_producer/
  nina_bbk_producer/
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
  ghcr.io/clemensv/real-time-sources-nina-bbk:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-nina-bbk-mqtt:latest
```

Topics follow the contract templates in [EVENTS.md](EVENTS.md); primary template: `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning`.

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/nina-bbk' \
  ghcr.io/clemensv/real-time-sources-nina-bbk-amqp:latest
```

## Configuration reference

The complete environment-variable contract per image is documented in [CONTAINER.md](CONTAINER.md), including connection-string mode, direct broker parameters, authentication options, and transport-specific knobs.

## Data model

This source exposes **1 event type(s)** across **1 base message group(s)**:

- `NINA.CivilWarning`

See [EVENTS.md](EVENTS.md) for the full field-level schema contract and routing metadata.

## Deploying into Microsoft Fabric

This source is documented as a streaming feeder for this rollout. Use the **Fabric ACI feeder** model to host the container and route into a Fabric Event Stream custom endpoint, then materialize into Eventhouse with the checked-in KQL assets.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#nina-bbk/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source folder:

- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-with-eventhub.json)
- **azure-template-with-servicebus.json** (with servicebus)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-with-servicebus.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full env-var matrix and auth variants.
- Choose Fabric ACI or direct Azure deployment based on your runtime target.
