# Wikimedia / OSM Candidates

Real-time data sources from Wikimedia projects and OpenStreetMap.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [Wikimedia EventStreams](wikimedia-eventstreams.md) | SSE | None | Sub-second | 17/18 |
| [OSM Minutely Diffs](osm-minutely-diffs.md) | HTTP file | None | 60 seconds | 17/18 |
| [Wikidata Recent Changes](wikidata-recent-changes.md) | REST + SSE | None | Real-time | 17/18 |
| [OSMCha](osmcha.md) | REST | OAuth2 | Minutes | 13/18 |

## Summary

The Wikimedia EventStreams SSE endpoint is the standout — zero-auth, sub-second latency, well-structured JSON with schemas. OSM minutely diffs are the canonical map update feed. Wikidata provides structured knowledge graph changes under CC0. OSMCha adds value as a quality layer but requires authentication.
