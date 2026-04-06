# Wikimedia EventStreams

**Country/Region**: Global
**Publisher**: Wikimedia Foundation
**API Endpoint**: `https://stream.wikimedia.org/v2/stream/recentchange`
**Documentation**: https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams
**Protocol**: SSE (Server-Sent Events)
**Auth**: None
**Data Format**: JSON (one event per SSE `data:` line)
**Update Frequency**: Real-time (continuous stream, hundreds of events/second)
**License**: CC BY-SA 4.0 (content); data stream itself is public

## What It Provides

Wikimedia EventStreams is a real-time SSE feed of all changes across Wikimedia projects — every edit to Wikipedia, Wikidata, Wikimedia Commons, and sister projects is broadcast as a structured JSON event. Streams include `recentchange`, `revision-create`, `page-create`, `page-delete`, `page-move`, and more. Each event contains the wiki identifier, page title, namespace, user, timestamp, revision IDs, comment, bot flag, and change size.

The `recentchange` stream alone produces hundreds of events per second globally, covering edits, new pages, log actions, and categorization changes across 800+ wiki projects.

## API Details

- **Base URL**: `https://stream.wikimedia.org/v2/stream/{stream_name}`
- **Available streams**: `recentchange`, `revision-create`, `revision-score`, `page-create`, `page-delete`, `page-links-change`, `page-move`, `page-properties-change`, `page-undelete`, `mediawiki.recentchange`
- **Filtering**: Append `?since=TIMESTAMP` (ISO 8601) to resume from a point; the server replays missed events from a buffer (~7 days)
- **Multi-stream**: Comma-separate stream names in the URL path
- **No rate limiting**: Public, unauthenticated, no API key required
- **EventSource protocol**: Standard SSE — connect with `EventSource` in JS, `sseclient` in Python, or `curl`
- **Event schema**: Each event has a `$schema` URI pointing to its JSON Schema definition
- **Sample event fields** (recentchange): `id`, `type` (edit/new/log/categorize), `namespace`, `title`, `comment`, `timestamp`, `user`, `bot`, `minor`, `patrolled`, `length` (old/new), `revision` (old/new), `server_name`, `wiki`, `meta` (uri, request_id, id, dt, domain, stream, topic, partition, offset)

## Freshness Assessment

This is one of the freshest open data streams on the planet. Events appear within 1-2 seconds of the edit being saved. The SSE connection is persistent and push-based — no polling required. The `?since=` parameter allows catch-up replay, making it resilient to brief disconnects. Kafka-backed with at-least-once delivery semantics.

## Entity Model

- **Wiki Project**: Identified by `wiki` field (e.g., `enwiki`, `dewiki`, `wikidatawiki`) and `server_name` (e.g., `en.wikipedia.org`)
- **Page**: `title` + `namespace` within a wiki
- **Revision**: `revision.new` / `revision.old` (integer IDs)
- **User**: `user` (string, may be username or IP for anonymous)
- **Event**: `meta.id` (UUID), `meta.dt` (ISO timestamp), `meta.offset` (Kafka offset)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Sub-second latency, continuous SSE push |
| Openness | 3 | No auth, no rate limit, public SSE endpoint |
| Stability | 3 | Production Wikimedia infrastructure, Kafka-backed, running since 2018 |
| Structure | 3 | Well-defined JSON schemas, consistent event envelope |
| Identifiers | 3 | Revision IDs, page IDs, wiki IDs, UUID event IDs |
| Additive Value | 2 | Massive global knowledge graph changes; unique dataset |
| **Total** | **17/18** | |

## Notes

- This is perhaps the most accessible real-time open data stream in existence. Zero barriers to entry.
- The underlying transport is Apache Kafka; SSE is the public-facing protocol. Wikimedia also exposes Kafka topics directly for internal consumers.
- The `revision-score` stream includes ORES (machine learning) quality scores for edits — useful for vandalism detection.
- Event replay via `?since=` is limited to ~7 days of buffer.
- CloudEvents-compatible event envelope with `$schema`, `meta.id`, `meta.dt`.
