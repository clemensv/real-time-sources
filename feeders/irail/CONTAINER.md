<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/be.png" alt="Belgium" width="64" height="48"><br>
<sub><b>Belgium</b></sub>
</td>
<td valign="middle">

# iRail

<sub>~600 NMBS/SNCB stations, departures, delays · Kafka · MQTT · AMQP · <a href="https://irail.be/">upstream</a> · <a href="https://docs.irail.be/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Belgium — ~600 NMBS/SNCB stations, departures, delays

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#irail) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#irail/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/irail.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://irail.be/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published container images for the iRail feeder. For overview and business context see [README.md](README.md); for event-contract details see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://irail.be/>
- API / data documentation: <https://docs.irail.be/>

<!-- upstream-links:end -->

## Why this container

iRail publishes live NMBS/SNCB station-board data for the Belgian rail network. This feeder republishes it as CloudEvents so operations and analytics teams subscribe to streams instead of polling hundreds of stations directly.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-irail` | Kafka | Polls upstream and publishes CloudEvents to one topic |
| `ghcr.io/clemensv/real-time-sources-irail-mqtt` | MQTT 5.0 | Publishes CloudEvents to xRegistry-mapped topics |
| `ghcr.io/clemensv/real-time-sources-irail-amqp` | AMQP 1.0 | Publishes CloudEvents to one AMQP address |

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.10-slim` |
| Default entrypoint | `python -m irail feed; python -m irail_mqtt feed; python -m irail_amqp feed` |
| Exposed ports | none — outbound publisher only |
| Signals | exits on `SIGTERM`; in-flight poll cycle is completed/flushed before shutdown where supported |
| State | Kafka: STATE_FILE; MQTT: STATE_FILE; AMQP: STATE_FILE. Mount `/state` when state is used. |
| Tags | `:latest` (mainline), plus immutable release/SHA tags published in GHCR. |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-irail:latest
docker pull ghcr.io/clemensv/real-time-sources-irail-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-irail-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/irail.json \
  -e KAFKA_BOOTSTRAP_SERVERS='<broker:9093>' \
  -e KAFKA_TOPIC='<topic>' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-irail:latest
```

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/irail.json \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-irail:latest
```

## Using the MQTT image

### With username/password authentication

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/irail-mqtt.json \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-irail-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Entra)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/irail-mqtt.json \
  -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-irail-mqtt:latest
```

## Using the AMQP image

### With Microsoft Entra ID (AMQP CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/irail-amqp.json \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='irail' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-irail-amqp:latest
```

### With SAS token CBS (Service Bus emulator / SAS-only namespaces)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/irail-amqp.json \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='irail' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-irail-amqp:latest
```

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `LOG_LEVEL` | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `POLLING_INTERVAL` | Seconds between polling cycles. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Source configuration

| Variable | Description |
|---|---|
| `STATION_FILTER` | Comma-separated station IDs or names to include; empty includes all stations. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style or Kafka-style connection string. |
| `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC` | Explicit Kafka destination. |
| `SASL_USERNAME`, `SASL_PASSWORD` | SASL PLAIN credentials when needed. |
| `KAFKA_ENABLE_TLS` | Set `false` for plaintext Kafka. |
| `ONCE_MODE` | Run one cycle and exit (where supported). |
| State variable | `STATE_FILE` |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_USERNAME`, `MQTT_PASSWORD` | Optional broker credentials. |
| `MQTT_CLIENT_ID` | Optional explicit client ID. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` where supported. |
| State variable | `STATE_FILE` |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL (`amqp://` or `amqps://`). |
| `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS` | Component-level AMQP endpoint settings. |
| `AMQP_USERNAME`, `AMQP_PASSWORD` | SASL PLAIN credentials (if used). |
| `AMQP_AUTH_MODE` | Auth mode where supported (`password`/`entra`/`sas`). |
| `AMQP_TLS` | Enable TLS where supported. |
| State variable | `STATE_FILE` |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

## Deploying into Microsoft Fabric

Fabric notebook and Fabric ACI hosting are both supported:

- Notebook: `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source irail ...`
- ACI: `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source irail ...`

Portal links:

- [Fabric Notebook](https://clemensv.github.io/real-time-sources/#irail/fabric-notebook)
- [Fabric ACI](https://clemensv.github.io/real-time-sources/#irail/fabric-aci)

## Deploying into Azure Container Instances

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Firail%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Firail%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Firail%2Fazure-template.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Firail%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Firail%2Fazure-template-with-eventgrid-mqtt.json)

## Related
- [README.md](README.md) — source overview, use cases, and quick start.
- [EVENTS.md](EVENTS.md) — event contract and schema details.
- [`xreg/irail.xreg.json`](xreg/irail.xreg.json) — authoritative manifest.
