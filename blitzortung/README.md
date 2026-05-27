<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# Blitzortung

<sub>community lightning strokes, seconds latency · Kafka · MQTT · AMQP · <a href="https://www.blitzortung.org/">upstream</a> · <a href="https://www.lightningmaps.org/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — community lightning strokes, seconds latency

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#blitzortung) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/blitzortung.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.blitzortung.org/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the public [LightningMaps / Blitzortung](https://www.lightningmaps.org/) live websocket feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.blitzortung.org/>
- API / data documentation: <https://www.lightningmaps.org/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

> [!IMPORTANT]
> **Blitzortung / LightningMaps is a community-run, non-commercial service** operated by volunteer detector operators. The upstream project explicitly frames its data as **not** an official safety information service: do not use it for life-safety alerting, aviation operations, or as a substitute for a certified lightning-detection feed. Honour the upstream non-commercial terms when redistributing.

## Why this bridge

[Blitzortung.org](https://www.blitzortung.org/) and its public viewer [LightningMaps.org](https://www.lightningmaps.org/) operate a worldwide volunteer network of VLF lightning detectors. The combined system geolocates **cloud-to-ground and cloud-to-cloud strokes within seconds of occurrence**, with continent-scale coverage that no other free feed approaches. The data is published over a live websocket, but every consumer ends up writing the same reconnect, dedupe, geohash-enrichment and CloudEvents-validation glue.

This feeder turns that websocket firehose into a first-class real-time event stream so consumers can stop holding their own socket and start subscribing to a topic:

- **Weather situational-awareness dashboards** — drive live storm tracking, convective-cell nowcasting, and outdoor-event safety operations from a normalized stroke feed.
- **Insurance and risk** — feed parametric weather-derivative triggers and exposure dashboards with sub-minute stroke timing and location.
- **Grid and infrastructure operations** — combine stroke positions with overhead-line geometry for proximity alerts, transmission-outage forensics, and faster fault localization.
- **Aviation ground-ops and outdoor venues** — supplement (but do not replace) certified detection feeds with continent-scale community coverage during convective events.
- **Climate and research** — long-running ingestion into Microsoft Fabric Eventhouse / Azure Data Explorer / a data lake for stroke-density climatology, convective-mode studies, and detector-network analysis.

The bridge does the boring work — websocket reconnect with resume from the last source-scoped stroke ids, cross-reconnect dedupe, geohash enrichment for routing, JSON-Structure–validated CloudEvents, identity plumbing — so the consumer just subscribes.

## Overview

**Blitzortung** is a streaming bridge that holds an open websocket connection to the LightningMaps / Blitzortung live feed and re-emits every located stroke as a CloudEvent. The source ships in three transport variants from a single upstream client:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-blitzortung` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{source_id}/{stroke_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-blitzortung-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree `weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke`, JSON body, CloudEvent attributes as MQTT 5 user properties, non-retained at QoS 0 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-blitzortung-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The upstream websocket client (`blitzortung` package).
* The xRegistry contract (`xreg/blitzortung.xreg.json`).
* The single CloudEvents schema for `Blitzortung.Lightning.LightningStroke`.

## Key features

- **Live stroke firehose** — seconds-latency, located lightning strokes from the community-run Blitzortung detector network with worldwide coverage.
- **Cross-reconnect dedupe** — resumes from the last source-scoped stroke id and suppresses duplicates after the websocket drops and reconnects.
- **Geohash enrichment** — every stroke is tagged with a 5-character (~5 km) and a 7-character (~150 m) geohash so MQTT subscribers can wildcard by geography at two zoom levels and KQL queries can spatial-bucket without recomputing.
- **Three transport binaries** sharing the same upstream client and the same single event family — switch transport without changing the data model.
- **Azure Event Hubs / Microsoft Fabric Event Streams** ready via standard connection strings (Kafka variant).
- **Unified Namespace** ready out of the box with MQTT 5.0 binary CloudEvents and a geohash-rooted topic tree (MQTT variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID** (no SAS-key rotation) via the AMQP variant's CBS put-token flow, plus SAS-token CBS for the Service Bus emulator and SAS-only namespaces.

## Repository layout

```text
blitzortung/
  xreg/blitzortung.xreg.json     # shared xRegistry contract
  blitzortung/                   # websocket client + Kafka feeder application
  blitzortung_mqtt/              # MQTT/UNS feeder application
  blitzortung_amqp/              # AMQP 1.0 feeder application
  blitzortung_producer/          # xRegistry-generated Kafka producer
  blitzortung_mqtt_producer/     # xRegistry-generated MQTT producer
  blitzortung_amqp_producer/     # xRegistry-generated AMQP producer
  Dockerfile                     # builds the Kafka feeder image
  Dockerfile.mqtt                # builds the MQTT feeder image
  Dockerfile.amqp                # builds the AMQP feeder image
  kql/                           # Eventhouse / KQL schema and update policies
  tests/                         # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound TLS (port 443) to `live.lightningmaps.org` and `live2.lightningmaps.org`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.

This feeder is a pure streaming bridge — it holds an open websocket and forwards strokes live. Cross-reconnect dedupe is an in-memory ring of recent stroke ids that rebuilds from the live stream after every restart, so no host volume is required.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-blitzortung:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-blitzortung-mqtt:latest
```

Topics published (non-retained, QoS 0):

```text
weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke
```

`{geohash5}` is a ~5 km cell, `{geohash7}` is a ~150 m cell, both derived from the stroke's latitude and longitude. Subscribe with `weather/intl/blitzortung/blitzortung/u281/#` to receive every stroke within a ~5 km cell, for example.

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/blitzortung' \
  ghcr.io/clemensv/real-time-sources-blitzortung-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via CBS, SAS-token CBS), and every Azure deployment shape lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for every image is `python -m blitzortung{,_mqtt,_amqp} feed`; the image's default `CMD` invokes it for you.

## Data model

The feeder emits a single event family:

- **`Blitzortung.Lightning.LightningStroke`** — one located lightning stroke from the public live feed.

The public websocket identifies strokes by source-scoped ids; the CloudEvents `subject` and the Kafka key therefore use the compound identity `{source_id}/{stroke_id}` so consumers can deduplicate across reconnects without ambiguity. The MQTT topic uses `{stroke_id}` only (geographic wildcards do the disambiguation).

The bridge preserves the detector-participation `sta` map from the upstream payload as a normalized array of `{station_id, status}` objects. The upstream does not currently publish a bit-level definition for the integer `status` value, so the bridge preserves it verbatim and documents the gap in [EVENTS.md](EVENTS.md) rather than inventing meanings. **No separate station-reference event type is emitted** because no public station-metadata endpoint exists.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

Blitzortung targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#blitzortung) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source blitzortung `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#blitzortung/fabric-aci)


### Deploying into Azure Container Instances

6 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-servicebus.json)

#### AMQP — bring your own AMQP 1.0 peer

Deploy the AMQP container against an existing AMQP 1.0 peer (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs). You pass the broker URL and credentials; the template provisions only the container.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-amqp.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Pick a hosting model: a [Fabric ACI feeder](#deploying-into-microsoft-fabric) if your destination is a Fabric workspace; a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs or Service Bus without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up authentication modes and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- Read the upstream project's [Blitzortung.org](https://www.blitzortung.org/) and [LightningMaps.org](https://www.lightningmaps.org/) sites for detector-network background and non-commercial-use terms.
