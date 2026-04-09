# NINA/BBK Container

## Quick Start

```bash
docker build -t nina-bbk .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" nina-bbk
```

## Description

This container bridges civil protection warnings from Germany's NINA/BBK
system to Kafka-compatible endpoints (Apache Kafka, Azure Event Hubs,
Microsoft Fabric Event Streams) as CloudEvents.

It polls all six NINA providers (MOWAS, KATWARN, BIWAPP, DWD, LHP, Police)
for active warnings, fetches full CAP details, and emits them as structured
CloudEvents.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes* | Event Hubs / Fabric connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes* | Kafka bootstrap servers |
| `KAFKA_TOPIC` | No | Topic name (default: `nina-bbk`) |
| `SASL_USERNAME` | No | SASL username |
| `SASL_PASSWORD` | No | SASL password |
| `NINA_BBK_STATE_FILE` | No | State file (default: `~/.nina_bbk_state.json`) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` is required.

## Azure Container Instance

```bash
az container create \
  --resource-group <rg> \
  --name nina-bbk \
  --image ghcr.io/clemensv/real-time-sources/nina-bbk:latest \
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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-with-eventhub.json)
