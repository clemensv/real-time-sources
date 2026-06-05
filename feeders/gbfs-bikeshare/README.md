<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# GBFS Bikeshare

<sub>Global micromobility systems via GBFS autodiscovery · Kafka · MQTT · AMQP · <a href="https://gbfs.org/">upstream</a> · <a href="https://github.com/MobilityData/gbfs/blob/master/gbfs.md">spec docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-2_paths-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">

> Global — user-configured GBFS systems for bikeshare, scooter-share, and shared micromobility

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#gbfs-bikeshare) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/gbfs-bikeshare.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://gbfs.org/)

</td></tr></table>
<!-- source-hero:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published images, environment variables, and Azure / Fabric deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, payload schemas, and per-transport routing templates.

## Upstream

- Home page: <https://gbfs.org/>
- Specification: <https://github.com/MobilityData/gbfs/blob/master/gbfs.md>
- MobilityData systems catalog: <https://github.com/MobilityData/gbfs/blob/master/systems.csv>

## Why this bridge

GBFS is the de-facto open data standard for bikeshare, scooter-share, and shared micromobility systems. Hundreds of operators publish the same discovery + feed pattern, but every downstream consumer otherwise has to implement its own poller, schema normalization, and transport adapter.

This feeder provides one reusable bridge for common mobility scenarios:

- **Operations dashboards** — track station availability and dockless fleet positions across one or many systems.
- **Streaming analytics** — land GBFS events directly in Eventhouse, ADX, lakehouse pipelines, or MQTT / AMQP consumers.
- **Cross-source correlation** — join micromobility supply with weather, transit, or event-demand feeds from this repository.
- **Platform reuse** — configure the same container for different systems via `GBFS_FEEDS` rather than building one image per operator.

## Overview

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-kafka` | Apache Kafka / Event Hubs / Fabric Event Streams | topic `gbfs-bikeshare`; keys follow the CloudEvents subject (`{system_id}`, `{system_id}/{station_id}`, `{system_id}/{bike_id}`) |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt` | MQTT 5.0 / Unified Namespace | `mobility/gbfs/...` topic tree with retained reference events |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp` | AMQP 1.0 / Service Bus / Artemis / RabbitMQ AMQP 1.0 | address `gbfs-bikeshare`, binary-mode CloudEvents |

All three variants share:

- the same xRegistry contract in `xreg/gbfs-bikeshare.xreg.json`
- the same acquisition and normalization code in `gbfs_bikeshare_core/`
- the same event families and schema definitions documented in [EVENTS.md](EVENTS.md)

## Configuring feeds

This source follows the GTFS-style deployment model: one container, user-configured for one or more upstream systems.

- `GBFS_FEEDS` — **required**. Either a comma-separated list of GBFS autodiscovery URLs or a file path / `@file` reference containing one URL per line.
- `GBFS_SYSTEM_IDS` — optional. Comma-separated override labels aligned positionally with `GBFS_FEEDS`. Use this when you want stable local system labels regardless of upstream `system_id` changes.
- `POLL_INTERVAL` — optional. Default `60` seconds.
- `ONCE_MODE=true` — run a single polling cycle. Required by the Fabric notebook hosting path.

Example:

```bash
docker run --rm \
  -e GBFS_FEEDS="https://gbfs.citibikenyc.com/gbfs/gbfs.json,https://gbfs.lyft.com/gbfs/2.3/chi/gbfs.json" \
  -e GBFS_SYSTEM_IDS="citibike-nyc,divvy-chicago" \
  -e CONNECTION_STRING="BootstrapServer=<host:port>;EntityPath=gbfs-bikeshare" \
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-kafka:latest
```

## Upstream data-channel audit

GBFS exposes more than the four feeds modeled here, so the bridge starts with an explicit keep / drop table.

| Feed family | GBFS file | Keep? | Reason |
|---|---|---:|---|
| Auto-discovery | `gbfs.json` | ✅ | Required to discover feed URLs per configured system. |
| Provider manifest | `manifest.json` | ❌ | Provider-level multi-dataset catalog, not a per-system real-time feed; users already provide system autodiscovery URLs. |
| Versions | `gbfs_versions.json` | ❌ | Metadata about alternate feed versions; duplicates discovery information for runtime purposes. |
| System metadata | `system_information.json` | ✅ | Reference data modeled as `org.gbfs.SystemInformation`. |
| Station metadata | `station_information.json` | ✅ | Reference data modeled as `org.gbfs.StationInformation`. |
| Station telemetry | `station_status.json` | ✅ | Telemetry modeled as `org.gbfs.StationStatus`. |
| Dockless telemetry | `free_bike_status.json` / `vehicle_status.json` | ✅ | Telemetry modeled as `org.gbfs.FreeBikeStatus`. |
| Vehicle types | `vehicle_types.json` | ❌ | Useful metadata, but excluded from this initial user-scoped contract to keep the bridge aligned with the requested four event families. |
| Regions | `system_regions.json` | ❌ | Region ids are preserved on stations; full region objects are not yet emitted as separate events in this user-scoped source. |
| Pricing plans | `system_pricing_plans.json` | ❌ | Commercial catalog data, not required for the requested operational event families. |
| Alerts | `system_alerts.json` | ❌ | Operationally useful but outside the requested four-event contract. |
| Geofencing | `geofencing_zones.json` | ❌ | Optional rich policy / GeoJSON feed outside the requested scope. |
| Vehicle availability | `vehicle_availability.json` | ❌ | Optional future-reservation feed, not required for current availability telemetry. |
| Legacy hours/calendar | `system_hours.json`, `system_calendar.json` | ❌ | Removed from modern GBFS; replaced by fields on `system_information`. |

## Event model

This source emits four first-class event types:

- `org.gbfs.SystemInformation` — system-level reference metadata
- `org.gbfs.StationInformation` — station reference metadata
- `org.gbfs.StationStatus` — station availability telemetry
- `org.gbfs.FreeBikeStatus` — dockless vehicle telemetry

Identity is stable and transport-aligned:

- `SystemInformation` → `{system_id}`
- `StationInformation`, `StationStatus` → `{system_id}/{station_id}`
- `FreeBikeStatus` → `{system_id}/{bike_id}`

## Repository layout

```text
gbfs-bikeshare/
  xreg/gbfs-bikeshare.xreg.json
  gbfs_bikeshare_core/
  gbfs_bikeshare_kafka/
  gbfs_bikeshare_mqtt/
  gbfs_bikeshare_amqp/
  gbfs_bikeshare_producer/
  gbfs_bikeshare_mqtt_producer/
  gbfs_bikeshare_amqp_producer/
  notebook/gbfs-bikeshare-feed.ipynb
  kql/gbfs-bikeshare.kql
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Deploy

### Fabric notebook feeder (poll-based)

GBFS bikeshare is a poll-based source and therefore ships a Fabric notebook at [`notebook/gbfs-bikeshare-feed.ipynb`](notebook/gbfs-bikeshare-feed.ipynb). The notebook runs `gbfs_bikeshare feed --once`, looks up the Event Stream connection string at runtime, and writes diagnostics to OneLake at `/lakehouse/default/Files/feeder-state/gbfs-bikeshare/last-run.log`.

### Fabric ACI feeder

Use the portal deploy button or the repo helper to host the Kafka container in Azure Container Instances and write into a Fabric Event Stream custom endpoint:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source gbfs-bikeshare `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

### Azure templates

- `azure-template.json` — Kafka / bring your own Event Hubs or Fabric connection string
- `azure-template-with-eventhub.json` — Kafka / provision a new Event Hub
- `azure-template-with-servicebus.json` — AMQP / provision a new Service Bus queue with Entra-authenticated sender identity
- `azure-template-mqtt.json` — MQTT / bring your own broker
- `azure-template-with-eventgrid-mqtt.json` — MQTT / provision a new Event Grid namespace broker

## Next steps

- Read [EVENTS.md](EVENTS.md) before building consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full environment-variable matrix and copy/paste deployment commands.
- Apply the generated [KQL schema](kql/gbfs-bikeshare.kql) before wiring Eventhouse tables.
