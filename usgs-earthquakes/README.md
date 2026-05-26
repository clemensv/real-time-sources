# USGS Earthquakes feeder

This feeder turns USGS Earthquake Hazards Program feeds into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

USGS earthquake feeds are a core public signal for seismic monitoring, civil-protection dashboards, and risk models. This feeder provides a transport-agnostic CloudEvents contract so downstream systems can subscribe once and fan out to analytics, alerting, and archival pipelines.

## Overview

**USGS Earthquakes** ships three transport variants from one source bridge:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-usgs-earthquakes` | Apache Kafka 2.x compatible (Azure Event Hubs, Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic, JSON CloudEvents (binary mode) |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-usgs-earthquakes-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Fabric MQTT broker) | Unified-Namespace topic tree defined in `xreg/usgs_earthquakes.xreg.json` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-usgs-earthquakes-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, Artemis, Qpid Dispatch, Azure Service Bus / Event Hubs) | Single AMQP address, binary CloudEvents |

All three variants share the same source contract in `xreg/usgs_earthquakes.xreg.json`.

## Key features

- Poll-based feeder with checkpointed state to avoid duplicate publication across restarts.
- Kafka, MQTT, and AMQP transport variants that share one xRegistry event contract.
- CloudEvents output suitable for Event Hubs, Fabric Event Streams, or self-managed brokers.
- Reference/telemetry publishing behavior and schemas documented in [EVENTS.md](EVENTS.md).

## Repository layout

```text
usgs-earthquakes/
  xreg/usgs_earthquakes.xreg.json
  usgs_earthquakes/
  usgs_earthquakes_mqtt/
  usgs_earthquakes_amqp/
  usgs_earthquakes_producer/
  usgs_earthquakes_mqtt_producer/
  usgs_earthquakes_amqp_producer/
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
  -e USGS_EQ_LAST_POLLED_FILE=/state/usgs-earthquakes.json \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-usgs-earthquakes:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_EARTHQUAKES_LAST_POLLED_FILE=/state/usgs-earthquakes.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-usgs-earthquakes-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e USGS_EARTHQUAKES_LAST_POLLED_FILE=/state/usgs-earthquakes.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/usgs-earthquakes" \
  ghcr.io/clemensv/real-time-sources-usgs-earthquakes-amqp:latest
```

## Configuration reference

For full transport/auth matrices (Kafka, MQTT, AMQP), source-specific options, and deployment options, see [CONTAINER.md](CONTAINER.md).

## Upstream source

USGS Earthquake Hazards Program GeoJSON summary feeds.

## Data model

This feeder emits the following event families:

- **`Event`**

See [EVENTS.md](EVENTS.md) for field-level schemas, subject templates, and key mapping per transport.

## Deploying into Microsoft Fabric

Two hosting options are available for this poll-based source:

### Fabric Notebook feeder

The notebook under [`notebook/`](notebook/) runs the bridge on a Fabric schedule and resolves the Event Stream connection string at runtime via Fabric topology APIs.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#usgs-earthquakes/fabric-notebook)

### Fabric ACI feeder

A long-running Azure Container Instance hosts one of the three transport images and publishes to a Fabric Event Stream custom endpoint.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#usgs-earthquakes/fabric-aci)

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

Deploys the Kafka image and uses a provided connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploys Kafka plus a new Event Hubs namespace and hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-with-eventhub.json)

### AMQP — bring your own AMQP broker

Deploys the AMQP image against a provided AMQP broker endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-amqp.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for complete env-var matrices and auth-mode examples.
