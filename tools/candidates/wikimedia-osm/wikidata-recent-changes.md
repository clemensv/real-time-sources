# Wikidata Recent Changes

**Country/Region**: Global
**Publisher**: Wikimedia Foundation / Wikidata
**API Endpoint**: `https://www.wikidata.org/w/api.php?action=query&list=recentchanges`
**Documentation**: https://www.wikidata.org/w/api.php?action=help&modules=query%2Brecentchanges
**Protocol**: REST (MediaWiki Action API) + SSE (via Wikimedia EventStreams)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (hundreds of edits/minute)
**License**: CC0 1.0 (Public Domain)

## What It Provides

Wikidata is the free, structured knowledge base that feeds Wikipedia infoboxes and thousands of other applications. Its Recent Changes API provides a paginated feed of all modifications to Wikidata items — property edits, label/description changes, sitelink updates, statement additions, and more. Each change record includes the item ID (Q-number), revision IDs, timestamp, user, comment, and change type.

Live probe confirmed active data: 5 edits returned with timestamps at `2026-04-06T10:25:28Z`, touching items like Q20376139, Q29555900, Q25144105 — all within the same second. This is a high-velocity stream.

## API Details

- **MediaWiki API**: `https://www.wikidata.org/w/api.php?action=query&list=recentchanges&rcnamespace=0&rclimit=500&format=json`
- **Key parameters**: `rcnamespace` (0 for items), `rclimit` (up to 500), `rcstart`/`rcend` (timestamps), `rcprop` (fields to return: `user|comment|timestamp|title|ids|sizes|flags|tags`), `rccontinue` (pagination)
- **SSE alternative**: `https://stream.wikimedia.org/v2/stream/recentchange` filtered by `wiki=wikidatawiki`
- **SPARQL endpoint**: `https://query.wikidata.org/sparql` for structured queries over the knowledge graph
- **Entity API**: `https://www.wikidata.org/wiki/Special:EntityData/Q42.json` for full entity data
- **Rate limits**: MediaWiki API has soft rate limits (~200 req/s for anonymous); SSE has none

## Freshness Assessment

Via the SSE stream, changes appear in real-time (sub-second). Via the REST API, you can poll as frequently as needed with `rcstart` parameter. The knowledge base sees ~500-1000 edits per minute during peak hours, with significant bot activity. Wikidata is one of the most actively edited Wikimedia projects.

## Entity Model

- **Item**: Q-numbered entity (e.g., Q42 = Douglas Adams), with labels, descriptions, aliases, statements, sitelinks
- **Property**: P-numbered predicate (e.g., P31 = instance of)
- **Statement**: Subject (item) → Predicate (property) → Value, with qualifiers and references
- **Revision**: Integer revision ID, monotonically increasing per page
- **User**: Username or IP address

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time via SSE; near-real-time via polling |
| Openness | 3 | CC0 license, no auth required |
| Stability | 3 | Core Wikimedia infrastructure |
| Structure | 3 | Highly structured knowledge graph with formal ontology |
| Identifiers | 3 | Q-numbers and P-numbers are globally unique, stable, widely adopted |
| Additive Value | 2 | Complements EventStreams; structured knowledge changes |
| **Total** | **17/18** | |

## Notes

- The SSE route (Wikimedia EventStreams filtered to `wikidatawiki`) is preferred over polling the MediaWiki API for real-time use.
- Wikidata edits include both human and bot changes — bots often make bulk imports or cross-wiki sync updates.
- The `rctype` parameter can filter to specific change types: `edit`, `new`, `log`, `categorize`, `external`.
- For structured diffs of what changed in an entity, use the `wbgetentities` API with revision parameters or the `revision-create` SSE stream.
- CC0 license makes this one of the most permissively licensed knowledge bases.
