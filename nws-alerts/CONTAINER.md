# NWS Alerts Container

## Quick Start

```bash
docker build -t nws-alerts .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" nws-alerts

# MQTT/UNS image
docker build -f Dockerfile.mqtt -t nws-alerts-mqtt .
docker run --rm -e MQTT_BROKER_URL="mqtt://broker:1883" nws-alerts-mqtt
```

## Description

This container bridges active weather alerts from the US National Weather
Service (NWS) to Kafka-compatible endpoints (Apache Kafka, Azure Event Hubs,
Microsoft Fabric Event Streams) as CloudEvents. The sibling `Dockerfile.mqtt`
image publishes the same alert payloads to MQTT 5.0 Unified Namespace brokers.

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
| `MQTT_BROKER_URL` | MQTT only | Broker URL (default: `mqtt://localhost:1883`) |
| `MQTT_AUTH_MODE` | MQTT only | `anonymous`, `userpass`, `tls-cert`, or `entra` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | MQTT only | Username/password credentials |
| `NWS_ALERTS_MQTT_EMIT_MOCK_CORPUS` | MQTT only | Emit five synthetic alerts, one per severity, then exit |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` is required for the Kafka image.

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

## MQTT and AMQP images

The source ships separate Kafka, MQTT, and AMQP containers. The AMQP image targets generic AMQP 1.0 brokers with SASL PLAIN or Azure Service Bus with Entra/SAS CBS authentication.

```bash
docker build -f Dockerfile.amqp -t nws-alerts-amqp .
docker run --rm -e AMQP_HOST=broker -e AMQP_PORT=5672 -e AMQP_ADDRESS=nws-alerts -e AMQP_USERNAME=admin -e AMQP_PASSWORD=admin nws-alerts-amqp
```

| Variable | Required | Description |
|---|---|---|
| `AMQP_BROKER_URL` | AMQP only | Broker URL, optionally including `/address` |
| `AMQP_HOST` / `AMQP_PORT` | AMQP only | Broker host and port when no URL is supplied |
| `AMQP_ADDRESS` | AMQP only | Queue/topic address, default `nws-alerts` |
| `AMQP_AUTH_MODE` | AMQP only | `password`, `entra`, or `sas` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | password | SASL PLAIN credentials |
| `AMQP_ENTRA_CLIENT_ID` | entra | Optional user-assigned managed identity client id |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | sas | Shared Access Signature credentials |
| `NWS_ALERTS_AMQP_EMIT_MOCK_CORPUS` | tests | Emit five synthetic alerts and exit |

Deploy MQTT with `azure-template-mqtt.json` or `azure-template-with-eventgrid-mqtt.json`; deploy AMQP with `azure-template-with-servicebus.json` (mirrored at `infra/azure-template-amqp.json`).
