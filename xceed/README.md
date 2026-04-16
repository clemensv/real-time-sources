# Xceed Nightlife Events Bridge

This bridge polls the [Xceed Open Event API](https://docs.xceed.me/) and forwards
European nightlife and live-entertainment event data as CloudEvents to Apache Kafka.

## Overview

[Xceed](https://xceed.me) is a European nightlife and ticketing platform covering clubs,
bars, parties, and festivals. Their public APIs expose event schedules from
`events.xceed.me` and per-event offer inventories from `offer.xceed.me`, including
ticket, guest-list, and bottle-service offers with sales-state signals such as
`isSoldOut` and `isSalesClosed`.

## Event Types

Two event types are emitted:

| Type | Description |
|------|-------------|
| `xceed.Event` | Event reference data: schedule, venue, and metadata. Emitted at startup and refreshed periodically. |
| `xceed.EventAdmission` | Offer telemetry: sales state, normalized price, remaining quantity, and `admission_type` for ticket, guest-list, and bottle-service records. Polled every cycle. |

See [EVENTS.md](EVENTS.md) for the full event catalog.

## Data Model

- **Events** are the scheduled nightlife or entertainment occurrences, each with a stable
  UUID (`event_id`), schedule timestamps, venue details, cover image, and an optional
  external sales link.
- **Event Admissions** represent normalized Xceed public offers and preserve the upstream
  offer kind in `admission_type` (for example `ticket`, `guestlist`, or `bottleservice`),
  alongside `is_sold_out`, `is_sales_closed`, `price`, `currency`, and `remaining`.

## Kafka Keys

| Message group | Kafka key template | Example |
|---------------|--------------------|---------|
| `xceed` | `{event_id}` | `297ad280-4fd4-4b9a-870e-b4de6b2588a0` |
| `xceed.admissions` | `{event_id}/{admission_id}` | `297ad280-.../adm-001` |

## Running

```bash
pip install .

# Emit events and admission updates
python -m xceed feed --connection-string "BootstrapServer=localhost:9092;EntityPath=xceed"
```

The bridge scans the newest slice of the public Xceed catalog so it emits current and
upcoming event offers instead of getting stuck in the historical archive.

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Public Filter Surface

Unlike Ticketmaster and Billetto, the public Xceed `/events` endpoint does not
present a meaningful set of semantic event filters in live probing. The
documented and observed upstream query controls are pagination-oriented:

| Upstream query param | Bridge surface | Meaning |
|---|---|---|
| `limit` | `--event-page-size` / `EVENT_PAGE_SIZE` | Number of events requested per `/events` page |
| `offset` | internal | Pagination cursor the bridge advances automatically |

Live probes against `city`, `country`, and `slug` query params returned the same
unfiltered result set, so the bridge does **not** expose those as operator
filters.

## Source Files

| File | Description |
|------|-------------|
| [xreg/xceed.xreg.json](xreg/xceed.xreg.json) | xRegistry manifest |
| [xceed/xceed.py](xceed/xceed.py) | Runtime bridge |
| [xceed_producer/](xceed_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |

## Upstream Source

- API base: `https://events.xceed.me/v1`
- Offer base: `https://offer.xceed.me/v1`
- Documentation: [https://docs.xceed.me/](https://docs.xceed.me/)
- Authentication: none required for the Open Event API
