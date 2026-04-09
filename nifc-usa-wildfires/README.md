# NIFC USA Wildfires - Active Wildfire Incident Feed

## Overview

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
