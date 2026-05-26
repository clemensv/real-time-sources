# LAQN London feeder

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

## Deploying into Microsoft Fabric

Two Fabric hosting models are supported for this poll-based source:

- **Fabric Notebook feeder** — scheduled runs inside Fabric, best for periodic polling workloads.
- **Fabric ACI feeder** — continuously running container feeder for always-on delivery.

### Fabric Notebook feeder

This source ships a notebook feeder in [`notebook/`](notebook/) for scheduled in-workspace execution. It runs the same poller logic, resolves the Event Stream custom-endpoint connection string at runtime, and stores run diagnostics in OneLake.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#laqn-london/fabric-notebook)

### Fabric ACI feeder

Deploy the container feeder directly into Azure Container Instances with Fabric Event Stream and Eventhouse wiring.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#laqn-london/fabric-aci)

## Deploying into Azure Container Instances

Use the ARM templates that ship with this source:

### AMQP — deploy the AMQP image against an existing AMQP 1.0 endpoint you configure.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-amqp.json)

### MQTT — bring your own MQTT 5.0 broker and deploy the MQTT image.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-mqtt.json)

### MQTT — provision an Azure Event Grid namespace MQTT broker plus required identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Azure Event Hubs namespace + event hub and wire the feeder automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace with managed identity + sender role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hubs / Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template.json)

## Next steps

- Choose a hosting model (Fabric Notebook, Fabric ACI, or direct Azure template deployment).
- Review [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for full auth-mode and environment-variable details.
