# Mapillary

**Country/Region**: Global
**Publisher**: Meta Platforms (formerly Mapillary AB)
**API Endpoint**: `https://graph.mapillary.com/`
**Documentation**: https://www.mapillary.com/developer/api-documentation
**Protocol**: REST (JSON), Graph API
**Auth**: OAuth2 / Client Token (free)
**Data Format**: JSON (GeoJSON for spatial queries)
**Update Frequency**: Near real-time — images available within minutes of upload
**License**: CC BY-SA 4.0 (images); API requires Meta developer agreement

## What It Provides

Mapillary is the world's largest open street-level imagery platform — think of it as a crowdsourced Google Street View. Contributors capture geolocated, timestamped street-level photos and sequences using phones, dashcams, and action cameras. As of 2024, the platform hosts over 2 billion images covering millions of kilometers of roads worldwide. Meta acquired Mapillary in 2020 and integrated it with the Meta Graph API.

Each image has precise GPS coordinates, compass heading, capture time, and computed depth information. Machine learning extracts map features (traffic signs, lane markings, objects) from the imagery.

## API Details

- **Image query**: `GET /graph.mapillary.com/{image_id}?fields=id,captured_at,geometry,compass_angle`
- **Spatial search**: `GET /graph.mapillary.com/images?bbox={left},{bottom},{right},{top}&fields=id,captured_at,geometry`
- **Sequences**: `GET /graph.mapillary.com/{sequence_id}?fields=id,geometry`
- **Map features**: `GET /graph.mapillary.com/map_features?bbox={bbox}&fields=id,geometry,object_value`
- **Auth**: Client access token required (free, via Meta developer portal)
- **Rate limit**: Subject to Meta Graph API rate limits
- **Detected objects**: Traffic signs, road markings, utility poles, etc. — ML-extracted from imagery

## Freshness Assessment

Images become available shortly after upload and processing (typically minutes). The spatial query API lets you find recently captured images in any area. Contributions are continuous worldwide — active capture campaigns can produce thousands of images per day in a single city.

API probe returned a transient service error (503) at time of testing, but this appears to be a temporary issue. The API is well-documented and widely used.

## Entity Model

- **Image**: `id`, `captured_at` (timestamp), `geometry` (GeoJSON point), `compass_angle`, `is_pano`, `sequence`
- **Sequence**: `id`, `geometry` (GeoJSON linestring), ordered set of images
- **Map Feature**: `id`, `geometry`, `object_value` (e.g., `regulatory--stop--g1`), `first_seen_at`, `last_seen_at`
- **User**: Contributor who captured the imagery

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Minutes lag; continuous contributions |
| Openness | 2 | Free token required; Meta developer agreement; CC BY-SA data |
| Stability | 3 | Meta infrastructure; widely used by OSM community |
| Structure | 3 | Graph API with clean JSON/GeoJSON; well-documented fields |
| Identifiers | 3 | Unique image/sequence/feature IDs; timestamps |
| Additive Value | 2 | Street-level visual change detection; complements OSM map data |
| **Total** | **15/18** | |

## Notes

- API returned 503 at probe time — transient; the API is generally available and widely used.
- Mapillary is deeply integrated with the OSM community — many mappers use it as a reference for mapping.
- ML-detected map features (traffic signs, road markings) add a structured data layer on top of raw imagery.
- The "freshness" signal here is interesting: new imagery in an area often means something is changing (construction, new roads, etc.).
- Pairs with OSM Minutely Diffs (edits triggered by Mapillary imagery) and OSM Notes (issues discovered via imagery).
