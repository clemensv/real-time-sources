# Overpass Augmented Diffs

**Country/Region**: Global
**Publisher**: OpenStreetMap community (Overpass API by Martin Raifer / Wikidata)
**API Endpoint**: `https://overpass-api.de/api/augmented_diff`
**Documentation**: https://wiki.openstreetmap.org/wiki/Overpass_API/Augmented_Diffs
**Protocol**: HTTP (XML response)
**Auth**: None
**Data Format**: OSM XML (augmented diff format with old/new element states)
**Update Frequency**: ~1 minute (follows OSM minutely replication)
**License**: ODbL

## What It Provides

Overpass Augmented Diffs extend the standard OSM minutely diffs by adding geographic context and before/after state for every changed element. Where a plain osmChange file tells you *what* changed, an augmented diff tells you *what it looked like before and after*, including the full geometry and tags. This makes it possible to answer questions like "what buildings were added in Berlin in the last hour?" without maintaining a full OSM database.

The Overpass API also supports `[diff:]` and `[adiff:]` query modes, letting you run arbitrary spatial/tag queries against a time window and get back only the changes within that window.

## API Details

- **Augmented diff by sequence**: `GET /api/augmented_diff?id={sequence_number}` — retrieves a specific minutely diff
- **Augmented diff by time**: `GET /api/augmented_diff?since={ISO8601}` — retrieves changes since timestamp
- **Overpass diff query**: POST to `/api/interpreter` with `[adiff:"YYYY-MM-DDTHH:MM:SSZ","YYYY-MM-DDTHH:MM:SSZ"];` prefix
- **Spatial + temporal query**: Combine `[adiff:...]` with any Overpass QL filter (bbox, tag, type)
- **No auth required**: Public Overpass instances
- **Rate limit**: Overpass has per-IP slot limits; heavy use should target a dedicated instance
- **Multiple public instances**: `overpass-api.de`, `overpass.kumi.systems`, etc.

## Freshness Assessment

Augmented diffs follow OSM's minutely replication cycle — about 60 seconds behind the live database. The `[adiff:]` query mode can retrieve changes for any time window, so you can poll every minute for the latest changes matching your spatial/tag criteria. This is effectively real-time for most use cases.

Confirmed live: queried nodes changed in a 1-minute window in central London, got back a Nando's restaurant edit with full metadata.

## Entity Model

- **OSM Element**: `node`, `way`, `relation` with `id`, `version`, `changeset`, `user`, `uid`, `timestamp`
- **Tags**: Key-value pairs on elements
- **Geometry**: Lat/lon for nodes, node references for ways
- **Augmented state**: Each element appears with both old and new states in the diff

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | ~60 second lag, minutely cycle |
| Openness | 3 | No auth, public API |
| Stability | 2 | Community-run; public instances can be overloaded |
| Structure | 2 | XML format is verbose; no native JSON |
| Identifiers | 3 | OSM element IDs, changeset IDs, user IDs |
| Additive Value | 2 | Geographic + temporal slicing of OSM changes is uniquely powerful |
| **Total** | **15/18** | |

## Notes

- Confirmed live: augmented diff `id=1` returned valid XML from `overpass-api.de`.
- The `[adiff:]` query mode is the real gem — it turns Overpass into a temporal-spatial change query engine.
- XML-only output is a friction point; JSON conversion requires post-processing.
- For production use, consider running a private Overpass instance to avoid public rate limits.
- Complements OSM Minutely Diffs: the latter gives you raw osmChange files; augmented diffs give you queryable, context-enriched change data.
