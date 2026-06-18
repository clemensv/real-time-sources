<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/de.png" alt="Germany" width="64" height="48"><br>
<sub><b>Germany</b></sub>
</td>
<td valign="middle">

# German Waters

<sub>12 state portals, ~2,724 stations · Kafka · MQTT · AMQP · <a href="https://hvz.lubw.baden-wuerttemberg.de/">upstream</a> · <a href="https://hvz.lubw.baden-wuerttemberg.de/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Germany — 12 state portals, ~2,724 stations

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#german-waters) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#german-waters/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/german_waters.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://hvz.lubw.baden-wuerttemberg.de/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns hydrometric data from 12 German federal-state water authorities into a CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://hvz.lubw.baden-wuerttemberg.de/>
- API / data documentation: <https://hvz.lubw.baden-wuerttemberg.de/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

**German Waters** aggregates open hydrometric data from **12 official German state authorities** — GKD Bayern, NRW, Schleswig-Holstein, Niedersachsen, Sachsen-Anhalt, Hessen, Sachsen, Baden-Württemberg, Brandenburg, Thüringen, Mecklenburg-Vorpommern, and Berlin — across roughly **2,724 stations**. The upstream landscape is deliberately heterogeneous: WISKI JSON, ArcGIS GeoJSON, Azure-hosted REST APIs, HTML tables, OpenLayers payloads, Leaflet markup, and JavaScript arrays, under a mix of public licenses including **CC-BY 4.0**, **dl-de/zero-2-0**, and **dl-de/by-2-0**.

This feeder turns that fragmented government-open-data landscape into a first-class real-time event stream so consumers can stop integrating 12 provider-specific portals and start subscribing to a topic:

- **Flood and river-operations monitoring** — track water levels across state borders from one normalized event stream.
- **Utilities, hydropower, and navigation support** — combine water-level and discharge readings from multiple authorities without writing custom scrapers per state.
- **Environmental and regulatory analytics** — land reference data and telemetry in Microsoft Fabric Eventhouse, Azure Data Explorer, or a lakehouse with one contract.
- **Research and journalism** — work from official state-published hydrometry instead of a commercial aggregator or one-off scraping scripts.
- **Selective regional ingest** — include or exclude providers to build state-specific or basin-specific pipelines from one deployment artifact.

The bridge does the boring work — polling 12 different upstream implementations, normalizing station catalogs, carrying forward water-body routing data, deduplicating observations, and publishing consistent CloudEvents — so the consumer just subscribes.

## Overview

**German Waters** is a poll-based bridge that queries 12 state hydrology providers, emits station reference data at startup, and then publishes only new or changed measurements on each poll cycle. The source ships in three transport variants from the same upstream provider stack:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-german-waters` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{station_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-german-waters-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `hydro/de/wsv/german-waters/{water_body}/{station_id}/{info|water-level}`, JSON body, CloudEvent attributes as MQTT 5 user properties, retained at QoS 1 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-german-waters-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (`german-waters` by default), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The upstream provider adapters and normalization logic.
* The xRegistry contract (`xreg/german_waters.xreg.json`).
* The same two event families: station reference data and water-level/discharge observations.

## Key features

- **12-provider federation** — roughly 2,724 stations from official state water portals across Germany.
- **Two event families** — `DE.Waters.Hydrology.Station` reference data plus `DE.Waters.Hydrology.WaterLevelObservation` telemetry.
- **Official-source only** — no commercial aggregator and no upstream API keys required.
- **Provider filters** — include or exclude individual state providers with `PROVIDERS` / `EXCLUDE_PROVIDERS`.
- **Delta-only observation emission** — optional `STATE_FILE` persistence suppresses replay after restart.
- **Three transport binaries** with the same contract — switch transport without changing consumer schemas.
- **Azure Event Hubs / Microsoft Fabric Event Streams ready** via standard Kafka connection strings (Kafka variant).
- **Unified Namespace ready** out of the box with retained QoS 1 topics rooted by water body and station id (MQTT variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID** (no SAS-key rotation) plus SAS-token CBS for emulator and SAS-only deployments (AMQP variant).

## Repository layout

```text
german-waters/
  xreg/german_waters.xreg.json                # shared xRegistry contract
  german_waters/                              # provider adapters + Kafka feeder application
  german_waters_mqtt/                         # MQTT/UNS feeder application
  german_waters_amqp/                         # AMQP 1.0 feeder application
  german_waters_producer/                     # xRegistry-generated Kafka producer
  german_waters_mqtt_producer/                # xRegistry-generated MQTT producer
  german_waters_amqp_producer/                # xRegistry-generated AMQP producer
  Dockerfile                                  # builds the Kafka feeder image
  Dockerfile.mqtt                             # builds the MQTT feeder image
  Dockerfile.amqp                             # builds the AMQP feeder image
  infra/                                      # legacy deployment helpers / mirrored templates
  kql/german_waters.kql                       # Eventhouse / KQL schema and update policies
  tests/                                      # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS (port 443) to the upstream German state-provider portals and APIs.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.

This feeder can persist de-duplication state through `STATE_FILE`, but the quick-start Docker commands below intentionally run without a mounted state volume. That is fine for evaluation or stateless deployments; if you need replay suppression across restarts, configure `STATE_FILE` as documented in [CONTAINER.md](CONTAINER.md).

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-german-waters:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-german-waters-mqtt:latest
```

Topics published (retained, QoS 1):

```text
hydro/de/wsv/german-waters/{water_body}/{station_id}/info
hydro/de/wsv/german-waters/{water_body}/{station_id}/water-level
```

`{water_body}` is normalized to lower-case kebab-case for topic safety; `info` carries the retained station record and `water-level` carries the latest retained reading for that station.

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/german-waters' \
  ghcr.io/clemensv/real-time-sources-german-waters-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via MQTT or AMQP CBS, SAS-token CBS), and the checked-in Azure deployment shapes lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for every image is `python -m german_waters{,_mqtt,_amqp} feed`; the image's default `CMD` invokes it for you. The source also exposes `python -m german_waters list-providers` and `python -m german_waters list` for provider and station discovery.

## Data model

The feeder emits two event families:

| CloudEvents type | Description |
|---|---|
| `DE.Waters.Hydrology.Station` | Station reference data for one state-provider gauge, emitted once at startup. |
| `DE.Waters.Hydrology.WaterLevelObservation` | Current water-level and discharge reading for one station, emitted when the value changes. |

The CloudEvents `subject` and Kafka key use the stable identity `{station_id}`. MQTT topics and AMQP routing properties add the `water_body` axis so subscribers can wildcard by river or canal without losing the stable station identity.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

German Waters targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#german-waters) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `german_waters` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/german-waters/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source german-waters `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#german-waters/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source german-waters `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#german-waters/fabric-aci)


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgerman-waters%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgerman-waters%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker. You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgerman-waters%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space rooted at `hydro/#`, a user-assigned managed identity, and a role assignment granting the identity the **EventGrid TopicSpaces Publisher** role on the topic space. The feeder authenticates to the broker using MQTT v5 enhanced authentication (`OAUTH2-JWT`) with tokens minted by the managed identity for audience `https://eventgrid.azure.net/`.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgerman-waters%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgerman-waters%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Pick a hosting model: a [Fabric Notebook feeder](#deploying-into-microsoft-fabric) for scheduled in-workspace polling, a [Fabric ACI feeder](#deploying-into-microsoft-fabric) for always-on runtime, or a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs / MQTT / Service Bus without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up provider filters, optional state persistence, and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- Use the official state-provider portals and licenses documented by this source when you need per-provider provenance alongside the normalized feed.
