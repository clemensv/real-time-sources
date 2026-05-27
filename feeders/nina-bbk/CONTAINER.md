<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/de.png" alt="Germany" width="64" height="48"><br>
<sub><b>Germany</b></sub>
</td>
<td valign="middle">

# NINA/BBK

<sub>MOWAS, KATWARN, BIWAPP, DWD, LHP, Police · Kafka · MQTT · AMQP · <a href="https://warnung.bund.de/">upstream</a> · <a href="https://nina.api.bund.dev/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Germany — MOWAS, KATWARN, BIWAPP, DWD, LHP, Police

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#nina-bbk) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/nina_bbk.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://warnung.bund.de/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI images for the NINA/BBK feeder and their runtime contract. See [README.md](README.md) for source overview and [EVENTS.md](EVENTS.md) for the CloudEvents schema/routing contract.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://warnung.bund.de/>
- API / data documentation: <https://nina.api.bund.dev/>

<!-- upstream-links:end -->

## Why this container

These images package the upstream connector, CloudEvents normalization, and transport-specific publisher wiring into ready-to-run artifacts for Kafka, MQTT/UNS, AMQP deployments.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-nina-bbk` | Kafka | Topic(s): `nina-bbk`, key = `{warning_id}` |
| `ghcr.io/clemensv/real-time-sources-nina-bbk-mqtt` | MQTT 5.0 | Topic template `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning` |
| `ghcr.io/clemensv/real-time-sources-nina-bbk-amqp` | AMQP 1.0 | Address `nina-bbk` |

Event families (base groups):

- `NINA.Warnings`

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.12-slim` |
| Default entry point | Kafka: `["python", "-m", "nina_bbk"]`; MQTT: `["python", "-m", "nina_bbk_mqtt", "feed"]`; AMQP: `["python", "-m", "nina_bbk_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | graceful shutdown on `SIGTERM` |
| State | `NINA_BBK_MQTT_STATE_FILE`, `NINA_BBK_STATE_FILE` |
| Image tags | `:latest`, `:sha-<git-sha>`, release tags |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-nina-bbk:latest
docker pull ghcr.io/clemensv/real-time-sources-nina-bbk-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-nina-bbk-amqp:latest
```

## Using the Kafka image

### With Azure Event Hubs / Fabric Event Streams (connection string)

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-nina-bbk:latest
```

### With Kafka broker parameters (SASL/PLAIN)

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<host:port>' \
  -e KAFKA_TOPIC='nina-bbk' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-nina-bbk:latest
```

## Using the MQTT image

### With generic MQTT broker (username/password)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-nina-bbk-mqtt:latest
```

### With Azure Event Grid MQTT broker (Microsoft Entra)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-nina-bbk-mqtt:latest
```

## Using the AMQP image

### With generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/nina-bbk' \
  ghcr.io/clemensv/real-time-sources-nina-bbk-amqp:latest
```

### With Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='nina-bbk' \
  -e AMQP_AUTH_MODE=entra \
  ghcr.io/clemensv/real-time-sources-nina-bbk-amqp:latest
```

### With SAS-token CBS (Service Bus emulator / SAS-only)

```bash
docker run --rm \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='nina-bbk' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-nina-bbk-amqp:latest
```

## Environment variables

### Common

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string for Kafka-mode publishing. |
| `KAFKA_ENABLE_TLS` | Set `false` for local/plain Kafka; default `true`. |
| `NINA_BBK_MQTT_STATE_FILE` | Source-specific state/resume setting. |
| `NINA_BBK_STATE_FILE` | Source-specific state/resume setting. |

### Kafka image

| Variable | Description |
|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list (`host:port,...`). |
| `KAFKA_TOPIC` | Destination topic (default from contract). |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials for Kafka-compatible brokers. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URI (`mqtt://` or `mqtts://`). |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for password mode. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for Microsoft Entra JWT. |
| `MQTT_CLIENT_ID` | Client identifier; must be unique per broker namespace. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Full AMQP URI (`amqp://` or `amqps://`). |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | Target queue/topic/address. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra ID token settings for CBS auth mode. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS-token settings for SAS CBS auth mode. |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

## Deploying into Azure Container Instances

One deploy button is provided per ARM template file present in this folder:

- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnina-bbk%2Fazure-template-with-eventhub.json)
- **azure-template-with-servicebus.json** (with servicebus)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnina-bbk%2Fazure-template-with-servicebus.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnina-bbk%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview and quick-start guidance.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schemas.
- [`xreg/nina_bbk.xreg.json`](xreg/nina_bbk.xreg.json) — authoritative xRegistry manifest.
