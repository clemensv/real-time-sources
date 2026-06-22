<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# GTFS Realtime

<sub>1,000+ transit agencies, vehicles, trips, alerts · Kafka · MQTT · AMQP · <a href="https://gtfs.org/">upstream</a> · <a href="https://gtfs.org/documentation/realtime/reference/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-4_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-4_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — 1,000+ transit agencies, vehicles, trips, alerts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#gtfs) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/gtfs.kql) &nbsp;·&nbsp;
[🗺️ **Fabric Map**](fabric/README.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://gtfs.org/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the upstream GTFS Realtime feed into a real-time CloudEvents stream over KAFKA / MQTT / AMQP.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://gtfs.org/>
- API / data documentation: <https://gtfs.org/documentation/realtime/reference/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

GTFS Realtime publishes operational real-time data that is useful across hazard and mobility analytics workflows, but each consumer otherwise has to build and operate its own source connector, transport adapter, and schema normalization.

This bridge provides one reusable feed for common scenarios:

- **Operations dashboards** — power near-real-time fleet, traffic, or incident views.
- **Streaming analytics** — ingest directly into Eventhouse, ADX, or a lakehouse pipeline.
- **Cross-source correlation** — join this stream with weather, hydrology, and public-safety feeds in this repository.
- **Alerting and automation** — trigger rules based on stable CloudEvents payloads and keys.
- **Research and reporting** — keep a reproducible event archive for retrospective analysis.

## Overview

**GTFS Realtime** in this repository is a streaming bridge and ships in the transport variants below:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-gtfs` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Fabric Event Streams) | Topic(s): `gtfs`, key = `{agencyid}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-gtfs-mqtt` | MQTT 5.0 broker (incl. Azure Event Grid MQTT and Fabric Real-Time Hub MQTT source) | Unified Namespace topic tree `transit/intl/gtfs/gtfs/{agencyid}/static/agency/{row_id}` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-gtfs-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch, Azure Service Bus/Event Hubs) | AMQP node `gtfs`, CloudEvents binary mode |

All variants share:

- The xRegistry contract (`xreg/gtfs.xreg.json`).
- A common upstream acquisition path and normalized event payloads.
- Stable CloudEvents subject/key identity derived from source-native identifiers.

## Key features

- Real-time source ingestion for **Global — 1,000+ transit agencies, vehicles, trips, alerts**.
- Contract-first CloudEvents output with JsonStructure schemas.
- Transport variants aligned to the same core event model.
- Deployment-ready container images for local, Azure, and Fabric-aligned topologies.

## Repository layout

```text
gtfs/
  xreg/                           # xRegistry contracts
  gtfs_amqp/
  gtfs_amqp_producer/
  gtfs_mqtt/
  gtfs_mqtt_producer/
  gtfs_producer/
  gtfs_rt_bridge/
  gtfs_rt_producer/
  kql/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Network access to the upstream data endpoint(s).
- Network access to your target broker (Kafka, MQTT, or AMQP).

This source is handled as a streaming feeder in this batch; no notebook runtime section is included.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-gtfs:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-gtfs-mqtt:latest
```

Topics follow the contract templates in [EVENTS.md](EVENTS.md); primary template: `transit/intl/gtfs/gtfs/{agencyid}/static/agency/{row_id}`.

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/gtfs' \
  ghcr.io/clemensv/real-time-sources-gtfs-amqp:latest
```

## Configuration reference

The complete environment-variable contract per image is documented in [CONTAINER.md](CONTAINER.md), including connection-string mode, direct broker parameters, authentication options, and transport-specific knobs.

## Configuring sources

GTFS has no universal public default feed. The feeder therefore supports both the original single-feed environment variables and a packaged file-based catalog. The legacy single-feed variables take precedence whenever `GTFS_RT_URLS`, `GTFS_URLS`, or `MDB_SOURCE_ID` is set.

| Variable / argument | Description |
|---|---|
| `GTFS_SOURCES_FILE` / `--gtfs-sources-file` | Path to a JSON catalog. Defaults to the packaged `gtfs_core/sources/gtfs-sources.json`. |
| `GTFS_SOURCES` / `--gtfs-sources` | Selector: comma-separated catalog `name` values, `*` for all entries, or unset for `enabled: true` entries only. |
| `GTFS_RT_URLS` / `--gtfs-rt-urls` | Legacy comma-separated GTFS-Realtime URLs. Takes precedence over the catalog. |
| `GTFS_URLS` / `--gtfs-urls` | Legacy comma-separated GTFS Schedule zip URLs. |
| `MDB_SOURCE_ID` / `--mdb-source-id` | Legacy Mobility Database source ID; the bridge resolves GTFS-RT and schedule URLs from the MDB cache path. |
| `AGENCY` / `--agency` | Agency tag used in CloudEvents subject/key identity. Required for legacy config and recommended in catalog entries. |
| `ROUTE` / `--route` | Optional route filter; defaults to `*`. |
| `GTFS_RT_HEADERS` / `--gtfs-rt-headers` | Optional realtime request headers as `Name=value` tokens. |
| `GTFS_HEADERS` / `--gtfs-headers` | Optional schedule request headers as `Name=value` tokens. |

### Catalog format

```json
{
  "sources": [
    {
      "name": "mbta-boston",
      "enabled": false,
      "description": "Massachusetts Bay Transportation Authority public feeds.",
      "agency": "mbta",
      "route": "*",
      "gtfs_rt_urls": [
        "https://cdn.mbta.com/realtime/TripUpdates.pb",
        "https://cdn.mbta.com/realtime/VehiclePositions.pb",
        "https://cdn.mbta.com/realtime/Alerts.pb"
      ],
      "gtfs_urls": ["https://cdn.mbta.com/MBTA_GTFS.zip"]
    }
  ]
}
```

| Field | Description |
|---|---|
| `name` | Stable catalog selector name. |
| `enabled` | Runs when `GTFS_SOURCES` is unset if `true`; disabled templates are skipped by default. |
| `description` | Human-readable operator/source note. |
| `gtfs_rt_urls` | List of GTFS-Realtime protobuf endpoint URLs. |
| `gtfs_urls` | List of GTFS Schedule zip URLs. |
| `mdb_source_id` | Optional Mobility Database source ID alternative to explicit URLs. |
| `agency` | Agency tag emitted in CloudEvents subjects/keys. |
| `route` | Optional route filter, default `*`. |
| `gtfs_rt_headers` / `gtfs_headers` | Optional object/list of request headers. |

### Selecting sources

- Unset `GTFS_SOURCES`: run only entries with `enabled: true`. The shipped catalog has none enabled, preserving the old “operator must configure a feed” behavior.
- `GTFS_SOURCES=*`: run every catalog entry, including disabled examples/templates.
- `GTFS_SOURCES=mbta-boston,other`: run named entries in that order; unknown names raise an error.

### Keeping secrets out of the catalog

Catalog string values expand `${ENV_VAR}` at runtime, so keys can live in the container environment or a mounted secret file instead of JSON:

```json
{
  "name": "keyed-operator",
  "enabled": true,
  "agency": "operator",
  "gtfs_rt_urls": ["https://operator.example/REPLACE_WITH_GTFS_RT_URL"],
  "gtfs_rt_headers": {"x-api-key": "${SOME_GTFS_KEY}"}
}
```

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  -e GTFS_SOURCES_FILE=/config/gtfs-sources.json \
  -e GTFS_SOURCES=keyed-operator \
  -e SOME_GTFS_KEY='<secret>' \
  -v "$PWD/gtfs-sources.json:/config/gtfs-sources.json:ro" \
  ghcr.io/clemensv/real-time-sources-gtfs:latest
```

### Known GTFS-Realtime sources

The GTFS ecosystem is decentralized: MobilityData’s [Mobility Database](https://database.mobilitydata.org/) catalogs many schedule and realtime feeds, and agencies often publish their own GTFS-Realtime endpoints. Many are free and keyless; others require registration, an API key, or custom headers. The packaged catalog intentionally ships only disabled entries:

- `mbta-boston` — disabled, fully worked, keyless MBTA GTFS-Realtime URLs plus the public GTFS Schedule zip.
- `tfnsw-sydney` — disabled, ready-to-enable Transport for NSW GTFS-Realtime feeds for Sydney / NSW trains, buses, ferries, light rail, and rail alerts; requires `TFNSW_API_KEY` in the documented `Authorization: apikey ...` header.
- `keyed-operator-template` — disabled template showing `REPLACE_WITH_*` URLs and `${SOME_GTFS_KEY}` header expansion.

## Data model

This source exposes **31 event type(s)** across **2 base message group(s)**:

- `GeneralTransitFeedRealTime.Vehicle.VehiclePosition`
- `GeneralTransitFeedRealTime.Trip.TripUpdate`
- `GeneralTransitFeedRealTime.Alert.Alert`
- `GeneralTransitFeedStatic.Agency`
- `GeneralTransitFeedStatic.Areas`
- `GeneralTransitFeedStatic.Attributions`
- `GeneralTransitFeed.BookingRules`
- `GeneralTransitFeedStatic.FareAttributes`
- `GeneralTransitFeedStatic.FareLegRules`
- `GeneralTransitFeedStatic.FareMedia`
- `GeneralTransitFeedStatic.FareProducts`
- `GeneralTransitFeedStatic.FareRules`
- … plus 19 more event type(s)

See [EVENTS.md](EVENTS.md) for the full field-level schema contract and routing metadata.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

GTFS Realtime targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/), and the bundled [Fabric Map](fabric/README.md) visualizes the live state on a basemap.

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#gtfs) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source gtfs `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#gtfs/fabric-aci)

#### Fabric Map visualization &nbsp;<sub><i>(optional, post-deploy)</i></sub>

After either hosting model has events flowing, run [`fabric/post-deploy.ps1`](fabric/README.md) (or `tools/deploy-fabric/deploy-fabric.ps1 -Source gtfs -Workspace <ws>`) to provision the bundled Fabric Map item and wire its Kusto-backed layers onto a basemap. The map updates live as new events arrive.


### Deploying into Azure Container Instances

4 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgtfs%2Fazure-template-with-eventgrid-mqtt.json)


### Self-hosted

Pull and run any of the 4 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full env-var matrix and auth variants.
- Choose Fabric ACI or direct Azure deployment based on your runtime target.
