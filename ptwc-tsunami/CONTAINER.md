<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Pacific and Atlantic" width="64" height="48"><br>
<sub><b>Pacific and Atlantic</b></sub>
</td>
<td valign="middle">

# PTWC Tsunami

<sub>NOAA tsunami bulletins · Kafka · MQTT · AMQP · <a href="https://www.tsunami.gov/">upstream</a> · <a href="https://www.tsunami.gov/?page=message_definitions">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Pacific and Atlantic — NOAA tsunami bulletins

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#ptwc-tsunami) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/ptwc_tsunami.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.tsunami.gov/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI images for the PTWC Tsunami feeder and their runtime contract. See [README.md](README.md) for source overview and [EVENTS.md](EVENTS.md) for the CloudEvents schema/routing contract.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.tsunami.gov/>
- API / data documentation: <https://www.tsunami.gov/?page=message_definitions>

<!-- upstream-links:end -->

## Why this container

These images package the upstream connector, CloudEvents normalization, and transport-specific publisher wiring into ready-to-run artifacts for Kafka, MQTT/UNS, AMQP deployments.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-ptwc-tsunami` | Kafka | Topic(s): `ptwc-tsunami`, key = `{bulletin_id}` |
| `ghcr.io/clemensv/real-time-sources-ptwc-tsunami-mqtt` | MQTT 5.0 | Topic template `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin` |
| `ghcr.io/clemensv/real-time-sources-ptwc-tsunami-amqp` | AMQP 1.0 | Address `ptwc-tsunami` |

Event families (base groups):

- `PTWC.Bulletins`

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.12-slim` |
| Default entry point | Kafka: `["python", "-m", "ptwc_tsunami"]`; MQTT: `["python", "-m", "ptwc_tsunami_mqtt", "feed"]`; AMQP: `["python", "-m", "ptwc_tsunami_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | graceful shutdown on `SIGTERM` |
| State | `PTWC_TSUNAMI_MQTT_STATE_FILE`, `PTWC_TSUNAMI_STATE_FILE` |
| Image tags | `:latest`, `:sha-<git-sha>`, release tags |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-ptwc-tsunami:latest
docker pull ghcr.io/clemensv/real-time-sources-ptwc-tsunami-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-ptwc-tsunami-amqp:latest
```

## Using the Kafka image

### With Azure Event Hubs / Fabric Event Streams (connection string)

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-ptwc-tsunami:latest
```

### With Kafka broker parameters (SASL/PLAIN)

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<host:port>' \
  -e KAFKA_TOPIC='ptwc-tsunami' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-ptwc-tsunami:latest
```

## Using the MQTT image

### With generic MQTT broker (username/password)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-ptwc-tsunami-mqtt:latest
```

### With Azure Event Grid MQTT broker (Microsoft Entra)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-ptwc-tsunami-mqtt:latest
```

## Using the AMQP image

### With generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/ptwc-tsunami' \
  ghcr.io/clemensv/real-time-sources-ptwc-tsunami-amqp:latest
```

### With Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='ptwc-tsunami' \
  -e AMQP_AUTH_MODE=entra \
  ghcr.io/clemensv/real-time-sources-ptwc-tsunami-amqp:latest
```

### With SAS-token CBS (Service Bus emulator / SAS-only)

```bash
docker run --rm \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='ptwc-tsunami' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-ptwc-tsunami-amqp:latest
```

## Environment variables

### Common

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string for Kafka-mode publishing. |
| `KAFKA_ENABLE_TLS` | Set `false` for local/plain Kafka; default `true`. |
| `PTWC_TSUNAMI_MQTT_STATE_FILE` | Source-specific state/resume setting. |
| `PTWC_TSUNAMI_STATE_FILE` | Source-specific state/resume setting. |

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
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventhub.json)
- **azure-template-with-servicebus.json** (with servicebus)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-servicebus.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview and quick-start guidance.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schemas.
- [`xreg/ptwc_tsunami.xreg.json`](xreg/ptwc_tsunami.xreg.json) — authoritative xRegistry manifest.
