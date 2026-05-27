<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/eu.png" alt="Europe" width="64" height="48"><br>
<sub><b>Europe</b></sub>
</td>
<td valign="middle">

# EURDEP Radiation

<sub>~5,500 stations, 39 countries, gamma dose · Kafka · MQTT · AMQP · <a href="https://remon.jrc.ec.europa.eu/">upstream</a> · <a href="https://eurdep.jrc.ec.europa.eu/Basic/Pages/Public/Data/Default.aspx">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Europe — ~5,500 stations, 39 countries, gamma dose

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#eurdep-radiation) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#eurdep-radiation/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/eurdep_radiation.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://remon.jrc.ec.europa.eu/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns EURDEP radiation monitoring data into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://remon.jrc.ec.europa.eu/>
- API / data documentation: <https://eurdep.jrc.ec.europa.eu/Basic/Pages/Public/Data/Default.aspx>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

EURDEP provides cross-country radiation measurements used for monitoring, preparedness, and compliance workflows. This feeder emits the data as CloudEvents so consumers can subscribe through their preferred transport without custom polling and normalization logic.

## Overview

**EURDEP Radiation** ships three transport variants from one source bridge:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-eurdep-radiation` | Apache Kafka 2.x compatible (Azure Event Hubs, Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic, JSON CloudEvents (binary mode) |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-eurdep-radiation-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Fabric MQTT broker) | Unified-Namespace topic tree defined in `xreg/eurdep_radiation.xreg.json` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-eurdep-radiation-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, Artemis, Qpid Dispatch, Azure Service Bus / Event Hubs) | Single AMQP address, binary CloudEvents |

All three variants share the same source contract in `xreg/eurdep_radiation.xreg.json`.

## Key features

- Poll-based feeder with checkpointed state to avoid duplicate publication across restarts.
- Kafka, MQTT, and AMQP transport variants that share one xRegistry event contract.
- CloudEvents output suitable for Event Hubs, Fabric Event Streams, or self-managed brokers.
- Reference/telemetry publishing behavior and schemas documented in [EVENTS.md](EVENTS.md).

## Repository layout

```text
eurdep-radiation/
  xreg/eurdep_radiation.xreg.json
  eurdep_radiation/
  eurdep_radiation_mqtt/
  eurdep_radiation_amqp/
  eurdep_radiation_producer/
  eurdep_radiation_mqtt_producer/
  eurdep_radiation_amqp_producer/
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
  -e STATE_FILE=/state/eurdep-radiation.json \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-eurdep-radiation:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/eurdep-radiation.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-eurdep-radiation-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/eurdep-radiation.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/eurdep-radiation" \
  ghcr.io/clemensv/real-time-sources-eurdep-radiation-amqp:latest
```

## Configuration reference

For full transport/auth matrices (Kafka, MQTT, AMQP), source-specific options, and deployment options, see [CONTAINER.md](CONTAINER.md).

## Upstream source

EURDEP public radiation monitoring endpoints.

## Data model

This feeder emits the following event families:

- **`Station`**
- **`DoseRateReading`**

See [EVENTS.md](EVENTS.md) for field-level schemas, subject templates, and key mapping per transport.

## Deploying into Microsoft Fabric

Two hosting options are available for this poll-based source:

### Fabric Notebook feeder

The notebook under [`notebook/`](notebook/) runs the bridge on a Fabric schedule and resolves the Event Stream connection string at runtime via Fabric topology APIs.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#eurdep-radiation/fabric-notebook)

### Fabric ACI feeder

A long-running Azure Container Instance hosts one of the three transport images and publishes to a Fabric Event Stream custom endpoint.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#eurdep-radiation/fabric-aci)

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

Deploys the Kafka image and uses a provided connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploys Kafka plus a new Event Hubs namespace and hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

Deploys the MQTT image against an existing MQTT 5 broker.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-mqtt.json)

### MQTT — provision Event Grid MQTT broker

Deploys MQTT plus a new Event Grid namespace broker and identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision Azure Service Bus

Deploys AMQP plus a new Service Bus namespace/queue and sender identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-servicebus.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for complete env-var matrices and auth-mode examples.
