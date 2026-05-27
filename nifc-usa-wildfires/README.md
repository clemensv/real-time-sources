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

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-eventhub.json)


## MQTT and AMQP companion feeders

This source now ships separate Kafka, MQTT, and AMQP containers. The MQTT companion publishes binary-mode CloudEvents to `wildfire/us/nifc/nifc-usa-wildfires/{state}/{status}/{irwin_id}/incident`, where `status` is one of `active`, `contained`, `controlled`, or `out`. The AMQP companion publishes the same CloudEvents to AMQP 1.0 brokers or Azure Service Bus using the IRWIN id subject and `state`/`status` application properties.

Images: `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-mqtt:latest`, `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-amqp:latest`. Deployment templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`, and `infra/azure-template-amqp.json`.
