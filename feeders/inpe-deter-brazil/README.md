<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/br.png" alt="Brazil" width="64" height="48"><br>
<sub><b>Brazil</b></sub>
</td>
<td valign="middle">

# INPE DETER Brazil

<sub>Amazon & Cerrado deforestation alerts · Kafka · MQTT · AMQP · <a href="http://terrabrasilis.dpi.inpe.br/">upstream</a> · <a href="http://terrabrasilis.dpi.inpe.br/geoserver/web/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Brazil — Amazon & Cerrado deforestation alerts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#inpe-deter-brazil) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/inpe_deter_brazil.kql) &nbsp;·&nbsp;
[↗ **Upstream**](http://terrabrasilis.dpi.inpe.br/)

</td></tr></table>
<!-- source-hero:end -->

## Overview

<!-- upstream-links:begin -->
## Upstream

- Home page: <http://terrabrasilis.dpi.inpe.br/>
- API / data documentation: <http://terrabrasilis.dpi.inpe.br/geoserver/web/>

<!-- upstream-links:end -->

**INPE-DETER-Brazil** is a tool designed to interact with the [INPE
TerraBrasilis DETER](http://terrabrasilis.dpi.inpe.br/) real-time deforestation
detection system to fetch deforestation alert data for the Amazon and Cerrado
biomes. The tool can list recent alerts or continuously poll the API to send
deforestation events to a Kafka topic.

INPE's DETER system uses satellite imagery to detect deforestation, degradation,
mining, and disorderly development across Brazil's major biomes. This bridge
converts those detections into [CloudEvents](https://cloudevents.io/) structured
JSON format and publishes them to Kafka, Azure Event Hubs, or Microsoft Fabric
Event Streams.

## Key Features:
- **Dual Biome Monitoring**: Polls both Amazon and Cerrado WFS endpoints.
- **Temporal Filtering**: Uses CQL_FILTER with view_date for efficient polling.
- **Centroid Computation**: Computes polygon centroids for lat/lon coordinates.
- **Deduplication**: Tracks seen alert IDs to avoid forwarding duplicates.
- **Kafka Integration**: Sends alerts as CloudEvents to a Kafka topic.

## Installation

The tool is written in Python and requires Python 3.10 or later.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=inpe-deter-brazil
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/inpe-deter-brazil
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `inpe-deter-brazil` command:
- **List Events (`events`)**: Fetch and display recent deforestation alerts.
- **List Biomes (`biomes`)**: Show available biomes and their WFS endpoints.
- **Feed Events (`feed`)**: Continuously poll and send alerts to Kafka.

### **List Events (`events`)**

```bash
inpe-deter-brazil events
inpe-deter-brazil events --biome amazon --days 14
```

### **List Biomes (`biomes`)**

```bash
inpe-deter-brazil biomes
```

### **Feed Events (`feed`)**

```bash
inpe-deter-brazil feed --connection-string "<your_connection_string>"
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Fabric Event Stream connection string.
- `INPE_DETER_LAST_POLLED_FILE`: Path to file storing the last polled state.
- `LOG_LEVEL`: Logging level (default: INFO).

## Data Source

The INPE TerraBrasilis DETER system provides deforestation alerts via OGC WFS
2.0 GeoServer endpoints. The alerts include:

- **Alert classes**: DESMATAMENTO_CR (clear-cut deforestation), DEGRADACAO
  (degradation), MINERACAO (mining), CS_DESORDENADO (disorderly settlement).
- **Satellites**: CBERS-4, Amazonia-1, and others.
- **Sensors**: AWFI, WFI, MSI.

## State Management

The tool tracks alert IDs in a local JSON file. Only new alerts are forwarded to
Kafka. State is pruned to prevent unbounded growth.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

INPE DETER Brazil targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#inpe-deter-brazil) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source inpe-deter-brazil `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#inpe-deter-brazil/fabric-aci)


### Deploying into Azure Container Instances

3 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Finpe-deter-brazil%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Finpe-deter-brazil%2Fazure-template-with-eventhub.json)

#### AMQP — bring your own AMQP 1.0 peer

Deploy the AMQP container against an existing AMQP 1.0 peer (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs). You pass the broker URL and credentials; the template provisions only the container.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Finpe-deter-brazil%2Fazure-template-amqp.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Transports

This source now ships separate Kafka, MQTT, and AMQP containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variants for INPE DETER Brazil deforestation and related land-disturbance alerts. The UNS topic tree is deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert. Payloads are JSON binary-mode CloudEvents. QoS 1 is used for at-least-once alert delivery; consumers MUST deduplicate by alert_id. retain=false is used because DETER alerts are immutable historical events and retaining each alert_id topic would create an unbounded retained-message graveyard. A Message Expiry Interval of 604800 seconds bounds queued delivery for offline durable subscribers. The state_slug axis is a lowercased Brazilian UF code or unknown when INPE omits or publishes an unsupported UF; class_slug is a supported topic-safe lowercase-kebab DETER class or unknown.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/inpe_deter_brazil.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert` | `BR.INPE.DETER.DeforestationAlert` | QoS 1, retain=false, expiry=604800s |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.

## AMQP 1.0 companion feeder

This source also ships an AMQP 1.0 companion container, `ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-amqp:latest`, for queue-oriented consumers using generic AMQP brokers or Azure Service Bus. It emits the same CloudEvents and payload schemas as the Kafka and MQTT variants on a single broker address (default `inpe-deter-brazil`).

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=inpe-deter-brazil   ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-amqp:latest
```

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Finpe-deter-brazil%2Fazure-template-amqp.json)

