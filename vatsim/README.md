# VATSIM feeder

This feeder turns VATSIM network snapshots into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.vatsim.net/>
- API / data documentation: <https://data.vatsim.net/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

VATSIM network data is useful for aviation simulation analytics, traffic visualization, and research. This feeder normalizes live VATSIM updates into CloudEvents so consumers can build streaming applications without bespoke ingest logic.

## Overview

**VATSIM** ships three transport variants from one source bridge:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-vatsim` | Apache Kafka 2.x compatible (Azure Event Hubs, Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic, JSON CloudEvents (binary mode) |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-vatsim-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Fabric MQTT broker) | Unified-Namespace topic tree defined in `xreg/vatsim.xreg.json` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-vatsim-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, Artemis, Qpid Dispatch, Azure Service Bus / Event Hubs) | Single AMQP address, binary CloudEvents |

All three variants share the same source contract in `xreg/vatsim.xreg.json`.

## Key features

- Poll-based feeder with checkpointed state to avoid duplicate publication across restarts.
- Kafka, MQTT, and AMQP transport variants that share one xRegistry event contract.
- CloudEvents output suitable for Event Hubs, Fabric Event Streams, or self-managed brokers.
- Reference/telemetry publishing behavior and schemas documented in [EVENTS.md](EVENTS.md).

## Repository layout

```text
vatsim/
  xreg/vatsim.xreg.json
  vatsim/
  vatsim_mqtt/
  vatsim_amqp/
  vatsim_producer/
  vatsim_mqtt_producer/
  vatsim_amqp_producer/
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
  -e STATE_FILE=/state/vatsim.json \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-vatsim:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-vatsim-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/vatsim" \
  ghcr.io/clemensv/real-time-sources-vatsim-amqp:latest
```

## Configuration reference

For full transport/auth matrices (Kafka, MQTT, AMQP), source-specific options, and deployment options, see [CONTAINER.md](CONTAINER.md).

## Upstream source

VATSIM data feed API snapshots.

## Data model

This feeder emits the following event families:

- **`PilotPosition`**
- **`ControllerPosition`**
- **`NetworkStatus`**

See [EVENTS.md](EVENTS.md) for field-level schemas, subject templates, and key mapping per transport.

## Deploying into Microsoft Fabric

Two hosting options are available for this poll-based source:

### Fabric Notebook feeder

The notebook under [`notebook/`](notebook/) runs the bridge on a Fabric schedule and resolves the Event Stream connection string at runtime via Fabric topology APIs.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#vatsim/fabric-notebook)

### Fabric ACI feeder

A long-running Azure Container Instance hosts one of the three transport images and publishes to a Fabric Event Stream custom endpoint.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#vatsim/fabric-aci)

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

Deploys the Kafka image and uses a provided connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploys Kafka plus a new Event Hubs namespace and hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventhub.json)

### AMQP — provision Azure Service Bus

Deploys AMQP plus a new Service Bus namespace/queue and sender identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-servicebus.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for complete env-var matrices and auth-mode examples.
