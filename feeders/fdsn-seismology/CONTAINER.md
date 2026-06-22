<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# FDSN Seismology

<sub>9 cataloged FDSN nodes · Kafka · MQTT · AMQP · <a href="https://www.fdsn.org/webservices/">upstream</a> · <a href="https://geofon.gfz-potsdam.de/fdsnws/event/1/application.wadl">event WADL</a></sub>

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
| `FDSN_SOURCES_FILE` | packaged catalog | Path to an alternate FDSN node catalog JSON mounted into the container. |
| `FDSN_NODES` / `NODES` | empty | Optional comma-separated allow-list of node ids (`emsc,gfz,usgs,...`). `FDSN_NODES` is preferred; `NODES` remains as a legacy fallback. |
| `FDSN_EXCLUDE_NODES` / `EXCLUDE_NODES` | empty | Optional comma-separated deny-list of node ids. `FDSN_EXCLUDE_NODES` is preferred; `EXCLUDE_NODES` remains as a legacy fallback. |
| `STATE_FILE` | variant-specific user-home path | JSON file storing per-node poll cursors and dedupe state. Mount a volume if you want replay suppression across restarts. |
| `ONCE_MODE` | `false` | Run exactly one cycle and exit. Required for Fabric notebook hosting. |
| `FDSN_LIMIT` | `500` | Per-node maximum record count per query. |
| `LOG_LEVEL` | `INFO` | Python logging level. |

## Configuring sources

The containers ship a checked-in FDSN node catalog at `fdsn_seismology_core/fdsn_seismology_core/sources/fdsn-seismology.sources.json`. Operators can keep the default enabled nodes, point `FDSN_SOURCES_FILE` at a mounted catalog copy, and use the existing `FDSN_NODES` / `FDSN_EXCLUDE_NODES` selector variables without changing transport configuration.

| Variable | Purpose | Default |
| --- | --- | --- |
| `FDSN_SOURCES_FILE` | Path to a JSON catalog with FDSN node entries. Mount your own copy when you need private, regional, or institutional nodes. | Packaged catalog |
| `FDSN_NODES` | Comma-separated node ids to run. When set, this explicit allow-list overrides `enabled: false` and can force a disabled catalog entry on. Legacy `NODES` remains supported as a fallback. | enabled entries |
| `FDSN_EXCLUDE_NODES` | Comma-separated node ids to subtract from either the default enabled set or the `FDSN_NODES` include list. Legacy `EXCLUDE_NODES` remains supported as a fallback. | unset |

### Catalog format

```json
{
  "description": "FDSN Seismology source catalog...",
  "sources": [
    {
      "name": "usgs",
      "enabled": true,
      "description": "USGS Earthquake Hazards Program global earthquake catalog FDSN Event service.",
      "display_name": "U.S. Geological Survey Earthquake Hazards Program (USGS)",
      "node_id": "usgs",
      "base_url": "https://earthquake.usgs.gov/fdsnws/event/1/",
      "coverage": "Global earthquake catalog",
      "country": "US"
    }
  ]
}
```

| Field | Required | Description |
| --- | ---: | --- |
| `name` | ✅ | Stable catalog entry name; for shipped entries it matches `node_id`. |
| `enabled` | ❌ | Defaults to `true`; disabled templates are skipped unless explicitly selected with `FDSN_NODES`. |
| `description` | ✅ | Human-readable node, coverage, and access notes. |
| `display_name` | ✅ | Full institution name emitted in the `org.fdsn.event.Node` reference event `name` field. |
| `node_id` | ✅ | Stable short id used by `FDSN_NODES`, `FDSN_EXCLUDE_NODES`, event subjects, and transport keys. |
| `base_url` | ✅ | FDSN Event service base URL ending in `/fdsnws/event/1/`. |
| `coverage` | ✅ | Geographic, magnitude, or catalog scope description emitted with the node reference record. |
| `country` | ❌ | ISO 3166-1 alpha-2 country code for the operating institution, if known. |

### Selecting nodes

- Unset `FDSN_NODES` — poll every catalog entry with `enabled: true`.
- `FDSN_NODES=usgs,gfz` — poll only those node ids, in that order.
- `FDSN_NODES=custom` — force a disabled catalog entry on after you have replaced its placeholder fields in your own catalog.
- `FDSN_EXCLUDE_NODES=emsc` — subtract EMSC from the default enabled set or from the explicit include list.
- Unknown node ids fail fast with a `ValueError` that lists known ids.

### Bring your own catalog

```powershell
docker run --rm `
  -v ${PWD}\my-fdsn.sources.json:/app/fdsn.sources.json:ro `
  -e FDSN_SOURCES_FILE="/app/fdsn.sources.json" `
  -e FDSN_NODES="custom" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=fdsn-seismology" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-fdsn-seismology:latest
```

`${ENV_VAR}` placeholders in string fields are expanded at load time, so private endpoints or tokens can stay outside the catalog file.

### Known FDSN nodes

#### Shipped and enabled by default

| Node id | Name | Coverage | Country |
| --- | --- | --- | --- |
| `emsc` | European-Mediterranean Seismological Centre (EMSC) | Global aggregator | FR |
| `gfz` | GFZ German Research Centre for Geosciences (GEOFON) | Global M4+ | DE |
| `ingv` | Istituto Nazionale di Geofisica e Vulcanologia (INGV) | Italy + Mediterranean | IT |
| `ethz` | Swiss Seismological Service at ETH Zurich (SED) | Switzerland + Alpine | CH |
| `resif` | Réseau Sismologique et géodésique Français (RESIF) | France + global M5+ | FR |
| `ipgp` | Institut de Physique du Globe de Paris (IPGP) | Mayotte volcanic swarm | FR |
| `niep` | National Institute for Earth Physics (NIEP) | Romania + Vrancea | RO |
| `usgs` | U.S. Geological Survey Earthquake Hazards Program (USGS) | Global earthquake catalog | US |

#### Available but disabled

| Node id | Name | Coverage | Country | Base URL | Ready-to-enable |
| --- | --- | --- | --- | --- | --- |
| `isc` | International Seismological Centre (ISC) | Global ISC bulletin and preliminary catalog | GB | `https://www.isc.ac.uk/fdsnws/event/1/` | Add `isc` to `FDSN_NODES` |
| `custom` | Custom FDSN Event service template | `REPLACE_WITH_COVERAGE` | `REPLACE_WITH_COUNTRY` | `REPLACE_WITH_FDSN_BASE_URL` | Replace placeholders, then add custom node id to `FDSN_NODES` |

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
