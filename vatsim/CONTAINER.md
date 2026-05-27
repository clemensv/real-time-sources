<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# VATSIM

<sub>virtual aviation network, pilots & controllers · Kafka · MQTT · AMQP · <a href="https://www.vatsim.net/">upstream</a> · <a href="https://data.vatsim.net/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — virtual aviation network, pilots & controllers

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#vatsim) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#vatsim/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/vatsim.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.vatsim.net/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI images for the VATSIM source, including runtime environment variables, auth modes, and deploy options. For source context see [README.md](README.md); for the event contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.vatsim.net/>
- API / data documentation: <https://data.vatsim.net/>

<!-- upstream-links:end -->

## Why this container

VATSIM network data is useful for aviation simulation analytics, traffic visualization, and research. This feeder normalizes live VATSIM updates into CloudEvents so consumers can build streaming applications without bespoke ingest logic.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-vatsim` | Kafka | JSON CloudEvents to one Kafka topic |
| `ghcr.io/clemensv/real-time-sources-vatsim-mqtt` | MQTT 5.0 | Binary CloudEvents into UNS topic tree from xRegistry |
| `ghcr.io/clemensv/real-time-sources-vatsim-amqp` | AMQP 1.0 | Binary CloudEvents to one AMQP address |

## Image contract

| Aspect | Value |
| --- | --- |
| Base image | Kafka: `python:3.10-slim`; MQTT: `python:3.10-slim`; AMQP: `python:3.10-slim` |
| Default entry point | Kafka: `python -m vatsim`; MQTT: `python -m vatsim_mqtt feed`; AMQP: `python -m vatsim_amqp feed` |
| Exposed ports | none — outbound publisher only |
| Persistent state vars | Kafka: `STATE_FILE`; MQTT: `STATE_FILE`; AMQP: `STATE_FILE` |
| Image tags | `:latest`, `:sha-<git-sha>`, release tags |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-vatsim:latest
docker pull ghcr.io/clemensv/real-time-sources-vatsim-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-vatsim-amqp:latest
```

## Using the Kafka image

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-vatsim:latest
```

### With a Kafka broker (SASL/PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e KAFKA_BOOTSTRAP_SERVERS="<host:9093>" \
  -e KAFKA_TOPIC="<topic>" \
  -e SASL_USERNAME="<username>" \
  -e SASL_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-vatsim:latest
```

## Using the MQTT image

### Generic MQTT 5 broker (username/password)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-vatsim-mqtt:latest
```

### Azure Event Grid MQTT broker (Entra JWT)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883" \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID="<managed-identity-client-id>" \
  -e MQTT_CLIENT_ID="<unique-client-id>" \
  ghcr.io/clemensv/real-time-sources-vatsim-mqtt:latest
```

## Using the AMQP image

### Generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/vatsim" \
  ghcr.io/clemensv/real-time-sources-vatsim-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra ID via CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e AMQP_HOST="<namespace>.servicebus.windows.net" \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS="vatsim" \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_CLIENT_ID="<managed-identity-client-id>" \
  ghcr.io/clemensv/real-time-sources-vatsim-amqp:latest
```

### Service Bus emulator / SAS namespaces (SAS-token CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/vatsim.json \
  -e AMQP_HOST="servicebus-emulator" \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS="vatsim" \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME="RootManageSharedAccessKey" \
  -e AMQP_SAS_KEY="<sas-key>" \
  ghcr.io/clemensv/real-time-sources-vatsim-amqp:latest
```

## Environment variables

### Common source runtime variables

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to persisted checkpoint/dedupe state for the KAFKA bridge runtime. |
| `POLLING_INTERVAL` | Polling interval in seconds. |
| `VATSIM_SAMPLE_MODE` | Optional sampling/test mode flag for development runs. |

### Kafka image variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric custom endpoint style connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list (`host:port`). |
| `KAFKA_TOPIC` | Destination Kafka topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL/PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | Set `false` to disable TLS (default `true`). |

### MQTT image variables

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for Event Grid JWT auth. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for `MQTT_AUTH_MODE=password`. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | User-assigned managed identity client id (optional). |
| `MQTT_CLIENT_ID` | MQTT client identifier (must be unique per broker). |
| `MQTT_CONTENT_MODE` | CloudEvents mode: `binary` (default) or `structured`. |

### AMQP image variables

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | URL form endpoint, e.g. `amqp://user:pw@host:5672/address`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level endpoint settings. |
| `AMQP_ADDRESS` | Target AMQP address (queue/topic). |
| `AMQP_AUTH_MODE` | `password` (default), `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | Credentials for `AMQP_AUTH_MODE=password`. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra auth settings for `AMQP_AUTH_MODE=entra`. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS policy/key pair for `AMQP_AUTH_MODE=sas`. |
| `AMQP_CONTENT_MODE` | CloudEvents mode: `binary` (default) or `structured`. |

## Deploying into Microsoft Fabric

### Fabric Notebook feeder

Use `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source vatsim -Workspace <id> -ResourceGroup <azure-rg> -Location <azure-region>` to deploy the notebook in `notebook/`, bind Event Stream/Lakehouse/KQL assets, and schedule poll runs.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#vatsim/fabric-notebook)

### Fabric ACI feeder

Use `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source vatsim -Workspace <id> -ResourceGroup <azure-rg> -Location <azure-region>` for always-on container hosting that publishes to Fabric Event Streams.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#vatsim/fabric-aci)

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

Deploys the Kafka image and uses a provided connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploys Kafka plus a new Event Hubs namespace and hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventhub.json)

### AMQP — provision Azure Service Bus

Deploys AMQP plus a new Service Bus namespace/queue and sender identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-servicebus.json)

## Related

- [README.md](README.md) — source overview, use cases, and quick-start guidance.
- [EVENTS.md](EVENTS.md) — CloudEvents schemas and routing contract.
- [`xreg/`](xreg/) — authoritative xRegistry manifest used to generate producers and event docs.

## Next steps

- Validate topics/subjects/schemas in [EVENTS.md](EVENTS.md).
- Use the deployment buttons above for the transport and hosting shape you need.
