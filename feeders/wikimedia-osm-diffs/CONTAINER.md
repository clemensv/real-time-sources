<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# OpenStreetMap Diffs

<sub>OSM minutely replication diffs · Kafka · MQTT · AMQP · <a href="https://www.openstreetmap.org/">upstream</a> · <a href="https://wiki.openstreetmap.org/wiki/Planet.osm/diffs">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — OSM minutely replication diffs

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#wikimedia-osm-diffs) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#wikimedia-osm-diffs/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/wikimedia_osm_diffs.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.openstreetmap.org/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published container images for the Wikimedia OSM Diffs feeder. For overview and business context see [README.md](README.md); for event-contract details see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.openstreetmap.org/>
- API / data documentation: <https://wiki.openstreetmap.org/wiki/Planet.osm/diffs>

<!-- upstream-links:end -->

## Why this container

OSM minutely diffs are a high-volume global map-change stream used in geospatial monitoring and ETL pipelines. This feeder parses the feed and emits CloudEvents for downstream consumers.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs` | Kafka | Polls upstream and publishes CloudEvents to one topic |
| `ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-mqtt` | MQTT 5.0 | Publishes CloudEvents to xRegistry-mapped topics |
| `ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-amqp` | AMQP 1.0 | Publishes CloudEvents to one AMQP address |

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.10-slim` |
| Default entrypoint | `python -m wikimedia_osm_diffs feed; python -m wikimedia_osm_diffs_mqtt feed; python -m wikimedia_osm_diffs_amqp feed` |
| Exposed ports | none — outbound publisher only |
| Signals | exits on `SIGTERM`; in-flight poll cycle is completed/flushed before shutdown where supported |
| State | Kafka: OSM_DIFFS_STATE_FILE; MQTT: OSM_DIFFS_STATE_FILE; AMQP: OSM_DIFFS_STATE_FILE. Mount `/state` when state is used. |
| Tags | `:latest` (mainline), plus immutable release/SHA tags published in GHCR. |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
docker pull ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs.json \
  -e KAFKA_BOOTSTRAP_SERVERS='<broker:9093>' \
  -e KAFKA_TOPIC='<topic>' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
```

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs.json \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
```

## Using the MQTT image

### With username/password authentication

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs-mqtt.json \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Entra)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs-mqtt.json \
  -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-mqtt:latest
```

## Using the AMQP image

### With Microsoft Entra ID (AMQP CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs-amqp.json \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='wikimedia-osm-diffs' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-amqp:latest
```

### With SAS token CBS (Service Bus emulator / SAS-only namespaces)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs-amqp.json \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='wikimedia-osm-diffs' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-amqp:latest
```

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `LOG_LEVEL` | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Source configuration

| Variable | Description |
|---|---|
| `OSM_DIFFS_BASE_URL` | Base URL for OpenStreetMap minutely diff files; defaults to the public planet.openstreetmap.org replication endpoint. |
| `OSM_DIFFS_MAX_RETRY_DELAY` | Maximum back-off delay in seconds between failed-fetch retries (default `120`). |
| `OSM_DIFFS_ONCE` | Set to a truthy value to process one diff batch and exit (default `false`). |
| `OSM_DIFFS_POLL_INTERVAL` | Seconds between replication-state polls (default `60`). |
| `OSM_DIFFS_STATE_URL` | URL of the replication `state.txt` used to discover the latest diff sequence number. |
| `OSM_DIFFS_USER_AGENT` | User-Agent header sent to the OSM replication server; set a contact address per the OSM usage policy. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style or Kafka-style connection string. |
| `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC` | Explicit Kafka destination. |
| `SASL_USERNAME`, `SASL_PASSWORD` | SASL PLAIN credentials when needed. |
| `KAFKA_ENABLE_TLS` | Set `false` for plaintext Kafka. |
| `ONCE_MODE` | Run one cycle and exit (where supported). |
| State variable | `OSM_DIFFS_STATE_FILE` |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_USERNAME`, `MQTT_PASSWORD` | Optional broker credentials. |
| `MQTT_CLIENT_ID` | Optional explicit client ID. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` where supported. |
| State variable | `OSM_DIFFS_STATE_FILE` |
| `MQTT_ENABLE_TLS` | Set `true` to use TLS (`mqtts`) for the MQTT connection. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL (`amqp://` or `amqps://`). |
| `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS` | Component-level AMQP endpoint settings. |
| `AMQP_USERNAME`, `AMQP_PASSWORD` | SASL PLAIN credentials (if used). |
| `AMQP_AUTH_MODE` | Auth mode where supported (`password`/`entra`/`sas`). |
| `AMQP_TLS` | Enable TLS where supported. |
| State variable | `OSM_DIFFS_STATE_FILE` |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

## Deploying into Microsoft Fabric

Fabric notebook and Fabric ACI hosting are both supported:

- Notebook: `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source wikimedia-osm-diffs ...`
- ACI: `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source wikimedia-osm-diffs ...`

Portal links:

- [Fabric Notebook](https://clemensv.github.io/real-time-sources/#wikimedia-osm-diffs/fabric-notebook)
- [Fabric ACI](https://clemensv.github.io/real-time-sources/#wikimedia-osm-diffs/fabric-aci)

## Deploying into Azure Container Instances

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwikimedia-osm-diffs%2Fazure-template-with-eventhub.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwikimedia-osm-diffs%2Fazure-template.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwikimedia-osm-diffs%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwikimedia-osm-diffs%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fwikimedia-osm-diffs%2Fazure-template-with-servicebus.json)

## Related
- [README.md](README.md) — source overview, use cases, and quick start.
- [EVENTS.md](EVENTS.md) — event contract and schema details.
- [`xreg/wikimedia_osm_diffs.xreg.json`](xreg/wikimedia_osm_diffs.xreg.json) — authoritative manifest.
