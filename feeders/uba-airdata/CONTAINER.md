<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/de.png" alt="Germany" width="64" height="48"><br>
<sub><b>Germany</b></sub>
</td>
<td valign="middle">

# UBA AirData

<sub>stations, pollutant components, hourly measures · Kafka · MQTT · AMQP · <a href="https://www.umweltbundesamt.de/">upstream</a> · <a href="https://www.umweltbundesamt.de/daten/luft/luftdaten/doc">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Germany — stations, pollutant components, hourly measures

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#uba-airdata) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#uba-airdata/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/uba_airdata.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.umweltbundesamt.de/)

</td></tr></table>
<!-- source-hero:end -->

This document describes the published OCI images for the UBA AirData feeder. For solution overview and usage scenarios, see [README.md](README.md). For the CloudEvents contract and schemas, see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.umweltbundesamt.de/>
- API / data documentation: <https://www.umweltbundesamt.de/daten/luft/luftdaten/doc>

<!-- upstream-links:end -->

## Why this container

These images package the poller, normalization logic, and transport producers so teams can subscribe to standardized air-quality CloudEvents without writing their own ingestion pipeline.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-uba-airdata` | Kafka | Poll upstream and publish CloudEvents to one Kafka topic with xRegistry keying |
| `ghcr.io/clemensv/real-time-sources-uba-airdata-mqtt` | MQTT 5.0 | Poll upstream and publish CloudEvents to MQTT topic hierarchy |
| `ghcr.io/clemensv/real-time-sources-uba-airdata-amqp` | AMQP 1.0 | Poll upstream and publish CloudEvents to a configured AMQP address |

Event families in this source:

- **`de.uba.airdata`**: Station, Measure
- **`de.uba.airdata.components`**: Component
- **`de.uba.airdata.mqtt`**: Station, Measure
- **`de.uba.airdata.amqp`**: Station, Measure
- **`de.uba.airdata.components.mqtt`**: Component
- **`de.uba.airdata.components.amqp`**: Component

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.10-slim` |
| Kafka entrypoint | `python -m uba_airdata` |
| MQTT entrypoint | `python -m uba_airdata_mqtt` |
| AMQP entrypoint | `python -m uba_airdata_amqp` |
| Exposed ports | none (outbound publisher only) |
| Signals | terminates on `SIGTERM` with producer flush on shutdown |
| Persistent state | `STATE_FILE` (mount host storage at `/state`) |
| Tags | `latest`, version tags, and immutable SHA tags in GHCR |

## Installing the images

```bash
docker pull ghcr.io/clemensv/real-time-sources-uba-airdata:latest
docker pull ghcr.io/clemensv/real-time-sources-uba-airdata-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-uba-airdata-amqp:latest
```

## Using the Kafka image

### Kafka with SASL/PLAIN

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/uba-airdata.json   -e KAFKA_BOOTSTRAP_SERVERS="<host:port>"   -e KAFKA_TOPIC="uba-airdata"   -e SASL_USERNAME="<username>"   -e SASL_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-uba-airdata:latest
```

### Kafka with Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/uba-airdata.json   -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-uba-airdata:latest
```

## Using the MQTT image

### MQTT with username/password

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/uba-airdata.json   -e MQTT_BROKER_URL="mqtts://<broker-host>:8883"   -e MQTT_USERNAME="<username>"   -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-uba-airdata-mqtt:latest
```

### MQTT with Azure Event Grid + Microsoft Entra ID

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/uba-airdata.json   -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883"   -e MQTT_AUTH_MODE=entra   -e MQTT_ENTRA_CLIENT_ID="<managed-identity-client-id>"   -e MQTT_CLIENT_ID="<unique-client-id>"   ghcr.io/clemensv/real-time-sources-uba-airdata-mqtt:latest
```

## Using the AMQP image

### AMQP generic broker (SASL PLAIN)

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/uba-airdata.json   -e AMQP_BROKER_URL="amqp://<user>:<password>@<host>:5672/uba-airdata"   ghcr.io/clemensv/real-time-sources-uba-airdata-amqp:latest
```

### AMQP with Azure Service Bus / Event Hubs (Entra-CBS)

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/uba-airdata.json   -e AMQP_HOST="<namespace>.servicebus.windows.net"   -e AMQP_PORT=5671 -e AMQP_TLS=true   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_CLIENT_ID="<managed-identity-client-id>"   ghcr.io/clemensv/real-time-sources-uba-airdata-amqp:latest
```

### AMQP with Service Bus emulator / SAS-CBS

```bash
docker run --rm   -v "$PWD/state:/state"   -e STATE_FILE=/state/uba-airdata.json   -e AMQP_HOST="servicebus-emulator"   -e AMQP_PORT=5672   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME="RootManageSharedAccessKey"   -e AMQP_SAS_KEY="<sas-key>"   ghcr.io/clemensv/real-time-sources-uba-airdata-amqp:latest
```

## Environment variable matrix

### Common (all images)

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to persistent poller resume/dedupe state file. |
| `POLLING_INTERVAL` | Polling interval in seconds (source default applies when not set). |

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

## Deploying into Azure Container Instances

### AMQP — deploy the AMQP image against an existing AMQP 1.0 endpoint you configure.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuba-airdata%2Fazure-template-amqp.json)

### MQTT — bring your own MQTT 5.0 broker and deploy the MQTT image.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuba-airdata%2Fazure-template-mqtt.json)

### MQTT — provision an Azure Event Grid namespace MQTT broker plus required identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuba-airdata%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Azure Event Hubs namespace + event hub and wire the feeder automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuba-airdata%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace with managed identity + sender role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuba-airdata%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hubs / Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuba-airdata%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview, deployment options, and quick starts.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schema details.
- [`xreg/uba_airdata.xreg.json`](xreg/uba_airdata.xreg.json) — authoritative event contract manifest.
