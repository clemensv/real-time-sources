# GTFS Realtime feeder

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

## Deploying into Microsoft Fabric

GTFS targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached Eventhouse / KQL database materializes the contract from [`kql/gtfs.kql`](kql/gtfs.kql), and the bundled Fabric map assets in [`fabric/`](fabric/README.md) can wire a ready-made transit visualization after the data plane is live.

This source's catalog entry is container-only (`notebook: false`), so the supported Fabric hosting model is the always-on **Fabric ACI feeder**.

### Fabric ACI feeder

Deploy with `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source gtfs -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>` (the portal button wraps the same flow for you). The script provisions the Eventhouse, applies [`kql/gtfs.kql`](kql/gtfs.kql), creates the Event Stream custom endpoint, deploys the Azure Container Instance with the connection string wired in, and auto-invokes [`fabric/post-deploy.ps1`](fabric/post-deploy.ps1) unless you skip the post-deploy hook.

For the map layers, helper functions, and standalone re-wire workflow, see [`fabric/README.md`](fabric/README.md).

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#gtfs/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source folder:

- **azure-template-mqtt.json** (mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-mqtt.json)
- **azure-template-with-eventgrid-mqtt.json** (with eventgrid mqtt)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-with-eventgrid-mqtt.json)
- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full env-var matrix and auth variants.
- Choose Fabric ACI or direct Azure deployment based on your runtime target.
