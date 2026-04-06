# Transit Real-Time Data — Candidate Sources

Candidates for real-time public transit data bridges, focusing on SIRI-native systems and high-value individual feeds that go beyond the generic GTFS-RT bridge.

## Already Implemented

| Source | Protocol | Directory |
|--------|----------|-----------|
| Generic GTFS-RT Bridge | GTFS-RT (Protobuf) | `gtfs/` |
| NextBus | XML (proprietary) | `nextbus/` |

## Candidates

### Tier 1 — SIRI-Native (High Additive Value)

These sources use the SIRI protocol natively. They can't be covered by the existing GTFS-RT bridge and represent genuinely new protocol territory.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 1 | [UK BODS (SIRI-VM)](uk-bods-siri.md) | 🇬🇧 UK | SIRI-VM 2.0 | **17/18** | `uk-bods-siri.md` |
| 2 | [Trafiklab SIRI Regional](trafiklab-siri.md) | 🇸🇪 Sweden | SIRI 2.0 (ET/VM/SX) | **18/18** | `trafiklab-siri.md` |
| 3 | [SNCF / France PAN](sncf-france.md) | 🇫🇷 France | SIRI-Lite + GTFS-RT | **16/18** | `sncf-france.md` |

**Recommendation**: Build a generic SIRI bridge (akin to the GTFS-RT bridge) that handles SIRI-ET, SIRI-VM, and SIRI-SX. Trafiklab (CC0, full SIRI 2.0) is the ideal development target. UK BODS is the highest-volume production deployment. France's SIRI-Lite variant offers a REST-friendly entry point.

### Tier 2 — Push / Event-Driven (Architecturally Interesting)

These sources use push-based protocols that align naturally with event-driven bridge design.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 4 | [Network Rail DARWIN](network-rail-darwin.md) | 🇬🇧 UK | STOMP push + SOAP | **16/18** | `network-rail-darwin.md` |
| 5 | [MBTA V3 API](mbta-v3-api.md) | 🇺🇸 USA (Boston) | REST + SSE streaming | **17/18** | `mbta-v3-api.md` |

**Recommendation**: Darwin's STOMP push and MBTA's SSE streaming are both genuinely push-based — they emit events rather than requiring polling. These are natural fits for CloudEvents bridges.

### Tier 3 — REST / Proprietary (Unique Sources)

These are high-value sources with proprietary REST APIs that provide data not available elsewhere.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 6 | [TfL Unified API](tfl-unified-api.md) | 🇬🇧 UK (London) | REST/JSON | **17/18** | `tfl-unified-api.md` |
| 7 | [DB Timetables (IRIS)](db-timetables.md) | 🇩🇪 Germany | REST/XML | **15/18** | `db-timetables.md` |
| 8 | [NS Dutch Railways](ns-dutch-rail.md) | 🇳🇱 Netherlands | REST/JSON | **14/18** | `ns-dutch-rail.md` |
| 9 | [MTA NYC](mta-nyc.md) | 🇺🇸 USA (NYC) | GTFS-RT + SIRI | **14/18** | `mta-nyc.md` |

**Recommendation**: TfL is the easiest to start with — works without authentication, returns clean JSON, and covers a massive multimodal network. DB Timetables is the only source for German rail real-time. MTA's bus SIRI feeds are notable as a US-based SIRI deployment.

## Priority Order for Implementation

1. **Generic SIRI Bridge** — using Trafiklab as dev target, then deploy against UK BODS, France PAN, MTA Bus
2. **DARWIN STOMP Bridge** — push-based GB rail (pairs with BODS for full UK coverage)
3. **TfL Unified API Bridge** — low barrier, high data value, clean JSON
4. **MBTA SSE Bridge** — demonstrates SSE-to-CloudEvents pattern
5. **DB Timetables Bridge** — German rail, unique XML format
6. **NS API Bridge** — Dutch rail (lower priority due to licensing)

## Candidates Not Pursued (Yet)

| Candidate | Country | Reason |
|-----------|---------|--------|
| Japan train APIs (ODPT) | 🇯🇵 Japan | Tokyo Open Data Challenge had APIs but current public access is unclear; registration appears closed or Japan-only |
| Indian Railways | 🇮🇳 India | No verified open real-time API found; third-party scrapers exist but no official open feed |
| Oxyfi Train Positions | 🇸🇪 Sweden | WebSocket + NMEA GPS — interesting but very niche (subset of Swedish trains only) |
| NDOV Loket (NL) | 🇳🇱 Netherlands | Raw KV6/KV17 feeds — complex Dutch-specific protocols, lower priority |
| Swiss Transport API | 🇨🇭 Switzerland | Unofficial wrapper around search.ch; limited real-time; official data on opendata.swiss as GTFS |

## See Also — Social / News / Wiki Feeds

These are not transit but are relevant real-time open data sources in the social/news domain. Most are already covered or trivially covered by existing bridges.

### Already Covered
- **Bluesky AT Protocol Firehose** (`bluesky/`) — full firehose of the Bluesky social network via AT Protocol Jetstream
- **RSS/Atom Generic** (`rss/`) — covers any RSS/Atom feed including news sites, blogs, government announcements

### Worth Noting

| Source | Protocol | Notes |
|--------|----------|-------|
| **Hacker News Firebase API** | REST + Firebase SSE | `https://hacker-news.firebaseio.com/v0/` — live story/comment IDs. Supports SSE streaming via Firebase's real-time database. Endpoints: `/topstories`, `/newstories`, `/beststories`, `/askstories`, `/showstories`, `/jobstories` (each returns array of item IDs). Individual items via `/item/{id}.json`. No auth required. Could bridge to CloudEvents for "new story" / "new comment" events. |
| **Mastodon / ActivityPub Streaming** | SSE (Server-Sent Events) | Any Mastodon instance exposes `GET /api/v1/streaming/public` for the local/federated timeline via SSE. Streams: `public`, `public:local`, `hashtag:{tag}`, `user` (authenticated). Events: `update` (new post), `delete`, `notification`. JSON payloads. No auth for public streams. Every instance is independent — connect to any instance's streaming endpoint. Relay servers aggregate multiple instances. |
| **Wikipedia Recent Changes** | SSE (EventStreams) | `https://stream.wikimedia.org/v2/stream/recentchange` — SSE stream of all edits across all Wikimedia projects. Already noted in `wikimedia-osm` candidates. |

### Assessment
The RSS bridge already covers most news sources (including HN via its RSS feed). Mastodon streaming is interesting as an ActivityPub/SSE source but overlaps with Bluesky's social feed niche. The HN Firebase API's SSE capability makes it a clean candidate for a small, focused bridge demonstrating Firebase SSE-to-CloudEvents conversion.
