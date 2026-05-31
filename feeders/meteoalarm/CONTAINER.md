<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/eu.png" alt="Europe" width="64" height="48"><br>
<sub><b>Europe</b></sub>
</td>
<td valign="middle">

# Meteoalarm

<sub>37 countries, severe weather warnings · Kafka · MQTT · AMQP · <a href="https://meteoalarm.org/">upstream</a> · <a href="https://feeds.meteoalarm.org/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Europe — 37 countries, severe weather warnings

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#meteoalarm) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/meteoalarm.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://meteoalarm.org/)

</td></tr></table>
<!-- source-hero:end -->

## Quick Start

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://meteoalarm.org/>
- API / data documentation: <https://feeds.meteoalarm.org/>

<!-- upstream-links:end -->

```bash
docker build -t meteoalarm .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" meteoalarm
```

## Description

This container bridges severe weather warnings from the EUMETNET Meteoalarm
system to Kafka-compatible endpoints (Apache Kafka, Azure Event Hubs,
Microsoft Fabric Event Streams), MQTT 5.0, and AMQP 1.0 as CloudEvents.

It polls the Meteoalarm JSON API for warnings from 30+ European national
meteorological services and emits them as structured CloudEvents using the
CAP (Common Alerting Protocol) schema.

## Image contract

| Image tag | Transport | Dockerfile | Persistent state share |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-meteoalarm:latest` | Kafka / Event Hubs | `Dockerfile` | Yes - stores `METEOALARM_STATE_FILE` dedupe state |
| `ghcr.io/clemensv/real-time-sources-meteoalarm-mqtt:latest` | MQTT 5 | `Dockerfile.mqtt` | No |
| `ghcr.io/clemensv/real-time-sources-meteoalarm-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | Yes - stores `STATE_FILE` dedupe state |

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes* | Event Hubs / Fabric connection string |
| `METEOALARM_CONNECTION_STRING` | No | Feeder-prefixed alias for `CONNECTION_STRING`; useful in Azure templates and orchestrators that standardize source-local settings. |
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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fmeteoalarm%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fmeteoalarm%2Fazure-template-with-eventhub.json)

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-meteoalarm-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `Meteoalarm.Warnings.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-meteoalarm-mqtt:latest
```

### MQTT environment variables

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL including host, port, and TLS scheme, for example `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional username/password credentials for brokers that require user authentication. Leave unset for anonymous brokers. |
| `MQTT_CLIENT_ID` | Optional MQTT client identifier. Set it explicitly on shared brokers and Event Grid namespaces. |
| `MQTT_CONTENT_MODE` | CloudEvents content mode, `binary` by default. Keep `binary` for MQTT 5 user-property metadata. |
| `POLLING_INTERVAL` | Source polling interval in seconds, when supported by the feeder. |
| `STATE_FILE` | Optional path for source dedupe/checkpoint state, when the feeder maintains local state. |
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `alerts/intl/meteoalarm/meteoalarm`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning` | `Meteoalarm.WeatherWarning` | `false` | `1` | `` |

### Subscription patterns

```text
# Everything from this source
alerts/intl/meteoalarm/meteoalarm/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fmeteoalarm%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fmeteoalarm%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP 1.0 container variant

Image: `ghcr.io/clemensv/real-time-sources-meteoalarm-amqp:latest`

The AMQP companion publishes Meteoalarm CloudEvents to generic AMQP 1.0 brokers with SASL PLAIN, Azure Service Bus with Entra ID CBS, or Service Bus-compatible SAS CBS. It uses the same event schemas as the Kafka and MQTT variants.

### Generic AMQP broker

```bash
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=meteoalarm \
  -e AMQP_USERNAME=admin \
  -e AMQP_PASSWORD=admin \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-meteoalarm-amqp:latest
```

### Azure Service Bus with Entra ID

```bash
docker run --rm \
  -e AMQP_HOST=<namespace>.servicebus.windows.net \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS=meteoalarm \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default \
  -e AMQP_ENTRA_CLIENT_ID=<managed-identity-client-id> \
  ghcr.io/clemensv/real-time-sources-meteoalarm-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm \
  -e AMQP_HOST=servicebus-emulator \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=meteoalarm \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey \
  -e AMQP_SAS_KEY=<key> \
  ghcr.io/clemensv/real-time-sources-meteoalarm-amqp:latest
```

| Variable | Description | Default |
| --- | --- | --- |
| `AMQP_BROKER_URL` | Optional `amqp://` or `amqps://` URL; path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | AMQP broker host and port when no broker URL is supplied. | `localhost` / `5672` (`5671` with TLS) |
| `AMQP_ADDRESS` | Queue, topic, or link target address. | `meteoalarm` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_TLS` | Enable TLS; automatically true for Entra auth. | `false` |
| `AMQP_ENTRA_AUDIENCE` | Token scope for CBS put-token. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials for Service Bus-compatible brokers. | empty |
| `AMQP_CONTENT_MODE` | CloudEvents AMQP content mode. | `binary` |
| `POLLING_INTERVAL` | Poll interval in seconds. | source-specific |
| `METEOALARM_POLL_INTERVAL` | Feeder-prefixed alias for `POLLING_INTERVAL`; useful in Azure templates that surface Meteoalarm-specific settings. | source-specific |
| `METEOALARM_COUNTRIES` | Comma-separated ISO country codes to limit which Meteoalarm national warning feeds are polled. | all Meteoalarm countries |
| `STATE_FILE` | Persistent dedupe state file path. | source-specific |
| `METEOALARM_MOCK` | Emit built-in sample events for Docker E2E and offline validation. | `false` |

Use `azure-template-with-servicebus.json` or `infra/azure-template-amqp.json` for one-click Azure Service Bus deployment. The templates create a queue, Azure Files state share, ACI, user-assigned managed identity, and `Azure Service Bus Data Sender` role assignment scoped to the queue.
