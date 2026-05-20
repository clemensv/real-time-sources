---
name: Billetto
category: public-events
status: implemented
source_url: https://billetto.dk/api/v3/public/events
---

# Billetto — European Ticketed Events

## Summary

Billetto is a pan-European ticketing and event-discovery platform operating in
Denmark, the United Kingdom, Germany, Sweden, Norway, Finland, Belgium, Austria,
and Ireland. The public REST API provides a paginated list of upcoming, publicly
advertised events with schedule, venue, organizer, pricing, and availability
information.

## API Details

- **Base URL**: `https://billetto.dk/api/v3/public/events`
- **Transport**: HTTPS REST / JSON
- **Auth**: `Api-Keypair: <key_id>:<secret>` header  
  (free developer account required at <https://go.billetto.com/en-gb/resources/developers>)
- **Pagination**: cursor-based via `next_url` and `has_more` response fields
- **Cadence**: events change slowly; polling every 5 minutes is adequate

## Available Data Channels

| Family | Endpoint | Identity | Cadence | Keep/Drop |
|--------|----------|----------|---------|-----------|
| Public Events | `GET /api/v3/public/events` | `id` (integer) | poll | KEEP — primary event schedules, availability, venue, organizer |

No separate reference data API exists for venues or organizers; all entity
metadata is embedded in the event record itself.

## Entity Model

Each event record carries:
- Stable numeric `id` (used as Kafka key and CloudEvents subject)
- `title`, `description`, `startdate`, `enddate`, `url`, `image_link`, `status`
- `location` — `city`, `location_name`, `address`, `zip_code`, `country_code`, `latitude`, `longitude`
- `organiser` — `id`, `name`
- `minimum_price` — `amount_in_cents`, `currency`
- Implied availability (presence of future events with active ticket links)

## Feasibility

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2/3 | Polled; events update on organizer action, not a push stream |
| Openness | 2/3 | Free API key; no redistribution restrictions for discovery use |
| Stability | 3/3 | Integer event IDs are immutable; API has been stable for years |
| Structure | 3/3 | Clean JSON with consistent field names |
| Identifiers | 3/3 | Numeric `id` is globally unique and stable across polls |
| Additive Value | 2/3 | Broad European coverage; good availability signal |
| **Total** | **15/18** | |

## Redistribution Notes

Billetto's terms permit display and integration of public event data for
discovery purposes. Commercial redistribution of ticket sales requires a
partnership agreement.
