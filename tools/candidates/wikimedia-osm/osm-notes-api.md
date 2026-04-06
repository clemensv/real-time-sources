# OpenStreetMap Notes API

**Country/Region**: Global
**Publisher**: OpenStreetMap Foundation
**API Endpoint**: `https://api.openstreetmap.org/api/0.6/notes`
**Documentation**: https://wiki.openstreetmap.org/wiki/API_v0.6#Map_Notes_API
**Protocol**: REST (XML or JSON)
**Auth**: None (read), OAuth2 (write)
**Data Format**: XML (default), JSON (with `.json` suffix), GeoJSON, GPX
**Update Frequency**: Real-time — notes appear within seconds of creation
**License**: ODbL (OpenStreetMap data license)

## What It Provides

OSM Notes are user-reported map issues — a crowdsourced bug tracker overlaid on the map itself. Anyone (including anonymous users) can drop a note on the map to report a missing road, incorrect name, demolished building, or any discrepancy between the map and reality. Each note has a location, a conversation thread (comments from multiple users), and a status (open/closed).

The Notes API provides a real-time feed of these reports: where are people finding the map to be wrong, right now? This is a fascinating signal — it reveals where the physical world is changing faster than mappers can keep up.

## API Details

- **Bounding box query**: `GET /api/0.6/notes.json?bbox={left},{bottom},{right},{top}&limit={n}&closed={days}`
- **Search**: `GET /api/0.6/notes/search.json?q={query}&limit={n}`
- **Single note**: `GET /api/0.6/notes/{id}.json`
- **RSS feed**: `GET /api/0.6/notes/feed?bbox={bbox}` — Atom/RSS feed of recent notes
- **Format selection**: Append `.json`, `.gpx`, `.rss` to endpoints
- **Pagination**: `limit` parameter (max 10000), `closed` parameter controls how many days of closed notes to include (0 = open only, -1 = all)
- **No auth for reads**: Completely open
- **Rate limit**: Standard OSM API rate limits apply; be respectful

## Freshness Assessment

Notes are available via the API within seconds of creation. The bounding box query returns notes ordered by last update time. The RSS feed provides a near-real-time push mechanism for monitoring specific geographic areas. Polling the search or bbox endpoint every few minutes gives effectively real-time coverage of new map issue reports.

## Entity Model

- **Note**: `id` (integer), `lat`/`lon` (WGS84), `status` (open/closed), `date_created`, `date_closed`
- **Comment**: `date`, `uid`, `user`, `action` (opened/commented/closed/reopened), `text`, `html`
- **GeoJSON Feature**: Each note is a GeoJSON Point with properties containing the conversation thread

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time availability, RSS feed for push |
| Openness | 3 | No auth for reads, open API |
| Stability | 3 | Core OSM API, stable for years |
| Structure | 3 | Clean JSON/GeoJSON, well-defined schema |
| Identifiers | 3 | Integer note IDs, user IDs, timestamps |
| Additive Value | 2 | Unique crowdsourced ground-truth signal about map accuracy |
| **Total** | **17/18** | |

## Notes

- Confirmed live: queried London bbox, received fresh notes including one created 2026-04-06 about a possible substation.
- JSON and GeoJSON output confirmed working.
- The Notes API is a sleeper — it's essentially a global, real-time crowdsourced survey of where the physical world disagrees with the digital map.
- Volume is moderate (hundreds to low thousands of new notes per day globally), making it very manageable for continuous monitoring.
- Combine with OSM Minutely Diffs to see notes that triggered map edits.
