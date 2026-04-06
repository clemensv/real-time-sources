# OpenAddresses

**Country/Region**: Global
**Publisher**: OpenAddresses community
**API Endpoint**: `https://batch.openaddresses.io/api/data`
**Documentation**: https://openaddresses.io/
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON (metadata), CSV (address data)
**Update Frequency**: Batch processing — sources are re-crawled periodically (days to weeks)
**License**: Varies by source (most CC0 or public domain); aggregation is open

## What It Provides

OpenAddresses is a global collection of address point data — street addresses with geographic coordinates, collected from authoritative open data sources (government open data portals, postal services, etc.). The project crawls and normalizes address data from thousands of sources worldwide into a consistent format: street number, street name, city, region, postcode, latitude, longitude.

The batch API provides metadata about processing runs, source status, and download links for processed address data.

## API Details

- **Data listing**: `GET /api/data` — list of processed data sources with metadata
- **Response fields**: `id`, `source` (path like `ae/az/drm-ar`), `layer` (addresses/buildings/parcels), `updated` (timestamp), `size`, `output` (cache, pmtiles, preview, validated flags)
- **Download**: Processed CSV files available via the output URLs
- **Job tracking**: `job` field links to the processing run
- **No auth required**: Public API
- **Layers**: `addresses`, `buildings`, `parcels`

## Freshness Assessment

OpenAddresses operates on a batch crawl cycle — sources are re-processed periodically. The `updated` timestamp indicates when a source was last processed. This is not a real-time stream; it's a continuously-refreshed snapshot of global address data. For detecting new address data (new developments, re-zoning), the update cadence is days to weeks.

Confirmed live: API returned entries with `updated` timestamps from recent processing runs.

## Entity Model

- **Source**: Hierarchical path (country/region/source), layer type, processing status
- **Address record**: `LON`, `LAT`, `NUMBER`, `STREET`, `UNIT`, `CITY`, `DISTRICT`, `REGION`, `POSTCODE`, `HASH`, `ID`
- **Processing job**: `id`, status, timestamps

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Batch processing, days-to-weeks cycle |
| Openness | 3 | No auth, open API, mostly CC0 data |
| Stability | 2 | Community project; smaller than OSM |
| Structure | 3 | Clean JSON API, standardized CSV output |
| Identifiers | 2 | Source paths, record IDs, processing job IDs |
| Additive Value | 2 | Unique normalized global address dataset |
| **Total** | **13/18** | |

## Notes

- Confirmed live: API returned metadata for processed address sources.
- The batch nature makes this less exciting for real-time use cases, but it's a valuable reference dataset.
- Address data is inherently less volatile than map geometry — addresses change slowly.
- The normalization across thousands of heterogeneous government data sources is the real value.
- Pairs with OSM (which has addresses too, but less authoritative) and geocoding services.
