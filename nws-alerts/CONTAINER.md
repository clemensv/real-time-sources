# NWS Alerts Container

## Quick Start

```bash
docker build -t nws-alerts .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" nws-alerts
```

## Description

This container bridges active weather alerts from the US National Weather
Service (NWS) to Kafka-compatible endpoints (Apache Kafka, Azure Event Hubs,
Microsoft Fabric Event Streams) as CloudEvents.

It polls the NWS alerts API for current warnings, watches, and advisories
across the United States and emits them as structured CloudEvents using the
CAP (Common Alerting Protocol) schema with SAME/UGC geocodes.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes* | Event Hubs / Fabric connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes* | Kafka bootstrap servers |
| `KAFKA_TOPIC` | No | Topic name (default: `nws-alerts`) |
| `SASL_USERNAME` | No | SASL username |
| `SASL_PASSWORD` | No | SASL password |
| `NWS_ALERTS_STATE_FILE` | No | State file (default: `~/.nws_alerts_state.json`) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` is required.

## Azure Container Instance

```bash
az container create \
  --resource-group <rg> \
  --name nws-alerts \
  --image ghcr.io/clemensv/real-time-sources/nws-alerts:latest \
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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-with-eventhub.json)
