# Ticketmaster Discovery API

## Metadata

- **Category:** public-events
- **Source:** Ticketmaster
- **API:** Discovery API v2
- **Base URL:** https://app.ticketmaster.com/discovery/v2/
- **Auth:** API key (free tier, register at developer.ticketmaster.com)
- **Transport:** REST / HTTP polling
- **Freshness:** Near-real-time; event on-sale status and schedules updated continuously
- **Openness:** Free API key required; 5 000 calls/day, 5 req/s on free tier
- **License:** Ticketmaster API Terms of Service; redistribution of aggregated data allowed for non-commercial use

## Why Interesting

Ticketmaster is the world's largest ticketing platform. The public Discovery API
exposes a broad catalogue of concerts, sports events, performing arts, theater, and
family events across North America, Europe, Australia, and other markets. The API
provides stable event identifiers, on-sale status, ticket availability signals,
venue reference data, attraction (performer/artist) reference data, and a
hierarchical classification (segment/genre/subgenre) taxonomy.

## Data Channels

| Family | Endpoint | Identity | Cadence | Keep/Drop |
|---|---|---|---|---|
| Events | `/discovery/v2/events` | `event_id` | Continuous updates, poll every 5 min | KEEP – core telemetry |
| Venues | embedded in events + `/discovery/v2/venues` | `venue_id` | Slow-changing reference | KEEP – reference data |
| Attractions | embedded in events + `/discovery/v2/attractions` | `attraction_id` | Slow-changing reference | KEEP – reference data |
| Classifications | `/discovery/v2/classifications` | `classification_id` | Rarely changes, refresh daily | KEEP – reference data |
| Suggest | `/discovery/v2/suggest` | n/a | Search aid only | DROP – not a data feed |

## Entity Model

- **Event** – scheduled public performance or competition, linked to one venue and one or more attractions and a classification (segment/genre/subgenre).
- **Venue** – physical or virtual location where the event takes place; carries address, timezone, coordinates, and capacity information.
- **Attraction** – performer, artist, sports team, or production associated with an event.
- **Classification** – hierarchical taxonomy: Segment (Music, Sports, Arts & Theatre…) → Genre → Subgenre.

## Key Questions

- Availability / inventory data (ticket counts) is gated behind partner status; the free tier exposes on-sale status, price ranges, and the availability flag.
- International Discovery API (INTL) uses the same endpoint syntax with different country codes and is included in the standard key.

## Feasibility Ratings

| Criterion | Score (0-3) | Notes |
|---|---|---|
| Freshness | 3 | Events updated continuously; on-sale status changes are near-real-time |
| Openness | 2 | Free API key required; 5 k calls/day limit; terms require attribution |
| Stability | 3 | v2 API has been stable since 2015; versioned endpoint |
| Structure | 3 | Well-documented JSON; stable IDs; embedded reference data |
| Identifiers | 3 | Stable event, venue, attraction, and classification IDs |
| Additive Value | 3 | No other real-time events source in this repo; broad global coverage |
| **Total** | **17/18** | |
