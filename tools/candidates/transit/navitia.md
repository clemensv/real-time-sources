# Navitia — Open Journey Planner with Real-Time

**Country/Region**: Global (primary coverage: France, Switzerland, Brazil, and 20+ regions)
**Publisher**: Hove (formerly Kisio Digital, part of Keolis/SNCF group)
**API Endpoint**: `https://api.navitia.io/v1/`
**Documentation**: https://doc.navitia.io/
**Protocol**: REST/JSON (HAL-style hypermedia)
**Auth**: API key required (free tier: 90 days trial with 5,000 req/day)
**Data Format**: JSON (HAL hypermedia links)
**Update Frequency**: Real-time — integrates GTFS-RT and SIRI feeds from participating agencies
**License**: Open source engine (AGPLv3 — github.com/hove-io/navitia); hosted API has usage terms

## What It Provides

Navitia is an open-source journey planning engine (alternative to OpenTripPlanner) with a powerful hosted API that integrates real-time data. It covers:

- **France**: major cities including Île-de-France (Paris region), Lyon, Bordeaux, Strasbourg, and more — real-time integration with SIRI feeds
- **Switzerland**: SBB integration
- **Brazil**: São Paulo (SPTrans integration)
- **20+ regions worldwide**: wherever Keolis/Hove operates or partners
- **Multi-modal**: transit, bike-sharing, car-sharing, walking, cycling

The hosted API at `api.navitia.io` demonstrated working authentication with a demo key — returning coverage information with links to available regions.

## API Details

Confirmed: demo API key `3b036afe-0110-4202-b9ed-99718476c2e0` returned 200 with coverage data (using Basic auth).

### Key Endpoints

- `GET /v1/coverage` — list available regions/datasets
- `GET /v1/coverage/{region}/stop_areas?q={query}` — search stops
- `GET /v1/coverage/{region}/stop_areas/{id}/departures` — real-time departure board
- `GET /v1/coverage/{region}/journeys?from={coord}&to={coord}` — journey planning with real-time
- `GET /v1/coverage/{region}/disruptions` — service disruptions
- `GET /v1/coverage/{region}/lines/{id}/vehicle_journeys` — line schedules

### Hypermedia Design

Responses follow HAL (Hypertext Application Language) with navigable `links`:
```json
{
  "links": [
    { "href": "https://api.navitia.io/v1/coverage/", "rel": "coverage", "type": "coverage" },
    { "href": "https://api.navitia.io/v1/coord/...", "rel": "coord", "type": "coord" }
  ]
}
```

The API is self-describing — you can navigate the entire data model by following links.

## Freshness Assessment

Good for covered regions. Where Navitia integrates SIRI or GTFS-RT feeds, departure boards and journey plans include real-time delay and disruption information. The quality depends on the underlying agency's real-time feed. French cities with Keolis operations tend to have the best real-time integration. The demo key provides read access to multiple regions — useful for evaluating data quality.

## Entity Model

- **StopArea**: id, name, coord, administrative_regions, lines, codes (external IDs)
- **Departure**: display_informations (direction, label, color), stop_date_time (departure_date_time, data_freshness: "realtime" | "base_schedule"), route, stop_point
- **Journey**: sections (public_transport, walking, transfer), departure/arrival, duration, nb_transfers, co2_emission
- **Disruption**: id, status, severity, messages, impacted_objects (lines, stop_areas, networks), application_periods
- **Line**: id, name, code, color, opening_time, closing_time, physical_modes

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 2     | Real-time where SIRI/GTFS-RT feeds are integrated            |
| Openness        | 2     | Free trial tier (90 days, 5K req/day); open source engine    |
| Stability       | 3     | Backed by Keolis/SNCF; running for 10+ years                 |
| Structure       | 3     | HAL hypermedia — self-describing, well-documented, clean JSON |
| Identifiers     | 2     | Navitia-internal IDs with external code mappings              |
| Additive Value  | 2     | Multi-region aggregator with real-time; HAL is architecturally interesting |
| **Total**       | **14/18** |                                                           |

## Notes

- Navitia's open-source engine (AGPLv3) means you can self-host it — no dependency on the hosted API. The source is at github.com/hove-io/navitia.
- The HAL hypermedia design is architecturally distinctive — the API is fully navigable without documentation, which is rare in transit APIs.
- Navitia's `data_freshness` field explicitly marks each departure as "realtime" or "base_schedule" — clear provenance of data quality.
- For French transit, Navitia is a strong complement to the SNCF/France PAN candidate — it covers urban transit in cities where SNCF covers intercity/rail.
- The `disruptions` endpoint aggregates SIRI-SX (Situation Exchange) data into a clean JSON format — could be a useful abstraction layer over raw SIRI.
- Navitia competes with OpenTripPlanner in the journey planning space — OTP is more popular for self-hosting, Navitia has a better hosted API.
