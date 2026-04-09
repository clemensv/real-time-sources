# WSDOT Container

## Overview

This container bridges the WSDOT Traveler Information API and Washington
State Ferries API to Apache Kafka endpoints. It polls eight data channels
covering traffic flow, travel times, mountain pass conditions, road weather,
toll rates, commercial vehicle restrictions, US-Canada border crossing wait
times, and ferry vessel locations, emitting all data as CloudEvents.

For the full event catalog, see [EVENTS.md](EVENTS.md).

## Container Image

```bash
docker pull ghcr.io/clemensv/real-time-sources/wsdot:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka connection string (see below) |
| `WSDOT_ACCESS_CODE` | Yes | — | WSDOT API access code ([register free](https://www.wsdot.wa.gov/traffic/api/)) |
| `POLLING_INTERVAL` | No | `120` | Polling interval in seconds |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain Kafka without TLS |
| `REGION_FILTER` | No | — | Comma-separated region names for traffic flow (default: all) |

## Running with Plain Kafka

```bash
docker run -d \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=wsdot" \
  -e WSDOT_ACCESS_CODE="your-access-code" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/wsdot:latest
```

## Running with Azure Event Hubs

```bash
docker run -d \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=wsdot" \
  -e WSDOT_ACCESS_CODE="your-access-code" \
  ghcr.io/clemensv/real-time-sources/wsdot:latest
```

## Running with Fabric Event Streams

Use the Kafka connection string from your Fabric Event Stream custom
endpoint. The format is the same as Azure Event Hubs.

## Behavior

1. At startup, fetches all data from every API channel and emits reference
   events (TrafficFlowStation, WeatherStation) and initial telemetry for all
   channels.
2. Enters a polling loop, re-fetching all channels every `POLLING_INTERVAL`
   seconds and emitting updated events.
3. Reference data (stations, CV restrictions) is refreshed every 6 hours.
4. Each channel uses its own Kafka key (see Data Model below).

## Data Channels

| Channel | Events/Poll | Key |
|---------|-------------|-----|
| Traffic Flow | ~1,400 | `{flow_data_id}` |
| Travel Times | ~163 | `{travel_time_id}` |
| Mountain Passes | 16 | `{mountain_pass_id}` |
| Road Weather | ~134 | `{station_id}` |
| Toll Rates | ~84 | `{trip_name}` |
| CV Restrictions | ~354 (ref only) | `{state_route_id}/{bridge_number}` |
| Border Crossings | 11 | `{crossing_name}` |
| Ferry Vessels | ~21 | `{vessel_id}` |

## Region Filter

To reduce traffic flow volume, set `REGION_FILTER` to a comma-separated
list of region names:

```bash
-e REGION_FILTER="Northwest,Olympic"
```

Valid regions: `Eastern`, `Northwest`, `Olympic`, `Southwest`.

The filter applies only to traffic flow data; all other channels are always
fetched in full.

## Upstream Sources

- WSDOT Traveler Information API: https://www.wsdot.wa.gov/traffic/api/
- Washington State Ferries API: https://www.wsdot.wa.gov/ferries/api/vessels/rest/
- License: Public domain (Washington State government data)

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-with-eventhub.json)
