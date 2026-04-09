# INPE DETER Brazil - Deforestation Alerts

## Overview

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

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-with-eventhub.json)
