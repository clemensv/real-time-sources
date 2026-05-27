<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/de.png" alt="Germany" width="64" height="48"><br>
<sub><b>Germany</b></sub>
</td>
<td valign="middle">

# Autobahn

<sub>roadworks, warnings, closures, webcams · Kafka · MQTT · AMQP · <a href="https://autobahn.de/">upstream</a> · <a href="https://autobahn.api.bund.dev/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Germany — roadworks, warnings, closures, webcams

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#autobahn) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#autobahn/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/autobahn.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://autobahn.de/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the Autobahn feeder, their environment-variable contract, authentication modes, and one-click Azure deployments.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://autobahn.de/>
- API / data documentation: <https://autobahn.api.bund.dev/>

<!-- upstream-links:end -->

Companion docs:

- [README.md](README.md) — source overview, value framing, and deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and routing details.

## Why this container

German motorway operations teams, logistics platforms, emergency planners, navigation systems, and insurers use Autobahn status data for closures, incidents, and restrictions. These containers package polling, event normalization, dedupe, and transport-specific publishing so teams can run production ingestion without custom bridge code.

## What ships in the box

| Image | Transport | Runtime entrypoint |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-autobahn` | Kafka | `python -m autobahn feed` |
| `ghcr.io/clemensv/real-time-sources-autobahn-mqtt` | MQTT | `python -m autobahn_mqtt feed` |
| `ghcr.io/clemensv/real-time-sources-autobahn-amqp` | AMQP | `python -m autobahn_amqp feed` |

The image set shares a single xRegistry contract and publishes the same event families listed in [EVENTS.md](EVENTS.md).

## Image contract

| Aspect | Value |
|---|---|
| Base image | Source Dockerfiles (`Dockerfile*`) currently use Python slim bases (Kafka may differ from MQTT/AMQP in some sources). |
| Entry point | `python -m <source>{,_mqtt,_amqp} feed` per image. |
| Exposed ports | None (outbound publisher only). |
| Signals | Graceful process termination on `SIGTERM`. |
| Persistent state | `AUTOBAHN_STATE_FILE` (mount `/state` volume for restart-safe dedupe). |
| Tags | `latest`, plus immutable release/sha tags from GHCR publishing workflows. |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-autobahn:latest
docker pull ghcr.io/clemensv/real-time-sources-autobahn-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-autobahn-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e KAFKA_BOOTSTRAP_SERVERS=<host:port> \
  -e KAFKA_TOPIC=autobahn \
  -e SASL_USERNAME=<username> \
  -e SASL_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-autobahn:latest
```

### With Azure Event Hubs / Fabric Event Stream connection string

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-autobahn:latest
```

## Using the MQTT image

### Generic MQTT 5 broker (username/password)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-autobahn-mqtt:latest
```

### Azure Event Grid namespace MQTT broker (Entra OAUTH2-JWT)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-autobahn-mqtt:latest
```

## Using the AMQP image

### Generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/autobahn' \
  ghcr.io/clemensv/real-time-sources-autobahn-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='autobahn' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-autobahn-amqp:latest
```

### Azure Service Bus emulator / SAS namespaces (SAS CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e AUTOBAHN_STATE_FILE=/state/autobahn.json \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='autobahn' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-autobahn-amqp:latest
```

## Environment variables

### Common

| Variable | Description |
|---|---|
| `AUTOBAHN_STATE_FILE` | Path to persisted poll/dedupe state file. |
| `AUTOBAHN_POLL_INTERVAL` | Polling interval in seconds (where supported by the runtime variant). |
| `ONCE_MODE` | Run one poll cycle and exit (used by notebook scheduling). |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric style connection string (overrides bootstrap/SASL fields). |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker list. |
| `KAFKA_TOPIC` | Kafka topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | Set `false` for plaintext Kafka links. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` or `MQTT_HOST`/`MQTT_PORT` | MQTT broker endpoint. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Password auth for generic brokers. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra`. |
| `MQTT_ENTRA_CLIENT_ID` / `MQTT_ENTRA_AUDIENCE` | Entra token configuration for Event Grid MQTT. |
| `MQTT_CLIENT_ID` | MQTT client identifier. |
| `MQTT_CONTENT_MODE` | `binary` or `structured` CloudEvents payload mode. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` or `AMQP_HOST`/`AMQP_PORT`/`AMQP_TLS` | AMQP broker endpoint. |
| `AMQP_ADDRESS` | Queue/topic/address target. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials (`password` mode). |
| `AMQP_ENTRA_CLIENT_ID` / `AMQP_ENTRA_AUDIENCE` | Entra CBS token configuration. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS token material for emulator/SAS namespaces. |

## Deploying into Azure Container Instances

### MQTT — bring your own broker

Deploy MQTT against an existing MQTT 5.0 broker endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid MQTT broker

Deploy MQTT plus an Event Grid namespace broker and managed-identity role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

Deploy Kafka plus a new Event Hubs namespace and event hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

Deploy AMQP plus Service Bus and managed-identity sender permissions.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Event Hubs/Fabric/Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fautobahn%2Fazure-template.json)

## Related

- [README.md](README.md) — project overview and hosting options.
- [EVENTS.md](EVENTS.md) — event contract and schema details.
- [`xreg/autobahn.xreg.json`](xreg/autobahn.xreg.json) — authoritative contract source.
