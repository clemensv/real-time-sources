# STIB-MIVB Brussels Open Data

**Country/Region**: Belgium - Brussels Capital Region
**Publisher**: STIB-MIVB (Brussels public transport operator)
**API Endpoint**: `https://data.stib-mivb.brussels/`
**Documentation**: https://data.stib-mivb.brussels/ and https://data.belgianmobility.io/en/data.html?agency=stibmivb
**Protocol**: REST (Opendatasoft JSON APIs) plus GTFS/GTFS-RT through the Belgian mobility portal
**Auth**: None for catalog access; verify per-feed limits during implementation
**Data Format**: JSON and GTFS-RT Protobuf
**Update Frequency**: Real-time - vehicle positions update about every 20 seconds
**License**: STIB-MIVB open data terms / Belgian mobility open data terms

## What It Provides

STIB-MIVB publishes one of the richer urban transit datasets in Belgium. The operator exposes real-time vehicle positions for buses, trams, and metro, stop-level waiting times, and traveler information covering disruptions and planned changes. Static line and stop data are also available, and GTFS plus GTFS-RT feeds are published through the Belgian Mobility Open Data Portal.

This is a good Brussels-focused candidate because it gives direct access to operator-native real-time data rather than only a generic GTFS-RT abstraction. The dataset mix is broad enough to support both telemetry-style events and operational alerts.

## API Details

Named real-time datasets called out in the STIB-MIVB catalog:

- `vehicle-position-rt-production` - real-time vehicle positions for active service
- `waiting-time-rt-production` - next arrivals per stop and line
- `travellers-information-rt-production` - disruptions, temporary changes, and traveler notices

The operator portal exposes table/export/API access through Opendatasoft. The Belgian Mobility Open Data Portal additionally lists STIB-MIVB GTFS and GTFS-RT resources as part of the national access point.

Observed characteristics from the catalog descriptions:

- Vehicle positions refreshed every ~20 seconds
- Coverage across metro, tram, and bus
- Waiting-time data keyed by stop and line
- Traveler information available in multiple languages
- Migration toward the centralized Belgian mobility portal is underway, so endpoint stability should be checked at implementation time

## Freshness Assessment

Strong. Vehicle positions update every ~20 seconds, which is excellent for a city transit source. Waiting-time and disruption feeds are also live operational data. This is still poll-driven from our point of view unless we rely directly on GTFS-RT feeds, but the freshness is comfortably within the repo's target range.

## Entity Model

- **Vehicle position** - line, vehicle, mode, current location, timestamp
- **Stop prediction** - stop ID, line ID, destination, expected arrivals
- **Traveler information** - disruption ID or notice, multilingual text, affected lines/stops, validity window
- **Static reference** - lines, stops, shapes, route metadata

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Vehicle positions around every 20 seconds |
| Openness | 2 | Official open data, but migration and product-level access details need confirming |
| Stability | 2 | Official operator source, but the platform is in transition toward the national portal |
| Structure | 3 | Opendatasoft catalog plus GTFS/GTFS-RT are easy to consume |
| Identifiers | 2 | Stop and line IDs are stable; exact vehicle key strategy needs inspection |
| Additive Value | 2 | Rich operator-native Brussels data, though partially overlaps GTFS-RT coverage |
| **Total** | **14/18** | |

## Notes

- This is a good source if we want a Brussels-specific bridge with richer data than a generic GTFS-RT connector.
- The most likely bridge shape is a multi-family source: vehicle positions, waiting times, and traveler information should probably not be collapsed into one schema.
- Because the platform is migrating toward `data.belgianmobility.io`, implementation should start with an endpoint audit rather than assuming the current STIB portal will remain the long-term home.
- De Lijn and TEC live in the same broader Belgian mobility ecosystem, but STIB-MIVB is the cleanest Brussels urban candidate from the shortlist.
