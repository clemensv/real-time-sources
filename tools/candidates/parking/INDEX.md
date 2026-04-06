# Parking Availability Candidates

Real-time parking garage and lot occupancy data sources. Parking data is highly fragmented — each city typically operates its own parking guidance system. Aggregators like ParkAPI provide multi-city coverage with a unified schema. DATEX II is the EU standard for parking data exchange.

## Candidates

| Candidate | Region | Score | Protocol | Key Value |
|-----------|--------|-------|----------|-----------|
| [ParkAPI (ParkenDD)](parkapi-germany.md) | **DE + EU (30+ cities)** | 16/18 | REST | Open-source aggregator; one API for 30+ cities |
| [Cologne Parking](cologne-parking.md) | Germany — Cologne | 13/18 | REST (Esri) | Direct city data; already in ParkAPI |
| [Ghent Parking](ghent-parking.md) | Belgium — Ghent | 16/18 | REST (Opendatasoft) | Clean real-time data; Opendatasoft pattern reusable |
| [NDW Parking Netherlands](ndw-parking-netherlands.md) | Netherlands | 17/18 | DATEX II v3 | Government truck parking; EU-standard format |
| [RDW Parking Netherlands](rdw-parking-netherlands.md) | Netherlands | 15/18 | REST (Socrata) | Static reference data; complements NDW |

## Recommended Approach

1. **Build a ParkAPI bridge** — immediate access to 30+ cities across Germany and Europe. One API, normalized schema, actively maintained. The highest-value first step for parking data.

2. **Build an NDW DATEX II parking bridge** — truck parking with real-time occupancy in EU-standard format. Building a DATEX II parking parser enables integration with other European countries' parking data. Complements the road traffic DATEX II work.

3. **Build an Opendatasoft parking pattern** — Ghent demonstrates the approach. Opendatasoft powers open data portals for hundreds of European cities (Paris, Bordeaux, Nantes, Brussels, etc.). A generic Opendatasoft parking bridge could cover many cities.

4. **Cologne** is already in ParkAPI — no standalone bridge needed.

5. **RDW** provides valuable reference data (capacity, specifications) but no real-time occupancy. Use as enrichment for NDW data.

## Coverage Summary

- **Multi-city aggregator**: ParkAPI — 30+ cities (Aachen, Basel, Dresden, Freiburg, Hamburg, Köln, Nürnberg, Zürich, etc.)
- **Netherlands**: NDW (real-time truck parking) + RDW (static reference)
- **Belgium**: Ghent (Opendatasoft — pattern reusable for other cities)
- **EU standard**: DATEX II v3 parking extension — cross-border interoperability
