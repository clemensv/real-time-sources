# iNaturalist

**Country/Region**: Global
**Publisher**: California Academy of Sciences / National Geographic
**API Endpoint**: `https://api.inaturalist.org/v1/`
**Documentation**: https://api.inaturalist.org/v1/docs/
**Protocol**: REST (JSON)
**Auth**: None (read), OAuth2 (write)
**Data Format**: JSON
**Update Frequency**: Real-time — observations available within seconds of upload
**License**: Mixed per observation (CC0, CC-BY, CC-BY-NC); metadata is open

## What It Provides

iNaturalist is the world's largest biodiversity observation platform, with over 335 million observations (confirmed via API probe). Users photograph plants, animals, fungi, and other organisms; community identification and machine learning drive species-level identification. Observations that reach "Research Grade" (community consensus on ID with photo evidence) feed directly into GBIF and scientific databases.

The API exposes a real-time stream of these observations — every snake spotted, every mushroom photographed, every bird identified, timestamped and geolocated. This is an extraordinary planetary-scale biodiversity monitoring network.

## API Details

- **Observations**: `GET /v1/observations?per_page={n}&order=desc&order_by=created_at` — latest observations
- **Filtering**: `taxon_id`, `place_id`, `quality_grade` (research/needs_id/casual), `d1`/`d2` (date range), `geo=true`, `iconic_taxa`
- **Taxon search**: `GET /v1/taxa?q={name}` — search for species/taxa
- **Places**: `GET /v1/places/autocomplete?q={name}` — geographic filtering
- **Pagination**: `per_page` (max 200), `page`, `id_above`/`id_below` for cursor-based paging
- **No auth for reads**: Completely open API
- **Rate limit**: Documented as "please be reasonable"; ~100 requests/minute appears safe
- **Response size**: Total results count returned with each query (335M+ as of April 2026)

## Freshness Assessment

Observations appear in API results within seconds of upload. The `order_by=created_at&order=desc` pattern gives you a near-real-time feed of new observations. Cursor-based pagination via `id_above` enables efficient polling without missing observations.

Confirmed live: latest observation at probe time was created at 2026-04-06T13:15:33, less than 2 minutes before the query.

## Entity Model

- **Observation**: `id` (integer), `species_guess`, `quality_grade`, `observed_on`, `created_at`, `place_guess`, `location` (lat,lng), `uri`
- **Taxon**: `id`, `name`, `preferred_common_name`, `rank`, `iconic_taxon_name`, `ancestry`
- **User**: `id`, `login`, `name`, `observations_count`
- **Identification**: `id`, `taxon`, `user`, `created_at`, `current` (boolean)
- **Photo**: `id`, `url` (multiple sizes), `license_code`

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Seconds-old observations accessible via API |
| Openness | 3 | No auth for reads, well-documented API |
| Stability | 3 | Major platform backed by Cal Academy + NatGeo, API v1 stable for years |
| Structure | 3 | Rich JSON with nested taxon, user, photo objects |
| Identifiers | 3 | Integer IDs for all entities, stable URIs |
| Additive Value | 3 | Unique planetary-scale biodiversity monitoring — nothing else like it |
| **Total** | **18/18** | |

## Notes

- This is a standout source. 335 million observations and growing rapidly.
- Research Grade observations feed into GBIF — this is real science infrastructure.
- Taxonomic hierarchy is deep and well-structured (kingdom → phylum → class → order → family → genus → species).
- Machine learning model (`vision`) provides initial ID suggestions; community consensus confirms.
- Spatial queries supported: `lat`, `lng`, `radius` parameters.
- Pairs beautifully with eBird for birds specifically, but iNaturalist covers *all* of life.
