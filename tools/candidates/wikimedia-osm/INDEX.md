# Wikimedia / OSM Candidates

Real-time data sources from Wikimedia projects and OpenStreetMap.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [Wikimedia EventStreams](wikimedia-eventstreams.md) | SSE | None | Sub-second | 17/18 |
| [OSM Minutely Diffs](osm-minutely-diffs.md) | HTTP file | None | 60 seconds | 17/18 |
| [Wikidata Recent Changes](wikidata-recent-changes.md) | REST + SSE | None | Real-time | 17/18 |
| [OSM Notes API](osm-notes-api.md) | REST | None | Real-time | 17/18 |
| [Wikipedia Pageviews API](wikipedia-pageviews-api.md) | REST | None | Daily | 16/18 |
| [Overpass Augmented Diffs](overpass-augmented-diffs.md) | HTTP | None | ~60 seconds | 15/18 |
| [Mapillary](mapillary.md) | REST (Graph API) | OAuth2 (free) | Minutes | 15/18 |
| [OSMCha](osmcha.md) | REST | OAuth2 | Minutes | 13/18 |
| [OpenAddresses](openaddresses.md) | REST | None | Days-weeks | 13/18 |

## Summary

The Wikimedia EventStreams SSE endpoint is the standout — zero-auth, sub-second latency, well-structured JSON with schemas. OSM minutely diffs are the canonical map update feed. Wikidata provides structured knowledge graph changes under CC0.

The OSM Notes API is a sleeper hit — real-time crowdsourced reports of where the map disagrees with reality, zero-auth, clean JSON/GeoJSON. Overpass Augmented Diffs turn minutely replication into a queryable temporal-spatial change engine. Wikipedia Pageviews adds an attention signal (what's the world reading about right now?) that correlates with EventStreams edit bursts.

Mapillary provides the visual layer — street-level imagery contributions that drive OSM edits. OpenAddresses is a batch-updated global address dataset, less fresh but uniquely normalized. OSMCha remains the quality monitoring layer.
