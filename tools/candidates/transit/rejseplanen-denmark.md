# Rejseplanen — Denmark National Journey Planner

**Country/Region**: Denmark (national)
**Publisher**: Rejseplanen A/S (Danish national journey planning company)
**API Endpoint**: `https://rejseplanen.dk/api/` (v2)
**Documentation**: https://labs.rejseplanen.dk/ (developer portal)
**Protocol**: REST/JSON (HAFAS-based)
**Auth**: API key required (free registration via labs.rejseplanen.dk)
**Data Format**: JSON or XML (configurable)
**Update Frequency**: Real-time — departure boards include live delay information
**License**: Open data (Danish public transit open data terms)

## What It Provides

Rejseplanen is Denmark's national journey planner, covering all Danish public transport:

- **DSB (Danish State Railways)**: S-tog (Copenhagen S-train), regional trains, IC/ICE
- **Movia**: Copenhagen region buses
- **Nordjyllands Trafikselskab (NT)**: North Jutland buses
- **Midttrafik**: Central Jutland buses
- **Sydtrafik**: South Jutland buses
- **FynBus**: Funen island buses
- **Copenhagen Metro** (Cityringen M1-M4)
- **Ferries**: domestic ferry services

The API provides departure boards with real-time delays, journey planning, and location search.

## API Details

The API is HAFAS-based (Hacon), similar to many European railway APIs (ÖBB, SBB, DB). Version 1 (`xmlopen.rejseplanen.dk`) was deprecated and shut down. Version 2 is the current API at `rejseplanen.dk/api/`.

Key endpoints (v2):

- `GET /departureBoard?id={stopId}&format=json` — live departure board
- `GET /arrivalBoard?id={stopId}&format=json` — live arrival board
- `GET /trip?originId={id}&destId={id}&format=json` — journey planning
- `GET /location.name?input={query}&format=json` — stop/station search

Real-time information appears as deviation fields (delay in minutes, cancellation flags, track changes) on departure board entries.

Registration is through the Rejseplanen Labs developer portal. The v1 API returned a 299 status with a deprecation notice pointing to v2 — confirming the migration.

## Freshness Assessment

Moderate to good. DSB trains and Copenhagen Metro have reliable real-time data with delay predictions. Bus operators vary — Movia (Copenhagen) has good real-time; smaller regional operators may be schedule-only. The HAFAS backend is the same proven engine used by Deutsche Bahn and other major European railways.

## Entity Model

- **Departure/Arrival**: name (line), type (IC/S/Bus/Metro), stop, direction, datetime, real-time datetime, track, cancelled flag, journey detail reference
- **Trip**: legs with origin/destination, departure/arrival times, real-time adjustments, transport type, operator
- **Location**: id, name, coordinates, type (stop/address/POI)
- Stop IDs use the Danish national stop numbering system

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 2     | Real-time for trains/metro; variable for buses                |
| Openness        | 2     | Free API key required; v2 docs behind developer portal        |
| Stability       | 2     | v1→v2 migration shows active development but also API churn   |
| Structure       | 2     | HAFAS-based JSON — well-known structure but proprietary schema|
| Identifiers     | 2     | Danish national stop IDs; HAFAS journey references            |
| Additive Value  | 1     | HAFAS is same engine as DB — limited new protocol territory   |
| **Total**       | **11/18** |                                                           |

## Notes

- Rejseplanen's HAFAS-based API shares the same underlying engine as DB (Germany), ÖBB (Austria), and SBB (Switzerland). A generic HAFAS bridge could cover multiple countries.
- Denmark also publishes GTFS and some GTFS-RT feeds through Rejseplanen — the GTFS-RT feeds would be coverable by the existing bridge.
- The v1→v2 migration (with v1 returning a 299 deprecation response) is a cautionary tale about API stability for proprietary journey planners.
- Copenhagen Metro (driverless M1-M4) has excellent real-time data since it's a fully automated system.
- For Nordic completeness, Rejseplanen pairs with Entur (Norway), Trafiklab (Sweden), and Digitransit (Finland).
