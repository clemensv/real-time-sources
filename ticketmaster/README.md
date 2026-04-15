# Ticketmaster Discovery API Bridge

This bridge polls the [Ticketmaster Discovery API v2](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
for upcoming public events and emits them as CloudEvents to an Apache Kafka topic.

## Data Model

The bridge emits four event families:

| Family | Type | Description |
|---|---|---|
| Event telemetry | `Ticketmaster.Events.Event` | Live event data: concerts, sports, theater, arts, and other public events |
| Venue reference | `Ticketmaster.Reference.Venue` | Venue location, address, timezone, and coordinates |
| Attraction reference | `Ticketmaster.Reference.Attraction` | Performer, artist, sports team, or production metadata |
| Classification reference | `Ticketmaster.Reference.Classification` | Classification segment hierarchy (Music, Sports, Arts & Theatre, etc.) |

Reference data (venues, attractions, classifications) is emitted at bridge startup
and refreshed every hour so downstream consumers can maintain temporally consistent
views of the entities that event telemetry references.

## Upstream Source

- **API:** [Ticketmaster Discovery API v2](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
- **Coverage:** North America, Europe, Australia, and other Ticketmaster markets
- **Auth:** Free API key required — register at [developer.ticketmaster.com](https://developer.ticketmaster.com)
- **Rate limits:** 5 000 API calls per day, 5 requests per second on the free tier

## Compliance Responsibility

The bridge does not transfer Ticketmaster compliance obligations away from the
operator. The user of this bridge is responsible for complying with
Ticketmaster's Terms of Service, branding requirements, rate limits, and any
rules governing how Ticketmaster data is represented or redistributed in their
application and downstream systems.

## Kafka Topic

All event types (telemetry and reference) are written to a single configurable Kafka topic.

| Message group | Kafka key |
|---|---|
| `Ticketmaster.Events` | `{event_id}` |
| `Ticketmaster.Reference` | `{entity_id}` |

See [EVENTS.md](EVENTS.md) for full CloudEvents and schema documentation.

## Quick Start

```bash
export TICKETMASTER_API_KEY=<your-api-key>
export CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=ticketmaster"
export KAFKA_ENABLE_TLS=false
python -m ticketmaster feed
```

See [CONTAINER.md](CONTAINER.md) for Docker and deployment instructions.

## Configuration

| Environment variable | Description | Default |
|---|---|---|
| `TICKETMASTER_API_KEY` | **Required.** Ticketmaster Discovery API key | — |
| `CONNECTION_STRING` | Kafka / Event Hubs / Fabric connection string | — |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers (alternative to connection string) | — |
| `KAFKA_TOPIC` | Kafka topic name | — |
| `COUNTRY_CODES` | Comma-separated ISO 3166-1 alpha-2 country codes to poll | `AU,AT,BE,CA,CZ,DK,FI,FR,DE,GR,HU,IE,IT,MX,NL,NZ,NO,PL,PT,ES,SE,CH,GB,US` |
| `TICKETMASTER_CITY` | Optional Ticketmaster `city` filter | — |
| `TICKETMASTER_VENUE_ID` | Optional Ticketmaster `venueId` filter | — |
| `TICKETMASTER_ATTRACTION_ID` | Optional Ticketmaster `attractionId` filter | — |
| `TICKETMASTER_SEGMENT_ID` | Optional Ticketmaster `segmentId` filter | — |
| `TICKETMASTER_GENRE_ID` | Optional Ticketmaster `genreId` filter | — |
| `TICKETMASTER_SUB_GENRE_ID` | Optional Ticketmaster `subGenreId` filter | — |
| `TICKETMASTER_MARKET_ID` | Optional Ticketmaster `marketId` filter | — |
| `TICKETMASTER_POSTAL_CODE` | Optional Ticketmaster `postalCode` filter | — |
| `TICKETMASTER_LOCALE` | Discovery API locale for event and reference requests | `*` |
| `TICKETMASTER_SORT` | Discovery API event sort order | `date,asc` |
| `TICKETMASTER_PAGE_SIZE` | Discovery API page size per request, up to 200 | `200` |
| `TICKETMASTER_START_DATETIME` | Optional absolute UTC lower bound for event search | — |
| `TICKETMASTER_END_DATETIME` | Optional absolute UTC upper bound for event search | — |
| `TICKETMASTER_LOOKAHEAD_DAYS` | Relative search window when explicit datetimes are not set | `90` |
| `POLL_INTERVAL` | Seconds between event polls | `300` |
| `REFERENCE_REFRESH` | Seconds between reference-data refreshes | `3600` |
| `KAFKA_ENABLE_TLS` | Enable TLS for Kafka connections | `true` |
| `LOG_LEVEL` | Python logging level | `INFO` |

## Supported Event Filters

The bridge now exposes the upstream Discovery API event filters below through
both CLI arguments and environment variables:

| API query param | CLI argument | Environment variable |
|---|---|---|
| `countryCode` | `--country-codes` | `COUNTRY_CODES` |
| `city` | `--city` | `TICKETMASTER_CITY` |
| `venueId` | `--venue-id` | `TICKETMASTER_VENUE_ID` |
| `attractionId` | `--attraction-id` | `TICKETMASTER_ATTRACTION_ID` |
| `segmentId` | `--segment-id` | `TICKETMASTER_SEGMENT_ID` |
| `genreId` | `--genre-id` | `TICKETMASTER_GENRE_ID` |
| `subGenreId` | `--sub-genre-id` | `TICKETMASTER_SUB_GENRE_ID` |
| `marketId` | `--market-id` | `TICKETMASTER_MARKET_ID` |
| `postalCode` | `--postal-code` | `TICKETMASTER_POSTAL_CODE` |
| `locale` | `--locale` | `TICKETMASTER_LOCALE` |
| `sort` | `--sort` | `TICKETMASTER_SORT` |
| `size` | `--page-size` | `TICKETMASTER_PAGE_SIZE` |
| `startDateTime` | `--start-datetime` | `TICKETMASTER_START_DATETIME` |
| `endDateTime` | `--end-datetime` | `TICKETMASTER_END_DATETIME` |

If you do not set `--start-datetime` and `--end-datetime`, the bridge uses a
rolling window from now through `TICKETMASTER_LOOKAHEAD_DAYS`.

Example:

```bash
export TICKETMASTER_CITY=Berlin
export TICKETMASTER_SEGMENT_ID=KZFzniwnSyZfZ7v7nJ
export TICKETMASTER_LOOKAHEAD_DAYS=30
python -m ticketmaster feed
```

## Links

- [Ticketmaster Developer Portal](https://developer.ticketmaster.com)
- [Discovery API v2 Documentation](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
- [EVENTS.md](EVENTS.md) — CloudEvents and schema documentation
- [CONTAINER.md](CONTAINER.md) — Docker deployment documentation
- [azure-template.json](azure-template.json) — Azure Container Instance deployment template
