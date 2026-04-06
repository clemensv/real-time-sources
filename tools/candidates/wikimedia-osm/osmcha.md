# OSMCha (OpenStreetMap Changeset Analyzer)

**Country/Region**: Global
**Publisher**: OSMCha / Mapbox (maintained by Wille Marcel)
**API Endpoint**: `https://osmcha.org/api/v1/changesets/`
**Documentation**: https://osmcha.org/api-docs/
**Protocol**: REST
**Auth**: OAuth2 (OpenStreetMap login) — required for API access
**Data Format**: JSON (GeoJSON for geometries)
**Update Frequency**: Near-real-time (changesets appear within minutes)
**License**: ISC (code); data derived from ODbL-licensed OSM data

## What It Provides

OSMCha is a changeset analysis and review tool for OpenStreetMap. It ingests the OSM replication stream and enriches changesets with quality analysis — flagging suspicious edits, mass deletions, imports, and potential vandalism. The API provides filtered access to changesets with their bounding boxes, tags, comments, review status, and quality flags.

API probe returned 401 Unauthorized, confirming that authentication via OSM OAuth is required for API access.

## API Details

- **Base URL**: `https://osmcha.org/api/v1/`
- **Endpoints**: `/changesets/` (list/search), `/changesets/{id}/` (detail), `/changesets/{id}/comment/` (post review comment)
- **Authentication**: OSM OAuth2 token required (login with OSM account, get token)
- **Filtering**: Extensive query parameters — `date__gte`, `date__lte`, `area_lt` (area threshold), `reasons` (suspicion reasons), `users`, `is_suspect`, `checked` (review status)
- **Response format**: JSON with changeset metadata, bbox geometry, editor used, source, flags, number of creates/modifies/deletes
- **Pagination**: Standard `page` / `page_size` parameters
- **Rate limits**: Not explicitly documented; reasonable use expected

## Freshness Assessment

OSMCha processes the OSM replication stream with a delay of a few minutes. Changesets are available for review shortly after they're closed on OSM. This is not a raw data feed but an enriched analysis layer on top of OSM changes.

## Entity Model

- **Changeset**: OSM changeset ID, with bbox, user, editor, comment, source, created date
- **Flags/Reasons**: Suspicious patterns detected (e.g., mass deletion, new mapper, large area)
- **Review**: `checked` status, `harmful`/`not harmful` verdict, reviewer, check_date
- **Features**: Individual modified elements within a changeset

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Minutes delay; dependent on replication processing |
| Openness | 1 | Requires OSM OAuth — not fully open/anonymous |
| Stability | 2 | Community-maintained project, has been running for years |
| Structure | 3 | Well-structured REST API with rich metadata |
| Identifiers | 3 | OSM changeset IDs, user IDs |
| Additive Value | 2 | Quality analysis layer on OSM changes |
| **Total** | **13/18** | |

## Notes

- OSMCha is more of a review/analysis tool than a raw data feed. Its value is in the quality flags and review workflow.
- The authentication requirement is the main barrier — you need an OSM account and OAuth token.
- The web UI at osmcha.org is the primary interface; the API is secondary.
- For raw OSM change data without auth, use the minutely diffs or Wikimedia EventStreams instead.
- Useful as a complementary source for detecting quality issues in OSM edits.
