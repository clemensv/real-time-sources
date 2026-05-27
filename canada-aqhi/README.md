<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/ca.png" alt="Canada" width="64" height="48"><br>
<sub><b>Canada</b></sub>
</td>
<td valign="middle">

# Canada AQHI

<sub>community AQHI observations and forecasts · Kafka · MQTT · AMQP · <a href="https://weather.gc.ca/airquality/pages/index_e.html">upstream</a> · <a href="https://eccc-msc.github.io/open-data/msc-datamart/readme_en/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Canada — community AQHI observations and forecasts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#canada-aqhi) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#canada-aqhi/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/canada-aqhi.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://weather.gc.ca/airquality/pages/index_e.html)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the upstream Canada AQHI air-quality feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://weather.gc.ca/airquality/pages/index_e.html>
- API / data documentation: <https://eccc-msc.github.io/open-data/msc-datamart/readme_en/>

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
| **Kafka** | `ghcr.io/clemensv/real-time-sources-canada-aqhi` | Apache Kafka 2.x compatible (including Azure Event Hubs and Microsoft Fabric Event Streams) | One topic with CloudEvents JSON and xRegistry-defined keying |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-canada-aqhi-mqtt` | MQTT 5.0 broker (including Azure Event Grid MQTT namespace) | Unified-Namespace-style topic publishing with CloudEvents metadata as MQTT user properties |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-canada-aqhi-amqp` | AMQP 1.0 brokers (generic + Azure Service Bus / Event Hubs) | Single AMQP node/address with binary CloudEvents |

All variants share:

- The same upstream poller semantics and dedupe model.
- The same xRegistry contract in `xreg/canada-aqhi.xreg.json`.
- The same event families in [EVENTS.md](EVENTS.md).

## Key features

- Poll-based ingestion with stateful resume across restarts.
- One contract, three transport options (Kafka, MQTT, AMQP).
- CloudEvents-compatible envelope and schema metadata.
- Azure-ready deployment options (Fabric, Event Hubs, Service Bus, Event Grid MQTT).

## Repository layout

```text
canada-aqhi/
  xreg/canada-aqhi.xreg.json                # shared xRegistry contract
  canada_aqhi/                        # Kafka feeder application
  canada_aqhi_mqtt/                        # MQTT/UNS feeder application
  canada_aqhi_amqp/                        # AMQP 1.0 feeder application
  canada_aqhi_producer/               # xRegistry-generated Kafka producer
  canada_aqhi_mqtt_producer/               # xRegistry-generated MQTT producer
  canada_aqhi_amqp_producer/               # xRegistry-generated AMQP producer
  Dockerfile                      # builds the Kafka feeder image
  Dockerfile.mqtt                 # builds the MQTT feeder image
  Dockerfile.amqp                 # builds the AMQP feeder image
  kql/                            # Eventhouse / KQL schema and update policies
  notebook/                       # Fabric notebook feeder
  tests/                          # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or another OCI-compatible runtime).
- Outbound network access to the upstream Canada AQHI endpoints.
- Network access to your target Kafka/MQTT/AMQP broker.
- A writable host folder mounted to `/state` for persistent `STATE_FILE`.

## Quick start with Docker

> [!IMPORTANT]
> Mount a host volume for `STATE_FILE` so poller resume/dedupe state survives container restarts.

### Kafka

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/canada-aqhi.json   -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>"   ghcr.io/clemensv/real-time-sources-canada-aqhi:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/canada-aqhi.json   -e MQTT_BROKER_URL="mqtts://<broker-host>:8883"   -e MQTT_USERNAME="<username>"   -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-canada-aqhi-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/canada-aqhi.json   -e AMQP_BROKER_URL="amqp://<user>:<password>@<host>:5672/canada-aqhi"   ghcr.io/clemensv/real-time-sources-canada-aqhi-amqp:latest
```

## Configuration reference

See [CONTAINER.md](CONTAINER.md) for the full per-image environment-variable matrix and all supported auth modes (Kafka SASL/Event Hubs, MQTT password/Entra, AMQP password/Entra-CBS/SAS-CBS).

## Data model

This source emits the following event types:

- **`Community`**
- **`Observation`**
- **`Forecast`**

Kafka key template `{province}/{community_name}`

## Deploying into Microsoft Fabric

Two Fabric hosting models are supported for this poll-based source:

- **Fabric Notebook feeder** — scheduled runs inside Fabric, best for periodic polling workloads.
- **Fabric ACI feeder** — continuously running container feeder for always-on delivery.

### Fabric Notebook feeder

This source ships a notebook feeder in [`notebook/`](notebook/) for scheduled in-workspace execution. It runs the same poller logic, resolves the Event Stream custom-endpoint connection string at runtime, and stores run diagnostics in OneLake.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#canada-aqhi/fabric-notebook)

### Fabric ACI feeder

Deploy the container feeder directly into Azure Container Instances with Fabric Event Stream and Eventhouse wiring.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#canada-aqhi/fabric-aci)

## Deploying into Azure Container Instances

Use the ARM templates that ship with this source:

### AMQP — deploy the AMQP image against an existing AMQP 1.0 endpoint you configure.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-amqp.json)

### MQTT — bring your own MQTT 5.0 broker and deploy the MQTT image.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-mqtt.json)

### MQTT — provision an Azure Event Grid namespace MQTT broker plus required identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Azure Event Hubs namespace + event hub and wire the feeder automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace with managed identity + sender role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hubs / Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template.json)

## Next steps

- Choose a hosting model (Fabric Notebook, Fabric ACI, or direct Azure template deployment).
- Review [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for full auth-mode and environment-variable details.
