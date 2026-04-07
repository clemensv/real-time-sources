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
