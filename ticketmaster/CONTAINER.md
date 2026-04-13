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

## Environment variables

| Variable | Required | Description | Default |
|---|---|---|---|
| `TICKETMASTER_API_KEY` | **Yes** | Ticketmaster Discovery API key | — |
| `CONNECTION_STRING` | **Yes** | Kafka / Event Hubs / Fabric connection string | — |
| `COUNTRY_CODES` | No | Comma-separated ISO 3166-1 alpha-2 country codes | `AU,AT,BE,CA,CZ,DK,FI,FR,DE,GR,HU,IE,IT,MX,NL,NZ,NO,PL,PT,ES,SE,CH,GB,US` |
| `POLL_INTERVAL` | No | Seconds between event polls | `300` |
| `REFERENCE_REFRESH` | No | Seconds between reference-data refreshes | `3600` |
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

To focus on a single market such as the United Kingdom:

```bash
docker run --rm \
  -e TICKETMASTER_API_KEY=<your-api-key> \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=ticketmaster" \
  -e COUNTRY_CODES=GB \
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

An Azure Container Instance template is not included in this release.  Use the
`docker run` examples above and adapt them to your deployment toolchain.
