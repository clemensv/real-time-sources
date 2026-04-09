# Meteoalarm Container

## Quick Start

```bash
docker build -t meteoalarm .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" meteoalarm
```

## Description

This container bridges severe weather warnings from the EUMETNET Meteoalarm
system to Kafka-compatible endpoints (Apache Kafka, Azure Event Hubs,
Microsoft Fabric Event Streams) as CloudEvents.

It polls the Meteoalarm JSON API for warnings from 30+ European national
meteorological services and emits them as structured CloudEvents using the
CAP (Common Alerting Protocol) schema.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes* | Event Hubs / Fabric connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes* | Kafka bootstrap servers |
| `KAFKA_TOPIC` | No | Topic name (default: `meteoalarm`) |
| `SASL_USERNAME` | No | SASL username |
| `SASL_PASSWORD` | No | SASL password |
| `METEOALARM_STATE_FILE` | No | State file (default: `~/.meteoalarm_state.json`) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` is required.

## Azure Container Instance

```bash
az container create \
  --resource-group <rg> \
  --name meteoalarm \
  --image ghcr.io/clemensv/real-time-sources/meteoalarm:latest \
  --environment-variables CONNECTION_STRING="<cs>" \
  --restart-policy Always
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-with-eventhub.json)
