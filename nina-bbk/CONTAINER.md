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
