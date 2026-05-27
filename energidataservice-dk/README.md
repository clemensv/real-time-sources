<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/dk.png" alt="Denmark" width="64" height="48"><br>
<sub><b>Denmark</b></sub>
</td>
<td valign="middle">

# Energi Data Service

<sub>power system, spot prices, CO₂ · Kafka · MQTT · AMQP · <a href="https://www.energidataservice.dk/">upstream</a> · <a href="https://www.energidataservice.dk/guides/api-guides">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Denmark — power system, spot prices, CO₂

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#energidataservice-dk) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#energidataservice-dk/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/energidataservice_dk.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.energidataservice.dk/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the [Energi Data Service API](https://www.energidataservice.dk/) into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.energidataservice.dk/>
- API / data documentation: <https://www.energidataservice.dk/guides/api-guides>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published images, environment variables, and deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and routing details.

## Why this bridge

Energinet power snapshots and spot prices are core inputs for Danish grid operations, market monitoring, and forecasting. This feeder emits those records as CloudEvents.

Concrete consumer scenarios:

- **Operations dashboards** ingest the stream for near-real-time visibility without polling logic in every app.
- **Data engineering pipelines** land events in Eventhouse/Data Lake/Kafka topics with stable keys and schemas.
- **Alerting and automation** subscribe to the relevant event families and trigger downstream workflows.
- **Research and analytics teams** replay the same contract across historical and live windows.
- **Cross-domain correlation** joins these events with weather, traffic, or incident streams from sibling feeders.

## Overview

Polls PowerSystemRightNow and ElspotPrices datasets and emits deduplicated events.

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-energidataservice-dk` | Apache Kafka compatible (incl. Azure Event Hubs/Fabric Event Streams) | CloudEvents on one topic |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-energidataservice-dk-mqtt` | MQTT 5.0 broker | CloudEvents with xRegistry topic mapping |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-energidataservice-dk-amqp` | AMQP 1.0 broker / Service Bus | CloudEvents on one AMQP address |

All variants share:

- The same upstream acquisition logic and poll cadence.
- The same xRegistry contract and schema set.
- The same event identities and key/subject model across transports.

## Key features

- Shared contract and event schemas across Kafka, MQTT, and AMQP images.
- Container-first deployment model for Azure ACI and Fabric hosting.
- Dedupe/resume behavior for long-running ingestion.
- Source-specific event families are documented in [EVENTS.md](EVENTS.md).

## Repository layout

```text
energidataservice-dk/
  xreg/energidataservice_dk.xreg.json     # shared xRegistry contract
  energidataservice_dk/ # feeder runtime
  energidataservice_dk_amqp/ # AMQP feeder application
  energidataservice_dk_mqtt/ # MQTT feeder application
  energidataservice_dk_amqp_producer/ # generated producer package
  energidataservice_dk_mqtt_producer/ # generated producer package
  energidataservice_dk_producer/ # generated producer package
  kql/ # KQL schema scripts
  notebook/ # Fabric notebook feeder
  tests/ # unit + integration tests
  Dockerfile                # builds the Kafka feeder image
  Dockerfile.mqtt                # builds the MQTT feeder image
  Dockerfile.amqp                # builds the AMQP feeder image
```

## Prerequisites

- Docker 20.10+.
- Outbound HTTPS access to the upstream source.
- Network access to your Kafka, MQTT, or AMQP destination.
- A writable `/state` mount for stateful polling deployments.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e EDS_LAST_POLLED_FILE=/state/energidataservice-dk.json \
  -e CONNECTION_STRING="<event-hubs-or-kafka-connection-string>" \
  ghcr.io/clemensv/real-time-sources-energidataservice-dk:latest
```

### MQTT

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-energidataservice-dk-mqtt:latest
```

### AMQP

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/energidataservice-dk" \
  ghcr.io/clemensv/real-time-sources-energidataservice-dk-amqp:latest
```

## Configuration reference

Full per-transport environment-variable matrices live in [CONTAINER.md](CONTAINER.md).

State-file behavior: Kafka uses `EDS_LAST_POLLED_FILE`; MQTT companion app is stateless; AMQP companion app is stateless.

## Data model

- Power-system snapshot events
- Spot-price events

## Deploying into Microsoft Fabric

This source supports both Fabric-hosted deployment models.

### Fabric Notebook feeder

Use `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source energidataservice-dk ...` to schedule the poller in a Fabric notebook using the source notebook under [`notebook/`](notebook/).

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#energidataservice-dk/fabric-notebook)

### Fabric ACI feeder

Use `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source energidataservice-dk ...` to run the container continuously in Azure Container Instances with Fabric Event Stream / Eventhouse wiring.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#energidataservice-dk/fabric-aci)

## Deploying into Azure Container Instances

### AMQP — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-amqp.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template.json)

## Next steps
- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for complete environment-variable and auth-mode details.
- Mount persistent state storage in production.
