<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="United States" width="64" height="48"><br>
<sub><b>United States</b></sub>
</td>
<td valign="middle">

# NIFC USA Wildfires

<sub>active wildfire incidents, NIFC · Kafka · MQTT · AMQP · <a href="https://www.nifc.gov/">upstream</a> · <a href="https://data-nifc.opendata.arcgis.com/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> United States — active wildfire incidents, NIFC

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#nifc-usa-wildfires) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/nifc_usa_wildfires.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.nifc.gov/)

</td></tr></table>
<!-- source-hero:end -->

## Overview

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.nifc.gov/>
- API / data documentation: <https://data-nifc.opendata.arcgis.com/>

<!-- upstream-links:end -->

**NIFC-USA-Wildfires** is a tool designed to interact with the [National
Interagency Fire Center (NIFC)](https://www.nifc.gov/) ArcGIS Feature Service to
fetch active wildfire incident data from the USA. The tool can list recent
incidents or continuously poll the API to send wildfire events to a Kafka topic.

The NIFC publishes real-time wildfire incident data from the Integrated Reporting
of Wildland-Fire Information (IRWIN) system via an ArcGIS Feature Service. This
bridge converts those incidents into [CloudEvents](https://cloudevents.io/)
structured JSON format and publishes them to Kafka, Azure Event Hubs, or
Microsoft Fabric Event Streams.

## Key Features

- **Active Wildfire Data**: Retrieves active wildfire incidents from the NIFC ArcGIS Feature Service.
- **Deduplication**: Tracks seen incidents by IRWIN ID and modified timestamp — only new or updated incidents are forwarded.
- **Paging Support**: Automatically pages through all results when the API exceeds transfer limits.
- **Kafka Integration**: Sends wildfire incidents as CloudEvents to a Kafka topic, supporting Microsoft Event Hubs and Microsoft Fabric Event Streams.

## Installation

The tool is written in Python and requires Python 3.10 or later.

### Installation Steps

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=nifc-usa-wildfires
```

If you clone the repository:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/nifc-usa-wildfires
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `nifc-usa-wildfires` command:

- **List Incidents (`incidents`)**: Fetch and display recent wildfire incidents.
- **Feed Incidents (`feed`)**: Continuously poll the NIFC feed and send updates to a Kafka topic.

### List Incidents

```bash
nifc-usa-wildfires incidents
```

### Feed Incidents

```bash
nifc-usa-wildfires feed --connection-string "<your_connection_string>"
```

Or with explicit Kafka configuration:

```bash
nifc-usa-wildfires feed --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

### Environment Variables

- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `NIFC_LAST_POLLED_FILE`: Path to file storing the last polled incident IDs (default: `~/.nifc_usa_wildfires_last_polled.json`).
- `LOG_LEVEL`: Logging level (default: INFO).
- `KAFKA_ENABLE_TLS`: Enable TLS for Kafka connections (default: true).

## Data Source

The data comes from the NIFC's USA Wildfires ArcGIS Feature Service Layer 0 (Incidents):

`https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/USA_Wildfires_v1/FeatureServer/0`

This is US Government public domain data, no authentication required.

## State Management

The tool tracks incident IRWIN IDs and their last modification timestamps in a local
JSON file. Only new incidents or incidents that have been updated since last seen are
forwarded to Kafka. Old entries are pruned after 90 days.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

NIFC USA Wildfires targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#nifc-usa-wildfires) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source nifc-usa-wildfires `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#nifc-usa-wildfires/fabric-aci)


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## MQTT and AMQP companion feeders

This source now ships separate Kafka, MQTT, and AMQP containers. The MQTT companion publishes binary-mode CloudEvents to `wildfire/us/nifc/nifc-usa-wildfires/{state}/{status}/{irwin_id}/incident`, where `status` is one of `active`, `contained`, `controlled`, or `out`. The AMQP companion publishes the same CloudEvents to AMQP 1.0 brokers or Azure Service Bus using the IRWIN id subject and `state`/`status` application properties.

Images: `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-mqtt:latest`, `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-amqp:latest`. Deployment templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`, and `infra/azure-template-amqp.json`.
