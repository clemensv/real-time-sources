# PTWC Tsunami Container

## Quick Start

```bash
docker build -t ptwc-tsunami .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" ptwc-tsunami
```

## Description

This container bridges tsunami bulletins from NOAA's National Tsunami Warning
Center (NTWC) and Pacific Tsunami Warning Center (PTWC) to Kafka-compatible
endpoints (Apache Kafka, Azure Event Hubs, Microsoft Fabric Event Streams) as
CloudEvents.

It polls two Atom XML feeds for seismic event bulletins, parses the XHTML
summaries for structured fields (category, magnitude, affected region), and
emits them as CloudEvents.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes* | Event Hubs / Fabric connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes* | Kafka bootstrap servers |
| `KAFKA_TOPIC` | No | Topic name (default: `ptwc-tsunami`) |
| `SASL_USERNAME` | No | SASL username |
| `SASL_PASSWORD` | No | SASL password |
| `PTWC_TSUNAMI_STATE_FILE` | No | State file (default: `~/.ptwc_tsunami_state.json`) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` is required.

## Azure Container Instance

```bash
az container create \
  --resource-group <rg> \
  --name ptwc-tsunami \
  --image ghcr.io/clemensv/real-time-sources/ptwc-tsunami:latest \
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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventhub.json)
