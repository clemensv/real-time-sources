# Ticketmaster Discovery API bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

## Upstream source

This bridge targets the public [Ticketmaster Discovery API v2](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/).
It polls for upcoming public events and emits CloudEvents for:

- **Event telemetry** — concerts, sports events, theater, arts, and other live events (`Ticketmaster.Events.Event`)
- **Venue reference data** — location, address, timezone, and coordinates (`Ticketmaster.Reference.Venue`)
- **Attraction reference data** — performer, artist, team, or production metadata (`Ticketmaster.Reference.Attraction`)
- **Classification reference data** — the Ticketmaster segment taxonomy (Music, Sports, etc.) (`Ticketmaster.Reference.Classification`)

Reference data is emitted at bridge startup and refreshed every hour.  All events
are emitted as structured CloudEvents documented in [EVENTS.md](EVENTS.md).

## Prerequisites

Register for a free API key at [developer.ticketmaster.com](https://developer.ticketmaster.com).
The free tier allows 5 000 API calls per day and 5 requests per second.

## Compliance responsibility

Using this container does not make Ticketmaster compliance automatic. The user
of the bridge is responsible for complying with Ticketmaster's Terms of
Service, branding guide, rate limits, and any requirements on how Ticketmaster
data is presented, attributed, or redistributed.

## Environment variables

| Variable | Required | Description | Default |
|---|---|---|---|
| `TICKETMASTER_API_KEY` | **Yes** | Ticketmaster Discovery API key | — |
| `CONNECTION_STRING` | **Yes** | Kafka / Event Hubs / Fabric connection string | — |
| `COUNTRY_CODES` | No | Comma-separated ISO 3166-1 alpha-2 country codes | `AU,AT,BE,CA,CZ,DK,FI,FR,DE,GR,HU,IE,IT,MX,NL,NZ,NO,PL,PT,ES,SE,CH,GB,US` |
| `TICKETMASTER_CITY` | No | Optional Ticketmaster `city` filter | — |
| `TICKETMASTER_VENUE_ID` | No | Optional Ticketmaster `venueId` filter | — |
| `TICKETMASTER_ATTRACTION_ID` | No | Optional Ticketmaster `attractionId` filter | — |
| `TICKETMASTER_SEGMENT_ID` | No | Optional Ticketmaster `segmentId` filter | — |
| `TICKETMASTER_GENRE_ID` | No | Optional Ticketmaster `genreId` filter | — |
| `TICKETMASTER_SUB_GENRE_ID` | No | Optional Ticketmaster `subGenreId` filter | — |
| `TICKETMASTER_MARKET_ID` | No | Optional Ticketmaster `marketId` filter | — |
| `TICKETMASTER_POSTAL_CODE` | No | Optional Ticketmaster `postalCode` filter | — |
| `TICKETMASTER_LOCALE` | No | Discovery API locale for event and reference requests | `*` |
| `TICKETMASTER_SORT` | No | Discovery API event sort order | `date,asc` |
| `TICKETMASTER_PAGE_SIZE` | No | Discovery API page size per request, up to 200 | `200` |
| `TICKETMASTER_START_DATETIME` | No | Optional absolute UTC startDateTime filter | — |
| `TICKETMASTER_END_DATETIME` | No | Optional absolute UTC endDateTime filter | — |
| `TICKETMASTER_LOOKAHEAD_DAYS` | No | Relative search window when explicit datetimes are not set | `90` |
| `POLL_INTERVAL` | No | Seconds between event polls | `300` |
| `REFERENCE_REFRESH` | No | Seconds between reference-data refreshes | `3600` |
| `STATE_FILE` | No | Path to JSON file for persisting dedupe state across restarts | `~/.ticketmaster_state.json` |
| `KAFKA_ENABLE_TLS` | No | Set to `false` for plain-text Kafka (non-Event Hubs) | `true` |
| `LOG_LEVEL` | No | Python logging level | `INFO` |

## Running with Docker (plain Kafka)

```bash
docker pull ghcr.io/clemensv/real-time-sources-ticketmaster:latest

docker run --rm \
  -e TICKETMASTER_API_KEY=<your-api-key> \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=ticketmaster" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-ticketmaster:latest
```

## Running with Azure Event Hubs

Create an Event Hubs namespace and a hub named `ticketmaster`, then run:

```bash
docker run --rm \
  -e TICKETMASTER_API_KEY=<your-api-key> \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<key>;EntityPath=ticketmaster" \
  ghcr.io/clemensv/real-time-sources-ticketmaster:latest
```

## Running with Microsoft Fabric Event Streams

```bash
docker run --rm \
  -e TICKETMASTER_API_KEY=<your-api-key> \
  -e CONNECTION_STRING="<Fabric-Event-Stream-connection-string>" \
  ghcr.io/clemensv/real-time-sources-ticketmaster:latest
```

## Reducing scope to specific markets

To focus on one city and segment instead of the full multi-country default:

```bash
docker run --rm \
  -e TICKETMASTER_API_KEY=<your-api-key> \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=ticketmaster" \
  -e COUNTRY_CODES=DE \
  -e TICKETMASTER_CITY=Berlin \
  -e TICKETMASTER_SEGMENT_ID=KZFzniwnSyZfZ7v7nJ \
  -e TICKETMASTER_LOOKAHEAD_DAYS=30 \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-ticketmaster:latest
```

## Rate limits

The free tier allows 5 000 calls per day and 5 requests per second.  The bridge
sleeps between API calls to stay within the rate limit.  Fetching venues and
attractions across many country codes can consume a large fraction of the daily
quota.  Set `COUNTRY_CODES` to only the markets you need, or set
`REFERENCE_REFRESH` to a longer interval (e.g. `86400` for once per day) to
reduce API call volume.

## Azure Container Instance (ACI) deployment

An ARM template is included as [azure-template.json](azure-template.json). It
exposes the runtime filters as optional template parameters, with descriptions
that tell the operator what each filter does and when to leave it blank.

Example deployment:

```bash
az deployment group create \
  --resource-group <resource-group> \
  --template-file azure-template.json \
  --parameters \
      connectionString="<event-hubs-or-kafka-connection-string>" \
      ticketmasterApiKey="<ticketmaster-api-key>" \
      countryCodes="DE" \
      city="Berlin" \
      segmentId="KZFzniwnSyZfZ7v7nJ" \
      lookaheadDays="30"
```
