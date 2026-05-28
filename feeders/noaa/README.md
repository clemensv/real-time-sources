<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="United States" width="64" height="48"><br>
<sub><b>United States</b></sub>
</td>
<td valign="middle">

# NOAA Tides & Currents

<sub>~3,000 stations · Kafka · MQTT · AMQP · <a href="https://tidesandcurrents.noaa.gov/">upstream</a> · <a href="https://api.tidesandcurrents.noaa.gov/api/prod/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> United States — ~3,000 stations

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#noaa) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#noaa/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/noaa.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://tidesandcurrents.noaa.gov/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the public [NOAA Tides and Currents API](https://api.tidesandcurrents.noaa.gov/) into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://tidesandcurrents.noaa.gov/>
- API / data documentation: <https://api.tidesandcurrents.noaa.gov/api/prod/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

[NOAA Tides and Currents](https://api.tidesandcurrents.noaa.gov/) publishes real-time coastal and tidal observations from thousands of U.S. stations: water level, tides, meteorology, currents, visibility, salinity, and station reference metadata. The upstream API is open, stable, and public-domain, but every consumer otherwise has to poll the station catalog, fan out per product, track watermarks, and normalize a dozen related payload shapes.

This bridge turns that API into a first-class real-time event stream so consumers can stop polling NOAA directly and start subscribing to a topic:

- **Port and pilot operations** — drive berth planning, tidal windows, and harbor approach dashboards from water-level, current, and prediction events.
- **Coastal flood and resilience analytics** — ingest water-level and meteorological observations into Microsoft Fabric Eventhouse / Azure Data Explorer for flood-threshold monitoring and historical replay.
- **Environmental monitoring** — combine water temperature, salinity, conductivity, and visibility with local sensors for estuary, fisheries, and habitat analysis.
- **Digital twins for coastal infrastructure** — feed storm-surge, tide, and currents context into port, bridge, lock, and shoreline digital twins.
- **Research and journalism** — consume a normalized public-domain NOAA stream without owning the polling, dedupe, and schema-validation glue.

The bridge does the boring work — station discovery, per-product polling, checkpoint state, reference-data emission, JSON-Structure–validated CloudEvents, and identity plumbing — so the consumer just subscribes.

## Overview

**NOAA Tides and Currents** is a poll-based bridge that walks the NOAA station catalog, emits station reference data, and then polls each supported product family for updates. The source ships in three transport variants from the same upstream poller contract:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-noaa` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{station_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-noaa-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `maritime/us/noaa/noaa/{region}/{station_id}/{product-slug}`, JSON body, CloudEvent attributes as MQTT 5 user properties, retained at QoS 1 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-noaa-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The NOAA polling logic and station/product normalization.
* The xRegistry contract (`xreg/noaa.xreg.json`).
* The same 13 CloudEvents types: 1 station reference event and 12 telemetry / prediction event types.

## Key features

- **13 NOAA event types** covering station reference data plus the core Tides and Currents products used in coastal operations.
- **Public-domain upstream** with no authentication or API key required.
- **Reference data first** — station metadata is emitted as a named event type and shares the same `{station_id}` identity as telemetry.
- **Source-scoped checkpointing** via `NOAA_LAST_POLLED_FILE` so restarts can resume from the last observed timestamps.
- **Three transport binaries** sharing the same product families and identity model — switch transport without changing the data contract.
- **Retained MQTT Last Known Value topics** at QoS 1 for station and telemetry branches.
- **Azure Event Hubs / Microsoft Fabric Event Streams** ready via standard connection strings (Kafka variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID** (no SAS-key rotation) via CBS put-token, plus SAS-token CBS for emulator / SAS-only namespaces.

## Repository layout

```text
noaa/
  xreg/noaa.xreg.json             # shared xRegistry contract
  noaa/                           # poller + Kafka feeder application
  noaa_mqtt/                      # MQTT/UNS feeder application
  noaa_amqp/                      # AMQP 1.0 feeder application
  noaa_producer/                  # xRegistry-generated Kafka producer
  noaa_mqtt_producer/             # xRegistry-generated MQTT producer
  noaa_amqp_producer/             # xRegistry-generated AMQP producer
  Dockerfile                      # builds the Kafka feeder image
  Dockerfile.mqtt                 # builds the MQTT feeder image
  Dockerfile.amqp                 # builds the AMQP feeder image
  kql/noaa.kql                    # Eventhouse / KQL schema and update policies
  tests/                          # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS access to `api.tidesandcurrents.noaa.gov`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.

This feeder is a poller, not a streaming socket bridge. It can run stateless for evaluation, but if you want restart continuity you should persist `NOAA_LAST_POLLED_FILE` outside the container in your real deployment.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-noaa:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-noaa-mqtt:latest
```

Topics published (retained, QoS 1):

```text
maritime/us/noaa/noaa/{region}/{station_id}/{product-slug}
```

`{product-slug}` is one of `info`, `water-level`, `predictions`, `air-pressure`, `air-temperature`, `water-temperature`, `wind`, `humidity`, `conductivity`, `salinity`, `visibility`, `currents`, or `current-predictions`.

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/noaa' \
  ghcr.io/clemensv/real-time-sources-noaa-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via CBS, SAS-token CBS), and every Azure deployment shape lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for the images is `python -m noaa feed`, `python -m noaa_mqtt feed`, or `python -m noaa_amqp feed`; the image default `CMD` invokes it for you.

## Data model

The feeder emits one reference-data event type and twelve telemetry / prediction event types, all keyed by the stable NOAA station identifier `{station_id}`.

### Reference data

| Event type | Description |
|---|---|
| `Microsoft.OpenData.US.NOAA.Station` | Station metadata for a NOAA tide or current station: identifiers, region, name, coordinates, and descriptive attributes consumers need to interpret telemetry. |

### Telemetry and prediction families

| Event type | Description |
|---|---|
| `Microsoft.OpenData.US.NOAA.WaterLevel` | Observed water level for a station. |
| `Microsoft.OpenData.US.NOAA.Predictions` | Tidal prediction values for a station. |
| `Microsoft.OpenData.US.NOAA.AirPressure` | Observed air pressure. |
| `Microsoft.OpenData.US.NOAA.AirTemperature` | Observed air temperature. |
| `Microsoft.OpenData.US.NOAA.WaterTemperature` | Observed water temperature. |
| `Microsoft.OpenData.US.NOAA.Wind` | Wind speed, gust, and direction measurements. |
| `Microsoft.OpenData.US.NOAA.Humidity` | Relative humidity observations. |
| `Microsoft.OpenData.US.NOAA.Conductivity` | Water conductivity observations. |
| `Microsoft.OpenData.US.NOAA.Salinity` | Water salinity observations. |
| `Microsoft.OpenData.US.NOAA.Visibility` | Visibility observations reported by the station. |
| `Microsoft.OpenData.US.NOAA.Currents` | Observed current speed and direction. |
| `Microsoft.OpenData.US.NOAA.CurrentPredictions` | Predicted current speed and direction. |

Kafka uses `{station_id}` as the record key. MQTT maps the same identity into `maritime/us/noaa/noaa/{region}/{station_id}/{product-slug}`. AMQP uses the message subject `{station_id}` on the configured address, with `region` available as an application property.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

NOAA Tides & Currents targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#noaa) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `noaa` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/noaa/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source noaa `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#noaa/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source noaa `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#noaa/fabric-aci)


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Pick a hosting model: a [Fabric ACI feeder](#deploying-into-microsoft-fabric) if your destination is a Fabric workspace; a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs, MQTT, or Service Bus without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up authentication modes and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- Browse the upstream NOAA API documentation at [api.tidesandcurrents.noaa.gov](https://api.tidesandcurrents.noaa.gov/) for station-specific product coverage and semantics.
