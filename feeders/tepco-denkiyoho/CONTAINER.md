<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/jp.png" alt="Japan / Kanto" width="64" height="48"><br>
<sub><b>Japan / Kanto</b></sub>
</td>
<td valign="middle">

# TEPCO Denkiyoho

<sub>TEPCO electricity supply, hourly forecast, 5-min actuals + solar · Kafka · MQTT · AMQP · <a href="https://www.tepco.co.jp/forecast/">upstream</a> · <a href="https://www.tepco.co.jp/forecast/html/download-j.html">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-4_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Japan / Kanto — TEPCO electricity supply, hourly forecast, 5-min actuals + solar

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#tepco-denkiyoho) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#tepco-denkiyoho/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/tepco-denkiyoho.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.tepco.co.jp/forecast/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published container images for the TEPCO Denkiyoho feeder. For overview and business context see [README.md](README.md); for event-contract details see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.tepco.co.jp/forecast/>
- API / data documentation: <https://www.tepco.co.jp/forecast/html/download-j.html>

<!-- upstream-links:end -->

## Why this container

TEPCO demand/supply telemetry is used in Kanto-region power operations and forecasting. This feeder normalizes the CSV stream into CloudEvents across Kafka, MQTT, and AMQP.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-tepco-denkiyoho` | Kafka | Polls upstream and publishes CloudEvents to one topic |
| `ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-mqtt` | MQTT 5.0 | Publishes CloudEvents to xRegistry-mapped topics |
| `ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-amqp` | AMQP 1.0 | Publishes CloudEvents to one AMQP address |

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.10-slim` |
| Default entrypoint | `python -m tepco_denkiyoho feed; python -m tepco_denkiyoho_mqtt feed; python -m tepco_denkiyoho_amqp feed` |
| Exposed ports | none — outbound publisher only |
| Signals | exits on `SIGTERM`; in-flight poll cycle is completed/flushed before shutdown where supported |
| State | Kafka: STATE_FILE; MQTT: Not used; AMQP: Not used. Mount `/state` when state is used. |
| Tags | `:latest` (mainline), plus immutable release/SHA tags published in GHCR. |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-tepco-denkiyoho:latest
docker pull ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/tepco-denkiyoho.json \
  -e KAFKA_BOOTSTRAP_SERVERS='<broker:9093>' \
  -e KAFKA_TOPIC='<topic>' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho:latest
```

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/tepco-denkiyoho.json \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho:latest
```

## Using the MQTT image

### With username/password authentication

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Entra)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-mqtt:latest
```

## Using the AMQP image

### With Microsoft Entra ID (AMQP CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='tepco-denkiyoho' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-amqp:latest
```

### With SAS token CBS (Service Bus emulator / SAS-only namespaces)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='tepco-denkiyoho' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho-amqp:latest
```

## Environment variables

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style or Kafka-style connection string. |
| `TEPCO_DENKIYOHO_URL` | Override URL for the upstream TEPCO CSV endpoint. Defaults to the published daily CSV URL. |
| `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC` | Explicit Kafka destination. |
| `SASL_USERNAME`, `SASL_PASSWORD` | SASL PLAIN credentials when needed. |
| `KAFKA_ENABLE_TLS` | Set `false` for plaintext Kafka. |
| `ONCE_MODE` | Run one cycle and exit (where supported). |
| State variable | `STATE_FILE` |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `TEPCO_DENKIYOHO_URL` | Override URL for the upstream TEPCO CSV endpoint. Defaults to the published daily CSV URL. |
| `MQTT_USERNAME`, `MQTT_PASSWORD` | Optional broker credentials. |
| `MQTT_CLIENT_ID` | Optional explicit client ID. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` where supported. |
| State variable | Not used by current MQTT companion app |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL (`amqp://` or `amqps://`). |
| `TEPCO_DENKIYOHO_URL` | Override URL for the upstream TEPCO CSV endpoint. Defaults to the published daily CSV URL. |
| `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS` | Component-level AMQP endpoint settings. |
| `AMQP_USERNAME`, `AMQP_PASSWORD` | SASL PLAIN credentials (if used). |
| `AMQP_AUTH_MODE` | Auth mode where supported (`password`/`entra`/`sas`). |
| `AMQP_TLS` | Enable TLS where supported. |
| State variable | Not used by current AMQP companion app |

## Deploying into Microsoft Fabric

Fabric notebook and Fabric ACI hosting are both supported:

- Notebook: `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source tepco-denkiyoho ...`
- ACI: `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source tepco-denkiyoho ...`

Portal links:

- [Fabric Notebook](https://clemensv.github.io/real-time-sources/#tepco-denkiyoho/fabric-notebook)
- [Fabric ACI](https://clemensv.github.io/real-time-sources/#tepco-denkiyoho/fabric-aci)

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftepco-denkiyoho%2Fazure-template.json)

### AMQP — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftepco-denkiyoho%2Fazure-template-amqp.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftepco-denkiyoho%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftepco-denkiyoho%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftepco-denkiyoho%2Fazure-template-with-servicebus.json)

## Related
- [README.md](README.md) — source overview, use cases, and quick start.
- [EVENTS.md](EVENTS.md) — event contract and schema details.
- [`xreg/tepco-denkiyoho.xreg.json`](xreg/tepco-denkiyoho.xreg.json) — authoritative manifest.
