<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/nl.png" alt="Netherlands" width="64" height="48"><br>
<sub><b>Netherlands</b></sub>
</td>
<td valign="middle">

# NDW Road Traffic

<sub>national road traffic, DATEX II XML · Kafka · MQTT · AMQP · <a href="https://www.ndw.nu/">upstream</a> · <a href="https://opendata.ndw.nu/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-4_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Netherlands — national road traffic, DATEX II XML

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#ndw-road-traffic) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/ndw-road-traffic.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.ndw.nu/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI images for the NDW Road Traffic feeder and their runtime contract. See [README.md](README.md) for source overview and [EVENTS.md](EVENTS.md) for the CloudEvents schema/routing contract.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.ndw.nu/>
- API / data documentation: <https://opendata.ndw.nu/>

<!-- upstream-links:end -->

## Why this container

These images package the upstream connector, CloudEvents normalization, and transport-specific publisher wiring into ready-to-run artifacts for Kafka, MQTT/UNS, AMQP deployments.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-ndw-road-traffic` | Kafka | Topic(s): `ndw-road-traffic`, key = `drips/{vms_controller_id}/{vms_index}`, `measurement-sites/{measurement_site_id}`, `msi-signs/{sign_id}`, `situations/{situation_record_id}` |
| `ghcr.io/clemensv/real-time-sources-ndw-road-traffic-mqtt` | MQTT 5.0 | Topic template `traffic/nl/ndw/ndw-road-traffic/drips/{road}/{vms_controller_id}/{vms_index}/display-state` |
| `ghcr.io/clemensv/real-time-sources-ndw-road-traffic-amqp` | AMQP 1.0 | Address `ndw-road-traffic` |

Event families (base groups):

- `NL.NDW.AVG`
- `NL.NDW.DRIP`
- `NL.NDW.MSI`
- `NL.NDW.Situations`

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.12-slim` |
| Default entry point | Kafka: `["python", "-m", "ndw_road_traffic"]`; MQTT: `["python", "-m", "ndw_road_traffic_mqtt", "feed"]`; AMQP: `["python", "-m", "ndw_road_traffic_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | graceful shutdown on `SIGTERM` |
| State | none required (streaming bridge) |
| Image tags | `:latest`, `:sha-<git-sha>`, release tags |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-ndw-road-traffic:latest
docker pull ghcr.io/clemensv/real-time-sources-ndw-road-traffic-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-ndw-road-traffic-amqp:latest
```

## Using the Kafka image

### With Azure Event Hubs / Fabric Event Streams (connection string)

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-ndw-road-traffic:latest
```

### With Kafka broker parameters (SASL/PLAIN)

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<host:port>' \
  -e KAFKA_TOPIC='ndw-road-traffic' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-ndw-road-traffic:latest
```

## Using the MQTT image

### With generic MQTT broker (username/password)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-ndw-road-traffic-mqtt:latest
```

### With Azure Event Grid MQTT broker (Microsoft Entra)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-ndw-road-traffic-mqtt:latest
```

## Using the AMQP image

### With generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/ndw-road-traffic' \
  ghcr.io/clemensv/real-time-sources-ndw-road-traffic-amqp:latest
```

### With Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='ndw-road-traffic' \
  -e AMQP_AUTH_MODE=entra \
  ghcr.io/clemensv/real-time-sources-ndw-road-traffic-amqp:latest
```

### With SAS-token CBS (Service Bus emulator / SAS-only)

```bash
docker run --rm \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='ndw-road-traffic' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-ndw-road-traffic-amqp:latest
```

## Environment variables

### Common

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string for Kafka-mode publishing. |
| `KAFKA_ENABLE_TLS` | Set `false` for local/plain Kafka; default `true`. |

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

- **azure-template-mqtt.json** (mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-mqtt.json)
- **azure-template-with-eventgrid-mqtt.json** (with eventgrid mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-with-eventgrid-mqtt.json)
- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview and quick-start guidance.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schemas.
- [`xreg/ndw-road-traffic.xreg.json`](xreg/ndw-road-traffic.xreg.json) — authoritative xRegistry manifest.
