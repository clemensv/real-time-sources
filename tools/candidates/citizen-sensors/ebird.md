# eBird

**Country/Region**: Global
**Publisher**: Cornell Lab of Ornithology
**API Endpoint**: `https://api.ebird.org/v2/`
**Documentation**: https://documenter.getpostman.com/view/664302/S1ENwy59
**Protocol**: REST (JSON)
**Auth**: API Key (free, requires eBird account)
**Data Format**: JSON
**Update Frequency**: Near real-time — observations available within minutes of checklist submission
**License**: eBird Terms of Use (free for non-commercial use; commercial requires agreement)

## What It Provides

eBird is the world's largest biodiversity-related citizen science project, specifically focused on birds. Birders worldwide submit checklists — structured observation records that include species seen, counts, location, date, time, duration, and effort. The result is a continuous, planet-wide monitoring network for avian biodiversity that generates over 200 million observations per year.

The eBird API 2.0 provides access to recent observations, notable sightings, hotspot data, and regional species lists. The "recent observations" endpoints effectively function as a near-real-time bird sighting feed.

## API Details

- **Recent observations**: `GET /v2/data/obs/{regionCode}/recent?maxResults={n}` — latest sightings in a region
- **Notable sightings**: `GET /v2/data/obs/{regionCode}/recent/notable` — rare/unusual species
- **Nearby recent**: `GET /v2/data/obs/geo/recent?lat={lat}&lng={lng}&dist={km}` — observations near a point
- **Species recent**: `GET /v2/data/obs/{regionCode}/recent/{speciesCode}` — recent sightings of a specific species
- **Hotspots**: `GET /v2/ref/hotspot/{regionCode}` — popular birding locations
- **Taxonomy**: `GET /v2/ref/taxonomy/ebird?fmt=json` — full eBird taxonomy
- **Auth**: `X-eBirdApiToken` header with free API key
- **Rate limit**: Not explicitly documented; reasonable use expected
- **Region codes**: eBird uses ISO country/subnational codes (e.g., `US-NY`, `GB-ENG`)

## Freshness Assessment

Observations become available shortly after a birder submits their checklist — typically within minutes. The "recent" endpoints return observations from the last 1-30 days (configurable via `back` parameter). For active birding hours, new data flows in continuously.

eBird's API requires an API key (free, instant approval), so it's not zero-auth, but the barrier is minimal.

## Entity Model

- **Observation**: `speciesCode`, `comName`, `sciName`, `locId`, `locName`, `obsDt`, `howMany`, `lat`, `lng`, `subId` (checklist ID)
- **Location**: `locId`, `locName`, `lat`, `lng`, `countryCode`, `subnational1Code`
- **Species**: `speciesCode`, `comName`, `sciName`, `familySciName`, `order`, `category`
- **Checklist**: `subId`, observer info, effort metrics (duration, distance, area)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Minutes lag from checklist submission to API availability |
| Openness | 2 | Free API key required; non-commercial use terms |
| Stability | 3 | Cornell Lab infrastructure, API v2 stable for years |
| Structure | 3 | Clean JSON, consistent schema, taxonomic backbone |
| Identifiers | 3 | Species codes (eBird taxonomy), location IDs, checklist IDs |
| Additive Value | 3 | Unmatched global bird monitoring — 200M+ observations/year |
| **Total** | **17/18** | |

## Notes

- API key is free and instant — register at ebird.org, request key in account settings.
- Confirmed: API returns 403 without key, meaning the auth gate is real but permissive.
- The "notable sightings" endpoint is particularly interesting — it flags species that are rare for a given region/time, essentially surfacing anomalous biodiversity events.
- eBird Status and Trends provides modeled abundance data, but that's a separate product (bulk download, not API).
- eBird data powers significant conservation research and policy decisions.
- Pairs naturally with iNaturalist (broader taxa) and weather data (migration correlates with weather patterns).
