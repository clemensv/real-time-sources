# Parking Availability Candidates

Real-time parking garage and lot occupancy data sources. Parking data is highly fragmented — each city typically operates its own parking guidance system. Aggregators like ParkAPI provide multi-city coverage with a unified schema. DATEX II is the EU standard for parking data exchange. Opendatasoft powers parking data portals in dozens of European and Australian cities.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [Melbourne Parking Sensors](melbourne-parking-sensors.md) | **Australia — Melbourne** | **18/18** | REST (Opendatasoft) | 3,309 in-ground bay sensors — individual space-level data |
| [Singapore LTA Carparks](singapore-lta-carparks.md) | **Singapore** | **17/18** | REST (OData) | Island-wide carpark availability; part of comprehensive LTA platform |
| [NDW Parking Netherlands](ndw-parking-netherlands.md) | Netherlands | **17/18** | DATEX II v3 | Government truck parking; EU-standard format |
| [ParkAPI (ParkenDD)](parkapi-germany.md) | **DE + EU (30+ cities)** | 16/18 | REST | Open-source aggregator; one API for 30+ cities |
| [Ghent Parking](ghent-parking.md) | Belgium — Ghent | 16/18 | REST (Opendatasoft) | Clean real-time data; Opendatasoft pattern reusable |
| [Swiss Parking (Basel + Zürich)](swiss-parking.md) | Switzerland | 16/18 | REST | Real-time garage occupancy; via ParkenDD + native portals |
| [TfL Car Parks London](tfl-carparks-london.md) | UK — London | 15/18 | REST | Park & Ride at Tube/rail stations; same TfL API as bikeshare |
| [RDW Parking Netherlands](rdw-parking-netherlands.md) | Netherlands | 15/18 | REST (Socrata) | Static reference data; complements NDW |
| [Cologne Parking](cologne-parking.md) | Germany — Cologne | 13/18 | REST (Esri) | Direct city data; already in ParkAPI |

## Recommended Approach

1. **Build a ParkAPI bridge** — immediate access to 30+ cities across Germany, Switzerland, Denmark, and other European countries. One API, normalized schema, actively maintained. The highest-value first step for parking data.

2. **Build an NDW DATEX II parking bridge** — truck parking with real-time occupancy in EU-standard format. Building a DATEX II parking parser enables integration with other European countries' parking data. Complements the road traffic DATEX II work.

3. **Build an Opendatasoft parking pattern** — Melbourne (3,309 bay sensors), Ghent (13 garages), and Basel all use Opendatasoft. A generic Opendatasoft parking bridge could cover many cities across multiple continents.

4. **Build a Singapore LTA carpark bridge** — the LTA DataMall platform provides comprehensive city-state-wide parking data alongside traffic data. One API key unlocks everything.

5. **Build a TfL parking bridge** — London car parks through the same TfL API used for Santander Cycles. Combines naturally with existing TfL work.

6. **Cologne** is already in ParkAPI — no standalone bridge needed.

7. **RDW** provides valuable reference data (capacity, specifications) but no real-time occupancy. Use as enrichment for NDW data.

## Sources Investigated but Not Viable

The following sources were researched but did not yield open real-time parking APIs:

- **Paris**: No real-time parking API on opendata.paris.fr — operators (Saemes, Indigo) don't publish open data
- **Berlin**: No parking data on daten.berlin.de
- **Stockholm**: No open parking API found
- **Copenhagen**: Portal unreachable; Aarhus available via ParkAPI
- **Madrid**: Static inventory only (datos.madrid.es) — no real-time occupancy
- **Barcelona BSM**: Real-time data exists but requires authentication token
- **Vienna**: WFS parking zone geometries only — no real-time garage occupancy
- **SFpark (San Francisco)**: Original API discontinued; SFMTA data unavailable
- **Airport parking**: No major airport publishes open real-time parking APIs
- **Smart platforms**: INRIX/ParkMe (commercial), SpotHero (no API), JustPark (no API)
- **APDS**: Data standard specification, not a data feed

## Coverage Summary

- **Multi-city aggregator**: ParkAPI — 30+ cities (Aachen, Basel, Bonn, Dortmund, Dresden, Freiburg, Hamburg, Köln, Nürnberg, Zürich, etc.)
- **Netherlands**: NDW (real-time truck parking) + RDW (static reference)
- **Belgium**: Ghent (Opendatasoft — pattern reusable for other cities)
- **Switzerland**: Basel + Zürich (via ParkAPI and native portals)
- **UK**: London (TfL car parks at Tube/rail stations)
- **Australia**: Melbourne (3,309 individual bay sensors — unique dataset)
- **Asia-Pacific**: Singapore (island-wide via LTA DataMall)
- **EU standard**: DATEX II v3 parking extension — cross-border interoperability
