# IOC Sea Level Station Monitoring Facility (SLSMF)

**Country/Region**: Global (~1,000 stations worldwide)
**Publisher**: UNESCO Intergovernmental Oceanographic Commission (IOC), hosted by Flanders Marine Institute (VLIZ, Belgium)
**API Endpoint**: `https://api.ioc-sealevelmonitoring.org/v2/`
**Documentation**: https://github.com/SLSMF/API-Documentation / https://api.ioc-sealevelmonitoring.org/v2/doc
**Protocol**: REST (OpenAPI / Slim Framework)
**Auth**: API Key (free registration required)
**Data Format**: JSON, XML, CSV, ASCII
**Update Frequency**: Real-time (minutes-level, varies by station)
**License**: Open data; registration required for API access

## What It Provides

Global real-time sea level observations from tide gauge networks worldwide. The SLSMF aggregates data from GLOSS Core stations and other national tide gauge networks via the Global Telecommunication System (GTS) and direct HTTP/FTP feeds. Approximately 1,000 stations across all ocean basins. The V2 API (launched 2025) adds automated quality-controlled research data with daily QC processing.

Key data types:
- Raw real-time sea level readings (relative, not datum-referenced)
- Station metadata (name, lat/lon, operator, sensor types)
- Sea Level Station Catalogue (SSC) cross-referencing identifiers across GLOSS data centers
- Research-quality QC'd data (V2) with completeness/distinctness/shift flags

## API Details

**V1 endpoints** (legacy):
- `GET /v1/stationlist` — list all stations with metadata
- `GET /v1/data?code={code}&start={date}&end={date}` — retrieve sea level data (30-day / 150k record limit)

**V2 endpoints** (current, OpenAPI):
- `GET /v2/stations` — list stations with lat, lon, operator info
- `GET /v2/stations/{code}` — single station metadata
- `GET /v2/stations/{code}/data` — real-time sea level data
- `GET /v2/research/stations/{code}` — QC'd research data with flags
- `GET /v2/countries` — list by country
- `GET /v2/catalogue` — SSC catalogue entries

Data query parameters: `start`, `end`, `includesensors[]`, `format`, `skip_gaps_until`, `nofilter`.

Response includes: timestamp (ISO 8601), sea level value (mm), sensor type (rad/prs/flt/enc/bwl), QC flags (V2 research).

## Freshness Assessment

Excellent. Data streams in near-real-time from operational tide gauges worldwide. Most stations report at 1–6 minute intervals. The V2 research endpoint applies daily automated QC. The facility has been operational since the early 2000s and is actively maintained with updates as recent as February 2026.

## Entity Model

- **Station**: code, name, latitude, longitude, country, operator
- **Sensor**: sensorId, sensorType (rad=radar, prs=pressure, flt=float, enc=encoder, bwl=bubbler), sample rate
- **Observation**: timestamp, sea level value (mm, relative), QC flags
- **SSC Entry**: mappings to GLOSS, PTWC, and other data center IDs

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, minutes-level updates |
| Openness | 2 | Free but requires API key registration |
| Stability | 3 | UNESCO/IOC-backed, operational since ~2003, V2 launched 2025 |
| Structure | 3 | Clean REST API with OpenAPI spec, JSON/CSV output |
| Identifiers | 3 | SSC catalogue cross-references GLOSS, PTWC, national IDs |
| Additive Value | 3 | ~1,000 global stations not covered by any single national feed |
| **Total** | **17/18** | |

## Notes

- This is the single most comprehensive global real-time tide gauge aggregator. It covers stations that would otherwise require dozens of national APIs.
- Data is relative (not datum-referenced). For absolute MSL, users must contact station operators or use PSMSL.
- The V2 research endpoint is a major differentiator — automated daily QC with spike removal, completeness checking, and shift detection.
- 30-day query limit per request; pagination via date ranges needed for longer series.
- The SSC (Sea Level Station Catalogue) is invaluable for cross-referencing station identifiers between different data centers.
