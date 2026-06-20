<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# FDSN Seismology

<sub>8 federated FDSN nodes · Kafka · MQTT · AMQP · <a href="https://www.fdsn.org/webservices/">upstream</a> · <a href="https://geofon.gfz-potsdam.de/fdsnws/event/1/application.wadl">event WADL</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI images for **FDSN Seismology**, their environment-variable contract, and the Azure deployment shapes. For the source overview see [README.md](README.md); for the event contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- FDSN Web Services overview: <https://www.fdsn.org/webservices/>
- Representative FDSN Event WADL: <https://geofon.gfz-potsdam.de/fdsnws/event/1/application.wadl>

<!-- upstream-links:end -->

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-fdsn-seismology` | Kafka | One topic, structured CloudEvents, `Node` reference events at startup, `Earthquake` telemetry on every poll cycle |
| `ghcr.io/clemensv/real-time-sources-fdsn-seismology-mqtt` | MQTT 5.0 | `seismology/fdsn/{node_id}/info` retained node records and `seismology/fdsn/{contributor}/{event_id}` event topics |
| `ghcr.io/clemensv/real-time-sources-fdsn-seismology-amqp` | AMQP 1.0 | One AMQP address (`fdsn-seismology` by default), binary CloudEvents, generic or Azure auth |

## Shared environment variables

| Variable | Default | Meaning |
|---|---|---|
| `POLL_INTERVAL` | `60` | Poll cadence in seconds. |
| `MIN_MAGNITUDE` | `0` | Optional minimum magnitude filter applied to every node query. |
| `NODES` / `FDSN_NODES` | empty | Optional comma-separated allow-list of node ids (`emsc,gfz,usgs,...`). |
| `EXCLUDE_NODES` / `FDSN_EXCLUDE_NODES` | empty | Optional comma-separated deny-list of node ids. |
| `STATE_FILE` | variant-specific user-home path | JSON file storing per-node poll cursors and dedupe state. Mount a volume if you want replay suppression across restarts. |
| `ONCE_MODE` | `false` | Run exactly one cycle and exit. Required for Fabric notebook hosting. |
| `FDSN_LIMIT` | `500` | Per-node maximum record count per query. |
| `LOG_LEVEL` | `INFO` | Python logging level. |

## Using the Kafka image

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<ns>.servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=fdsn-seismology" \
  -e MIN_MAGNITUDE=2.5 \
  ghcr.io/clemensv/real-time-sources-fdsn-seismology:latest
```

For plain Kafka in Docker E2E or local development, use:

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=<broker>:9092;EntityPath=fdsn-seismology" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-fdsn-seismology:latest
```

## Using the MQTT image

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-fdsn-seismology-mqtt:latest
```

For Azure Event Grid namespace MQTT, set `MQTT_AUTH_MODE=entra`, `MQTT_ENTRA_CLIENT_ID`, and a unique `MQTT_CLIENT_ID`.

## Using the AMQP image

Generic AMQP 1.0 broker:

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/fdsn-seismology' \
  ghcr.io/clemensv/real-time-sources-fdsn-seismology-amqp:latest
```

Azure Service Bus / Event Hubs with Entra ID:

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS='fdsn-seismology' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-fdsn-seismology-amqp:latest
```

## Deploying into Microsoft Fabric

- **Fabric Notebook feeder** — use `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source fdsn-seismology ...` for scheduled polling inside Fabric.
- **Fabric ACI feeder** — use `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source fdsn-seismology ...` for always-on container hosting.

## Deploying into Azure Container Instances

This source ships the standard five ARM templates:

- `azure-template.json` — Kafka image, bring your own Event Hubs / Fabric endpoint
- `azure-template-with-eventhub.json` — Kafka image plus a new Event Hubs namespace and event hub
- `azure-template-with-servicebus.json` — AMQP image plus a new Service Bus namespace and queue
- `azure-template-mqtt.json` — MQTT image, bring your own MQTT broker
- `azure-template-with-eventgrid-mqtt.json` — MQTT image plus a new Event Grid namespace MQTT broker
