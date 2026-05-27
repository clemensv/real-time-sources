<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/ca.png" alt="Canada" width="64" height="48"><br>
<sub><b>Canada</b></sub>
</td>
<td valign="middle">

# Canada ECCC Water Office

<sub>~2,100 hydrometric stations, ECCC/WSC · Kafka · MQTT · AMQP · <a href="https://wateroffice.ec.gc.ca/">upstream</a> · <a href="https://api.weather.gc.ca/openapi">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Canada — ~2,100 hydrometric stations, ECCC/WSC

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#canada-eccc-wateroffice) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/canada-eccc-wateroffice.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://wateroffice.ec.gc.ca/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the real-time [Environment and Climate Change Canada (ECCC) Water Survey of Canada](https://wateroffice.ec.gc.ca/) hydrometric feed into a CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://wateroffice.ec.gc.ca/>
- API / data documentation: <https://api.weather.gc.ca/openapi>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

The [ECCC Water Survey of Canada](https://wateroffice.ec.gc.ca/) publishes official real-time hydrometric data for roughly **2,100 active gauging stations** across Canada via the OGC API Features service at `https://api.weather.gc.ca`. That gives you national water-level and discharge telemetry plus station reference metadata from a single open government source, but every consumer still has to poll the API, track the rolling observation window, refresh the station catalog, normalize payloads, and publish them into its own event backbone.

This feeder turns that national hydrometric feed into a first-class real-time event stream so consumers can stop polling the OGC API themselves and start subscribing to a topic:

- **Flood forecasting and emergency operations** — push near-real-time river levels into alerting dashboards and regional response workflows.
- **Hydropower and water-resource operations** — monitor upstream levels and discharge for reservoir, diversion, and generation planning.
- **Environmental and climate analytics** — ingest long-running hydrometric series into Microsoft Fabric Eventhouse, Azure Data Explorer, or a lakehouse without building a custom poller first.
- **Cross-basin monitoring** — join station reference data with live observations to track conditions across provinces, drainage basins, and RHBN stations.
- **Research and public transparency** — subscribe to a normalized event stream instead of repeatedly scraping or re-polling the public API.

The bridge does the boring work — polling, rolling-window observation fetches, daily station-catalog refresh, CloudEvents shaping, and transport-specific publishing — so the consumer just subscribes.

## Overview

**Canada ECCC Water Office** is a poll-based bridge that queries the Water Survey of Canada OGC API Features endpoints and re-emits station metadata plus real-time hydrometric observations as CloudEvents. The source ships in three transport variants from the same upstream poller logic:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `stations/{station_number}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `hydro/ca/eccc/canada-eccc-wateroffice/{basin}/{station_number}/{info|observation}`, JSON body, CloudEvent attributes as MQTT 5 user properties, retained at QoS 1 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (`canada-eccc-wateroffice` by default), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The upstream OGC API poller and normalization logic.
* The xRegistry contract (`xreg/canada-eccc-wateroffice.xreg.json`).
* The same two event families: station reference data and real-time observations.

## Key features

- **National Canadian hydrometric coverage** — roughly 2,100 active stations across provinces and territories.
- **Two event families** — `CA.Gov.ECCC.Hydro.Station` reference data plus `CA.Gov.ECCC.Hydro.Observation` telemetry.
- **Source-aligned cadence** — observations are polled about every 5 minutes; the station catalog refreshes every 24 hours.
- **No upstream credentials required** — the Water Survey of Canada OGC API is open and anonymous.
- **Rolling observation window** — the bridge queries a 2-hour lookback window so short upstream or network gaps do not force consumers to backfill manually.
- **Three transport binaries** with the same data model — switch transport without changing the contract.
- **Azure Event Hubs / Microsoft Fabric Event Streams ready** via standard Kafka connection strings (Kafka variant).
- **Unified Namespace ready** out of the box with retained QoS 1 topics rooted by basin and station number (MQTT variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID** (no SAS-key rotation) plus SAS-token CBS for emulator and SAS-only deployments (AMQP variant).

## Repository layout

```text
canada-eccc-wateroffice/
  xreg/canada-eccc-wateroffice.xreg.json       # shared xRegistry contract
  canada_eccc_wateroffice/                     # OGC API poller + Kafka feeder application
  canada_eccc_wateroffice_mqtt/                # MQTT/UNS feeder application
  canada_eccc_wateroffice_amqp/                # AMQP 1.0 feeder application
  canada_eccc_wateroffice_producer/            # xRegistry-generated Kafka producer
  canada_eccc_wateroffice_mqtt_producer/       # xRegistry-generated MQTT producer
  canada_eccc_wateroffice_amqp_producer/       # xRegistry-generated AMQP producer
  Dockerfile                                   # builds the Kafka feeder image
  Dockerfile.mqtt                              # builds the MQTT feeder image
  Dockerfile.amqp                              # builds the AMQP feeder image
  kql/canada-eccc-wateroffice.kql              # Eventhouse / KQL schema and update policies
  tests/                                       # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS (port 443) to `api.weather.gc.ca`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.

This feeder is a poller, but it does **not** require a persistent state file. It fetches observations from a rolling 2-hour window and deduplicates them in memory within the current process lifetime, so the quick-start Docker commands below do not need a host volume.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice-mqtt:latest
```

Topics published (retained, QoS 1):

```text
hydro/ca/eccc/canada-eccc-wateroffice/{basin}/{station_number}/info
hydro/ca/eccc/canada-eccc-wateroffice/{basin}/{station_number}/observation
```

`{basin}` is derived from the station's drainage-basin metadata and normalized for topic safety; `info` carries the retained station record and `observation` carries the latest retained measurement for that station.

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/canada-eccc-wateroffice' \
  ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via MQTT or AMQP CBS, SAS-token CBS), and every Azure deployment shape lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for every image is `python -m canada_eccc_wateroffice{,_mqtt,_amqp} feed`; the image's default `CMD` invokes it for you.

## Data model

The feeder emits two event families:

| CloudEvents type | Description |
|---|---|
| `CA.Gov.ECCC.Hydro.Station` | Station reference data for one Water Survey of Canada hydrometric station, emitted at startup and refreshed every 24 hours. |
| `CA.Gov.ECCC.Hydro.Observation` | Real-time water-level and discharge observation for one station, polled on roughly a 5-minute cadence. |

The CloudEvents `subject` and Kafka key use the stable identity `stations/{station_number}`. MQTT topics and AMQP routing properties add the basin axis so subscribers can wildcard by drainage basin without losing the stable station identity.

## Deploying into Microsoft Fabric

Canada ECCC Water Office targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), and an attached Eventhouse / KQL database materializes the contract from [`kql/canada-eccc-wateroffice.kql`](kql/canada-eccc-wateroffice.kql) with one table per event family and update policies that decode the CloudEvent envelope.

This source is documented for the long-running **Fabric ACI feeder** deployment shape. It does not ship a Fabric notebook artifact; use the always-on container deployment when the destination is a Fabric workspace.

### Fabric ACI feeder

A long-running Azure Container Instance hosts one of the three container images and writes into a Fabric Event Stream custom endpoint. Use this whenever the destination is a Fabric workspace.

Deploy with `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source canada-eccc-wateroffice -Workspace <id> -ResourceGroup <azure-rg> -Location <azure-region>` (the portal button wraps this for you). The script creates the Eventhouse, the KQL database with the [`kql/canada-eccc-wateroffice.kql`](kql/canada-eccc-wateroffice.kql) schema and update policies, the Event Stream with a custom endpoint, and the ACI with the connection string wired in.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#canada-eccc-wateroffice/fabric-aci)

## Deploying into Azure Container Instances

Five one-click deployment templates are available — Kafka (bring your own Event Hub or provision a new one), MQTT (bring your own broker or provision an Azure Event Grid namespace), and AMQP (provision a new Azure Service Bus namespace).

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-with-eventhub.json)

### MQTT — bring your own MQTT broker

Deploy the MQTT container with your own MQTT 5.0 broker endpoint and credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-mqtt.json)

### MQTT — provision an Azure Event Grid namespace

Deploy the MQTT container together with an Azure Event Grid namespace configured for MQTT publishing.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue named `canada-eccc-wateroffice`, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-with-servicebus.json)

## Next steps

- Pick a hosting model: a [Fabric ACI feeder](#deploying-into-microsoft-fabric) if your destination is a Fabric workspace; a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs, MQTT, or Service Bus without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up authentication modes and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- Read the upstream Water Survey of Canada pages at [wateroffice.ec.gc.ca](https://wateroffice.ec.gc.ca/), the OGC API at `https://api.weather.gc.ca`, and the [Open Government Licence — Canada](https://open.canada.ca/en/open-government-licence-canada).
