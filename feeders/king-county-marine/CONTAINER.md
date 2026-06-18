<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="Washington State / Puget Sound" width="64" height="48"><br>
<sub><b>Washington State / Puget Sound</b></sub>
</td>
<td valign="middle">

# King County Marine

<sub>buoy and mooring telemetry · Kafka · MQTT · AMQP · <a href="https://green2.kingcounty.gov/marine/">upstream</a> · <a href="https://data.kingcounty.gov/Environment-Waste-Management/Puget-Sound-Marine-Monitoring/t5pc-wkwc">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Washington State / Puget Sound — buoy and mooring telemetry

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#king-county-marine) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#king-county-marine/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/king_county_marine.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://green2.kingcounty.gov/marine/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the King County Marine feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://green2.kingcounty.gov/marine/>
- API / data documentation: <https://data.kingcounty.gov/Environment-Waste-Management/Puget-Sound-Marine-Monitoring/t5pc-wkwc>

<!-- upstream-links:end -->

## Why this container

The King County Marine source is exposed as a polling API upstream. These container images package polling cadence control, stateful dedupe, CloudEvents production, and transport/auth wiring so operators can deploy a ready-to-run feeder instead of building source-specific integration code.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-king-county-marine` | Apache Kafka 2.x | JSON CloudEvents on one topic; key template `{station_id}` |
| `ghcr.io/clemensv/real-time-sources/king-county-marine-mqtt` | MQTT 5.0 | Unified-Namespace topic template `(see EVENTS.md)` |
| `ghcr.io/clemensv/real-time-sources-king-county-marine-amqp` | AMQP 1.0 | Binary CloudEvents to AMQP node `king-county-marine` |

Event families in this source:

- **US.WA.KingCounty.Marine** — `Station`, `WaterQualityReading`.

## Image contract

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` (source Dockerfiles) |
| Default entry point | Kafka `["python", "-m", "king_county_marine"]`; MQTT `["python", "-m", "king_county_marine_mqtt", "feed"]`; AMQP `["python", "-m", "king_county_marine_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | process exits cleanly on `SIGTERM` |
| Persistent state | `KING_COUNTY_MARINE_STATE_FILE`; mount a host volume for restart-safe dedupe/checkpoint behavior |
| Image tags | `:latest` and immutable release/sha tags published from repository CI |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-king-county-marine:latest
docker pull ghcr.io/clemensv/real-time-sources/king-county-marine-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-king-county-marine-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL/PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e KAFKA_BOOTSTRAP_SERVERS="<host:port>" \
  -e KAFKA_TOPIC="<topic>" \
  -e SASL_USERNAME="<username>" \
  -e SASL_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-king-county-marine:latest
```

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-king-county-marine:latest
```

## Using the MQTT image

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources/king-county-marine-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883" \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  -e MQTT_CLIENT_ID="<unique-client-id>" \
  ghcr.io/clemensv/real-time-sources/king-county-marine-mqtt:latest
```

## Using the AMQP image

### With AMQP 1.0 and Microsoft Entra ID (CBS put-token)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e AMQP_HOST="<namespace>.servicebus.windows.net" \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS="king-county-marine" \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE="https://servicebus.azure.net/.default" \
  -e AMQP_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  ghcr.io/clemensv/real-time-sources-king-county-marine-amqp:latest
```

### With AMQP 1.0 and SAS-token CBS

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e KING_COUNTY_MARINE_STATE_FILE=/state/king-county-marine.json \
  -e AMQP_HOST="servicebus-emulator" \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS="king-county-marine" \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME="RootManageSharedAccessKey" \
  -e AMQP_SAS_KEY="<sas-key>" \
  ghcr.io/clemensv/real-time-sources-king-county-marine-amqp:latest
```

## Environment variables

### Kafka image

| Variable | Description |
|---|---|
| `KING_COUNTY_MARINE_STATE_FILE` | Path to dedupe/checkpoint state file. |
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string (optional alternative to explicit Kafka variables). |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list. |
| `KAFKA_TOPIC` | Kafka destination topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL/PLAIN credentials for Kafka. |
| `POLLING_INTERVAL` | Poll interval in seconds. |

### MQTT image

| Variable | Description |
|---|---|
| `KING_COUNTY_MARINE_STATE_FILE` | Path to dedupe/checkpoint state file. |
| `KING_COUNTY_MARINE_SAMPLE_MODE` | Set to `true` to publish deterministic sample station and reading events instead of polling the live upstream feed. |
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for `MQTT_AUTH_MODE=password`. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra`. |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID. |
| `MQTT_CLIENT_ID` | MQTT client ID (must be unique per broker). |
| `POLLING_INTERVAL` | Poll interval in seconds. |

### AMQP image

| Variable | Description |
|---|---|
| `KING_COUNTY_MARINE_STATE_FILE` | Path to dedupe/checkpoint state file. |
| `KING_COUNTY_MARINE_SAMPLE_MODE` | Set to `true` to publish deterministic sample station and reading events instead of polling the live upstream feed. |
| `AMQP_BROKER_URL` | Full AMQP URL form (`amqp://` or `amqps://`). |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component endpoint settings when URL form is not used. |
| `AMQP_ADDRESS` | AMQP node/address name. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra-ID CBS settings. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS-token CBS settings. |
| `POLLING_INTERVAL` | Poll interval in seconds. |

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fking-county-marine%2Fazure-template.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fking-county-marine%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fking-county-marine%2Fazure-template-mqtt.json)

### MQTT — provision an Azure Event Grid namespace MQTT broker plus required identity wiring.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fking-county-marine%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fking-county-marine%2Fazure-template-with-servicebus.json)

## Related

- [README.md](README.md) — project overview and deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schema details.
- [`xreg/king_county_marine.xreg.json`](xreg/king_county_marine.xreg.json) — source contract used to generate producer bindings.
