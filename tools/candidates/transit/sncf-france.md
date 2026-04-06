# SNCF / transport.data.gouv.fr (France Rail Real-Time)

**Country/Region**: France
**Publisher**: SNCF / Ministère de la Transition Écologique (via PAN — Point d'Accès National)
**API Endpoint**: Listed on https://transport.data.gouv.fr/ — per-operator SIRI-Lite and GTFS-RT endpoints
**Documentation**: https://doc.transport.data.gouv.fr/
**Protocol**: SIRI-Lite (REST) + GTFS-RT + SIRI (SOAP)
**Auth**: None for most feeds (open by default per French regulation)
**Data Format**: XML (SIRI-Lite), Protobuf (GTFS-RT), XML (SIRI SOAP)
**Update Frequency**: Every 30 seconds (GTFS-RT snapshot); SIRI-Lite per request
**License**: Licence Ouverte v2.0 / ODbL (varies by operator)

## What It Provides

France's national transport data portal (Point d'Accès National — PAN) aggregates real-time transit data from across the country. The SNCF dataset is the crown jewel, covering:

- **TGV, Intercités, TER** (regional trains) — real-time delays, cancellations, platform changes
- **219 transit networks** with real-time data listed on the PAN
- **39 networks with native SIRI feeds**, 193 with GTFS-RT, 7 with SIRI-Lite

SIRI-Lite is the French adaptation of SIRI for open-data consumption — it uses the same data model as SIRI but is accessed via REST (HTTP GET) rather than SOAP, making it far easier to consume.

## API Details

The PAN catalogs real-time feeds per operator. For SNCF specifically:

- GTFS-RT feeds for TGV/IC/TER (trip updates, vehicle positions, service alerts)
- SIRI-Lite EstimatedTimetable endpoint for the full network snapshot
- NeTEx static data as the reference timetable

The SIRI-Lite specification (French SIRI profile) defines:
- `EstimatedTimetable` — mandatory; full network snapshot of current delays/cancellations
- `StopMonitoring` — next departures at a stop
- `VehicleMonitoring` — vehicle positions
- `GeneralMessage` / `SituationExchange` — disruption alerts

French regulation requires: no authentication for open data, no rate limiting (where technically feasible), and publication on the PAN.

Other notable networks on the PAN:
- Île-de-France Mobilités (IDFM) — Paris metro/bus/tram (SIRI-Lite)
- Lyon TCL, Toulouse Tisséo, Marseille RTM — all with real-time feeds

## Freshness Assessment

Good. SNCF GTFS-RT is updated every 30 seconds. SIRI-Lite feeds vary by operator — most update every 30–60 seconds. The PAN proxies GTFS-RT feeds to handle request load. SIRI/SIRI-Lite endpoints are served directly by operators.

## Entity Model

- SIRI-Lite follows standard SIRI 2.0 data model (French profile)
- `EstimatedVehicleJourney` with `EstimatedCall` for each stop
- `MonitoredStopVisit` for stop-centric queries
- References GTFS/NeTEx IDs for stops, routes, trips
- GTFS-RT uses standard `TripUpdate`, `VehiclePosition`, `Alert` entities

## Feasibility Rating

| Criterion       | Score | Notes                                                         |
|-----------------|-------|---------------------------------------------------------------|
| Freshness       | 3     | 30 s updates for SNCF; varies by operator                     |
| Openness        | 3     | Licence Ouverte, no auth required for most feeds               |
| Stability       | 2     | PAN is government-backed but individual operator feeds vary    |
| Structure       | 3     | SIRI-Lite (French profile) + GTFS-RT — well-standardized      |
| Identifiers     | 2     | Mix of GTFS IDs and French national stop codes; some variation |
| Additive Value  | 3     | SIRI-Lite is distinct from pure GTFS-RT; SNCF is unique source|
| **Total**       | **16/18** |                                                            |

## Notes

- The SIRI-Lite protocol is particularly interesting — it's the "REST version of SIRI" and could serve as a simpler entry point for SIRI protocol support than full SIRI SOAP.
- Île-de-France Mobilités (Paris region) is arguably the highest-value single network after SNCF — covers RATP metro, RER, bus, tram.
- The PAN acts as a GTFS-RT proxy (caching/redistributing feeds) but does NOT proxy SIRI — each operator hosts their own SIRI endpoint.
- French open data regulation (LOM law) mandates real-time publication, giving long-term stability assurance.
- Could implement as a single "France PAN" bridge that discovers and aggregates multiple operator feeds from the catalog.
