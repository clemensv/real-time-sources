<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/nl.png" alt="Netherlands" width="64" height="48"><br>
<sub><b>Netherlands</b></sub>
</td>
<td valign="middle">

# Luchtmeetnet Netherlands

<sub>station measurements, components, LKI index · Kafka · MQTT · AMQP · <a href="https://www.luchtmeetnet.nl/">upstream</a> · <a href="https://api-docs.luchtmeetnet.nl/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Netherlands — station measurements, components, LKI index

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#luchtmeetnet-nl) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#luchtmeetnet-nl/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/luchtmeetnet-nl.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.luchtmeetnet.nl/)

</td></tr></table>
<!-- source-hero:end -->

This document describes the published OCI images for the Luchtmeetnet Netherlands feeder. For solution overview and usage scenarios, see [README.md](README.md). For the CloudEvents contract and schemas, see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.luchtmeetnet.nl/>
- API / data documentation: <https://api-docs.luchtmeetnet.nl/>

<!-- upstream-links:end -->

## Why this container

These images package the poller, normalization logic, and transport producers so teams can subscribe to standardized air-quality CloudEvents without writing their own ingestion pipeline.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl` | Kafka | Poll upstream and publish CloudEvents to one Kafka topic with xRegistry keying |
| `ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-mqtt` | MQTT 5.0 | Poll upstream and publish CloudEvents to MQTT topic hierarchy |
| `ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-amqp` | AMQP 1.0 | Poll upstream and publish CloudEvents to a configured AMQP address |

Event families in this source:

- **`nl.rivm.luchtmeetnet`**: Station, Measurement, LKI
- **`nl.rivm.luchtmeetnet.components`**: Component
- **`nl.rivm.luchtmeetnet.mqtt`**: Station, Measurement, LKI
- **`nl.rivm.luchtmeetnet.amqp`**: Station, Measurement, LKI
- **`nl.rivm.luchtmeetnet.components.mqtt`**: Component
- **`nl.rivm.luchtmeetnet.components.amqp`**: Component

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.10-slim` |
| Kafka entrypoint | `python -m luchtmeetnet_nl` |
| MQTT entrypoint | `python -m luchtmeetnet_nl_mqtt` |
| AMQP entrypoint | `python -m luchtmeetnet_nl_amqp` |
| Exposed ports | none (outbound publisher only) |
| Signals | terminates on `SIGTERM` with producer flush on shutdown |
| Persistent state | `STATE_FILE` (mount host storage at `/state`) |
| Tags | `latest`, version tags, and immutable SHA tags in GHCR |

## Installing the images

```bash
docker pull ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl:latest
docker pull ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-amqp:latest
```

## Using the Kafka image

### Kafka with SASL/PLAIN

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/luchtmeetnet-nl.json   -e KAFKA_BOOTSTRAP_SERVERS="<host:port>"   -e KAFKA_TOPIC="luchtmeetnet-nl"   -e SASL_USERNAME="<username>"   -e SASL_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl:latest
```

### Kafka with Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/luchtmeetnet-nl.json   -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl:latest
```

## Using the MQTT image

### MQTT with username/password

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/luchtmeetnet-nl.json   -e MQTT_BROKER_URL="mqtts://<broker-host>:8883"   -e MQTT_USERNAME="<username>"   -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-mqtt:latest
```

### MQTT with Azure Event Grid + Microsoft Entra ID

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/luchtmeetnet-nl.json   -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883"   -e MQTT_AUTH_MODE=entra   -e MQTT_ENTRA_CLIENT_ID="<managed-identity-client-id>"   -e MQTT_CLIENT_ID="<unique-client-id>"   ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-mqtt:latest
```

## Using the AMQP image

### AMQP generic broker (SASL PLAIN)

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/luchtmeetnet-nl.json   -e AMQP_BROKER_URL="amqp://<user>:<password>@<host>:5672/luchtmeetnet-nl"   ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-amqp:latest
```

### AMQP with Azure Service Bus / Event Hubs (Entra-CBS)

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/luchtmeetnet-nl.json   -e AMQP_HOST="<namespace>.servicebus.windows.net"   -e AMQP_PORT=5671 -e AMQP_TLS=true   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_CLIENT_ID="<managed-identity-client-id>"   ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-amqp:latest
```

### AMQP with Service Bus emulator / SAS-CBS

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/luchtmeetnet-nl.json   -e AMQP_HOST="servicebus-emulator"   -e AMQP_PORT=5672   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME="RootManageSharedAccessKey"   -e AMQP_SAS_KEY="<sas-key>"   ghcr.io/clemensv/real-time-sources-luchtmeetnet-nl-amqp:latest
```

## Environment variable matrix

### Source configuration

| Variable | Description |
|---|---|
| `STATION_LIMIT` | Optional cap on the number of stations to poll, mainly for testing and fair-use throttling (default `0`). |
| `STATION_REFRESH_INTERVAL` | Refresh station metadata after this many telemetry polls (default `24`). |

### Common (all images)

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to persistent poller resume/dedupe state file. |
| `POLLING_INTERVAL` | Polling interval in seconds (source default applies when not set). |
| `LOG_LEVEL` | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric custom endpoint connection string shortcut. |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC` | Output topic name. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL/PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | Set `false` to disable TLS for local brokers. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_AUTH_MODE` | `password` (default) or `entra`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Username/password credentials for `password` mode. |
| `MQTT_ENTRA_CLIENT_ID` | Managed identity client id for `entra` mode (optional). |
| `MQTT_CLIENT_ID` | Unique MQTT client identifier. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_HOST` | MQTT broker host (component-level alternative to `MQTT_BROKER_URL`). |
| `MQTT_PORT` | MQTT broker port (component-level alternative to `MQTT_BROKER_URL`). |
| `MQTT_TLS` | Set `true` to use TLS (`mqtts`) for the component-level connection. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Full AMQP connection URL shortcut. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Host/port/TLS settings when not using URL shortcut. |
| `AMQP_ADDRESS` | Destination queue/topic/address. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | Credentials for `password` mode. |
| `AMQP_ENTRA_CLIENT_ID` | Managed identity client id for `entra` mode (optional). |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |

## Deploying into Azure Container Instances

### AMQP — deploy the AMQP image against an existing AMQP 1.0 endpoint you configure.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fluchtmeetnet-nl%2Fazure-template-amqp.json)

### MQTT — bring your own MQTT 5.0 broker and deploy the MQTT image.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fluchtmeetnet-nl%2Fazure-template-mqtt.json)

### MQTT — provision an Azure Event Grid namespace MQTT broker plus required identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fluchtmeetnet-nl%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Azure Event Hubs namespace + event hub and wire the feeder automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fluchtmeetnet-nl%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace with managed identity + sender role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fluchtmeetnet-nl%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hubs / Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fluchtmeetnet-nl%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview, deployment options, and quick starts.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schema details.
- [`xreg/luchtmeetnet-nl.xreg.json`](xreg/luchtmeetnet-nl.xreg.json) — authoritative event contract manifest.
