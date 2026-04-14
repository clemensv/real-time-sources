# Xceed Nightlife Events Bridge

This bridge polls the [Xceed Open Event API](https://docs.xceed.me/) and forwards
European nightlife and live-entertainment event data as CloudEvents to Apache Kafka.

## Overview

[Xceed](https://xceed.me) is a European nightlife and ticketing platform covering clubs,
bars, parties, and festivals. Their public Open Event API returns scheduled event listings
with embedded venue information and optional external sales links. The partner ticketing
surface that exposes admission-tier availability is not part of the unauthenticated public API,
so this source is scoped to public event reference data only.

## Event Types

One event type is emitted:

| Type | Description |
|------|-------------|
| `xceed.Event` | Event reference data: schedule, venue, and metadata. Emitted at startup and refreshed periodically. |

See [EVENTS.md](EVENTS.md) for the full event catalog.

## Data Model

- **Events** are the scheduled nightlife or entertainment occurrences, each with a stable
  UUID (`event_id`), schedule timestamps, venue details, cover image, and an optional
  external sales link.

## Kafka Keys

| Message group | Kafka key template | Example |
|---------------|--------------------|---------|
| `xceed` | `{event_id}` | `297ad280-4fd4-4b9a-870e-b4de6b2588a0` |

## Running

```bash
pip install .

# Emit event reference updates
python -m xceed feed --connection-string "BootstrapServer=localhost:9092;EntityPath=xceed"
```

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

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
- Documentation: [https://docs.xceed.me/](https://docs.xceed.me/)
- Authentication: none required for the Open Event API
