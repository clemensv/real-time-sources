# UK Bus Open Data Service (BODS) — SIRI-VM

**Country/Region**: United Kingdom
**Publisher**: Department for Transport (DfT)
**API Endpoint**: `https://data.bus-data.dft.gov.uk/api/v1/datafeed/` (SIRI-VM bulk download and streaming)
**Documentation**: https://data.bus-data.dft.gov.uk/guidance/
**Protocol**: SIRI-VM (Service Interface for Real-time Information — Vehicle Monitoring)
**Auth**: API Key (free registration required)
**Data Format**: XML (SIRI 2.0 profile)
**Update Frequency**: ~10 seconds per operator feed; bulk snapshot every 10–30 s
**License**: Open Government Licence v3.0 (OGL v3)

## What It Provides

BODS is the UK government's mandatory open data service for bus operators. Since January 2021, all bus operators in England with local service registrations are legally required to publish:

- **Real-time vehicle locations** via SIRI-VM — GPS positions, bearing, delay, route, destination, scheduled/actual times
- **Timetable data** in TransXChange format (the UK NeTEx precursor)
- **Fares data** in NeTEx

The SIRI-VM feed covers over 30,000 buses across England at peak times, making it one of the largest mandated open SIRI deployments in the world.

## API Details

The BODS API exposes several endpoints:

- `GET /api/v1/datafeed/` — lists available SIRI-VM data feeds
- `GET /api/v1/datafeed/{id}/` — retrieves a specific operator's SIRI-VM feed
- `GET /api/v1/datafeed/?operatorRef={NOC}` — filter by National Operator Code
- Bulk download endpoint provides a single SIRI-VM XML snapshot of all current vehicle activities across England

The XML conforms to SIRI 2.0 VM profile (UK DfT BODS profile). Each `VehicleActivity` element contains:
- `RecordedAtTime`, `ValidUntilTime`
- `MonitoredVehicleJourney` with `LineRef`, `DirectionRef`, `PublishedLineName`, `OperatorRef`, `OriginRef`, `DestinationRef`, `OriginAimedDepartureTime`
- `VehicleLocation` (longitude, latitude), `Bearing`, `BlockRef`, `VehicleRef`
- `Delay` (ISO 8601 duration)

Rate limits are generous — the service is designed for bulk consumption.

## Freshness Assessment

Excellent. Feeds are updated every 10–30 seconds depending on the operator's AVL system. DfT monitors compliance and publishes data quality scores. The SIRI-VM data is a live aggregation of all English bus operators' AVL feeds.

## Entity Model

- **VehicleActivity**: the core real-time entity — one per vehicle per update cycle
- **MonitoredVehicleJourney**: trip-level context (route, direction, stops)
- **VehicleLocation**: lat/lon fix
- Links to TransXChange static timetable data via `LineRef`, `OperatorRef`, NaPTAN stop codes

## Feasibility Rating

| Criterion       | Score | Notes                                                    |
|-----------------|-------|----------------------------------------------------------|
| Freshness       | 3     | 10–30 s updates, legally mandated                        |
| Openness        | 3     | OGL v3, free registration, no commercial restrictions    |
| Stability       | 3     | Government-mandated platform, multi-year commitment      |
| Structure       | 3     | SIRI 2.0 — international standard, well-defined schema   |
| Identifiers     | 2     | NaPTAN stops, NOC operators — but some operator IDs vary |
| Additive Value  | 3     | Only native SIRI-VM source; not a GTFS-RT feed           |
| **Total**       | **17/18** |                                                      |

## Notes

- This is the premier SIRI-VM source globally — mandated by law, covering all English bus operators.
- Scotland and Wales have separate arrangements (Traveline Scotland uses SIRI too, but through different channels).
- The BODS platform also validates data quality and publishes compliance reports.
- A GTFS-RT conversion exists, but the native SIRI-VM is the authoritative format and contains fields (like `BlockRef`, `VehicleRef`) not always preserved in conversions.
- Natural complement to the existing GTFS-RT bridge — demonstrates SIRI protocol handling.
