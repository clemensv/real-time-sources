# US CBP Border Wait feeder

This feeder turns US CBP Border Wait Time API into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://bwt.cbp.gov/>
- API / data documentation: <https://bwt.cbp.gov/api/bwtnew>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

Cross-border logistics operators, customs-broker tools, travel apps, and public-sector planning teams use border wait telemetry for routing, staffing, and delay forecasting. This bridge standardizes polling, normalization, dedupe, CloudEvents shaping, and transport delivery so consumers subscribe once and reuse the same contract across platforms.

- **Traffic and mobility operations** — live dashboards and operational control-room views.
- **Route and dispatch optimization** — dynamic rerouting and ETA management under disruptions.
- **Analytics and planning** — long-running ingestion into Fabric Eventhouse / ADX / lakes.
- **Compliance and reporting** — auditable event history for public-sector and regulated workflows.
- **Cross-domain correlation** — fuse mobility events with weather, safety, and infrastructure feeds.

## Overview

**US CBP Border Wait** is a poll-based bridge that ingests upstream data from [US CBP Border Wait Time API](https://bwt.cbp.gov/) and re-emits normalized CloudEvents.

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-cbp-border-wait` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | JSON CloudEvents (binary mode), key templates `{port_number}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-cbp-border-wait-mqtt` | MQTT 5.0 broker (incl. Azure Event Grid MQTT) | Unified-Namespace topic tree rooted under `mobility/us/cbp/border-wait/...` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-cbp-border-wait-amqp` | AMQP 1.0 brokers incl. Azure Service Bus / Event Hubs | Binary CloudEvents to AMQP address `cbp-border-wait` |

All variants share:

- The same xRegistry contract (`xreg/cbp_border_wait.xreg.json`).
- The same event-family model and schema set.
- Poll-based acquisition logic with periodic refresh cycles.

## Key features

- Poll-based bridge with CloudEvents-first contract design.
- Shared event contract across Kafka, MQTT, and AMQP transports.
- Fabric-ready deployment path (Notebook and ACI hosting options).
- ARM templates for direct Azure Container Instance deployment targets.
- Source-specific event families and stable domain key templates.

## Repository layout

```text
cbp-border-wait/
  xreg/cbp_border_wait.xreg.json
  cbp_border_wait/
  cbp_border_wait_mqtt/
  cbp_border_wait_amqp/
  cbp_border_wait_producer/
  cbp_border_wait_mqtt_producer/
  cbp_border_wait_amqp_producer/
  kql/
  notebook/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS connectivity to the upstream API at `https://bwt.cbp.gov/`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.
- A writable host directory mounted at `/state` for persistent polling/dedupe state.

## Quick start with Docker

> [!IMPORTANT]
> This source is poll-based. Mount a host volume and set `STATE_FILE` so state survives container restarts.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/cbp-border-wait.json \
  -e CONNECTION_STRING="<event-hubs-or-kafka-connection-string>" \
  ghcr.io/clemensv/real-time-sources-cbp-border-wait:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/cbp-border-wait.json \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-cbp-border-wait-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/cbp-border-wait.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/cbp-border-wait' \
  ghcr.io/clemensv/real-time-sources-cbp-border-wait-amqp:latest
```

## Configuration reference

The complete environment-variable matrix for Kafka, MQTT, and AMQP images (including authentication-mode differences and Azure deployment assumptions) is documented in [CONTAINER.md](CONTAINER.md).

## Data model

This source emits the following event families (see [EVENTS.md](EVENTS.md) for full schema-level detail):

- **gov.cbp.borderwait** — 2 event type(s): gov.cbp.borderwait.Port, gov.cbp.borderwait.WaitTime.

## Deploying into Microsoft Fabric

US CBP Border Wait supports both Fabric hosting models via the source card on the [project portal](https://clemensv.github.io/real-time-sources/#cbp-border-wait).

### Fabric Notebook feeder

Because this source is poll-based and ships a notebook asset (`notebook/`), you can run scheduled ingestion in-Fabric with:

`tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source cbp-border-wait -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>`

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#cbp-border-wait/fabric-notebook)

### Fabric ACI feeder

For always-on execution, deploy a long-running Azure Container Instance feeder with:

`tools/deploy-fabric/deploy-fabric-aci.ps1 -Source cbp-border-wait -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>`

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#cbp-border-wait/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source directory and have matching deploy buttons:

### Kafka — provision a new Event Hub

Deploy Kafka plus a new Event Hubs namespace and event hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

Deploy AMQP plus Service Bus and managed-identity sender permissions.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Event Hubs/Fabric/Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Use [CONTAINER.md](CONTAINER.md) for full auth-mode and environment-variable details.
- Validate transport-specific routing and key templates against your downstream topology.
- Review upstream usage guidance at [US CBP Border Wait Time API](https://bwt.cbp.gov/).
