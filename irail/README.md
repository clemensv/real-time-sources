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
