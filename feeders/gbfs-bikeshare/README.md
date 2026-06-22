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

> Global — configurable GBFS bikeshare, scooter-share, and micromobility availability feeds

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

GBFS is the open data standard used by bikeshare, scooter-share, and shared-micromobility operators to publish station inventory, vehicle availability, and system reference data. This feeder lets mobility operations teams, city dashboards, trip planners, and streaming analytics platforms consume many GBFS systems through one normalized CloudEvents contract instead of maintaining one poller per operator.

## Upstream

- Home page: <https://gbfs.org/>
- Specification: <https://github.com/MobilityData/gbfs/blob/master/gbfs.md>
- MobilityData systems catalog: <https://github.com/MobilityData/gbfs/blob/master/systems.csv>

## Transports

| App | Image | Transport | Default shape |
| --- | --- | --- | --- |
| `gbfs_bikeshare` | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest` | Kafka/Event Hubs | CloudEvents on topic `gbfs-bikeshare`. |
| `gbfs_bikeshare_mqtt` | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-mqtt:latest` | MQTT 5 | Binary CloudEvents under `mobility/gbfs/...`. |
| `gbfs_bikeshare_amqp` | `ghcr.io/clemensv/real-time-sources-gbfs-bikeshare-amqp:latest` | AMQP 1.0 | Binary CloudEvents to address `gbfs-bikeshare`. |

## Quick start

Kafka/Event Hubs using the packaged default catalog:

```powershell
docker run --rm `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=gbfs-bikeshare" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

Select two catalog entries:

```powershell
docker run --rm `
  -e GBFS_SOURCES="citibike-nyc,bike-share-toronto" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=gbfs-bikeshare" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

Quick override without a catalog:

```powershell
docker run --rm `
  -e GBFS_FEEDS="https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json,https://gbfs.divvybikes.com/gbfs/2.3/gbfs.json" `
  -e GBFS_SYSTEM_IDS="citibike-nyc,divvy-chicago" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=gbfs-bikeshare" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

## Configuring sources

The feeder now ships a checked-in source catalog at `gbfs_bikeshare_core/gbfs_bikeshare_core/sources/gbfs-bikeshare.sources.json`. Use the catalog for repeatable deployments and keep `GBFS_FEEDS` as a one-off override.

| Variable | Purpose | Default |
| --- | --- | --- |
| `GBFS_SOURCES_FILE` | Path to a JSON catalog with GBFS source entries. Mount your own copy when you need private or regional systems. | Packaged catalog |
| `GBFS_SOURCES` | Comma-separated catalog entry `name`s to run, or `*` for every entry including disabled templates. When unset, entries with `enabled: true` run. | enabled entries |

`GBFS_FEEDS` still works for quick tests and takes precedence over the catalog whenever it is set. The legacy companion variables `GBFS_SYSTEM_IDS`, `GBFS_API_KEY`, and `GBFS_API_KEY_PARAM` remain supported for that inline path.

### Catalog format

```json
{
  "description": "GBFS source catalog...",
  "sources": [
    {
      "name": "citibike-nyc",
      "enabled": true,
      "description": "Citi Bike (New York City, US) public GBFS v2.3 auto-discovery feed operated by Lyft.",
      "autodiscovery_url": "https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json",
      "system_id": "citibike-nyc"
    },
    {
      "name": "private-operator",
      "enabled": false,
      "description": "Private operator template.",
      "autodiscovery_url": "https://operator.example/gbfs.json",
      "system_id": "private-operator",
      "api_key": "${PRIVATE_GBFS_KEY}",
      "api_key_param": "api_key"
    }
  ]
}
```

| Field | Required | Description |
| --- | ---: | --- |
| `name` | ✅ | Stable catalog selector used by `GBFS_SOURCES`. |
| `enabled` | ❌ | Defaults to `true`; disabled templates are skipped unless `GBFS_SOURCES=*` or selected by name. |
| `description` | ✅ | Human-readable operator, geography, and access notes. |
| `autodiscovery_url` | ✅ | GBFS `gbfs.json` auto-discovery URL. |
| `system_id` | ❌ | Optional stable override for the emitted `system_id`; use it to avoid operator-side identifier churn. |
| `api_key` | ❌ | Optional upstream API key. Use `${ENV_VAR}` so secrets come from the runtime environment. |
| `api_key_param` | ❌ | Query parameter used when appending `api_key`; defaults to `acl:consumerKey`. |

### Selecting sources

- Unset `GBFS_SOURCES` — poll every catalog entry with `enabled: true`.
- `GBFS_SOURCES=citibike-nyc,bike-share-toronto` — poll only those entries, in that order.
- `GBFS_SOURCES=*` — load every entry, including disabled templates. This is mostly useful for validation after editing a private catalog.
- Unknown names fail fast with a `ValueError` that lists known names.

### Keeping secrets out of the catalog

Put placeholders in the catalog and provide the secret at runtime:

```powershell
docker run --rm `
  -v ${PWD}\my-gbfs.sources.json:/app/gbfs.sources.json:ro `
  -e GBFS_SOURCES_FILE="/app/gbfs.sources.json" `
  -e GBFS_SOURCES="private-operator" `
  -e PRIVATE_GBFS_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=gbfs-bikeshare" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-gbfs-bikeshare:latest
```

### Known GBFS sources

#### Ready to configure

These entries are checked into the default catalog and were verified against the MobilityData systems catalog plus a live `gbfs.json` probe.

| Catalog name | System | Auto-discovery URL |
| --- | --- | --- |
| `citibike-nyc` | Citi Bike — New York City | `https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json` |
| `divvy-chicago` | Divvy — Chicago | `https://gbfs.divvybikes.com/gbfs/2.3/gbfs.json` |
| `bay-wheels-sf` | Bay Wheels — San Francisco Bay Area | `https://gbfs.baywheels.com/gbfs/2.3/gbfs.json` |
| `capital-bikeshare-dc` | Capital Bikeshare — Washington, DC | `https://gbfs.capitalbikeshare.com/gbfs/2.3/gbfs.json` |
| `bluebikes-boston` | Bluebikes — Boston metro | `https://gbfs.bluebikes.com/gbfs/gbfs.json` |
| `bike-share-toronto` | Bike Share Toronto — Toronto | `https://toronto.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json` |

#### Needs an adapter / not GBFS (roadmap)

- Taipei YouBike is not GBFS; it uses proprietary Taipei city / YouBike APIs and needs an adapter before it can share this feeder.
- Seoul Ddareungi is not GBFS; it uses proprietary Seoul bike APIs and needs an adapter.
- Santander Cycles London (TfL) is not GBFS; TfL publishes proprietary bike-point APIs and needs an adapter.

## Upstream data-channel audit

| Feed family | GBFS file | Keep? | Reason |
|---|---|---:|---|
| Auto-discovery | `gbfs.json` | ✅ | Required to discover feed URLs per configured system. |
| System metadata | `system_information.json` | ✅ | Reference data modeled as `org.gbfs.SystemInformation`. |
| Station metadata | `station_information.json` | ✅ | Reference data modeled as `org.gbfs.StationInformation`. |
| Station telemetry | `station_status.json` | ✅ | Telemetry modeled as `org.gbfs.StationStatus`. |
| Dockless telemetry | `free_bike_status.json` / `vehicle_status.json` | ✅ | Telemetry modeled as `org.gbfs.FreeBikeStatus`. |
| Other optional GBFS feeds | `vehicle_types.json`, `system_regions.json`, pricing, alerts, geofencing | ❌ | Useful future reference or policy data, outside the current four-event contract. |

## Event model

This source emits `org.gbfs.SystemInformation`, `org.gbfs.StationInformation`, `org.gbfs.StationStatus`, and `org.gbfs.FreeBikeStatus`. Identity is stable and transport-aligned: `{system_id}`, `{system_id}/{station_id}`, and `{system_id}/{bike_id}`.

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

Use the portal card for Azure Container Instances, Event Hubs, MQTT, AMQP, and Fabric notebook deployment: <https://clemensv.github.io/real-time-sources#gbfs-bikeshare>.

- `azure-template.json` — Kafka / bring your own Event Hubs or Fabric connection string
- `azure-template-with-eventhub.json` — Kafka / provision a new Event Hub
- `azure-template-with-servicebus.json` — AMQP / provision a new Service Bus queue with Entra-authenticated sender identity
- `azure-template-mqtt.json` — MQTT / bring your own broker
- `azure-template-with-eventgrid-mqtt.json` — MQTT / provision a new Event Grid namespace broker

## Next steps

- Read [CONTAINER.md](CONTAINER.md) for the complete container variable matrix.
- Read [EVENTS.md](EVENTS.md) before building consumers.
- Apply the generated [KQL schema](kql/gbfs-bikeshare.kql) before wiring Eventhouse tables.

