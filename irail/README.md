# iRail Belgian Railway Bridge

Real-time Belgian railway data bridge to Apache Kafka via CloudEvents.

## Overview

This source bridges the [iRail API](https://docs.irail.be/) to Apache
Kafka. iRail provides real-time data for the Belgian national railway
network operated by NMBS/SNCB (Nationale Maatschappij der Belgische
Spoorwegen / Société Nationale des Chemins de fer Belges).

The bridge polls the iRail liveboard API for approximately 600 Belgian
railway stations, emitting station metadata as reference events and real-time
departure boards as telemetry events in CloudEvents format.

## Data Model

### Station (Reference)

Station metadata including the 9-digit UIC-derived NMBS identifier,
geographic coordinates, and multilingual names. Emitted at startup.

### StationBoard (Telemetry)

A snapshot of the current departure board for a station. Contains an array
of departures with real-time delay information, platform assignments,
cancellation status, vehicle identifiers, and crowd-sourced occupancy
estimates. Polled periodically for each station.

## Upstream API

- Documentation: https://docs.irail.be/
- Rate limits: 3 requests/second with 5 burst
- No authentication required
- License: iRail open data

## Channel Audit

| Endpoint | Decision | Reason |
|---|---|---|
| `/stations/` | Keep | Reference data for all NMBS stations |
| `/liveboard/` | Keep | Core real-time departure data with delays |
| `/vehicle/` | Drop | Requires known vehicle IDs; data available through liveboard |
| `/connections/` | Drop | Trip planner (query-based A→B), not a feed |
| `/composition/` | Drop | Carriage composition, noted as buggy in API docs |
| `/disturbances/` | Drop | No stable unique identifier for keying |
| `/feedback/` | Drop | POST endpoint for crowd-sourced occupancy |
| `/logs/` | Drop | API usage analytics |

## Running

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.
See [EVENTS.md](EVENTS.md) for the full event catalog.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-with-eventhub.json)

## Fabric notebook hosting

This source can also be hosted as a scheduled Microsoft Fabric notebook (see `irail/notebook/irail-feed.ipynb`) deployed via [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1).

## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-irail-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variants for iRail Belgian railway station metadata and live board snapshots. Topics are retained QoS-1 state leaves under transit/be/irail/irail/{station_id}/{event}. The station_id topic axis preserves the existing Kafka/CloudEvents subject. Use transit/be/irail/irail/{station_id}/# for one station, transit/be/irail/irail/+/station-board for all departure boards, and transit/be/irail/irail/+/arrival-board for all arrival boards. Board snapshots use message expiry so stale liveboards age out if polling stops.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/irail.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `transit/be/irail/irail/{station_id}/info` | `be.irail.Station` | QoS 1, retain=true |
| `transit/be/irail/irail/{station_id}/station-board` | `be.irail.StationBoard` | QoS 1, retain=true, expiry=900s |
| `transit/be/irail/irail/{station_id}/arrival-board` | `be.irail.ArrivalBoard` | QoS 1, retain=true, expiry=900s |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.
