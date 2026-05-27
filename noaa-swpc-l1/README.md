<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# NOAA SWPC L1

<sub>L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time · Kafka · MQTT · AMQP · <a href="https://www.swpc.noaa.gov/">upstream</a> · <a href="https://services.swpc.noaa.gov/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#noaa-swpc-l1) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#noaa-swpc-l1/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/noaa_swpc_l1.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.swpc.noaa.gov/)

</td></tr></table>
<!-- source-hero:end -->

## Why this bridge

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.swpc.noaa.gov/>
- API / data documentation: <https://services.swpc.noaa.gov/>

<!-- upstream-links:end -->

NOAA Space Weather Prediction Center (**SWPC**) publishes the
[propagated solar wind](https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json)
product: the L1 solar-wind time series forward-projected to predicted
Earth arrival. L1 is the Sun-Earth Lagrange point about 1.5 million km
sunward of Earth. NOAA DSCOVR is the operational primary; NASA ACE is the
backup.

This bridge turns that rolling REST document into a first-class real-time
event stream so operational consumers can subscribe instead of polling:

- **Geomagnetic-storm forecasting** — `propagated_time_tag` gives the
  predicted Earth-arrival time of the observed L1 solar-wind parcel.
- **Power-grid operations** — sustained southward Bz is an input to GIC
  threat assessments and geomagnetic-storm procedures.
- **Aviation and maritime operations** — HF radio blackouts and navigation
  impacts can be correlated with the same SWPC input used by forecasters.
- **Satellite operations** — radiation and geomagnetic activity models can
  ingest a deduped, typed feed instead of scraping the SWPC JSON file.
- **Fabric Eventhouse / ADX / data lakes** — keep the full minute-level
  time series for replay, alerting and model development.

The bridge does the polling, cold-start backfill, state-file dedupe,
CloudEvents mapping, JsonStructure schema contract and transport-specific
partitioning.

## Overview

**NOAA SWPC L1** polls one upstream endpoint and emits one CloudEvent type
in three transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest` | Apache Kafka 2.x compatible (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic `noaa-swpc-l1`, JSON CloudEvents (binary mode), key = `{spacecraft}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT) | Retained QoS-1 CloudEvents on `space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest` | AMQP 1.0 (RabbitMQ AMQP 1.0, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs) | Single address `noaa-swpc-l1`, binary CloudEvents, AMQP subject and `x-opt-partition-key` = `{spacecraft}` |

All variants share:

* The transport-agnostic poller (`noaa_swpc_l1_core`).
* The xRegistry contract (`xreg/noaa_swpc_l1.xreg.json`).
* The `gov.noaa.swpc.l1.PropagatedSolarWind` JsonStructure schema.

## Upstream API

The bridge reads:

```text
GET https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json
```

The response is an array-of-arrays. Row 0 is the column header:

```text
time_tag, speed, density, temperature, bx, by, bz, bt, vx, vy, vz, propagated_time_tag
```

Rows 1..N are one observation per minute for a seven-day rolling window.
Upstream timestamps are `YYYY-MM-DD HH:MM:SS.fff` with implicit UTC; the
bridge normalizes them to RFC 3339 UTC. Numeric fields are nullable and
partial rows are emitted rather than skipped.

## Data model

The single event type is:

* `gov.noaa.swpc.l1.PropagatedSolarWind` — one minute-resolution L1 row
  containing:
  * plasma: `speed`, `density`, `temperature`
  * magnetic field in GSM coordinates: `bx`, `by`, `bz`, `bt`
  * bulk velocity in GSM coordinates: `vx`, `vy`, `vz`
  * timestamps: `time_tag` at L1 and `propagated_time_tag` at predicted
    Earth arrival
  * synthetic spacecraft channel: `spacecraft` (`dscovr` by default,
    `ace` reserved for backup failover)

The identity model is intentionally stable and low-cardinality:

| Context | Value |
|---|---|
| CloudEvent subject | `{spacecraft}` |
| Kafka key | `{spacecraft}` |
| MQTT topic segment | `{spacecraft}` |
| AMQP subject | `{spacecraft}` |
| AMQP partition annotation | `x-opt-partition-key = {spacecraft}` |

`time_tag` is the CloudEvent `time` and a payload field, but it is not the
partition key. This keeps each spacecraft channel ordered on all
transports.

## Event schema

The event contract is documented in [EVENTS.md](EVENTS.md). The
authoritative xRegistry document is
[`xreg/noaa_swpc_l1.xreg.json`](xreg/noaa_swpc_l1.xreg.json). The KQL
schema for Fabric Eventhouse / Azure Data Explorer is
[`kql/noaa_swpc_l1.kql`](kql/noaa_swpc_l1.kql).

## Transports

### Kafka

Use Kafka when you need ordered replay, seven-day backfill into a
persistent log, Fabric Eventhouse / ADX ingestion, or multiple consumer
groups reading the same spacecraft stream independently.

```bash
docker run --rm \
  -e CONNECTION_STRING="$EVENT_HUBS_OR_FABRIC_CONNECTION_STRING" \
  ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest
```

### MQTT / UNS

Use MQTT when you need last-known-value distribution, edge-gateway
integration, UNS topic routing, retained dashboards, or a simple
subscription for the latest propagated solar-wind state.

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://broker.example.com:8883 \
  -e MQTT_USERNAME=alice \
  -e MQTT_PASSWORD=secret \
  ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest
```

Published topic (retained, QoS 1):

```text
space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind
```

### AMQP 1.0

Use AMQP when consumers are built around Azure Service Bus or AMQP-native
brokers and need queue semantics, sessions, scheduled delivery,
dead-lettering, or native SB/EH clients. The bridge can authenticate with
SASL PLAIN, Microsoft Entra ID via CBS, or SAS-token CBS.

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://user:pw@broker.example.com:5672/noaa-swpc-l1' \
  ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service
Bus emulator, or SAS-only namespaces, see
[CONTAINER.md](CONTAINER.md#using-the-amqp-image).

## Configuration reference

The complete list of environment variables for every variant (Kafka /
MQTT / AMQP), every authentication mode, state handling and Azure
deployment shape lives in [CONTAINER.md](CONTAINER.md). Defaults shared by
all transports include:

| Setting | Default |
|---|---|
| `POLLING_INTERVAL` | `60` seconds |
| `BACKFILL_MINUTES` | `5` minutes on cold start |
| `STATE_FILE` | `~/.noaa_swpc_l1_state.json` |
| `SPACECRAFT` | `dscovr` |

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

NOAA SWPC L1 targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#noaa-swpc-l1) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `noaa_swpc_l1` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/noaa-swpc-l1/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source noaa-swpc-l1 `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#noaa-swpc-l1/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source noaa-swpc-l1 `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#noaa-swpc-l1/fabric-aci)


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Repository layout

```text
noaa-swpc-l1/
  xreg/noaa_swpc_l1.xreg.json       # shared xRegistry contract
  noaa_swpc_l1_core/                # transport-agnostic acquisition + state
  noaa_swpc_l1_kafka/               # Kafka feeder application
  noaa_swpc_l1_mqtt/                # MQTT/UNS feeder application
  noaa_swpc_l1_amqp/                # AMQP 1.0 feeder application
  noaa_swpc_l1_producer/            # xrcg-generated Kafka producer
  noaa_swpc_l1_mqtt_producer/       # xrcg-generated MQTT producer
  noaa_swpc_l1_amqp_producer/       # xrcg-generated AMQP producer
  Dockerfile.kafka
  Dockerfile.mqtt
  Dockerfile.amqp
  kql/noaa_swpc_l1.kql
  tests/
```

## Development pointers

- Regenerate producers with `generate_producer.ps1` after changing the
  xRegistry contract; do not hand-edit generated producer code.
- The shared acquisition code validates the upstream header exactly and
  raises on header drift.
- Rows are sorted chronologically and emitted only when `time_tag` is
  strictly newer than the stored `last_time_tag`.
- The state file is a single JSON file with key `last_time_tag`.
- See [CONTAINER.md](CONTAINER.md) for deployment behavior and
  [EVENTS.md](EVENTS.md) for the event contract.
