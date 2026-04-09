# King County Marine Bridge

## Overview

**King County Marine Bridge** polls the current King County marine buoy and mooring raw-data datasets and emits station reference events plus normalized water-quality readings to Kafka as CloudEvents.

The source focuses on near-real-time raw buoy and mooring telemetry published on `data.kingcounty.gov`. It excludes periodic laboratory programs and historical backfill datasets that are not part of the current operational feed.

## Upstream Audit

| Family | Transport | Identity | Keep/Drop | Why |
|---|---|---|---|---|
| Coupeville Wharf Mooring Raw Data Output (`6trh-ufm8`) | Socrata JSON | `station_id + observation_time` | Keep | Current 15-minute mooring telemetry. |
| Penn Cove Entrance Buoy Raw Data Output - Surface (`59w7-7h7b`) | Socrata JSON | `station_id + observation_time` | Keep | Current surface buoy telemetry. |
| Penn Cove Entrance Buoy Raw Data Output - Bottom (`fkix-9yyf`) | Socrata JSON | `station_id + observation_time` | Keep | Current bottom-sensor telemetry. |
| Port Susan Buoy Raw Data Output (`d5u3-dkbj`) | Socrata JSON | `station_id + observation_time` | Keep | Current buoy telemetry. |
| Port Susan historical raw output (`b8te-p5dc`) | Socrata JSON | historical only | Drop | Superseded backfill dataset. |
| Beach bacteria and periodic marine lab programs | separate datasets/pages | different lifecycle | Drop | Not near-real-time buoy telemetry. |
| Dataset metadata `/api/views/{id}` | Socrata metadata API | `station_id` | Keep | Used to emit station reference events and parse location metadata. |

## Event Model

- **Station** — reference event for each active buoy/mooring dataset, keyed by `station_id`
- **WaterQualityReading** — normalized buoy/mooring reading keyed by `station_id`

The bridge intentionally drops undocumented vendor/diagnostic fields that lack usable field descriptions in the public metadata, such as opaque `suna_m_parameter3`, `suna_m_parameter4`, and similar counters. The retained schema covers the documented and consistently interpretable environmental measurements.

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Kafka/Event Hubs/Fabric connection string |
| `KING_COUNTY_MARINE_STATE_FILE` | Dedupe state file |

## Upstream Links

- King County buoy search surface: https://data.kingcounty.gov/
- Catalog search: https://api.us.socrata.com/api/catalog/v1?search_context=data.kingcounty.gov&q=buoy
- Marine monitoring portal: https://green2.kingcounty.gov/marine-buoy/
