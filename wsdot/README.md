# WSDOT Traveler Information feeder

This feeder turns Washington State DOT traveler and ferry APIs into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://wsdot.wa.gov/>
- API / data documentation: <https://wsdot.wa.gov/traffic/api/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

State traffic centers, ferry operations, logistics planners, and public traveler-information systems use WSDOT feeds for live network status and incident-aware routing. This bridge standardizes polling, normalization, dedupe, CloudEvents shaping, and transport delivery so consumers subscribe once and reuse the same contract across platforms.

- **Traffic and mobility operations** — live dashboards and operational control-room views.
- **Route and dispatch optimization** — dynamic rerouting and ETA management under disruptions.
- **Analytics and planning** — long-running ingestion into Fabric Eventhouse / ADX / lakes.
- **Compliance and reporting** — auditable event history for public-sector and regulated workflows.
- **Cross-domain correlation** — fuse mobility events with weather, safety, and infrastructure feeds.

## Overview

**WSDOT Traveler Information** is a poll-based bridge that ingests upstream data from [Washington State DOT traveler and ferry APIs](https://www.wsdot.wa.gov/traffic/api/) and re-emits normalized CloudEvents.

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-wsdot` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | JSON CloudEvents (binary mode), key templates `{crossing_name}, {flow_data_id}, {mountain_pass_id}, {state_route_id}/{bridge_number}, {station_id}, {travel_time_id}, {trip_name}, {vessel_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-wsdot-mqtt` | MQTT 5.0 broker (incl. Azure Event Grid MQTT) | Unified-Namespace topic tree rooted under `mobility/us/wa/wsdot/...` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-wsdot-amqp` | AMQP 1.0 brokers incl. Azure Service Bus / Event Hubs | Binary CloudEvents to AMQP address `wsdot` |

All variants share:

- The same xRegistry contract (`xreg/wsdot.xreg.json`).
- The same event-family model and schema set.
- Poll-based acquisition logic with periodic refresh cycles.

## Key features

- Poll-based bridge with CloudEvents-first contract design.
- Shared event contract across Kafka, MQTT, and AMQP transports.
- Fabric-ready deployment path (Notebook and ACI hosting options).
- ARM templates for direct Azure Container Instance deployment targets.
- Source-specific event families and stable domain key templates.

## Repository layout

```text
wsdot/
  xreg/wsdot.xreg.json
  wsdot/
  wsdot_mqtt/
  wsdot_amqp/
  wsdot_producer/
  wsdot_mqtt_producer/
  wsdot_amqp_producer/
  kql/
  notebook/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS connectivity to the upstream API at `https://www.wsdot.wa.gov/traffic/api/`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.
- A writable host directory mounted at `/state` for persistent polling/dedupe state.

## Quick start with Docker

> [!IMPORTANT]
> This source is poll-based. Mount a host volume and set `STATE_FILE` so state survives container restarts.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/wsdot.json \
  -e CONNECTION_STRING="<event-hubs-or-kafka-connection-string>" \
  ghcr.io/clemensv/real-time-sources-wsdot:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/wsdot.json \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-wsdot-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/wsdot.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/wsdot' \
  ghcr.io/clemensv/real-time-sources-wsdot-amqp:latest
```

## Configuration reference

The complete environment-variable matrix for Kafka, MQTT, and AMQP images (including authentication-mode differences and Azure deployment assumptions) is documented in [CONTAINER.md](CONTAINER.md).

## Data model

This source emits the following event families (see [EVENTS.md](EVENTS.md) for full schema-level detail):

- **us.wa.wsdot.traffic** — 2 event type(s): us.wa.wsdot.traffic.TrafficFlowStation, us.wa.wsdot.traffic.TrafficFlowReading.
- **us.wa.wsdot.traveltimes** — 1 event type(s): us.wa.wsdot.traveltimes.TravelTimeRoute.
- **us.wa.wsdot.mountainpass** — 1 event type(s): us.wa.wsdot.mountainpass.MountainPassCondition.
- **us.wa.wsdot.weather** — 2 event type(s): us.wa.wsdot.weather.WeatherStation, us.wa.wsdot.weather.WeatherReading.
- **us.wa.wsdot.tolls** — 1 event type(s): us.wa.wsdot.tolls.TollRate.
- **us.wa.wsdot.cvrestrictions** — 1 event type(s): us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction.
- **us.wa.wsdot.border** — 1 event type(s): us.wa.wsdot.border.BorderCrossing.
- **us.wa.wsdot.ferries** — 1 event type(s): us.wa.wsdot.ferries.VesselLocation.

## Deploying into Microsoft Fabric

WSDOT Traveler Information supports both Fabric hosting models via the source card on the [project portal](https://clemensv.github.io/real-time-sources/#wsdot).

### Fabric Notebook feeder

Because this source is poll-based and ships a notebook asset (`notebook/`), you can run scheduled ingestion in-Fabric with:

`tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source wsdot -Workspace <fabric-workspace>`

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#wsdot/fabric-notebook)

### Fabric ACI feeder

For always-on execution, deploy a long-running Azure Container Instance feeder with:

`tools/deploy-fabric/deploy-fabric-aci.ps1 -Source wsdot -Workspace <fabric-workspace>`

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#wsdot/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source directory and have matching deploy buttons:

### MQTT — bring your own broker

Deploy MQTT against an existing MQTT 5.0 broker endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid MQTT broker

Deploy MQTT plus an Event Grid namespace broker and managed-identity role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

Deploy Kafka plus a new Event Hubs namespace and event hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-with-eventhub.json)

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Event Hubs/Fabric/Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Use [CONTAINER.md](CONTAINER.md) for full auth-mode and environment-variable details.
- Validate transport-specific routing and key templates against your downstream topology.
- Review upstream usage guidance at [Washington State DOT traveler and ferry APIs](https://www.wsdot.wa.gov/traffic/api/).
