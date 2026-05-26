# Digitraffic Road feeder

This feeder turns the upstream Digitraffic Road feed into a real-time CloudEvents stream over KAFKA.

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

Digitraffic Road publishes operational real-time data that is useful across hazard and mobility analytics workflows, but each consumer otherwise has to build and operate its own source connector, transport adapter, and schema normalization.

This bridge provides one reusable feed for common scenarios:

- **Operations dashboards** — power near-real-time fleet, traffic, or incident views.
- **Streaming analytics** — ingest directly into Eventhouse, ADX, or a lakehouse pipeline.
- **Cross-source correlation** — join this stream with weather, hydrology, and public-safety feeds in this repository.
- **Alerting and automation** — trigger rules based on stable CloudEvents payloads and keys.
- **Research and reporting** — keep a reproducible event archive for retrospective analysis.

## Overview

**Digitraffic Road** in this repository is a streaming bridge and ships in the transport variants below:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-digitraffic-road` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Fabric Event Streams) | Topic(s): `digitraffic-road-maintenance`, `digitraffic-road-messages`, `digitraffic-road-sensors`, key = `{domain}`, `{situation_id}`, `{station_id}`, `{station_id}/{sensor_id}`, `{task_id}` |

All variants share:

- The xRegistry contract (`xreg/digitraffic_road.xreg.json`).
- A common upstream acquisition path and normalized event payloads.
- Stable CloudEvents subject/key identity derived from source-native identifiers.

## Key features

- Real-time source ingestion for **Finland — TMS sensors, road weather, traffic messages**.
- Contract-first CloudEvents output with JsonStructure schemas.
- Transport variants aligned to the same core event model.
- Deployment-ready container images for local, Azure, and Fabric-aligned topologies.

## Repository layout

```text
digitraffic-road/
  xreg/                           # xRegistry contracts
  digitraffic_road/
  digitraffic_road_producer/
  kql/
  tests/
  Dockerfile
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
  ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

## Configuration reference

The complete environment-variable contract per image is documented in [CONTAINER.md](CONTAINER.md), including connection-string mode, direct broker parameters, authentication options, and transport-specific knobs.

## Data model

This source exposes **10 event type(s)** across **5 base message group(s)**:

- `fi.digitraffic.road.sensors.TmsSensorData`
- `fi.digitraffic.road.sensors.WeatherSensorData`
- `fi.digitraffic.road.messages.TrafficAnnouncement`
- `fi.digitraffic.road.messages.RoadWork`
- `fi.digitraffic.road.messages.WeightRestriction`
- `fi.digitraffic.road.messages.ExemptedTransport`
- `fi.digitraffic.road.maintenance.MaintenanceTracking`
- `fi.digitraffic.road.stations.TmsStation`
- `fi.digitraffic.road.stations.WeatherStation`
- `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType`

See [EVENTS.md](EVENTS.md) for the full field-level schema contract and routing metadata.

## Deploying into Microsoft Fabric

This source is documented as a streaming feeder for this rollout. Use the **Fabric ACI feeder** model to host the container and route into a Fabric Event Stream custom endpoint, then materialize into Eventhouse with the checked-in KQL assets.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#digitraffic-road/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source folder:

- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full env-var matrix and auth variants.
- Choose Fabric ACI or direct Azure deployment based on your runtime target.
