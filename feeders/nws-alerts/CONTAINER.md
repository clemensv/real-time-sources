<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="United States" width="64" height="48"><br>
<sub><b>United States</b></sub>
</td>
<td valign="middle">

# NWS CAP Alerts

<sub>active alerts via api.weather.gov · Kafka · MQTT · AMQP · <a href="https://www.weather.gov/">upstream</a> · <a href="https://www.weather.gov/documentation/services-web-api">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> United States — active alerts via api.weather.gov

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#nws-alerts) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/nws-alerts.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.weather.gov/)

</td></tr></table>
<!-- source-hero:end -->

## Quick Start

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.weather.gov/>
- API / data documentation: <https://www.weather.gov/documentation/services-web-api>

<!-- upstream-links:end -->

```bash
docker build -t nws-alerts .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" nws-alerts

# MQTT/UNS image
docker build -f Dockerfile.mqtt -t nws-alerts-mqtt .
docker run --rm -e MQTT_BROKER_URL="mqtt://broker:1883" nws-alerts-mqtt
```

## Image contract

| Image tag | Transport | Dockerfile | Persistent state share |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-nws-alerts:latest` | Kafka / Event Hubs | `Dockerfile` | Yes - stores `NWS_ALERTS_STATE_FILE` dedupe state |
| `ghcr.io/clemensv/real-time-sources-nws-alerts-mqtt:latest` | MQTT 5 | `Dockerfile.mqtt` | No |
| `ghcr.io/clemensv/real-time-sources-nws-alerts-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | Yes - stores `STATE_FILE` dedupe state |

## Description

This container bridges active weather alerts from the US National Weather
Service (NWS) to Kafka-compatible endpoints (Apache Kafka, Azure Event Hubs,
Microsoft Fabric Event Streams) as CloudEvents. The sibling `Dockerfile.mqtt`
image publishes the same alert payloads to MQTT 5.0 Unified Namespace brokers.

It polls the NWS alerts API for current warnings, watches, and advisories
across the United States and emits them as structured CloudEvents using the
CAP (Common Alerting Protocol) schema with SAME/UGC geocodes.

## Environment Variables

### Common (all images)

| Variable | Description |
|---|---|
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |

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
| `NWS_CONNECTION_STRING` | No | Source-specific override for the Kafka / Event Hubs connection string; falls back to `CONNECTION_STRING`. |
| `NWS_STATE_FILE` | No | State-file path used by the MQTT and AMQP images (the Kafka image uses `NWS_ALERTS_STATE_FILE`). |
| `POLLING_INTERVAL` | No | Seconds between alert polls. |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` is required for the Kafka image.


### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra ID (Azure Event Grid). |
| `MQTT_CLIENT_ID` | MQTT client identifier. |
| `MQTT_ENABLE_TLS` | Set `true` to use TLS (`mqtts`) for the MQTT connection. |
| `MQTT_CA_FILE` | Path to a CA certificate bundle for verifying the broker's TLS certificate. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |
| `MQTT_CLIENT_CERT` | Path to a client certificate for mutual-TLS authentication. |
| `MQTT_CLIENT_KEY` | Path to the client private key for mutual-TLS authentication. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_HOST` | AMQP broker host (component-level alternative to `AMQP_BROKER_URL`). |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name to publish to. |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS. |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `AMQP_PORT` | AMQP broker port (default `5672`, or `5671` with TLS). |
| `AMQP_TLS` | Set `true` to use TLS (`amqps`) for the component-level connection. |
| `AMQP_USERNAME` | SASL PLAIN username, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_PASSWORD` | SASL PLAIN password, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). Required when `AMQP_AUTH_MODE=sas`. |


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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnws-alerts%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnws-alerts%2Fazure-template-with-eventhub.json)

## AMQP 1.0 companion

This source also ships an AMQP 1.0 companion feeder (`Dockerfile.amqp`) alongside the Kafka and MQTT variants. It publishes the same CloudEvents to a single AMQP address named after the source, with CloudEvent `subject` and AMQP application properties mirroring the Kafka key/MQTT topic axes for broker-side filtering. Use `azure-template-with-servicebus.json` to deploy the AMQP feeder to Azure Service Bus with Entra ID/CBS authentication, or set `AMQP_BROKER_URL` for a generic AMQP 1.0 broker.
